import string
import datetime

class StringUtils(object):
    #---------------------------------------------------------------------
    @staticmethod
    def is_decimal_number(string_value):
        try:
            int(string_value)
            return True
        except ValueError:
            return False
    #---------------------------------------------------------------------
    @staticmethod
    def remove_non_printable_chars_from_string(s):
        return ''.join(filter(lambda x: x in string.printable,s))
    #---------------------------------------------------------------------
    @staticmethod
    def date_parser(s,list_of_patterns):
        for current_date_format in list_of_patterns:
            try:
                return datetime.datetime.strptime(s,current_date_format)
            except ValueError:
                pass
        #print('DEBUG: Unable to parse date: '+s)
        return None
    #---------------------------------------------------------------------
    @staticmethod
    def seconds_to_time_string(input_seconds):
        minutes ,   seconds =   divmod(input_seconds    ,   60)
        hours   ,   minutes =   divmod(minutes          ,   60)        
        days    ,   hours   =   divmod(hours            ,   24)        
        years   ,   days    =   divmod(days             ,  365)
        if(     years!=0    ):      return str(years)+'y '+str(days)+'d '+str(hours)+':'+str(minutes)+':'+str(seconds)        
        elif(   days!=0     ):      return                 str(days)+'d '+str(hours)+':'+str(minutes)+':'+str(seconds)        
        elif(   hours!=0    ):      return                                str(hours)+':'+str(minutes)+':'+str(seconds)        
        elif(   minutes!=0  ):      return                                               str(minutes)+':'+str(seconds)        
        else:                       return                                                                str(seconds)+'s'        
    #---------------------------------------------------------------------
        
