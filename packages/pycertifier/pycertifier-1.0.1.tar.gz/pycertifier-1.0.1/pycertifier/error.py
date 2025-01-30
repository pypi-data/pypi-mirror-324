
from .log import log, log_destroy

from inspect import getframeinfo, currentframe
import json

class CertifierError:
    def __init__(self, app_error_code = 0, app_error_msg = None, output = None):
        self.application_error_code = app_error_code
        self.application_error_msg = app_error_msg
        self.output = output
        
    def clear(self):
        self.application_error_code = 0
        self.application_error_msg = None
        self.output = None

def gen_application_error_msg(error_message: str, resp):
    '''
    Formats application error message to additionally include info about method, file, and line # where error occurred. Also includes HTTP response if passed
    '''
    application_error_msg = {
        "message": error_message,
        "method": str(getframeinfo(currentframe().f_back.f_back).function) ,
        "file": str(getframeinfo(currentframe().f_back.f_back).filename),
        "line": str(getframeinfo(currentframe().f_back.f_back).lineno),
    }

    if resp != None:        
        replacements = [('"', ''), (':', ': '), (',', ', ')]
        
        body = resp.text
        
        for old, new in replacements:
            body = body.replace(old, new)
        
        application_error_msg.update({"http_response": body})
    
    return application_error_msg

def certifier_create_info(last_error: CertifierError, return_code: int, output: str):
    '''
    Handles final printing/logging for all commands. Provides end return code and relevant error codes and messages from application
        
    Dictionary with return code, error message, and relevant output is returned on success
    
    Program will exit on failure
    '''
    root_object = {
        "return_code": return_code,
        "error": last_error.application_error_msg,
        }
    
    if output:
        root_object.update({"output": output})

    serialized_string = json.dumps(root_object, indent=4)
    
    if root_object["error"]:
        log(f"\nInfo: {serialized_string}", "ERROR")
        log_destroy()
        exit()
    else:
        log(f"\nInfo: {serialized_string}", "INFO")
        log_destroy()
        return root_object