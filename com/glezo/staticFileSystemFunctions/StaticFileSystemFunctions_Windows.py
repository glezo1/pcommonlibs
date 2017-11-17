
import datetime
import pytz
import os
from os import listdir
from os.path import join
import pywintypes
import win32file
import win32con

from CMD_Wrapper import CMD_Wrapper

class StaticFileSystemFunctions_Windows(object):

    #---------------------------------------------------------------------
    @staticmethod
    def hide(path,literals_provider):
        if(path.find(' ')!=-1):
            #os.system(literals_provider.get_atrrib_plus_h()+' "'+path+'"')
            CMD_Wrapper.subprocess_check_output([literals_provider.get_attribdotexe(),literals_provider.get_plush(),'"'+path+'"'])
        else:
            #os.system(literals_provider.get_atrrib_plus_h()+' '+path)
            CMD_Wrapper.subprocess_check_output([literals_provider.get_attribdotexe(),literals_provider.get_plush(),path])
    #---------------------------------------------------------------------
    @staticmethod
    def unhide(path,literals_provider):
        os.system(literals_provider.get_attrib_minus_h()+' '+path)
    #---------------------------------------------------------------------
    @staticmethod
    def recursive_hide(path,literals_provider):
        if(os.path.isfile(path)):
            StaticFileSystemFunctions_Windows.hide(path,literals_provider)
        else:
            StaticFileSystemFunctions_Windows.hide(path,literals_provider)
            for f in listdir(path):
                current_object=join(path,f)
                #recursive call ,wether its file or dir
                StaticFileSystemFunctions_Windows.recursive_hide(current_object,literals_provider)
    #---------------------------------------------------------------------
    @staticmethod
    def isHidden(path,literals_provider):
        #cmd_output = subprocess.check_output([literals_provider.get_attrib(), path])
        cmd_output = CMD_Wrapper.subprocess_check_output([literals_provider.get_attribdotexe(), path])
        cmd_output_string = cmd_output.decode("utf-8") 
        return len(cmd_output_string)>4 and cmd_output_string[4]=='H'
    #---------------------------------------------------------------------
    @staticmethod
    def change_file_ctime(fname, newtime_string):
        newtime     =   datetime.datetime.strptime(newtime_string,'%Y-%m-%d %H:%M:%S')
        timezone    =   pytz.timezone('Europe/Lisbon')
        newtime     =   timezone.localize(newtime)
        wintime     =   pywintypes.Time(newtime)
        winfile     =   win32file.CreateFile(
            fname, win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None, win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL, None)
        win32file.SetFileTime(winfile, wintime, None, None)
        winfile.close()
    #------------------------------------------------------------------------------------------------
    @staticmethod
    def change_file_mtime(fname, newtime_string):
        newtime     =   datetime.datetime.strptime(newtime_string,'%Y-%m-%d %H:%M:%S')
        timezone    =   pytz.timezone('Europe/Lisbon')
        newtime     =   timezone.localize(newtime)
        wintime     =   pywintypes.Time(newtime)
        winfile     =   win32file.CreateFile(
            fname, win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None, win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL, None)
        win32file.SetFileTime(winfile, None, None, wintime)
        winfile.close()
    #---------------------------------------------------------------------
