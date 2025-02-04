from .cli import cli_setup
from .log import log_setup, log_destroy, Namespace
from .xpki_client import *
from .certifier import Certifier, certifier_get_property, certifier_create_info, get_last_error, certifier_get_node_address
from .constants import CERTIFIER_OPT, SECTIGO_OPT
from .sectigo import sectigo_get_cert, sectigo_search_cert, sectigo_renew_cert, sectigo_revoke_cert
from .autorenew import start_autorenew

import sys, os

def main():
    try:
        arg_parser = cli_setup()
        args = arg_parser.parse_args(sys.argv[1:] or ['--help'])
    
        # Autorenew command has logging configuration that deviates (handled in autorenew.py)
        if args.command != 'autorenew':
            log_setup(args)
        
        xpki_perform(args)
    finally:
        log_destroy()

def update(args, params):
    ''' 
    Update params with common attributes from args. Sets attribute values in params to corresponding values in args
    '''
    for key in vars(params).keys():
        if key in vars(args).keys() and getattr(args, key) is not None:
            setattr(params, key, getattr(args, key))

            log(f"Loaded {key} value: '{getattr(args, key)}' from args", "DEBUG")
    
    log("---------- FINISHED LOADING ARGUMENTS FROM COMMAND LINE ----------\n", "DEBUG")

def process(certifier: Certifier, args: Namespace, params: get_cert_param_t | get_cert_status_param_t | get_cert_validity_param_t | renew_cert_param_t): 
    if isinstance(params, get_cert_param_t):
        if certifier.cert_type == 'xpki':
            xc_get_default_cert_param(certifier, params)

            update(args, params)
            
        elif certifier.cert_type == 'sectigo':
            update(args, params)
        
    elif isinstance(params, get_cert_validity_param_t) or isinstance(params, print_cert_param_t) or isinstance(params, revoke_cert_param_t):
        if certifier.cert_type == 'xpki':
            xc_get_default_cert_validity_param(certifier, params)
            
            update(args, params)
        elif certifier.cert_type == 'sectigo':
            update(args, params)

    elif isinstance(params, renew_cert_param_t):
        if certifier.cert_type == 'xpki':
            xc_get_default_renew_cert_param(certifier, params)

            update(args, params)
            
            if params.auth_type == None:
                params.auth_type = "X509"
                        
            params.auth_type = map_to_xpki_auth_type(params.auth_type)

        elif certifier.cert_type == 'sectigo':
            update(args, params)
    elif isinstance(params, get_cert_status_param_t):
        xc_get_default_cert_status_param(certifier, params)

        update(args, params)

    elif isinstance(params, search_cert_param_t):
        update(args, params)
        
def xpki_perform(args):
    if (args.command == 'autorenew'):
        start_autorenew(args)    
            
    cert_type = os.environ.get('CERT_TYPE').lower()
    
    certifier = get_certifier_instance(args, cert_type)

    if (args.command == 'get-cert'):
        params = get_cert_param_t(cert_type)
        process(certifier, args, params)
                
        if cert_type == 'xpki':
            xc_get_cert(certifier, params)
            output = str(certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CERT_X509_OUT))
        elif cert_type == 'sectigo':
            sectigo_get_cert(certifier, params)
            output = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERT_OUTPUT)
        
        last_error = get_last_error(certifier)
        return_code = last_error.application_error_code
        
        return certifier_create_info(last_error, return_code, output)        

    if (args.command == 'renew-cert'):
        params = renew_cert_param_t(cert_type)
        process(certifier, args, params)

        if cert_type == 'xpki':
            xc_renew_cert(certifier, params)
            output = certifier_get_node_address(certifier)
        elif cert_type == 'sectigo':
            sectigo_renew_cert(certifier, params)
            output = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERT_OUTPUT)
            
        last_error = get_last_error(certifier)
        return_code = last_error.application_error_code
        
        return certifier_create_info(last_error, return_code, output)

    if (args.command == 'revoke-cert'):
        params = revoke_cert_param_t(cert_type)
        process(certifier, args, params)

        if cert_type == 'xpki':
            xc_revoke_cert(certifier, params)
            output = certifier_get_node_address(certifier)
        elif cert_type == 'sectigo':
            sectigo_revoke_cert(certifier, params)
            output = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERT_OUTPUT)

        last_error = get_last_error(certifier)
        return_code = last_error.application_error_code
        
        return certifier_create_info(last_error, return_code, output)

    if (args.command == 'get-crt-token'):
        params = renew_cert_param_t(cert_type)
        process(certifier, args, params)
                                
        xc_create_crt(certifier, params.auth_type, params, False)
        last_error = get_last_error(certifier)
        return_code = last_error.application_error_code
        
        return certifier_create_info(last_error, return_code, certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CRT))
        
    if (args.command == 'get-cert-status'):
        params = get_cert_status_param_t(cert_type)
        process(certifier, args, params)
        status: XPKI_CLIENT_CERT_STATUS = None

        status = xc_get_cert_status(certifier, params)
        last_error = get_last_error(certifier)
        return_code = last_error.application_error_code

        return certifier_create_info(last_error, return_code, XPKI_CLIENT_CERT_STATUS(status).name)

    if (args.command == 'get-cert-validity'):
        params = get_cert_validity_param_t(cert_type)
        process(certifier, args, params)
        validity: XPKI_CLIENT_CERT_STATUS = None
                
        validity = xc_get_cert_validity(certifier, params)
        last_error = get_last_error(certifier)
        return_code = last_error.application_error_code

        return certifier_create_info(last_error, return_code, XPKI_CLIENT_CERT_STATUS(validity).name)
        
    if (args.command == 'print-cert'):
        params = print_cert_param_t(cert_type)
        process(certifier, args, params)
        
        b64_der_cert = xc_print_cert(certifier, params)
        last_error = get_last_error(certifier)
        return_code = last_error.application_error_code

        return certifier_create_info(last_error, return_code, b64_der_cert) 

    if (args.command == 'search-cert'):
        params = search_cert_param_t(cert_type)
        process(certifier, args, params)
        
        sectigo_search_cert(certifier, params)
        last_error = get_last_error(certifier)
        return_code = last_error.application_error_code
        
        return certifier_create_info(last_error, return_code, certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERT_OUTPUT))    

if __name__ == '__main__':
    main()