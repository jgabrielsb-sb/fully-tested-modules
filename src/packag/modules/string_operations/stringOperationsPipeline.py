from .functions import *
from abc import ABC, abstractmethod
from typing import Callable

from packag.utils.decorators import log_execution

from packag.utils.logger import get_logger

string_operations_logger = get_logger('string_operations')

class StringOperationsPipeline(ABC):
    
    def __init__(self, pipeline: list[Callable]):
        
        if not isinstance(pipeline, list):
            string_operations_logger.error(f"Input 'pipeline' must be a list")
            raise TypeError("Input 'pipeline' must be a list")
        
        if not all(isinstance(function, Callable) for function in pipeline):
            string_operations_logger.error(f"Input 'pipeline' must be a list of Callable functions")
            raise TypeError("Input 'pipeline' must be a list of Callable functions")
        
        
        self.pipeline = pipeline
    
    @log_execution(string_operations_logger)
    def run(self, input_text: str):
        """
        Run the pipeline of string operations on the input text.
        
        Args:
            text (str): The input text to process.
            
        Returns:
            str: The processed text.
            
        Raises:
            TypeError: If the input is not a string. 
        """
        
        if not isinstance(input_text, str):
            string_operations_logger.error(f"Input 'text' must be a string")
            raise TypeError("Input 'text' must be a string")
        
        for function in self.pipeline:
            input_text = function(input_text)
            
        if not isinstance(input_text, str):
            string_operations_logger.error(f"Output must be a string")
            raise TypeError("Output must be a string")
            
        return input_text


NormalizeEnderecoPipeline = StringOperationsPipeline(
    [
        remove_all_accents,
        remove_all_spaces,
        get_upper_case_string
    ]
)

NormalizeAtvEconomicaPipeline = StringOperationsPipeline(
    [
        get_str_with_only_numbers,
        remove_all_spaces
    ]
)
        