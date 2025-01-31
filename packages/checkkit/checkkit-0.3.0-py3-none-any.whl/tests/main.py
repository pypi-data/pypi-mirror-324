def test_is_69():
    from checkkit import is_69
    assert is_69(69) == True
    assert is_69(42) == False
    assert is_69(0) == False