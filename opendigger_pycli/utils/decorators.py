import typing as t
from functools import update_wrapper

import click


pass_filtered_dataloaders = click.decorators.pass_meta_key(
    "filtered_dataloaders",
    doc_description="Filtered dataloaders stored in context's meta",
)


def process_commands(processors, results):
    """This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    """
    items = results

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


def generator(f):
    """Similar to the :func:`processor` but passes through old values
    unchanged and does not pass through the values as parameter.
    """

    @processor
    def new_func(stream, *args, **kwargs):
        yield from stream
        yield from f(*args, **kwargs)

    return update_wrapper(new_func, f)
