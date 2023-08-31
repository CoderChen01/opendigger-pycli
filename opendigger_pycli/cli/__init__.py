from .base import opendigger_cmd as opendigger
from .base import query_cmd as query
from .commands.config_cmd import config
from .commands.display_cmd import display
from .commands.export_cmd import export

opendigger.add_command(config)

query.add_command(display)
query.add_command(export)
