from .log import log_setup, Namespace
from .xpki_client import expand_path, map_to_xpki_auth_type
from .main import xpki_perform

import os

def get_xpki_cert_status(input_p12_path: str = None, input_p12_password: str = None, config: str = None, enable_logging: bool = False, verbose: bool = False, ca_path: str = None, mtls_p12_path: str = None, mtls_p12_password: str = None):
    """
    Get the status of an xPKI certificate. 

    This function checks the status of an xPKI certificate and returns whether it is valid, about to expire, not yet valid, or expired. 
    
    Either `input_p12_path` and `input_p12_password` must be provided, or a `config` file that contains these details.

    Args:
        input_p12_path (str, optional): Path to the input PKCS#12 file. Required if `config` is not provided.
        input_p12_password (str, optional): Password for the input PKCS#12 file. Required if `config` is not provided.
        config (str, optional): Path to the configuration file that contains the required details.
        enable_logging (bool): Enable logging output. Default is False.
        verbose (bool, optional): Enable verbose output. Default is False.
        ca_path (str, optional): Path to the CA certificate.
        mtls_p12_path (str, optional): Path to the mTLS PKCS#12 file.
        mtls_p12_password (str, optional): Password for the mTLS PKCS#12 file.

    Returns:
        dict: A dictionary containing the return code, error message (if any), and the status of the xPKI certificate.

    Raises:
        ValueError: If neither `input_p12_path` and `input_p12_password` nor `config` are provided.
    """
    
    if not input_p12_path and not config:
        raise ValueError("Either input_p12_path and input_p12_password or config must be provided.")
    
    return perform_action(
        'xpki',
        'get-cert-status',
        input_p12_path=input_p12_path,
        input_p12_password=input_p12_password,
        config=config,
        enable_logging=enable_logging,
        verbose=verbose,
        ca_path=ca_path,
        mtls_p12_path=mtls_p12_path,
        mtls_p12_password=mtls_p12_password
    )

def get_xpki_cert_validity(input_p12_path: str = None, input_p12_password: str = None, config: str = None, enable_logging: bool = False, verbose: bool = False, ca_path: str = None, mtls_p12_path: str = None, mtls_p12_password: str = None):
    """
    Get the validity period of an xPKI certificate.

    This function retrieves the validity period of an xPKI certificate and returns whether it is valid, about to expire, not yet valid, or expired. 
    
    Either `input_p12_path` and `input_p12_password` must be provided, or a `config` file that contains these details.

    Args:
        input_p12_path (str, optional): Path to the input PKCS#12 file. Required if `config` is not provided.
        input_p12_password (str, optional): Password for the input PKCS#12 file. Required if `config` is not provided.
        config (str, optional): Path to the configuration file that contains the required details.
        enable_logging (bool): Enable logging output. Default is False.        
        verbose (bool, optional): Enable verbose output. Default is False.
        ca_path (str, optional): Path to the CA certificate.
        mtls_p12_path (str, optional): Path to the mTLS PKCS#12 file.
        mtls_p12_password (str, optional): Password for the mTLS PKCS#12 file.

    Returns:
        dict: A dictionary containing the return code, error message (if any), and the validity period of the xPKI certificate.

    Raises:
        ValueError: If neither `input_p12_path` and `input_p12_password` nor `config` are provided.
    """
    if not input_p12_path and not config:
        raise ValueError("Either input_p12_path and input_p12_password or config must be provided.")
    
    return perform_action(
        'xpki',
        'get-cert-validity',
        input_p12_path=input_p12_path,
        input_p12_password=input_p12_password,
        config=config,
        enable_logging=enable_logging,
        verbose=verbose,
        ca_path=ca_path,
        mtls_p12_path=mtls_p12_path,
        mtls_p12_password=mtls_p12_password
    )

def renew_xpki_cert(input_p12_path: str = None, input_p12_password: str = None, config: str = None, enable_logging: bool = False, verbose: bool = False, ca_path: str = None, mtls_p12_path: str = None, mtls_p12_password: str = None):
    """
    Renew an xPKI certificate.

    This function renews an xPKI certificate using the original validity period specified during its creation.
    
    Either `input_p12_path` and `input_p12_password` must be provided, or a `config` file that contains these details.

    Args:
        input_p12_path (str, optional): Path to the input PKCS#12 file. Required if `config` is not provided.
        input_p12_password (str, optional): Password for the input PKCS#12 file. Required if `config` is not provided.
        config (str, optional): Path to the configuration file that contains the required details.
        enable_logging (bool): Enable logging output. Default is False.
        verbose (bool, optional): Enable verbose output. Default is False.
        ca_path (str, optional): Path to the CA certificate.
        mtls_p12_path (str, optional): Path to the mTLS PKCS#12 file.
        mtls_p12_password (str, optional): Password for the mTLS PKCS#12 file.

    Returns:
        dict: A dictionary containing the return code, error message (if any), and the result of the renewal process.

    Raises:
        ValueError: If neither `input_p12_path` and `input_p12_password` nor `config` are provided.
    """
    if not input_p12_path and not config:
        raise ValueError("Either input_p12_path and input_p12_password or config must be provided.")
    
    return perform_action(
        'xpki',
        'renew-cert',
        input_p12_path=input_p12_path,
        input_p12_password=input_p12_password,
        config=config,
        enable_logging=enable_logging,
        verbose=verbose,
        ca_path=ca_path,
        mtls_p12_path=mtls_p12_path,
        mtls_p12_password=mtls_p12_password
    )

def print_xpki_cert(input_p12_path: str = None, input_p12_password: str = None, config: str = None, enable_logging: bool = False, verbose: bool = False):
    """
    Print the details of an xPKI certificate.

    This function prints the details of an xPKI certificate. Either `input_p12_path` and `input_p12_password` must be provided, or a `config` file that contains these details.

    Args:
        input_p12_path (str, optional): Path to the input PKCS#12 file. Required if `config` is not provided.
        input_p12_password (str, optional): Password for the input PKCS#12 file. Required if `config` is not provided.
        config (str, optional): Path to the configuration file that contains the required details.
        enable_logging (bool): Enable logging output. Default is False.
        verbose (bool, optional): Enable verbose output. Default is False.

    Returns:
        dict: A dictionary containing the return code, error message (if any), and the xPKI certificate details in base64-encoded DER format.

    Raises:
        ValueError: If neither `input_p12_path` and `input_p12_password` nor `config` are provided.
    """
    if not input_p12_path and not config:
        raise ValueError("Either input_p12_path and input_p12_password or config must be provided.")
    
    return perform_action(
        'xpki',
        'print-cert',
        input_p12_path=input_p12_path,
        input_p12_password=input_p12_password,
        config=config,
        enable_logging=enable_logging,
        verbose=verbose
    )

def revoke_xpki_cert(input_p12_path: str = None, input_p12_password: str = None, config: str = None, enable_logging: bool = False, verbose: bool = False, ca_path: str = None, mtls_p12_path: str = None, mtls_p12_password: str = None):
    """
    Revoke an xPKI certificate.

    This function revokes an xPKI certificate. 
    
    Either `input_p12_path` and `input_p12_password` must be provided, or a `config` file that contains these details.

    Args:
        input_p12_path (str, optional): Path to the input PKCS#12 file. Required if `config` is not provided.
        input_p12_password (str, optional): Password for the input PKCS#12 file. Required if `config` is not provided.
        config (str, optional): Path to the configuration file that contains the required details.
        enable_logging (bool): Enable logging output. Default is False.
        verbose (bool, optional): Enable verbose output. Default is False.
        ca_path (str, optional): Path to the CA certificate.
        mtls_p12_path (str, optional): Path to the mTLS PKCS#12 file.
        mtls_p12_password (str, optional): Password for the mTLS PKCS#12 file.

    Returns:
        dict: A dictionary containing the return code, error message (if any), and the result of the revocation process.

    Raises:
        ValueError: If neither `input_p12_path` and `input_p12_password` nor `config` are provided.
    """
    if not input_p12_path and not config:
        raise ValueError("Either input_p12_path and input_p12_password or config must be provided.")
    
    return perform_action(
        'xpki',
        'revoke-cert',
        input_p12_path=input_p12_path,
        input_p12_password=input_p12_password,
        config=config,
        enable_logging=enable_logging,
        verbose=verbose,
        ca_path=ca_path,
        mtls_p12_path=mtls_p12_path,
        mtls_p12_password=mtls_p12_password
    )

def get_crt_token(input_p12_path: str = None, input_p12_password: str = None, config: str = None, enable_logging: bool = False, verbose: bool = False, auth_type: str = None, auth_token: str = None):
    """
    Get a certificate request token.

    The `auth_type` must be either "X509" or "SAT". 
    
    If `auth_type` is "X509", `input_p12_path` and `input_p12_password` must be provided. 
    
    If `auth_type` is "SAT", `auth_token` must be provided.
    
    Alternatively, these values can be provided in a `config` file.

    Args:
        input_p12_path (str, optional): Path to the input PKCS#12 file. Required if `auth_type` is "X509".
        input_p12_password (str, optional): Password for the input PKCS#12 file. Required if `auth_type` is "X509".
        config (str, optional): Path to the configuration file that contains the required details.
        enable_logging (bool): Enable logging output. Default is False.
        verbose (bool, optional): Enable verbose output. Default is False.
        auth_type (str, optional): The authentication type. Must be "X509" or "SAT".
        auth_token (str, optional): The authentication token. Required if `auth_type` is "SAT".

    Returns:
        dict: A dictionary containing the return code, error message (if any), and the certificate request token.

    Raises:
        ValueError: If `auth_type` is not "X509" or "SAT".
        ValueError: If `auth_type` is "X509" and `input_p12_path` or `input_p12_password` is not provided.
        ValueError: If `auth_type` is "SAT" and `auth_token` is not provided.
    """
    if auth_type not in ["X509", "SAT"]:
        raise ValueError("auth_type must be 'X509' or 'SAT'")
    if auth_type == "X509" and (not input_p12_path or not input_p12_password):
        raise ValueError("If auth_type is 'X509', input_p12_path and input_p12_password must be provided.")
    if auth_type == "SAT" and not auth_token:
        raise ValueError("If auth_type is 'SAT', auth_token must be provided.")
    
    return perform_action(
        'xpki',
        'get-crt-token',
        input_p12_path=input_p12_path,
        input_p12_password=input_p12_password,
        config=config,
        enable_logging=enable_logging,
        verbose=verbose,
        auth_type=map_to_xpki_auth_type(auth_type),
        auth_token=auth_token
    )

def get_xpki_cert(input_p12_path: str = None, input_p12_password: str = None, config: str = None, enable_logging: bool = False, verbose: bool = None, auth_type: str = None, auth_token: str = None, crt: str = None, output_p12_path: str = None, output_p12_password: str = None, overwrite_p12: bool = None, profile_name: str = None, validity_days: int = None, ca_path: str = None, mtls_p12_path: str = None, mtls_p12_password: str = None):
    """
    Get an xPKI certificate.

    This function retrieves an xPKI certificate and saves it to the local filesystem. 
    
    The `auth_type` must be either "X509" or "SAT". 
    
    If `auth_type` is "X509", `input_p12_path` and `input_p12_password` must be provided. 
    
    If `auth_type` is "SAT", `auth_token` must be provided.

    Args:
        input_p12_path (str, optional): Path to the input PKCS#12 file. Required if `auth_type` is "X509".
        input_p12_password (str, optional): Password for the input PKCS#12 file. Required if `auth_type` is "X509".
        config (str, optional): Path to the configuration file that can contain these arguments.
        enable_logging (bool): Enable logging output. Default is False.
        verbose (bool, optional): Enable verbose output. Default is False.
        auth_type (str, optional): The authentication type. Must be "X509" or "SAT".
        auth_token (str, optional): The authentication token. Required if `auth_type` is "SAT".
        crt (str, optional): The certificate request token.
        output_p12_path (str, optional): Path to the output PKCS#12 file (i.e. where certificate is saved).
        output_p12_password (str, optional): Password for the output PKCS#12 file.
        overwrite_p12 (bool, optional): Whether to overwrite if PKCS#12 file already exists. Default is False.
        profile_name (str, optional): The profile name for the certificate.
        validity_days (int, optional): The number of days the certificate is valid for.
        ca_path (str, optional): Path to the CA certificate.
        mtls_p12_path (str, optional): Path to the mTLS PKCS#12 file.
        mtls_p12_password (str, optional): Password for the mTLS PKCS#12 file.

    Returns:
        dict: A dictionary containing the return code, error message (if any), and the certificate information.

    Raises:
        ValueError: If `auth_type` is not "X509" or "SAT".
    """
    
    validate_auth_type(auth_type)
    
    return perform_action(
        'xpki',
        'get-cert',
        input_p12_path=expand_path(input_p12_path),
        input_p12_password=input_p12_password,
        config=expand_path(config),
        enable_logging=enable_logging,
        verbose=verbose,
        auth_type=map_to_xpki_auth_type(auth_type),
        auth_token=auth_token,
        crt=crt,
        output_p12_path=expand_path(output_p12_path),
        output_p12_password=output_p12_password,
        overwrite_p12=overwrite_p12,
        profile_name=profile_name,
        validity_days=validity_days,
        ca_path=ca_path,
        mtls_p12_path=expand_path(mtls_p12_path),
        mtls_p12_password=mtls_p12_password
    )
    
def get_sectigo_cert(auth_token: str = None, source: str = None, config: str = None, enable_logging: bool = False, verbose: bool = None, owner_last_name: str = None, owner_first_name: str = None, owner_phone_number: str = None, owner_email: str = None, group_name: str = None, group_email: str = None, common_name: str = None, id: str = None, employee_type: str = None, server_platform: str = None, sensitive: bool = None, project_name: str = None, business_justification: str = None, subject_alt_names: list = None, ip_addresses: list = None):
    """
    Get a Sectigo certificate.

    This function retrieves a Sectigo certificate. All parameters are required.

    Args:
        auth_token (str): Azure CRT Token or SAT token.
        source (str): The source systemId - Ex: ProjectName.
        config (str): Path to the configuration file that can contain these arguments.
        enable_logging (bool): Enable logging output. Default is False.
        verbose (bool): Enable verbose output. Default is False.
        owner_last_name (str): The owner's last name.
        owner_first_name (str): The owner's first name.
        owner_phone_number (str): The owner's phone number. Ex Format: 9999999999
        owner_email (str): The owner's email address.
        group_name (str): The email distro name. This should match one of your associated AD groups. 
        group_email (str): The email distro's address. This should match one of your associated AD group emails. 
        common_name (str): The common name for the certificate. This should match CN of CSR.
        id (str): The user's NTID (requestor). 
        employee_type (str): The owner's employee type. Options are 'fte', 'contractor', and 'associate'.
        server_platform (str): ServerType where Certificate intended to use.
        sensitive (bool): Whether the certificate is sensitive.
        project_name (str): The name of the project where the certificate will be used.
        business_justification (str): The purpose of the certificate.
        subject_alt_names (list): The list of valid DNS names to be added on SAN, pass empty array [] if none.
        ip_addresses (list): The list of valid IP address to be added on SAN, pass empty array [] if none.

    Returns:
        dict: A dictionary containing the return code, error message (if any), and the Sectigo certificate.

    Raises:
        ValueError: If any required parameter is not provided.
    """
    
    required_params = [
        auth_token, source, owner_last_name, owner_first_name, owner_phone_number, owner_email,
        group_name, group_email, common_name, id, employee_type, server_platform, sensitive,
        project_name, business_justification, subject_alt_names, ip_addresses
    ]
    
    if any(param is None for param in required_params) and not config:
        raise ValueError("All parameters are required.")
    
    return perform_action(
        'sectigo',
        'get-cert',
        auth_token=auth_token,
        source=source,
        config=expand_path(config),
        enable_logging=enable_logging,
        verbose=verbose,
        owner_last_name=owner_last_name,
        owner_first_name=owner_first_name,
        owner_phone_number=owner_phone_number,
        owner_email=owner_email,
        group_name=group_name,
        group_email=group_email,
        common_name=common_name,
        id=id,
        employee_type=employee_type,
        server_platform=server_platform,
        sensitive=sensitive,
        project_name=project_name,
        business_justification=business_justification,
        subject_alt_names=subject_alt_names,
        ip_addresses=ip_addresses
    )

def search_sectigo_cert(auth_token: str = None, source: str = None, config: str = None, enable_logging: bool = False, verbose: bool = None, group_name: str = None, group_email: str = None, status: str = None, common_name: str = None, offset: int = None, limit: int = None, start_date: str = None, end_date: str = None, certificate_id: int = None, validity_start_date: str = None, cert_order_id: str = None, validity_end_date: str = None, is_cn_in_san: bool = None, request_type: str = None, timestamp: str = None):
    """
    Search for Sectigo certificates.

    This function fetches Sectigo certificates based on arguments supplied. 
    
    Apart from 'auth_token' and 'source', all other parameters are optional and can be used to filter the search results.

    Args:
        auth_token (str): Azure CRT Token or SAT token.
        source (str): The source systemId - Ex: ProjectName.
        config (str): Path to the configuration file that can contain these arguments.
        enable_logging (bool): Enable logging output. Default is False.
        verbose (bool): Enable verbose output. Default is False.
        group_name (str): The email distro name. This should match one of your associated AD groups. 
        group_email (str): The email distro's address. This should match one of your associated AD group emails. 
        status (str): Options are 'created', 'revoked', 'approved', 'signed', 'signing requested', 'on hold', 'rejected', 'revocation requested'.
        common_name (str): The common name for the certificate. This should match CN of CSR.
        offset (int): To display the next set of records. 
        limit (int): To identify the number of results to be fetched. Default is 10.
        start_date (str): To fetch the created certificates starting from date given. ex: 2021-07-30
        end_date (str): To fetch created certificates until date given. ex: 2021-07-30
        certificate_id (int): To fetch certificate with specific certificateID.
        validity_start_date (str): To fetch the created certificates valid on or after the date given. Ex: 2021-07-30
        cert_order_id (str): Options are 'leaf', 'ica', 'root'.
        validity_end_date (str): To fetch the created certificates valid up to the date given. Ex: 2021-07-30
        is_cn_in_san (bool): Whether the common name is in the SAN.
        request_type (str): To fetch certificates based on type of requests via: ACME, API, WEB, XCM.
        timestamp (str): to fetch certificates based on timestamp types. Options are 'createdTimestamp', 'approvedTimestamp', 'signedTimestamp', 'rejectedTimestamp', 'revokedTimestamp'

    Returns:
        dict: A dictionary containing the return code, error message (if any), and the search results.

    Raises:
        ValueError: If any required parameter is not provided.
    """
    required_params = [auth_token, source]

    if any(param is None for param in required_params) and not config:
        raise ValueError("auth_token and source are required.")

    return perform_action(
        'sectigo',
        'search-cert',
        auth_token=auth_token,
        source=source,
        config=expand_path(config),
        enable_logging=enable_logging,
        verbose=verbose,
        group_name=group_name,
        group_email=group_email,
        status=status,
        common_name=common_name,
        offset=offset,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        certificate_id=certificate_id,
        validity_start_date=validity_start_date,
        cert_order_id=cert_order_id,
        validity_end_date=validity_end_date,
        is_cn_in_san=is_cn_in_san,
        request_type=request_type,
        timestamp=timestamp
    )

def renew_sectigo_cert(auth_token: str = None, source: str = None, config: str = None, enable_logging: bool = False, verbose: bool = None, common_name: str = None, serial_number: int = None, certificate_id: int = None, requestor_email: str = None):
    """
    Renew a Sectigo certificate.

    This function renews a Sectigo certificate. 
    
    `auth_token`, `source`, `common_name`, and `requestor_email` are required. 
    
    Additionally, one of `serial_number` or `certificate_id` must be provided.

    Args:
        auth_token (str): Azure CRT Token or SAT token.
        source (str): The source systemId - Ex: ProjectName.
        config (str): Path to the configuration file that can contain these arguments.
        enable_logging (bool): Enable logging output. Default is False.
        verbose (bool): Enable verbose output. Default is False.
        common_name (str): The common name for the certificate. This should match CN of CSR.
        serial_number (int): The serial number of the certificate. To get serial number 'openssl x509 -noout -in CERT.pem -serial'
        certificate_id (int): The ID of the certificate. 
        requestor_email (str): The email of the requestor.

    Returns:
        dict: A dictionary containing the return code, error message (if any), and the renewed Sectigo certificate.

    Raises:
        ValueError: If any required parameter is not provided or if neither `serial_number` nor `certificate_id` is provided.
    """
    
    required_params = [auth_token, source, common_name, serial_number, certificate_id, requestor_email]

    if any(param is None for param in required_params) and not config:
        raise ValueError("All parameters are required.")
    
    return perform_action(
        'sectigo',
        'renew-cert',
        auth_token=auth_token,
        source=source,
        config=expand_path(config),
        enable_logging=enable_logging,
        verbose=verbose,
        common_name=common_name,
        serial_number=serial_number,
        certificate_id=certificate_id,
        requestor_email=requestor_email
    )

def revoke_sectigo_cert(auth_token: str = None, source: str = None, config: str = None, enable_logging: bool = False, verbose: bool = None, common_name: str = None, serial_number: int = None, certificate_id: int = None, requestor_email: str = None, revocation_request_reason: str = None):
    """
    Revoke a Sectigo certificate.

    This function revokes a Sectigo certificate. 
    
    `auth_token`, `source`, `common_name`, `requestor_email`, and `revocation_request_reason` are required. 
    
    Additionally, one of `serial_number` or `certificate_id` must be provided.

    Args:
        auth_token (str): Azure CRT Token or SAT token.
        source (str): The source systemId - Ex: ProjectName.
        config (str): Path to the configuration file that can contain these arguments.
        enable_logging (bool): Enable logging output. Default is False.
        verbose (bool): Enable verbose output. Default is False.
        common_name (str): The common name for the certificate. This should match CN of CSR.
        serial_number (int): The serial number of the certificate. To get serial number 'openssl x509 -noout -in CERT.pem -serial'
        certificate_id (int): The ID of the certificate.
        requestor_email (str): The email of the requestor.
        revocation_request_reason (str): The reason for the revocation request.

    Returns:
        dict: A dictionary containing the return code, error message (if any), and the result of the revocation process.

    Raises:
        ValueError: If any required parameter is not provided or if neither `serial_number` nor `certificate_id` is provided.
    """
    
    required_params = [auth_token, source, common_name, requestor_email, revocation_request_reason]

    if any(param is None for param in required_params) and not config:
        raise ValueError("auth_token, source, common_name, requestor_email, and revocation_request_reason are required.")
    if (serial_number is None and certificate_id is None) and not config:
        raise ValueError("One of serial_number or certificate_id must be provided.")
    
    return perform_action(
        'sectigo',
        'revoke-cert',
        auth_token=auth_token,
        source=source,
        config=expand_path(config),
        enable_logging=enable_logging,
        verbose=verbose,
        common_name=common_name,
        serial_number=serial_number,
        certificate_id=certificate_id,
        requestor_email=requestor_email,
        revocation_request_reason=revocation_request_reason
    )

def perform_action(cert_type: str, command: str, enable_logging: bool, **kwargs):
    os.environ["CERT_TYPE"] = cert_type
    
    args = {'command': command}
    args.update(kwargs)
    
    if enable_logging:
        log_setup(Namespace(**args))
    info = xpki_perform(Namespace(**args))
    os.environ.pop("CERT_TYPE")
    return info

def validate_auth_type(auth_type: str):
    if auth_type.upper() not in ['X509', 'SAT']:
        raise ValueError("auth_type must be 'X509' or 'SAT'")
