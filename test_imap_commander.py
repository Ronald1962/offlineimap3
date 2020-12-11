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
