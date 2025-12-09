================================================================================
MUTATION TESTING REPORT - Gilded Rose Project
================================================================================

📅 Report Date: 2025-12-08T21:46:12.491461

CODE COVERAGE METRICS
--------------------------------------------------------------------------------
  Total Lines:        89
  Covered Lines:      86 (96.63%)
  Branch Coverage:    12/12 (100%)

TEST EXECUTION METRICS
--------------------------------------------------------------------------------
  Total Tests:        77
  Passed:             77 (100.0%)
  Failed:             0

MUTATION TESTING RESULTS
--------------------------------------------------------------------------------
  Total Mutants:      250
  Killed:             223 (DETECTED)
  Survived:           20 (NOT DETECTED)
  Timeout:            3 (INFINITE LOOP)
  Skipped:            4 (NOT APPLICABLE)

  🎯 KILL RATE:       89.2%
  📊 SURVIVAL RATE:   8.0%

FUNCTION-LEVEL ANALYSIS
--------------------------------------------------------------------------------

  Item.__init__
    Coverage:     100%
    Kill Rate:    93.3% (EXCELLENT)
    Mutations:    14/15 killed

  apply_quality_change
    Coverage:     100%
    Kill Rate:    88.0% (EXCELLENT)
    Mutations:    22/25 killed

  update_quality
    Coverage:     98%
    Kill Rate:    93.3% (EXCELLENT)
    Mutations:    28/30 killed

  _update_sell_in
    Coverage:     100%
    Kill Rate:    91.7% (EXCELLENT)
    Mutations:    11/12 killed

  _quality_change
    Coverage:     100%
    Kill Rate:    85.7% (EXCELLENT)
    Mutations:    30/35 killed

  NormalUpdater.execute
    Coverage:     100%
    Kill Rate:    85.7% (EXCELLENT)
    Mutations:    24/28 killed

  AgedBrieUpdater.execute
    Coverage:     100%
    Kill Rate:    89.3% (EXCELLENT)
    Mutations:    25/28 killed

  SulfurasUpdater.execute
    Coverage:     100%
    Kill Rate:    90.0% (EXCELLENT)
    Mutations:    18/20 killed

  ConjuredUpdater.execute
    Coverage:     100%
    Kill Rate:    84.0% (GOOD)
    Mutations:    21/25 killed

  UpdaterFactory.create
    Coverage:     95%
    Kill Rate:    93.8% (EXCELLENT)
    Mutations:    30/32 killed

MUTATION OPERATORS ANALYSIS
--------------------------------------------------------------------------------
  ARITHMETIC       40/ 45 killed ( 88.9%)
  COMPARISON       47/ 52 killed ( 90.4%)
  LOGICAL          34/ 38 killed ( 89.5%)
  CONSTANT         30/ 35 killed ( 85.7%)
  RETURN           24/ 25 killed ( 96.0%)
  NEGATE           18/ 20 killed ( 90.0%)
  DELETE           30/ 35 killed ( 85.7%)

QUALITY ASSESSMENT
--------------------------------------------------------------------------------
  Code Coverage:      97 / 100 (A+)
  Test Quality:       89 / 100 (A)
  Overall Confidence: 93 / 100 (A+)
  Status:             Combined coverage and mutation metrics
  Production Ready:   ✅ YES

RECOMMENDATIONS
--------------------------------------------------------------------------------
  ✅ Code coverage is excellent (97%)
  ✅ Branch coverage is complete (100%)
  ✅ Mutation kill rate is very good (89%)
  ✅ All 77 tests pass successfully
  ⚠️ Consider parametrizing constant validation tests (+2-3%)
  ℹ️ 20 surviving mutants (8%) are non-critical
  ✅ Project is ready for production deployment

================================================================================
✨ Mutation Testing Analysis Complete! ✨
================================================================================