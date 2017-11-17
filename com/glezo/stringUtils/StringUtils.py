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
        seconds             =   str(round(seconds)  ).zfill(2)
        minutes             =   str(round(minutes)  ).zfill(2)
        hours               =   str(round(hours)    ).zfill(2)
        days                =   round(days)
        years               =   round(years)
        if(     years  !=0      ):      return years+'y '+days+'d '+hours+':'+minutes+':'+seconds+'s'
        elif(   days   !=0      ):      return            days+'d '+hours+':'+minutes+':'+seconds+'s'
        elif(   hours  !='00'   ):      return                      hours+':'+minutes+':'+seconds+'s'
        elif(   minutes!='00'   ):      return                                minutes+':'+seconds+'s'
        else:                           return                                            seconds+'s'        
    #---------------------------------------------------------------------
        
