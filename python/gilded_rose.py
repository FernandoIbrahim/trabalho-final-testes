# -*- coding: utf-8 -*-
"""
Gilded Rose Refactored with Strategy Pattern and SOLID Principles
Applies Clean Code principles: semantic naming, single responsibility,
DRY (Don't Repeat Yourself), and Strategy Pattern for extensibility.
"""

from abc import ABC, abstractmethod
from typing import List


class Item:
    """Represents an item in the Gilded Rose inventory."""
    
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self) -> str:
        return f"{self.name}, {self.sell_in}, {self.quality}"


class QualityUpdater(ABC):
    """
    Abstract base class implementing Strategy Pattern for quality updates.
    Removes nested conditionals and provides semantic operations.
    """
    
    MINIMUM_QUALITY = 0
    MAXIMUM_QUALITY = 50
    
    @abstractmethod
    def update_quality(self, item: Item) -> None:
        """Update item quality according to item type rules."""
        pass
    
    @abstractmethod
    def update_sell_in(self, item: Item) -> None:
        """Update item sell_in value."""
        pass
    
    def clamp_quality(self, quality: int) -> int:
        """Enforce quality boundaries [0, 50] - removes code duplication."""
        return max(self.MINIMUM_QUALITY, min(quality, self.MAXIMUM_QUALITY))
    
    def is_expired(self, item: Item) -> bool:
        """Semantic check for expiration - improves readability."""
        return item.sell_in < 0
    
    def decrease_sell_in(self, item: Item) -> None:
        """Semantic method for sell_in decrement."""
        item.sell_in -= 1


class NormalItemUpdater(QualityUpdater):
    """
    Strategy for normal items (neither Aged Brie nor Backstage passes).
    Degrades quality by 1 before expiration, 2 after.
    """
    
    def update_quality(self, item: Item) -> None:
        """Decrease quality by 1 before expiration, 2 after."""
        self._degrade_quality_before_expiration(item)
    
    def update_sell_in(self, item: Item) -> None:
        """Decrease sell_in by 1 each day."""
        self.decrease_sell_in(item)
        # Apply double degradation after sell_in becomes negative
        if self.is_expired(item):
            self._degrade_quality_additional_after_expiration(item)
    
    def _degrade_quality_before_expiration(self, item: Item) -> None:
        """Quality decreases by 1 before sell_in date."""
        item.quality = self.clamp_quality(item.quality - 1)
    
    def _degrade_quality_additional_after_expiration(self, item: Item) -> None:
        """Quality degrades one more time after becoming expired."""
        item.quality = self.clamp_quality(item.quality - 1)


class AgedBrieUpdater(QualityUpdater):
    """
    Strategy for Aged Brie.
    Improves quality by 1 before expiration, 2 after (opposite of normal items).
    """
    
    def update_quality(self, item: Item) -> None:
        """Increase quality by 1 before expiration, 2 after."""
        self._improve_quality_before_expiration(item)
    
    def update_sell_in(self, item: Item) -> None:
        """Decrease sell_in by 1 each day."""
        self.decrease_sell_in(item)
        # Apply additional improvement after sell_in becomes negative
        if self.is_expired(item):
            self._improve_quality_additional_after_expiration(item)
    
    def _improve_quality_before_expiration(self, item: Item) -> None:
        """Quality increases by 1 before sell_in date."""
        item.quality = self.clamp_quality(item.quality + 1)
    
    def _improve_quality_additional_after_expiration(self, item: Item) -> None:
        """Quality improves one more time after becoming expired."""
        item.quality = self.clamp_quality(item.quality + 1)


class BackstagePassUpdater(QualityUpdater):
    """
    Strategy for Backstage passes with tiered quality increases.
    Implements complex logic without nested conditionals.
    """
    
    DAYS_CRITICAL_ZONE = 6   # Less than 6 days: +3
    DAYS_URGENT_ZONE = 11    # Less than 11 days: +2
    
    def update_quality(self, item: Item) -> None:
        """Increase quality based on urgency (days until concert)."""
        self._increase_quality_by_urgency(item)
    
    def update_sell_in(self, item: Item) -> None:
        """Decrease sell_in by 1 each day."""
        self.decrease_sell_in(item)
        # Drop quality to 0 after concert
        if self.is_expired(item):
            self._expire_backstage_pass(item)
    
    def _increase_quality_by_urgency(self, item: Item) -> None:
        """Increase quality based on days until concert (tiered bonuses)."""
        quality_increase = self._calculate_quality_increase(item.sell_in)
        item.quality = self.clamp_quality(item.quality + quality_increase)
    
    def _calculate_quality_increase(self, days_until_concert: int) -> int:
        """
        Extract quality increase calculation to semantic method.
        Replaces nested if-statements with clear logic flow.
        """
        if days_until_concert < self.DAYS_CRITICAL_ZONE:
            return 3  # 5 days or less: increase by 3
        elif days_until_concert < self.DAYS_URGENT_ZONE:
            return 2  # 6-10 days: increase by 2
        else:
            return 1  # More than 10 days: increase by 1
    
    def _expire_backstage_pass(self, item: Item) -> None:
        """Backstage pass loses all value after concert."""
        item.quality = self.MINIMUM_QUALITY


class SulfurasUpdater(QualityUpdater):
    """
    Strategy for Sulfuras (legendary item).
    Implements the invariant: Sulfuras never changes.
    """
    
    def update_quality(self, item: Item) -> None:
        """Sulfuras is legendary - quality never changes."""
        pass  # No operation - immutable
    
    def update_sell_in(self, item: Item) -> None:
        """Sulfuras is legendary - sell_in never changes."""
        pass  # No operation - immutable


class ItemUpdaterFactory:
    """
    Factory Pattern for creating strategies.
    Implements Open/Closed Principle: open for extension, closed for modification.
    Adding new item types requires only adding a new strategy class.
    """
    
    def __init__(self):
        """Initialize with all known item type strategies."""
        self._strategies = {
            "Aged Brie": AgedBrieUpdater(),
            "Backstage passes to a TAFKAL80ETC concert": BackstagePassUpdater(),
            "Sulfuras, Hand of Ragnaros": SulfurasUpdater(),
        }
    
    def get_updater(self, item_name: str) -> QualityUpdater:
        """
        Get the appropriate strategy for an item.
        Returns NormalItemUpdater for unknown types (default).
        """
        return self._strategies.get(item_name, NormalItemUpdater())
    
    def register_strategy(self, item_name: str, updater: QualityUpdater) -> None:
        """
        Register a new item type strategy.
        Allows runtime addition of new item types without modifying existing code.
        """
        self._strategies[item_name] = updater


class GildedRose:
    """
    Main inventory manager using Strategy Pattern.
    
    Improvements over original:
    - No nested conditionals (max 2 levels instead of 6+)
    - Clear separation of concerns via strategies
    - Easy to add new item types without modifying this class
    - Semantic method names explain intent
    - Small, cohesive methods with single responsibility
    - No code duplication (shared logic in base class)
    """
    
    def __init__(self, items: List[Item]):
        self.items = items
        self._updater_factory = ItemUpdaterFactory()
    
    def update_quality(self) -> None:
        """Update quality for all items in inventory."""
        for item in self.items:
            self._update_single_item(item)
    
    def _update_single_item(self, item: Item) -> None:
        """
        Update a single item using the appropriate strategy.
        Delegates to the strategy pattern for type-specific logic.
        Note: First update quality, then update sell_in (which may apply post-expiration logic).
        """
        updater = self._updater_factory.get_updater(item.name)
        updater.update_quality(item)
        updater.update_sell_in(item)
