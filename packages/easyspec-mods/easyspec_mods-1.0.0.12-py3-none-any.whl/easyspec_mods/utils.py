import inspect
from functools import wraps
import types

def show_signature_if_no_args(func):
    """
    A decorator that prints the function's signature if called without arguments.
    If called with arguments, it executes the function normally.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Check if no arguments were passed
        if not args and not kwargs:
            # Get the function's signature
            sig = inspect.signature(func)
            print(f"\n{' '*4}{func.__name__}{sig}")
        else:
            # Call the function normally if arguments are provided
            return func(*args, **kwargs)
    return wrapper


def decorate_all_functions_within_module(decorator, global_scope):
    """
    Apply the given decorator to all functions in the current module.
    """
    current_globals = global_scope
    for name, obj in current_globals.items():
        if isinstance(obj, types.FunctionType) and name not in ['wraps', 'show_signature_if_no', 'decorate_all_functions_within_module']:  # Check if it's a function
            # print(name)
            # input()
            current_globals[name] = decorator(obj)


