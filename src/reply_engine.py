"""
reply_engine.py — Core engine for the AI Email Reply Generator.

No API key and no internet required. The engine reads an incoming email,
detects what the sender actually needs (questions, a meeting, a price,
a complaint, a deadline, thanks), and drafts ready-to-send replies in
the tone you choose.

How it works (simple, explainable "AI-style" automation):
  1. Analyse  — scan the email for intent signals, questions, dates,
                urgency and sentiment keywords.
  2. Plan     — turn those signals into reply building blocks
                (acknowledgement, answer placeholder, next step).
  3. Write    — assemble 3 reply variants (Detailed / Balanced / Short)
                in the requested tone, with a proper sign-off.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Tone definitions: greeting, sign-off and filler phrases per tone.
# ---------------------------------------------------------------------------
TONES = {
    "professional": {
        "greeting": "Dear {name},",
        "thanks": "Thank you for your email.",
        "sign_off": "Best regards",
    },
    "friendly": {
        "greeting": "Hi {name},",
        "thanks": "Thanks so much for reaching out!",
        "sign_off": "Warm regards",
    },
    "apologetic": {
        "greeting": "Dear {name},",
        "thanks": "Thank you for your email, and I sincerely apologise for the inconvenience.",
        "sign_off": "With apologies",
    },
    "sales": {
        "greeting": "Hi {name},",
        "thanks": "Great to hear from you — thanks for getting in touch!",
        "sign_off": "Looking forward to working with you",
    },
    "short": {
        "greeting": "Hi {name},",
        "thanks": "Thanks for your email.",
        "sign_off": "Regards",
    },
}

# Keyword groups used for intent detection.
INTENT_KEYWORDS = {
    "meeting": ["meeting", "call", "schedule", "zoom", "discuss", "appointment"],
    "price": ["price", "cost", "quote", "quotation", "budget", "how much", "fee"],
    "complaint": ["not happy", "disappointed", "problem", "issue", "broken", "late delivery", "refund"],
    "thanks": ["thank you", "thanks", "appreciate", "great work", "well done"],
    "order": ["order", "delivery", "shipped", "tracking", "dispatch"],
    "job": ["interview", "application", "resume", "cv", "position", "hiring"],
}

URGENCY_WORDS = ["urgent", "asap", "immediately", "today", "deadline", "by tomorrow", "priority"]


@dataclass
class EmailAnalysis:
    """What the engine found in the incoming email."""

    sender_name: str = "there"
    questions: list[str] = field(default_factory=list)
    intents: list[str] = field(default_factory=list)
    urgent: bool = False
    mentioned_dates: list[str] = field(default_factory=list)
    subject_hint: str = ""


def extract_sender_name(email_text: str, fallback: str = "there") -> str:
    """Try to read the sender's name from a sign-off like 'Regards, Ahmed'."""
    match = re.search(
        r"(?:regards|thanks|best|cheers|sincerely)[,\s]+([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)",
        email_text,
        flags=re.IGNORECASE,
    )
    return match.group(1).strip() if match else fallback


def analyse_email(email_text: str, sender_name: str = "") -> EmailAnalysis:
    """Scan an email and return an EmailAnalysis (questions, intents, urgency)."""
    text = email_text.strip()
    lower = text.lower()
    analysis = EmailAnalysis()
    analysis.sender_name = sender_name or extract_sender_name(text)

    # Questions = sentences ending with '?'
    analysis.questions = [
        s.strip() for s in re.split(r"(?<=[.!?])\s+", text.replace("\n", " ")) if s.strip().endswith("?")
    ]

    # Intent detection from keyword groups
    analysis.intents = [
        intent for intent, words in INTENT_KEYWORDS.items() if any(w in lower for w in words)
    ]

    analysis.urgent = any(w in lower for w in URGENCY_WORDS)

    # Very small date finder: '12 Nov', 'November 12', '12/11/2026', weekdays
    date_patterns = [
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
        r"\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
        r"\b\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\b",
    ]
    for pattern in date_patterns:
        analysis.mentioned_dates += re.findall(pattern, text, flags=re.IGNORECASE)

    # Subject hint = first non-empty line, shortened
    first_line = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")
    analysis.subject_hint = (first_line[:60] + "…") if len(first_line) > 60 else first_line
    return analysis


def _building_blocks(analysis: EmailAnalysis, purpose: str) -> list[str]:
    """Turn the analysis into the middle paragraphs of the reply."""
    blocks: list[str] = []

    if "complaint" in analysis.intents:
        blocks.append(
            "I completely understand your frustration, and I am sorry this happened. "
            "I am looking into it personally and will update you with a solution shortly."
        )
    if analysis.questions:
        joined = " ".join(f'"{q}"' for q in analysis.questions[:2])
        blocks.append(
            f"To answer your question{'s' if len(analysis.questions) > 1 else ''} ({joined}): "
            "[add your answer here — the engine kept your question in view so nothing is missed]."
        )
    if "price" in analysis.intents:
        blocks.append(
            "On pricing: [insert your price / quote here]. This includes [what is included], "
            "and I am happy to walk you through the details."
        )
    if "meeting" in analysis.intents:
        when = f" — {analysis.mentioned_dates[0]} works for me" if analysis.mentioned_dates else ""
        blocks.append(f"A call sounds good{when}. Please let me know a time that suits you, and I will confirm right away.")
    if "order" in analysis.intents:
        blocks.append("I have checked your order status: [insert tracking / delivery update here].")
    if "job" in analysis.intents:
        blocks.append("Thank you for considering me. I have attached / linked my updated CV and portfolio for your review.")
    if "thanks" in analysis.intents and "complaint" not in analysis.intents:
        blocks.append("You are most welcome — I am glad I could help. Please do not hesitate to reach out again.")

    if purpose:
        blocks.append(purpose.strip())
    if analysis.urgent:
        blocks.append("I understand this is urgent, so I am treating it as a priority today.")
    if not blocks:
        blocks.append("I have noted the details in your email and I am on it. I will follow up with a complete update shortly.")
    return blocks


def generate_replies(
    email_text: str,
    tone: str = "professional",
    your_name: str = "Hasnaat",
    sender_name: str = "",
    purpose: str = "",
) -> dict:
    """
    Generate 3 reply variants for an incoming email.

    Returns {"analysis": EmailAnalysis, "replies": {"detailed": str,
    "balanced": str, "short": str}}
    """
    tone_key = tone.lower() if tone.lower() in TONES else "professional"
    style = TONES[tone_key]
    analysis = analyse_email(email_text, sender_name=sender_name)
    greeting = style["greeting"].format(name=analysis.sender_name)
    blocks = _building_blocks(analysis, purpose)
    sign = f"{style['sign_off']},\n{your_name}"

    detailed = "\n\n".join([greeting, style["thanks"]] + blocks + [sign])
    balanced = "\n\n".join([greeting, style["thanks"], blocks[0]] + ([blocks[-1]] if len(blocks) > 1 and purpose else []) + [sign])
    short_body = blocks[0].split(". ")[0].rstrip(".") + "."
    short = "\n\n".join([greeting, short_body, sign])

    return {"analysis": analysis, "replies": {"detailed": detailed, "balanced": balanced, "short": short}}


if __name__ == "__main__":  # Quick self-demo: python -m src.reply_engine
    sample = "Hi, what is your price for a business website? Can we schedule a call on Friday? This is urgent. Regards, Ahmed"
    result = generate_replies(sample)
    print(result["replies"]["balanced"])
