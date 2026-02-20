---
name: review-reproduction
description: >
  Review a completed reproduction report for completeness, internal consistency,
  and overclaiming. Flags critical issues for human review.
argument-hint: "[path-to-reproduction-report.qmd]"
---

# Skill: Review Reproduction Report

## Overview

You are a quality-control reviewer for computational reproduction reports. Your task is to read a completed reproduction report (`.qmd` file and its rendered `.html` output) and check it against the reproduction skill's requirements. You produce a structured review that flags issues by severity, so a human can quickly see what needs fixing.

**Core principle**: Be precise and evidence-based. Every issue you flag must cite specific text, section, or line from the report. Do NOT invent problems — if something looks correct, say so. When flagging discrepancies, quote the conflicting passages. The goal is to help, not to nitpick stylistic preferences.

## Inputs

- **Report QMD**: $ARGUMENTS
- The rendered output: prefer the `.md` file (same filename with `.md` extension) if it exists, as it is much smaller and easier to read. Fall back to the `.html` file only if no `.md` is available. The `.md` file is produced when the report YAML includes `keep-md: true`.
- The claim mapping file (`claim_result_mapping.md` in the same directory)
- The reproduction skill definition at `.claude/skills/reproduce-paper/SKILL.md` (for reference on requirements)
- The report template at `.claude/skills/reproduce-paper/reproduction_report_template.qmd`

## Workflow

### Step 1: Read All Inputs

1. Read the `.qmd` source file
2. Read the rendered output — prefer the `.md` file (same base name with `.md` extension) if it exists; fall back to the `.html` file otherwise. The `.md` contains the same computed output (inline R values, rendered tables) but is much smaller.
3. Read the `claim_result_mapping.md` in the same directory
4. Read the reproduction skill's `SKILL.md` and report template for the canonical requirements

### Step 2: Structural Completeness Check

Verify the report contains ALL required sections in the correct order, as defined in the template. The required sections are:

1. **YAML header** — correct format settings (`html`, `toc`, `code-fold`, `embed-resources`)
2. **Setup chunk** — includes `classify_deviation()` helper function
3. **Abstract callout** (`::: {.callout-note}`) — with Paper, Data, Verdict, and summary
4. **Open Materials** — table with 4 rows (supplementary, replication code, replication data, raw data) + note on consultation
5. **Paper Overview** — with "Research Question", "Key Methods", "Claims from the Abstract" (numbered)
6. **Data and Variable Construction**
7. **Analytical Decisions and Assumptions** — table with columns: Decision, Paper says, Our interpretation, Rationale, Alternative possible
8. **Reproduction Results** — subsections per analysis
9. **Deviation Log** — programmatic (not hardcoded), structured by claim, color-coded
10. **Discrepancy Investigation** — present only if deviations exceed rounding error
11. **Conclusion** — verdict + summary paragraph + claim-by-claim numbered assessment
12. **Session Info**

For each missing or misnamed section, flag it. Pay special attention to:
- "Executive Summary" instead of the Abstract callout (a known recurring issue)
- Missing "Analytical Decisions and Assumptions" section
- Deviation log that is hardcoded rather than computed from model objects
- Missing claim-by-claim assessment in the Conclusion

### Step 3: Internal Consistency Check

Cross-check these elements against each other for contradictions:

1. **Verdict consistency**: The verdict in the Abstract must match the verdict in the Conclusion. Both must be one of the five canonical categories:
   - COMPUTATIONALLY REPRODUCED
   - QUALITATIVELY REPRODUCED
   - QUALITATIVELY REPRODUCED (substantial numeric deviations)
   - PARTIALLY REPRODUCED
   - NOT REPRODUCED

   Check that the chosen verdict is justified by the deviation log. For example:
   - "COMPUTATIONALLY REPRODUCED" requires ALL statistics to match within rounding
   - "QUALITATIVELY REPRODUCED" requires ALL claims confirmed in direction and significance
   - "PARTIALLY REPRODUCED" requires at least one claim NOT confirmed

2. **Claims consistency**: The numbered claims in "Paper Overview" must match those in `claim_result_mapping.md` and must all appear in the claim-by-claim conclusion assessment. Check that no claim is dropped or added between sections.

3. **Numbers in narrative vs. tables**: Where the report narrative mentions specific statistics (coefficients, p-values, sample sizes), verify they match the computed tables in the rendered HTML. Flag any discrepancy with the exact values found.

4. **Deviation categories vs. thresholds**: Verify that the deviation log categories are correctly assigned per the threshold rules:
   - Exact: reproduced value rounds to the same reported value **at the precision the paper reports**. For example, if the paper reports −0.0005 (4 decimal places), the reproduced value must round to −0.0005 at 4 decimal places. The near-zero absolute threshold (0.005) does NOT override this rounding check — it is meant for values like 0.01 vs 0.02, not for high-precision values that happen to be small.
   - Minor deviation: ≤5% relative (or ≤0.01 absolute when |paper value| < 0.2 **and the parameter is not statistically significant**)
   - Substantive deviation: >5% relative (and >0.01 absolute)
   - Conclusion change: significance or direction differs
   - **Near-zero rule with significance override**: The near-zero absolute threshold (≤0.01 when |paper value| < 0.2) is designed for noisy parameters near zero, not for parameters that are small due to their units but statistically significant. When a near-zero parameter IS significant in the paper, the 5% relative threshold should apply instead — a 50% decline in a significant coefficient should be flagged as substantive regardless of absolute magnitude. Check that the report passes `significant = TRUE` to `classify_deviation()` for such parameters.
   - Pay special attention to parameters reported at ≥3 decimal places — these are most prone to misclassification by the near-zero rule.

5. **Deviation log completeness**: Check that the deviation log covers all **claim-relevant parameters** mentioned in the claim mapping — i.e., parameters that directly bear on the abstract claims (main predictors, interactions, moderators, sample sizes, fit statistics). Control variable coefficients do not need deviation log entries unless a claim specifically depends on them. Specifically:
   - For each table/model reproduced in the Reproduction Results section, verify its claim-relevant parameters appear in the deviation log. If a table has multiple models (e.g., Table 2 Model 1 and Model 2), ALL models must be in the log.
   - Check for claim-relevant parameters that appear in comparison tables in the Reproduction Results but are absent from the deviation log (a common omission).

6. **Claim coverage**: For each numbered claim in Paper Overview, count the deviation log entries with that claim number. Flag any claim with zero entries. If a claim was not numerically tested, it must either (a) have a deviation log entry with category "Not tested", or (b) be explicitly noted as untested in the claim-by-claim conclusion. A claim with zero deviation log entries that is described as "Reproduced" in the conclusion is a **Critical** issue.

7. **Open Materials note**: If the Open Materials table says replication materials exist, verify the report documents whether/when they were consulted.

8. **Replication code consultation for substantive deviations**: If the deviation log contains any "Substantive deviation" or "Conclusion change" entries AND the Open Materials table indicates that replication code is available, verify that:
   - The Discrepancy Investigation section documents that the replication code was actually read and compared against the reproduction code
   - Specific analytical differences are identified (e.g., variable construction, sample restrictions, model specification, software)
   - If the replication code was NOT consulted despite being available, flag this as a **Critical** issue: "Replication code is available but was not consulted to investigate substantive deviations. Stage 6 of the reproduction workflow requires consulting authors' replication materials when deviations cannot be explained through alternative specifications alone."

### Step 4: Overclaiming and Language Check

Review all explanatory and interpretive text for:

1. **Unhedged causal claims about discrepancies**: Explanations for deviations must use hedged language ("one possible explanation is...", "this may be due to...") unless there is direct evidence. Flag any statement that presents a hypothesis as fact. Examples of overclaiming:
   - BAD: "The deviation is caused by dataset version differences"
   - GOOD: "One possible explanation is dataset version differences"
   - EXCEPTION: Direct evidence makes a confident statement acceptable (e.g., "We verified in the dataset changelog that variable X was recoded in version 2.1")

2. **Statistical errors in prose**: Watch for common mistakes:
   - Confusing significance with effect size
   - Claiming reference category changes affect other predictors' coefficients
   - Saying "results are significant" without specifying the threshold or test
   - Misinterpreting interaction terms

3. **Missing substantive direction of deviations**: When deviations are described, the report should state whether they strengthen or weaken the paper's claims. Flag any deviation discussion that omits this.

4. **Overclaiming reproduction success**: If there are substantive deviations or conclusion changes, the report should not describe the reproduction as fully successful without qualification.

5. **Underclaiming / excessive hedging**: If all values match exactly and all claims are confirmed, the report should not add unnecessary caveats. The review should note if the report is being overly cautious.

6. **Phantom references**: Search the report text for references to figures or tables (e.g., "Figure 13", "Table 3") that appear in narrative or conclusion text. Verify that each referenced figure/table actually exists in the Reproduction Results section. Flag any reference to an analysis that was not performed — this is a **Critical** issue because it presents unverified assertions as confirmed findings.

7. **Conclusion overclaiming check**: If the conclusion says "all claims confirmed" or equivalent, verify this is actually true: every claim in the Paper Overview must have deviation log entries, and none can be marked "Not tested" or have zero entries. Flag any mismatch as **Critical**.

### Step 5: Code Quality Check (Light)

This is NOT a full code review. Only check for:

1. **`cat()` for reporting**: The report should NOT use `cat()` for presenting results in the rendered document. Results should use inline R expressions and `kable()` tables.

2. **Hardcoded values in deviation log**: The deviation log tibble must pull reproduced values from model objects or stored results, not manually typed numbers.

3. **`cache: false` for final render**: The YAML header should have `cache: false` if this is the final version. If `cache: true`, flag it as a reminder.

4. **Missing `set.seed()`**: Check that a random seed is set in the setup chunk.

### Step 6: Produce Review Output

Write the review as a markdown document in the same directory as the report, named `review_[report_name].md`. Structure it as follows:

```markdown
# Review: [Report Title]

**Report**: [path to .qmd file]
**Reviewed**: [date]

## Summary

[1-3 sentence overall assessment: Is the report ready for human review, or does it need revisions first?]

## Critical Issues

[Issues that MUST be fixed before the report can be considered reliable. These are errors that could mislead a reader about whether the reproduction succeeded.]

### [Issue title]
- **Location**: [section/line reference]
- **Problem**: [specific description with quotes from the report]
- **Suggestion**: [how to fix it]

## Structural Issues

[Missing sections, wrong section names, template deviations]

### [Issue title]
- **Location**: [section/line reference]
- **Problem**: [specific description]
- **Suggestion**: [how to fix it]

## Consistency Issues

[Contradictions between sections, numbers that don't match]

### [Issue title]
- **Location**: [section/line reference]
- **Problem**: [specific description with quotes]
- **Suggestion**: [how to fix it]

## Language and Hedging Issues

[Overclaiming, unhedged hypotheses, missing substantive direction]

### [Issue title]
- **Location**: [section/line reference]
- **Problem**: [specific description with quotes]
- **Suggestion**: [how to fix it]

## Minor Issues

[Style, formatting, non-critical improvements]

- [item]
- [item]

## What's Done Well

[Briefly note 2-3 things the report does well — this helps calibrate the review and shows it's not just looking for problems]
```

### Severity Classification

- **Critical**: Would mislead a reader about reproduction success/failure. Examples: verdict contradicts deviation log, claim dropped from assessment, hardcoded deviation values that don't match computed output, wrong deviation category for a conclusion change.
- **Structural**: Report deviates from template in ways that reduce clarity or completeness but don't introduce errors. Examples: missing section, wrong section name, missing Analytical Decisions table.
- **Consistency**: Internal contradictions that need resolution. Examples: abstract says "all claims confirmed" but conclusion says one wasn't, narrative number doesn't match table.
- **Language**: Overclaiming, unhedged hypotheses, missing context. Important but typically quick to fix.
- **Minor**: Formatting, style, non-critical suggestions.

## Important Notes

- Do NOT re-run the R code or re-render the report. Your review is based on reading the source and rendered output.
- When checking numbers, rely on the rendered output (`.md` or `.html`) for computed values (inline R results, table contents).
- If you cannot determine whether something is an issue (e.g., you can't see the computed value in the HTML), note it as "unable to verify" rather than flagging it as wrong.
- Be specific. "The deviation log may have issues" is not helpful. "The deviation log is missing Table 3 parameters for Claim 2 (donating interaction terms)" is helpful.
- The review should be actionable: someone should be able to go through it item by item and fix each issue.
- If the report has no critical or structural issues, say so clearly. A clean review is a valid outcome.
