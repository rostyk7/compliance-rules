# compliance-rules

[![PyPI](https://img.shields.io/pypi/v/compliance-rules)](https://pypi.org/project/compliance-rules/)

Stateless AML transaction screening rules engine. Runs a set of configurable rules against a transaction and returns a verdict (`CLEAR`, `FLAGGED`, or `BLOCKED`) along with a risk score and per-rule details.

## Installation

```bash
pip install compliance-rules
```

Or with uv:

```bash
uv add compliance-rules
```

## Quick start

```python
from compliance_rules import screen, ScreeningRequest, CustomerHistory

result = screen(
    request=ScreeningRequest(
        order_id="ord_123",
        customer_email="user@example.com",
        amount=950_000,       # in cents
        currency="USD",
        card_token="tok_abc",
    ),
    history=CustomerHistory(
        email_orders_last_hour=1,
        card_distinct_emails_last_24h=0,
    ),
)

print(result.verdict)      # Verdict.FLAGGED
print(result.risk_score)   # 35
print(result.rules_fired)  # ['structuring']
```

## API

### `screen(request, history=None, config=None) → ScreeningResult`

Run all rules against a transaction.

| Argument | Type | Description |
|---|---|---|
| `request` | `ScreeningRequest` | Transaction details |
| `history` | `CustomerHistory` | Pre-aggregated counts from your DB. Omit to treat all counts as zero. |
| `config` | `RulesConfig` | Thresholds and blacklist. Omit to use production defaults. |

### `ScreeningRequest`

| Field | Type | Description |
|---|---|---|
| `order_id` | `str` | Unique order identifier |
| `customer_email` | `str` | Customer email |
| `amount` | `int` | Amount in cents |
| `currency` | `str` | ISO 4217 currency code |
| `card_token` | `str` | Tokenised card identifier |
| `metadata` | `dict` | Optional pass-through data |

### `CustomerHistory`

These counts must be fetched from your own database before calling `screen`.

| Field | Type | Default | Description |
|---|---|---|---|
| `email_orders_last_hour` | `int` | `0` | Orders placed with this email in the last hour |
| `card_distinct_emails_last_24h` | `int` | `0` | Distinct emails that used this card token in the last 24 h |

### `RulesConfig`

All thresholds have production-safe defaults.

| Field | Type | Default | Description |
|---|---|---|---|
| `amount_threshold` | `int` | `1_000_000` | Cents above which `amount_threshold` rule fires (score +40) |
| `email_velocity_threshold` | `int` | `3` | Orders/hour above which `email_velocity` fires (score +30) |
| `card_sharing_threshold` | `int` | `2` | Distinct emails/24 h above which `card_sharing` fires (score +50) |
| `structuring_low` | `int` | `900_000` | Lower bound of structuring band in cents (score +35) |
| `structuring_high` | `int` | `999_999` | Upper bound of structuring band in cents |
| `currency_blacklist` | `frozenset[str]` | `{"IRR","KPW","SYP","CUC"}` | Currencies that immediately block (score +100) |
| `flagged_score_min` | `int` | `1` | Minimum cumulative score for `FLAGGED` verdict |
| `blocked_score_min` | `int` | `50` | Minimum cumulative score for `BLOCKED` verdict |

### `ScreeningResult`

| Field | Type | Description |
|---|---|---|
| `verdict` | `Verdict` | `CLEAR`, `FLAGGED`, or `BLOCKED` |
| `risk_score` | `int` | Cumulative score, capped at 100 |
| `rules_fired` | `list[str]` | Names of rules that triggered |
| `rule_results` | `list[RuleResult]` | Full per-rule breakdown |

## Rules

| Rule | Triggers when | Score |
|---|---|---|
| `amount_threshold` | `amount > amount_threshold` | +40 |
| `email_velocity` | `email_orders_last_hour > email_velocity_threshold` | +30 |
| `card_sharing` | `card_distinct_emails_last_24h > card_sharing_threshold` | +50 |
| `currency_blacklist` | `currency` is in the blacklist | +100 |
| `structuring` | `amount` falls in `[structuring_low, structuring_high]` | +35 |

Scores are summed and capped at 100. A score ≥ 50 produces `BLOCKED`; ≥ 1 produces `FLAGGED`; 0 produces `CLEAR`.

## Verdict flow

```
score ≥ blocked_score_min (50)  →  BLOCKED
score ≥ flagged_score_min  (1)  →  FLAGGED
score == 0                      →  CLEAR
```

## Development

```bash
uv sync
uv run pytest --cov=compliance_rules
```

## License

MIT
