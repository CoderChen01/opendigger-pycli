import typing as t
from functools import update_wrapper

import click

if t.TYPE_CHECKING:
    from click import Context


# def pass_meta_key(
#     key: str, *, doc_description: t.Optional[str] = None
# ) -> "t.Callable[[t.Callable[te.Concatenate[t.Any, P], R]], t.Callable[P, R]]":
#     """Create a decorator that passes a key from
#     :attr:`click.Context.meta` as the first argument to the decorated
#     function.

#     :param key: Key in ``Context.meta`` to pass.
#     :param doc_description: Description of the object being passed,
#         inserted into the decorator's docstring. Defaults to "the 'key'
#         key from Context.meta".

#     .. versionadded:: 8.0
#     """

#     def pass_decorator(ctx: "Context" = None):
#         def decorator(
#             f: "t.Callable[te.Concatenate[t.Any, P], R]",
#         ) -> "t.Callable[P, R]":
#             def new_func(*args: "P.args", **kwargs: "P.kwargs") -> R:
#                 if ctx is None:
#                     ctx = click.get_current_context()
#                 obj = ctx.meta[key]
#                 return ctx.invoke(f, obj, *args, **kwargs)

#             return update_wrapper(new_func, f)

#         if doc_description is None:
#             doc_description = (
#                 f"the {key!r} key from :attr:`click.Context.meta`"
#             )

#         decorator.__doc__ = (
#             f"Decorator that passes {doc_description} as the first argument"
#             " to the decorated function."
#         )

#     return pass_decorator  # type: ignore[return-value]


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
