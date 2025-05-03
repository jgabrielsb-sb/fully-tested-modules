import pytest
from packag.modules.string_operations import (
    remove_all_accents,
    remove_all_spaces,
    get_upper_case_string,
    get_str_with_only_numbers,
    get_formatted_cpf,
    safe_float,
    safe_int,
    safe_str
)

######## REMOVE_ALL_ACCENTS TESTS ########
def test_string_with_accents():
    """Test if a string with accents is converted to a string without accents."""
    input_str = "João está no café."
    expected = "Joao esta no cafe."
    assert remove_all_accents(input_str) == expected

def test_string_without_accents():
    """Test if a string without accents remains the same."""
    input_str = "Simple text"
    expected = "Simple text"
    assert remove_all_accents(input_str) == expected

def test_string_with_numbers():
    """Test if a string with numbers retains the numbers."""
    input_str = "Café 123"
    expected = "Cafe 123"
    assert remove_all_accents(input_str) == expected

def test_string_with_special_characters():
    """Test if a string with special characters remains the same."""
    input_str = "Olá! Como vai? #python"
    expected = "Ola! Como vai? #python"
    assert remove_all_accents(input_str) == expected

def test_invalid_input_type_remove_all_accents():
    with pytest.raises(TypeError):
        remove_all_accents(12345)
        
######## REMOVE_ALL_SPACES TESTS ########

def test_string_with_spaces():
    """Test if a string with spaces is converted to a string without spaces."""
    input_str = "This is a test"
    expected = "Thisisatest"
    assert remove_all_spaces(input_str) == expected

def test_string_without_spaces():
    """Test if a string without spaces remains the same."""
    input_str = "AlreadyClean"
    expected = "AlreadyClean"
    assert remove_all_spaces(input_str) == expected

def test_invalid_input_type_remove_all_spaces():
    with pytest.raises(TypeError):
        remove_all_spaces(12345)
        
######## GET_UPPER_CASE_STRING TESTS ########

def test_string_with_lower_case():
    """Test if a string with lower case is converted to a string with upper case."""
    input_str = "This is a test"
    expected = "THIS IS A TEST"
    assert get_upper_case_string(input_str) == expected
    
def test_string_with_upper_case():
    """Test if a string with upper case remains the same."""
    input_str = "ALREADYUPPER"
    expected = "ALREADYUPPER"
    assert get_upper_case_string(input_str) == expected
    
def test_invalid_input_type_upper_case():
    with pytest.raises(TypeError):
        get_upper_case_string(12345)
    
######## GET_STR_WITH_ONLY_NUMBERS TESTS ########

def test_string_with_numbers():
    """Test if a string with numbers is converted to a string with only numbers."""
    input_str = "12345"
    expected = "12345"
    assert get_str_with_only_numbers(input_str) == expected
    
def test_string_without_numbers():
    """Test if a string without numbers will return an empty string."""
    input_str = "NoNumbersHere"
    expected = ""
    assert get_str_with_only_numbers(input_str) == expected
    
def test_invalid_input_type_only_numbers():
    with pytest.raises(TypeError):
        get_str_with_only_numbers(12345)
        
######## GET_FORMATTED_CPF TESTS ########

def test_value_error_when_cpf_is_not_a_string():
    with pytest.raises(TypeError):
        get_formatted_cpf(12345678901)
        
def test_value_error_when_cpf_has_more_than_11_digits():
    with pytest.raises(ValueError):
        get_formatted_cpf('1234567890345312')
    
def test_value_error_when_cpf_has_less_than_11_digits():
    with pytest.raises(ValueError):
        get_formatted_cpf('03453')
        

def test_value_error_when_cpf_has_non_digit_characters():
    with pytest.raises(ValueError):
        get_formatted_cpf('1234567890345312a')
        
def test_correct_cpf_is_formatted():
    assert get_formatted_cpf('03453123456') == '034.531.234-56'
    assert isinstance(get_formatted_cpf('03453123456'), str)
    
###### SAFE_FLOAT TESTS ########

def test_safe_float_with_none():
    assert safe_float(None) is None
    
def test_safe_float_with_string():
    assert safe_float('123.45') == 123.45
    assert isinstance(safe_float('123.45'), float)
    
def test_safe_float_with_int():
    assert safe_float(123) == 123.0
    assert isinstance(safe_float(123), float)
    
def test_safe_float_with_float():
    assert safe_float(123.45) == 123.45
    assert isinstance(safe_float(123.45), float)
    
def test_safe_float_with_string():
    assert safe_float('STRING') == None
    
def test_safe_float_with_list():
    assert safe_float(['lista']) == None
    
###### SAFE_INT TESTS ########

def test_safe_int_with_none():
    assert safe_int(None) is None

def test_safe_int_with_string():
    assert safe_int('123.45') == 123
    assert isinstance(safe_int('123.45'), int)
    
def test_safe_int_with_int():
    assert safe_int(123) == 123
    assert isinstance(safe_int(123), int)
    
def test_safe_int_with_float():
    assert safe_int(123.45) == 123
    assert isinstance(safe_int(123.45), int)
    
def test_safe_int_with_string():
    assert safe_int('STRING') == None
    
def test_safe_int_with_list():
    assert safe_int(['lista']) == None

###### SAFE_STR TESTS ########

def test_safe_str_with_none():
    assert safe_str(None) == None
    
def test_safe_str_with_string():
    assert safe_str('STRING') == 'STRING'
    assert isinstance(safe_str('STRING'), str)
    
def test_safe_str_with_int():
    assert safe_str(123) == '123'
    assert isinstance(safe_str(123), str)
    
def test_safe_str_with_float():
    assert safe_str(123.45) == '123.45'
    assert isinstance(safe_str(123.45), str)
    
def test_safe_str_with_exotic_class_that_does_not_support_string_conversion():
    class BadStr:
        def __str__(self):
            raise TypeError("BadStr does not support string conversion")
    
    assert safe_str(BadStr()) == None
    
    
        
        
    
    
        
        
        
        
        
        
        
        
        



            
            
    

