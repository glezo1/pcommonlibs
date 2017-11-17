import inspect
import traceback
import json

class StaticUtils(object):
    #---------------------------------------------------------------------
    @staticmethod
    def is_primitive(something):
        primitives=(int,float,str,bool)
        return isinstance(something,primitives)
    #---------------------------------------------------------------------
    @staticmethod
    def is_object_instance(something):
        return inspect.isclass(type(something)) and not type(something) == type and not StaticUtils.is_primitive(something)
    #---------------------------------------------------------------------
    @staticmethod
    def function_brief(class_methods,arguments_dict):
        arguments_dict.pop('self');      
        for k,v in arguments_dict.items():
            if(StaticUtils.is_object_instance(v)):
                class_name=v.__class__.__name__
                arguments_dict[k]=class_name
        arguments_string=json.dumps(arguments_dict);
        return class_methods+'('+arguments_string+')'
    #---------------------------------------------------------------------
    @staticmethod
    def exception_to_string(excp):
        stack = traceback.extract_stack()[:-3] + traceback.extract_tb(excp.__traceback__)  # add limit=?? 
        pretty = traceback.format_list(stack)
        return ''.join(pretty) + '\n  {} {}'.format(excp.__class__,excp)
    #---------------------------------------------------------------------
    '''
    @staticmethod
    def get_browser_active_tab_url(browser_getwindowtext,sendkeys_actions):
        winsound.Beep(400,400)
        time.sleep(1)
        
        current_window_handler      =   win32gui.GetForegroundWindow()
        current_window_text         =   win32gui.GetWindowText(current_window_handler)
        if(not re.match(browser_getwindowtext,current_window_text)):
            print('browser_getwindowtext doesnt match')
            return None
        win32clipboard.OpenClipboard()
        previous_clipboard_format_string    =   None
        previous_clipboard_format_int       =   None
        previous_clipboard_content          =   None
        there_is_data_in_previous_clipboard =   False
        formats = {val: name for name, val in vars(win32clipboard).items() if name.startswith('CF_')}
        format_number = 0
        while(True):
            format_number = win32clipboard.EnumClipboardFormats(format_number)
            if(format_number == 0): 
                break
            if(format_number in formats):
                if(previous_clipboard_format_string==None):
                    previous_clipboard_format_string = formats[format_number]
                    previous_clipboard_format_int    = format_number
                    #print(previous_clipboard_format_string)
        if(previous_clipboard_format_int!=None):
            there_is_data_in_previous_clipboard=True
            previous_clipboard_content = win32clipboard.GetClipboardData(previous_clipboard_format_int)
        
        #it seems that, unless clipboard content is text, I wont be able to restore.
        if(previous_clipboard_format_string not in [None,'CF_UNICODETEXT','CF_LOCALE','CF_TEXT','CF_OEMTEXT']):
            print('wont be able to restore clipboard')
            win32clipboard.CloseClipboard()
            return None

        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
        
        SendKeysCtypes.SendKeys(sendkeys_actions,pause=0.01)

        win32clipboard.OpenClipboard()
        #if url bar is empty (e.g., new tab) this will throw an exception
        active_url = None
        try:
            active_url = win32clipboard.GetClipboardData(win32con.CF_TEXT)
        except:
            pass
        win32clipboard.EmptyClipboard()
        if(there_is_data_in_previous_clipboard):
            win32clipboard.SetClipboardData(previous_clipboard_format_int,previous_clipboard_content)
        win32clipboard.CloseClipboard()  
        result = {
                'url'       :   active_url
                ,'title'    :   None
            }
        return result
    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------
    '''
