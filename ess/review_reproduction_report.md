# Review: Reproduction Report — Huppert & So (2013)

**Report**: /Users/lukaswallrich/Documents/Coding/ai_reproduction/ess/reproduction_report.qmd
**Reviewed**: 2026-02-13

## Summary

The report is well-structured, covers all five claims with programmatic deviation log entries, and reaches a defensible verdict. However, there are several critical issues that should be fixed before the report can be considered reliable: an inconsistency between the Analytical Decisions table and the actual CFA estimator used, a factual error in the Claim 2 conclusion text (Portugal's rate), unhedged causal language in the conclusion, and extensive use of `cat()` for reporting. After addressing the critical and structural issues below, the report will be ready for human review.

## Critical Issues

### 1. CFA estimator inconsistency between Analytical Decisions table and code
- **Location**: Analytical Decisions table (line ~317 in QMD) vs CFA code (lines 676-692 in QMD)
- **Problem**: The Analytical Decisions table states "Used DWLS estimation (appropriate for ordinal indicators)" for the CFA estimation decision. However, the actual code uses `estimator = "MLR"` (robust maximum likelihood). The Discrepancy Investigation section correctly says "We used lavaan with robust ML estimation (MLR)." This is a direct contradiction.
- **Suggestion**: Update the Analytical Decisions table to say "Used MLR (robust maximum likelihood) estimation" and adjust the rationale accordingly (e.g., "MLR is robust to non-normality; items are treated as continuous after within-region standardisation"). Alternatively, if DWLS was intended, change the code to use `estimator = "DWLS"`.

### 2. Factual error in Claim 2 conclusion: Portugal prevalence
- **Location**: Claim-by-Claim Assessment, Claim 2 (line ~1118 in QMD)
- **Problem**: The conclusion states "Portugal the lowest (8.3%, paper: 9.3%)". But the deviation log and prevalence table show Portugal at 9.0%, not 8.3%. The value 8.3% does not appear anywhere in the computed output. This is a hardcoded error in narrative text.
- **Suggestion**: Replace "8.3%" with the actual reproduced value from the deviation log (9.0%).

### 3. Unhedged causal language in Conclusion
- **Location**: Conclusion summary paragraph (line ~1113 in QMD)
- **Problem**: The conclusion states "most likely due to dataset edition differences" — this is an unverified hypothesis presented with excessive confidence. The Discrepancy Investigation section appropriately uses "one possible explanation" language, but the Conclusion escalates to "most likely."
- **Suggestion**: Change "most likely due to" to "possibly due to" to match the hedging standard used elsewhere in the report.

### 4. `classify_deviation()` missing `significant` parameter
- **Location**: Setup chunk (lines 37-71 in QMD)
- **Problem**: The `classify_deviation()` function in the report does not include the `significant` parameter from the template. The template version includes this parameter to prevent the near-zero absolute threshold from misclassifying small but significant parameters. While this may not materially affect results in this report (most near-zero values are correlations that are indeed near zero), the function should match the template for consistency.
- **Suggestion**: Update `classify_deviation()` to include the `significant` parameter as specified in the template.

## Structural Issues

### 1. Extensive use of `cat()` for reporting results
- **Location**: Multiple chunks — `cor-summary` (lines 400-409), `efa2-variance` (lines 450-458), `efa3-variance` (lines 485-494), `flourishing-definition` (lines 564-566), `cfa-paper-comparison` (lines 749-752), `flourishing-vs-ls` (lines 765-766), `deviation-summary-stats` (lines 1038-1047), `conclusion-check` (lines 1086-1108), `investigate` (lines 1053-1068)
- **Problem**: The skill instructions explicitly state: "Do NOT use `cat()` for reporting results — it produces repetitive, disjointed output in rendered documents. Instead, use inline R expressions for narrative text and `kable()` tables for structured comparisons." The report uses `cat()` extensively for variance explained summaries, correlation summaries, prevalence comparisons, and coverage checks. This produces fragmented output with multiple separate code blocks in the rendered document.
- **Suggestion**: Replace `cat()` calls with `kable()` tables or inline R expressions. For example, the variance explained comparison could be a small table; the correlation summary could be a single table row; the CFA region sample sizes could be a formatted table.

### 2. Correlation comparison details not in deviation log
- **Location**: Deviation log (lines 836-848 in QMD)
- **Problem**: The correlation deviation log only includes 3 correlations selected by specific filters (max deviation, plus self-esteem/optimism and vitality/emot.stability). The claim mapping lists 45 pairwise correlations as key values. While including all 45 would be excessive, the current selection of 3 is quite sparse for a claim about factor structure. Some correlations with large deviations may be missed.
- **Suggestion**: Consider including a summary row (e.g., "Mean absolute correlation deviation" or "Number of correlations with >0.05 deviation") to better represent the correlation reproduction, or expand the selection to cover a broader range.

### 3. Self-esteem–life satisfaction correlation discrepancy not flagged
- **Location**: Analysis 6 table (rendered output lines 1836-1840)
- **Problem**: The reproduced correlation between self-esteem and life satisfaction is 0.24, while the paper reports 0.49. This is a deviation of −0.25 (over 50% relative), which is the largest single deviation in the report. However, this value does not appear in the deviation log and is not discussed in the Discrepancy Investigation. This is a notable omission since Claim 5 is about life satisfaction comparisons.
- **Suggestion**: Add the self-esteem–life satisfaction correlation to the deviation log under Claim 5. Investigate the large discrepancy — it may indicate a coding issue with the self-esteem variable or a difference in the variable used.

## Consistency Issues

### 1. Claim 2 abstract text vs deviation log: Portugal lowest
- **Location**: Abstract callout (line 31) vs deviation log
- **Problem**: The abstract states "Portugal lowest," and the deviation log shows Portugal at 9.0% (rank 21 of 22). But the country prevalence table shows Russian Federation at 7.7% is actually the lowest in the reproduction. The paper says Portugal is lowest at 9.3%, but the reproduction finds Russia lower. This ranking change is not discussed.
- **Suggestion**: Note in the Claim 2 assessment that while Portugal remains near the bottom, the reproduction finds Russia at 7.7% is actually the lowest — though both are below 10% as the paper claims.

### 2. Claim 3 narrative: "acceptable ranges" for CFI
- **Location**: Claim-by-Claim Assessment, Claim 3 (line ~1119)
- **Problem**: The conclusion says CFA fit indices are "in acceptable ranges." However, CFI of 0.90-0.91 is at the conventional threshold boundary (typically CFI ≥ 0.95 is "good", ≥ 0.90 is "acceptable") and RMSEA of 0.055-0.065 is marginal. The paper's CFI was 0.95-0.96 (good). The difference between "good" and "marginal" fit should be acknowledged more clearly.
- **Suggestion**: Acknowledge that the reproduced CFI values (0.90-0.91) are at the lower boundary of conventional acceptability, substantially below the paper's values (0.95-0.96), and note this as a substantive difference.

### 3. r(Engagement, Emot. stability) paper value discrepancy
- **Location**: Deviation log first row vs Table 2 paper values
- **Problem**: The deviation log shows `r(Engagement, Emot. stability)` with paper value 0.31, reproduced 0.42. But looking at Table 2 in the paper, the correlation between Engagement (row 3) and Emot. stability (column 2) should be 0.10, not 0.31. The value 0.31 appears to be the Competence-Meaning correlation (row 4, col 1). This suggests a possible indexing error in the paper values matrix, where `paper_cor[3,1]` was set to .37 (Engagement-Competence), but the deviation log filter picked up the wrong pair. Verify the paper correlation matrix entries.
- **Suggestion**: Double-check that `paper_cor[3,2] <- .10` is the correct assignment for r(Engagement, Emot. stability). The rendered correlation matrix shows the reproduced value for this pair as 0.14, not 0.42. The deviation log entry showing 0.42 may actually be r(Meaning, Competence) mislabelled. This needs careful verification.

## Language and Hedging Issues

### 1. Discrepancy Investigation: "likely stem from"
- **Location**: Discrepancy Investigation opening sentence (line ~1070)
- **Problem**: "The numeric deviations are consistent across analyses and likely stem from a small number of systematic sources" — "likely stem from" is somewhat confident for unverified hypotheses. The individual explanations use better hedging ("one possible explanation," "may reflect"), but the opening framing overpromises.
- **Suggestion**: Change to "The numeric deviations are consistent across analyses and may stem from..."

### 2. Missing substantive direction for CFA deviations
- **Location**: Discrepancy Investigation, point 4 (line ~1078)
- **Problem**: The CFA deviations are described factually but without noting their substantive direction. CFI of 0.91 vs 0.96 means the reproduced model fits notably worse. RMSEA of 0.065 vs 0.027 is much worse. While measurement invariance is still supported qualitatively (CFI doesn't drop much between models), the absolute fit is substantially poorer, which could weaken the claim.
- **Suggestion**: Add a sentence noting that the reproduced CFA fit is notably poorer than reported, but the pattern of minimal CFI decline across invariance levels is preserved, supporting the measurement invariance claim qualitatively.

### 3. Claim 4 assessment vagueness
- **Location**: Claim-by-Claim Assessment, Claim 4 (line ~1120)
- **Problem**: Claim 4 is about "striking differences in country profiles across the 10 features" (i.e., Table 6 showing feature-by-feature prevalence across countries). The report assesses this through overall flourishing prevalence ranks, but the claim is specifically about profiles — whether countries rank differently on different features. The report does not reproduce Table 6 (feature-specific weighted prevalence by country), which is the key evidence for this claim.
- **Suggestion**: Acknowledge that the feature-specific profiles (Table 6) were not reproduced and that Claim 4 is only partially assessed through the overall prevalence ranking.

## Minor Issues

- **`cache: false`** is correctly set in the YAML header — good.
- **`set.seed(12345)`** is present in the setup chunk — good.
- The rendered MD includes raw variable names in table row labels (e.g., `accdng_r_z` alongside "Competence" in EFA tables). Consider removing the raw variable name column for cleaner presentation.
- The 3-factor EFA table column headers say "Factor 1", "Factor 2", "Factor 3" but the underlying columns are TC1/TC2/TC3 from `principal()`. The display names are correct, but note that the factor ordering may differ from the paper's (the paper's F3 is the satisfaction/emotion factor).
- The deviation log entry for "r(Self-esteem, Optimism)" shows Paper = 0.22 but this is actually from the deviation log's filter selecting `paper_cor[9,5] = .49` for Self-esteem–Optimism. The rendered table shows 0.22/0.24 which doesn't match the paper's .49. This needs verification as it may be another indexing issue (see Consistency Issue #3).
- Several `print()` calls for tibbles in the rendered output produce raw console-style output rather than formatted tables.

## What's Done Well

1. **Programmatic deviation log**: The deviation log is built entirely from model objects and computed values, not hardcoded. This is a significant strength and follows the template requirements well.

2. **Comprehensive claim coverage**: All 5 claims have deviation log entries (Claim 1: 16, Claim 2: 7, Claim 3: 16, Claim 4: 3, Claim 5: 5 entries), and the coverage check is included programmatically.

3. **Good investigative work on PCA vs FA**: The discovery that PCA (not common factor analysis) reproduces the reported variance explained, and the documentation of this decision in the Analytical Decisions table, is a valuable finding.
