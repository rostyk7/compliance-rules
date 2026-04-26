from dataclasses import dataclass, field
from enum import Enum


class Verdict(str, Enum):
    CLEAR = "CLEAR"
    FLAGGED = "FLAGGED"
    BLOCKED = "BLOCKED"


@dataclass
class RulesConfig:
    amount_threshold: int = 1_000_000
    email_velocity_threshold: int = 3
    card_sharing_threshold: int = 2
    structuring_low: int = 900_000
    structuring_high: int = 999_999
    currency_blacklist: frozenset[str] = field(
        default_factory=lambda: frozenset({"IRR", "KPW", "SYP", "CUC"})
    )
    flagged_score_min: int = 1
    blocked_score_min: int = 50


@dataclass
class ScreeningRequest:
    order_id: str
    customer_email: str
    amount: int  # cents
    currency: str
    card_token: str
    metadata: dict = field(default_factory=dict)


@dataclass
class CustomerHistory:
    email_orders_last_hour: int = 0
    card_distinct_emails_last_24h: int = 0


@dataclass
class RuleResult:
    rule_name: str
    triggered: bool
    score: int
    detail: dict = field(default_factory=dict)


@dataclass
class ScreeningResult:
    verdict: Verdict
    risk_score: int
    rules_fired: list[str]
    rule_results: list[RuleResult]
