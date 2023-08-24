from .base import opendigger, repo, user
from .query_cmd import query


repo.add_command(query)
user.add_command(query)
