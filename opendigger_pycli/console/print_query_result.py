from opendigger_pycli.console import CONSOLE


class QueryResultPrinter(object):
    """Prints the result of a query to the console."""

    def __init__(self, query_result):
        self.query_result = query_result

    def print_result(self):
        """Prints the result of a query to the console."""
        CONSOLE.print("Query result:")
        CONSOLE.print(self.query_result)
