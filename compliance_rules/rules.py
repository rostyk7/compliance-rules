from .models import CustomerHistory, RuleResult, RulesConfig, ScreeningRequest


def amount_threshold(request: ScreeningRequest, history: CustomerHistory, config: RulesConfig) -> RuleResult:
    triggered = request.amount > config.amount_threshold
    return RuleResult(
        rule_name="amount_threshold",
        triggered=triggered,
        score=40 if triggered else 0,
        detail={"amount": request.amount, "threshold": config.amount_threshold},
    )


def email_velocity(request: ScreeningRequest, history: CustomerHistory, config: RulesConfig) -> RuleResult:
    triggered = history.email_orders_last_hour > config.email_velocity_threshold
    return RuleResult(
        rule_name="email_velocity",
        triggered=triggered,
        score=30 if triggered else 0,
        detail={"count": history.email_orders_last_hour, "threshold": config.email_velocity_threshold},
    )


def card_sharing(request: ScreeningRequest, history: CustomerHistory, config: RulesConfig) -> RuleResult:
    # Same card used by more than threshold distinct emails in 24h → stolen card signal.
    # Same card / same email is normal repeat purchase and is NOT flagged.
    triggered = history.card_distinct_emails_last_24h > config.card_sharing_threshold
    return RuleResult(
        rule_name="card_sharing",
        triggered=triggered,
        score=50 if triggered else 0,
        detail={
            "distinct_emails": history.card_distinct_emails_last_24h,
            "threshold": config.card_sharing_threshold,
        },
    )


def currency_blacklist(request: ScreeningRequest, history: CustomerHistory, config: RulesConfig) -> RuleResult:
    triggered = request.currency.upper() in config.currency_blacklist
    return RuleResult(
        rule_name="currency_blacklist",
        triggered=triggered,
        score=100 if triggered else 0,
        detail={"currency": request.currency, "blacklist": sorted(config.currency_blacklist)},
    )


def structuring(request: ScreeningRequest, history: CustomerHistory, config: RulesConfig) -> RuleResult:
    # Amounts deliberately kept just under the CTR threshold — smurfing signal.
    triggered = config.structuring_low <= request.amount <= config.structuring_high
    return RuleResult(
        rule_name="structuring",
        triggered=triggered,
        score=35 if triggered else 0,
        detail={
            "amount": request.amount,
            "band": [config.structuring_low, config.structuring_high],
        },
    )


RULES = [
    amount_threshold,
    email_velocity,
    card_sharing,
    currency_blacklist,
    structuring,
]
