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

#sync source and destination
def sync(source, dest):
    #sync file exists , desc not
    source_hashes = {}
    for folder, _, files in os.walk(source):
        for filename in files:
            source_hashes[hash_file(Path(folder) / filename)]  = filename # this is the same as os.path.join(folder, filename)
    
    seen = {}
    for folder, _, files in os.walk(dest):
        for filename in files:
            dest_file_path = Path(folder) / filename
            dest_hash = hash_file(dest_file_path)
            seen[dest_hash] = filename
            # if not in sources, remove
            if dest_hash not in source_hashes.keys():
                dest_file_path.unlink()

            #if hash equals but name doesn't - rename
            elif dest_hash in source_hashes.keys() and filename != source_hashes[dest_hash]:
                shutil.move(dest_file_path, Path(folder) / source_hashes[dest_hash])

    # if not in destination, copy
    for source_hash, source_filename in source_hashes.items():
        if source_hash not in seen.keys():
            shutil.copy(Path(source) / source_filename, Path(dest) /  source_filename)



def read_paths_and_hashes(dir):
    files_and_hashes = {}
    for folder, _, files in os.walk(dir):
        for filename in files:
            files_and_hashes[hash_file(Path(folder) / filename)]  = filename

    return files_and_hashes

def determine_actions(source_hashes: dict, dest_hashes: dict, source, dest):   
    for hash, source_name in source_hashes.items(): #you can iterate through dictionarys like that     

        if hash not in dest_hashes:
            yield 'COPY', Path(source)/source_name, Path(dest)/source_name
        elif hash in dest_hashes and dest_hashes[hash] != source_name:
            yield 'MOVE',Path(dest)/dest_hashes[hash], Path(dest)/source_name
    #nie ma w source ale jest w dest
    
    for dest_hash, dest_fname in dest_hashes.items():
        if dest_hash not in source_hashes:
            
            yield 'DELETE', Path(dest)/dest_fname
        


#refactored sync
def sync2(source, dest):
    #sync file exists , desc not
    source_hashes = read_paths_and_hashes(source)
    seen = read_paths_and_hashes(dest)


    actions = determine_actions(source_hashes, seen, source, dest)

    for act, src, dst in actions:
        if act == 'COPY':
            shutil.copy(src, dst)
        if act == 'MOVE':
            shutil.move(src, dst)
        if act == 'DELETE':
            src.unlink()



# sync("source", "destination")