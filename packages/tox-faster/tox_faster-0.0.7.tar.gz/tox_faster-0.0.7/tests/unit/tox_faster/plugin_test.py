from unittest.mock import sentinel

import pytest

from tox_faster import plugin


@pytest.mark.parametrize(
    "environ,expected",
    [
        # In dev there's no CI envvar and tox-faster disables the envreport.
        ({}, []),
        # On GitHub Actions CI is set to "true" and tox-faster doesn't disable the envreport.
        ({"CI": "true"}, None),
    ],
)
def test_tox_runenvreport(mocker, environ, expected):
    mocker.patch.dict(plugin.environ, environ)

    assert plugin.tox_runenvreport(sentinel.venv, sentinel.action) == expected
