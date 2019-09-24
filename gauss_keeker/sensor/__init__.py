

class ChangeSensor:
    """Recognize changes of specific file"""
    
    def __init__(self, filename, seek_no=0):
        self.target = filename
        self._seek_no = seek_no
        self.reader = open(filename, 'r')

    def read_from_offset(self):
        self.reader.seek(self._seek_no)



