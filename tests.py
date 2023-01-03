from FileSystem import FileSystem, Directory, MAX_BUF_FILE_SIZE, DIR_MAX_ELEMS
import pytest


@pytest.fixture
def FileSystem() -> FileSystem:
    fs = FileSystem()
    fs.create_directory('.', "Dir_1")

    return fs

@pytest.fixture
def FileSystem_complex() -> FileSystem:
    ms = FileSystem()
    ms.create_directory('.', "Dir_1")
    ms.create_directory('.', "Dir_2")
    ms.create_directory('.', "Dir_3")
    ms.create_directory('./Dir_1', "Dir_11")
    ms.create_directory('./Dir_1', "Dir_12")
    ms.create_directory('./Dir_2', "Dir_21")
    ms.create_directory('./Dir_2', "Dir_22")

    return ms


def test_FileSystem_creation():
    fs = FileSystem()
    
    assert fs.root.name == '~'
    assert fs.root.son == []



def test_FileSystem_create_directories():
    fs = FileSystem()
    fs.create_directory('.', "Dir_1")
    fs.create_directory('./Dir_1', "Nested_Dir")

    assert fs.root.son[0].son[0].name == "Nested_Dir"


def test_get_node(filesystem_complex: FileSystem):
    node = filesystem_complex.get_node("./Dir_1/Dir_12")

    assert isinstance(node, Directory)
    assert node.name == "Dir_12"


def test_create_binary_file(filesystem: FileSystem):
    file = filesystem.create_binary_file("./Dir_1", "file.bin", "Dummy info")

    assert filesystem.root.son[0].son[0].name == "file.bin"
    assert filesystem.root.son[0].son[0].information == "Dummy info"


def test_create_log_file(filesystem: FileSystem):
    file = filesystem.create_log_file("./Dir_1", "file.log", "Log info")

    assert filesystem.root.son[0].son[0].name == "file.log"
    assert filesystem.root.son[0].son[0].information == "Log info"


def test_create_buffer(filesystem: FileSystem):
    file = filesystem.create_buffer("./Dir_1", "file.buf")

    assert filesystem.root.son[0].son[0].name == "file.buf"
    assert len(filesystem.root.son[0].son[0].items) == 0


def test_delete(filesystem_complex: FileSystem):
    filesystem_complex.create_buffer("./Dir_1/Dir_11", "dummy.buf")

    buffer_file = filesystem_complex.get_node("./Dir_1/Dir_11/dummy.buf")
    folder = filesystem_complex.get_node("./Dir_1/Dir_11")

    buffer_file.delete()


def test_delete_2(filesystem_complex: FileSystem):
    filesystem_complex.create_buffer("./Dir_1/Dir_11", "dummy.buf")
    filesystem_complex.create_log_file("./Dir_1/Dir_11", "1.log")
    filesystem_complex.create_log_file("./Dir_1/Dir_11", "2.log")
    filesystem_complex.create_log_file("./Dir_1/Dir_11", "3.log")

    target = filesystem_complex.get_node("./Dir_1/Dir_11/2.log")
    folder = filesystem_complex.get_node("./Dir_1/Dir_11")

    target.delete()


def test_binary_file_read(FileSystem: FileSystem):
    FileSystem.create_binary_file("./Dir_1/Dir_11", "dummy.bin", "some info")
    bin_file = FileSystem.get_node("./Dir_1/Dir_11/dummy.bin")

    assert (bin_file.read() == "some info")


def test_log_file_read(FileSystem: FileSystem):
    FileSystem.create_log_file("./Dir_1/Dir_11", "dummy.log", "some info")
    log_file = FileSystem.get_node("./Dir_1/Dir_11/dummy.log")
    log_file.append("\nsome more info")

    assert (log_file.read() == "some info\nsome more info")


def test_buffer_file_push(FileSystem: FileSystem):
    FileSystem.create_buffer("./Dir_1/Dir_11", "dummy.buf")
    buffer = FileSystem.get_node("./Dir_1/Dir_11/dummy.buf")

    assert len(buffer.items) == 0

    buffer.push(1)
    buffer.push(2)
    buffer.push(3)

    assert len(buffer.items) == 3


    FileSystem.create_directory(".", "Dummy")