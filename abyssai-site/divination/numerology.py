"""
ABYSSAI — Numerology Module · Professor Apollyon
Life Path, Expression, Soul Urge, Personality, Birthday numbers.
Kabbalah, Pythagorean, and Chaldean traditions.
No external API — all calculations local.
"""

from dataclasses import dataclass
from typing import List, Tuple


# ── Letter-to-number mappings ───────────────────────────────────────────────
PYTHAGOREAN = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8,
}

CHALDEAN = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8,
    'I': 1, 'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8,
    'Q': 1, 'R': 2, 'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 6,
    'Y': 7, 'Z': 7,
}

VOWELS = set('AEIOUY')
CONSONANTS = set('BCDFGHJKLMNPQRSTVWXYZ')

MASTER_NUMBERS = {11, 22, 33}

NUMBER_MEANINGS = {
    1:  {"name": "The Leader",       "keyword": "Independence",
         "meaning": "Initiative, originality, courage, self-reliance. You are the spark that starts fires."},
    2:  {"name": "The Peacemaker",   "keyword": "Cooperation",
         "meaning": "Diplomacy, patience, partnership, intuition. You harmonize what others fracture."},
    3:  {"name": "The Communicator", "keyword": "Expression",
         "meaning": "Creativity, joy, social grace, imagination. You give voice to what others feel."},
    4:  {"name": "The Builder",      "keyword": "Stability",
         "meaning": "Order, discipline, practicality, endurance. You lay foundations that last centuries."},
    5:  {"name": "The Freedom-Seeker","keyword": "Change",
         "meaning": "Adventure, versatility, curiosity, freedom. You are the wind that refuses to be caught."},
    6:  {"name": "The Nurturer",     "keyword": "Responsibility",
         "meaning": "Care, harmony, service, domesticity. You heal by holding space for others."},
    7:  {"name": "The Seeker",       "keyword": "Wisdom",
         "meaning": "Analysis, intuition, spirituality, mystery. You see what others overlook."},
    8:  {"name": "The Executive",    "keyword": "Power",
         "meaning": "Authority, abundance, achievement, mastery. You command resources and respect."},
    9:  {"name": "The Humanitarian", "keyword": "Compassion",
         "meaning": "Completion, universal love, service, wisdom. You carry the lessons of all numbers."},
    11: {"name": "The Illuminator",  "keyword": "Inspiration",
         "meaning": "Intuition, enlightenment, inspiration, spiritual insight. A master number."},
    22: {"name": "The Master Builder","keyword": "Manifestation",
         "meaning": "Vision, practical idealism, large-scale achievement. A master number."},
    33: {"name": "The Master Teacher","keyword": "Teaching",
         "meaning": "Healing, compassion, teaching, selfless service. A master number."},
}

NUMBER_ADVICE = {
    1:  "Lead without waiting for permission. Your path is to begin what others fear to start.",
    2:  "Cooperate without losing yourself. Your gift is making peace, not people-pleasing.",
    3:  "Express without apology. Your voice matters — use it to create, not to complain.",
    4:  "Build with patience. Your strength is in showing up every day, not in sudden brilliance.",
    5:  "Embrace change without escaping responsibility. Freedom is earned through discipline.",
    6:  "Serve without sacrificing yourself. You heal others by first healing your own boundaries.",
    7:  "Seek without isolating. Your wisdom is meant to be shared, not hoarded in silence.",
    8:  "Lead without becoming tyrannical. Power is a tool, not a trophy.",
    9:  "Give without depleting yourself. Compassion includes knowing when to say no.",
    11: "Trust your intuition without abandoning reason. You are a bridge between worlds.",
    22: "Build dreams into matter. Your visions are meant to be lived, not just imagined.",
    33: "Teach through example, not martyrdom. Your service elevates others when you remain whole.",
}


def reduce_number(n: int, allow_master: bool = True) -> int:
    """Reduce a number to a single digit or master number."""
    while n >= 10:
        if n in MASTER_NUMBERS and allow_master:
            return n
        n = sum(int(d) for d in str(n))
    return n


def life_path(birth_date) -> int:
    """Calculate Life Path number from birth date."""
    month = birth_date.month
    day = birth_date.day
    year = birth_date.year
    total = month + day + year
    return reduce_number(total)


def expression_number(full_name: str) -> int:
    """Calculate Expression number from full birth name."""
    total = 0
    for ch in full_name.upper():
        if ch.isalpha():
            total += PYTHAGOREAN.get(ch, 0)
    return reduce_number(total)


def soul_urge(full_name: str) -> int:
    """Calculate Soul Urge (Heart's Desire) from vowels in full name."""
    total = 0
    for ch in full_name.upper():
        if ch in VOWELS:
            total += PYTHAGOREAN.get(ch, 0)
    return reduce_number(total)


def personality_number(full_name: str) -> int:
    """Calculate Personality number from consonants in full name."""
    total = 0
    for ch in full_name.upper():
        if ch in CONSONANTS:
            total += PYTHAGOREAN.get(ch, 0)
    return reduce_number(total)


def birthday_number(birth_date) -> int:
    """Calculate Birthday number from day of birth."""
    return reduce_number(birth_date.day)


@dataclass
class NumerologyReading:
    name: str
    birth_date: date
    life_path: int
    expression: int
    soul_urge: int
    personality: int
    birthday: int


def calculate_numerology(name: str, birth_date) -> NumerologyReading:
    """Calculate full numerology reading."""
    return NumerologyReading(
        name=name,
        birth_date=birth_date,
        life_path=life_path(birth_date),
        expression=expression_number(name),
        soul_urge=soul_urge(name),
        personality=personality_number(name),
        birthday=birthday_number(birth_date),
    )


def format_reading(reading: NumerologyReading) -> str:
    """Generate Professor Apollyon's numerology reading text."""
    lp = NUMBER_MEANINGS.get(reading.life_path, {})
    ex = NUMBER_MEANINGS.get(reading.expression, {})
    su = NUMBER_MEANINGS.get(reading.soul_urge, {})
    pe = NUMBER_MEANINGS.get(reading.personality, {})
    bi = NUMBER_MEANINGS.get(reading.birthday, {})

    lines = []
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("  THE NUMBERS DO NOT LIE — THEY ONLY REVEAL")
    lines.append(f"  Subject: {reading.name}")
    lines.append(f"  Born: {reading.birth_date.strftime('%B %d, %Y')}")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("")

    lines.append(f"  LIFE PATH {reading.life_path} — {lp.get('name', 'Unknown')}")
    lines.append(f"    Keyword: {lp.get('keyword', '')}")
    lines.append(f"    {lp.get('meaning', '')}")
    lines.append(f"    {NUMBER_ADVICE.get(reading.life_path, '')}")
    lines.append("")

    lines.append(f"  EXPRESSION {reading.expression} — {ex.get('name', 'Unknown')}")
    lines.append(f"    {ex.get('meaning', '')}")
    lines.append(f"    {NUMBER_ADVICE.get(reading.expression, '')}")
    lines.append("")

    lines.append(f"  SOUL URGE {reading.soul_urge} — {su.get('name', 'Unknown')}")
    lines.append(f"    {su.get('meaning', '')}")
    lines.append("")

    lines.append(f"  PERSONALITY {reading.personality} — {pe.get('name', 'Unknown')}")
    lines.append(f"    {pe.get('meaning', '')}")
    lines.append("")

    lines.append(f"  BIRTHDAY {reading.birthday} — {bi.get('name', 'Unknown')}")
    lines.append(f"    {bi.get('meaning', '')}")
    lines.append("")

    lines.append("  THE VERDICT:")
    lines.append(f"    You were born to {lp.get('keyword', 'be').lower()}.")
    lines.append(f"    Your expression {reading.expression} shows how the world sees you: "
                 f"{ex.get('keyword', '').lower()}.")
    lines.append(f"    Beneath that, your soul urges {su.get('keyword', '').lower()}.")
    lines.append(f"    Your birthday number {reading.birthday} adds {bi.get('keyword', '').lower()}")
    lines.append("    to the mix.")
    lines.append("")
    lines.append("  The numbers are not your prison. They are the rhythm")
    lines.append("  you were born dancing to. Dance better.")
    lines.append("")
    lines.append("  — Professor Apollyon, King-Angel of the Inner Temple")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)