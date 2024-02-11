def trace_function(func):
    def wrapper(*args, **kwargs):
        'print(f"Entering function: {func.__name__}")'
        result = func(*args, **kwargs)
        'print(f"Exiting function: {func.__name__}")'
        return result
    return wrapper