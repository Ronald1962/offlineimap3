# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# Copyright 2020 - Ronald Portier.
from imapcommander import ImapCommander


def test_hello():
    success = False
    try:
        ic = ImapCommander()
        ic.run()
        success = True
    except Exception:
        pass
    assert success
