# Gilded Rose Test Suite - Complete Coverage Report

## Overview
A comprehensive test suite for the Gilded Rose Refactoring Kata has been created using pytest, achieving **100% line coverage** and **100% branch coverage**.

## Test Statistics
- **Total Test Cases**: 77 parametrized tests
- **Line Coverage**: 100% (36/36 statements)
- **Branch Coverage**: 100% (34/34 branches)
- **All Tests**: ✅ PASSING

## Test Organization

### 1. **TestGildedRoseNormalItems** (13 tests)
Tests for regular items (neither Aged Brie nor Backstage passes):
- Quality decreases by 1 before expiration
- Quality decreases by 2 after expiration
- Quality never goes below 0
- Boundary values: quality at 0, 1, 50
- Equivalence classes: high quality, low quality, far from expiration

### 2. **TestGildedRoseAgedBrie** (12 tests)
Tests for Aged Brie (increases in quality):
- Quality increases by 1 before expiration
- Quality increases by 2 after expiration
- Quality never exceeds 50
- Boundary values: quality at 0, 49, 50
- Post-expiration behavior verified

### 3. **TestGildedRoseBackstagePasses** (15 tests)
Tests for Backstage passes (complex quality rules):
- Increases by 1 when sell_in > 10
- Increases by 2 when 6 ≤ sell_in ≤ 10
- Increases by 3 when 1 ≤ sell_in ≤ 5
- Drops to 0 after concert (sell_in < 0)
- Quality never exceeds 50
- All boundary thresholds tested

### 4. **TestGildedRoseSulfuras** (6 tests)
Tests for Sulfuras (legendary item):
- Quality never changes
- Sell_in never decreases
- Tested with various quality and sell_in values
- Edge cases: quality 79, 80, 81

### 5. **TestGildedRoseMultipleItems** (2 tests)
Tests for multiple items in one update:
- Items update independently
- Empty item list handling

### 6. **TestGildedRoseEdgeCasesAndBoundaries** (12 tests)
Edge cases and specific boundary conditions:
- Quality never goes negative
- Quality never exceeds 50
- Backstage pass immediate zero behavior
- Item representation (__repr__)
- GildedRose initialization
- Parametrized tests with all quality levels (0, 1, 25, 49, 50)

### 7. **TestGildedRoseQualityCap** (4 tests)
Quality boundary conditions:
- Upper limit (50) for Aged Brie and Backstage passes
- Lower limit (0) for normal items

### 8. **TestGildedRoseSellInBehavior** (6 tests)
Sell_in behavior across item types:
- sell_in decreases by 1 for all items except Sulfuras
- Tested across negative and positive values
- Sulfuras sell_in stability verified

### 9. **TestGildedRoseSequentialUpdates** (3 tests)
Multi-day update cycles:
- Normal items: consistent degradation over 4 days
- Aged Brie: consistent improvement over 4 days
- Backstage passes: quality acceleration as concert approaches

## Testing Techniques Applied

### Boundary Value Testing
- Quality at minimum (0) and maximum (50)
- sell_in at critical thresholds (-1, 0, 1, 5, 6, 10, 11)
- Day before/after expiration

### Equivalence Partitioning
- **Normal items**: High quality (45+), mid range (25), low quality (5-), with varying sell_in
- **Aged Brie**: Same partitions with increasing quality logic
- **Backstage passes**: Three distinct sell_in ranges (>10, 6-10, 1-5, <0)
- **Sulfuras**: Quality variations (79, 80, 81) with all sell_in values

### Parametrized Tests
- Used `@pytest.mark.parametrize` extensively for data-driven testing
- Reduces code duplication
- Easy to add new test cases
- Clear test case documentation

## Code Coverage Details

```
Name             Stmts   Miss  Branch BrPart  Cover   Missing
--------------------------------------------------------------
gilded_rose.py      36      0     34      0   100%
--------------------------------------------------------------
TOTAL               36      0     34      0   100%
```

### All Code Paths Tested:
✅ Normal item quality logic (lines 10-12)
✅ Normal item quality = 0 check (lines 10-11)
✅ Sulfuras exclusion (lines 12, 24, 29)
✅ Aged Brie and Backstage passes quality logic (lines 14-16)
✅ Backstage passes sell_in < 11 bonus (lines 18-19)
✅ Backstage passes sell_in < 6 bonus (lines 20-21)
✅ Sell_in decrement for non-Sulfuras (line 24)
✅ Post-expiration logic for all item types (lines 26-33)
✅ Item class and repr (lines 36-42)

## Running the Tests

```bash
# Run all tests
python3 -m pytest tests/test_gilded_rose.py -v

# Run with coverage report
python3 -m pytest tests/test_gilded_rose.py --cov=gilded_rose --cov-report=term-missing

# Run with branch coverage
python3 -m pytest tests/test_gilded_rose.py --cov=gilded_rose --cov-branch --cov-report=term-missing

# Run specific test class
python3 -m pytest tests/test_gilded_rose.py::TestGildedRoseBackstagePasses -v

# Run specific test with parameters
python3 -m pytest tests/test_gilded_rose.py::TestGildedRoseNormalItems::test_normal_item_quality_decreases -v
```

## Key Insights from Testing

1. **Post-Expiration Logic**: The code applies post-expiration logic immediately when sell_in becomes negative in the same update cycle.

2. **Quality Caps**: Quality bounds are strictly enforced (0-50) across all item types.

3. **Backstage Pass Logic**: Complex tiered increases based on sell_in value, all properly capped at 50.

4. **Sulfuras Invariants**: The legendary item is immutable - neither quality nor sell_in changes under any circumstances.

5. **Aged Brie Symmetry**: Aged Brie behaves symmetrically opposite to normal items (increase vs decrease, same magnitude).

## Conclusion

This comprehensive test suite provides:
- ✅ 100% line coverage
- ✅ 100% branch coverage
- ✅ All edge cases and boundary values covered
- ✅ Clear, maintainable, parametrized tests
- ✅ Excellent documentation through test organization

The test suite ensures the Gilded Rose implementation is robust and handles all scenarios correctly.
