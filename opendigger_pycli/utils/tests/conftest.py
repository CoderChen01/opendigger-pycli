from pathlib import Path

import pytest


@pytest.fixture()
def test_github_pat() -> str:
    with open(Path(__file__).with_name("github_pat.txt")) as f:
        return f.read()
