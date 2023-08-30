from .base import opendigger_cmd as opendigger
from .base import query_cmd as query

from .commands.config_cmd import config
from .commands.display_cmd import display
from .commands.export_cmd import export
from .commands.monitor_cmd import monitor
from .commands.report_cmd import report

opendigger.add_command(config)

query.add_command(display)
query.add_command(export)
query.add_command(report)
query.add_command(monitor)
