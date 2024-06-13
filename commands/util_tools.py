def docstring_prefix(prefix):
    def decorator(func):
        func.__doc__ = prefix + (func.__doc__ or '')
        return func
    return decorator
