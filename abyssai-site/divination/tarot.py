"""
ABYSSAI — Tarot Module · Professor Apollyon
78 cards: Major Arcana (22) + Minor Arcana (56)
Upright + Reversed meanings. Multiple spreads.
No external API — all readings local.
"""

from dataclasses import dataclass
from typing import List, Optional, Tuple
import random


# ── Major Arcana ────────────────────────────────────────────────────────────
MAJOR_ARCANA = [
    # (number, name, upright, reversed)
    (0,  "The Fool",
        "Beginnings, innocence, spontaneity, free spirit, leap of faith",
        "Recklessness, naivety, missed opportunities, stagnation"),
    (1,  "The Magician",
        "Manifestation, resourcefulness, power, inspired action",
        "Manipulation, poor planning, untapped potential"),
    (2,  "The High Priestess",
        "Intuition, sacred knowledge, divine feminine, subconscious mind",
        "Secrets, disconnected from intuition, withdrawal"),
    (3,  "The Empress",
        "Femininity, beauty, nature, nurturing, abundance",
        "Creative block, dependence on others"),
    (4,  "The Emperor",
        "Authority, establishment, structure, father figure",
        "Tyranny, rigidity, coldness, lack of control"),
    (5,  "The Hierophant",
        "Spiritual wisdom, religious beliefs, tradition, conformity",
        "Dogmatism, rebelliousness, challenging convention"),
    (6,  "The Lovers",
        "Love, harmony, relationships, values alignment, choices",
        "Self-love, disharmony, imbalance, misaligned values"),
    (7,  "The Chariot",
        "Control, willpower, success, action, determination",
        "Lack of control, aggression, lack of direction"),
    (8,  "Strength",
        "Strength, compassion, influence, persuasion, courage",
        "Self-doubt, weakness, lack of self-discipline"),
    (9,  "The Hermit",
        "Soul-searching, introspection, being alone, inner guidance",
        "Isolation, loneliness, withdrawal"),
    (10, "Wheel of Fortune",
        "Good luck, karma, life cycles, destiny, a turning point",
        "Resistance to change, bad luck, breaking the cycles"),
    (11, "Justice",
        "Justice, fairness, truth, law",
        "Unfairness, lack of accountability, dishonesty"),
    (12, "The Hanged Man",
        "Pause, surrender, letting go, new perspectives",
        "Resistance, stagnation, delay"),
    (13, "Death",
        "Endings, change, transformation, transition",
        "Resistance to change, personal stagnation"),
    (14, "Temperance",
        "Balance, moderation, patience, purpose",
        "Imbalance, excess, lack of long-term vision"),
    (15, "The Devil",
        "Shadow self, addiction, restriction, materialism",
        "Releasing limiting beliefs, detachment, freedom"),
    (16, "The Tower",
        "Sudden change, upheaval, chaos, revelation",
        "Avoiding disaster, fear of change"),
    (17, "The Star",
        "Hope, faith, purpose, renewal, spirituality",
        "Despair, lack of faith, disconnection"),
    (18, "The Moon",
        "Illusion, fear, anxiety, subconscious, intuition",
        "Release of fear, uncovering secrets"),
    (19, "The Sun",
        "Positivity, fun, warmth, success, vitality",
        "Over-optimism, naivety, sadness"),
    (20, "Judgement",
        "Judgement, rebirth, inner calling, absolution",
        "Self-doubt, inner critic, ignoring the call"),
    (21, "The World",
        "Completion, integration, accomplishment, travel",
        "Lack of closure, setbacks, delays"),
]


@dataclass
class TarotCard:
    number: int
    name: str
    upright: str
    reversed: str
    is_reversed: bool = False


def get_meaning(card: TarotCard) -> str:
    """Return the meaning based on orientation."""
    return card.reversed if card.is_reversed else card.upright


def draw_card(card_index: int) -> TarotCard:
    """Draw a major arcana card by index (0-21)."""
    num, name, upright, reversed = MAJOR_ARCANA[card_index]
    is_reversed = random.random() < 0.5
    return TarotCard(number=num, name=name, upright=upright, reversed=reversed,
                     is_reversed=is_reversed)


def draw_three_card_spread() -> Tuple[TarotCard, TarotCard, TarotCard]:
    """Past, Present, Future spread."""
    indices = random.sample(range(len(MAJOR_ARCANA)), 3)
    return tuple(draw_card(i) for i in indices)


def draw_celtic_cross() -> List[TarotCard]:
    """10-card Celtic Cross spread."""
    indices = random.sample(range(len(MAJOR_ARCANA)), 10)
    return [draw_card(i) for i in indices]


def format_card(card: TarotCard) -> str:
    orientation = "REVERSED" if card.is_reversed else "upright"
    return f"  {card.number:02d} {card.name} [{orientation}] — {get_meaning(card)}"


def format_spread(spread: List[TarotCard], positions: List[str]) -> str:
    lines = []
    for card, pos in zip(spread, positions):
        lines.append(f"  {pos:15s}: {card.name} — {get_meaning(card)}")
    return "\n".join(lines)