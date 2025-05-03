import unicodedata

from packag.utils.decorators import log_execution

from packag.utils.logger import get_logger

string_operation_logger = get_logger('string_operations')

@log_execution(string_operation_logger)
def remove_all_accents(text: str) -> str:
    """
    Remove all accents from a string.
    
    Args:
        text (str): The input string to remove accents from.
        
    Returns:
        str: The input string without accents.
        
    Raises:
        TypeError: If the input is not a string.
        
    """
    if not isinstance(text, str):
        string_operation_logger.error(f"Input must be a string")
        raise TypeError("Input must be a string")
    
    return ''.join(char for char in unicodedata.normalize('NFD', text) if unicodedata.category(char) != 'Mn')

@log_execution(string_operation_logger)
def remove_all_spaces(text: str) -> str:
    """
    Remove all spaces from a string.
    
    Args:
        text (str): The input string to remove spaces from.
        
    Returns:
        str: The input string without spaces.
        
    Raises:
        TypeError: If the input is not a string.
        
    """
    if not isinstance(text, str):
        string_operation_logger.error(f"Input must be a string")
        raise TypeError("Input must be a string")
    
    return text.replace(' ', '')

@log_execution(string_operation_logger)
def get_upper_case_string(text: str) -> str:
    """
    Convert a string to uppercase.
    
    Args:
        text (str): The input string to convert to uppercase.
        
    Returns:
        str: The input string in uppercase.
        
    Raises:
        TypeError: If the input is not a string.
        
    """
    if not isinstance(text, str):
        string_operation_logger.error(f"Input must be a string")
        raise TypeError("Input must be a string")
    
    return text.upper()

@log_execution(string_operation_logger)
def get_str_with_only_numbers(text: str) -> str:
    """
    Get a string with only numbers.
    
    Args:
        text (str): The input string to get only numbers from.
        
    Returns:
        str: The input string with only numbers.
        
    Raises:
        TypeError: If the input is not a string.
        
    """
    if not isinstance(text, str):
        string_operation_logger.error(f"Input must be a string")
        raise TypeError("Input must be a string")
    
    return ''.join(char for char in text if char.isdigit())

@log_execution(string_operation_logger)
def get_formatted_cpf(cpf: str) -> str:
    """
    Formata um string para o formato de CPF: XXX.XXX.XXX-XX

    :param cpf: string que representa o CPF
    :return: cpf formatado XXX.XXX.XXX-XX
    :raises ValueError: se a string não contém 11 dígitos.
    """
    
    if not isinstance(cpf, str):
        string_operation_logger.error(f"Input must be a string")
        raise TypeError("Input must be a string")
    
    if len(cpf) != 11 or not cpf.isdigit():
        string_operation_logger.error(f"CPF must be a string of exactly 11 digits.")
        raise ValueError("CPF must be a string of exactly 11 digits.")
    
    formatted_cpf = f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return formatted_cpf

@log_execution(string_operation_logger)
def safe_float(value: object | None) -> float | None:
    """
    Converts value to float, returning None if conversion fails.
    
    Args:
        value: The value to convert to float.
        
    Returns:
        float: The value converted to float.
        None: If the value is not a string or if conversion fails.
    """
    if value is None:
        return None
    
    try:
        return float(value)
    except (TypeError, ValueError):
        string_operation_logger.info(f"Could not convert {value} to float")
        return None

@log_execution(string_operation_logger)
def safe_int(value: object | None) -> int | None:
    """
    Converts value to int, returning None if conversion fails.
    """
    if value is None:
        return None
    
    try:
        return int(value)
    except (TypeError, ValueError):
        string_operation_logger.info(f"Could not convert {value} to int")
        return None


@log_execution(string_operation_logger)
def safe_str(value: object | None) -> str | None:
    """
    Converts value to str, returning None if conversion fails.
    
    Args:
        value: The value to convert to str.
        
    Returns:
        str: The value converted to str.
        None: If the value is not a string or if conversion fails.
    """
    if value is None:
        return None
    
    try:
        return str(value)
    except (TypeError, ValueError):
        string_operation_logger.info(f"Could not convert to str")
        return None