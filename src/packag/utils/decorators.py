import time
import inspect
import logging
from functools import wraps


def retry(max_attempts=3):
    """
    Esta função serve como decorator para repetir a execução de determinadas funções por 
    'max_attempts' vezes. Caso não obtenha sucesso após as tentativas, levanta a exceção.

    """
    def decorator(func):
        def wrapper(* args,  **kwargs):
            tentativa = 0
            func_location = inspect.getfile(func)
            error = ""
                
            while tentativa <= max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"Tentativa {tentativa} falhou para a funcaoo {func.__name__} em {func_location}", exc_info=True)
                    error = e
                    tentativa += 1
                    time.sleep(3)

            raise Exception(f"Erro na função {func.__name__} localizada em {func_location}. Erro: {error}")   
        return wrapper
    return decorator

def log_execution(logger: logging.Logger):
    """
    Decorator to log the execution of utility functions using a provided logger.
    
    Args:
        logger (logging.Logger): The logger instance to use.
        level (int): The logging level for the execution log (default: INFO).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            file_path = func.__code__.co_filename
            func_name = func.__name__
            logger.info(f"Function '{func_name}' executed in file '{file_path}'.")
            logger.debug(f"Inputs to '{func_name}': args={args}, kwargs={kwargs}")
            result = func(*args, **kwargs)
            logger.debug(f"Output from '{func_name}': '{result}'")
            return result
        return wrapper
    return decorator


def log_pipeline(logger: logging.Logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Pipeline '{args[0].__class__.__name__}' started")
            result = func(*args, **kwargs)
            logger.info(f"Pipeline '{args[0].__class__.__name__}' finished with result: {result}")
            return result
        return wrapper
    return decorator