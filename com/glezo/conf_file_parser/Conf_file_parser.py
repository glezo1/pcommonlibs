import os.path

class Conf_file_parser():
    conf_file_path  =   None
    conf            =   {}
    def __init__(self,conf_file_path):
        self.conf_file_path =   conf_file_path
        if(not os.path.isfile(self.conf_file_path)):
            raise ValueError("File "+self.conf_file_path+" does not exist")
        fd                  =   None
        try:
            fd  =   open(self.conf_file_path, 'r')
        except Exception as e:
            raise ValueError("File " + self.conf_file_path + " is not readable")
        file_lines          =   fd.readlines()
        current_line_number =   0
        for current_line in file_lines:
            current_line_number +=  1
            if(current_line.startswith('#') or current_line.strip()==''):
                pass
            else:
                key         =   None
                value       =   None
                try:
                    key     =   current_line.strip().split('=')[0].strip()
                    value   =   '"'.join(current_line.strip().split('=')[1:]).strip()
                except:
                    raise ValueError('Error at file '+self.conf_file_path+' line '+str(current_line_number)+': Not key = value!')
                self.conf[key]  =   value




