def test_vision_annotate(setup_vision_client):
    vc = setup_vision_client

    with open('./images/whale.jpeg', 'rb') as f:
        resp = vc.annotate(content=f.read())
        assert(len(resp))