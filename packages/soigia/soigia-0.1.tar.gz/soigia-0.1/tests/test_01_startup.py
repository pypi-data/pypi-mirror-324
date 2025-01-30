# from soigia.envs import *
from soigia.models import Token


def test_startup():
    assert len(Token.objects.all()) >= 0
