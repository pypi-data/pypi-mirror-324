from .certifier import Certifier, CertifierError, certifier_set_property, certifier_get_property, certifier_setup_keys, sectigo_generate_certificate_signing_request, gen_application_error_msg, get_last_error, certifier_create_info, assign_last_error
from .xpki_client import get_cert_param_t, search_cert_param_t, renew_cert_param_t, revoke_cert_param_t
from .constants import SECTIGO_OPT, ALLOWABLE_CHARACTERS, get_cert_error, renew_cert_error, revoke_error, get_cert_status_error
from .log import log

import requests
import json
import secrets

def _sectigo_get_cert(certifier: Certifier, body):
    '''
    Queries API to request a certificate. 
    
    Returns None and sets SECTIGO_OPT_CERT_OUTPUT with API response on success
    
    Returns CertifierError() on failure
    '''    
    certifier_get_url = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SECTIGO_URL) + "/api/createCertificate"
            
    tracking_id = ''.join(secrets.choice(ALLOWABLE_CHARACTERS) for i in range(16))
    source = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SOURCE)
    
    log(f"\nTracking ID is: {tracking_id}\n", "DEBUG")
    log(f"\nSource ID is: {source}", "DEBUG")
    
    crt = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_AUTH_TOKEN)

    headers = {
            "Accept": "*/*", 
            "Connection": "keep-alive",
            "cache-control": "no-cache",
            "x-xpki-source": source,
            "x-xpki-request-id": tracking_id,
            "x-xpki-partner-id": "comcast",
            "Authorization": crt
            }

    log("Request Headers: \n" + json.dumps(headers, indent=4), "DEBUG")
    log("Request Body: \n" + json.dumps(body, indent=4), "DEBUG")
    
    try:
        resp = requests.post(certifier_get_url, headers=headers, json=body)

        if resp.status_code != 200:
            raise Exception()
        
        resp_output = resp.json() if resp.json else resp.text
        
        certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERT_OUTPUT, resp_output)
        
    except Exception as e:        
        rc = CertifierError(app_error_code=16, app_error_msg=gen_application_error_msg(f"POST request failed. Status Code: {resp.status_code}. Reason: {resp.reason}", resp))

        assign_last_error(certifier, rc)
        
        return get_last_error(certifier)

def sectigo_get_cert(certifier: Certifier, params: get_cert_param_t):
    '''
    Constructs request body from params argument before calling helper to make request
        
    Returns None on success
    
    Program exits and reports an error with get-cert-related code mapping on failure
    '''    
    try:
        assert check_and_set(certifier, SECTIGO_OPT.SECTIGO_OPT_AUTH_TOKEN, "authentication token", params.auth_token, 22) == None
        
        assert check_and_set(certifier, SECTIGO_OPT.SECTIGO_OPT_SOURCE, "source", params.source, 22) == None
        
        certifier_setup_keys(certifier)

        body = {}
    
        if params.common_name:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_COMMON_NAME, params.common_name)
        body.update({"commonName": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_COMMON_NAME)})
        
        if params.group_name:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_GROUP_NAME, params.group_name)
        body.update({"groupName": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_GROUP_NAME)})

        if params.group_email:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_GROUP_EMAIL, params.group_email)
        body.update({"groupEmailAddress": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_GROUP_EMAIL)})

        if params.id:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_ID, params.id)
        body.update({"id": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_ID)})

        if params.owner_last_name:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_OWNER_LAST_NAME, params.owner_last_name)
        body.update({"ownerLastName": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_OWNER_LAST_NAME)})

        if params.owner_first_name:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_OWNER_FIRST_NAME, params.owner_first_name)
        body.update({"ownerFirstName": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_OWNER_FIRST_NAME)})
        
        if params.employee_type: 
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_EMPLOYEE_TYPE, params.employee_type)
        body.update({"employeeType": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_EMPLOYEE_TYPE)})
        
        log("\nCreating Certificate Signing Request...\n", "DEBUG")
        csr = sectigo_generate_certificate_signing_request(certifier)
        log("\nGot a valid Certificate Signing Request.\n", "DEBUG")
        log(f"\nCertificate Signing Request: \n\n{csr}", "DEBUG")

        body.update({"certificateSigningRequest": csr})
                
        if params.server_platform:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SERVER_PLATFORM, params.server_platform)
        body.update({"serverPlatform": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SERVER_PLATFORM)})
        
        if params.sensitive:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SENSITIVE, params.sensitive)
        body.update({"sensitive": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SENSITIVE)})
        
        if params.project_name:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_PROJECT_NAME, params.project_name)
        body.update({"projectName": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_PROJECT_NAME)})
        
        if params.business_justification:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_BUSINESS_JUSTIFICATION, params.business_justification)
        body.update({"businessJustification": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_BUSINESS_JUSTIFICATION)})
        
        if params.subject_alt_names:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SUBJECT_ALT_NAMES, params.subject_alt_names)
        body.update({"subjectAltNames": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SUBJECT_ALT_NAMES)})

        if params.ip_addresses:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_IP_ADDRESSES, params.ip_addresses)
        body.update({"ipAddresses": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_IP_ADDRESSES)})
        
        if params.certificate_type:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_TYPE, params.certificate_type)
        body.update({"certificateType": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_TYPE)})
        
        if params.owner_phone_number:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_OWNER_PHONE_NUMBER, params.owner_phone_number)
        body.update({"ownerPhoneNumber": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_OWNER_PHONE_NUMBER)})
        
        if params.owner_email:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_OWNER_EMAIL, params.owner_email)
        body.update({"ownerEmailAddress": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_OWNER_EMAIL)})
                
        # Get the list of all possible properties for instance of get_cert_param_t
        names = list(vars(params).keys())

        # Collect the relevant key-value property pairings from CertifierPropMap
        get_cert_properties = {name: getattr(certifier.CertifierPropMap, name) for name in names if hasattr(certifier.CertifierPropMap, name)}

        # If any of those properties are still None at this point, exit
        if any(value is None for value in get_cert_properties.values()):
            none_items = [name for name in get_cert_properties.keys() if get_cert_properties.get(name) is None]
            rc = CertifierError(22, gen_application_error_msg(f"Required value(s) were unexpectedly None! Check that these are set via CLI or config: {none_items}", None), None)
            assign_last_error(certifier, rc)
            assert False
                        
        assert _sectigo_get_cert(certifier, body) == None    
    except AssertionError:
        last_error = get_last_error(certifier)
        certifier_create_info(last_error, get_cert_error + last_error.application_error_code, None)

def _sectigo_search_cert(certifier: Certifier, request_params):
    '''
    Queries API to search for certificates.
    
    Returns None and sets SECTIGO_OPT_CERT_OUTPUT with API response on success
    
    Returns CertifierError() on failure
    '''    
    certifier_search_url = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SECTIGO_URL) + "/api/getCertificates"
            
    tracking_id = ''.join(secrets.choice(ALLOWABLE_CHARACTERS) for i in range(16))
    source = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SOURCE)
    
    log(f"\nTracking ID is: {tracking_id}\n", "DEBUG")
    log(f"\nSource ID is: {source}", "DEBUG")
    
    crt = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_AUTH_TOKEN)

    headers = {
            "Accept": "*/*", 
            "Connection": "keep-alive",
            "cache-control": "no-cache",
            "x-xpki-source": source,
            "x-xpki-request-id": tracking_id,
            "x-xpki-partner-id": "comcast",
            "Authorization": crt
            }
    
    log("Request Headers: \n" + json.dumps(headers, indent=4), "DEBUG")
    log("Request Parameters: \n" + json.dumps(request_params, indent=4), "DEBUG")

    try:
        resp = requests.get(certifier_search_url, headers=headers, params=request_params)
        
        if resp.status_code != 200:
            raise Exception()

        resp_output = resp.json() if resp.json else resp.text

        certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERT_OUTPUT, resp_output)
    except Exception as e:        
        rc = CertifierError(app_error_code=11, app_error_msg=gen_application_error_msg(f"GET request failed. Status Code: {resp.status_code}. Reason: {resp.reason}", resp))

        assign_last_error(certifier, rc)
        
        return get_last_error(certifier)
  
def sectigo_search_cert(certifier: Certifier, params: search_cert_param_t):
    '''
    Constructs request body from params argument before calling helper to make request
        
    Returns None on success
    
    Program exits and reports an error with search-related code mapping on failure
    '''    
    try:
        assert check_and_set(certifier, SECTIGO_OPT.SECTIGO_OPT_AUTH_TOKEN, "authentication token", params.auth_token, 12) == None
        
        assert check_and_set(certifier, SECTIGO_OPT.SECTIGO_OPT_SOURCE, "source", params.source, 12) == None
                
        request_params = {}
        
        if params.group_name:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_GROUP_NAME, params.group_name)
        request_params.update({"groupName": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_GROUP_NAME)})
        
        if params.group_email:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_GROUP_EMAIL, params.group_email)
        request_params.update({"groupEmail": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_GROUP_EMAIL)})
        
        if params.status:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_STATUS, params.status)
        request_params.update({"status": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_STATUS)})
        
        if params.common_name:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_COMMON_NAME, params.common_name)
        request_params.update({"commonName": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_COMMON_NAME)})
        
        if params.offset:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_OFFSET, params.offset)
        request_params.update({"offset": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_OFFSET)})
        
        if params.limit:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_LIMIT, params.limit)
        request_params.update({"limit": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_LIMIT)})
        
        if params.start_date:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_START_DATE, params.start_date)
        request_params.update({"startDate": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_START_DATE)})
        
        if params.end_date:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_END_DATE, params.end_date)
        request_params.update({"endDate": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_END_DATE)})
        
        if params.certificate_id:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_ID, params.certificate_id)
        request_params.update({"certificateId": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_ID)})
        
        if params.validity_start_date:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_VALIDITY_START_DATE, params.validity_start_date)
        request_params.update({"validityStartDate": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_VALIDITY_START_DATE)})
        
        if params.cert_order:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERT_ORDER, params.cert_order)
        request_params.update({"certOrder": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERT_ORDER)})
        
        if params.validity_end_date:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_VALIDITY_END_DATE, params.validity_end_date)
        request_params.update({"validityEndDate": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_VALIDITY_END_DATE)})
        
        if params.is_cn_in_san:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_IS_CN_IN_SAN, params.is_cn_in_san)
        request_params.update({"isCNinSAN": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_IS_CN_IN_SAN)})
        
        if params.request_type:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_REQUEST_TYPE, params.request_type)
        request_params.update({"requestType": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_REQUEST_TYPE)})
        
        if params.timestamp:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_TIMESTAMP, params.timestamp)
        request_params.update({"timestamp": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_TIMESTAMP)})
            
        assert _sectigo_search_cert(certifier, request_params) == None
    except AssertionError:
        last_error = get_last_error(certifier)
        certifier_create_info(last_error, get_cert_status_error + last_error.application_error_code, None)

def _sectigo_renew_cert(certifier: Certifier, body):
    '''
    Queries API to renew certificate.
    
    Returns None and sets SECTIGO_OPT_CERT_OUTPUT with API response on success
    
    Returns CertifierError() on failure
    '''    
    certifier_renew_url = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SECTIGO_URL) + "/api/renewCertificate"
            
    tracking_id = ''.join(secrets.choice(ALLOWABLE_CHARACTERS) for i in range(16))
    source = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SOURCE)
    
    log(f"\nTracking ID is: {tracking_id}\n", "DEBUG")
    log(f"\nSource ID is: {source}", "DEBUG")
    
    crt = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_AUTH_TOKEN)

    headers = {
            "Accept": "*/*", 
            "Connection": "keep-alive",
            "cache-control": "no-cache",
            "x-xpki-source": source,
            "x-xpki-request-id": tracking_id,
            "x-xpki-partner-id": "comcast",
            "Authorization": crt
            }
    
    log("Request Headers: \n" + json.dumps(headers, indent=4), "DEBUG")
    log("Request Body: \n" + json.dumps(body, indent=4), "DEBUG")
    
    try:
        resp = requests.post(certifier_renew_url, headers=headers, json=body)
        
        if resp.status_code != 200:
            raise Exception()

        resp_output = resp.json() if resp.json else resp.text

        certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERT_OUTPUT, resp_output)
    except Exception as e:                
        rc = CertifierError(app_error_code=15, app_error_msg=gen_application_error_msg(f"POST request failed. Status Code: {resp.status_code}. Reason: {resp.reason}", resp))
        
        assign_last_error(certifier, rc)
        
        return get_last_error(certifier)

def sectigo_renew_cert(certifier: Certifier, params: renew_cert_param_t):   
    '''
    Constructs request body from params argument before calling helper to make request
        
    Returns None on success
    
    Program exits and reports an error with renew-related code mapping on failure
    '''    
    try: 
        assert check_and_set(certifier, SECTIGO_OPT.SECTIGO_OPT_AUTH_TOKEN, "authentication token", params.auth_token, 21) == None
        
        assert check_and_set(certifier, SECTIGO_OPT.SECTIGO_OPT_SOURCE, "source", params.source, 21) == None

        assert check_and_set(certifier, SECTIGO_OPT.SECTIGO_OPT_COMMON_NAME, "common name", params.common_name, 21) == None
        
        assert check_and_set(certifier, SECTIGO_OPT.SECTIGO_OPT_REQUESTOR_EMAIL, "requestor email", params.requestor_email, 21) == None

        assert check_identifier(certifier, params.certificate_id, params.serial_number, 22) == None

        body = {}

        if params.common_name:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_COMMON_NAME, params.common_name)
        body.update({"commonName": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_COMMON_NAME)})
        
        if params.serial_number:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SERIAL_NUMBER, params.serial_number)
        body.update({"serialNumber": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SERIAL_NUMBER)})
        
        if params.certificate_id:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_ID, params.certificate_id)
        body.update({"certificateId": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_ID)})
        
        if params.requestor_email:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_REQUESTOR_EMAIL, params.requestor_email)
        body.update({"requestorEmail": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_REQUESTOR_EMAIL)})
        
        assert _sectigo_renew_cert(certifier, body) == None
    except AssertionError:
        last_error = get_last_error(certifier)
        certifier_create_info(last_error, renew_cert_error + last_error.application_error_code, None)

def _sectigo_revoke_cert(certifier: Certifier, body):
    '''
    Queries API to revoke certificate.
    
    Returns None and sets SECTIGO_OPT_CERT_OUTPUT with API response on success
    
    Returns CertifierError() on failure
    '''    
    certifier_revoke_url = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SECTIGO_URL) + "/api/revokeCertificate"
            
    tracking_id = ''.join(secrets.choice(ALLOWABLE_CHARACTERS) for i in range(16))
    source = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SOURCE)
    
    log(f"\nTracking ID is: {tracking_id}\n", "DEBUG")
    log(f"\nSource ID is: {source}", "DEBUG")
    
    crt = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_AUTH_TOKEN)

    headers = {
            "Accept": "*/*", 
            "Connection": "keep-alive",
            "cache-control": "no-cache",
            "x-xpki-source": source,
            "x-xpki-request-id": tracking_id,
            "x-xpki-partner-id": "comcast",
            "Authorization": crt
            }

    log("Request Headers: \n" + json.dumps(headers, indent=4), "DEBUG")
    log("Request Body: \n" + json.dumps(body, indent=4), "DEBUG")
    
    try:
        resp = requests.put(certifier_revoke_url, headers=headers, json=body)
        
        if resp.status_code != 200:
            raise Exception()
 
        resp_output = resp.json() if resp.json else resp.text

        certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERT_OUTPUT, resp_output)
    
    except Exception as e:        
        rc = CertifierError(app_error_code=14, app_error_msg=gen_application_error_msg(f"PUT request failed. Status Code: {resp.status_code}. Reason: {resp.reason}", resp))
        
        assign_last_error(certifier, rc)
        
        return get_last_error(certifier)

def sectigo_revoke_cert(certifier: Certifier, params: revoke_cert_param_t):  
    '''
    Constructs request body from params argument before calling helper to make request
        
    Returns None on success
    
    Program exits and reports an error with revoke-related code mapping on failure
    '''    
 
    try:
        assert check_and_set(certifier, SECTIGO_OPT.SECTIGO_OPT_AUTH_TOKEN, "authentication token", params.auth_token, 15) == None
         
        assert check_and_set(certifier, SECTIGO_OPT.SECTIGO_OPT_SOURCE, "source", params.source, 15) == None

        assert check_and_set(certifier, SECTIGO_OPT.SECTIGO_OPT_COMMON_NAME, "common name", params.common_name, 15) == None

        assert check_and_set(certifier, SECTIGO_OPT.SECTIGO_OPT_REQUESTOR_EMAIL, "requestor email", params.requestor_email, 15) == None
        
        assert check_and_set(certifier, SECTIGO_OPT.SECTIGO_OPT_REVOCATION_REQUEST_REASON, "revocation request reason", params.revocation_request_reason, 15) == None
                                
        assert check_identifier(certifier, params.certificate_id, params.serial_number, 16) == None                                

        body = {}

        if params.common_name:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_COMMON_NAME, params.common_name)
        body.update({"commonName": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_COMMON_NAME)})
        
        if params.revocation_request_reason:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_REVOCATION_REQUEST_REASON, params.revocation_request_reason)
        body.update({"revocationRequestReason": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_REVOCATION_REQUEST_REASON)})    
        
        if params.requestor_email:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_REQUESTOR_EMAIL, params.requestor_email)
        body.update({"requestorEmail": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_REQUESTOR_EMAIL)})

        if params.serial_number: 
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SERIAL_NUMBER, params.serial_number)
        body.update({"serialNumber": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SERIAL_NUMBER)})
        
        if params.certificate_id:
            certifier_set_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_ID, params.certificate_id)
        body.update({"certificateId": certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_ID)})
        
        assert _sectigo_revoke_cert(certifier, body) == None
    except AssertionError:
        last_error = get_last_error(certifier)
        certifier_create_info(last_error, revoke_error + last_error.application_error_code, None)
        
def check_and_set(certifier, option, params_name, params_value, error_code):
    '''
    Function checks if required property was passed as command line argument or in configuration file. Sets property with value from command line if possible
    
    Returns None on success
    
    Returns CertifierError() on failure
    '''
    if params_value is None and certifier_get_property(certifier, option) is None:
            rc = CertifierError(error_code, gen_application_error_msg(f"Required value was unexpectedly None! Check that '{params_name}' was provided via CLI or configuration file", None), None)
            assign_last_error(certifier, rc)
            return get_last_error(certifier)
    elif params_value:
        certifier_set_property(certifier, option, params_value)
        
def check_identifier(certifier, certificate_id, serial_number, error_code):
    # True if certificate id or serial number was passed in config
    in_config = certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_CERTIFICATE_ID) is not None or certifier_get_property(certifier, SECTIGO_OPT.SECTIGO_OPT_SERIAL_NUMBER) is not None
    
    # True if certificate id or serial number was passed in args
    in_cli_args = certificate_id is not None or serial_number is not None
        
    if (in_config or in_cli_args) is False:
        rc = CertifierError(error_code, gen_application_error_msg(f"'Certificate ID' or 'Serial Number' (one required) was not provided via CLI or configuration file", None), None)
        assign_last_error(certifier, rc)
        return get_last_error(certifier)

    
