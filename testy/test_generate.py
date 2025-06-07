from projekt.server import Server


def test_generate():
    assert len(Server.generate(4)) == 4
