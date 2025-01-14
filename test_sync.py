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

