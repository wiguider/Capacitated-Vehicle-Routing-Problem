def rounds(value):
    assert isinstance(value, float)
    if value > 50.0:
        return round(float(value / 10), 2)
    return value
