from compliance_rules import CustomerHistory, RulesConfig, screen


def test_not_triggered(make_request):
    result = screen(make_request(), history=CustomerHistory(card_distinct_emails_last_24h=2))
    assert "card_sharing" not in result.rules_fired

def test_triggered(make_request):
    result = screen(make_request(), history=CustomerHistory(card_distinct_emails_last_24h=3))
    assert "card_sharing" in result.rules_fired

def test_custom_threshold(make_request):
    result = screen(
        make_request(),
        history=CustomerHistory(card_distinct_emails_last_24h=2),
        config=RulesConfig(card_sharing_threshold=1),
    )
    assert "card_sharing" in result.rules_fired
