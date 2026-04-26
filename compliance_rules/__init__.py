from .models import CustomerHistory, RuleResult, RulesConfig, ScreeningRequest, ScreeningResult, Verdict
from .rules import RULES

__all__ = [
    "screen",
    "ScreeningRequest",
    "CustomerHistory",
    "RulesConfig",
    "ScreeningResult",
    "RuleResult",
    "Verdict",
]


def screen(
    request: ScreeningRequest,
    history: CustomerHistory | None = None,
    config: RulesConfig | None = None,
) -> ScreeningResult:
    """Run all AML rules against a transaction and return a verdict.

    Args:
        request: The transaction to screen.
        history: Pre-aggregated counts fetched by the caller from their own DB.
                 If omitted, velocity/sharing rules evaluate against zero counts.
        config:  Thresholds and blacklist. If omitted, production defaults are used.
    """
    if history is None:
        history = CustomerHistory()
    if config is None:
        config = RulesConfig()

    results = [rule(request, history, config) for rule in RULES]

    total_score = min(sum(r.score for r in results), 100)
    rules_fired = [r.rule_name for r in results if r.triggered]

    if total_score >= config.blocked_score_min:
        verdict = Verdict.BLOCKED
    elif total_score >= config.flagged_score_min:
        verdict = Verdict.FLAGGED
    else:
        verdict = Verdict.CLEAR

    return ScreeningResult(
        verdict=verdict,
        risk_score=total_score,
        rules_fired=rules_fired,
        rule_results=results,
    )
