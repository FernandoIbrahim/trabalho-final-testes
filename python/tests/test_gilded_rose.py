# -*- coding: utf-8 -*-
import pytest
from gilded_rose import Item, GildedRose


class TestGildedRoseNormalItems:
    """Tests for normal items (neither Aged Brie nor Backstage passes)."""

    @pytest.mark.parametrize(
        "initial_quality,initial_sell_in,expected_quality,expected_sell_in",
        [
            # Boundary: Quality at maximum
            (50, 10, 49, 9),
            # Boundary: Quality at 1 (will decrease to 0)
            (1, 10, 0, 9),
            # Normal case: Quality > 1
            (25, 10, 24, 9),
            # Boundary: sell_in = 1 (before expiration)
            (10, 1, 9, 0),
            # Boundary: Quality = 0 (cannot go below 0)
            (0, 10, 0, 9),
            # Equivalence class: High quality, far from expiration
            (45, 20, 44, 19),
            # Equivalence class: Low quality, far from expiration
            (5, 20, 4, 19),
        ],
    )
    def test_normal_item_quality_decreases(
        self, initial_quality, initial_sell_in, expected_quality, expected_sell_in
    ):
        """Normal items decrease in quality by 1 before expiration."""
        items = [Item("Normal Item", initial_sell_in, initial_quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        assert items[0].quality == expected_quality
        assert items[0].sell_in == expected_sell_in

    @pytest.mark.parametrize(
        "initial_quality,initial_sell_in,expected_quality",
        [
            # Boundary: Just expired
            (10, -1, 8),
            # Boundary: Far expired
            (10, -10, 8),
            # Boundary: Quality at 2 (decreases by 2 after expiration)
            (2, -1, 0),
            # Boundary: Quality at 1 (would go below 0, but clamped to 0)
            (1, -1, 0),
            # Normal expired case
            (25, -1, 23),
            # Quality at 0 after expiration
            (0, -1, 0),
        ],
    )
    def test_normal_item_expired_quality_decreases_by_two(
        self, initial_quality, initial_sell_in, expected_quality
    ):
        """After expiration, normal items degrade twice as fast."""
        items = [Item("Normal Item", initial_sell_in, initial_quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        assert items[0].quality == expected_quality


class TestGildedRoseAgedBrie:
    """Tests for Aged Brie (increases in quality)."""

    @pytest.mark.parametrize(
        "initial_quality,initial_sell_in,expected_quality,expected_sell_in",
        [
            # Boundary: Quality at 49 (will increase to 50, max)
            (49, 10, 50, 9),
            # Boundary: Quality at 0 (will increase to 1)
            (0, 10, 1, 9),
            # Normal case: Quality in middle range
            (25, 10, 26, 9),
            # Boundary: Quality at 50 (already at max, cannot increase)
            (50, 10, 50, 9),
            # Boundary: sell_in = 1 (before expiration, next call will trigger post-expiration)
            (25, 1, 26, 0),
            # Equivalence class: High quality, far from expiration
            (45, 20, 46, 19),
            # Equivalence class: Low quality, far from expiration
            (5, 20, 6, 19),
        ],
    )
    def test_aged_brie_increases_quality(
        self, initial_quality, initial_sell_in, expected_quality, expected_sell_in
    ):
        """Aged Brie increases in quality."""
        items = [Item("Aged Brie", initial_sell_in, initial_quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        assert items[0].quality == expected_quality
        assert items[0].sell_in == expected_sell_in

    @pytest.mark.parametrize(
        "initial_quality,initial_sell_in,expected_quality",
        [
            # Boundary: Just expired, quality at 49
            (49, -1, 50),
            # Boundary: Just expired, quality at 48 (increases to 49 then to 50 cap)
            (48, -1, 50),
            # Boundary: Quality at 50 (already max, cannot increase further)
            (50, -1, 50),
            # Normal expired case
            (25, -1, 27),
            # Boundary: Quality at 0 after expiration
            (0, -1, 2),
        ],
    )
    def test_aged_brie_expired_increases_by_two(
        self, initial_quality, initial_sell_in, expected_quality
    ):
        """After expiration, Aged Brie increases by 2 per day (capped at 50)."""
        items = [Item("Aged Brie", initial_sell_in, initial_quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        assert items[0].quality == expected_quality


class TestGildedRoseBackstagePasses:
    """Tests for Backstage passes (increases with complex rules)."""

    @pytest.mark.parametrize(
        "initial_quality,initial_sell_in,expected_quality,expected_sell_in",
        [
            # Boundary: sell_in = 11 (not in either bonus range)
            (25, 11, 26, 10),
            # Boundary: sell_in = 10 (starts "less than 11" bonus)
            (25, 10, 27, 9),
            # Equivalence: sell_in in (6, 10]
            (25, 8, 27, 7),
            (25, 6, 27, 5),
            # Boundary: sell_in = 5 (starts "less than 6" bonus)
            (25, 5, 28, 4),
            # Equivalence: sell_in in (0, 5)
            (25, 3, 28, 2),
            (25, 1, 28, 0),
            # Boundary: Quality at 48 (will increase by 3 to 51, capped at 50)
            (48, 5, 50, 4),
            # Boundary: Quality at 49 (will increase by 2 to 51, capped at 50)
            (49, 10, 50, 9),
            # Boundary: Quality at 50 (already at max)
            (50, 5, 50, 4),
            # Boundary: Quality at 0, far from expiration
            (0, 11, 1, 10),
        ],
    )
    def test_backstage_pass_before_expiration(
        self, initial_quality, initial_sell_in, expected_quality, expected_sell_in
    ):
        """Backstage passes increase in quality at different rates before expiration."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", initial_sell_in, initial_quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        assert items[0].quality == expected_quality
        assert items[0].sell_in == expected_sell_in

    @pytest.mark.parametrize(
        "initial_quality,initial_sell_in,expected_quality",
        [
            # Boundary: Just expired (sell_in becomes -1)
            (25, 0, 0),
            # Boundary: Far expired
            (25, -5, 0),
            # Quality at 0 after expiration
            (0, -1, 0),
            # Quality at 50 after expiration
            (50, -1, 0),
        ],
    )
    def test_backstage_pass_expired_becomes_zero(
        self, initial_quality, initial_sell_in, expected_quality
    ):
        """After expiration, Backstage passes drop to 0 quality."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", initial_sell_in, initial_quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        assert items[0].quality == expected_quality


class TestGildedRoseSulfuras:
    """Tests for Sulfuras (legendary item, never decreases)."""

    @pytest.mark.parametrize(
        "initial_quality,initial_sell_in",
        [
            # Legendary item should maintain quality and sell_in
            (80, 0),
            (80, 10),
            (80, -1),
            (80, 100),
            # Edge cases for Sulfuras
            (79, 5),
            (81, 5),
        ],
    )
    def test_sulfuras_never_changes(self, initial_quality, initial_sell_in):
        """Sulfuras is a legendary item and never changes."""
        items = [Item("Sulfuras, Hand of Ragnaros", initial_sell_in, initial_quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        assert items[0].quality == initial_quality
        assert items[0].sell_in == initial_sell_in


class TestGildedRoseMultipleItems:
    """Tests for multiple items in one update."""

    def test_multiple_items_update_independently(self):
        """Multiple items should update independently."""
        items = [
            Item("Normal Item", 10, 20),
            Item("Aged Brie", 10, 20),
            Item("Backstage passes to a TAFKAL80ETC concert", 10, 20),
            Item("Sulfuras, Hand of Ragnaros", 10, 80),
        ]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        assert items[0].quality == 19  # Normal item decreases
        assert items[0].sell_in == 9
        assert items[1].quality == 21  # Aged Brie increases
        assert items[1].sell_in == 9
        assert items[2].quality == 22  # Backstage pass increases by 2
        assert items[2].sell_in == 9
        assert items[3].quality == 80  # Sulfuras unchanged
        assert items[3].sell_in == 10

    def test_empty_item_list(self):
        """Empty item list should not raise an error."""
        items = []
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()  # Should not raise

        assert len(items) == 0


class TestGildedRoseEdgeCasesAndBoundaries:
    """Tests for edge cases and specific boundary conditions."""

    def test_normal_item_quality_never_negative(self):
        """Quality of normal items should never go below 0."""
        items = [Item("Normal Item", 10, 0)]
        gilded_rose = GildedRose(items)

        for _ in range(5):
            gilded_rose.update_quality()
            assert items[0].quality >= 0

    def test_aged_brie_quality_never_above_50(self):
        """Quality of Aged Brie should never exceed 50."""
        items = [Item("Aged Brie", 0, 45)]
        gilded_rose = GildedRose(items)

        for _ in range(10):
            gilded_rose.update_quality()
            assert items[0].quality <= 50

    def test_backstage_pass_quality_never_above_50(self):
        """Quality of Backstage passes should never exceed 50."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 5, 45)]
        gilded_rose = GildedRose(items)

        for _ in range(10):
            gilded_rose.update_quality()
            assert items[0].quality <= 50

    def test_backstage_pass_drops_to_zero_immediately_after_concert(self):
        """Backstage pass quality becomes 0 the day after concert."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 0, 50)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        assert items[0].quality == 0
        assert items[0].sell_in == -1

    @pytest.mark.parametrize("quality", [0, 1, 25, 49, 50])
    def test_normal_item_with_various_qualities(self, quality):
        """Normal items work correctly with all quality levels."""
        items = [Item("Normal Item", 10, quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        expected = max(0, quality - 1)
        assert items[0].quality == expected

    @pytest.mark.parametrize("quality", [0, 1, 25, 49, 50])
    def test_aged_brie_with_various_qualities(self, quality):
        """Aged Brie works correctly with all quality levels."""
        items = [Item("Aged Brie", 10, quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        expected = min(50, quality + 1)
        assert items[0].quality == expected

    def test_item_representation(self):
        """Test Item __repr__ method."""
        item = Item("Test Item", 5, 25)
        assert repr(item) == "Test Item, 5, 25"

    def test_gilded_rose_initialization(self):
        """Test GildedRose initialization."""
        items = [Item("Test", 5, 25)]
        gilded_rose = GildedRose(items)

        assert gilded_rose.items == items
        assert len(gilded_rose.items) == 1


class TestGildedRoseQualityCap:
    """Tests specifically for quality boundary conditions (0 and 50)."""

    @pytest.mark.parametrize(
        "item_name,initial_quality,initial_sell_in",
        [
            ("Aged Brie", 50, 10),
            ("Backstage passes to a TAFKAL80ETC concert", 50, 10),
        ],
    )
    def test_quality_respects_upper_limit_50(
        self, item_name, initial_quality, initial_sell_in
    ):
        """Quality should never exceed 50."""
        items = [Item(item_name, initial_sell_in, initial_quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        assert items[0].quality == 50

    @pytest.mark.parametrize(
        "item_name,initial_quality,initial_sell_in",
        [
            ("Normal Item", 0, 10),
            ("Normal Item", 0, -1),
        ],
    )
    def test_quality_respects_lower_limit_0(
        self, item_name, initial_quality, initial_sell_in
    ):
        """Quality should never be negative."""
        items = [Item(item_name, initial_sell_in, initial_quality)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        assert items[0].quality == 0


class TestGildedRoseSellInBehavior:
    """Tests specifically for sell_in behavior."""

    @pytest.mark.parametrize(
        "item_name,initial_sell_in,expected_sell_in",
        [
            ("Normal Item", 10, 9),
            ("Aged Brie", 5, 4),
            ("Backstage passes to a TAFKAL80ETC concert", 3, 2),
            ("Normal Item", 0, -1),
            ("Normal Item", -5, -6),
        ],
    )
    def test_sell_in_decreases_except_sulfuras(self, item_name, initial_sell_in, expected_sell_in):
        """sell_in should decrease by 1 each day for all items except Sulfuras."""
        items = [Item(item_name, initial_sell_in, 25)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()

        assert items[0].sell_in == expected_sell_in

    def test_sulfuras_sell_in_never_decreases(self):
        """Sulfuras sell_in should never decrease."""
        items = [Item("Sulfuras, Hand of Ragnaros", 10, 80)]
        gilded_rose = GildedRose(items)

        for _ in range(5):
            gilded_rose.update_quality()
            assert items[0].sell_in == 10


class TestGildedRoseSequentialUpdates:
    """Tests for items over multiple update cycles."""

    def test_normal_item_over_multiple_days(self):
        """Normal item should degrade consistently over multiple days."""
        items = [Item("Normal Item", 3, 10)]
        gilded_rose = GildedRose(items)

        # Day 1: quality 10 -> 9, sell_in 3 -> 2
        gilded_rose.update_quality()
        assert items[0].quality == 9
        assert items[0].sell_in == 2

        # Day 2: quality 9 -> 8, sell_in 2 -> 1
        gilded_rose.update_quality()
        assert items[0].quality == 8
        assert items[0].sell_in == 1

        # Day 3: quality 8 -> 7, sell_in 1 -> 0
        gilded_rose.update_quality()
        assert items[0].quality == 7
        assert items[0].sell_in == 0

        # Day 4: quality 7 -> 5 (double degradation), sell_in 0 -> -1
        gilded_rose.update_quality()
        assert items[0].quality == 5
        assert items[0].sell_in == -1

    def test_aged_brie_over_multiple_days(self):
        """Aged Brie should improve consistently over multiple days."""
        items = [Item("Aged Brie", 3, 10)]
        gilded_rose = GildedRose(items)

        # Day 1: quality 10 -> 11, sell_in 3 -> 2
        gilded_rose.update_quality()
        assert items[0].quality == 11
        assert items[0].sell_in == 2

        # Day 2: quality 11 -> 12, sell_in 2 -> 1
        gilded_rose.update_quality()
        assert items[0].quality == 12
        assert items[0].sell_in == 1

        # Day 3: quality 12 -> 13, sell_in 1 -> 0
        gilded_rose.update_quality()
        assert items[0].quality == 13
        assert items[0].sell_in == 0

        # Day 4: quality 13 -> 15 (double improvement), sell_in 0 -> -1
        gilded_rose.update_quality()
        assert items[0].quality == 15
        assert items[0].sell_in == -1

    def test_backstage_pass_approaching_concert(self):
        """Backstage pass should improve at increasing rates as concert approaches."""
        items = [Item("Backstage passes to a TAFKAL80ETC concert", 15, 20)]
        gilded_rose = GildedRose(items)

        # Day 1: 15 days away, +1
        gilded_rose.update_quality()
        assert items[0].quality == 21
        assert items[0].sell_in == 14

        # Fast forward to 10 days
        for _ in range(4):
            gilded_rose.update_quality()

        assert items[0].sell_in == 10
        assert items[0].quality == 25

        # Day at 10 days: +2
        gilded_rose.update_quality()
        assert items[0].quality == 27
        assert items[0].sell_in == 9

        # Fast forward to 5 days
        for _ in range(4):
            gilded_rose.update_quality()

        assert items[0].sell_in == 5
        assert items[0].quality == 35

        # Day at 5 days: +3
        gilded_rose.update_quality()
        assert items[0].quality == 38
        assert items[0].sell_in == 4


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
