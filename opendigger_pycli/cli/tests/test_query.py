from click.testing import CliRunner

from opendigger_pycli.cli import opendigger


def test_query():
    runner = CliRunner()
    result = runner.invoke(
        opendigger, ["repo", "-r", "X-lab2017/open-digger", "query"]  # type: ignore
    )
    assert result.exit_code == 0
