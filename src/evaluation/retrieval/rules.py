"""
Rule-based relevance evaluation.

These rules define the characteristics a retrieved product should
satisfy in order to be considered relevant.

The evaluator uses these rules alongside exact ASIN matching to
perform richer retrieval evaluation.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from typing import Any


class RuleOperator(StrEnum):
    """
    Supported relevance rule operators.
    """

    EQUALS = "equals"
    CONTAINS = "contains"
    GREATER_EQUAL = "greater_equal"
    LESS_EQUAL = "less_equal"


@dataclass(frozen=True, slots=True)
class RelevanceRule:
    """
    Represents a single relevance rule.

    Example
    -------
    field="brand"
    operator=RuleOperator.EQUALS
    value="ZITY Store"
    """

    field: str
    operator: RuleOperator
    value: str | float


class RuleEvaluator:
    """
    Evaluate products against relevance rules.
    """

    def matches(
        self,
        product: Any,
        rules: list[RelevanceRule],
    ) -> bool:
        """
        Return True if the product satisfies every relevance rule.
        """

        return all(
            self._matches_rule(product, rule)
            for rule in rules
        )

    def _matches_rule(
        self,
        product: Any,
        rule: RelevanceRule,
    ) -> bool:
        """
        Evaluate a single relevance rule.
        """

        value = getattr(
            product,
            rule.field,
            None,
        )

        if value is None:
            return False

        match rule.operator:

            case RuleOperator.EQUALS:
                return value == rule.value

            case RuleOperator.CONTAINS:
                return str(rule.value).lower() in str(value).lower()

            case RuleOperator.GREATER_EQUAL:
                return float(value) >= float(rule.value)

            case RuleOperator.LESS_EQUAL:
                return float(value) <= float(rule.value)

        return False