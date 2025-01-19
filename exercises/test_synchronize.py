import tempfile
import shutil
from . import synchronize
from pathlib import Path
from filesystem import  FakeFileSystem

def test_when_a_file_exists_in_the_source_but_not_the_destination():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()
        source_path = Path(source)
        
        content = "asdasdasdasd"
        (source_path / "newfile.txt").write_text(content)
        expected_path = Path(dest) / "newfile.txt"

        synchronize.sync(source, dest)

        assert expected_path.exists()
        assert expected_path.read_text() == content

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)


def test_when_a_file_has_been_renamed_in_the_source():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()

        content = "fghfghfghfghfg"
        file_to_delete = (Path(dest) / "newfile.txt")
        (Path(dest) / "newfile.txt").write_text(content)

        synchronize.sync(source, dest)

        assert not file_to_delete.exists()

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)

        

def test_when_a_file_exists_in_the_source_but_not_the_destination():
    source_hashes = {'hash1': 'fn1'}
    dest_hashes = {}
    expected_actions = [('COPY', Path('/src/fn1'), Path('/dst/fn1'))]

    result = synchronize.determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))

    assert list(result) == expected_actions 

def test_when_a_file_has_been_renamed_in_the_source():
    source_hashes = {'hash1': 'fn1'}
    dest_hashes = {'hash1': 'fn2'}
    expected_actions = [('MOVE', Path('/dst/fn2'), Path('/dst/fn1'))]

    result = synchronize.determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
    assert list(result) == expected_actions 

def test_when_a_file_does_not_exist_in_source_but_exists_in_destination():
    source_hashes = {}
    dest_hashes = {'hash1': 'fn1'}
    expected_actions = [('DELETE', Path('/dst/fn1'))]

    result = synchronize.determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))

    assert list(result) == expected_actions 


def test_sync3_copy():
    files = {"/src" : {"sha1" : "filename1"}, "/dst" : {}}
    fs = FakeFileSystem(files)
    synchronize.sync3("/src", "/dst", fs)

    assert fs.actions[0] == ('COPY', Path("/src/filename1"), Path("/dst/filename1"))

def test_sync3_move():
    files = {"/src" : {"sha1" : "filename2"}, "/dst" : {"sha1" : "filename1"}}
    fs = FakeFileSystem(files)
    synchronize.sync3("/src", "/dst", fs)

    assert fs.actions[0] == ('MOVE', Path("/dst/filename1"), Path("/dst/filename2"))

def test_sync3_delete():
    files = {"/src" : {}, "/dst" : {"sha1" : "filename1"}}
    fs = FakeFileSystem(files)
    synchronize.sync3("/src", "/dst", fs)

    assert fs.actions[0] == ('DELETE', Path("/dst/filename1"))