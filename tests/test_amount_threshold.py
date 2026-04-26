from compliance_rules import RulesConfig, screen


def test_not_triggered(make_request):
    assert "amount_threshold" not in screen(make_request(amount=999_999)).rules_fired

def test_triggered(make_request):
    assert "amount_threshold" in screen(make_request(amount=1_000_001)).rules_fired

def test_exact_boundary_not_triggered(make_request):
    assert "amount_threshold" not in screen(make_request(amount=1_000_000)).rules_fired

def test_custom_threshold(make_request):
    result = screen(make_request(amount=500_001), config=RulesConfig(amount_threshold=500_000))
    assert "amount_threshold" in result.rules_fired
