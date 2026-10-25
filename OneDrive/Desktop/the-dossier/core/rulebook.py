"""
The Dossier — Contract Playbook Rulebook.

A transparent, editable set of rules used to flag risky or missing clauses in a
contract. Every rule is plain-text and regex-driven so a reviewer can always see
*why* something was flagged. No machine learning, no black box.

Two evaluation modes:
  - "flag_if_present": the clause itself is a risk (e.g. uncapped liability).
  - "flag_if_absent":  the clause is a protection that *should* be there
                       (e.g. governing law); its absence is the risk.

Each rule also carries a `plain` line: a one-sentence, jargon-free explanation of
what the issue means for a non-lawyer.

Users can turn rules on/off and change their severity on the Rulebook page; those
overrides live in the database and are merged in by ``get_effective_rules()``.
"""

from __future__ import annotations

# Severity ordering used for sorting and scoring.
SEVERITY_ORDER = {"high": 3, "medium": 2, "low": 1}
SEVERITY_WEIGHT = {"high": 5, "medium": 2, "low": 1}

RULES: list[dict] = [
    {
        "id": "uncapped_liability",
        "clause_type": "Limitation of Liability",
        "title": "Uncapped or Unlimited Liability",
        "severity": "high",
        "mode": "flag_if_present",
        "plain": "If something goes wrong, there is no ceiling on how much you could be made to pay.",
        "patterns": [
            r"unlimited\s+liabilit",
            r"without\s+(?:any\s+)?limit(?:ation)?\s+(?:as\s+to|of|on)\s+liabilit",
            r"liable\s+for\s+all\s+(?:losses|damages|claims)",
            r"no\s+(?:cap|ceiling|limit)\s+on\s+(?:its\s+)?liabilit",
        ],
        "rationale": (
            "The agreement exposes a party to liability with no monetary ceiling. "
            "For a small firm or startup this can be existential — a single dispute "
            "may exceed the entire contract value."
        ),
        "recommendation": (
            "Negotiate a liability cap, typically limited to fees paid in the "
            "preceding 12 months, and carve out only genuinely necessary exceptions."
        ),
    },
    {
        "id": "missing_liability_cap",
        "clause_type": "Limitation of Liability",
        "title": "No Limitation of Liability Clause",
        "severity": "high",
        "mode": "flag_if_absent",
        "plain": "Nothing in this contract limits how much you could owe if there is a dispute.",
        "patterns": [
            r"limitation\s+of\s+liabilit",
            r"aggregate\s+liabilit",
            r"total\s+liabilit\w*\s+(?:shall|will|is)\s+(?:not\s+)?(?:exceed|be\s+limited)",
            r"liabilit\w*\s+(?:shall|will)\s+not\s+exceed",
        ],
        "rationale": (
            "No limitation of liability clause was found. Without one, liability "
            "defaults to being effectively open-ended under general contract law."
        ),
        "recommendation": (
            "Insert a mutual limitation of liability clause with a clear aggregate "
            "cap and standard carve-outs (fraud, wilful misconduct, IP infringement)."
        ),
    },
    {
        "id": "one_sided_indemnity",
        "clause_type": "Indemnification",
        "title": "One-Sided or Broad Indemnity",
        "severity": "high",
        "mode": "flag_if_present",
        "plain": "You may have to cover the other side's legal costs and losses — even for things that are not fully your fault.",
        "patterns": [
            r"shall\s+(?:fully\s+)?indemnify(?:,)?\s+defend\s+and\s+hold\s+harmless",
            r"indemnify\s+and\s+hold\s+harmless\s+.{0,40}\s+from\s+and\s+against\s+any\s+and\s+all",
            r"defend,?\s+indemnify",
        ],
        "rationale": (
            "A broad 'indemnify, defend and hold harmless against any and all "
            "claims' obligation can shift disproportionate risk onto one party, "
            "including third-party and consequential claims."
        ),
        "recommendation": (
            "Make indemnities mutual where possible, tie them to specific triggers "
            "(IP, confidentiality, data breach), and subject them to the liability cap."
        ),
    },
    {
        "id": "auto_renewal",
        "clause_type": "Term & Renewal",
        "title": "Automatic Renewal (Evergreen) Clause",
        "severity": "medium",
        "mode": "flag_if_present",
        "plain": "This contract renews itself automatically unless you cancel in time — it is easy to get locked in.",
        "patterns": [
            r"automatically\s+renew",
            r"auto(?:-|\s)?renew",
            r"shall\s+renew\s+for\s+successive",
            r"evergreen",
        ],
        "rationale": (
            "The contract renews automatically unless notice is given. This can lock "
            "a small business into unwanted extensions and recurring fees."
        ),
        "recommendation": (
            "Confirm the notice window and diarise it, or convert to an opt-in "
            "renewal so the term does not extend without an affirmative decision."
        ),
    },
    {
        "id": "termination_for_convenience_one_sided",
        "clause_type": "Termination",
        "title": "One-Sided Termination for Convenience",
        "severity": "medium",
        "mode": "flag_if_present",
        "plain": "The other party can walk away whenever they like — make sure you can too.",
        "patterns": [
            r"terminate\s+(?:this\s+agreement\s+)?(?:at\s+any\s+time\s+)?for\s+(?:any\s+reason|convenience)",
            r"terminate\s+(?:this\s+agreement\s+)?without\s+cause",
            r"sole\s+discretion\s+to\s+terminate",
        ],
        "rationale": (
            "One party may terminate at will. If the right is not reciprocal, it "
            "leaves the other party without revenue certainty or wind-down time."
        ),
        "recommendation": (
            "Make termination-for-convenience rights mutual and add a reasonable "
            "notice period (e.g. 30–60 days) plus payment for work performed."
        ),
    },
    {
        "id": "missing_governing_law",
        "clause_type": "Governing Law & Jurisdiction",
        "title": "No Governing Law / Jurisdiction Clause",
        "severity": "high",
        "mode": "flag_if_absent",
        "plain": "The contract does not say which law applies or which court decides disputes.",
        "patterns": [
            r"governing\s+law",
            r"governed\s+by\s+the\s+laws\s+of",
            r"jurisdiction\s+of\s+the\s+courts",
            r"courts\s+(?:at|of|in)\s+\w+\s+shall\s+have\s+(?:exclusive\s+)?jurisdiction",
        ],
        "rationale": (
            "No governing law or jurisdiction clause was found. Disputes then turn "
            "on conflict-of-law arguments, which is costly and uncertain."
        ),
        "recommendation": (
            "Specify governing law (e.g. laws of India) and the exclusive "
            "jurisdiction of a named city's courts (e.g. courts at Mumbai)."
        ),
    },
    {
        "id": "missing_confidentiality",
        "clause_type": "Confidentiality",
        "title": "No Confidentiality Clause",
        "severity": "medium",
        "mode": "flag_if_absent",
        "plain": "There is no clause protecting the private information you share.",
        "patterns": [
            r"confidential(?:ity)?\s+(?:information|obligations?)",
            r"non(?:-|\s)?disclosure",
            r"shall\s+(?:keep|treat)\s+.{0,30}\s+confidential",
        ],
        "rationale": (
            "No confidentiality obligation was found. Business, technical or "
            "customer information exchanged under the contract is left unprotected."
        ),
        "recommendation": (
            "Add a mutual confidentiality clause defining confidential information, "
            "permitted use, and a survival period after termination."
        ),
    },
    {
        "id": "missing_force_majeure",
        "clause_type": "Force Majeure",
        "title": "No Force Majeure Clause",
        "severity": "low",
        "mode": "flag_if_absent",
        "plain": "If a disaster or event outside anyone's control happens, neither side is protected.",
        "patterns": [
            r"force\s+majeure",
            r"beyond\s+the\s+reasonable\s+control\s+of",
            r"act\s+of\s+god",
        ],
        "rationale": (
            "No force majeure clause was found. Neither party is excused for "
            "failures caused by events genuinely outside their control."
        ),
        "recommendation": (
            "Add a force majeure clause listing qualifying events and the "
            "consequences (suspension, notice, and a long-stop termination right)."
        ),
    },
    {
        "id": "broad_non_compete",
        "clause_type": "Restrictive Covenants",
        "title": "Overly Broad Non-Compete",
        "severity": "medium",
        "mode": "flag_if_present",
        "plain": "There is a clause stopping you from competing — and in India these are often unenforceable anyway.",
        "patterns": [
            r"shall\s+not\s+(?:directly\s+or\s+indirectly\s+)?compete",
            r"non(?:-|\s)?compete",
            r"restrained\s+from\s+(?:carrying\s+on|engaging\s+in)\s+any\s+business",
        ],
        "rationale": (
            "A non-compete restriction is present. Under Section 27 of the Indian "
            "Contract Act, 1872, post-term restraints of trade are generally void, "
            "so a broad clause may be both risky and unenforceable."
        ),
        "recommendation": (
            "Narrow the restraint to the term of the contract and to legitimate "
            "interests; over-broad post-termination non-competes are unlikely to hold."
        ),
    },
    {
        "id": "assignment_without_consent",
        "clause_type": "Assignment",
        "title": "Assignment Without Consent",
        "severity": "low",
        "mode": "flag_if_present",
        "plain": "The other party can hand this contract to someone else without asking you.",
        "patterns": [
            r"may\s+assign\s+(?:this\s+agreement\s+)?(?:its\s+rights\s+)?without\s+(?:the\s+)?(?:prior\s+)?(?:written\s+)?consent",
            r"freely\s+assign",
            r"assign\s+or\s+transfer\s+.{0,40}\s+without\s+consent",
        ],
        "rationale": (
            "A party may assign the contract without consent. You could end up bound "
            "to an unknown counterparty with a different risk profile."
        ),
        "recommendation": (
            "Require prior written consent to assignment, with a carve-out only for "
            "group reorganisations or a bona fide sale of the whole business."
        ),
    },
    {
        "id": "missing_payment_terms",
        "clause_type": "Payment",
        "title": "No Clear Payment / Late-Payment Terms",
        "severity": "medium",
        "mode": "flag_if_absent",
        "plain": "The contract does not clearly say when you get paid or what happens if payment is late.",
        "patterns": [
            r"payment\s+(?:shall\s+be\s+made\s+)?within\s+\d+\s+days",
            r"net\s+\d+",
            r"invoice\w*\s+.{0,40}\s+within\s+\d+\s+days",
            r"interest\s+(?:at|of)\s+.{0,20}\s+(?:per\s+annum|p\.a\.)\s+on\s+(?:overdue|late)",
        ],
        "rationale": (
            "No clear payment window or late-payment interest was found. This "
            "commonly leads to cash-flow disputes for small vendors."
        ),
        "recommendation": (
            "State a payment window (e.g. within 30 days of invoice) and interest "
            "on overdue amounts to discourage delayed payment."
        ),
    },
    {
        "id": "missing_dispute_resolution",
        "clause_type": "Dispute Resolution",
        "title": "No Arbitration / Dispute Resolution Clause",
        "severity": "low",
        "mode": "flag_if_absent",
        "plain": "There is no agreed way to settle disputes, so you would be stuck going to court.",
        "patterns": [
            r"arbitration",
            r"arbitral\s+tribunal",
            r"dispute\w*\s+shall\s+be\s+(?:referred|resolved)",
            r"conciliation",
        ],
        "rationale": (
            "No dispute-resolution mechanism was found. Disputes then default to "
            "litigation, which is slow and expensive in Indian courts."
        ),
        "recommendation": (
            "Add an arbitration clause under the Arbitration and Conciliation Act, "
            "1996, specifying seat, venue, number of arbitrators, and language."
        ),
    },
]

# Convenient lookup by id.
RULES_BY_ID = {r["id"]: r for r in RULES}


def get_rules() -> list[dict]:
    """Return the full rulebook (sorted high → low severity), ignoring overrides."""
    return sorted(RULES, key=lambda r: SEVERITY_ORDER[r["severity"]], reverse=True)


def get_effective_rules() -> list[dict]:
    """
    Return only the *enabled* rules, with any user severity override applied.

    Overrides come from the database (see core.db.get_rule_settings). Imported
    lazily to keep this module dependency-free for callers that only need data.
    """
    from core.db import get_rule_settings

    settings = get_rule_settings()
    effective: list[dict] = []
    for rule in RULES:
        cfg = settings.get(rule["id"], {})
        if not cfg.get("enabled", True):
            continue
        merged = dict(rule)
        merged["severity"] = cfg.get("severity") or rule["severity"]
        effective.append(merged)
    return sorted(effective, key=lambda r: SEVERITY_ORDER[r["severity"]], reverse=True)


def rule_count() -> int:
    return len(RULES)


def active_rule_count() -> int:
    return len(get_effective_rules())
