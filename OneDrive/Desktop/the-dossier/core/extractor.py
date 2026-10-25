"""
Text extraction + regex clause analysis.

Handles reading uploaded files (PDF / DOCX / TXT) and running the rulebook
against the extracted text. Deliberately transparent: every finding carries the
exact snippet that triggered it, so a reviewer can verify the machine's reasoning.
"""

from __future__ import annotations

import io
import re

from core.rulebook import SEVERITY_WEIGHT, get_rules


# --------------------------------------------------------------------------- #
# Text extraction
# --------------------------------------------------------------------------- #
def extract_text(filename: str, data: bytes) -> str:
    """Extract plain text from an uploaded file's raw bytes."""
    name = (filename or "").lower()
    if name.endswith(".pdf"):
        return _extract_pdf(data)
    if name.endswith(".docx"):
        return _extract_docx(data)
    # Fallback: treat as UTF-8 text.
    return data.decode("utf-8", errors="ignore")


def _extract_pdf(data: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(data))
    parts = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)


def _extract_docx(data: bytes) -> str:
    import docx

    document = docx.Document(io.BytesIO(data))
    return "\n".join(p.text for p in document.paragraphs)


def normalise(text: str) -> str:
    """Collapse whitespace so multi-line clauses match cleanly."""
    return re.sub(r"\s+", " ", text or "").strip()


# --------------------------------------------------------------------------- #
# Analysis
# --------------------------------------------------------------------------- #
def _snippet(text: str, start: int, end: int, pad: int = 90) -> str:
    lo = max(0, start - pad)
    hi = min(len(text), end + pad)
    prefix = "…" if lo > 0 else ""
    suffix = "…" if hi < len(text) else ""
    return f"{prefix}{text[lo:hi].strip()}{suffix}"


def analyze(raw_text: str) -> dict:
    """
    Run the rulebook against a contract.

    Returns a dict:
      {
        "findings": [ {rule fields + status + matches[]}, ... ],
        "summary":  {"high": n, "medium": n, "low": n, "flagged": n,
                     "checks": total_rules, "risk_score": int, "risk_band": str},
        "word_count": int,
      }
    """
    text = normalise(raw_text)
    lower = text.lower()

    findings: list[dict] = []
    counts = {"high": 0, "medium": 0, "low": 0}

    for rule in get_rules():
        matches: list[str] = []
        for pattern in rule["patterns"]:
            for m in re.finditer(pattern, lower, flags=re.IGNORECASE):
                matches.append(_snippet(text, m.start(), m.end()))
                if len(matches) >= 3:
                    break
            if len(matches) >= 3:
                break

        present = len(matches) > 0
        flagged = present if rule["mode"] == "flag_if_present" else (not present)

        if flagged:
            counts[rule["severity"]] += 1
            status = "flagged"
        else:
            status = "ok"

        findings.append(
            {
                "id": rule["id"],
                "clause_type": rule["clause_type"],
                "title": rule["title"],
                "severity": rule["severity"],
                "mode": rule["mode"],
                "status": status,
                "matches": matches,
                "rationale": rule["rationale"],
                "recommendation": rule["recommendation"],
            }
        )

    # Sort: flagged first (by severity), then the clean checks.
    order = {"high": 3, "medium": 2, "low": 1}
    findings.sort(
        key=lambda f: (f["status"] == "flagged", order[f["severity"]]),
        reverse=True,
    )

    flagged_total = sum(counts.values())
    risk_score = sum(counts[s] * SEVERITY_WEIGHT[s] for s in counts)
    if counts["high"] > 0 or risk_score >= 8:
        band = "High risk"
    elif flagged_total > 0:
        band = "Moderate risk"
    else:
        band = "Low risk"

    return {
        "findings": findings,
        "summary": {
            **counts,
            "flagged": flagged_total,
            "checks": len(findings),
            "risk_score": risk_score,
            "risk_band": band,
        },
        "word_count": len(text.split()),
    }
