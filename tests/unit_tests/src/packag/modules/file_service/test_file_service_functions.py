import os

import stat

import pytest

from pathlib import Path

from packag.modules.file_service import (
    validate_extension,
    create_dir,
    change_file_dir,
    rename_file,
    extract_file,
    count_how_many_files,
    get_last_file_path,
    lock_until_download_is_complete,
    delete_all_dir_files,
    extract_text_from_pdf
    )

import zipfile

import time

from unittest.mock import patch

from reportlab.pdfgen import canvas



@pytest.fixture
def create_dir_with_permissions(tmp_path):
    """
    Creates a temporary directory with write permission.
    """
    # Step 1: Create the base directory
    dir = tmp_path / "read_write"
    dir.mkdir()

    # Step 2: giving all permissions to the directory
    dir.chmod(stat.S_IWUSR | stat.S_IREAD | stat.S_IEXEC)

    yield dir
    
@pytest.fixture
def create_read_only_dir(tmp_path):
    """
    Creates a temporary directory with no write permission.
    """
    # Step 1: Create the base directory
    protected_dir = tmp_path / "read_only"
    protected_dir.mkdir()

    # Step 2: Remove write permission (Unix only)
    protected_dir.chmod(stat.S_IREAD | stat.S_IEXEC)

    yield protected_dir

    # Step 3: Restore permissions so pytest can clean up
    protected_dir.chmod(stat.S_IWUSR | stat.S_IREAD | stat.S_IEXEC)
    
@pytest.fixture
def create_dir_without_read_permissions(tmp_path):
    """
    Creates a temporary directory with no read permission.
    """
    dir = tmp_path / "read_write"
    dir.mkdir()
    
    # remove read permission
    dir.chmod(stat.S_IEXEC)
    
    yield dir
    
    # restore read permission
    dir.chmod(stat.S_IWUSR | stat.S_IREAD | stat.S_IEXEC)
    
@pytest.fixture
def create_dir_without_all_permissions(tmp_path):
    """
    Creates a temporary directory with NO read or execute permissions.
    """
    protected_dir = tmp_path / "no_permissions"
    protected_dir.mkdir()

    # Remove all permissions for owner (just an example)
    protected_dir.chmod(0)

    yield protected_dir

    # Restore permissions so pytest can clean up
    protected_dir.chmod(stat.S_IWUSR | stat.S_IREAD | stat.S_IEXEC)
    
@pytest.fixture
def create_temporary_txt_file(tmp_path) -> Path:
    file_path = tmp_path / 'test_file.txt'
    file_path.write_text('test')
    return file_path

@pytest.fixture
def create_empty_temporary_pdf_file(tmp_path) -> Path:
    file_path = tmp_path / 'test_file.pdf'
    file_path.write_text('')
    return file_path

@pytest.fixture
def create_temporary_pdf_file(tmp_path) -> Path:
    file_path = tmp_path / 'test_file.pdf'

    # Create a PDF and write "Hello, World!" on it
    c = canvas.Canvas(str(file_path))
    c.drawString(100, 750, "Hello, World!")
    c.save()

    return file_path

@pytest.fixture
def create_temporary_empty_pdf_file(tmp_path) -> Path:
    file_path = tmp_path / 'test_file.pdf'

    # Create a PDF and write "Hello, World!" on it
    c = canvas.Canvas(str(file_path))
    c.save()
    
    return file_path

@pytest.fixture
def create_temporary_txt_file_without_permissions(tmp_path) -> Path:
    protected_dir = tmp_path / "protected"
    protected_dir.mkdir()

    file_path = protected_dir / "test_file.txt"
    file_path.write_text("test content")

    # Remove write permission from the directory (rename will fail)
    protected_dir.chmod(stat.S_IREAD | stat.S_IEXEC)  # No write

    yield file_path

    # Teardown: restore permission so pytest can clean it up
    protected_dir.chmod(stat.S_IWUSR | stat.S_IREAD | stat.S_IEXEC)
    
@pytest.fixture
def create_temporary_zip_file(tmp_path) -> Path:
    
    # create a directory
    dir = tmp_path / "test_dir"
    dir.mkdir()
    
    # create a txt file
    txt_file_path = dir / "test_file.txt"
    txt_file_path.write_text("test content")
    
    # create a zip file
    zip_file_path = dir / "test_file.zip"
    
    # write the txt file to the zip file
    with zipfile.ZipFile(zip_file_path, 'w') as zip_ref:
        zip_ref.write(txt_file_path, txt_file_path.name)
    
    # remove the txt file
    txt_file_path.unlink()
    
    # return the zip file path
    return zip_file_path

@pytest.fixture
def create_temporary_zip_file_without_permissions(tmp_path) -> Path:
    # create directory
    protected_dir = tmp_path / "test_protected_dir"
    protected_dir.mkdir()
    
    # create zip inside the protected directory
    zip_file_path = protected_dir / "test_file.zip"
    print(f"zip_file_path: {zip_file_path}")
    
    # create a txt file
    txt_file_path = protected_dir / "test_file.txt"
    txt_file_path.write_text("test content")
    
    # write the txt file to the zip file
    with zipfile.ZipFile(zip_file_path, 'w') as zip_ref:
        zip_ref.write(txt_file_path, txt_file_path.name)
        
    # remove the txt file
    txt_file_path.unlink()
    
    # remove permissions from the protected directory
    zip_file_path.chmod(stat.S_IWUSR)  # No write

    yield zip_file_path

    # Teardown: restore permission so pytest can clean it up
    zip_file_path.chmod(stat.S_IWUSR | stat.S_IREAD | stat.S_IEXEC)
    
###### VALIDATE EXTENSION TESTS ########

def test_validate_extension_raise_value_error_when_extension_is_not_a_string():
    """
    Test if the function raises a ValueError when the extension is not a string.
    """
    with pytest.raises(ValueError):
        validate_extension(124)
        
def test_validate_extension_raise_value_error_when_extension_is_not_allowed():
    """
    Test if the function raises a ValueError when the extension is not allowed.
    """
    with pytest.raises(ValueError):
        validate_extension("not_allowed_extension")
        
def test_validate_extension_returns_extension_when_extension_is_allowed():
    """
    Test if the function returns the extension when the extension is allowed.
    """
    assert validate_extension("txt") == "txt"

###### CREATE_DIR TESTS ########

def test_create_dir_correctly(create_dir_with_permissions):
    """
    Test if the function correctly creates a subdirectory inside a writable directory.
    """
    # Arrange: Define the subdirectory path
    target_dir = create_dir_with_permissions / "test_dir"
    
    # Act: Call the function under test
    result = create_dir(target_dir)

    # Assert: Check if the directory was actually created and returned
    assert target_dir.exists()
    assert result == target_dir
    
def test_create_dir_raise_permission_error_when_read_only_dir(create_read_only_dir):
    """
    Test if the function raises an error when the user does not have permissions to create the directory.
    """
    with pytest.raises(PermissionError):
        create_dir(create_read_only_dir / "test_dir")

def test_raise_value_error_when_input_is_not_a_path():
    """
    Test if the function raises a ValueError when the input is not a Path instance.
    """
    with pytest.raises(ValueError):
        create_dir("not_a_path")

def test_create_dir_raise_os_error_when_creating_dir(tmp_path):
    """
    Test if the function raises an OSError when the directory cannot be created due to an operating system error.
    """
    target = tmp_path / "test_dir"
    
    with patch('os.makedirs') as mock_makedirs:
        mock_makedirs.side_effect = OSError("Test error")
        
        with pytest.raises(OSError):
            create_dir(target)

def test_create_dir_return_correct_path(create_dir_with_permissions):
    """
    Test if the function returns the correct path.
    """
    target = create_dir_with_permissions / 'test_dir'
    
    created_dir_path = create_dir(target)
    
    assert created_dir_path == target
    
###### CHANGE_FILE_DIR TESTS ########

#### TEST IF THE FUNCTION RETURN VALUE ERROR WHEN THE INPUT IS NOT A PATH ########
def test_change_file_dir_raise_value_error_when_input_is_not_a_path():
    """
    Test if the function raises a ValueError when the input is not a Path instance.
    """
    with pytest.raises(ValueError):
        change_file_dir("not_a_path", "not_a_path")
         
#### TEST IF THE FUNCTION CORRECTLY MOVES THE FILE TO THE CORRECT DIRECTORY ########
def test_change_file_dir_when_successfully_moves_file(
    create_temporary_txt_file, 
    create_dir_with_permissions
    ):
    """
    Test if the function correctly moves the file to the correct directory.
    """
    current_file_path = create_temporary_txt_file
    target = create_dir_with_permissions / "test_dir"
    
    new_file_path = change_file_dir(current_file_path, target)
    
    assert new_file_path == target / current_file_path.name
    assert new_file_path.exists()
    assert isinstance(new_file_path, Path)
    
        
def test_change_file_dir_raise_permission_error_when_moving_file(
    create_temporary_txt_file,
    create_read_only_dir
    
):
    # creating a dir with read only permission
    temporary_txt_file = create_temporary_txt_file 
    read_only_dir = create_read_only_dir 
    
    with pytest.raises(PermissionError):
        change_file_dir(temporary_txt_file, read_only_dir)
    
    
###### RENAME_FILE TESTS ########
def test_rename_file_raise_value_error_when_old_file_path_is_not_a_path():
    """
    Test if the function raises a ValueError when the old_file_path is not a Path instance.
    """
    old_file_path = "not_a_path"
    new_file_name = Path("new_file_name.txt")
    
    with pytest.raises(ValueError):
        rename_file(old_file_path, new_file_name)

def test_rename_file_raise_value_error_when_new_file_name_is_not_a_path():
    """
    Test if the function raises a ValueError when the new_file_name is not a Path instance.
    """
    old_file_path = Path("old_file_path.txt")
    new_file_name = "not_a_path"
    
    with pytest.raises(ValueError):
        rename_file(old_file_path, new_file_name)
        
def test_rename_file_raise_value_error_when_old_file_name_does_not_have_an_extension():
    """
    Test if the function raises a ValueError when the old_file_name does not have an extension.
    """
    old_file_path = Path("old_file_path")
    new_file_name = Path("new_file_name.txt")
    
    with pytest.raises(ValueError):
        rename_file(old_file_path, new_file_name)
        
def test_rename_file_raise_value_error_when_new_file_name_does_not_have_an_extension():
    """
    Test if the function raises a ValueError when the new_file_name does not have an extension.
    """
    old_file_path = Path("old_file_path.txt")
    new_file_name = Path("new_file_name")
    
    with pytest.raises(ValueError):
        rename_file(old_file_path, new_file_name)

def test_rename_file_raise_file_not_found_error_when_file_does_not_exist():
    """
    Test if the function raises a FileNotFoundError when the file does not exist.
    """
    old_file_path = Path("inexistent_dir/inexistent_file.txt")
    new_file_name = Path("new_file_name.txt")
    
    with pytest.raises(FileNotFoundError):
        rename_file(old_file_path, new_file_name)

def test_rename_file_raise_value_error_when_path_is_not_from_a_file():
    """
    Test if the function raises a ValueError when the path is not from a file.
    """
    old_file_path = Path("inexistent_dir")
    new_file_name = Path("new_file_name.txt")

def test_rename_file_raise_value_error_when_new_file_name_has_a_different_extension_than_the_old_file_name(create_temporary_txt_file):
    """
    Test if the function raises a ValueError when the new_file_name has a different extension than the old_file_name.
    """
    
    old_file_path = create_temporary_txt_file
    new_file_name = Path("new_file_name.pdf")
    
    with pytest.raises(ValueError):
        rename_file(old_file_path, new_file_name)
    
#### CHECK IF THE FUNCTION RETURNS THE CORRECT PATH ########
def test_rename_file_returns_correct_path(create_temporary_txt_file):
    """
    Test if the function returns the correct path.
    """
    old_file_path = create_temporary_txt_file
    new_file_name = Path("new_file_name.txt")
    
    new_file_path = rename_file(old_file_path, new_file_name)
    
    assert new_file_path == old_file_path.parent / new_file_name
    assert new_file_path.exists()

#### CHECK IF THE FUNCTION RAISES PERMISSION ERROR WHEN TRYING TO RENAME THE FILE WITH NOT ENOUGH PERMISSIONS ########
def test_rename_file_when_not_enough_permissions(create_temporary_txt_file_without_permissions):
    """
    Test if the function raises a PermissionError when the user does not have enough permissions to rename the file.
    """
    old_file_path = create_temporary_txt_file_without_permissions
    new_file_name = Path("new_file_name.txt")
    
    with pytest.raises(PermissionError):
        rename_file(old_file_path, new_file_name)

#### CHECK IF THE FUNCTION RAISES OS ERROR WHEN TRYING TO RENAME THE FILE WITH AN OS ERROR ########
def test_rename_file_raises_oserror(tmp_path):
    """
    Test if rename_file raises OSError when the OS prevents renaming the file.
    """
    # Arrange: create a dummy file
    old_file = tmp_path / "file.txt"
    old_file.write_text("test content")

    new_file = Path("file_renamed.txt")

    # Patch the rename method to simulate an OSError
    with patch.object(Path, "rename", side_effect=OSError("Simulated OS-level error")):
        with pytest.raises(OSError) as exc_info:
            rename_file(old_file, new_file)

    assert "Simulated OS-level error" in str(exc_info.value)
    
#### EXTRACT_FILE TESTS ########

#### TEST IF THE FUNCTION RAISES VALUE ERROR WHEN THE ZIP_PATH IS NOT A PATH ########
def test_extract_file_raise_value_error_when_zip_path_is_not_a_path():
    """
    Test if the function raises a ValueError when the zip_path is not a Path instance.
    """
    zip_path = "not_a_path"
    extract_to_path = Path('path_to_extract')
    with pytest.raises(ValueError):
        extract_file(zip_path, extract_to_path)

#### TEST IF THE FUNCTION RAISES VALUE ERROR WHEN THE ZIP_PATH IS NOT A .ZIP FILE ########
def test_extract_file_raise_value_error_when_zip_path_is_not_a_zip_file():
    """
    Test if the function raises a ValueError when the zip_path is not a .zip file.
    """
    zip_path = Path('path_to_zip.zip')
    extract_to_path = 'path_to_extract'
    with pytest.raises(ValueError):
        extract_file(zip_path, extract_to_path)
        
def test_extract_file_raise_value_error_when_extract_to_path_is_not_a_path(create_temporary_txt_file):
    """
    Test if the function raises a ValueError when the extract_to_path is not a Path instance.
    """
    zip_path = create_temporary_txt_file
    extract_to_path = "not_a_path"
    with pytest.raises(ValueError):
        extract_file(zip_path, extract_to_path)

#### TEST IF THE FUNCTION RAISES VALUE ERROR WHEN THE EXTRACT_TO_PATH IS NOT A PATH ########
def test_extract_file_raise_value_error_when_extract_to_path_is_not_a_path():
    """
    Test if the function raises a ValueError when the extract_to_path is not a Path instance.
    """
    zip_path = Path('path_to_zip')
    extract_to_path = "not_a_path"
    
    with pytest.raises(ValueError):
        extract_file(zip_path, extract_to_path)
        
#### TEST IF THE FUNCTION RETURNS THE CORRECT PATH ########
def test_extract_file_returns_correct_path(
    create_temporary_zip_file,
    create_dir_with_permissions
    ):
    """
    Test if the function returns the correct path.
    """
    zip_path = create_temporary_zip_file
    extract_to_path = create_dir_with_permissions
    
    extracted_file_path = extract_file(zip_path, extract_to_path)
    
    assert extracted_file_path == extract_to_path / 'test_file.txt'
    assert extracted_file_path.exists()
    
#### TEST IF THE FUNCTION RAISES PERMISSION ERROR WHEN TRYING TO EXTRACT THE ZIP FILE WIHOUT PERMISSIONS ########
def test_extract_file_raise_permission_error_when_trying_to_extract_file_without_permissions(
    create_temporary_zip_file_without_permissions,
    create_dir_with_permissions
):
    """
    Test if the function raises a PermissionError when the user does not have enough permissions to extract the file.
    """
    zip_path = create_temporary_zip_file_without_permissions
    extract_to_path = create_dir_with_permissions
    
    with pytest.raises(PermissionError):
        extract_file(zip_path, extract_to_path)

#### TEST IF THE FUNCTION RAISES PERMISSION ERROR WHEN TRYING TO EXTRACT THE FILE TO A READ ONLY DIRECTORY ########
def test_extract_file_raise_permission_error_when_trying_to_extract_file_to_a_read_only_directory(
    create_temporary_zip_file,
    create_read_only_dir
):
    """
    Test if the function raises a PermissionError when the user does not have enough permissions to extract the file.
    """
    zip_path = create_temporary_zip_file
    extract_to_path = create_read_only_dir
    
    with pytest.raises(PermissionError):
        extract_file(zip_path, extract_to_path)

#### TEST IF THE FUNCTION RAISES OS ERROR WHEN TRYING TO EXTRACT THE FILE ########


#### COUNT HOW MANY FILES TESTS ########

def test_count_how_many_files_raise_value_error_when_path_is_not_a_path():
    """
    Test if the function raises a ValueError when the path is not a Path instance.
    """
    path = "not_a_path"
    with pytest.raises(ValueError):
        count_how_many_files(path)
        
def test_count_how_many_files_raise_value_error_when_extension_is_not_allowed():
    """
    Test if the function raises a ValueError when the extension is not allowed.
    """
    path = Path("path_to_directory")
    extension = "not_allowed_extension"
    with pytest.raises(ValueError):
        count_how_many_files(path, extension)
        
def test_count_how_many_files_raise_file_not_found_error_when_path_does_not_exist():
    """
    Test if the function raises a FileNotFoundError when the path does not exist.
    """
    path = Path("inexistent_path")
    with pytest.raises(FileNotFoundError):
        count_how_many_files(path)
        
def test_count_how_many_files_raise_value_error_when_path_is_not_a_directory(
    create_temporary_txt_file
):
    """
    Test if the function raises a ValueError when the path is not a directory.
    """
    path = create_temporary_txt_file
    with pytest.raises(ValueError):
        count_how_many_files(path)

def test_count_how_many_files_returns_correct_number_of_files_when_no_extension_is_provided(
    create_dir_with_permissions,
    ):
    """
    Test if the function returns the correct number of files.
    """
    dir_path = create_dir_with_permissions 
    
    # create a txt file
    txt_file = dir_path / "test_file.txt"
    txt_file.write_text("test content")
    
    # create a zip file
    zip_file = dir_path / "test_file.zip"
    zip_file.write_bytes(b"test content")
    
    assert count_how_many_files(dir_path) == 2
    
def test_count_how_many_files_returns_correct_number_of_files_when_extension_is_provided(
    create_dir_with_permissions,
    ):
    """
    Test if the function returns the correct number of files.
    """
    dir_path = create_dir_with_permissions 
    
    # create a txt file
    txt_file = dir_path / "test_file.txt"
    txt_file.write_text("test content")
    
    # create a zip file
    zip_file = dir_path / "test_file.zip"
    zip_file.write_bytes(b"test content")
    
    # create a pdf file
    pdf_file = dir_path / "test_file.pdf"
    pdf_file.write_bytes(b"test content")
    
    # create a html file
    html_file = dir_path / "test_file.html"
    html_file.write_bytes(b"test content")
    
    assert count_how_many_files(dir_path, "txt") == 1
    assert count_how_many_files(dir_path, "zip") == 1
    assert count_how_many_files(dir_path, "pdf") == 1
    assert count_how_many_files(dir_path, "html") == 1
    
def test_count_how_many_files_raises_permission_error_when_trying_to_count_files_in_a_directory_without_permissions(
    create_dir_without_read_permissions
):
    """
    Test if the function raises a PermissionError when the user does not have enough permissions to count the files.
    """
    path = create_dir_without_read_permissions
    
    with pytest.raises(PermissionError):
        count_how_many_files(path)
        
###### GET LAST FILE PATH TESTS ########

    
def test_get_last_file_path_raise_value_error_when_extension_is_not_allowed():
    """
    Test if the function raises a ValueError when the extension is not allowed.
    """
    path = Path("path_to_directory")
    extension = "not_allowed_extension"
    with pytest.raises(ValueError):
        get_last_file_path(path, extension)
    
    
def test_get_last_file_path_raise_value_error_when_path_is_not_a_path():
    """
    Test if the function raises a ValueError when the path is not a Path instance.
    """
    path = "not_a_path"
    with pytest.raises(ValueError):
        get_last_file_path(path, 'txt')
    
def test_get_last_file_path_raise_file_not_found_error_when_path_does_not_exist():
    """
    Test if the function raises a FileNotFoundError when the path does not exist.
    """
    path = Path("inexistent_path")
    with pytest.raises(FileNotFoundError):
        get_last_file_path(path, 'txt')
        
def test_get_last_file_path_raise_value_error_when_path_is_not_a_directory(
    create_temporary_txt_file
):
    """
    Test if the function raises a ValueError when the path is not a directory.
    """
    path = create_temporary_txt_file
    with pytest.raises(ValueError):
        get_last_file_path(path, 'txt')

def test_get_last_file_path_returns_correct_path(
    create_dir_with_permissions
):
    """
    Test if the function returns the correct path.
    """
    path = create_dir_with_permissions
    
    # create a txt file
    txt_file = path / "test_file.txt"
    txt_file.write_text("test content")
    
    # create a zip file
    zip_file = path / "test_file.zip"
    zip_file.write_bytes(b"test content")
    
    assert get_last_file_path(path, "txt") == txt_file
    assert get_last_file_path(path, "zip") == zip_file
    
def test_get_last_file_path_raise_file_not_found_error_when_no_files_are_found(
    create_dir_with_permissions
):
    """
    Test if the function raises a FileNotFoundError when no files are found.
    """
    path = create_dir_with_permissions
    
    with pytest.raises(FileNotFoundError):
        get_last_file_path(path, "txt")
        
#### LOCK UNTIL DOWNLOAD IS COMPLETE TESTS ########

def test_lock_until_download_is_complete_raise_value_error_when_path_is_not_a_path():
    """
    Test if the function raises a ValueError when the path is not a Path instance.
    """
    path = "not_a_path"
    
    with pytest.raises(ValueError):
        lock_until_download_is_complete(path, 1)
        
def test_lock_until_download_is_complete_raise_value_error_when_old_files_quantity_is_not_an_int():
    """
    Test if the function raises a ValueError when the old_files_quantity is not an int.
    """
    path = Path("path_to_directory")
    old_files_quantity = "not_an_int"
    
    with pytest.raises(ValueError):
        lock_until_download_is_complete(path, old_files_quantity)
        
def test_lock_until_download_is_complete_raise_value_error_when_extension_is_not_a_string():
    """
    Test if the function raises a ValueError when the extension is not a string.
    """
    path = Path("path_to_directory")
    extension = 123
    
    with pytest.raises(ValueError):
        lock_until_download_is_complete(path, 1, extension)
        
def test_lock_until_download_is_complete_returns_true_when_download_is_complete(
    create_dir_with_permissions
):
    """
    Test if the function returns True when the download is complete.
    """
    path = create_dir_with_permissions
    old_files_quantity = 0
    extension = "txt"
    
    # side effects values
    side_effects_values = [0, 0, 1]
    
    with patch('packag.modules.file_service.functions.count_how_many_files', side_effect=side_effects_values):
        with patch('time.sleep'):
            result = lock_until_download_is_complete(path, old_files_quantity, extension)
            
    assert result == True
    
def test_lock_until_download_is_complete_returns_false_when_download_is_not_complete(
    create_dir_with_permissions
):
    """
    Test if the function returns False when the download is not complete.
    """
    path = create_dir_with_permissions
    old_files_quantity = 0
    extension = "txt"
    
    # side effects values -> the new files quantity is always 0 for more than 9 attempts
    side_effects_values = [
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0,
        ]
    
    with patch('packag.modules.file_service.functions.count_how_many_files', side_effect=side_effects_values):
        with patch('time.sleep'):
            result = lock_until_download_is_complete(path, old_files_quantity, extension)
            
    assert result == False
    
###### DELETE ALL DIR FILES TESTS ########
    
def test_delete_all_dir_files_raise_value_error_when_path_is_not_a_path():
    """
    Test if the function raises a ValueError when the path is not a Path instance.
    """
    path = "not_a_path"
    
    with pytest.raises(ValueError):
        delete_all_dir_files(path)
        
def test_delete_all_dir_files_raise_file_not_found_error_when_path_does_not_exist():
    """
    Test if the function raises a FileNotFoundError when the path does not exist.
    """
    path = Path("inexistent_path")
    
    with pytest.raises(FileNotFoundError):
        delete_all_dir_files(path)
        
def test_delete_all_dir_files_raise_value_error_when_path_is_not_a_directory(
    create_temporary_txt_file
):
    """
    Test if the function raises a ValueError when the path is not a directory.
    """
    path = create_temporary_txt_file
    
    with pytest.raises(ValueError):
        delete_all_dir_files(path)
        
def test_delete_all_dir_files_raise_permission_error_when_trying_to_delete_files_in_a_directory_without_permissions(
    create_dir_without_all_permissions
):
    """
    Test if the function raises a PermissionError when the user does not have enough permissions to delete the files.
    """
    path = create_dir_without_all_permissions
    
    with pytest.raises(PermissionError):
        delete_all_dir_files(path)
        
def test_delete_all_dir_files_works_when_there_are_no_files_in_the_directory(
    create_dir_with_permissions
):
    """
    Test if the function works when there are no files in the directory.
    """
    path = create_dir_with_permissions
    old_files_quantity = 0
    
    delete_all_dir_files(path)
    
    new_files_quantity = count_how_many_files(path)
    
    assert new_files_quantity == 0
    
def test_delete_all_dir_files_works_when_there_are_files_in_the_directory(
    create_dir_with_permissions
):
    """
    Test if the function works when there are files in the directory.
    """
    path = create_dir_with_permissions
    
    # create a txt file
    txt_file = path / "test_file.txt"
    txt_file.write_text("test content")
    
    assert count_how_many_files(path) == 1
    
    # create a zip file
    zip_file = path / "test_file.zip"
    zip_file.write_bytes(b"test content")
    
    assert count_how_many_files(path) == 2
    
    delete_all_dir_files(path)
    
    assert count_how_many_files(path) == 0
    
def test_extract_text_from_pdf_raise_value_error_when_pdf_path_is_not_a_path():
    """
    Test if the function raises a ValueError when the pdf_path is not a Path instance.
    """
    pdf_path = "not_a_path"
    
    with pytest.raises(ValueError):
        extract_text_from_pdf(pdf_path)
        
def test_extract_text_from_pdf_raise_file_not_found_error_when_pdf_path_does_not_exist():
    """
    Test if the function raises a FileNotFoundError when the pdf_path does not exist.
    """
    pdf_path = Path("inexistent_path")
    
    with pytest.raises(FileNotFoundError):
        extract_text_from_pdf(pdf_path)
        
def test_extract_text_from_pdf_raise_value_error_when_pdf_path_is_not_a_pdf_file(
    create_temporary_txt_file
):
    """
    Test if the function raises a ValueError when the pdf_path is not a .pdf file.
    """
    txt_file_path = create_temporary_txt_file
    
    with pytest.raises(ValueError):
        extract_text_from_pdf(txt_file_path)
        
def test_extract_text_from_pdf_returns_text_when_pdf_path_is_a_pdf_file(
    create_temporary_pdf_file
):
    """
    Test if the function returns the text when the pdf_path is a .pdf file.
    """
    pdf_path = create_temporary_pdf_file
    
    text = extract_text_from_pdf(pdf_path)
    assert text == 'Hello, World!'
    

def test_extract_text_from_pdf_returns_text_when_pdf_path_is_a_empty_pdf_file(
    create_temporary_empty_pdf_file
):
    """
    Test if the function returns the text when the pdf_path is a .pdf file.
    """
    pdf_path = create_temporary_empty_pdf_file
    
    text = extract_text_from_pdf(pdf_path)
    assert text is None      
        
def test_extract_text_from_pdf_when_does_not_have_permissions_to_read_pdf_file(
    create_dir_without_all_permissions
):
    """
    Test if the function returns None when the user does not have permissions to read the pdf file.
    """
    pdf_path = create_dir_without_all_permissions / "test_file.pdf"
    
    with pytest.raises(PermissionError):
        extract_text_from_pdf(pdf_path)
    