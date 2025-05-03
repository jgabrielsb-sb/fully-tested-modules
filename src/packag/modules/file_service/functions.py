import os
import glob
import shutil
import zipfile
from pathlib import Path
from packag.utils.decorators import log_execution
from packag.utils.logger import get_logger
import time
import pdfplumber

file_service_logger = get_logger('file_service')

@log_execution(file_service_logger)
def validate_extension(extension: str) -> None:
    """
    Validates if a file extension is in the list of allowed extensions.

    Args:
        extension (str): The file extension to validate (without the dot).

    Returns:
        str: The validated extension if successful.

    Raises:
        ValueError: If the extension is not a string or not in the allowed list.

    Examples:
        >>> validate_extension("pdf")
        'pdf'
        >>> validate_extension("doc")  # Not allowed
        ValueError: Extension 'doc' is not allowed (must be one of the following: ['pdf', 'xml', 'zip', 'txt', 'html'])
    """
    allowed_extensions = ["pdf", "xml", "zip", "txt", "html"]
    if not isinstance(extension, str):
        raise ValueError(f"Extension '{extension}' must be a string")
    
    if extension not in allowed_extensions:
        file_service_logger.error(f"Extension '{extension}' is not allowed (must be one of the following: {allowed_extensions})")
        raise ValueError(f"Extension '{extension}' is not allowed (must be one of the following: {allowed_extensions})")
    
    return extension

@log_execution(file_service_logger)
def create_dir(dir_to_create: Path) -> Path:
    """
    Creates a directory at the specified path if it doesn't exist.

    Args:
        dir_to_create (Path): Path object representing the directory to create.

    Returns:
        Path: Path object of the created directory.

    Raises:
        ValueError: If dir_to_create is not a Path instance.
        PermissionError: If user lacks permission to create directory.
        OSError: If directory creation fails due to system error.

    Examples:
        >>> from pathlib import Path
        >>> new_dir = create_dir(Path("data/processed"))
        >>> print(new_dir)
        data/processed
        >>> print(new_dir.exists())
        True
    """
    if not isinstance(dir_to_create, Path):
        file_service_logger.error(f"'{dir_to_create}' must be an instance of Path")
        raise ValueError(f"'{dir_to_create}' must be an instance of Path")
    
    try:
        os.makedirs(dir_to_create, exist_ok=True)
    except PermissionError as e:
        file_service_logger.error(f"Permission error when trying to create directory '{dir_to_create}': {e}")
        raise 
    
    return dir_to_create

@log_execution(file_service_logger)
def change_file_dir(current_file_path: Path, dir_to_save: Path) -> Path:
    """
    Moves a file from its current location to a new directory.

    Args:
        current_file_path (Path): Current path of the file to be moved.
        dir_to_save (Path): Destination directory where the file should be moved.

    Returns:
        Path: New path of the moved file.

    Raises:
        ValueError: If either argument is not a Path instance.
        PermissionError: If user lacks permission to move file.
        OSError: If file movement fails due to system error.

    Examples:
        >>> from pathlib import Path
        >>> old_path = Path("downloads/invoice.pdf")
        >>> new_dir = Path("processed_files")
        >>> new_path = change_file_dir(old_path, new_dir)
        >>> print(new_path)
        processed_files/invoice.pdf
    """
    
    for path in [current_file_path, dir_to_save]:
        if not isinstance(path, Path):
            file_service_logger.error(f"Argument {path} must be an instance of Path")
            raise ValueError(f"Argument {path} must be an instance of Path")
        
   
    create_dir(dir_to_save)
    
    new_file_path = dir_to_save / current_file_path.name
    
    try:
        shutil.move(current_file_path, new_file_path)
    except PermissionError as e:
        file_service_logger.error(f"Permission error when trying to move file '{current_file_path}' to '{new_file_path}': {e}")
        raise
    

    return new_file_path

##############  ERRADO -> new_file_name deve ser um STR ###################
@log_execution(file_service_logger)
def rename_file(old_file_path: Path, new_file_name: Path) -> Path:  
    """
    Renames a file to a new name within the same directory.

    Args:
        old_file_path (Path): The current full path to the file to be renamed.
        new_file_name (Path): The new name for the file (including the extension).

    Returns:
        Path: The full path to the renamed file.

    Raises:
        ValueError: If inputs are not of the correct type or the file extensions do not match.
        FileNotFoundError: If the specified file does not exist or is not a file.
        PermissionError: If the file cannot be renamed due to insufficient permissions.
        OSError: If an OS-level error occurs during renaming.

    Example:
        To rename a file from 'C:\\Sebrae\\img.png' to 'img_001.png', use:

        >>> old_file_path = Path("C:/Sebrae/img.png")
        >>> rename_file(old_file_path, "img_001.png")
    """
    new_file_path = None
    
    # check if the old_file_path is a Path instance
    if not isinstance(old_file_path, Path):
        file_service_logger.error(f"Argument '{old_file_path}' must be an instance of Path")
        raise ValueError(f"Argument '{old_file_path}' must be an instance of Path")

    # check if the new_file_name is a Path instance
    if not isinstance(new_file_name, Path):
        file_service_logger.error(f"Argument '{new_file_name}' must be an instance of Path")
        raise ValueError(f"Argument '{new_file_name}' must be an instance of Path")
    
    # check if the old file path is from a file
    if not old_file_path.suffix:
        file_service_logger.error(f"File '{old_file_path}' must have an extension")
        raise ValueError(f"File '{old_file_path}' must have an extension")
    
    # check if the new file name is from a file with extension
    if not new_file_name.suffix:
        file_service_logger.error(f"New file name '{new_file_name}' must include an extension")
        raise ValueError(f"New file name '{new_file_name}' must include an extension")
    
    # check if the file path exists
    if not old_file_path.exists():
        file_service_logger.error(f"File '{old_file_path}' does not exist")
        raise FileNotFoundError(f"File '{old_file_path}' does not exist")
    
    # check if the new file name has the same extension as the old file name
    if new_file_name.suffix != old_file_path.suffix:
        file_service_logger.error(f"New file name '{new_file_name}' must have the same extension as the old file name '{old_file_path.name}'")
        raise ValueError(f"New file name '{new_file_name}' must have the same extension as the old file name '{old_file_path.name}'")
    
    # create the new file path
    new_file_path = old_file_path.parent / new_file_name
    
    # rename the file
    try:
        new_file_path = old_file_path.rename(new_file_path)
    except PermissionError as e:
        file_service_logger.error(f"Permission error when trying to rename file '{old_file_path}' to '{new_file_path}': {e}")
        raise
    
    
    return Path(new_file_path)

@log_execution(file_service_logger)
def extract_file(zip_path: Path, extract_to_path: Path) -> str:
    """
    Extracts the first file from a ZIP archive to the specified directory.

    Args:
        zip_path (Path): Path to the ZIP file to extract.
        extract_to_path (Path): Directory where contents should be extracted.

    Returns:
        str: Path to the first extracted file.

    Raises:
        ValueError: If zip_path is not a .zip file or arguments aren't Path instances.
        PermissionError: If user lacks permission to extract files.
        OSError: If extraction fails due to system error.

    Examples:
        >>> from pathlib import Path
        >>> zip_file = Path("downloads/invoices.zip")
        >>> extract_dir = Path("extracted")
        >>> extracted_file = extract_file(zip_file, extract_dir)
        >>> print(extracted_file)
        extracted/invoice001.pdf
    """

    # check if the zip_path is a Path instance
    if not isinstance(zip_path, Path):
        file_service_logger.error(f"Argument '{zip_path}' must be an instance of Path")
        raise ValueError(f"Argument '{zip_path}' must be an instance of Path")
    
    # check if the zip_path is a .zip file
    if not zip_path.suffix == ".zip":
        file_service_logger.error(f"File '{zip_path}' must be a .zip file")
        raise ValueError(f"File '{zip_path}' must be a .zip file")
    
    # check if the extract_to_path is a Path instance
    if not isinstance(extract_to_path, Path):
        file_service_logger.error(f"Argument '{extract_to_path}' must be an instance of Path")
        raise ValueError(f"Argument '{extract_to_path}' must be an instance of Path")
    
    #  extract the file
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            file_name = zip_ref.namelist()[0]
            zip_ref.extractall(extract_to_path)
    except PermissionError as e:
        file_service_logger.error(f"Permission error when trying to extract file '{zip_path}' to '{extract_to_path}': {e}")
        raise
    
    
    extracted_file_path = Path(os.path.join(extract_to_path, file_name))
    return extracted_file_path

@log_execution(file_service_logger)
def count_how_many_files(path: Path, extension: str = None) -> int:
    """
    Counts files in a directory, optionally filtering by extension.

    Args:
        path (Path): Directory path to search for files.
        extension (str, optional): File extension to filter by (without dot).

    Returns:
        int: Number of files found matching criteria.

    Raises:
        ValueError: If path is not a directory or extension is invalid.
        FileNotFoundError: If directory doesn't exist.
        PermissionError: If user lacks permission to read directory.

    Examples:
        >>> from pathlib import Path
        >>> doc_dir = Path("documents")
        >>> total_files = count_how_many_files(doc_dir)
        >>> print(f"Total files: {total_files}")
        Total files: 15
        >>> pdf_files = count_how_many_files(doc_dir, "pdf")
        >>> print(f"PDF files: {pdf_files}")
        PDF files: 7
    """
    
    if extension:
        validate_extension(extension)
    
    if not isinstance(path, Path):
        file_service_logger.error(f"Argument '{path}' must be an instance of Path")
        raise ValueError(f"Argument '{path}' must be an instance of Path")
        
    if not path.exists():
        file_service_logger.error(f"Path '{path}' does not exist")
        raise FileNotFoundError(f"Path '{path}' does not exist")
    
    if not path.is_dir():
        file_service_logger.error(f"Path '{path}' is not a directory")
        raise ValueError(f"Path '{path}' is not a directory")
    
    # search for the files
    try:
        if extension:
            paths_to_search = f"*.{extension}"
            paths_with_extension = list(path.glob(paths_to_search))
            return len(paths_with_extension)
        else:
            return len([file for file in os.listdir(path)])
    except PermissionError as e:
        file_service_logger.error(f"Permission error when trying to count files in {path}: {e}")
        raise
    
    
@log_execution(file_service_logger)
def get_last_file_path(path: Path, extension: str) -> Path:
    """
    Retrieves the most recently modified file with specified extension in a directory.

    Args:
        path (Path): Directory to search for files.
        extension (str): File extension to filter by (without dot).

    Returns:
        Path: Path to the most recently modified file.

    Raises:
        ValueError: If path is not a directory or extension is invalid.
        FileNotFoundError: If no matching files found.
        PermissionError: If user lacks permission to read directory.

    Examples:
        >>> from pathlib import Path
        >>> invoice_dir = Path("invoices")
        >>> latest_pdf = get_last_file_path(invoice_dir, "pdf")
        >>> print(latest_pdf)
        invoices/invoice_2024_03_15.pdf
    """
    
    validate_extension(extension)
    
    if not isinstance(path, Path):
        file_service_logger.error(f"Argument '{path}' must be an instance of Path")
        raise ValueError(f"Argument '{path}' must be an instance of Path")
        
    if not path.exists():
        file_service_logger.error(f"Path '{path}' does not exist")
        raise FileNotFoundError(f"Path '{path}' does not exist")
    
    if not path.is_dir():
        file_service_logger.error(f"Path '{path}' is not a directory")
        raise ValueError(f"Path '{path}' is not a directory")
    
    # search for the files
    list_of_files = list(path.glob(f"*.{extension}"))
    
    if not list_of_files:
        file_service_logger.error(f"No files with extension .{extension} found in {path}")
        raise FileNotFoundError(f"No files with extension .{extension} found in {path}")
    
    latest_file_path = max(list_of_files, key=os.path.getctime)
    return latest_file_path
   
@log_execution(file_service_logger)
def lock_until_download_is_complete(path: Path, old_files_quantity: int, extension: str = None) -> bool:
    """
    Monitors a directory until new files appear or timeout occurs.

    Args:
        path (Path): Directory to monitor for new files.
        old_files_quantity (int): Previous count of files in directory.
        extension (str, optional): File extension to monitor (without dot).

    Returns:
        bool: True if new files appeared, False if timeout occurred.

    Raises:
        ValueError: If path is not a directory or arguments are invalid.
        FileNotFoundError: If directory doesn't exist.
        PermissionError: If user lacks permission to read directory.

    Examples:
        >>> from pathlib import Path
        >>> download_dir = Path("downloads")
        >>> initial_count = count_how_many_files(download_dir, "pdf")
        >>> # Start download process here
        >>> is_complete = lock_until_download_is_complete(download_dir, initial_count, "pdf")
        >>> print("Download complete" if is_complete else "Download timeout")
    """
    if not isinstance(path, Path):
        file_service_logger.error(f"Argument '{path}' must be an instance of Path")
        raise ValueError(f"Argument '{path}' must be an instance of Path")
    
    if not isinstance(old_files_quantity, int):
        file_service_logger.error(f"Argument '{old_files_quantity}' must be an instance of int")
        raise ValueError(f"Argument '{old_files_quantity}' must be an instance of int")
    
    if extension:
        validate_extension(extension)
    
    attempts = 0
    MAX_ATTEMPTS = 9
    new_files_quantity = count_how_many_files(path, extension=extension)
    
    # keep checking until the new files quantity is greater than the old files quantity or the max attempts is reached
    while (new_files_quantity == old_files_quantity) and (attempts <= MAX_ATTEMPTS):
        new_files_quantity = count_how_many_files(path, extension)
        attempts += 1
        time.sleep(2)
        
    if new_files_quantity > old_files_quantity:
        return True
    
    return False

@log_execution(file_service_logger)
def delete_all_dir_files(path: Path) -> None:
    """
    Deletes all files within a specified directory while preserving the directory structure.

    This function iterates through all files in the specified directory and removes them.
    It does not remove subdirectories, only files directly in the specified directory.

    Args:
        path (Path): Path object representing the directory whose files should be deleted.

    Returns:
        None

    Raises:
        ValueError: If the path is not a Path instance or not a directory.
        FileNotFoundError: If the specified directory doesn't exist.
        PermissionError: If the user lacks permission to delete files.
        OSError: If file deletion fails due to system error.

    Examples:
        >>> from pathlib import Path
        >>> temp_dir = Path("temp_files")
        >>> # Assuming temp_dir contains files: file1.txt, file2.pdf
        >>> delete_all_dir_files(temp_dir)
        >>> print(len(list(temp_dir.glob('*'))))  # Should print 0
        0

        # Error case - non-existent directory
        >>> delete_all_dir_files(Path("non_existent"))
        FileNotFoundError: Path 'non_existent' does not exist

        # Error case - file instead of directory
        >>> delete_all_dir_files(Path("file.txt"))
        ValueError: Path 'file.txt' is not a directory
    """
    if not isinstance(path, Path):
        file_service_logger.error(f"Argument '{path}' must be an instance of Path")
        raise ValueError(f"Argument '{path}' must be an instance of Path")
    
    if not path.exists():
        file_service_logger.error(f"Path '{path}' does not exist")
        raise FileNotFoundError(f"Path '{path}' does not exist")
    
    if not path.is_dir():
        file_service_logger.error(f"Path '{path}' is not a directory")
        raise ValueError(f"Path '{path}' is not a directory")
    
    try:
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)

            if os.path.isfile(file_path):
                os.remove(file_path)
    except PermissionError as e:
        file_service_logger.error(f"Permission error when trying to delete files in {path}: {e}")
        raise

def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extracts and returns all text from a PDF file using pdfplumber.

    This function opens the specified PDF file, extracts text from each page,
    and concatenates the text into a single string separated by newlines.
    If the PDF contains no extractable text, returns None.

    Args:
        pdf_path (Path): Path object pointing to the PDF file to extract text from.

    Returns:
        str: The combined text from all pages of the PDF, or None if no text is found.

    Raises:
        ValueError: If pdf_path is not a Path instance or is not a .pdf file.
        FileNotFoundError: If the specified PDF file does not exist.
        PermissionError: If the user does not have permission to read the file.

    Examples:
        >>> pdf_path = Path("documents/sample.pdf")
        >>> text = extract_text_from_pdf(pdf_path)
        >>> print(text)
        This is the text content of the PDF.
    """
    if not isinstance(pdf_path, Path):
        file_service_logger.error(f"Argument '{pdf_path}' must be an instance of Path")
        raise ValueError(f"Argument '{pdf_path}' must be an instance of Path")
    
    if not pdf_path.exists():
        file_service_logger.error(f"Path '{pdf_path}' does not exist")
        raise FileNotFoundError(f"Path '{pdf_path}' does not exist")
    
    if not pdf_path.suffix == ".pdf":
        file_service_logger.error(f"File '{pdf_path}' must be a .pdf file")
        raise ValueError(f"File '{pdf_path}' must be a .pdf file")
    
    all_text = []
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
        
            for _, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                
                if page_text:
                    all_text.append(page_text)
    except PermissionError as e:
        file_service_logger.error(f"Permission error when trying to extract text from {pdf_path}: {e}")
        raise
    
    if all_text:
        combined_text = "\n".join(all_text)
        return combined_text
    else:
        combined_text = None
    
    






    
    
    



    


    

    





