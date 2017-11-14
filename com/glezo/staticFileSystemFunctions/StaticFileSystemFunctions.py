import sys
sys.path.extend(('C:\\Python34\\lib\\site-packages\\win32', 'C:\\Python34\\lib\\site-packages\\win32\\lib', 'C:\\Python34\\lib\\site-packages\\Pythonwin'))


from pathlib    import Path
import os
from os import listdir
from os.path import isfile, join
import shutil
import hashlib
import re
import zipfile

class StaticFileSystemFunctions(object):
    KILOBYTE    =   1024
    MEGABYTE    =   1048576
    GIGABYTE    =   1073741824
    #---------------------------------------------------------------------
    @staticmethod
    def fileExists(path):
        return os.path.exists(path)
    #---------------------------------------------------------------------
    @staticmethod
    def createFileIfNotExists(path):
        if StaticFileSystemFunctions.fileExists(path):
            return True
        else:
            folder,_ = os.path.split(path)
            StaticFileSystemFunctions.createFolder(folder)
            fd = open(path,"w")          
            fd.close()
            return StaticFileSystemFunctions.fileExists(path)
    #---------------------------------------------------------------------
    @staticmethod
    def folderExists(path):
        fd = Path(path)
        return fd.is_dir()
    #---------------------------------------------------------------------
    @staticmethod
    def renameFile(old,new):
        if(old==new):
            return True
        if(StaticFileSystemFunctions.fileExists(new)):
            StaticFileSystemFunctions.deleteFile(new)
        os.rename(old,new)
        return StaticFileSystemFunctions.fileExists(new) and not StaticFileSystemFunctions.fileExists(old)
    #---------------------------------------------------------------------
    @staticmethod
    def get_folder_filename_extension(file_path):
            folder,filename = os.path.split(file_path)
            extension = StaticFileSystemFunctions.get_file_extension(filename)
            if(extension==None):
                return folder,filename,None
            else:
                return folder,filename[:-(len(extension)+1)] ,extension
    #---------------------------------------------------------------------
    @staticmethod
    def get_file_extension(file_path):
        string_parts = file_path.split('.')
        if(len(string_parts)==1):
            return None
        else:
            return string_parts[len(string_parts)-1]
    #---------------------------------------------------------------------
    @staticmethod
    def change_file_extension(file_path,new_extension):
        #if(not StaticFileSystemFunctions.fileExists(file_path)):
        #    return False
        previous_extension  =   StaticFileSystemFunctions.get_file_extension(file_path)
        if(previous_extension==None):
            return False
        new_file_path = file_path[:-len(previous_extension)]+new_extension
        StaticFileSystemFunctions.renameFile(file_path,new_file_path)
        return True
    #---------------------------------------------------------------------
    @staticmethod
    def copyFile(original,copy):
        shutil.copy2(original,copy)
    #---------------------------------------------------------------------
    @staticmethod
    def corruptFile(path):
        file_size   =   StaticFileSystemFunctions.fileSize(path)
        random_data =   bytearray(os.urandom(file_size))
        fo          =   open(path , "wb")
        fo.seek(0)
        fo.truncate()
        fo.write(random_data)
        fo.close()
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    #---------------------------------------------------------------------
    @staticmethod
    def deleteFile(path):
        if(StaticFileSystemFunctions.fileExists(path)):
            os.remove(path)
        return not StaticFileSystemFunctions.fileExists(path)
    #---------------------------------------------------------------------
    @staticmethod
    def deleteFolder(path):
        if(StaticFileSystemFunctions.folderExists(path)):
            shutil.rmtree(path)
            return not StaticFileSystemFunctions.folderExists(path)
        return True
    #---------------------------------------------------------------------
    @staticmethod
    def deleteFilesMatching(directory_path, pattern):
        for f in os.listdir(directory_path):
            if re.search(pattern, f):
                os.remove(os.path.join(directory_path, f))
    #---------------------------------------------------------------------
    @staticmethod
    def createFolder(path):
        if(not StaticFileSystemFunctions.folderExists(path)):
            os.makedirs(path)
            return StaticFileSystemFunctions.folderExists(path)
    #---------------------------------------------------------------------
    @staticmethod
    def fileSize(path):
        return os.path.getsize(path)
    #---------------------------------------------------------------------
    @staticmethod
    def folderSize(path):
        if(not StaticFileSystemFunctions.folderExists(path)):
            return 0
        result=0
        for f in listdir(path):
            ff=join(path,f) 
            if isfile(ff):      result+=StaticFileSystemFunctions.fileSize(ff)
            else:               result+=StaticFileSystemFunctions.folderSize(ff)
        return result
    #---------------------------------------------------------------------
    @staticmethod
    def getAtime(path):
        return os.path.getatime(path)
    #---------------------------------------------------------------------
    @staticmethod
    def getCtime(path):
        return os.path.getctime(path)
    #---------------------------------------------------------------------
    @staticmethod
    def getMtime(path):
        return os.path.getmtime(path)
    #---------------------------------------------------------------------
    @staticmethod
    def get_size_atime_mtime_ctime(path):
        struct_stat    =   os.stat(path)
        return struct_stat.st_size,struct_stat.st_atime,struct_stat.st_mtime,struct_stat.st_ctime
    #---------------------------------------------------------------------
    @staticmethod
    def concatenateFiles(destiny,source):
        with open(destiny,'a') as outfile:
            with open(source) as infile:
                for line in infile:
                    outfile.write(line)        
    #---------------------------------------------------------------------
    @staticmethod
    def read_file(path):
        try:
            with open(path,'r',encoding='utf8') as f:
                return f.read()
        except Exception as e:
            print(str(e))
            return ''
    #---------------------------------------------------------------------
    @staticmethod
    def read_file_in_lines(path):
        try:
            with open(path,'r',encoding='utf8') as f:
                return f.readlines()
        except Exception as e:
            print(e)
            return []
    #---------------------------------------------------------------------
    @staticmethod
    def read_file_line(path,line_number):
        #try:
            with open(path,'r') as f:
                return f.readlines()[line_number]
        #except:
        #    return ''
    #---------------------------------------------------------------------
    @staticmethod
    def truncate_file(path):
        if(not StaticFileSystemFunctions.fileExists(path)):
            return
        #with open(path,'w'): pass        #this, if the file exists, throws error: permission denied
        fo = open(path , "r+")
        fo.seek(0)
        fo.truncate()
        fo.close()
    #---------------------------------------------------------------------
    @staticmethod
    def truncate_and_write_file(path,content):
        StaticFileSystemFunctions.deleteFile(path)
        StaticFileSystemFunctions.appendToFile(path, content)
    #---------------------------------------------------------------------
    @staticmethod
    def format_file_size(size):
        G=int(size / StaticFileSystemFunctions.GIGABYTE)
        size -= StaticFileSystemFunctions.GIGABYTE * G
        M=int(size / StaticFileSystemFunctions.MEGABYTE)
        size -= StaticFileSystemFunctions.MEGABYTE * M
        K=int(size / StaticFileSystemFunctions.KILOBYTE)
        size -= StaticFileSystemFunctions.KILOBYTE * K
        return str(G)+'.'+str(M)+'.'+str(K)+'.'+str(size)
    #---------------------------------------------------------------------
    @staticmethod
    def md5(file_path):
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()        
    #---------------------------------------------------------------------
    @staticmethod
    def preprend_to_file(file_path,prepend_content):
        with open(file_path,'rb') as original:   
            data=original.read()
        with open(file_path,'wb') as modified:   
            modified.write(prepend_content)
            modified.write(data)
    #---------------------------------------------------------------------
    @staticmethod
    def appendToFile(path,content):
        StaticFileSystemFunctions.createFileIfNotExists(path)
        with open(path,"ab") as fd:
            fd.write(bytes(content,'UTF-8'))
    #---------------------------------------------------------------------
    @staticmethod
    def create_and_return_next_file(folder_path,file_name_regex,file_name_number_preffix,file_extension):
        #TODO! lock
        last_file_number=None
        for f in listdir(folder_path): 
            if isfile(join(folder_path,f)) and re.match(file_name_regex,f):
                #let's remove prefix and file extension
                int_part = f[len(file_name_number_preffix):]
                int_part = int_part.split('.')[0]
                file_number=int(int_part)
                if(last_file_number==None or last_file_number<file_number):
                    last_file_number=file_number
        next_file_number=None
        if(last_file_number==None):     next_file_number=1
        else:                           next_file_number=last_file_number+1
        result=join(folder_path,file_name_number_preffix+str(next_file_number)+'.'+file_extension)
        StaticFileSystemFunctions.createFileIfNotExists(result)
        return result 
    #---------------------------------------------------------------------
    @staticmethod
    def get_sorted_list_of_files(folder_path,file_name_regex,file_name_number_preffix,file_name_number_suffix):
        result      =   []
        pre_result  =   []
        for f in listdir(folder_path): 
            ff=join(folder_path,f)
            if isfile(ff) and re.match(file_name_regex,f):
                file_number=int(f[len(file_name_number_preffix):-len(file_name_number_suffix)])
                pre_result.append(file_number,ff)
        pre_result=sorted(pre_result,key=lambda kv: kv[0])
        for i in range(0,len(pre_result)):
            result.append(pre_result[i][1])
        return result
    #---------------------------------------------------------------------
    @staticmethod
    def compress_folder_zip(input_folder_path,output_folder_path=None):
        if(output_folder_path==None):
            output_folder_path=input_folder_path
        shutil.make_archive(input_folder_path,'zip',output_folder_path)
    #---------------------------------------------------------------------
    @staticmethod
    def compress_file_zip(input_file_path,output_file_path=None):
        if(output_file_path==None):
            output_file_path=input_file_path+'.zip'
        '''
        this will recreate the directory structure
        zip_handle = zipfile.ZipFile(output_file_path, 'w')
        zip_handle.write(input_file_path, compress_type=zipfile.ZIP_DEFLATED)
        zip_handle.close()
        '''
        input_target_folder,input_target_file,input_target_extension = StaticFileSystemFunctions.get_folder_filename_extension(input_file_path)
        if(input_target_extension!=''):
            input_target_file+='.'+input_target_extension
        zip_handle = zipfile.ZipFile(output_file_path, 'w')
        zip_handle.write(os.path.join(input_target_folder, input_target_file), input_target_file, compress_type = zipfile.ZIP_DEFLATED)
        zip_handle.close()
    #---------------------------------------------------------------------
