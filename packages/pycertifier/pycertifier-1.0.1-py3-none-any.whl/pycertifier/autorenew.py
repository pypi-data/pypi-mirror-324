from time import sleep
from os import listdir, fork, path
from lockfile.pidlockfile import PIDLockFile
from signal import SIGINT, SIGHUP, signal
from functools import partial
from textwrap import dedent
import base64
import logging
import re
import sys

sys.path.append('..')

from .certifier import (
    certifier_new, certifier_set_property, certifier_get_property,
    certifier_get_device_certificate_status, certifier_get_device_registration_status,
    certifier_renew_certificate, certifier_setup_keys, certifier_create_x509_crt, Certifier
)
from .property import get_default_cfg_filename
from .constants import (
    CERTIFIER_OPT, CERTIFIER_ERR_GET_CERT_STATUS_GOOD, CERTIFIER_ERR_GET_CERT_STATUS_REVOKED,
    CERTIFIER_ERR_GET_CERT_STATUS_UNKNOWN, CERTIFIER_ERR_REGISTRATION_STATUS_CERT_ABOUT_TO_EXPIRE,
    CERTIFIER_ERR_REGISTRATION_STATUS_CERT_EXPIRED_1, CERTIFIER_ERR_REGISTRATION_STATUS_CERT_EXPIRED_2
)

counter = 1
ignore_list = []
key_lookup = {}
pid_file = None
daemon_logger = None
attempt_threshold = 3

LEVELS = {
    1: "DEBUG",
    2: "WARN",
    3: "INFO",
    4: "ERROR",
}

def shutdown():
    '''Terminates program gracefully. Releases PIDLockFile if possible and exits.'''
    global daemon_logger, pid_file

    if pid_file:
        try:
            daemon_logger.info(f"Attempting to release lockfile '{pid_file.unique_name}'...")
            pid_file.release()
            daemon_logger.info(f"Release succeeded. Exiting...")
        except Exception as e:
            daemon_logger.error(f"Failed to release '{pid_file.unique_name}' during shutdown. Exception was: {e}")
    exit()
    
def handle_signal(signal, frame, certifier, cfg):  
    '''Handles SIGINT (stops daemon) and SIGHUP (reloads config) signals to process'''
    global pid_file, daemon_logger

    if signal == SIGINT:
        daemon_logger.info("Stopping daemon...\n")
        shutdown()
    elif signal == SIGHUP:        
        config_file = cfg or get_default_cfg_filename()  
        daemon_logger.info(f"Reloading daemon config file '{path.expanduser(config_file)}'...\n")    
        certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CFG_FILENAME, path.expanduser(config_file))

def setup_logging(args):
    ''' Sets up logger. Outputs to stdout if no log file path is provided via command line.'''
    global daemon_logger
    daemon_logger = logging.getLogger('Daemon')
    
    handler = logging.StreamHandler(sys.stdout) if args.log_file is None else logging.FileHandler(args.log_file.name)

    logging.basicConfig(
    handlers=[handler],
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    for level, name in LEVELS.items():
        logging.addLevelName(level, name)

    daemon_logger.setLevel(logging.DEBUG)
    
    return daemon_logger
    
def refresh_list_of_certificates(cert_dir_list):
    '''Checks the specified path for list of certificates to autorenew. Returns list with file names'''    
    global pid_file, daemon_logger
    
    list_of_certificates = []

    for dir in cert_dir_list:               
        if not path.isdir(dir):
            daemon_logger.error(f"{dir} is not a directory!")
            shutdown()
        
        files = [dir + "/" + file for file in listdir(dir) if path.isfile(dir + "/" + file)]

        for file in files:
            if file.endswith('.p12'):
                list_of_certificates.append(file)
            
    return list_of_certificates

def check_ignore_list(list_of_certificates, daemon_toggled):
    '''Returns the difference between the detected certificate list and certificates in ignore list'''
    global ignore_list, attempt_threshold
    
    list_of_certificates = list(set(list_of_certificates) - set(ignore_list))
        
    if list_of_certificates == []:
        daemon_logger.info("There are no certificates deemed valid to renew in the target directory.\n")
        
        if daemon_toggled:
            attempt_threshold -= 1
            
            if attempt_threshold > 0:
                daemon_logger.info(f'Returning. Will check {attempt_threshold} more times before exiting.')
                return []
            else:
                daemon_logger.info(f'Reached attempt threshold.')
                shutdown()
        else:
            daemon_logger.info('Exiting')
            shutdown()
    
    return list_of_certificates
            
def try_renew_certificates(certifier: Certifier, list_of_certificates, daemon_toggled: bool):
    '''Iterates through list of detected certificates. Checks status and validity before calling renew_certificate() helper to attempt renewal.'''
    global ignore_list, key_lookup, daemon_logger, attempt_threshold
        
    list_of_certificates = check_ignore_list(list_of_certificates, daemon_toggled)
    
    if list_of_certificates == []:
        return
        
    for cert in list_of_certificates:        
        status = "Status: Did not check"
        validity = "Validity: Did not check"
        renew_result = "Result: Did not attempt renewal"

        certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH, cert)
        
        ignore_msg = "Ignoring certificate from now on." if daemon_toggled else ""
        
        if key_lookup.get(cert) is None:
            daemon_logger.info(dedent(
                    f'''
                    -------------------------
                    Attempting to renew {cert}
                    
                    Key was not specified or recognized in key list. {ignore_msg}
                    
                    {status}
                    {validity}
                    {renew_result}
                    -------------------------
                   '''))
            ignore_list.append(cert)
            continue
                
        certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD, key_lookup.get(cert))

        certifier_get_device_certificate_status(certifier, True)

        certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PATH, cert)
        
        if certifier.last_error.application_error_code != 0:
            msg = certifier.last_error.application_error_msg['message']
            
            daemon_logger.error(dedent(
                                f'''
                                -------------------------
                                Attempting to renew {cert}
                                
                                Issue checking certificate status while attempting renewal. {ignore_msg}
                                    Message: {msg}
                                    
                                {status}
                                {validity}
                                {renew_result}
                                -------------------------
                                 '''))            
            
            ignore_list.append(cert)
            continue
        
        can_renew = False
        
        status = certifier.last_error.output
        
        match status:
            case value if value == CERTIFIER_ERR_GET_CERT_STATUS_GOOD:
                status = "Status: Good"
                can_renew = True
            case value if value == CERTIFIER_ERR_GET_CERT_STATUS_REVOKED:
                status = "Status: Revoked. Not renewing it."
            case value if value == CERTIFIER_ERR_GET_CERT_STATUS_UNKNOWN:
                status = "Status: Unknown. Not renewing it."

        certifier.last_error.clear()
        
        if can_renew:    
            certifier_get_device_registration_status(certifier, True)
                            
            validity = certifier.last_error.output
            
            match validity:
                case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_CERT_EXPIRED_1:
                    validity = "Validity: Not yet valid. Not renewing it."
                    can_renew = False
                case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_CERT_EXPIRED_2:
                    validity = "Validity: Expired. Not renewing it."
                    ignore_list.append(cert)
                    can_renew = False
                case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_CERT_ABOUT_TO_EXPIRE:
                    validity = "Validity: About to Expire"

            certifier.last_error.clear()

        renew_result = "Result: Failed to be renewed"

        if can_renew:
            result = renew_certificate(certifier)
            
            if result is None:
                renew_result = "Result: Successfully renewed"
            else:
                ignore_list.append(cert)
                daemon_logger.error(dedent(
                                    f'''
                                    -------------------------
                                    Attempting to renew {cert}
                                    
                                    Issue attempting renewal. {ignore_msg}
                                        Message: {result.application_error_msg['message']}
                                        HTTP Response: {result.application_error_msg['http_response']}
                                        
                                    {status}
                                    {validity}
                                    {renew_result}
                                    -------------------------
                                    '''))            
                continue
        
        daemon_logger.info(dedent(
                                f'''
                                -------------------------
                                Attempting to renew {cert}
                                
                                {status}
                                {validity}
                                {renew_result}
                                -------------------------
                                 '''))
        
        daemon_logger.parent.handlers[0].flush()

def renew_certificate(certifier: Certifier):
    '''Makes calls to helpers to set up keys and create CRT for renewal attempt. Calls certifier_renew_certificate() to perform renewal.'''
    certifier_setup_keys(certifier)
    
    crt = certifier_create_x509_crt(certifier, True)

    crt = base64.b64encode(crt.encode('utf-8')).decode('utf-8')
        
    certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CRT, crt)
    
    return certifier_renew_certificate(certifier)             

def start_autorenew(args):
    '''Forks to create daemon process and PID lock file if daemon mode specified. Calls process() for next steps.'''
    try:
        global daemon_logger, pid_file
        
        if args.daemon:       
            if args.pid_file is None:
                print("PID file required! Use '-p' option to specify path")      
                exit()
            
            n = fork()
            
            if n > 0:
                exit()
            
            pid_file = PIDLockFile(args.pid_file)
                        
            if pid_file.is_locked():
                print(f"PID lock exists, process already running with PID: {pid_file.read_pid()}")
                exit()  
            
            daemon_logger = setup_logging(args)

            pid_file.acquire()
            
            daemon_logger.info(f"Lock acquired. PID: {pid_file.read_pid()}\n")
            
            process(args)     
            
        else:
            daemon_logger = setup_logging(args)
            process(args)
    except Exception as e:
        print(f"Ran into an error. Exception was {e}")
        shutdown()
            
def process(args):
    '''Creates certifier instance, sets up signal handling, and processes command line arguments. Outlines main renewal procedure.'''
    global daemon_logger, pid_file, counter, key_lookup, attempt_threshold, handle_signal
        
    running = True
    
    certifier = certifier_new(args, 'xpki')
    
    handle_signal = partial(handle_signal, certifier=certifier, cfg=args.config)
    signal(SIGINT, handle_signal)
    signal(SIGHUP, handle_signal)
    
    if certifier is not None:
        certifier_set_property(certifier,CERTIFIER_OPT.CERTIFIER_OPT_CFG_FILENAME, args.config or get_default_cfg_filename())
        
        if args.cert_paths:
            dirs = [path.abspath(dir) for dir in args.cert_paths.split(':')]
                    
            certifier_set_property(certifier,CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_CERTS_PATH_LIST, dirs)
            
        if args.autorenew_interval:
            certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_INTERVAL, args.autorenew_interval)

        attempt_threshold = args.attempt_threshold

        while running == True:
            try:
                daemon_logger.parent.handlers[0].flush()
                daemon_logger.info(f"Iteration #{counter}")
            except Exception as e:
                daemon_logger.error(f"Issue with log stream log stream, error: {str(e)}")
            
            counter += 1

            cert_dir_list = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_CERTS_PATH_LIST)
            
            list_of_certificates = refresh_list_of_certificates(cert_dir_list)
            
            if args.key_list:
                with open(path.expanduser(args.key_list), 'r') as file:
                    pattern = r"^[^:]+:[^:]+$"
                    key_lookup = {path.expanduser(cert): pwd.strip() for cert, pwd in (line.split(':') for line in file if re.match(pattern, line))}
                    
                    for cert in key_lookup.keys():
                        if not path.isfile(cert) or not cert.endswith('.p12'):
                            daemon_logger.error(f"Check that '{cert}' in argument to '--key-list/-k' is a valid .p12 file")
                            shutdown()       
            
            list_of_certificates = list(set(list_of_certificates) - set(ignore_list))

            formatted_certificate_list = '\n' + '\n'.join(list_of_certificates) if list_of_certificates != [] else 'None'
            formatted_ignore_list = '\n' + '\n'.join(ignore_list) if ignore_list != [] else 'None'            
            
            daemon_logger.info(f"Scanning these directories {cert_dir_list}")
            daemon_logger.info(f"Certificates detected: {formatted_certificate_list}\n")
            daemon_logger.info(f"Certificates ignored: {formatted_ignore_list}\n")

            try_renew_certificates(certifier, list_of_certificates, args.daemon)

            if args.daemon:
                delay = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_INTERVAL)
                daemon_logger.info(dedent(
                    f'''
                    Going to sleep. Attempting autorenewal again in {delay} seconds
                    
                    =====================================================================================================================================
                    '''))
                sleep(delay)
            else:
                running = False
                daemon_logger.info(dedent(
                    f'''
                    Finished batch renewal. Exiting...
                    
                    =====================================================================================================================================
                    '''
                ))

if __name__ == '__main__':
    start_autorenew()