from opendigger_pycli.datatypes import ActivityData


def test_activity_fields():
    print(
        ActivityData.__annotations__["value"]
        .__args__[0]
        .__args__[0]
        .__args__[0]
    )
