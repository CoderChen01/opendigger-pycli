from click.testing import CliRunner

from opendigger_pycli.cli import opendigger


def test_repo_name_type():
    test_true_repo = "CoderChen01/aocpo"
    runner = CliRunner()
    result = runner.invoke(
        opendigger, ["repo", "--repo", test_true_repo]
    )  # type: ignore
    assert result.exit_code == 0

    test_false_repo = "opendigger\\opendigger"
    result = runner.invoke(
        opendigger, ["repo", "--repo", test_false_repo]
    )  # type: ignore
    assert result.exit_code == 2

    test_non_existing_repo = "opendigger/opendigger"
    result = runner.invoke(
        opendigger, ["repo", "--repo", test_non_existing_repo]
    )  # type: ignore
    assert result.exit_code == 2
