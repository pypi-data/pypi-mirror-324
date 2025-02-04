from argparse import ArgumentParser, FileType
import os

def cli_setup():
    
    cert_type = os.environ.get('CERT_TYPE')
      
    if cert_type and cert_type.lower() in ('xpki', 'sectigo'):
        cert_type = cert_type.lower()
    elif cert_type:
        print(f"Environment variable CERT_TYPE was set to this invalid value: \"{cert_type}\". Set to desired certificate type. \n\nOptions are: \n1) xpki \n2) sectigo")
        exit()
    else:
        print("Environment variable CERT_TYPE was unset. Set to desired certificate type. \n\nOptions are: \n1) xpki \n2) sectigo")
        exit()
    
    arg_parser = ArgumentParser()
    subparsers = arg_parser.add_subparsers(dest='command', required=True)

    if cert_type == 'xpki':
        base_options = ArgumentParser()
        base_options.add_argument('--input-p12-path', '-k', type=FileType('r'))
        base_options.add_argument('--input-p12-password', '-p')
        base_options.add_argument('--config', '-L', default='pycertifier.cfg')
        base_options.add_argument('--verbose', '-v', action='store_true')
        
        get_crt_token_options = ArgumentParser(add_help=False)
        get_crt_token_options.add_argument('--auth-type', '-X', choices=['X509', 'SAT'])
        get_crt_token_options.add_argument('--auth-token', '-S')

        get_cert_options = ArgumentParser(add_help=False)
        get_cert_options.add_argument('--crt', '-T')
        get_cert_options.add_argument('--output-p12-path', '-o')
        get_cert_options.add_argument('--output-p12-password', '-w')
        get_cert_options.add_argument('--overwrite-p12', '-f', action='store_true')
        get_cert_options.add_argument('--profile-name', '-P')

        validity_days_option = ArgumentParser(add_help=False)
        validity_days_option.add_argument('--validity_days', '-t')

        ca_path_option = ArgumentParser(add_help=False)
        ca_path_option.add_argument('--ca-path', '-c', type=FileType('r'))

        mtls_options = ArgumentParser(add_help=False)
        mtls_options.add_argument('--mtls-p12-path', '-q', type=FileType('r'))
        mtls_options.add_argument('--mtls-p12-password', '-Q', default='changeit')

        autorenew_options = ArgumentParser(add_help=False)
        autorenew_options.add_argument('--config', '-c', metavar='path', help='Read configuration from the file at provided path')
        autorenew_options.add_argument('--log-file', '-l', metavar='path', help='Write logs to the file', type=FileType('a+'))
        autorenew_options.add_argument('--daemon', '-d', help='Daemonize this application', action='store_true')
        autorenew_options.add_argument('--pid-file', '-p', metavar='path', help='Path to PID file used by daemonized app')
        autorenew_options.add_argument('--cert-paths', '-x', metavar='dir:list', help='Directory list where certificates shall be monitored for expiry/renewal', required=True)
        autorenew_options.add_argument('--autorenew-interval', '-i', metavar='interval', help='Time in seconds to wait before next renewal attempt. Default is 24 hours.', type=int, default=86400)
        autorenew_options.add_argument('--key-list', '-k', metavar='path', help='Key list corresponding to passwords for certificates in specified directories', type=str, required=True)
        autorenew_options.add_argument('--attempt-threshold', '-a', metavar='threshold', help='Number of tries if no valid certificates are present before exiting. Default is 3.', type=int, default=3)
                
        subparsers.add_parser('get-cert', parents=[base_options, get_crt_token_options, get_cert_options, 
                                        validity_days_option, ca_path_option, mtls_options], add_help=False, help="Fetch an xPKI certificate")
        
        subparsers.add_parser('get-crt-token', parents=[base_options, get_crt_token_options], add_help=False, help="Fetch a certificate request token. Optionally can be used in 'get-cert' command")

        subparsers.add_parser('get-cert-status', parents=[base_options, ca_path_option, mtls_options], add_help=False, help="Check the status of an xPKI certificate (good, revoked, unknown)")
        
        subparsers.add_parser('get-cert-validity', parents=[base_options, ca_path_option], add_help=False, help="Get the validity of an xPKI certificate (valid, about to expire, not yet valid, expired)")
        
        subparsers.add_parser('renew-cert', parents=[base_options, ca_path_option, mtls_options], add_help=False, help="Renew an xPKI certificate")

        subparsers.add_parser('print-cert', parents=[base_options], add_help=False, help="Print information about an xPKI certificate")
        
        subparsers.add_parser('revoke-cert', parents=[base_options, ca_path_option, mtls_options], add_help=False, help="Revoke an xPKI certificate")
        
        subparsers.add_parser('autorenew', parents=[autorenew_options, mtls_options], help="Set up an autorenewal daemon to handle certificate renewal")

    elif cert_type == 'sectigo':
        base_options = ArgumentParser(add_help=False)  
        base_options.add_argument('--auth-token', '-at')
        base_options.add_argument('--source', '-src', type=str)
        base_options.add_argument('--config', '-cfg', default='pycertifier.cfg')
        base_options.add_argument('--verbose', '-v', action='store_true')

        lookup_options = ArgumentParser(add_help=False)
        lookup_options.add_argument('--common-name', '-cn', type=str)        
        lookup_options.add_argument('--serial-number', '-sn', type=str)
        lookup_options.add_argument('--certificate-id', '-cid', type=int)
        lookup_options.add_argument('--requestor-email', '-re', type=str)

        owner_info_options = ArgumentParser(add_help=False)
        owner_info_options.add_argument('--owner-last-name', '-oln', type=str)
        owner_info_options.add_argument('--owner-first-name', '-ofn', type=str)
        owner_info_options.add_argument('--owner-phone-number', '-op', type=str)
        owner_info_options.add_argument('--owner-email', '-oe', type=str)    

        group_info_options = ArgumentParser(add_help=False)
        group_info_options.add_argument('--group-name', '-gn', type=str)
        group_info_options.add_argument('--group-email', '-ge', type=str)

        sectigo_get_cert_options = ArgumentParser(add_help=False)
        sectigo_get_cert_options.add_argument('--common-name', '-cn', type=str)
        sectigo_get_cert_options.add_argument('--id', '-id', type=str)
        sectigo_get_cert_options.add_argument('--employee-type', '-et', choices=['fte', 'contractor', 'associate'], type=str)
        sectigo_get_cert_options.add_argument('--server-platform', '-sp', action='store_true')
        sectigo_get_cert_options.add_argument('--sensitive', '-s', action='store_true')
        sectigo_get_cert_options.add_argument('--project-name', '-pn', type=str)
        sectigo_get_cert_options.add_argument('--business-justification', '-j', type=str)
        sectigo_get_cert_options.add_argument('--subject-alt-names', '-san', default=[], type=str)
        sectigo_get_cert_options.add_argument('--ip-addresses', '-ip', default=[], type=str)
        
        sectigo_search_cert_options = ArgumentParser(add_help=False)
        sectigo_search_cert_options.add_argument('--status', '-s', type=str)
        sectigo_search_cert_options.add_argument('--common-name', '-cn', type=str)
        sectigo_search_cert_options.add_argument('--offset', '-off', type=str)
        sectigo_search_cert_options.add_argument('--limit', '-l', type=str)
        sectigo_search_cert_options.add_argument('--start-date', '-sd', type=str)
        sectigo_search_cert_options.add_argument('--end-date', '-ed', type=str)
        sectigo_search_cert_options.add_argument('--certificate-id', '-cid', type=str)
        sectigo_search_cert_options.add_argument('--validity-start-date', '-vsd', type=str)
        sectigo_search_cert_options.add_argument('--cert-order', '-co', type=str)
        sectigo_search_cert_options.add_argument('--validity-end-date', '-ved', type=str)
        sectigo_search_cert_options.add_argument('--is-cn-in-san', '-cis', default="NO", choices=['NO', 'YES'], type=str)
        sectigo_search_cert_options.add_argument('--request-type', '-rt', type=str)
        sectigo_search_cert_options.add_argument('--timestamp', '-t', type=str)
                
        sectigo_revoke_cert_options = ArgumentParser(add_help=False)
        sectigo_revoke_cert_options.add_argument('--revocation-request-reason', '-rsn', type=str)

        subparsers.add_parser('get-cert', parents=[base_options, owner_info_options, group_info_options, sectigo_get_cert_options], help="Fetch a Sectigo certificate")
        
        subparsers.add_parser('search-cert', parents=[base_options, group_info_options, sectigo_search_cert_options], help="Query for Sectigo certificates based on provided arguments")
        
        subparsers.add_parser('renew-cert', parents=[base_options, lookup_options], help="Renew a Sectigo certificate")
        
        subparsers.add_parser('revoke-cert', parents=[base_options, lookup_options, sectigo_revoke_cert_options], help="Revoke a Sectigo certificate")
        
    return arg_parser