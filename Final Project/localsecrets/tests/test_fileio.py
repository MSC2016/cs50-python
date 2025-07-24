import pytest
import os
from localsecrets.fileio import FileIO

@pytest.fixture
def tmp_file(tmp_path):
    return tmp_path / "testfile.txt"

def test_file_exists_and_save_read(tmp_file):
    fio = FileIO(str(tmp_file))
    assert not fio.file_exists()
    data = b"hello world"
    assert fio.save_data(data) is True
    assert fio.file_exists()
    read_data = fio.read_data()
    assert read_data == data

def test_backup_and_restore(tmp_file):
    fio = FileIO(str(tmp_file))
    data = b"data"
    fio.save_data(data)
    fio._backup_file()
    with open(tmp_file, 'wb') as f:
        f.write(b"corrupt data")
    fio._restore_backup()
    restored = fio.read_data()
    assert restored == data
