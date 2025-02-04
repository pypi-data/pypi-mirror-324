from .certifier import gen_application_error_msg, get_last_error, set_last_error, assign_last_error, CertifierError, CertifierPropMap, Certifier
from .constants import *
from .property import property_is_option_set, xpki_property_get
from .log import log

from requests_toolbelt.utils import dump
import requests
import requests_pkcs12
import threading
import json

lock = threading.Lock()   

@staticmethod
def check_certificate_status(certifier: Certifier, digest, as_helper: bool):
    '''
    Queries API for status of a certificate. 
    
    Returns None on success
    
    Returns CertifierError() on failure
    '''    
    if digest == None: 
        error_msg = gen_application_error_msg("Digest cannot be None", None)
        set_last_error(certifier, 9, error_msg)
        return get_last_error(certifier)

    certifier_url = xpki_property_get(certifier.CertifierPropMap, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL)
    certifier_status_url = f"{certifier_url}/certificate/status/{digest}"

    mtls_creds, http_timeouts, ca_bundle = set_curl_options(certifier.CertifierPropMap, as_helper)
  
    try:
        is_trace_http_enabled = property_is_option_set(certifier.CertifierPropMap, CERTIFIER_OPT_OPTION.CERTIFIER_OPTION_TRACE_HTTP)

        if all(item is not None for item in mtls_creds):
            resp = requests_pkcs12.get(certifier_status_url, pkcs12_filename=mtls_creds[0], pkcs12_password=mtls_creds[1], timeout=http_timeouts, verify=ca_bundle)
        else:
            resp = requests_pkcs12.get(certifier_status_url, timeout=http_timeouts, verify=ca_bundle)
        resp.raise_for_status()

        certificate_status = resp.json()['status']

        if not as_helper:
            log("Request Response: \n" + str(resp.text) + "\n", "DEBUG")
            log("Obtained certificate status successfully", "INFO")
            log(f"Certificate Status={certificate_status}" + "\n", "INFO")

        if certificate_status == "GOOD":
            assign_last_error(certifier, CertifierError(output=CERTIFIER_ERR_GET_CERT_STATUS_GOOD))
        elif certificate_status == "UNKNOWN":
            assign_last_error(certifier, CertifierError(output=CERTIFIER_ERR_GET_CERT_STATUS_UNKNOWN))
        elif certificate_status == "REVOKED":
            assign_last_error(certifier, CertifierError(output=CERTIFIER_ERR_GET_CERT_STATUS_REVOKED))
        else:
            assign_last_error(certifier, CertifierError(output=CERTIFIER_ERR_GET_CERT_STATUS_UNKNOWN))
                
        if is_trace_http_enabled:
            data = dump.dump_all(resp, "Request: ".encode(), "Response: ".encode())
            log(data.decode('utf-8'), "DEBUG")
    except Exception as e:
        if type(e) == ValueError:
            log("GET request failed because of MTLS credentials provided. Error was: " + str(e), "ERROR")
            rc = CertifierError(app_error_code=20, app_error_msg=gen_application_error_msg("GET request failed because of MTLS credentials provided.", None))
        elif type(e) in (requests.RequestException, requests.exceptions.HTTPError, requests.exceptions.ConnectionError):            
            if not as_helper:
                rc = CertifierError(app_error_code=10, 
                                            app_error_msg=gen_application_error_msg(f"GET request failed. Status Code: {resp.status_code}. Reason: {resp.reason}", resp))
            else:
                rc = CertifierError(app_error_code=14, 
                                            app_error_msg=gen_application_error_msg(f"GET request failed. Status Code: {resp.status_code}. Reason: {resp.reason}", resp))

        set_last_error(certifier, rc.application_error_code, rc.application_error_msg)
        return get_last_error(certifier)
    
def renew_x509_certificate(certifier: Certifier, digest):
    '''
    Queries API to renew a certificate. 
    
    Returns Certificate Chain from parsed JSON on success
    
    Returns CertifierError() on failure
    '''
    serialized_string = None
    certificate_chain = None
    tracking_id = xpki_property_get(certifier.CertifierPropMap, CERTIFIER_OPT.CERTIFIER_OPT_TRACKING_ID)
    bearer_token = xpki_property_get(certifier.CertifierPropMap, CERTIFIER_OPT.CERTIFIER_OPT_CRT)
    source = xpki_property_get(certifier.CertifierPropMap, CERTIFIER_OPT.CERTIFIER_OPT_SOURCE)
    certifier_url = xpki_property_get(certifier.CertifierPropMap, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL)
    
    certifier_renew_url = certifier_url + "/renew"
    
    mtls_creds, http_timeouts, ca_bundle = set_curl_options(certifier.CertifierPropMap, False)

    headers = {"Accept": "application/json", 
               "Content-Type": "application/json", 
              }
            
    headers.update({"Authorization": f"Bearer {bearer_token}"[:VERY_LARGE_STRING_SIZE * 4]})
    headers.update({"x-xpki-tracking-id": tracking_id[:SMALL_STRING_SIZE]})
    headers.update({"x-xpki-source": source[:SMALL_STRING_SIZE]})

    serialized_string = json.dumps(headers, indent=4)
    log(f"\nRequest Headers:\n{serialized_string}\n", "DEBUG")

    body = {"certificateID": ''.join(digest)}
    
    serialized_string = json.dumps(body, indent=4)
    log(f"\nRequest Body:\n{serialized_string}\n", "DEBUG")
    
    with lock:
        try:  
            is_trace_http_enabled = property_is_option_set(certifier.CertifierPropMap, CERTIFIER_OPT_OPTION.CERTIFIER_OPTION_TRACE_HTTP)

            if all(item is not None for item in mtls_creds):
                resp = requests_pkcs12.post(certifier_renew_url, headers=headers, json=digest, pkcs12_filename=mtls_creds[0], pkcs12_password=mtls_creds[1], timeout=http_timeouts, verify=ca_bundle)
            else:
                resp = requests_pkcs12.post(certifier_renew_url, headers=headers, json=digest, timeout=http_timeouts, verify=ca_bundle)
            resp.raise_for_status()
            
            if is_trace_http_enabled:
                data = dump.dump_all(resp, "Request: ".encode(), "Response: ".encode())
                log(data.decode('utf-8'), "DEBUG")
        except Exception as e:
            rc = CertifierError(app_error_code=15, 
                                                app_error_msg=gen_application_error_msg(f"POST request failed. Status Code: {resp.status_code}. Reason: {resp.reason}", resp))

            set_last_error(certifier, rc.application_error_code, rc.application_error_msg)
            return get_last_error(certifier)
        
    log(f"Request Response: \n{resp.text}\n", "DEBUG")
    
    try:
        parsed_json = resp.json()
        certificate_chain = parsed_json.get("certificateChain")
        assert certificate_chain != None
    except Exception as e:
        log(f"Could not parse JSON from post request response. Got error: {e}", "ERROR")
        rc = CertifierError(app_error_code=16, 
                                            app_error_msg=gen_application_error_msg(f"Could not parse JSON from post request response", resp))
        set_last_error(certifier, rc.application_error_code, rc.application_error_msg)
        return get_last_error(certifier)          
    
    log(f"Certificate Chain: \n{certificate_chain}", "DEBUG")

    return certificate_chain

def revoke_x509_certificate(certifier: Certifier, digest):
    '''
    Queries API to revoke a certificate. 
    
    Returns None on success
    
    Returns CertifierError() on failure
    '''
    source = xpki_property_get(certifier.CertifierPropMap, CERTIFIER_OPT.CERTIFIER_OPT_SOURCE)
    tracking_id = xpki_property_get(certifier.CertifierPropMap, CERTIFIER_OPT.CERTIFIER_OPT_TRACKING_ID)
    bearer_token = xpki_property_get(certifier.CertifierPropMap, CERTIFIER_OPT.CERTIFIER_OPT_CRT)
    certifier_revoke_url = xpki_property_get(certifier.CertifierPropMap, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL) + "/revoke"

    mtls_creds, http_timeouts, ca_bundle = set_curl_options(certifier.CertifierPropMap, False)

    headers = { 
               "Accept": "application/json", 
                "Content-Type": "application/json",
                "Authorization": f"Bearer {bearer_token}"[:VERY_LARGE_STRING_SIZE * 4],
                "x-xpki-tracking-id": tracking_id[:SMALL_STRING_SIZE],
                "x-xpki-source": source[:SMALL_STRING_SIZE]
              }
    
    serialized_string = json.dumps(headers, indent=4)

    log(f"\nRequest Headers:\n{serialized_string}\n", "DEBUG")
    
    body = {
        "certificateId": ''.join(digest), 
        "revokeReason": "UNSPECIFIED"
        }
    
    serialized_string = json.dumps(body, indent=4)
    
    log(f"\nRequest Body:\n{serialized_string}\n", "DEBUG")
        
    with lock:
        try:  
            is_trace_http_enabled = property_is_option_set(certifier.CertifierPropMap, CERTIFIER_OPT_OPTION.CERTIFIER_OPTION_TRACE_HTTP)

            if all(item is not None for item in mtls_creds):
                resp = requests_pkcs12.post(certifier_revoke_url, headers=headers, json=body, pkcs12_filename=mtls_creds[0], pkcs12_password=mtls_creds[1], timeout=http_timeouts, verify=ca_bundle)
            else:
                resp = requests_pkcs12.post(certifier_revoke_url, headers=headers, json=body, timeout=http_timeouts, verify=ca_bundle)
            resp.raise_for_status()

            if is_trace_http_enabled:
                data = dump.dump_all(resp, "Request: ".encode(), "Response: ".encode())
                log(data.decode('utf-8'), "DEBUG")            
        except Exception as e:        
            rc = CertifierError(app_error_code=14, 
                                      app_error_msg=gen_application_error_msg(f"POST request failed. Status Code: {resp.status_code}. Reason: {resp.reason}", resp))
            set_last_error(certifier, rc.application_error_code, rc.application_error_msg)
            return get_last_error(certifier)        

def request_x509_certificate(certifier: Certifier, csr, node_address, certifier_id):    
    '''
    Queries API to request a certificate. 
    
    Returns Certificate Chain from parsed JSON on success
    
    Returns CertifierError() on failure
    '''    
    certifier_get_url = xpki_property_get(certifier.CertifierPropMap, CERTIFIER_OPT.CERTIFIER_OPT_CERTIFIER_URL) + "/certificate"
    tracking_id = xpki_property_get(certifier.CertifierPropMap, CERTIFIER_OPT.CERTIFIER_OPT_TRACKING_ID)
    bearer_token = xpki_property_get(certifier.CertifierPropMap, CERTIFIER_OPT.CERTIFIER_OPT_CRT)
    source = xpki_property_get(certifier.CertifierPropMap, CERTIFIER_OPT.CERTIFIER_OPT_SOURCE)
        
    headers = {"Accept": "application/json", 
               "Content-Type": "application/json; charset=utf-8"}
        
    if bearer_token != None:
        headers.update({"Authorization": f"Bearer {bearer_token}"[:VERY_LARGE_STRING_SIZE * 4]})
            
    headers.update({"x-xpki-tracking-id": tracking_id[:SMALL_STRING_SIZE]})
    headers.update({"x-xpki-source": source[:SMALL_STRING_SIZE]})
    
    serialized_string = json.dumps(headers, indent=4)

    log(f"\nRequest Headers:\n{serialized_string}\n", "DEBUG")
    
    body = create_csr_post_data(certifier.CertifierPropMap, csr, node_address, certifier_id)
    
    mtls_creds, http_timeouts, ca_bundle = set_curl_options(certifier.CertifierPropMap, False)
    
    with lock:
        try:  
            is_trace_http_enabled = property_is_option_set(certifier.CertifierPropMap, CERTIFIER_OPT_OPTION.CERTIFIER_OPTION_TRACE_HTTP)

            if all(item is not None for item in mtls_creds):
                resp = requests_pkcs12.post(certifier_get_url, headers=headers, json=body, pkcs12_filename=mtls_creds[0], pkcs12_password=mtls_creds[1], timeout=http_timeouts, verify=ca_bundle)
            else:
                resp = requests_pkcs12.post(certifier_get_url, headers=headers, json=body, timeout=http_timeouts, verify=ca_bundle)
            resp.raise_for_status()

            if is_trace_http_enabled:
                data = dump.dump_all(resp, "Request: ".encode(), "Response: ".encode())
                log(data.decode('utf-8'), "DEBUG")
        except Exception as e:
            if type(e) == ValueError:
                log("POST request failed because of MTLS credentials provided. Error was: " + str(e), "ERROR")
                rc = CertifierError(app_error_code=21, app_error_msg=gen_application_error_msg("POST request failed because of MTLS credentials provided.", None))
            else:                
                rc = CertifierError(app_error_code=16, 
                                        app_error_msg=gen_application_error_msg(f"POST request failed. Status Code: {resp.status_code}. Reason: {resp.reason}", resp))
            set_last_error(certifier, rc.application_error_code, rc.application_error_msg)
            return get_last_error(certifier)        
    
    log(f"Request Response: \n{resp.text}\n", "DEBUG")
    
    try:
        parsed_json = resp.json()
        certificate_chain = parsed_json.get("certificateChain")
        assert certificate_chain != None
    except Exception as e:
        log(f"Could not parse JSON from post request response. Got error: {e}", "ERROR")
        rc = CertifierError(app_error_code=17, 
                                      app_error_msg=gen_application_error_msg("Could not parse JSON from post request response", resp))
        set_last_error(certifier, rc.application_error_code, rc.application_error_msg)
        return get_last_error(certifier)

    log(f"Certificate Chain: \n{certificate_chain}\n", "DEBUG")

    return certificate_chain

def create_csr_post_data(props: CertifierPropMap, csr, node_address, certifier_id):
    '''
    Creates CSR in JSON format to include in request for new certificate. 
    
    Returns CSR on success
    
    Will exit program with property-related error code on failure
    '''    
    
    serialized_string  = None

    system_id           = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_SYSTEM_ID)
    mac_address         = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_MAC_ADDRESS)
    dns_san             = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_DNS_SAN)
    ip_san              = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_IP_SAN)
    email_san           = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_EMAIL_SAN)
    domain              = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_DOMAIN)
    profile_name        = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_PROFILE_NAME)
    num_days            = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_VALIDITY_DAYS)
    use_scopes          = property_is_option_set(props, CERTIFIER_OPT_OPTION.CERTIFIER_OPTION_USE_SCOPES)
    is_certificate_lite = property_is_option_set(props, CERTIFIER_OPT_OPTION.CERTIFIER_OPTION_CERTIFICATE_LITE)
    
    body = {"csr": csr}
    
    if node_address:
        body.update({"nodeAddress": node_address})
        
    if domain:
        body.update({"domain": domain})
    
    body.update({"profileName": profile_name})
            
    if system_id:
        body.update({"systemId": system_id})
        
    if certifier_id:
        body.update({"ledgerId": certifier_id})
        
    if mac_address:
        body.update({"macAddress": mac_address})
    
    if dns_san:
        body.update({"dnsNames": dns_san})
        
    if ip_san:
        body.update({"ipAddresses": ip_san})
    
    if email_san:
        body.update({"emails": email_san})
        
    if num_days > 0:
        body.update({"validityDays": num_days})
    
    if is_certificate_lite:
        body.update({"certificateLite": "true"})
        
    if use_scopes:
        body.update({"useScopes": "true"})
        
    serialized_string = json.dumps(body, indent=4)
    
    log(f"\nRequest Body:\n{serialized_string}\n", "DEBUG")
    
    return body

def set_curl_options(props: CertifierPropMap, as_helper: bool):
    '''
    Called before every request to query certifier object for properties relevant for requests.
    
    Returns such fields to be passed into GET and POST requests respectively
    '''
    is_trace_http_enabled = property_is_option_set(props, CERTIFIER_OPT_OPTION.CERTIFIER_OPTION_TRACE_HTTP)
    http_timeout         = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_HTTP_TIMEOUT)
    http_connect_timeout = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_HTTP_CONNECT_TIMEOUT)
    mtls_p12           = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_MTLS_P12_PATH)
    mtls_password      = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_MTLS_P12_PASSWORD)
    ca_path = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_CA_PATH)
    ca_info = xpki_property_get(props, CERTIFIER_OPT.CERTIFIER_OPT_CA_INFO)    

    if not as_helper: 
        log("Trace HTTP Enabled=" + str(is_trace_http_enabled) + "\n", "DEBUG")
        
    verify_ca = ca_info if ca_info else ca_path
        
    return (mtls_p12, mtls_password), (http_connect_timeout, http_timeout), verify_ca