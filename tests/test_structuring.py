from compliance_rules import RulesConfig, screen


def test_not_triggered_below_band(make_request):
    assert "structuring" not in screen(make_request(amount=899_999)).rules_fired

def test_not_triggered_above_band(make_request):
    assert "structuring" not in screen(make_request(amount=1_000_000)).rules_fired

def test_triggered_at_low_boundary(make_request):
    assert "structuring" in screen(make_request(amount=900_000)).rules_fired

def test_triggered_in_band(make_request):
    assert "structuring" in screen(make_request(amount=990_000)).rules_fired

def test_custom_band(make_request):
    result = screen(
        make_request(amount=450_000),
        config=RulesConfig(structuring_low=400_000, structuring_high=499_999),
    )
    assert "structuring" in result.rules_fired
