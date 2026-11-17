"""GoBOT triage: a lightweight, dependency-free keyword classifier.

It suggests a category, a priority and a short summary for a new request.
The interface (`triage`) is deliberately small so the body can later be
swapped for a call to a real LLM API without touching the views.
"""
import re

from .models import ServiceRequest

C = ServiceRequest.Category
P = ServiceRequest.Priority

CATEGORY_KEYWORDS = {
    C.BILLING: ["invoice", "billing", "charge", "charged", "refund", "payment", "price", "subscription", "receipt"],
    C.ACCOUNT: ["password", "login", "log in", "sign in", "account", "locked", "access", "permission", "username", "2fa"],
    C.TECHNICAL: ["error", "bug", "crash", "crashes", "broken", "not working", "slow", "down", "outage", "fails", "failed", "install"],
}

PRIORITY_KEYWORDS = {
    P.URGENT: ["urgent", "asap", "immediately", "emergency", "outage", "production down", "data loss", "security breach"],
    P.HIGH: ["cannot", "can't", "unable", "blocked", "critical", "crash", "crashes", "deadline"],
    P.LOW: ["question", "suggestion", "feature request", "when possible", "no rush", "minor"],
}


def _score(text: str, words: list[str]) -> int:
    return sum(1 for w in words if w in text)


def _summarize(description: str, limit: int = 140) -> str:
    first = re.split(r"(?<=[.!?])\s+|\n", description.strip(), maxsplit=1)[0]
    return first if len(first) <= limit else first[: limit - 1].rstrip() + "…"


def triage(title: str, description: str) -> dict:
    text = f"{title} {description}".lower()

    scores = {cat: _score(text, words) for cat, words in CATEGORY_KEYWORDS.items()}
    best_cat, best_score = max(scores.items(), key=lambda kv: kv[1])
    category = best_cat if best_score > 0 else C.GENERAL

    priority = P.MEDIUM
    for level in (P.URGENT, P.HIGH, P.LOW):
        if _score(text, PRIORITY_KEYWORDS[level]) > 0:
            priority = level
            break

    return {
        "category": category.value,
        "priority": priority.value,
        "summary": _summarize(description),
    }
