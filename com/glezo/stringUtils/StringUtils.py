import string
import datetime
from itertools      import combinations

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
    @staticmethod
    def str_split_all_permutations(str_input,separator='|',num_fragments_in_output=1):
        #based on https://stackoverflow.com/questions/69555581/python-string-split-by-separator-all-possible-permutations/
        def lst_merge(lst, positions, sep='|'):
            #merges a list on points other than positions
            #A, B, C, D and 0, 1 -> A, B, C|D
            a   =   -1
            out =   []
            for b in list(positions)+[len(lst)-1]:
                out.append('|'.join(lst[a+1:b+1]))
                a   =   b
            return out

        def split_comb(s, sep='|',split=1):
            l = s.split(sep)
            return [lst_merge(l, pos, sep=sep)
                    for pos in combinations(range(len(l)-1), split)]

        if(num_fragments_in_output==0):
            raise ValueError("num_fragments_in_output shall be > 0")
        return split_comb(str_input,separator,num_fragments_in_output-1)
    #---------------------------------------------------------------------
        
