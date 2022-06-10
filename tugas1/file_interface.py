import os
import json
import base64
from glob import glob

class FileInterface:
    def __init__(self):
        os.chdir('files/')

    def list(self):
        try:
            filelist = glob('*.*')
            return dict(status='OK',data=filelist)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

    def get(self,filename=''):
        if(filename==''):
            return None
        try:
            fp = open(f"{filename}",'rb')
            isifile = base64.b64encode(fp.read()).decode()
            return dict(status='OK',data_namafile=filename,data_file=isifile)
        except Exception as e:
            return dict(status='ERROR',data=str(e))
        
    def delete(self,filename=""):
        if(filename==''):
            return None
        try:
            if os.path.exists(filename):
                os.remove(filename)
                return dict(status='OK',data_namafile=filename)
            else:
                return dict(status='NOTFOUND', data_namafile=filename)
        except Exception as e:
            return dict(status='ERROR',data=str(e))
        
    def post(self,filename="", isifile=""):
        if (filename=='' or isifile==''):
            return None
        try:
            decoded_file = base64.b64decode(isifile)
            fp = open(filename,'wb+')
            fp.write(decoded_file)
            fp.close()
            return dict(status='OK',data_namafile=filename)
        except Exception as e:
            return dict(status='ERROR',data=str(e))

if __name__=='__main__':
    f = FileInterface()
    print(f.list())
    print(f.get('donalbebek.jpg'))