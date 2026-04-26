from compliance_rules import CustomerHistory, RulesConfig, screen


def test_not_triggered(make_request):
    result = screen(make_request(), history=CustomerHistory(email_orders_last_hour=3))
    assert "email_velocity" not in result.rules_fired

def test_triggered(make_request):
    result = screen(make_request(), history=CustomerHistory(email_orders_last_hour=4))
    assert "email_velocity" in result.rules_fired

def test_custom_threshold(make_request):
    result = screen(
        make_request(),
        history=CustomerHistory(email_orders_last_hour=2),
        config=RulesConfig(email_velocity_threshold=1),
    )
    assert "email_velocity" in result.rules_fired
