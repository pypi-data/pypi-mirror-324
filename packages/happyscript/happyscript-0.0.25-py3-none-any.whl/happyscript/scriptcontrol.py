#   ____       _    _                                     
#  |  _ \  ___| | _(_)_ __ ___   ___    Copyright  | Title   : Object for some flow control during a script
#  | | | |/ _ \ |/ / | '_ ` _ \ / _ \   (c) 2020   | Project : Oce BE-Board
#  | |_| |  __/   <| | | | | | | (_) |   Dekimo    | Authors : MVR
#  |____/ \___|_|\_\_|_| |_| |_|\___/   Products   | Created : 5/2/2020
#__________________________________________________|_________________________________________________________

# import wx
import time

from .scriptexceptions import ScriptUserAbortException

class ScriptControl:
    ''' object to allow flow control during script execution
    '''
    def __init__(self):
        self.m_stop_script = False               # must the script stop ?
        self._is_busy = False
        self._script_runner = None

    def set_script_runner(self, runner):
        ''' sets the ScriptRunner object that is used for running scripts
        '''
        self._script_runner = runner

    def set_busy(self, is_busy):
        self._is_busy = is_busy
        self.m_stop_script = False

    def is_busy(self):
        return self._is_busy

    def stop(self):
        if self._is_busy:
            print("'stop' flag is set.  Scripts may stop soon.")
        else:
            print("Normally no script is active, but I'll set the 'stop' flag anyway.")
        self.m_stop_script = True

    def ok(self):
        ''' For use in a loop with blocking functions.  ok() will return True until the 'stop' button 
            is pressed.  Exit your script loop when ok() returns False
        '''
        # wx.Yield()
        return not self.m_stop_script
    
    def check(self):
        ''' For use in a loop with blocking functions.  check() will raise an exception when the 'abort'
            button is pressed
        '''
        # wx.Yield()
        if self.m_stop_script:
            raise ScriptUserAbortException( "Script stopping on user request" )

    def sleep(self, time_in_seconds):
        ''' Allows a script to pause for some time, while still providing a fast "abort".
        '''
        t = time_in_seconds
        
        # wx.Yield()
        
        while t>0:
            if t > 0.5:
                time.sleep(0.5)
            else:
                time.sleep(t)
            t = t-0.5
            # wx.Yield()
            if self.m_stop_script:
                raise ScriptUserAbortException( "Script stopping on user request" )

    def run(self, script_name, **argv):
        ''' Execute a script from within another script.
        '''
        assert self._script_runner is not None, "Internal error: scriptrunner is not set"
        return self._script_runner.run_script(script_name, **argv)

    def run_parallel(self, func, parname, parvalues, **extra_params):
        ''' excecute a function in parallel using different values for a given parameter
        '''
        return self._script_runner.run_parallel(func, parname, parvalues, **extra_params)