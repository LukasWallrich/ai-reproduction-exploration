# Review: Reproduction Report — Iyengar & Krupenkin (2018)

**Report**: anes1/reproduction_report.qmd
**Reviewed**: 2026-02-13

## Summary

The report is well-structured, covers all five abstract claims, and demonstrates careful data handling. However, there are two critical issues that need resolution before the report can be considered reliable: (1) the deviation log omits a significance check on the key interaction terms in Table 2, meaning a potential conclusion change for Claim 5 may go undetected; and (2) Table 1 affect polarization values are discussed in the Discrepancy Investigation but missing from the deviation log.

## Critical Issues

### 1. Missing significance check in deviation log — possible unreported conclusion change for In-party Therm × Year (Model 1)

- **Location**: Deviation log code (QMD lines 1207–1215), Conclusion Claim 5 assessment (line 1296)
- **Problem**: The deviation log only checks for *direction* changes (`sign(Paper) != sign(Reproduced)`) but never checks whether *statistical significance* differs between paper and reproduced values. For Table 2 Model 1, the paper reports In-party Therm × Year = −0.0003 (SE = 0.0001, p < 0.001), while the reproduced value is −0.0001 (SE = 0.0001). With a coefficient one-third the size and similar SE, the reproduced z-ratio would be approximately −1 (vs. −3 in the paper), making this parameter likely non-significant. If confirmed, this constitutes a **conclusion change**: the paper claims the in-party thermometer's effect on voting participation has declined significantly over time, but the reproduced model may not support this at conventional significance levels. The deviation log classifies this as "Minor deviation" (near-zero rule, abs_dev = 0.0002 ≤ 0.01), masking the potential significance change.
- **Suggestion**: Add p-values to the extracted coefficients and implement a significance-change check in the deviation log (e.g., flag when paper reports p < 0.05 but reproduced p ≥ 0.05, or vice versa). If the In-party Therm × Year interaction in Model 1 is indeed non-significant, override the category to "Conclusion change" and update the Claim 5 assessment accordingly. This may also affect the overall verdict — if a key interaction is not significant, Claim 5 may only be partially supported.

### 2. Table 1 Affect polarization values missing from deviation log

- **Location**: Deviation log (QMD lines 1082–1094), Discrepancy Investigation (lines 1266)
- **Problem**: The Discrepancy Investigation discusses affect polarization deviations from Table 1 (FtF: 1.89 vs. 2.22; Online: 2.16 vs. 2.55) but these values are NOT included in the deviation log. The `claim1_table1` tibble only contains Feel Therm FtF/Online and Trait FtF/Online — it omits Affect FtF and Affect Online. These are claim-relevant parameters for Claim 1 (mode effects supporting the negativity finding). The affect deviations (15% and 15% respectively) would be classified as "Substantive deviation", which would change the Claim 1 summary in the coverage table (currently showing 0 substantive deviations).
- **Suggestion**: Add the Affect FtF and Affect Online entries to `claim1_table1`, pulling values from `affect_mode`.

## Structural Issues

### 1. Use of `cat()` for reporting

- **Location**: QMD lines 286–287 (`cat("Partisan sample size:", ...)` and `cat("Years available:", ...)`)
- **Problem**: The report uses `cat()` to display sample size and available years. The SKILL.md explicitly states: "Do NOT use `cat()` for reporting results."
- **Suggestion**: Replace with inline R expressions in narrative text or a small `kable()` table.

## Consistency Issues

### 1. Discrepancy Investigation references "−0.30" for 1980 party thermometer correlation but deviation log shows −0.2965

- **Location**: Discrepancy Investigation paragraph on correlation values (line 1268 of QMD)
- **Problem**: The report states "Our reproduced 1980 party thermometer correlation (−0.30)..." but the rendered deviation log shows the reproduced value is −0.2965. While −0.30 is a reasonable rounding, the same paragraph contrasts it with the paper's "approximate −0.22", making −0.30 sound like a precise value. The actual reproduced value rounds to −0.30 at 2dp, which is already displayed in the Figure 6 table. This is minor but could be clearer.
- **Suggestion**: Use the exact reproduced value (−0.30 is acceptable as a rounding) or add "(rounded)" for clarity.

### 2. Abstract and Conclusion use "likely" for unverified dataset version hypothesis

- **Location**: Abstract (line 75): "possibly due to dataset version differences"; Conclusion (line 1284): "likely attributable to dataset version differences"
- **Problem**: The Abstract correctly uses "possibly" but the Conclusion upgrades this to "likely attributable" without any additional evidence. Both should use the same hedging level.
- **Suggestion**: Change Conclusion to "possibly attributable to dataset version differences" to match the Abstract's hedging.

### 3. Deviation log precision for interaction terms may mask meaningful deviations

- **Location**: Deviation log — In-party Therm × Year (M1) and Out-party Therm × Year (M1)
- **Problem**: The paper reports these at 4 decimal places (−0.0003 and −0.0005). The `classify_deviation()` function auto-detects decimal places, so it should use 4 decimal places. For In-party Therm × Year: round(−0.0001, 4) = −0.0001 ≠ −0.0003, so not Exact — correctly classified as Minor deviation by the near-zero absolute rule (abs_dev = 0.0002 ≤ 0.01). However, the absolute deviation represents a 67% reduction in the coefficient, which is substantively very large even if the near-zero rule technically applies. The near-zero rule is designed for cases like 0.01 vs 0.02, not for interaction terms where the magnitude directly determines the practical effect. This is the same underlying issue as Critical Issue #1.
- **Suggestion**: Consider whether the near-zero threshold of 0.01 is appropriate for interaction terms that are reported at high precision and central to the paper's claims. At minimum, the Discrepancy Investigation should note that the interaction coefficients are roughly half to one-third the paper's values, which has substantive implications for the predicted probability plots even if significance is retained.

## Language and Hedging Issues

### 1. Discrepancy Investigation slightly overclaims on affect coding explanation

- **Location**: Discrepancy Investigation, Table 1 paragraph (line 1266): "this is likely because the CDF recodes the 2016 5-point affect scale as binary"
- **Problem**: While it is a documented fact that the CDF uses binary coding for emotion variables, the claim that this is the cause of the deviation is still an inference (the authors may have used a different scoring approach entirely). "Likely" is borderline acceptable here since the mechanism is well-understood, but "most likely" or a more direct phrasing like "this appears to be because" would be more precise.
- **Suggestion**: Minor — consider "this is most plausibly because" or leave as is.

### 2. Table 2 deviations described without explicit substantive direction

- **Location**: Discrepancy Investigation, Table 2 paragraph (line 1270)
- **Problem**: The report notes that "The Year coefficient and its interactions with thermometer scores are approximately half the paper's values" but does not explicitly state what this means for the paper's claims. The deviations are smaller coefficients, meaning weaker effects — which somewhat *weakens* the paper's central claim about participation. This substantive direction is implied by the subsequent paragraph confirming qualitative conclusions but should be stated directly.
- **Suggestion**: Add a sentence such as: "The smaller interaction coefficients imply weaker time-varying effects, i.e., the divergence between in-party and out-party thermometer effects on participation is less dramatic than the paper's estimates suggest, though the qualitative pattern remains the same."

## Minor Issues

- The Discrepancy Investigation mentions "FtF: 7.87 vs. 7.77" for trait polarization. The rendered Table 1 shows Reproduced FtF = 7.87 and Paper = 7.77. ✓ Consistent.
- Claim 3 deviation log entries duplicate Claim 1 entries (Out-party therm mean 1988 and 2016). This is acceptable since the claims overlap, but a note in the deviation log or a compound claim label ("1, 3") would reduce redundancy.
- The report reproduces Figures 9 and 10 (trait correlations) and presents them in tables, but these are not included in the deviation log for Claims 2 or 4. These figures are mentioned in the claim_result_mapping under Claims 2 and 4. While the claim mapping's parameter registry does not list specific values for Figures 9/10 (only approximate ranges), the report does compute these values and could include representative entries.
- The Figure 10 rendered table shows NA for 1980 within-candidate trait correlations (both Dem and Rep). This suggests the trait battery was not asked in 1980, yet the claim_result_mapping says the paper reports "~0.4 (1980) → ~0.8 (2016)" for Figure 10. This discrepancy between the paper's reported starting point and what the CDF contains is not discussed.
- The rendered nonvoting participation predicted effects table (Figure 13 bottom) shows that in 1980, the warm in-party effect (0.175) already exceeds the cold out-party effect (0.112), and by 2016 the pattern reverses (0.128 vs 0.314). The paper reports "1980 out-party negativity → 0.1 increase; by 2016 → 0.4 increase (fourfold)" — the reproduced 2016 value of 0.314 is notably lower than the paper's 0.4. This deviation in predicted effects is not discussed anywhere in the report.

## What's Done Well

1. **Thorough Analytical Decisions table**: The report identifies and documents multiple ambiguous choices (survey weights, nonvoting DV specification, thermometer scale), including the clever deduction that the nonvoting model uses binomial(5) logit based on the log-likelihood magnitude. This is excellent detective work.
2. **Programmatic deviation log**: The deviation log correctly pulls values from computed objects rather than hardcoding, and the coverage summary by claim is a useful addition.
3. **Comprehensive figure reproduction**: The report reproduces the key figures (1, 3, 6, 13) as visual outputs alongside the numeric comparisons, making it easy to verify qualitative trends visually.
