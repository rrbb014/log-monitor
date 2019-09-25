import os


class ChangeSensor:
    """ 
    Description:

    ChangeSensor recognize logfile's changes based on offset.
    This object delegate to recognize file changes and commit offset,
    notify change to EventHandler

    Keyword Arguments:

    filepath    -- logfile's realpath .
    offset_root -- directory path where offset files located.
                   It comes from config yaml's 'offset_path'.
    LOGGER      -- for logging
    """
    
    def __init__(self, filepath: str, offset_root: str, LOGGER):
        self.target_file = filepath
        self._offset_root = offset_root

        _ , filename = os.path.split(self.target_file)
        title, _ = os.path.splitext(filename)

        self.offset_path = os.path.join(self._offset_root, title) + '.offset'

        self._reader = open(self.target_file, 'r')
        self.LOGGER = LOGGER

        self.find_offset()

    def find_offset(self):
        if not os.path.exists(self.offset_path):
            with open(self.offset_path, 'w') as f:
                f.write('0')
            LOGGER.info("No offset file: %s. It will be created." % self.offset_path)
            self.offset = 0
            return 0

        with open(self.offset_path) as f:
            content = f.read().strip()
            self.offset = int(content) if content != '' else 0
            return self.offset

    def detect(self):
        """Detect target log file's change"""
        last_offset = self._reader.seek(0, 2)
        self._reader.seek(self.offset)

        if self.offset < last_offset:
            self.LOGGER.info("Change is detected! - file: %s" % self.target_file)
            return True
        else:
            # TODO: If file is reset, should be handle
            return False

    def read(self):
        self._reader.seek(self.offset)
        text = self._reader.readline().strip()
        next_offset = self._reader.tell()
        self._reader.seek(self.offset)
        return text, next_offset
    
    def commit(self, offset):
        with open(self.offset_path, 'w') as f:
            f.write(str(offset))
        self.LOGGER.info("Committed offset: %d - file: %s" % (self.offset, self.target_file))

    def close(self):
        self._reader.close()
