import typing as t
from functools import update_wrapper


def process_commands(processors, params: t.List[str]):
    """This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    """
    items = (param for param in params)

    # Pipe it through all item processors.
    for processor in processors:
        items = processor(items)

    # Evaluate the items and throw away the item.
    for _ in items:
        pass


def processor(f):
    """Helper decorator to rewrite a function so that it returns another
    function from it.
    """

    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)

        return processor

    return update_wrapper(new_func, f)
