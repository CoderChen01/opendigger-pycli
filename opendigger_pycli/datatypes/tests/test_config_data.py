from dataclasses import fields

from opendigger_pycli.datatypes import AppKeyConfig, UserInfoConfig


def test_config_data():
    print(fields(AppKeyConfig))
    print(fields(UserInfoConfig))
