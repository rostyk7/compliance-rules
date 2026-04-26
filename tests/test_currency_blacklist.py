import pytest
from compliance_rules import RulesConfig, Verdict, screen


def test_not_triggered(make_request):
    assert "currency_blacklist" not in screen(make_request(currency="USD")).rules_fired

@pytest.mark.parametrize("currency", ["IRR", "KPW", "SYP", "CUC"])
def test_default_blacklisted_currencies(make_request, currency):
    result = screen(make_request(currency=currency))
    assert "currency_blacklist" in result.rules_fired
    assert result.verdict == Verdict.BLOCKED

def test_case_insensitive(make_request):
    assert "currency_blacklist" in screen(make_request(currency="irr")).rules_fired

def test_custom_blacklist(make_request):
    result = screen(make_request(currency="GBP"), config=RulesConfig(currency_blacklist=frozenset({"GBP"})))
    assert "currency_blacklist" in result.rules_fired

def test_custom_blacklist_excludes_defaults(make_request):
    result = screen(make_request(currency="IRR"), config=RulesConfig(currency_blacklist=frozenset({"GBP"})))
    assert "currency_blacklist" not in result.rules_fired
