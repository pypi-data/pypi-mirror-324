from .certifier import *
from .log import log
from .constants import *
from .error import gen_application_error_msg, certifier_create_info, CertifierError

from dataclasses import dataclass
from importlib import resources
from enum import IntEnum
import re
import inspect

class XPKI_CLIENT_ERROR_CODE(IntEnum):
    XPKI_CLIENT_SUCCESS            = 0,
    XPKI_CLIENT_ERROR_INTERNAL     = 1,
    XPKI_CLIENT_INVALID_ARGUMENT   = 2,
    XPKI_CLIENT_NOT_IMPLEMENTED    = 3,
    XPKI_CLIENT_CERT_ALREADY_VALID = 4,
    XPKI_CLIENT_ERROR_NO_MEMORY    = 5,

class XPKI_CLIENT_CERT_STATUS(IntEnum):
    XPKI_CLIENT_CERT_VALID           = 0,
    XPKI_CLIENT_CERT_ABOUT_TO_EXPIRE = 1 << 0,
    XPKI_CLIENT_CERT_EXPIRED         = 1 << 1,
    XPKI_CLIENT_CERT_NOT_YET_VALID   = 1 << 2,
    XPKI_CLIENT_CERT_REVOKED         = 1 << 3,
    XPKI_CLIENT_CERT_UNKNOWN         = 1 << 4,
    XPKI_CLIENT_CERT_INVALID         = 1 << 5,

class XPKI_AUTH_TYPE(IntEnum):
    XPKI_AUTH_X509 = 0,
    XPKI_AUTH_SAT = 1

@dataclass
class get_cert_param_t():
    def __init__(self, cert_type):
        if cert_type == 'xpki':
            self.crt: str = None
            self.input_p12_path: str = None
            self.input_p12_password: str = None
            self.output_p12_path: str = None
            self.output_p12_password: str = None
            self.profile_name: str = None
            self.source_id: str = None
            self.auth_token: str = None
            self.auth_type: XPKI_AUTH_TYPE = None
            self.overwrite_p12: bool = None 
            self.validity_days: int = None
            self.lite: bool = None 
            self.keypair = None
            # optional parameters below
            self.static_certifier: bool = None
            self.use_scopes: bool = None
            self.mac_address: str = None
            self.serial_number: str = None
            self.dns_san: str = None
            self.ip_san: str = None
            self.email_san: str = None
            self.common_name: str = None
            self.domain: str = None
            self.cert_x509_out = None
            self.mtls_p12_path: str = None
            self.mtls_p12_password: str = None
            self.verbose: bool = None
        elif cert_type == 'sectigo':
            self.source: str = None
            self.auth_token: str = None
            self.owner_last_name: str = None
            self.owner_first_name: str = None
            self.owner_phone_number: str = None
            self.owner_email: str = None
            self.group_name: str = None
            self.group_email: str = None
            self.common_name: str = None
            self.id: str = None
            self.employee_type: str = None
            self.server_platform: str = None
            self.sensitive: str = None
            self.project_name: str = None
            self.business_justification: str = None
            self.subject_alt_names: str = None
            self.ip_addresses: str = None
            self.certificate_type: str = 'comodo'
            self.verbose: bool = None
            
@dataclass
class get_cert_status_param_t():    
    def __init__(self, cert_type):
        if cert_type == 'xpki':
            self.input_p12_path: str = None 
            self.input_p12_password: str = None 
            self.source_id: str = None
            self.auth_token: str = None  
            self.auth_type: XPKI_AUTH_TYPE = None
            self.static_certifier: bool = None
            self.verbose: bool = None
        elif cert_type == 'sectigo':
            self.source: str = None
            self.auth_token: str = None
            self.common_name: str = None
            self.serial_number: str = None
            self.certificate_id: int = None
            self.requestor_email: str = None
            self.verbose: bool = None

@dataclass
class get_cert_validity_param_t():
    def __init__(self, cert_type):
        if cert_type == 'xpki':
            self.input_p12_path: str = None
            self.input_p12_password: str = None 
            self.verbose: bool = None
            self.mtls_p12_path: str = None
            self.mtls_p12_password: str = None
        elif cert_type == 'sectigo':
            self.source: str = None
            self.auth_token: str = None
            self.common_name: str = None
            self.serial_number: str = None
            self.certificate_id: int = None
            self.requestor_email: str = None
            self.revocation_request_reason: str = None
            self.verbose: bool = None

@dataclass
class search_cert_param_t():
    def __init__(self, cert_type):
        if cert_type == 'sectigo':
            self.source: str = None
            self.auth_token: str = None
            self.group_name: str = None
            self.group_email: str = None
            self.status: str = None
            self.common_name: str = None
            self.offset: str = None
            self.limit: int = None
            self.start_date: str = None
            self.end_date: str = None
            self.certificate_id: int = None
            self.validity_start_date: str = None
            self.cert_order: str = None
            self.validity_end_date: str = None
            self.is_cn_in_san: str = None
            self.request_type: str = None
            self.timestamp: str = None
            self.verbose: bool = None
    
@dataclass
class renew_cert_param_t(get_cert_status_param_t):
    def __init__(self, cert_type):
        super().__init__(cert_type)

@dataclass
class print_cert_param_t(get_cert_validity_param_t):
    def __init__(self, cert_type):
        super().__init__(cert_type)

@dataclass
class revoke_cert_param_t(get_cert_validity_param_t):
    def __init__(self, cert_type):
        super().__init__(cert_type)    

# Utils
def verify_or_return_error(expr, code, certifier):
    ''' 
    Utility that either verifies expression.
    
    Returns None (on success)
    
    Returns a CertifierError() instance (on failure) with the supplied code
    '''
    
    if not expr:
        frame = inspect.currentframe().f_back
        line = inspect.getframeinfo(frame).code_context[0].strip()
        input = re.search(r'\(([^,]*)', line).group(1)
        application_error_msg = gen_application_error_msg(f"Expression passed ({input}) was unexpectedly false", None)
        set_last_error(certifier, code, application_error_msg)
        
        return get_last_error(certifier)

def is_mac_valid(mac: str):
    if mac is None or (len(mac) != 17):
        return False

    mac_pattern = r'^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$'
    
    return bool(re.match(mac_pattern, mac))

def expand_path(input: str):
    if input and isinstance(input, str):
        return path.expandvars(path.expanduser(input))        
# End Utils

def get_certifier_instance(args: Namespace, cert_type: str):
    '''
    Calls helper to create new certifier instance. 
    
    Returns certifier instance on success
    
    Returns certifier-related error on failure.
    '''
    try:
        certifier = certifier_new(args, cert_type)

        if certifier is None:
            rc = CertifierError(app_error_code=2, app_error_msg=gen_application_error_msg("Failed to instantiate Certifier. Certifier is None!", None))
            certifier_create_info(rc, certifier_error + rc.application_error_code, None)

        return certifier
    except AssertionError:
        return get_last_error(certifier)
    
def map_to_xpki_auth_type(str: str):
    if (str == "X509"):
        return XPKI_AUTH_TYPE.XPKI_AUTH_X509
    elif (str == "SAT"):
        return XPKI_AUTH_TYPE.XPKI_AUTH_SAT

def xpki_auth_type_to_string(auth_type: XPKI_AUTH_TYPE):
    match(auth_type):
        case XPKI_AUTH_TYPE.XPKI_AUTH_X509:
            return "X509"
        case XPKI_AUTH_TYPE.XPKI_AUTH_SAT:
            return "SAT"
        case _:
            return None
            
def xc_map_cert_status(value: int):
    '''
    Maps status to XPKI_CLIENT_CERT_STATUS() enum
    '''
    cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_VALID

    match (value):
        case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_CERT_ABOUT_TO_EXPIRE:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_ABOUT_TO_EXPIRE
        case value if value == CERTIFIER_ERR_GET_CERT_STATUS_GOOD: 
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_VALID
        case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_CERT_EXPIRED_2:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_EXPIRED
        case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_CERT_EXPIRED_1:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_NOT_YET_VALID
        case value if value == CERTIFIER_ERR_GET_CERT_STATUS_REVOKED:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_REVOKED
        case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_P12_NONEXISTENT:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_INVALID
        case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_X509_NONEXISTENT:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_INVALID
        case value if value == CERTIFIER_ERR_GET_CERT_STATUS_UNKNOWN | CERTIFIER_ERR_REGISTRATION_STATUS_CERT_ABOUT_TO_EXPIRE:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_ABOUT_TO_EXPIRE
        case _:
            cert_status |= XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_UNKNOWN

    return cert_status

def xc_map_cert_validity(value: int):
    '''
    Maps validity to XPKI_CLIENT_CERT_STATUS() enum
    '''
    cert_status: XPKI_CLIENT_CERT_STATUS = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_UNKNOWN
    
    match (value):
        case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_CERT_ABOUT_TO_EXPIRE:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_ABOUT_TO_EXPIRE
        case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_CERT_TIME_VALID:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_VALID
        case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_CERT_EXPIRED_2:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_EXPIRED
        case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_CERT_EXPIRED_1:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_NOT_YET_VALID
        case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_P12_NONEXISTENT:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_INVALID
        case value if value == CERTIFIER_ERR_REGISTRATION_STATUS_X509_NONEXISTENT:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_INVALID
        case value if value == CERTIFIER_ERR_GET_CERT_STATUS_UNKNOWN:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_UNKNOWN
        case _:
            cert_status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_UNKNOWN

    return cert_status

def xc_set_source_id(certifier: Certifier, source_id):
    if (source_id): 
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_SOURCE, source_id) == None

def xc_get_default_cert_param(certifier: Certifier, params: get_cert_param_t):
    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH)
    params.input_p12_path = param if (param) else None

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD)
    params.input_p12_password = param if (param) else None

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PATH)
    params.output_p12_path = param if (param) else None

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PASSWORD)
    params.output_p12_password = param if (param) else None

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_PROFILE_NAME)
    params.profile_name = param if (param) else None

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TOKEN)
    params.auth_token = param if (param) else None

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TYPE)
    params.auth_type = map_to_xpki_auth_type(param) if (param) else XPKI_AUTH_TYPE.XPKI_AUTH_X509

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_FORCE_REGISTRATION)
    params.overwrite_p12 = bool(param)

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_VALIDITY_DAYS)
    params.validity_days = (param) if (param) else 365

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFICATE_LITE)
    params.lite = bool(param)

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_USE_SCOPES)
    params.use_scopes = bool(param)

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CN_PREFIX)
    params.common_name = param if (param) else None

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_SOURCE)
    params.source_id = param if (param) else None

    params.static_certifier = False
    params.verbose = False
    params.keypair = None
    params.mac_address = None
    params.dns_san = None
    params.ip_san = None
    params.email_san = None
    params.domain = None
    params.serial_number = None
    params.crt = None

def xc_get_default_cert_status_param(certifier: Certifier, params: get_cert_status_param_t):
    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH)
    params.input_p12_path = param if (param) else None

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD)
    params.input_p12_password = param if (param) else None

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_SOURCE)
    params.source_id = param if (param) else None

    params.static_certifier = False
    params.verbose = False

def xc_get_default_cert_validity_param (certifier: Certifier, params: get_cert_validity_param_t):
    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH)
    params.input_p12_path = param if (param) else None

    param = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD)
    params.input_p12_password = param if (param) else None

    params.verbose = False

def xc_get_default_renew_cert_param(certifier: Certifier, params: renew_cert_param_t):
    xc_get_default_cert_status_param(certifier, params)

def xc_register_certificate(certifier: Certifier):
    '''
    Verifies CN prefix is set, constructs keys for certificate request, and calls helper certifier_register()
    
    Returns None on success
    
    Returns CertifierError() on failure
    '''
    try:
        cn_prefix = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CN_PREFIX)
        assert verify_or_return_error(cn_prefix != None, 9, certifier) == None
                
        assert certifier_register(certifier) == None        
    except AssertionError:
        return get_last_error(certifier)
        
def xc_get_cert(certifier: Certifier, params: get_cert_param_t):
    '''
    Sets certifier instance's CertifierPropMap with values from params argument. Then calls xc_register_certificate() helper
    
    Returns None on success
    
    Any errors from this function or propogated from helpers will result in program exit on failure
    '''
    try:
        assert verify_or_return_error(xpki_auth_type_to_string(params.auth_type) != None, 1, certifier) == None

        if (params.auth_type == XPKI_AUTH_TYPE.XPKI_AUTH_SAT):
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TOKEN, params.auth_token) == None
            assert verify_or_return_error((params.auth_token != None), 2, certifier) == None
        elif (params.auth_type == XPKI_AUTH_TYPE.XPKI_AUTH_X509):
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH, params.input_p12_path) == None

            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD, params.input_p12_password) == None
                
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PATH, params.output_p12_path) == None
        
        if (params.output_p12_password):
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PASSWORD, params.output_p12_password) == None
            
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_VALIDITY_DAYS, params.validity_days) == None
        
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFICATE_LITE, params.lite) == None

        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_USE_SCOPES, params.use_scopes) == None
        
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_PROFILE_NAME, params.profile_name) == None
        
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TYPE, xpki_auth_type_to_string(params.auth_type)) == None

        assert xc_set_source_id(certifier, params.source_id) == None

        if (params.common_name != None):
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CN_PREFIX, params.common_name) == None
            
        if (params.domain != None):
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_DOMAIN, params.domain) == None
            
        if (params.mac_address != None):
            assert verify_or_return_error(is_mac_valid(params.mac_address) == True, 8, certifier) == None
            
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_MAC_ADDRESS, params.mac_address) == None
            
        if (params.mac_address != None and is_mac_valid(params.mac_address) and params.serial_number != None):
            system_id = params.mac_address.join(params.serial_number)
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_SYSTEM_ID, system_id) == None
            
        if (params.dns_san != None):
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_DNS_SAN, params.dns_san) == None
    
        if (params.ip_san != None):
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_IP_SAN, params.ip_san) == None
            
        if (params.email_san != None):
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_EMAIL_SAN, params.email_san) == None
  
        if (params.crt == None):
            assert xc_create_crt(certifier, params.auth_type, params, True) == None

        if (params.static_certifier == True):
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL, CERTIFIER_STATIC_URL) == None
        else:
            certifier_url = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL)
            
            if ((certifier_url == None) or (len(certifier_url) == 0)):
                assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL, DEFAULT_CERTIFER_URL) == None
        
        if (certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PATH) != None):
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH, certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PATH)) == None
        
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_FORCE_REGISTRATION, params.overwrite_p12) == None
        
        if (certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PASSWORD) != None):
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD, certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_OUTPUT_P12_PASSWORD)) == None
                    
        assert xc_register_certificate(certifier) == None
                
        params.cert_x509_out = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CERT_X509_OUT)            
    except AssertionError:
        last_error = get_last_error(certifier)
        certifier_create_info(last_error, get_cert_error + last_error.application_error_code, None)
        
def _xc_get_cert_status(certifier: Certifier):
    '''
    Makes call to certifier_get_device_certificate_status() and then maps integer from helper to a member of XPKI_CLIENT_CERT_STATUS() enum representing status (good, unknown, revoked)
    
    Returns status of certificate (good, unknown, revoked) on success
    
    Returns CertifierError() on failure
    '''
    
    try:
        status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_INVALID

        assert certifier_get_device_certificate_status(certifier, False) == None

        assert isinstance(get_last_error(certifier).output, int)

        status = xc_map_cert_status(get_last_error(certifier).output)

        assert isinstance(status, XPKI_CLIENT_CERT_STATUS)
                
        return status
    except AssertionError:
        return get_last_error(certifier)
    
def xc_get_cert_status(certifier: Certifier, params: get_cert_status_param_t):
    '''
    Sets certifier instance's CertifierPropMap with values from params argument. Then calls _xc_get_cert_status helper
    
    Returns status of certificate, i.e. a member of XPKI_CLIENT_CERT_STATUS() enum, on success
    
    Any errors from this function or propogated from helpers will result in program exit on failure
    '''        
    try:
        assert verify_or_return_error(params != None and params.input_p12_path != None and params.input_p12_password != None and params.source_id != None, 1, certifier) == None
            
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH, params.input_p12_path)  == None
            
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD, params.input_p12_password) == None
        
        assert xc_set_source_id(certifier, params.source_id) == None
        
        if (params.static_certifier == True):
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL, CERTIFIER_STATIC_URL) == None
        else:
            certifier_url = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL)

            if ((certifier_url == None) or (len(certifier_url) == 0)):
                assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL, DEFAULT_CERTIFER_URL) == None

        status = _xc_get_cert_status(certifier)
        
        assert isinstance(status, XPKI_CLIENT_CERT_STATUS)
        
        return status
    except AssertionError:
        last_error = get_last_error(certifier)
        certifier_create_info(last_error, get_cert_status_error + last_error.application_error_code, None)

def _xc_get_cert_validity(certifier: Certifier):
    '''
    Makes call to certifier_get_device_registration_status() and then maps integer from helper to a member of XPKI_CLIENT_CERT_STATUS() enum representing validity
    
    Returns validity of certificate on success
    
    Returns CertifierError() on failure
    '''
    try:
        status = XPKI_CLIENT_CERT_STATUS.XPKI_CLIENT_CERT_INVALID
        assert certifier_get_device_registration_status(certifier, False) == None

        assert isinstance(get_last_error(certifier).output, int)
    
        status = xc_map_cert_validity(get_last_error(certifier).output)
        
        return status
    except AssertionError:
        return get_last_error(certifier)

def xc_get_cert_validity(certifier: Certifier, params: get_cert_validity_param_t):
    '''
    Sets certifier instance's CertifierPropMap with values from params argument. Then calls _xc_get_cert_validity helper
    
    Returns validity of certificate, i.e. a member of XPKI_CLIENT_CERT_STATUS() enum, on success
    
    Any errors from this function or propogated from helpers will result in program exit on failure
    '''
    try:
        assert verify_or_return_error(params != None and params.input_p12_path != None and params.input_p12_password != None, 1, certifier) == None
                
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH, params.input_p12_path) == None

        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD, params.input_p12_password) == None

        status = _xc_get_cert_validity(certifier)
        
        assert isinstance(status, XPKI_CLIENT_CERT_STATUS)
        
        return status
    except AssertionError:
        last_error = get_last_error(certifier)
        certifier_create_info(last_error, get_cert_validity_error + last_error.application_error_code, None)

def _xc_renew_certificate(certifier: Certifier, auth_type: CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TYPE, params: renew_cert_param_t):
    '''
    Creates CRT for request and stores in certifier instance. Calls helper to prepare SHA1 hash of serialized certificate
    
    Returns None on success
    
    Returns CertifierError() on failure
    '''
    try:
        assert xc_create_crt(certifier, auth_type, params, True) == None
            
        assert certifier_renew_certificate(certifier) == None
    except AssertionError:
        return get_last_error(certifier)


def xc_renew_cert(certifier: Certifier, params: renew_cert_param_t):
    '''
    Sets certifier instance's CertifierPropMap with values from params argument and verifies status/validity. Then calls _xc_renew_cert helper
    
    Returns None on success
    
    Any errors from this function or propogated from helpers will result in program exit on failure
    '''
    try:
        assert verify_or_return_error(params != None and params.input_p12_path != None and params.input_p12_password != None and params.source_id != None, 1, certifier) == None
                
        assert verify_or_return_error(xpki_auth_type_to_string(params.auth_type) != None, 8, certifier) == None
        
        if (params.auth_type == XPKI_AUTH_TYPE.XPKI_AUTH_SAT):
            assert verify_or_return_error(params.auth_token != None, 9, certifier) == None
            
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TOKEN, params.auth_token) == None

        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH, params.input_p12_path) == None
        
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD, params.input_p12_password) == None
               
        if (params.static_certifier == True):
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL, CERTIFIER_STATIC_URL) == None
        else:
            certifier_url = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL)
            
            if ((certifier_url == None) or (len(certifier_url) == 0)):
                assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL, DEFAULT_CERTIFER_URL) == None
            
        assert xc_set_source_id(certifier, params.source_id) == None
        
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TYPE, xpki_auth_type_to_string(params.auth_type)) == None
        
        assert certifier_get_device_certificate_status(certifier, True) == None
        last_error = get_last_error(certifier)

        # Only renew certificates that have a good status (i.e. not revoked or unkown)
        if last_error.output == CERTIFIER_ERR_GET_CERT_STATUS_UNKNOWN:
            set_last_error(certifier, 10, gen_application_error_msg("Cannot renew an unknown (non-xPKI) certificate. Verify status with 'get-cert-status' command.", None))
            assert False
        elif last_error.output == CERTIFIER_ERR_GET_CERT_STATUS_REVOKED:
            set_last_error(certifier, 11, gen_application_error_msg("Cannot renew a certificate that was previously revoked. Verify status with 'get-cert-status' command", None))
            assert False     
            
        last_error.clear()

        assert certifier_get_device_registration_status(certifier, True) == None
        last_error = get_last_error(certifier)

        # Only renew certificates that are about to expire or not yet valid
        if last_error.output != CERTIFIER_ERR_REGISTRATION_STATUS_CERT_ABOUT_TO_EXPIRE and last_error.output != CERTIFIER_ERR_REGISTRATION_STATUS_CERT_EXPIRED_1:
            set_last_error(certifier, 12, gen_application_error_msg("Cannot renew a certificate that is not about to expire or not yet valid.", None))
            assert False

        last_error.clear()

        assert _xc_renew_certificate(certifier, params.auth_type, params) == None        
    except AssertionError:
        last_error = get_last_error(certifier)
        certifier_create_info(last_error, renew_cert_error + last_error.application_error_code, None)

def xc_create_crt(certifier: Certifier, auth_type: XPKI_AUTH_TYPE, params: renew_cert_param_t | revoke_cert_param_t | None, as_helper: bool):
    '''
    Sets certifier instance's CertifierPropMap with values from params argument and verifies status/validity. Depending on authentication type 
    specified (x509 by default or SAT), will call helper certifier_create_x509_crt() or certifier_create_sat_crt() respectively.
    
    Returns None on success    
        
    Any errors from this function or propogated from helpers will result in program exit on failure
    '''
    try:
        assert verify_or_return_error(xpki_auth_type_to_string(auth_type) != None, 1, certifier) == None

        use_default = False
        
        if params and params.input_p12_path:
            file = params.input_p12_path if (isinstance(params.input_p12_path, str)) else params.input_p12_path.name

            if path.exists(file):
                assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH, params.input_p12_path) == None
                
                assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD, params.input_p12_password) == None
            else:
                use_default = True
        elif isinstance(params, renew_cert_param_t) and params.auth_type is XPKI_AUTH_TYPE.XPKI_AUTH_SAT and params.auth_token:
            assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TOKEN, params.auth_token) == None
        else:
            use_default = True
           
        if use_default:
            with resources.path('pycertifier.resources', 'seedtest.p12') as default:
                input_p12_path = str(default)

                certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH, input_p12_path)
                certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD, 'changeit')
            
        crt = None        
        
        if auth_type == XPKI_AUTH_TYPE.XPKI_AUTH_X509:
            certifier_setup_keys(certifier)
            
            crt = certifier_create_x509_crt(certifier, as_helper)
        elif auth_type == XPKI_AUTH_TYPE.XPKI_AUTH_SAT:
            crt = certifier_create_sat_crt(certifier, xpki_auth_type_to_string(auth_type), as_helper)
         
        assert not isinstance(crt, CertifierError)
                
        crt = base64.b64encode(crt.encode('utf-8')).decode('utf-8')
        
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_CRT, crt) == None             
    except AssertionError:
        last_error = get_last_error(certifier)
        certifier_create_info(last_error, get_crt_token_error + last_error.application_error_code, None)

def _xc_revoke_cert(certifier: Certifier, params: revoke_cert_param_t):
    '''
    Creates CRT for request and stores in certifier instance. Calls helper to prepare SHA1 hash of serialized certificate
    
    Returns None on success
    
    Returns CertifierError() on failure
    '''
    try:        
        auth_type = certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_AUTH_TYPE)

        assert xc_create_crt(certifier, map_to_xpki_auth_type(auth_type), params, True) == None
            
        assert certifier_revoke_certificate(certifier) == None
    except AssertionError:
        return get_last_error(certifier)
    
def xc_revoke_cert(certifier: Certifier, params: revoke_cert_param_t):
    '''
    Sets certifier instance's CertifierPropMap with values from params argument and verifies status/validity. Then calls _xc_revoke_cert helper
    
    Returns None on success
    
    Any errors from this function or propogated from helpers will result in program exit on failure
    '''
    try:
        assert verify_or_return_error(params != None and params.input_p12_path != None and params.input_p12_password != None, 1, certifier) == None

        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH, params.input_p12_path) == None

        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD, params.input_p12_password) == None
        
        assert certifier_get_device_certificate_status(certifier, True) == None
        last_error = get_last_error(certifier)
                
        # Only revoke certificates that have a good status (i.e. not revoked or unkown)
        if last_error.output == CERTIFIER_ERR_GET_CERT_STATUS_UNKNOWN:
            set_last_error(certifier, 10, gen_application_error_msg("Cannot revoke an unknown (non-xPKI) certificate. Verify status with 'get-cert-status' command.", None))
            assert False
        elif last_error.output == CERTIFIER_ERR_GET_CERT_STATUS_REVOKED:
            set_last_error(certifier, 11, gen_application_error_msg("Cannot revoke a certificate that was previously revoked. Verify status with 'get-cert-status' command", None))
            assert False     

        last_error.clear()
            
        assert certifier_get_device_registration_status(certifier, True) == None
        last_error = get_last_error(certifier)

        # Only revoke certificates if they are not expired
        if last_error.output == CERTIFIER_ERR_REGISTRATION_STATUS_CERT_EXPIRED_2:
            set_last_error(certifier, 12, gen_application_error_msg("Cannot revoke a certificate that has expired.", None))
            assert False
        
        last_error.clear()
                    
        assert _xc_revoke_cert(certifier, params) == None
                
    except AssertionError:
        last_error = get_last_error(certifier)
        certifier_create_info(last_error, revoke_error + last_error.application_error_code, None)

def xc_print_cert(certifier: Certifier, params: print_cert_param_t):    
    '''
    Sets certifier instance's CertifierPropMap with values from params argument. Then loads and prints certificate information.
    
    Formatted Base64 DER certificate will be returned on success
    
    Program will exit on failure
    '''
    try: 
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH, params.input_p12_path) == None
        
        assert certifier_set_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD, params.input_p12_password) == None

        file = params.input_p12_path if (isinstance(params.input_p12_path, str)) else params.input_p12_path.name

        log(f"Attempting to print {file}", "INFO")
        
        _, certificate, _ = load_pkcs12_file(certifier, 
                                       certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PATH), 
                                       certifier_get_property(certifier, CERTIFIER_OPT.CERTIFIER_OPT_INPUT_P12_PASSWORD))
        
        assert not isinstance(certificate, CertifierError)
        
        subject = re.search(r'<Name\((.+?)\)>', str(certificate.subject)).group(1)
        issuer = re.search(r'<Name\((.+?)\)', str(certificate.issuer)).group(1)
                
        if subject is None:
            set_last_error(certifier, 1, gen_application_error_msg("Couldn't find subject in certificate!", None))
            assert subject != None
        
        if issuer is None:
            set_last_error(certifier, 2, gen_application_error_msg("Couldn't find issuer in certificate!", None))
            assert issuer != None
                
        log("\n\nsubject: " + subject + "\n\n" + "issuer: " + issuer, "INFO")

        _, b64_der_cert = get_der_cert_and_b64_der_cert(certifier, certificate)
        
        if isinstance(b64_der_cert, CertifierError):
            assert False
                
        formatted_b64_der_cert = '\n'.join(b64_der_cert[i:i+64] for i in range(0, len(b64_der_cert), 64))
        log("\n\n" + PEM_BEGIN_CERTIFICATE + "\n" + formatted_b64_der_cert + "\n" + PEM_END_CERTIFICATE, "INFO")

        return PEM_BEGIN_CERTIFICATE + formatted_b64_der_cert + PEM_END_CERTIFICATE   
    except AssertionError:        
        last_error = get_last_error(certifier)
        certifier_create_info(last_error, print_cert_error + last_error.application_error_code, None)