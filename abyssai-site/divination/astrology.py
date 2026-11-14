"""
ABYSSAI — Natal Chart (Astrology) Module · Professor Apollyon
Reads the birth chart: Sun, Moon, Rising, planets in signs/houses.
No external API — all calculations local.
"""

from datetime import datetime, date
from dataclasses import dataclass
from typing import List, Dict, Optional


# ── Zodiac signs with date ranges (tropical) ────────────────────────────────
SIGNS = [
    ("Aries",     "♈",  (3, 21),  (4, 19)),
    ("Taurus",    "♉",  (4, 20),  (5, 20)),
    ("Gemini",    "♊",  (5, 21),  (6, 20)),
    ("Cancer",    "♋",  (6, 21),  (7, 22)),
    ("Leo",       "♌",  (7, 23),  (8, 22)),
    ("Virgo",     "♍",  (8, 23),  (9, 22)),
    ("Libra",     "♎",  (9, 23),  (10, 22)),
    ("Scorpio",   "♏",  (10, 23), (11, 21)),
    ("Sagittarius","♐", (11, 22), (12, 21)),
    ("Capricorn", "♑",  (12, 22), (1, 19)),
    ("Aquarius",  "♒",  (1, 20),  (2, 18)),
    ("Pisces",    "♓",  (2, 19),  (3, 20)),
]

SIGN_RULERS = {
    "Aries":     "Mars",
    "Taurus":    "Venus",
    "Gemini":    "Mercury",
    "Cancer":    "Moon",
    "Leo":       "Sun",
    "Virgo":     "Mercury",
    "Libra":     "Venus",
    "Scorpio":   "Pluto",
    "Sagittarius": "Jupiter",
    "Capricorn": "Saturn",
    "Aquarius":  "Uranus",
    "Pisces":    "Neptune",
}

SIGN_ELEMENTS = {
    "Aries":     "Fire",
    "Taurus":    "Earth",
    "Gemini":    "Air",
    "Cancer":    "Water",
    "Leo":       "Fire",
    "Virgo":     "Earth",
    "Libra":     "Air",
    "Scorpio":   "Water",
    "Sagittarius": "Fire",
    "Capricorn": "Earth",
    "Aquarius":  "Air",
    "Pisces":    "Water",
}

SIGN_QUALITIES = {
    "Aries":     "Cardinal",
    "Taurus":    "Fixed",
    "Gemini":    "Mutable",
    "Cancer":    "Cardinal",
    "Leo":       "Fixed",
    "Virgo":     "Mutable",
    "Libra":     "Cardinal",
    "Scorpio":   "Fixed",
    "Sagittarius": "Mutable",
    "Capricorn": "Cardinal",
    "Aquarius":  "Fixed",
    "Pisces":    "Mutable",
}

PLANETS = [
    "Sun", "Moon", "Mercury", "Venus", "Mars",
    "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto"
]

HOUSE_MEANINGS = {
    1:  "Self, identity, appearance, first impressions",
    2:  "Possessions, values, resources, self-worth",
    3:  "Communication, siblings, short trips, early education",
    4:  "Home, family, roots, mother, inner foundations",
    5:  "Creativity, romance, children, pleasure, self-expression",
    6:  "Health, service, daily routines, work, pets",
    7:  "Partnerships, marriage, contracts, open enemies",
    8:  "Transformation, shared resources, sex, death, rebirth",
    9:  "Higher learning, travel, philosophy, religion, foreign lands",
    10: "Career, public image, reputation, father, ambition",
    11: "Friendships, groups, hopes, wishes, social causes",
    12: "Hidden matters, solitude, secrets, subconscious, institutions",
}


def sign_for_date(month: int, day: int) -> tuple:
    """Return (sign_name, symbol) for a given month/day."""
    for name, symbol, start, end in SIGNS:
        sm, sd = start
        em, ed = end
        if sm < em:
            if (month, day) >= (sm, sd) and (month, day) <= (em, ed):
                return name, symbol
        else:  # wraps around year (Capricorn)
            if (month, day) >= (sm, sd) or (month, day) <= (em, ed):
                return name, symbol
    return "Capricorn", "♑"


def planet_sign(planet: str, month: int, day: int, year: int) -> tuple:
    """
    Simplified planetary position calculation.
    Returns (sign_name, symbol, degree).
    This is a deterministic approximation based on birth data —
    sufficient for personality profiling, not ephemeris-precise.
    """
    # Use birth data as a seed for deterministic but varied placement
    seed = year * 372 + month * 31 + day
    base = {
        "Sun":    0,
        "Moon":   2,
        "Mercury": 1,
        "Venus":  3,
        "Mars":   4,
        "Jupiter": 6,
        "Saturn": 8,
        "Uranus": 10,
        "Neptune": 11,
        "Pluto":  12,
    }[planet]
    idx = (base + seed) % 12
    name, symbol = SIGNS[idx]
    degree = (seed * 13) % 30
    return name, symbol, degree


def house_for_degree(degree: float, asc_degree: float) -> int:
    """Assign a planet to a house based on degree distance from ascendant."""
    rel = (degree - asc_degree) % 360
    house = int(rel // 30) + 1
    return min(house, 12)


@dataclass
class PlanetPosition:
    planet: str
    sign: str
    symbol: str
    degree: float
    house: int
    ruler: str
    element: str
    quality: str


@dataclass
class NatalChart:
    name: str
    birth_date: date
    birth_time: str
    birth_place: str
    sun_sign: str
    sun_symbol: str
    sun_degree: float
    sun_house: int
    moon_sign: str
    moon_symbol: str
    moon_degree: float
    moon_house: int
    rising_sign: str
    rising_symbol: str
    rising_degree: float
    planets: List[PlanetPosition]
    summary: str


def calculate_chart(name: str, birth_date: date, birth_time: str,
                    birth_place: str) -> NatalChart:
    """Calculate a full natal chart from birth data."""
    month = birth_date.month
    day = birth_date.day
    year = birth_date.year

    # Parse time for ascendant approximation
    try:
        hour = int(birth_time.split(":")[0])
    except Exception:
        hour = 12

    # Sun
    sun_name, sun_symbol = sign_for_date(month, day)
    sun_degree = ((day * 7 + month * 3 + year) % 30) + 0.5

    # Moon
    moon_name, moon_symbol, moon_degree = planet_sign("Moon", month, day, year)

    # Ascendant (rising) — approximated from time of day
    asc_idx = (hour * 2 + month) % 12
    rising_name, rising_symbol = SIGNS[asc_idx][0], SIGNS[asc_idx][1]
    rising_degree = ((hour * 17 + day * 3) % 30) + 0.5

    # All planets
    planets = []
    for p in PLANETS:
        p_name, p_symbol, p_degree = planet_sign(p, month, day, year)
        p_house = house_for_degree(p_degree, rising_degree)
        p_ruler = SIGN_RULERS.get(p_name, "Sun")
        p_element = SIGN_ELEMENTS.get(p_name, "Ether")
        p_quality = SIGN_QUALITIES.get(p_name, "Mutable")
        planets.append(PlanetPosition(
            planet=p_name, sign=p_name, symbol=p_symbol,
            degree=p_degree, house=p_house,
            ruler=p_ruler, element=p_element, quality=p_quality
        ))

    # Sun house
    sun_house = house_for_degree(sun_degree, rising_degree)
    moon_house = house_for_degree(moon_degree, rising_degree)

    # Build narrative summary
    summary = build_summary(name, sun_name, moon_name, rising_name,
                            sun_house, moon_house, planets)

    return NatalChart(
        name=name,
        birth_date=birth_date,
        birth_time=birth_time,
        birth_place=birth_place,
        sun_sign=sun_name, sun_symbol=sun_symbol, sun_degree=sun_degree,
        sun_house=sun_house,
        moon_sign=moon_name, moon_symbol=moon_symbol, moon_degree=moon_degree,
        moon_house=moon_house,
        rising_sign=rising_name, rising_symbol=rising_symbol,
        rising_degree=rising_degree,
        planets=planets,
        summary=summary,
    )


def build_summary(name: str, sun: str, moon: str, rising: str,
                  sun_house: int, moon_house: int,
                  planets: List[PlanetPosition]) -> str:
    """Generate Professor Apollyon's narrative reading."""
    lines = []
    lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append(f"  THE SEAL IS BROKEN — NATAL CHART UNVEILED")
    lines.append(f"  Subject: {name}")
    lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("")
    lines.append(f"  THE SUN — {sun} {get_sign_symbol(sun)}")
    lines.append(f"    The core self, the will, the life force.")
    lines.append(f"    Placed in the {sun_house}{ordinal(sun_house)} house — this is where your")
    lines.append(f"    light is meant to shine, where you must become visible.")
    lines.append("")
    lines.append(f"  THE MOON — {moon} {get_sign_symbol(moon)}")
    lines.append(f"    The subconscious, the inner child, emotional tides.")
    lines.append(f"    Housed in the {moon_house}{ordinal(moon_house)} house — this is where")
    lines.append(f"    you retreat to feel safe, where your instincts govern.")
    lines.append("")
    lines.append(f"  THE ASCENDANT — {rising} {get_sign_symbol(rising)}")
    lines.append(f"    The mask you wear, the face you show the world.")
    lines.append(f"    The lens through which all else is filtered.")
    lines.append("")
    lines.append(f"  THE PLANETS IN HOUSES:")
    for p in planets:
        lines.append(f"    {p.planet:10s} in {p.sign:10s} ({p.degree:.1f}°) → House {p.house}")
    lines.append("")
    lines.append("  THE VERDICT:")
    lines.append(f"    You were born under a {sun} sun with {moon} moon and {rising} rising.")
    lines.append(f"    This combination suggests a life of tension between")
    lines.append(f"    {get_sun_archetype(sun)} and {get_moon_archetype(moon)}.")
    lines.append(f"    The rising {rising} colors how others perceive you —")
    lines.append(f"    they see {get_rising_archetype(rising)}, but beneath that")
    lines.append(f"    beats the heart of {sun}.")
    lines.append("")
    lines.append("  The void does not make mistakes. Every placement has")
    lines.append("  its purpose. Your task is not to change the chart,")
    lines.append("  but to stop fighting it and start using it.")
    lines.append("")
    lines.append("  — Professor Apollyon, King-Angel of the Inner Temple")
    lines.append(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)


def get_sign_symbol(name: str) -> str:
    for s, sym, _, _ in SIGNS:
        if s == name:
            return sym
    return ""


def get_sun_archetype(sign: str) -> str:
    return {
        "Aries": "the pioneer who leaps before looking",
        "Taurus": "the builder who refuses to move",
        "Gemini": "the twin who speaks both sides of truth",
        "Cancer": "the nurturer who shelters everything",
        "Leo": "the performer who demands the stage",
        "Virgo": "the critic who perfects through correction",
        "Libra": "the diplomat who weighs every word",
        "Scorpio": "the alchemist who burns to rebuild",
        "Sagittarius": "the archer who aims beyond the horizon",
        "Capricorn": "the climber who scales alone",
        "Aquarius": "the visionary who dreams in code",
        "Pisces": "the mystic who dissolves into feeling",
    }.get(sign, "the soul who wanders")


def get_moon_archetype(sign: str) -> str:
    return {
        "Aries": "emotions that strike like flint on steel",
        "Taurus": "feelings that root like stone in soil",
        "Gemini": "moods that flicker like candlelight",
        "Cancer": "tides that rise and fall without permission",
        "Leo": "a heart that loves in technicolor",
        "Virgo": "anxiety dressed as carefulness",
        "Libra": "emotions balanced on a knife's edge",
        "Scorpio": "feelings that cut to the bone",
        "Sagittarius": "emotions that roam the wilderness",
        "Capricorn": "feelings locked behind stone walls",
        "Aquarius": "feelings observed like specimens",
        "Pisces": "emotions that dissolve into the ocean",
    }.get(sign, "a shadow without a name")


def get_rising_archetype(sign: str) -> str:
    return {
        "Aries": "someone who charges through the door",
        "Taurus": "someone who settles in and refuses to leave",
        "Gemini": "someone who talks their way into every room",
        "Cancer": "someone who mothering everyone they meet",
        "Leo": "someone who enters wearing gold",
        "Virgo": "someone who notices every out-of-place thread",
        "Libra": "someone who smiles and waits to be invited",
        "Scorpio": "someone who watches from the shadows",
        "Sagittarius": "someone who arrives with stories from elsewhere",
        "Capricorn": "someone who carries their ambition like a coat",
        "Aquarius": "someone who looks like they belong nowhere",
        "Pisces": "someone who seems to float through walls",
    }.get(sign, "a face the abyss forgot to name")


def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        return f"{n}th"
    return {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th") + str(n)