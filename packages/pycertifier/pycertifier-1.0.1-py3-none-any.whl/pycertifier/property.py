
from .error import CertifierError, gen_application_error_msg, certifier_create_info
from .log import log, cfg
from .constants import *

from dataclasses import dataclass
from importlib import resources
import json
import secrets

ca_path_order_list = [DEFAULT_CA_PATH, DEFAULT_USER_CA_PATH, DEFAULT_GLOBAL_CA_PATH, DEFAULT_CURDIR_CA_PATH]

def get_default_cfg_filename():
    '''
    Function to find config file to use by default if not provided on command line
    
    Returns default config filename to use on success
    
    Program exits and reports an error with property-related code mapping on failure
    '''
    path = None

    with resources.path('pycertifier.resources', 'pycertifier.cfg') as cfg_path:
        path = str(cfg_path)

    if (path is None):
        log("Could not resolve default config filename", "ERROR")
        error_message = gen_application_error_msg("Could not resolve default configuration filename", None)
        rc = CertifierError(9, 0, error_message, None)
        certifier_create_info(rc, property_error + 9, None)
    
    return path

def get_default_ca_info():
    '''
    Function to find CA info to use by default
    
    Returns default CA info to use on success
    
    Program exits and reports an error with property-related code mapping on failure
    '''
    path = None

    with resources.path('pycertifier.resources', 'pycertifier-cert.crt') as ca_info_path:
        path = str(ca_info_path)

    if (path is None):
        log("Could not resolve default CA info", "ERROR")
        error_message = gen_application_error_msg("Could not resolve default CA info", None)
        rc = CertifierError(10, 0, error_message, None)
        certifier_create_info(rc, property_error + 10, None)

    return path

def get_default_ca_path():
    '''
    Function to find CA path to use by default if not provided on command line
    
    Returns default CA path to use on success
    
    Program exits and reports an error with property-related code mapping on failure
    '''
    ca_path = None
    
    for opt in ca_path_order_list:
        if (os.path.exists(opt)):
            ca_path = opt
            break

    if (ca_path is None):
        log("Could not resolve default CA path", "ERROR")
        error_message = gen_application_error_msg("Could not resolve default CA path", None)
        rc = CertifierError(11, 0, error_message, None)
        certifier_create_info(rc, property_error + 11, None)

    return ca_path

def print_warning(property_name: str):
    '''
    Print warning that given property shouldn't be used in production.
    '''
    log("WARNING! Property key: " + str(property_name) + " should not be used in PRODUCTION. It could cause security-related issues.", "INFO")

@dataclass
class CertifierPropMap():
    def __init__(self, cert_type):
        if cert_type == 'xpki':
            self.log_level: int = None
            self.log_max_size: int = None
            self.http_connect_timeout: int = None
            self.http_timeout: int = None
            self.options: int = 0
            self.cert_min_time_left_s: int = None
            self.validity_days: int = None
            self.autorenew_interval: int = None
            self.log_file: str = None
            self.ca_info: str = None
            self.ca_path: str = None
            self.certifier_url: str = None
            self.cfg_filename: str = None
            self.auth_type: str = None
            self.p12_filename: str = None
            self.output_p12_filename: str = None
            self.password: str = None
            self.password_out: str = None
            self.certifier_id: str = None
            self.system_id: str = None
            self.mac_address: str = None
            self.dns_san: str = None
            self.ip_san: str = None
            self.email_san: str = None
            self.crt: str = None
            self.profile_name: str = None
            self.source: str = None
            self.cn_prefix: str = None
            self.domain: str = None
            self.ext_key_usage_value: str = None
            self.tracking_id: str = None
            self.ecc_curve_id: str = None
            self.auth_token: str = None 
            self.output_node: str = None
            self.target_node: str = None
            self.action: str = None
            self.input_node: str = None
            self.autorenew_certs_path_list: str = None
            self.cert_x509_out = None
            self.mtls_filename: str = None
            self.mtls_p12_filename: str = None
            self.verbose: bool = None
        elif cert_type == 'sectigo':
            self.sectigo_url: str = None
            self.auth_token: str = None
            self.cfg_filename: str = None
            self.verbose: bool = None
            self.common_name: str = None
            self.serial_number: str = None
            self.certificate_id: int = None
            self.requestor_email: str = None
            self.owner_last_name: str = None
            self.owner_first_name: str = None
            self.owner_phone_number: str = None
            self.owner_email: str = None
            self.group_name: str = None
            self.group_email: str = None
            self.id: str = None
            self.employee_type: str = None
            self.server_platform: str = None
            self.sensitive: str = None
            self.project_name: str = None
            self.business_justification: str = None
            self.subject_alt_names: str = None
            self.ip_addresses: str = None
            self.certificate_type: str = None
            self.status: str = None
            self.offset: str = None
            self.limit: str = None
            self.start_date: str = None
            self.end_date: str = None
            self.validity_start_date: str = None
            self.cert_order: str = None
            self.validity_end_date: str = None
            self.is_cn_in_san: str = None
            self.request_type: str = None
            self.timestamp: str = None
            self.revocation_request_reason: str = None
            self.log_level: int = None
            self.log_max_size: int = None
            self.options: int = 0
            self.output = None
            self.cfg_filename = None
            self.source: str = None

def property_new(cert_type):
    '''
    Constructs CertifierPropMap for certifier instance
    
    Returns CertifierPropMap on success
    
    Program exits and reports an error with certifier-related code mapping on failure
    '''
    prop_map = CertifierPropMap(cert_type)

    if (prop_map == None):
        log("CertifierPropMap was None after attempted initialization", "ERROR")
        rc = CertifierError(1, 0, gen_application_error_msg("CertifierPropMap was None after attempted initialization", None), None, None)
        certifier_create_info(rc, certifier_error + 1, None)

    if cert_type == 'xpki':
        xpki_property_set_defaults(prop_map)
    elif cert_type == 'sectigo':
        sectigo_property_set_defaults(prop_map)
    
    return prop_map

def property_get(cert_type, prop_map, name):
    if cert_type == 'xpki':
        xpki_property_get(prop_map, name)
    elif cert_type == 'sectigo':
        sectigo_property_get(prop_map, name)

def property_set(cert_type, prop_map, name, value):
    if cert_type == 'xpki':
        xpki_property_set(prop_map, name, value)
    elif cert_type == 'sectigo':
        sectigo_property_set(prop_map, name, value)

def xpki_property_get(prop_map: CertifierPropMap, name: CERTIFIER_OPT):
    '''
    Function to retrieve a given property from certifier instance's CertifierPropMap based on name passed in.
    
    Returns value associated with property name on success
    
    Program exits and reports an error with property-related code mapping on failure
    '''
    return_value = None

    if (name <= 0):
        log("invalid property [" + str(name) + "]", "ERROR")
        rc = CertifierError(3, None, gen_application_error_msg("Property name was <= 0", None))
        certifier_create_info(rc, property_error + 3, None)
    elif (name > max(CERTIFIER_OPT, key = lambda e: e.value)):
        log("invalid property [" + str(name) + "]", "ERROR")
        rc = CertifierError(4, None, gen_application_error_msg("Property name was > than max in CERTIFIER_OPT enum.", None))
        certifier_create_info(rc, property_error + 4, None)
    
    match(name):
        case CERTIFIER_OPT.CERTIFIER_OPT_CFG_FILENAME:
            return_value = prop_map.cfg_filename
        case CERTIFIER_OPT.CERTIFIER_OPT_CERT_X509_OUT:
            return_value = prop_map.cert_x509_out
        case CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TYPE:
            return_value = prop_map.auth_type
        case CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL:
            return_value = prop_map.certifier_url
        case CERTIFIER_OPT.CERTIFIER_OPT_HTTP_TIMEOUT:
            return_value = prop_map.http_timeout
        case CERTIFIER_OPT.CERTIFIER_OPT_HTTP_CONNECT_TIMEOUT:
            return_value = prop_map.http_connect_timeout
        case CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH:
            return_value = prop_map.p12_filename
        case CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PATH:
            return_value = prop_map.output_p12_filename
        case CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD:
            return_value = prop_map.password
        case CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PASSWORD:
            return_value = prop_map.password_out
        case CERTIFIER_OPT.CERTIFIER_OPT_CA_INFO:
            return_value = prop_map.ca_info
        case CERTIFIER_OPT.CERTIFIER_OPT_CA_PATH:
            return_value = prop_map.ca_path
        case CERTIFIER_OPT.CERTIFIER_OPT_CRT:
            return_value = prop_map.crt
        case CERTIFIER_OPT.CERTIFIER_OPT_PROFILE_NAME:
            return_value = prop_map.profile_name
        case CERTIFIER_OPT.CERTIFIER_OPT_ECC_CURVE_ID:
            return_value = prop_map.ecc_curve_id
        case CERTIFIER_OPT.CERTIFIER_OPT_OPTIONS:
            return_value = prop_map.options
        case CERTIFIER_OPT.CERTIFIER_OPT_SYSTEM_ID:
            return_value = prop_map.system_id
        case CERTIFIER_OPT.CERTIFIER_OPT_MAC_ADDRESS:
            return_value = prop_map.mac_address
        case CERTIFIER_OPT.CERTIFIER_OPT_DNS_SAN:
            return_value = prop_map.dns_san
        case CERTIFIER_OPT.CERTIFIER_OPT_IP_SAN:
            return_value = prop_map.ip_san
        case CERTIFIER_OPT.CERTIFIER_OPT_EMAIL_SAN:
            return_value = prop_map.email_san
        case CERTIFIER_OPT.CERTIFIER_OPT_LOG_LEVEL:
            return_value = prop_map.log_level
        case CERTIFIER_OPT.CERTIFIER_OPT_LOG_MAX_SIZE:
            return_value = prop_map.log_max_size
        case CERTIFIER_OPT.CERTIFIER_OPT_LOG_FILENAME:
            return_value = prop_map.log_file
        case CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TOKEN:
            return_value = prop_map.auth_token
        case CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_NODE:
            return_value = prop_map.output_node
        case CERTIFIER_OPT.CERTIFIER_OPT_TARGET_NODE:
            return_value = prop_map.target_node
        case CERTIFIER_OPT.CERTIFIER_OPT_ACTION:
            return_value = prop_map.action
        case CERTIFIER_OPT.CERTIFIER_OPT_INPUT_NODE:
            return_value = prop_map.input_node
        case CERTIFIER_OPT.CERTIFIER_OPT_TRACKING_ID:
            return_value = prop_map.tracking_id
        case CERTIFIER_OPT.CERTIFIER_OPT_SOURCE:
            return_value = prop_map.source
        case CERTIFIER_OPT.CERTIFIER_OPT_CN_PREFIX:
            return_value = prop_map.cn_prefix
        case CERTIFIER_OPT.CERTIFIER_OPT_DOMAIN:
            return_value = prop_map.domain
        case CERTIFIER_OPT.CERTIFIER_OPT_VALIDITY_DAYS:
            return_value = prop_map.validity_days
        case CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_INTERVAL:
            return_value = prop_map.autorenew_interval
        case CERTIFIER_OPT.CERTIFIER_OPT_CERT_MIN_TIME_LEFT_S:
            return_value = prop_map.cert_min_time_left_s
        case CERTIFIER_OPT.CERTIFIER_OPT_EXT_KEY_USAGE:
            return_value = prop_map.ext_key_usage_value
        case CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_CERTS_PATH_LIST:
            return_value = prop_map.autorenew_certs_path_list
        case CERTIFIER_OPT.CERTIFIER__OPT_LOG_FUNCTION:
            # Write-only value
            return_value = None
        case CERTIFIER_OPT.CERTIFIER_OPT_MTLS_P12_PATH:
            return_value = prop_map.mtls_filename
        case CERTIFIER_OPT.CERTIFIER_OPT_MTLS_P12_PASSWORD:
            return_value = prop_map.mtls_p12_filename
        case CERTIFIER_OPT.CERTIFIER_OPT_DEBUG_HTTP | CERTIFIER_OPT.CERTIFIER_OPT_TRACE_HTTP | CERTIFIER_OPT.CERTIFIER_OPT_FORCE_REGISTRATION | CERTIFIER_OPT.CERTIFIER_OPT_MEASURE_PERFORMANCE | CERTIFIER_OPT.CERTIFIER_OPT_CERTIFICATE_LITE | CERTIFIER_OPT.CERTIFIER_OPT_USE_SCOPES | CERTIFIER_OPT.CERTIFIER_OPT_VERBOSE: 
            bit = name - CERTIFIER_OPT.CERTIFIER_OPT_BOOL_FIRST
            option: CERTIFIER_OPT_OPTION = 1 << bit
            
            return_value = property_is_option_set(prop_map, option)                
        case _:
            log("property_get: unrecognized property [" + str(name) + "]", "WARN")
            rc = CertifierError(8, None, gen_application_error_msg("Attempted to set unrecognized property in property_get()", None))
            certifier_create_info(rc, property_error + 8, None)

    return return_value

def xpki_property_set(prop_map: CertifierPropMap, name: CERTIFIER_OPT, value):
    '''
    Function attempts to set certifier instance's CertifierPropMap property of type [name] with [value].
    
    Returns None on success
    
    Program exits and reports an error with property-related code mapping on failure
    '''
    rc = CertifierError()

    match(name):
        case CERTIFIER_OPT.CERTIFIER_OPT_HTTP_TIMEOUT:
            None
        case CERTIFIER_OPT.CERTIFIER_OPT_HTTP_CONNECT_TIMEOUT:
            None
        case CERTIFIER_OPT.CERTIFIER_OPT_OPTIONS:
            None
        case CERTIFIER_OPT.CERTIFIER_OPT_LOG_LEVEL:
            None
        case CERTIFIER_OPT.CERTIFIER__OPT_LOG_FUNCTION:
            None
        case CERTIFIER_OPT.CERTIFIER_OPT_CERT_MIN_TIME_LEFT_S:
            None
        case CERTIFIER_OPT.CERTIFIER_OPT_VALIDITY_DAYS:
            None
        case CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_INTERVAL:
            None
        case _:
            # Checking if non-boolean option (string option) is None
            if not (name >= CERTIFIER_OPT.CERTIFIER_OPT_BOOL_FIRST) and (value is None):
                rc = CertifierError(6, None, gen_application_error_msg(f"Attempted to set {CERTIFIER_OPT(name).name} with property value None", None))
                certifier_create_info(rc, property_error + 6, None)
                
    match(name):
        case CERTIFIER_OPT.CERTIFIER_OPT_CERT_X509_OUT:
            prop_map.cert_x509_out = value
        case CERTIFIER_OPT.CERTIFIER_OPT_CFG_FILENAME:
            prop_map.cfg_filename = value
        case CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TYPE:
            prop_map.auth_type = value
        case CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL:
            if str(value).startswith("https://"):
                prop_map.certifier_url = value
            else:
                rc = CertifierError(7, None, gen_application_error_msg("Attempted to set URL property with value not starting with https://", None))
                certifier_create_info(rc, property_error + 7, None)
        case CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH:
            prop_map.p12_filename = value
        case CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PATH:
            prop_map.output_p12_filename = value
        case CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD:
            prop_map.password = value
        case CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PASSWORD:
            prop_map.password_out = value
        case CERTIFIER_OPT.CERTIFIER_OPT_CA_INFO:
            prop_map.ca_info = value
        case CERTIFIER_OPT.CERTIFIER_OPT_CA_PATH:
            prop_map.ca_path = value
        case CERTIFIER_OPT.CERTIFIER_OPT_CRT:
            prop_map.crt = value
        case CERTIFIER_OPT.CERTIFIER_OPT_PROFILE_NAME:
            prop_map.profile_name = value
        case CERTIFIER_OPT.CERTIFIER_OPT_ECC_CURVE_ID:
            prop_map.ecc_curve_id = value
        case CERTIFIER_OPT.CERTIFIER_OPT_SYSTEM_ID:
            prop_map.system_id = value
        case CERTIFIER_OPT.CERTIFIER_OPT_MAC_ADDRESS:
            prop_map.mac_address = value
        case CERTIFIER_OPT.CERTIFIER_OPT_DNS_SAN:
            prop_map.dns_san = value
        case CERTIFIER_OPT.CERTIFIER_OPT_IP_SAN:
            prop_map.ip_san = value
        case CERTIFIER_OPT.CERTIFIER_OPT_EMAIL_SAN:
            prop_map.email_san = value

        # integer options            
        case CERTIFIER_OPT.CERTIFIER_OPT_HTTP_TIMEOUT:
            property_set_int(prop_map, name, int(value))
        case CERTIFIER_OPT.CERTIFIER_OPT_HTTP_CONNECT_TIMEOUT:
            property_set_int(prop_map, name, int(value))
        case CERTIFIER_OPT.CERTIFIER_OPT_LOG_LEVEL:
            property_set_int(prop_map, name, int(value))
        case CERTIFIER_OPT.CERTIFIER_OPT_LOG_MAX_SIZE:
            property_set_int(prop_map, name, int(value))
        case CERTIFIER_OPT.CERTIFIER_OPT_CERT_MIN_TIME_LEFT_S:
            property_set_int(prop_map, name, int(value))
        case CERTIFIER_OPT.CERTIFIER_OPT_VALIDITY_DAYS:
            property_set_int(prop_map, name, int(value))
        case CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_INTERVAL:
            property_set_int(prop_map, name, int(value))
        case CERTIFIER_OPT.CERTIFIER_OPT_LOG_FILENAME:
            prop_map.log_file = value
            cfg.file_name = value
        case CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TOKEN:
            prop_map.auth_token = value
        case CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_NODE:
            prop_map.output_node = value
        case CERTIFIER_OPT.CERTIFIER_OPT_TARGET_NODE:
            prop_map.target_node = value
        case CERTIFIER_OPT.CERTIFIER_OPT_ACTION:
            prop_map.action = value
        case CERTIFIER_OPT.CERTIFIER_OPT_INPUT_NODE:
            prop_map.input_node = value
        case CERTIFIER_OPT.CERTIFIER_OPT_SOURCE:
            prop_map.source = value
        case CERTIFIER_OPT.CERTIFIER_OPT_CN_PREFIX:
            prop_map.cn_prefix = value
        case CERTIFIER_OPT.CERTIFIER_OPT_DOMAIN:
            prop_map.domain = value
        case CERTIFIER_OPT.CERTIFIER_OPT_TRACKING_ID:
            prop_map.tracking_id = value
        case CERTIFIER_OPT.CERTIFIER_OPT_EXT_KEY_USAGE:
            prop_map.ext_key_usage_value = value
        case CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_CERTS_PATH_LIST:
            prop_map.autorenew_certs_path_list = value
        case CERTIFIER_OPT.CERTIFIER_OPT_OPTIONS:
            # readonly value 
            log(property_is_option_set(name, option),"Property [" + str(name) + "] is read-only", "WARN")
        case CERTIFIER_OPT.CERTIFIER_OPT_MTLS_P12_PATH:
            prop_map.mtls_filename = value
        case CERTIFIER_OPT.CERTIFIER_OPT_MTLS_P12_PASSWORD:
            prop_map.mtls_p12_filename = value
        case CERTIFIER_OPT.CERTIFIER_OPT_DEBUG_HTTP | CERTIFIER_OPT.CERTIFIER_OPT_TRACE_HTTP | CERTIFIER_OPT.CERTIFIER_OPT_FORCE_REGISTRATION | CERTIFIER_OPT.CERTIFIER_OPT_MEASURE_PERFORMANCE | CERTIFIER_OPT.CERTIFIER_OPT_CERTIFICATE_LITE | CERTIFIER_OPT.CERTIFIER_OPT_USE_SCOPES | CERTIFIER_OPT.CERTIFIER_OPT_VERBOSE:            
            bit = name - CERTIFIER_OPT.CERTIFIER_OPT_BOOL_FIRST

            option = 1 << bit

            property_set_option(prop_map, option, value != 0)
        case _:
            # some unknown property type
            log("property_set: unrecognized property [" + str(name) + "]", "WARN")
            rc = CertifierError(8, None, gen_application_error_msg("Attempted to set unrecognized property in property_set()", None))
            certifier_create_info(rc, property_error + 8, None)

def sectigo_property_get(prop_map: CertifierPropMap, name: SECTIGO_OPT):
    '''
    Function to retrieve a given property from certifier instance's CertifierPropMap based on name passed in.
    
    Returns value associated with property name on success
    
    Program exits and reports an error with property-related code mapping on failure
    '''
    rc = CertifierError()
    
    return_value = None
    
    match(name):            
        # Properties unique to search cert
        case SECTIGO_OPT.SECTIGO_OPT_STATUS:
            return_value = prop_map.status   
        case SECTIGO_OPT.SECTIGO_OPT_OFFSET:
            return_value = prop_map.offset        
        case SECTIGO_OPT.SECTIGO_OPT_LIMIT:
            return_value = prop_map.limit        
        case SECTIGO_OPT.SECTIGO_OPT_START_DATE:
            return_value = prop_map.start_date
        case SECTIGO_OPT.SECTIGO_OPT_END_DATE:
            return_value = prop_map.end_date
        case SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_ID:
            return_value = prop_map.certificate_id
        case SECTIGO_OPT.SECTIGO_OPT_VALIDITY_START_DATE:
            return_value = prop_map.validity_start_date
        case SECTIGO_OPT.SECTIGO_OPT_VALIDITY_END_DATE:
            return_value = prop_map.validity_end_date
        case SECTIGO_OPT.SECTIGO_OPT_CERT_ORDER:
            return_value = prop_map.cert_order
        case SECTIGO_OPT.SECTIGO_OPT_IS_CN_IN_SAN:
            return_value = prop_map.is_cn_in_san
        case SECTIGO_OPT.SECTIGO_OPT_REQUEST_TYPE:
            return_value = prop_map.request_type
        case SECTIGO_OPT.SECTIGO_OPT_TIMESTAMP:
            return_value = prop_map.timestamp
            
        # Properties unique to revoke cert
        case SECTIGO_OPT.SECTIGO_OPT_SERIAL_NUMBER:
            return_value = prop_map.serial_number
        case SECTIGO_OPT.SECTIGO_OPT_REQUESTOR_EMAIL:
            return_value = prop_map.requestor_email
            
        # General properties
        case SECTIGO_OPT.SECTIGO_OPT_SECTIGO_URL:
            return_value = prop_map.sectigo_url
        case SECTIGO_OPT.SECTIGO_OPT_AUTH_TOKEN:
            return_value = prop_map.auth_token
        case SECTIGO_OPT.SECTIGO_OPT_CERT_OUTPUT:
            return_value = prop_map.output
        case SECTIGO_OPT.SECTIGO_OPT_VERBOSE:
            return_value = prop_map.verbose
        case SECTIGO_OPT.SECTIGO_OPT_COMMON_NAME:
            return_value = prop_map.common_name
        case SECTIGO_OPT.SECTIGO_OPT_GROUP_NAME:
            return_value = prop_map.group_name
        case SECTIGO_OPT.SECTIGO_OPT_GROUP_EMAIL:
            return_value = prop_map.group_email
        case SECTIGO_OPT.SECTIGO_OPT_ID:
            return_value = prop_map.id
        case SECTIGO_OPT.SECTIGO_OPT_OWNER_LAST_NAME:
            return_value = prop_map.owner_last_name
        case SECTIGO_OPT.SECTIGO_OPT_OWNER_FIRST_NAME:
            return_value = prop_map.owner_first_name
        case SECTIGO_OPT.SECTIGO_OPT_EMPLOYEE_TYPE:
            return_value = prop_map.employee_type
        case SECTIGO_OPT.SECTIGO_OPT_SERVER_PLATFORM:
            return_value = prop_map.server_platform
        case SECTIGO_OPT.SECTIGO_OPT_SENSITIVE:
            return_value = prop_map.sensitive
        case SECTIGO_OPT.SECTIGO_OPT_PROJECT_NAME:
            return_value = prop_map.project_name
        case SECTIGO_OPT.SECTIGO_OPT_BUSINESS_JUSTIFICATION:
            return_value = prop_map.business_justification
        case SECTIGO_OPT.SECTIGO_OPT_SUBJECT_ALT_NAMES:
            return_value = prop_map.subject_alt_names
        case SECTIGO_OPT.SECTIGO_OPT_IP_ADDRESSES:
            return_value = prop_map.ip_addresses
        case SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_TYPE:
            return_value = prop_map.certificate_type
        case SECTIGO_OPT.SECTIGO_OPT_OWNER_PHONE_NUMBER:
            return_value = prop_map.owner_phone_number
        case SECTIGO_OPT.SECTIGO_OPT_OWNER_EMAIL:
            return_value = prop_map.owner_email
        case SECTIGO_OPT.SECTIGO_OPT_REVOCATION_REQUEST_REASON:
            return_value = prop_map.revocation_request_reason
        case SECTIGO_OPT.SECTIGO_OPT_SOURCE:
            return_value = prop_map.source
        case SECTIGO_OPT.SECTIGO_OPT_CFG_FILENAME:
            return_value = prop_map.cfg_filename
        case SECTIGO_OPT.SECTIGO_OPT_SOURCE:
            return_value = prop_map.source
        case SECTIGO_OPT.SECTIGO_OPT_LOG_LEVEL:
            return_value = prop_map.log_level
        case SECTIGO_OPT.SECTIGO_OPT_LOG_MAX_SIZE:
            return_value = prop_map.log_max_size
        case SECTIGO_OPT.SECTIGO_OPT_LOG_FILENAME:
            return_value = prop_map.log_file
        case _:
            log("property_get: unrecognized property [" + str(name) + "]", "WARN")
            rc = CertifierError(8, gen_application_error_msg("Attempted to set unrecognized property in sectigo_property_get()", None))
            certifier_create_info(rc, property_error + 8, None)

    return return_value

def sectigo_property_set(prop_map: CertifierPropMap, name: SECTIGO_OPT, value):
    '''
    Function attempts to set certifier instance's CertifierPropMap property of type [name] with [value].
    
    Returns None on success
    
    Program exits and reports an error with property-related code mapping on failure
    '''
    rc = CertifierError()
    
    match name:
        # Properties unique to search cert
        case SECTIGO_OPT.SECTIGO_OPT_STATUS:
            prop_map.status = value
        case SECTIGO_OPT.SECTIGO_OPT_OFFSET:
            prop_map.offset = value    
        case SECTIGO_OPT.SECTIGO_OPT_LIMIT:
            prop_map.limit = value   
        case SECTIGO_OPT.SECTIGO_OPT_START_DATE:
            prop_map.start_date = value
        case SECTIGO_OPT.SECTIGO_OPT_END_DATE:
            prop_map.end_date = value
        case SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_ID:
            prop_map.certificate_id = value
        case SECTIGO_OPT.SECTIGO_OPT_VALIDITY_START_DATE:
            prop_map.validity_start_date = value
        case SECTIGO_OPT.SECTIGO_OPT_VALIDITY_END_DATE:
            prop_map.validity_end_date = value
        case SECTIGO_OPT.SECTIGO_OPT_CERT_ORDER:
            prop_map.cert_order = value
        case SECTIGO_OPT.SECTIGO_OPT_IS_CN_IN_SAN:
            prop_map.is_cn_in_san = value
        case SECTIGO_OPT.SECTIGO_OPT_REQUEST_TYPE:
            prop_map.request_type = value
        case SECTIGO_OPT.SECTIGO_OPT_TIMESTAMP:
            prop_map.timestamp = value
            
        # Properties unique to revoke cert
        case SECTIGO_OPT.SECTIGO_OPT_SERIAL_NUMBER:
            prop_map.serial_number = value
        case SECTIGO_OPT.SECTIGO_OPT_REQUESTOR_EMAIL:
            prop_map.requestor_email = value
            
        # General properties
        case SECTIGO_OPT.SECTIGO_OPT_SECTIGO_URL:
            prop_map.sectigo_url = value
        case SECTIGO_OPT.SECTIGO_OPT_AUTH_TOKEN:
            prop_map.auth_token = value
        case SECTIGO_OPT.SECTIGO_OPT_CERT_OUTPUT:
            prop_map.output = value
        case SECTIGO_OPT.SECTIGO_OPT_VERBOSE:
            prop_map.verbose = value
        case SECTIGO_OPT.SECTIGO_OPT_COMMON_NAME:
            prop_map.common_name = value
        case SECTIGO_OPT.SECTIGO_OPT_GROUP_NAME:
            prop_map.group_name = value
        case SECTIGO_OPT.SECTIGO_OPT_GROUP_EMAIL:
            prop_map.group_email = value
        case SECTIGO_OPT.SECTIGO_OPT_ID:
            prop_map.id = value
        case SECTIGO_OPT.SECTIGO_OPT_OWNER_LAST_NAME:
            prop_map.owner_last_name = value
        case SECTIGO_OPT.SECTIGO_OPT_OWNER_FIRST_NAME:
            prop_map.owner_first_name = value
        case SECTIGO_OPT.SECTIGO_OPT_EMPLOYEE_TYPE:
            prop_map.employee_type = value
        case SECTIGO_OPT.SECTIGO_OPT_SERVER_PLATFORM:
            prop_map.server_platform = value
        case SECTIGO_OPT.SECTIGO_OPT_SENSITIVE:
            prop_map.sensitive = value
        case SECTIGO_OPT.SECTIGO_OPT_PROJECT_NAME:
            prop_map.project_name = value
        case SECTIGO_OPT.SECTIGO_OPT_BUSINESS_JUSTIFICATION:
            prop_map.business_justification = value
        case SECTIGO_OPT.SECTIGO_OPT_SUBJECT_ALT_NAMES:
            prop_map.subject_alt_names = value
        case SECTIGO_OPT.SECTIGO_OPT_IP_ADDRESSES:
            prop_map.ip_addresses = value
        case SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_TYPE:
            prop_map.certificate_type = value
        case SECTIGO_OPT.SECTIGO_OPT_OWNER_PHONE_NUMBER:
            prop_map.owner_phone_number = value
        case SECTIGO_OPT.SECTIGO_OPT_OWNER_EMAIL:
            prop_map.owner_email = value
        case SECTIGO_OPT.SECTIGO_OPT_REVOCATION_REQUEST_REASON:
            prop_map.revocation_request_reason = value
        case SECTIGO_OPT.SECTIGO_OPT_SOURCE:
            prop_map.source = value
        case SECTIGO_OPT.SECTIGO_OPT_CFG_FILENAME:
            prop_map.cfg_filename = value
        case SECTIGO_OPT.SECTIGO_OPT_SOURCE:
            prop_map.source = value
        case SECTIGO_OPT.SECTIGO_OPT_LOG_LEVEL:
            prop_map.log_level = value
        case SECTIGO_OPT.SECTIGO_OPT_LOG_MAX_SIZE:
            prop_map.log_max_size = value
        case SECTIGO_OPT.SECTIGO_OPT_LOG_FILENAME:
            prop_map.log_file = value
        case _:
            # some unknown property type
            log("sectigo_property_set: unrecognized property [" + str(name) + "]", "WARN")
            rc = CertifierError(8, gen_application_error_msg("Attempted to set unrecognized property in sectigo_property_set()", None))
            certifier_create_info(rc, property_error + 8, None)

def property_set_option(prop_map: CertifierPropMap, option: CERTIFIER_OPT.CERTIFIER_OPT_OPTIONS, enable: bool):
    '''
    If enable boolean is True, sets option by bitwise OR operation on CertifierPropMap's options field.
    
    If enable boolean is False, disables option by bitwise AND operation on CertifierPropMap's options field.
    
    Returns None
    '''
    if (enable):
        prop_map.options |= option
    else:
        prop_map.options &= ~option

def property_is_option_set(prop_map: CertifierPropMap, option: CERTIFIER_OPT_OPTION):
    '''
    Function checks if option is set by comparing the bitwise AND operation between CertifierPropMap's options field and a given option
    
    Returns boolean
    '''
    return (prop_map.options & option) != 0
    
def property_set_int(prop_map: CertifierPropMap, name: CERTIFIER_OPT, value: int):
    rc = CertifierError()
    
    if (value < 0):
        rc = CertifierError(5, gen_application_error_msg("Property integer value was < 0", None), None)
        certifier_create_info(rc, property_error + 5, None)

    match (name):
        case CERTIFIER_OPT.CERTIFIER_OPT_HTTP_TIMEOUT:
            prop_map.http_timeout = value
        case CERTIFIER_OPT.CERTIFIER_OPT_HTTP_CONNECT_TIMEOUT:
            prop_map.http_connect_timeout = value
        case CERTIFIER_OPT.CERTIFIER_OPT_LOG_LEVEL:
            prop_map.log_level = value
            cfg.level = prop_map.log_level
        case CERTIFIER_OPT.CERTIFIER_OPT_LOG_MAX_SIZE:
            prop_map.log_max_size = value
            cfg.max_size = prop_map.log_max_size
        case CERTIFIER_OPT.CERTIFIER_OPT_CERT_MIN_TIME_LEFT_S:
            prop_map.cert_min_time_left_s = value
        case CERTIFIER_OPT.CERTIFIER_OPT_VALIDITY_DAYS:
            prop_map.validity_days = value
        case CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_INTERVAL:
            prop_map.autorenew_interval = value
        case _:
            log("property_set_int: unrecognized property [" + str(name) + "]", "WARN")
            rc = CertifierError(8, None, gen_application_error_msg("Attempted to set unrecognized property in property_set_int()", None))
            certifier_create_info(rc, property_error + 8, None)
    
def xpki_property_set_defaults(prop_map: CertifierPropMap):  
    '''
    Function to set defaults of a certifier instance's CertifierPropMap before a config file is applied.
    
    Returns None on success
    
    Program exits and reports an error with property-related code mapping on failure via calls to helpers
    '''  
    trace_id = ''.join(secrets.choice(ALLOWABLE_CHARACTERS) for i in range(16))

    if (trace_id):
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_TRACKING_ID, trace_id)
    
    if (prop_map.verbose == None):
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_VERBOSE, False)
    
    if (prop_map.cfg_filename == None):
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_CFG_FILENAME, get_default_cfg_filename())
    
    if (prop_map.auth_type == None):
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TYPE, DEFAULT_AUTH_TYPE)

    if (prop_map.certifier_url == None):
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL, DEFAULT_CERTIFER_URL)
        
    if (prop_map.profile_name == None):
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_PROFILE_NAME, DEFAULT_PROFILE_NAME)
        
    xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_HTTP_TIMEOUT, DEFAULT_HTTP_TIMEOUT)
    
    xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_HTTP_CONNECT_TIMEOUT, DEFAULT_HTTP_CONNECT_TIMEOUT)

    if (prop_map.ca_info == None):
        default_ca_info = get_default_ca_info()
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_CA_INFO, default_ca_info)

    if (prop_map.ca_path == None):
        default_ca_path = get_default_ca_path()
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_CA_PATH, default_ca_path)

    if (prop_map.ecc_curve_id == None):
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_ECC_CURVE_ID, DEFAULT_ECC_CURVE_ID)
        
    xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_LOG_LEVEL, DEFAULT_LOG_LEVEL)

    xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_LOG_MAX_SIZE, DEFAULT_LOG_MAX_SIZE)
    
    cfg.max_size = prop_map.log_max_size

    prop_map.cert_min_time_left_s = DEFAULT_CERT_MIN_TIME_LEFT_S

    xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_SOURCE, DEFAULT_OPT_SOURCE)

    if (prop_map.output_p12_filename == None):
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PATH, DEFAULT_OUTPUT_P12_PATH)  
        
    xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_INTERVAL, DEFAULT_AUTORENEW_INTERVAL)

    if (prop_map.autorenew_certs_path_list == None):
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_CERTS_PATH_LIST, [DEFAULT_AUTORENEW_CERTS_PATH])   
def sectigo_property_set_defaults(prop_map: CertifierPropMap):     
    if (prop_map.verbose == None):
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_VERBOSE, False)
           
    if (prop_map.cfg_filename == None):
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_CFG_FILENAME, get_default_cfg_filename())
    
    if (prop_map.sectigo_url == None):
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_SECTIGO_URL, IMPULSE_URL)
    
    sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_LOG_LEVEL, DEFAULT_LOG_LEVEL)

    sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_LOG_MAX_SIZE, DEFAULT_LOG_MAX_SIZE)
    
    cfg.max_size = prop_map.log_max_size

    sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_SOURCE, DEFAULT_OPT_SOURCE)

def xpki_property_set_defaults_from_cfg_file(prop_map: CertifierPropMap):
    '''
    Function to set defaults of certifier instance's CertifierPropMap from a config file (either from CLI or default file)
    
    Returns None on success
    
    Program exits and reports an error with property-related code mapping on failure via calls to helpers
    '''     
    log_level = "DEBUG"
    
    log("Loading cfg file: " + str(prop_map.cfg_filename), log_level)

    with open(prop_map.cfg_filename, 'r') as file:
        data = json.load(file)
        
    if 'pycertifier.certifier.url' in data:
        log("Loaded certifier url: " + str(data['pycertifier.certifier.url']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL, data['pycertifier.certifier.url'])

    if 'pycertifier.profile.name' in data:
        log("Loaded profile name: " + str(data['pycertifier.profile.name']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_PROFILE_NAME, data['pycertifier.profile.name'])

    if 'pycertifier.auth.type' in data:
        log("Loaded auth_type: " + str(data['pycertifier.auth.type']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TYPE, data['pycertifier.auth.type'])

    if 'pycertifier.auth.token' in data:
        log("Loaded auth_token from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TOKEN, data['pycertifier.auth.token'])

    if 'pycertifier.input.p12.password' in data:
        log("Loaded password from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD, data['pycertifier.input.p12.password'])

    if 'pycertifier.system.id' in data:
        log("Loaded system_id_value: " + str(data['pycertifier.system.id']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_SYSTEM_ID, data['pycertifier.system.id'])
        
    if 'pycertifier.http.timeout' in data and data['pycertifier.http.timeout'] >= 0:
        log("Loaded http_timeout_value: " + str(data['pycertifier.http.timeout']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_HTTP_TIMEOUT, data['pycertifier.http.timeout'])

    if 'pycertifier.http.connect.timeout' in data and data['pycertifier.http.connect.timeout'] >= 0:
        log("Loaded http_connect_timeout_value: " + str(data['pycertifier.http.connect.timeout']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_HTTP_CONNECT_TIMEOUT, data['pycertifier.http.connect.timeout'])

    if 'pycertifier.http.trace' in data and data['pycertifier.http.trace'] == 1:
        log("Loaded http_trace_value: " + str(data['pycertifier.http.trace']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_TRACE_HTTP, data['pycertifier.http.trace'])

        prop_map.options |= (CERTIFIER_OPT_OPTION.CERTIFIER_OPTION_TRACE_HTTP | CERTIFIER_OPT_OPTION.CERTIFIER_OPTION_DEBUG_HTTP)

    if 'pycertifier.measure.performance' in data and data['pycertifier.measure.performance'] == 1:
        log("Loaded measure.performance: " + str(data['pycertifier.measure.performance']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_MEASURE_PERFORMANCE, data['pycertifier.measure.performance'])
        prop_map.options |= CERTIFIER_OPT_OPTION.CERTIFIER_OPTION_MEASURE_PERFORMANCE

    if 'pycertifier.autorenew.interval' in data and data['pycertifier.autorenew.interval'] == 1:
        log("Loaded autorenew.interval: " + str(data['pycertifier.autorenew.interval']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_INTERVAL, data['pycertifier.autorenew.interval'])

    if 'pycertifier.input.p12.path' in data:
        log("Loaded input_p12_path value: " + str(data['pycertifier.input.p12.path']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH, os.path.expanduser(os.path.expandvars(data['pycertifier.input.p12.path'])))

    if 'pycertifier.output.p12.path' in data:
        log("Loaded output_p12_path value: " + str(data['pycertifier.output.p12.path']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PATH, os.path.expanduser(os.path.expandvars(data['pycertifier.output.p12.path'])))

    if 'pycertifier.sat.token' in data:
        log("Loaded sat_token_value: " + str(data['pycertifier.sat.token']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TOKEN, data['pycertifier.sat.token'])

    if 'pycertifier.ca.info' in data:
        log("Loaded ca_info_value: " + str(data['pycertifier.ca.info']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_CA_INFO, data['pycertifier.ca.info'])

    if 'pycertifier.ca.path' in data:
        log("Loaded ca_path_value: " + str(data['pycertifier.ca.path']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_CA_PATH, data['pycertifier.ca.path'])

    if 'pycertifier.validity.days' in data:
        log("Loaded validity_days: " + str(data['pycertifier.validity.days']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_VALIDITY_DAYS, data['pycertifier.validity.days'])

    if 'pycertifier.ecc.curve.id' in data:
        log("Loaded ecc_curve_id_value " + str(data['pycertifier.ecc.curve.id']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_ECC_CURVE_ID, data['pycertifier.ecc.curve.id'])

    if 'pycertifier.log.file' in data:
        log("Loaded log_file_value: " + str(data['pycertifier.log.file']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_LOG_FILENAME, os.path.expanduser(os.path.expandvars(data['pycertifier.log.file'])))

    if 'pycertifier.log.level' in data and data['pycertifier.log.level'] >= 0:
        log("Loaded log_level_value: " + str(data['pycertifier.log.level']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_LOG_LEVEL, data['pycertifier.log.level'])

    if 'pycertifier.log.max.size' in data and data['pycertifier.log.max.size'] >= 0:
        log("Loaded log_max_size_value: " + str(data['pycertifier.log.max.size']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_LOG_MAX_SIZE, data['pycertifier.log.max.size'])

    cfg.max_size = prop_map.log_max_size

    if 'pycertifier.source.id' in data:
        log("Loaded source.id: " + str(data['pycertifier.source.id']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_SOURCE, data['pycertifier.source.id'])

    if 'pycertifier.certificate.lite' in data and data['pycertifier.certificate.lite'] == 1:
        log("Loaded certificate.lite: " + str(data['pycertifier.certificate.lite']) + " from config file.", log_level)
        prop_map.options |= (CERTIFIER_OPT_OPTION.CERTIFIER_OPTION_CERTIFICATE_LITE)
        
    if 'pycertifier.certificate.scopes' in data and data['pycertifier.certificate.scopes'] == 1:
        log(f"Loaded certificate.scopes: {data['pycertifier.certificate.scopes']} from cfg file.", log_level)
        prop_map.options |= (CERTIFIER_OPT_OPTION.CERTIFIER_OPTION_USE_SCOPES)
        
    if 'pycertifier.cn.name' in data and data['pycertifier.cn.name'] != None:
        log("Loaded common_name_value: " + str(data['pycertifier.cn.name']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_CN_PREFIX, data['pycertifier.cn.name'])

    if 'pycertifier.ext.key.usage' in data:
        log("Loaded extended_key_usage_values: " + str(data['pycertifier.ext.key.usage']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_EXT_KEY_USAGE, data['pycertifier.ext.key.usage'])

    if 'pycertifier.autorenew.certs.path.list' in data:
        log("Loaded autorenew_certs_path: " + str(data['pycertifier.autorenew.certs.path.list']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_AUTORENEW_CERTS_PATH_LIST, data['pycertifier.autorenew.certs.path.list'])

    if 'pycertifier.mtls.p12.path' in data:
        log("Loaded mtls_p12_path_value: " + str(data['pycertifier.mtls.p12.path']) + " from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_MTLS_P12_PATH, os.path.expanduser(os.path.expandvars(data['pycertifier.mtls.p12.path'])))
        
    if 'pycertifier.mtls.p12.password' in data:
        log("Loaded mTLS password from config file.", log_level)
        xpki_property_set(prop_map, CERTIFIER_OPT.CERTIFIER_OPT_MTLS_P12_PASSWORD, data['pycertifier.mtls.p12.password'])
        
    log("---------- FINISHED LOADING DEFAULTS FROM CONFIG FILE ----------\n", log_level)
    
def sectigo_property_set_defaults_from_cfg_file(prop_map: CertifierPropMap):
    '''
    Function to set defaults of certifier instance's CertifierPropMap from a config file (either from CLI or default file)
    
    Returns None on success
    
    Program exits and reports an error with property-related code mapping on failure via calls to helpers
    '''     
    log_level = "DEBUG"

    log("Loading cfg file: " + str(prop_map.cfg_filename), log_level)

    with open(prop_map.cfg_filename, 'r') as file:
        data = json.load(file)
    
    if 'pycertifier.sectigo.url' in data:
        log("Loaded Sectigo url: " + str(data['pycertifier.sectigo.url']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_SECTIGO_URL, data['pycertifier.sectigo.url'])

    if 'pycertifier.log.file' in data:
        log("Loaded log_file_value: " + str(data['pycertifier.log.file']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_LOG_FILENAME, data['pycertifier.log.file'])

    if 'pycertifier.log.level' in data and data['pycertifier.log.level'] >= 0:
        log("Loaded log_level_value: " + str(data['pycertifier.log.level']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_LOG_LEVEL, data['pycertifier.log.level'])

    if 'pycertifier.log.max.size' in data and data['pycertifier.log.max.size'] >= 0:
        log("Loaded log_max_size_value: " + str(data['pycertifier.log.max.size']) + " from config file.", log_level)
        xpki_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_LOG_MAX_SIZE, data['pycertifier.log.max.size'])

    cfg.max_size = prop_map.log_max_size
   
    if 'pycertifier.source.id' in data:
        log("Loaded source: " + str(data['pycertifier.source.id']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_SOURCE, data['pycertifier.source.id'])
    if 'pycertifier.auth.token' in data:
        log("Loaded auth_token from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_AUTH_TOKEN, data['pycertifier.auth.token'])
    if 'pycertifier.owner.last.name' in data:
        log("Loaded owner_last_name: " + str(data['pycertifier.owner.last.name']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_OWNER_LAST_NAME, data['pycertifier.owner.last.name'])
    if 'pycertifier.owner.first.name'in data:
        log("Loaded owner_first_name: " + str(data['pycertifier.owner.first.name']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_OWNER_FIRST_NAME, data['pycertifier.owner.first.name'])
    if 'pycertifier.owner.phone.number' in data:
        log("Loaded owner_phone_number: " + str(data['pycertifier.owner.phone.number']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_OWNER_PHONE_NUMBER, data['pycertifier.owner.phone.number'])
    if 'pycertifier.owner.email.address' in data:
        log("Loaded owner_email: " + str(data['pycertifier.owner.email.address']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_OWNER_EMAIL, data['pycertifier.owner.email.address'])
    if 'pycertifier.group.name' in data:
        log("Loaded group_name: " + str(data['pycertifier.group.name']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_GROUP_NAME, data['pycertifier.group.name'])
    if 'pycertifier.group.email.address' in data:
        log("Loaded group_email_address: " + str(data['pycertifier.group.email.address']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_GROUP_EMAIL, data['pycertifier.group.email.address'])
    if 'pycertifier.common.name' in data:
        log("Loaded common_name: " + str(data['pycertifier.common.name']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_COMMON_NAME, data['pycertifier.common.name'])
    if 'pycertifier.id' in data:
        log("Loaded id: " + str(data['pycertifier.id']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_ID, data['pycertifier.id'])
    if 'pycertifier.employee.type' in data:
        log("Loaded employee_type: " + str(data['pycertifier.employee.type']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_EMPLOYEE_TYPE, data['pycertifier.employee.type'])
    if 'pycertifier.server.platform' in data:
        log("Loaded server_platform: " + str(data['pycertifier.server.platform']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_SERVER_PLATFORM, data['pycertifier.server.platform'])
    if 'pycertifier.sensitive' in data:
        log("Loaded sensitive: " + str(data['pycertifier.sensitive']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_SENSITIVE, data['pycertifier.sensitive'])
    if 'pycertifier.project.name' in data:
        log("Loaded project_name: " + str(data['pycertifier.project.name']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_PROJECT_NAME, data['pycertifier.project.name'])
    if 'pycertifier.business.justification' in data:
        log("Loaded business_justification: " + str(data['pycertifier.business.justification']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_BUSINESS_JUSTIFICATION, data['pycertifier.business.justification'])
    if 'pycertifier.subject.alt.names' in data:
        log("Loaded subject_alt_names: " + str(data['pycertifier.subject.alt.names']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_SUBJECT_ALT_NAMES, data['pycertifier.subject.alt.names'])
    if 'pycertifier.ip.addresses' in data:
        log("Loaded ip_addresses: " + str(data['pycertifier.ip.addresses']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_IP_ADDRESSES, data['pycertifier.ip.addresses'])
    if 'pycertifier.requestor.email' in data:
        log("Loaded requestor_email: " + str(data['pycertifier.requestor.email']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_REQUESTOR_EMAIL, data['pycertifier.requestor.email'])
    if 'pycertifier.revocation.reason' in data:
        log("Loaded revocation_reason: " + str(data['pycertifier.revocation.reason']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_REVOCATION_REQUEST_REASON, data['pycertifier.revocation.reason'])
    if 'pycertifier.serial.number' in data:
        log("Loaded serial_number: " + str(data['pycertifier.serial.number']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_SERIAL_NUMBER, data['pycertifier.serial.number'])
    if 'pycertifier.certificate.id' in data:
        log("Loaded certificate_id: " + str(data['pycertifier.certificate.id']) + " from config file.", log_level)
        sectigo_property_set(prop_map, SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_ID, data['pycertifier.certificate.id'])
    log("---------- FINISHED LOADING DEFAULTS FROM CONFIG FILE ----------\n", log_level)