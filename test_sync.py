import tempfile
import shutil
import sync
from pathlib import Path

def test_when_a_file_exists_in_the_source_but_not_the_destination():
    try:
        source = tempfile.mkdtemp()
        dest = tempfile.mkdtemp()
        source_path = Path(source)
        
        content = "asdasdasdasd"
        (source_path / "newfile.txt").write_text(content)
        expected_path = Path(dest) / "newfile.txt"

        sync.sync(source, dest)

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

        sync.sync(source, dest)

        assert not file_to_delete.exists()

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)

        

def test_when_a_file_exists_in_the_source_but_not_the_destination():
    source_hashes = {'hash1': 'fn1'}
    dest_hashes = {}
    expected_actions = [('COPY', Path('/src/fn1'), Path('/dst/fn1'))]

    result = sync.determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))

    assert list(result) == expected_actions 

def test_when_a_file_has_been_renamed_in_the_source():
    source_hashes = {'hash1': 'fn1'}
    dest_hashes = {'hash1': 'fn2'}
    expected_actions = [('MOVE', Path('/dst/fn2'), Path('/dst/fn1'))]

    result = sync.determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))
    assert list(result) == expected_actions 

def test_when_a_file_does_not_exist_in_source_but_exists_in_destination():
    source_hashes = {}
    dest_hashes = {'hash1': 'fn1'}
    expected_actions = [('DELETE', Path('/dst/fn1'))]

    result = sync.determine_actions(source_hashes, dest_hashes, Path("/src"), Path("/dst"))

    assert list(result) == expected_actions 