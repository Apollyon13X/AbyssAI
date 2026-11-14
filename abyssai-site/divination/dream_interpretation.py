"""
ABYSSAI — Dream Interpretation Module · Professor Apollyon
Freudian, Miller, and symbolic dream analysis.
All interpretations local — no external API.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import re


# ── Dream symbol dictionary (from Miller, Freud, psychoanalytic tradition) ──
DREAM_SYMBOLS = {
    # Water
    "water": {
        "meaning": "Emotions, the subconscious, the flow of life",
        "interpretation": "Calm water = emotional clarity. Murky water = repressed feelings. Drowning = being overwhelmed by emotion.",
    },
    "ocean": {
        "meaning": "The collective unconscious, vast unknown",
        "interpretation": "Vast emotional depths. Stormy seas = inner turmoil. Calm sea = peace with the subconscious.",
    },
    "river": {
        "meaning": "Life's journey, passage of time",
        "interpretation": "Crossing a river = transition. Drowning in a river = being swept away by circumstance.",
    },
    # Flying
    "flying": {
        "meaning": "Freedom, escape, transcendence",
        "interpretation": "Flying easily = liberation from burdens. Struggling to fly = fear of failure. Freud saw this as sexual release.",
    },
    # Falling
    "falling": {
        "meaning": "Loss of control, fear, insecurity",
        "interpretation": "Sudden fall = anxiety about a situation. Falling and waking = fear of failure in waking life.",
    },
    # Teeth
    "teeth": {
        "meaning": "Power, confidence, communication",
        "interpretation": "Losing teeth = fear of aging, loss of power, or communication breakdown. Broken teeth = vulnerability.",
    },
    # Death
    "death": {
        "meaning": "Transformation, endings, rebirth",
        "interpretation": "Dreaming of death rarely means literal death. It signals the end of a phase — job, relationship, identity — and rebirth into something new.",
    },
    # Naked
    "naked": {
        "meaning": "Vulnerability, exposure, authenticity",
        "interpretation": "Being naked in public = fear of exposure, shame, or desire for authenticity.",
    },
    # House
    "house": {
        "meaning": "The self, psyche, family",
        "interpretation": "Each room represents a part of the psyche. Attic = intellect. Basement = subconscious. Kitchen = nourishment.",
    },
    # Car
    "car": {
        "meaning": "Life direction, control",
        "interpretation": "Driving = control over life. Car crash = fear of losing control. Being a passenger = feeling powerless.",
    },
    # Snake
    "snake": {
        "meaning": "Transformation, hidden fears, sexuality",
        "interpretation": "Snake shedding skin = renewal. Snake bite = hidden threat or repressed sexual energy.",
    },
    # Flying animal
    "bird": {
        "meaning": "Freedom, spirit, messages",
        "interpretation": "Flying bird = spiritual freedom. Caged bird = feeling trapped.",
    },
    # Death/Money
    "money": {
        "meaning": "Value, self-worth, energy",
        "interpretation": "Finding money = unexpected opportunity. Losing money = fear of scarcity.",
    },
    # Fire
    "fire": {
        "meaning": "Passion, destruction, transformation",
        "interpretation": "Controlled fire = passion. Uncontrolled fire = anger, destructive impulses.",
    },
    # Dog
    "dog": {
        "meaning": "Loyalty, friendship, protection",
        "interpretation": "Friendly dog = loyal friends. Aggressive dog = betrayal, conflict.",
    },
    # Cat
    "cat": {
        "meaning": "Independence, intuition, femininity",
        "interpretation": "Cat = independence, mystery. Black cat = superstition, fear of the unknown.",
    },
    # Blood
    "blood": {
        "meaning": "Life force, sacrifice, injury",
        "interpretation": "Blood = vital energy. Losing blood = energy drain, emotional wound.",
    },
    # Death of loved one
    "dead relative": {
        "meaning": "Unresolved grief, ancestral messages",
        "interpretation": "Dreaming of dead relatives = processing grief, receiving ancestral wisdom, unfinished business.",
    },
    # Pregnancy
    "pregnancy": {
        "meaning": "Creativity, new beginnings",
        "interpretation": "Pregnancy = new project, idea, or phase coming to life — not necessarily literal children.",
    },
    # Flying/Teeth combo
    "falling teeth": {
        "meaning": "Powerlessness, anxiety about appearance",
        "interpretation": "Classic anxiety dream. Fear of losing attractiveness, influence, or ability to communicate.",
    },
    # Being chased
    "being chased": {
        "meaning": "Avoidance, fear, running from something",
        "interpretation": "Being chased = avoiding an issue. The chaser = the part of yourself you're avoiding.",
    },
    # School
    "school": {
        "meaning": "Learning, social anxiety, performance",
        "interpretation": "Being late to class = fear of missing opportunity. Being unprepared = performance anxiety.",
    },
    # Elevator
    "elevator": {
        "meaning": "Life transitions, ups and downs",
        "interpretation": "Elevator going up = advancement. Going down = exploring subconscious. Stuck elevator = feeling trapped.",
    },
    # Bridge
    "bridge": {
        "meaning": "Transition, connection",
        "interpretation": "Crossing a bridge = moving from one phase to another. Broken bridge = blocked progress.",
    },
    # Mirror
    "mirror": {
        "meaning": "Self-reflection, truth",
        "interpretation": "Mirror = self-examination. Broken mirror = distorted self-image.",
    },
    # Death of self
    "dying": {
        "meaning": "Transformation, letting go",
        "interpretation": "Dreaming of your own death = major life transition, shedding old identity.",
    },
    # Money lost
    "losing money": {
        "meaning": "Fear of scarcity, loss of value",
        "interpretation": "Losing money = fear of financial instability or loss of self-worth.",
    },
    # Prison
    "prison": {
        "meaning": "Confinement, restriction",
        "interpretation": "Being imprisoned = feeling trapped by circumstances, relationship, or job.",
    },
    # Wedding
    "wedding": {
        "meaning": "Union, commitment, transition",
        "interpretation": "Wedding = commitment to something new — relationship, job, or life phase.",
    },
    # Baby
    "baby": {
        "meaning": "New beginnings, vulnerability, responsibility",
        "interpretation": "Baby = new project, idea, or responsibility entering your life.",
    },
    # Forest
    "forest": {
        "meaning": "The unknown, subconscious",
        "interpretation": "Lost in forest = feeling lost in life. Walking through forest = journey into the unconscious.",
    },
    # Mountain
    "mountain": {
        "meaning": "Challenge, achievement, spiritual ascent",
        "interpretation": "Climbing mountain = pursuing a goal. Reaching summit = achievement.",
    },
    # Door
    "door": {
        "meaning": "Opportunity, transition",
        "interpretation": "Open door = opportunity. Closed door = missed opportunity or blocked path.",
    },
    # Key
    "key": {
        "meaning": "Solution, access, knowledge",
        "interpretation": "Key = solution to a problem. Lost key = feeling locked out of opportunity.",
    },
    # Clock
    "clock": {
        "meaning": "Time, deadlines, mortality",
        "interpretation": "Clock = awareness of time passing. Broken clock = feeling stuck in time.",
    },
    # Mirror
    "mirror": {
        "meaning": "Self-reflection",
        "interpretation": "Mirror = self-examination. What do you see? What do you avoid seeing?",
    },
}


def interpret_symbol(symbol: str) -> dict:
    """Look up a dream symbol."""
    key = symbol.lower().strip()
    if key in DREAM_SYMBOLS:
        return DREAM_SYMBOLS[key]
    # Try partial match
    for k, v in DREAM_SYMBOLS.items():
        if key in k or k in key:
            return v
    return {
        "meaning": "Unknown symbol",
        "interpretation": "The symbol is personal to you. Ask: what emotion does it evoke? What memory does it surface?",
    }


def interpret_dream(dream_text: str) -> str:
    """Analyze a full dream narrative."""
    text = dream_text.lower()
    found_symbols = []

    for symbol in DREAM_SYMBOLS:
        if symbol in text:
            found_symbols.append(symbol)

    lines = []
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("  THE DREAM ORACLE SPEAKS")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    lines.append("")
    lines.append(f"  YOUR DREAM: {dream_text}")
    lines.append("")

    if not found_symbols:
        lines.append("  The void offers no ready-made symbol here.")
        lines.append("  This dream speaks in a private language — yours alone.")
        lines.append("  Ask: what emotion dominated? What color? What temperature?")
        lines.append("")
        lines.append("  — Professor Apollyon")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        return "\n".join(lines)

    lines.append(f"  SYMBOLS DETECTED: {', '.join(found_symbols)}")
    lines.append("")

    for symbol in found_symbols:
        info = interpret_symbol(symbol)
        lines.append(f"  ▸ {symbol.title()}: {info['meaning']}")
        lines.append(f"    → {info['interpretation']}")
        lines.append("")

    lines.append("  THE VERDICT:")
    lines.append("    Dreams are not prophecies. They are the psyche's")
    lines.append("    way of digesting what waking life could not swallow.")
    lines.append("")
    lines.append("    Ask yourself: what emotion did you wake with?")
    lines.append("    That emotion is the key. The symbols are merely doors.")
    lines.append("")
    lines.append("    — Professor Apollyon, King-Angel of the Inner Temple")
    lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    return "\n".join(lines)