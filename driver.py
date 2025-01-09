import re

from Exscript.protocols.drivers.driver import Driver

_prompt_re = [re.compile(r'\r*\n*\w*0/FMC[01]:atDR1\w*[#>] '),
              re.compile(r'\r*\n*\w*0/FMC[01]:atDR1-2\w*[#>] '),
              re.compile(r'\r\n0/ME[25][120]0[01]:atAR[12]\w*[#>] '),
              re.compile(r'Log'),
              re.compile(r'0/FMC[0|1]:atDR1#'),
              re.compile(r'0/FMC[0|1]:atDR1\(\S+\)#'),
              re.compile(r'0/ME5[1|2]00:ER0[5|6]#'),
              re.compile(r'0/ME5[1|2]00:atAR[1|2]\(\S+\)#'),
              re.compile(r'0/ME5[1|2]00:atAR[1|2]#'),]
_error_re = [re.compile(r'invalid command'),
             re.compile(r'unrecognized command'),
             re.compile(r'[U|u]nknown command'),
             re.compile(r'incomplete command'),
             re.compile(r'failed to open input file'),
             re.compile(r'No such file or directory'),
             re.compile(r'Error: Can\'t setup session, netconf server doesn\'t respond'), 
             re.compile(r'file not found'),
#             re.compile(r'\(offline mode\):at'),
             re.compile(r'Error: malloc failed'),
             re.compile(r'Error: Syntax error on line'),
             re.compile('Synchronization is in progress')]
_user_re = [re.compile(r'(^|[\r\n]+)User Name: *$'),
            re.compile(r'Username: *$'),
            re.compile(r'atAR[1|2] login:'),
            re.compile(r'ER0[5|6] login:'),
            re.compile(r'atDR1-2 login:'),
            re.compile(r'atDR1 login:')]
_password_re = [re.compile(r'(^|[\r\n]+)Password: *$')]
_login_error_re = [re.compile(r'press ENTER key to retry authentication'),
                   re.compile(r'authentication failed'),
                   re.compile('Detected speed: \d+'),
                   re.compile('press Enter twice to complete the detection process')]



_promptXR_re = [re.compile(r'\r*\n*\w*0/FMC[01]:atDR1\w*[#>] '),
              re.compile(r'\r\n0/ME5[12]00:atAR[12]\w*[#>] '),
              re.compile(r'RP/0/0/CPU0:XRv[2|3]#'),
              re.compile(r'RP/0/0/CPU0:XRv-Avtotests[2|3]'),]
_errorXR_re = [re.compile(r'invalid'),
             re.compile(r'unrecognized'),
             re.compile(r'Unknown command'),
             re.compile(r'incomplete'),
             re.compile(r'failed to open input file'),
             re.compile(r'No such file or directory'),
             re.compile(r'Failed to commit'),
             re.compile(r'Error: Can\'t setup session, netconf server doesn\'t respond'),
             re.compile('Synchronization is in progress')]
_userXR_re = [re.compile(r'(^|[\r\n]+)User Name: *$'),
            re.compile(r'Username: *$'),
            re.compile(r'at[AD]R[12] login:')]
_passwordXR_re = [re.compile(r'(^|[\r\n]+)Password: *$')]
_login_errorXR_re = [re.compile(r'press ENTER key to retry authentication'),
                   re.compile(r'authentication failed'),
                   re.compile('Detected speed: \d+'),
                   re.compile('press Enter twice to complete the detection process')]

_promptMES_re = [re.compile(r'\r*\n*\w*5324-at-stand-ethlab\w*[#>]'),
                 re.compile(r'.* local user table ACCEPTED.')]
_errorMES_re = [re.compile(r'% Unrecognized command'),
                re.compile(r'Server unreachable'),
                re.compile(r'Failed to connect server')]
_userMES_re = [re.compile(r'User Name:'),
               re.compile(r'(^|[\r\n]+)User Name:')]
_passwordMES_re = [re.compile(r'Password:')]
_login_errorMES_re = [re.compile(r'press ENTER key to retry authentication'),
                      re.compile(r'authentication failed')]

class ME5000CliDriver(Driver):
    def __init__(self):
        Driver.__init__(self, 'ME5000CliDriver')
        self.user_re = _user_re
        self.password_re = _password_re
        self.prompt_re = _prompt_re
        self.error_re = _error_re
        self.login_error_re = _login_error_re
#        self.states = _states_map
#        self.commands = _commands_map



class IOS_XR_CliDriver(Driver):
    def __init__(self):
        Driver.__init__(self, 'IOS_XR_CliDriver')
        self.user_re = _userXR_re
        self.password_re = _passwordXR_re
        self.prompt_re = _promptXR_re
        self.error_re = _errorXR_re
        self.login_error_re = _login_errorXR_re
        
class MES5324CliDriver(Driver):
    def __init__(self):
        Driver.__init__(self, 'MES5324CliDriver')
        self.user_re = _userMES_re
        self.password_re = _passwordMES_re
        self.prompt_re = _promptMES_re
        self.error_re = _errorMES_re
        self.login_error_re = _login_errorMES_re
        
