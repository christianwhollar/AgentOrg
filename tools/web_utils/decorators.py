# decorators.py
import time
import logging

logger = logging.getLogger(__name__)

# Decorator for logging method calls
def log_method_call(func):
    def wrapper(*args, **kwargs):
        logger.info(f'Calling {func.__name__} with args: {args}, kwargs: {kwargs}')
        result = func(*args, **kwargs)
        logger.info(f'{func.__name__} returned: {result}')
        return result
    return wrapper

# Decorator for retrying a method in case of transient failures
def retry_on_exception(max_retries, exceptions, delay=1):
    def decorator(func):
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning(f'Retry {retries + 1}/{max_retries} failed: {e}')
                    retries += 1
                    time.sleep(delay)
            raise Exception(f'Retry limit reached: {func.__name__}')
        return wrapper
    return decorator
