import re

from .models import PasswordAuditResult


COMMON_PATTERNS = [
    r"password",
    r"123456",
    r"qwerty",
    r"admin",
    r"letmein",
    r"welcome",
    r"iloveyou",
]


LEET_MAP = {
    "a": ["a", "@", "4"],
    "e": ["e", "3"],
    "i": ["i", "1", "!"],
    "o": ["o", "0"],
    "s": ["s", "$", "5"],
}


def generate_defensive_blocklist(seed_terms: list[str], max_terms: int = 100) -> list[str]:
    """Generate weak password pattern variants for policy enforcement, not cracking."""
    out: set[str] = set()
    for term in seed_terms:
        raw = term.strip().lower()
        if not raw:
            continue
        out.add(raw)
        out.add(f"{raw}123")
        out.add(f"{raw}1234")
        out.add(f"{raw}@123")
        out.add(f"{raw}2024")
        out.add(f"{raw}2025")
        out.add(f"{raw}2026")
        out.add(raw[::-1])

        chars = list(raw)
        for i, ch in enumerate(chars):
            if ch in LEET_MAP:
                for alt in LEET_MAP[ch]:
                    candidate = chars.copy()
                    candidate[i] = alt
                    out.add("".join(candidate))

    return sorted(out)[:max_terms]


def password_pattern_features(password: str) -> dict[str, float]:
    unique_ratio = (len(set(password)) / len(password)) if password else 0.0
    digits = len(re.findall(r"\d", password))
    specials = len(re.findall(r"[^A-Za-z0-9]", password))
    letters = len(re.findall(r"[A-Za-z]", password))
    repeated_runs = 1.0 if re.search(r"(.)\1{2,}", password) else 0.0
    keyboard_pattern = 1.0 if re.search(r"qwerty|asdf|zxcv|12345", password.lower()) else 0.0

    return {
        "length": float(len(password)),
        "unique_ratio": round(unique_ratio, 3),
        "digit_ratio": round(digits / len(password), 3) if password else 0.0,
        "special_ratio": round(specials / len(password), 3) if password else 0.0,
        "letter_ratio": round(letters / len(password), 3) if password else 0.0,
        "repeated_runs": repeated_runs,
        "keyboard_pattern": keyboard_pattern,
    }


def audit_password(password: str) -> PasswordAuditResult:
    findings: list[str] = []
    recommendations: list[str] = []
    score = 0

    if len(password) >= 12:
        score += 30
    elif len(password) >= 8:
        score += 18
    else:
        findings.append("Password length is below recommended minimum (12+).")
        recommendations.append("Use at least 12-16 characters.")

    if re.search(r"[A-Z]", password):
        score += 15
    else:
        findings.append("Missing uppercase letters.")
        recommendations.append("Add uppercase letters.")

    if re.search(r"[a-z]", password):
        score += 15
    else:
        findings.append("Missing lowercase letters.")
        recommendations.append("Add lowercase letters.")

    if re.search(r"\d", password):
        score += 15
    else:
        findings.append("Missing numbers.")
        recommendations.append("Add numbers.")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 20
    else:
        findings.append("Missing special characters.")
        recommendations.append("Add special characters.")

    lower = password.lower()
    for pattern in COMMON_PATTERNS:
        if re.search(pattern, lower):
            score -= 20
            findings.append(f"Contains common weak pattern: '{pattern}'.")
            recommendations.append("Avoid dictionary words or common keyboard patterns.")
            break

    if re.search(r"(.)\1{2,}", password):
        score -= 10
        findings.append("Has repeated character sequences.")
        recommendations.append("Avoid repeated character runs.")

    score = max(0, min(100, score))
    if score >= 80:
        rating = "Strong"
    elif score >= 55:
        rating = "Moderate"
    else:
        rating = "Weak"

    if not recommendations:
        recommendations.append("Password is strong. Rotate periodically and avoid re-use.")

    return PasswordAuditResult(
        score=score,
        rating=rating,
        findings=sorted(set(findings)),
        recommendations=sorted(set(recommendations)),
    )
