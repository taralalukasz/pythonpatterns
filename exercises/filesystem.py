import hashlib
import os
import shutil
from pathlib import Path



BUF_SIZE = 65536 #size of one chunk of the file in bytes 
def hash_file(path):
    sha1 = hashlib.sha1()
    with open(path, 'rb') as file:
        chunk = file.read(BUF_SIZE)
        while chunk:
            sha1.update(chunk)
            chunk = file.read(BUF_SIZE)
    return sha1.hexdigest()           

def read_paths_and_hashes(dir):
    files_and_hashes = {}
    for folder, _, files in os.walk(dir):
        for filename in files:
            files_and_hashes[hash_file(Path(folder) / filename)]  = filename

    return files_and_hashes


class FileSystem: 
    def read(self, dir):
       return read_paths_and_hashes(dir)
    def copy(self, src, dst):
        shutil.copy(self, src, dst)
    def move(self, src, dst):
        shutil.move(src, dst)
    def delete(self, dest):
        os.remove(dest)

class FakeFileSystem:
    def __init__(self, paths_hashes):
        #here there will be assignment of fake hashes and paths
        self.paths_hashes = paths_hashes
        self.actions = []

    def read(self, dir):
        return self.paths_hashes[dir]
    def copy(self, src, dst):
        self.actions.append(('COPY', src, dst))
    def move(self, src, dst):
        self.actions.append(('MOVE', src, dst))
    def delete(self, dest):
        self.actions.append(('DELETE', dest))

        
    