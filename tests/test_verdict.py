from compliance_rules import CustomerHistory, RulesConfig, Verdict, screen


def test_clean_transaction_is_clear(make_request):
    result = screen(make_request(amount=5000))
    assert result.verdict == Verdict.CLEAR
    assert result.risk_score == 0
    assert result.rules_fired == []

def test_single_medium_rule_is_flagged(make_request):
    # amount_threshold alone → score 40 → FLAGGED
    assert screen(make_request(amount=1_500_000)).verdict == Verdict.FLAGGED

def test_card_sharing_alone_is_blocked(make_request):
    # card_sharing → score 50 → BLOCKED
    result = screen(make_request(), history=CustomerHistory(card_distinct_emails_last_24h=3))
    assert result.verdict == Verdict.BLOCKED

def test_combined_rules_push_to_blocked(make_request):
    # amount_threshold (40) + email_velocity (30) = 70 → BLOCKED
    result = screen(
        make_request(amount=1_500_000),
        history=CustomerHistory(email_orders_last_hour=5),
    )
    assert result.verdict == Verdict.BLOCKED

def test_risk_score_capped_at_100(make_request):
    result = screen(
        make_request(currency="IRR", amount=1_500_000),
        history=CustomerHistory(email_orders_last_hour=5, card_distinct_emails_last_24h=3),
    )
    assert result.risk_score == 100

def test_no_history_defaults_to_zero_counts(make_request):
    assert screen(make_request()).verdict == Verdict.CLEAR

def test_custom_blocked_score_min(make_request):
    # card_sharing scores 50 — normally BLOCKED, but threshold raised to 100
    result = screen(
        make_request(),
        history=CustomerHistory(card_distinct_emails_last_24h=3),
        config=RulesConfig(blocked_score_min=100),
    )
    assert result.verdict == Verdict.FLAGGED
