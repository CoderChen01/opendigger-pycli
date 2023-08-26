from .base import opendigger_cmd as opendigger
from .base import query_cmd as query
from .display_cmd import display
from .export_cmd import export
from .config_cmd import config
from .report_cmd import report
from .monitor_cmd import monitor

opendigger.add_command(config)

query.add_command(display)
query.add_command(export)
query.add_command(report)
query.add_command(monitor)
