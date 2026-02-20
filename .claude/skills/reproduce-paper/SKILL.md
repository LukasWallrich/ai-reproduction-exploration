---
name: reproduce-paper
description: >
  Reproduce empirical claims from a published research paper using raw data.
  Use when the user wants to independently verify statistical results from
  an academic paper and produce a Quarto reproducibility report.
argument-hint: "[path-to-paper-pdf]"
---

# Skill: Reproduce Paper

## Overview
You are a computational reproducibility agent. Your task is to independently reproduce the empirical claims from a published research paper using the raw data, and produce a Quarto reproducibility report documenting your findings.

**Core principle**: The reproduction must work from the paper text and raw data alone. Authors' replication packages (code, processed data) are ONLY consulted if you cannot explain discrepancies through your own investigation. This tests whether the paper contains sufficient information for independent reproduction.

## Inputs
- **Paper**: $ARGUMENTS
- **Working directory**: current directory (will contain `claim_result_mapping.md`, `reproduction_report.qmd`, and `data/` subfolder)
- **Authors' replication materials** (optional): "Not available" — **do NOT open or read these until Stage 6**

## Workflow

### Stage 0: Data Acquisition

Before writing any code, identify what data is needed and ensure it is available.

1. Read the paper's data section to identify the **exact dataset(s)**: name, version, study number, source archive (e.g., GESIS, ICPSR, UK Data Service)
2. **Always use the exact dataset version cited by the authors.** If the paper cites "ALLBUS Cumulation 1980-2008 (ZA4572)", use ZA4572 — do NOT substitute a newer cumulation (e.g., ZA4576) even if it covers the same period, because:
   - Variable codes, value labels, and data cleaning may differ between versions
   - Cumulative files may receive corrections or recoding between releases
   - Using a different version introduces an unnecessary confound when interpreting deviations

   If the exact version is unavailable and a different version must be used, this MUST be:
   - Explicitly flagged to the user before proceeding, explaining what version is available vs. what was cited
   - Prominently documented in the **Analytical Decisions and Assumptions** section of the report
   - Noted as a possible explanation for any deviations observed

   If the paper uses multiple data files (e.g., a cumulation covering most years + an individual wave for a later year), obtain ALL of them in the exact versions cited.

3. Check whether the data files are already present in the working directory's `data/` subfolder. If the available files are a different version than what the paper cites, tell the user and ask whether to proceed with the available version or wait for the correct one.
4. If data is missing:
   - Check if the data can be downloaded programmatically (many archives require registration)
   - If it cannot be downloaded directly, **ask the user** to provide the data. Be specific:
     - Exact dataset name and study number (e.g., "ALLBUS Cumulation 1980-2008, GESIS ZA4572")
     - File format needed (`.sav`, `.dta`, `.csv`)
     - Where to place the files (e.g., `data/filename.sav`)
     - Download URL if available (e.g., `https://search.gesis.org/research_data/ZA4572`)
   - **Stop and wait** for the user to confirm the data is available before proceeding
5. If the paper uses **multiple data files** (e.g., a cumulation + individual wave, or linked datasets), identify ALL of them upfront
6. Document the data sources in `claim_result_mapping.md`, including exact version numbers and any discrepancies between cited and used versions

**IMPORTANT**: Do NOT proceed to coding (Stage 3) until all required data files are confirmed present.

### Stage 1: Extract Claims

1. Read the paper PDF
2. Extract ALL specific empirical claims from the **abstract**
3. For each claim, identify the corresponding statistical result in the paper body (table, figure, or in-text statistic)
4. Document Open Materials availability: search for replication code, data, and supplementary materials; record what is available and where
5. **Flag any analytical choices in the paper that seem unusual, non-standard, or insufficiently justified** (e.g., unusual variable transformations, unexplained sample restrictions, non-standard model specifications, questionable operationalisations). Record these in the claim mapping document and carry them forward to the report.
6. Create `claim_result_mapping.md` documenting each claim-result pair with:
   - The verbatim claim from the abstract
   - Location in paper (Table X, Figure Y, page Z)
   - Specific numerical values to reproduce
   - The statistical method used
   - Key methodological details needed for reproduction (variable names, recoding rules, model specification, etc.)
7. **Build a parameter registry**: For each claim, list the **claim-relevant parameters** (coefficients directly tested by the claim, key effect sizes, sample sizes) that will need a deviation log entry. Focus on parameters that bear on whether the claim holds — typically the main predictors, interactions, and moderators referenced in the abstract claims, plus sample sizes and model fit statistics. Control variable coefficients do not need deviation log entries unless a claim specifically depends on them. This registry is the contract — every parameter listed here must appear in the deviation log, or be explicitly marked "Not tested" with justification. The claims listed in `claim_result_mapping.md` must exactly match the numbered claims in the Paper Overview section of the report.

### Stage 2: Identify Dataset & Methods

1. Identify the exact dataset(s) used (name, version, source) — should already be documented from Stage 0
2. Document the data preparation steps (recoding, filtering, variable construction)
3. Document the statistical models and software used by the authors
4. Search the web for available replication materials (Dataverse, OSF, GitHub, journal supplements)
5. If replication materials exist, **note the location but do NOT download or read them yet**
6. Update `claim_result_mapping.md` with complete methodological details

### Stage 3: Write Reproduction Code

1. Create `reproduction_report.qmd` using the template in [reproduction_report_template.qmd](reproduction_report_template.qmd). Ensure `keep-md: true` is in the YAML header (required for reviewing rendered output).
2. Fill in the **Open Materials** section with the availability information gathered in Stage 1
3. Place the numbered **claims list in Paper Overview** (under `### Claims from the Abstract`), NOT in a separate executive summary
4. Load and prepare data following the paper's description

**Data loading pitfalls to watch for**:
- When combining multiple data files from the same survey program (e.g., cumulation + individual wave), **variable codes may differ between files**. Always verify variable codes by checking labels, not assuming the same code means the same item.
- Process each data file separately and combine at the variable level, not by row-binding with shared column names
- Use `haven::read_sav()` / `haven::read_dta()` for SPSS/Stata files; strip haven labels before merging with `zap_labels()` or manual conversion
- Check for negative values that represent missing data codes in survey data (e.g., -1 = "don't know", -9 = "not applicable")

5. **Descriptive statistics comparison**: If the paper reports descriptive statistics (means, SDs, frequencies) for the analysis sample, reproduce these and include a comparison table before the main analysis results. Discuss any notable discrepancies — they indicate sample composition differences that may explain downstream coefficient deviations.
6. **For every analytical decision where the paper is ambiguous or silent, document your choice and rationale in the 'Analytical Decisions and Assumptions' section of the report.** Do not silently make assumptions — every inferred choice must be recorded.
6. For each claim-result pair:
   - Write R code that produces the corresponding statistic
   - Store both the paper's target value and the reproduced value
   - Compute the deviation
7. Build comparison tables programmatically using `tibble()` and `kable()`
8. Build the **deviation log programmatically** — NEVER hardcode deviation tibbles with manually entered reproduced values. The deviation log must compute values from model objects or stored results. Structure the deviation log **by claim** (Claim column as first column).
9. **Deviation log completeness**: The deviation log must include entries for all **claim-relevant parameters** from all reproduced models/tables/figures — i.e., the parameters that directly bear on the abstract claims (main predictors, interactions, moderators, sample sizes, fit statistics). Control variable coefficients do not need entries unless a claim depends on them. If a table has multiple models (e.g., Table 2 Model 1 and Model 2), ALL models must be in the log. If a parameter supports multiple claims, either duplicate the entry or use a compound claim label (e.g., "1, 3"). Do not reference results in the conclusion that are not in the deviation log.
10. **Significance in the deviation log**: The deviation log should report statistical significance when available. For each fixed-effect parameter (not variance components or fit statistics):
    - **Paper significance**: Extract from the paper as reported. Look in three places, in order of priority:
      1. **Tables**: significance stars, explicit p-values, confidence intervals excluding zero/null, or stated significance thresholds. Record as-is (e.g., "p < .05", "***", "n.s.").
      2. **Prose**: If tables do not report significance (e.g., only coef and SE), check the paper's text for significance claims about specific parameters (e.g., "the time trend is significant", "the interaction was not statistically different from zero"). These textual claims are the paper's assertion and should be recorded as the paper's significance for that parameter.
      3. **Neither**: If neither tables nor prose make a significance claim for a parameter, leave the paper significance blank.

      Do NOT compute significance from the paper's rounded coefficient and SE using a normal/Wald approximation — papers may use different tests (likelihood ratio, Satterthwaite, F-test, permutation, etc.) and rounding of SEs makes such approximations unreliable. The paper's significance claims are what we reproduce, not what we can reverse-engineer from rounded numbers.
    - **Reproduced significance**: Always compute from the reproduced model using the appropriate test for that model type. For `lme4`/`lmerTest` models, use `lmerTest::lmer()` (load `library(lmerTest)` instead of `library(lme4)`) to get Satterthwaite p-values. For `glm`, use the model summary p-values. For other packages, use whatever significance test the package provides.
    - Display reproduced significance stars alongside reproduced values in the deviation log table.
    - **Conclusion changes based on significance**: Flag a significance-based conclusion change if the paper claims a parameter is significant (or non-significant) — whether in a table or in the prose — and the reproduction contradicts this. If neither tables nor prose make a significance claim for a parameter, do not flag significance-based conclusion changes for it — only flag direction reversals.
    - Include a footnote in the deviation log table explaining how reproduced significance was computed (e.g., "Satterthwaite p-values via lmerTest") and where paper significance was sourced from (table stars, prose claims, or not reported).

**Reporting style**:
- **Do NOT use `cat()` for reporting results** — it produces repetitive, disjointed output in rendered documents
- Instead, use **inline R expressions** (`` `r expr` ``) for narrative text and **`kable()` tables** for structured comparisons
- Store model results in data frames/tibbles, then display them as formatted tables
- For model summaries, extract coefficients into a tibble rather than printing raw `summary()` output
- Sample size comparisons, fit statistics, and deviation assessments should all be presented in tables, not as sequences of `cat()` calls

### Stage 4: Test & Render

1. Set `cache: true` in the YAML header during development to speed up iteration
2. Run the Quarto document: `quarto render reproduction_report.qmd`
3. Fix any errors in the code
4. Verify all code chunks execute successfully
5. **After any code changes**: delete the Quarto cache directory (`*_cache/`) before re-rendering. Stale caches are a common source of confusion where rendered output doesn't reflect code changes.

### Stage 5: Assess Deviations

Apply these **uniform relative thresholds** to classify each deviation:

| Category | Criterion | Action |
|----------|-----------|--------|
| **Exact** | Reproduced value rounds to the same reported value | None needed |
| **Minor deviation** | ≤5% relative deviation (or ≤0.01 absolute when near-zero rule applies*) | Note in deviation log |
| **Substantive deviation** | >5% relative deviation (and >0.01 absolute when near-zero rule applies*) | Investigation required |
| **Conclusion change** | Statistical significance or effect direction differs | Full investigation + alternative reproduction |

*Near-zero rule: when |paper value| < 0.2 **and the parameter is not statistically significant (or significance is unknown)**, use absolute threshold of 0.01 instead of relative, to avoid inflated percentages on noisy values near zero. When a near-zero parameter IS statistically significant in the paper, always use the 5% relative threshold — the small absolute value reflects the parameter's units, not proximity to the null. Pass `significant = TRUE` to `classify_deviation()` for such parameters.

**Precision-aware "Exact" classification**: The `classify_deviation()` helper in the template includes a rounding check based on the paper's reported decimal places. A value is "Exact" only if the reproduced value rounds to the same number at the precision the paper reports. For example, if the paper reports −0.0005 (4 decimal places), the reproduced value must round to −0.0005 at 4 decimal places to be "Exact" — the near-zero absolute threshold does NOT override this. When calling `classify_deviation()`, pass the `paper_decimals` argument for parameters reported at high precision (≥3 decimal places).

For conclusion changes (significance or direction differs), manually override the category to "Conclusion change".

**Direction reversal for ratio-scale statistics**: For odds ratios, hazard ratios, incidence rate ratios, and similar ratio-scale statistics, a direction reversal occurs when one value is >1 and the other is <1, since 1.0 is the null value — not when signs differ (both ORs are always positive). The `classify_deviation()` direction check using `sign()` only works for additive-scale statistics (coefficients, betas). Add an explicit check for ratio-scale crossings of 1.0 when building the conclusion-change override logic.

Also check:
- Do all abstract claims hold in the reproduced results?
- Are any significance conclusions different?
- Do effect directions match (using the appropriate null value: 0 for additive-scale, 1.0 for ratio-scale)?

**Model fit statistics**: For each model in the deviation log, include the primary reported fit statistic (e.g., R², Pseudo R², Nagelkerke R²) and sample size. Including every reported fit statistic is optional but encouraged for consistency across tables.

**Coverage check**: After building the deviation log, produce a coverage summary: for each claim number in the Paper Overview, count the deviation log entries and list which tables/figures are covered. Cross-reference against the parameter registry in `claim_result_mapping.md`. If any claim has zero entries, either (a) add entries for that claim's key parameters, or (b) add an entry with `Reproduced = NA` and manually set `category = "Not tested"`, with a justification note. Every claim must be accounted for.

### Stage 6: Investigate Discrepancies (if any)

If deviations exceed rounding error:

1. **First**: Try alternative R specifications (different packages, estimation methods, handling of edge cases)
2. **Check dataset version differences**: If the data source publishes updated releases (common for cumulative survey files, panel datasets, etc.), check the errata/changelog for corrections between the version the authors likely used (based on publication date) and the version you are using. When listing possible explanations, use hedged language ("one possible explanation is...", "this may be due to..."). Do NOT present hypotheses as established facts. Only state a cause confidently if you have direct evidence (e.g., you verified the dataset changelog shows specific corrections). "Dataset version differences" is a hypothesis unless you can point to specific documented changes.
3. Do not speculate about causes you cannot verify. It is better to say "the source of this deviation is unclear" than to offer an unsubstantiated explanation.
4. **Then, if needed**: Consult authors' replication materials (code, processed data)
   - Download/read the replication code
   - Compare analytical decisions: variable construction, sample restrictions, model specification
   - Document specifically what differs between your approach and theirs
5. If the original language was NOT R and an interpreter is available, attempt reproduction in that language
6. Document possible explanations (software differences, undocumented decisions, dataset version differences, data errors) — using appropriately hedged language for any that are not directly verified

**When you discover a data error or coding mistake in the original**:
- **Do NOT replicate the error** to match the published numbers
- Instead, **correct the error** in your reproduction
- Add an **impact analysis** section: run the analysis both ways (corrected and with the error) and report how results change
- Document the error clearly, including how you discovered it and how you confirmed it

### Stage 7: Report

1. Review the rendered output from Stage 4 to assess all deviations and identify possible explanations. Use the rendered `.md` file (produced by `keep-md: true` in the YAML header) rather than the `.html`, as it is much smaller and easier to read while containing the same computed values.
2. Write the report following the **exact section structure** from the template:
   - **Abstract** (callout) — verdict + summary
   - **Open Materials** — availability table + note on whether/when replication materials were consulted
   - **Paper Overview** — research question, key methods, claims from the abstract (numbered list)
   - **Data and Variable Construction**
   - **Analytical Decisions and Assumptions** — all inferred decisions documented
   - **Reproduction Results** — subsection per analysis
   - **Deviation Log** — programmatic, structured by claim, color-coded with background colors (green `#d4edda` = Exact, yellow `#fff3cd` = Minor, red `#f8d7da` = Substantive, dark red `#f5c6cb` = Conclusion change)
   - **Discrepancy Investigation** — only if deviations exceed rounding error
   - **Conclusion** — summary paragraph + claim-by-claim numbered assessment
   - **Session Info**
3. The **Abstract callout** MUST state the verdict directly (e.g., `**Verdict**: QUALITATIVELY REPRODUCED`). It MUST NOT defer to the Conclusion section. This is a hard structural requirement.
4. The **Conclusion** must contain:
   - A summary paragraph with the overall assessment
   - A **claim-by-claim numbered assessment** stating whether each claim was reproduced, with brief explanation
   - The conclusion MUST NOT claim "all claims confirmed" or "all qualitative conclusions confirmed" if any claim has zero deviation log entries or any entry marked "Not tested". Add a programmatic check: for each claim number listed in the Paper Overview, count deviation log rows. If any claim has zero rows, the verdict paragraph must explicitly note which claims were not numerically tested and exclude them from the "all confirmed" language.
5. Set `cache: false` in the YAML header and do a clean final render
6. Verify the final HTML output is complete and self-contained

7. **Final review checklist** — read the entire rendered report end-to-end and check for:
   - **Section structure matches template exactly** (no extra or missing sections, no "Executive Summary")
   - **Abstract states the verdict directly** (not "See Conclusion section below")
   - Inconsistencies between sections (e.g., abstract verdict that contradicts the deviation log or conclusion)
   - Overclaimed causality (distinguish between established explanations and hypotheses)
   - Statistical errors in prose (e.g., claiming that reference category choices affect other predictors' coefficients — they don't; or confusing significance with effect size)
   - Placeholder text that was never filled in
   - Numbers in narrative text that don't match the computed tables
   - Deviations described without noting their substantive direction: always state whether deviations strengthen or weaken the paper's claims (e.g., "more negative correlations, i.e., stronger effects that reinforce the paper's conclusion" rather than just "more negative correlations")
   - Deviation log is computed programmatically (not hardcoded) and structured by claim
   - Deviation log uses background-color styling for categories
   - **Claim coverage**: every claim in Paper Overview has ≥1 deviation log entry (or explicit "Not tested" entry)
   - **Claims consistency**: the numbered claims in Paper Overview match exactly those in `claim_result_mapping.md` — no claims added, dropped, or renumbered between documents
   - **Phantom references**: search the report text for references to figures or tables (e.g., "Figure 13", "Table 3") and verify that each referenced figure/table actually exists in the Reproduction Results section. Remove or qualify any reference to an analysis that was not performed.
   - **All inferred decisions and assumptions are documented in the Analytical Decisions section**
   - **Deviation explanations use appropriately hedged language — no unsubstantiated causal claims**
   - **Abstract hedging**: The Abstract callout must use the same hedging standards as the Discrepancy Investigation section. Avoid "most likely due to" for unverified explanations — use "possibly due to" or "which may be related to."
   - **Abstract-deviation log consistency**: For each claim described as "fully reproduced" or "reproduced" in the Abstract, verify that the deviation log contains zero conclusion changes for that claim. If any conclusion changes exist, the Abstract must acknowledge them — use "qualitatively reproduced" with caveats, not "fully reproduced."
   - **Conclusion does not overclaim**: if any claim was not tested, the conclusion must not say "all claims confirmed"

### Stage 8: Automated Review

After the final render is complete:

1. Invoke the `/review-reproduction` skill, passing the path to the reproduction report QMD file as the argument (e.g., `/review-reproduction reproduction_report.qmd`)
2. Read the generated review document (`review_reproduction_report.md`)
3. Address all **Critical** and **Structural** issues identified in the review
4. If any changes were made, re-render the report (`quarto render reproduction_report.qmd`) and re-run `/review-reproduction` to verify the fixes
5. Repeat until no Critical or Structural issues remain
6. Present the remaining **Consistency**, **Language**, and **Minor** issues to the user for their judgement on whether to address them

## Deviation Assessment Categories

| Category | Criterion | Action |
|----------|-----------|--------|
| **Exact** | Rounds to same reported value | None needed |
| **Minor deviation** | ≤5% relative deviation (or ≤0.01 absolute when |paper value| < 0.2) | Note in deviation log |
| **Substantive deviation** | >5% relative deviation (and >0.01 absolute) | Investigation required |
| **Conclusion change** | Significance/direction differs | Full investigation + alternative reproduction |

## Overall Verdict Criteria

The verdict is primarily about whether the qualitative claims hold. Computational precision is noted in parentheses.

- **COMPUTATIONALLY REPRODUCED**: All statistics match within rounding error, all claims confirmed
- **QUALITATIVELY REPRODUCED**: All claims confirmed in direction and significance; minor computational deviations
- **QUALITATIVELY REPRODUCED (substantial numeric deviations)**: All claims confirmed in direction and significance; but widespread or large computational deviations
- **PARTIALLY REPRODUCED**: Some claims confirmed, some not
- **NOT REPRODUCED**: Major claims not confirmed

## Notes
- Use R as the primary reproduction language
- Prefer `tidyverse` + domain packages (e.g., `lme4`, `lavaan`, `survey`) over base R
- Always set a random seed for reproducibility of bootstrap/simulation results
- Document any assumptions or decisions not specified in the paper
- When the paper doesn't specify details, follow standard practices and document what was assumed
- When working with survey data, always verify variable codes against labels — the same variable code can refer to different items across different files or versions of the same survey
