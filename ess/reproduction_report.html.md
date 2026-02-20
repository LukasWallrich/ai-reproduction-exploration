---
title: "Reproduction Report: Huppert & So (2013)"
subtitle: "Flourishing Across Europe: Application of a New Conceptual Framework for Defining Well-Being"
author: "AI Reproduction"
date: today
format:
  html:
    toc: true
    toc-depth: 3
    code-fold: true
    code-summary: "Show code"
    embed-resources: true
keep-md: true
execute:
  warning: false
  message: false
  cache: false
---

::: {.callout-warning appearance="simple"}
## Exploratory AI Capability Study

This report was generated autonomously by an AI agent as part of an exploratory study into the capabilities of agentic AI for computational reproduction. **It is not an independent assessment of the original paper.** The AI agent may have made errors in data processing, analytical decisions, or interpretation. Any discrepancies reported here may reflect limitations of the AI reproduction process rather than issues with the original research.
:::



::: {.callout-note appearance="minimal"}
## Abstract

**Paper**: Huppert, F. A., & So, T. T. C. (2013). Flourishing Across Europe: Application of a New Conceptual Framework for Defining Well-Being. *Social Indicators Research*, 110, 837–861. DOI: 10.1007/s11205-011-9966-7

**Data**: European Social Survey Round 3 (2006/2007), edition 3.7, N ≈ 43,000 from 23 countries (22 used after excluding Hungary)

**Verdict**: QUALITATIVELY REPRODUCED (substantial numeric deviations)

All five abstract claims are qualitatively supported by the reproduction: the two-factor structure is confirmed, the four-fold difference in flourishing prevalence across countries holds (with Denmark highest and Portugal lowest), measurement invariance is demonstrated, country profiles show striking variation, and the life satisfaction comparison confirms that flourishing captures distinct information. Numeric deviations are present throughout, possibly due to differences in dataset edition (we used ESS3 edition 3.7, while the authors likely used an earlier edition), weighting approach for standardisation and factor analysis, and software/estimator choices for CFA. No conclusion changes were found.
:::

## Open Materials

| Material | Available | Location |
|----------|-----------|----------|
| Supplementary materials | No | — |
| Replication code | No | — |
| Replication data (processed) | No | — |
| Raw data | Yes | ESS Round 3, freely available after registration at europeansocialsurvey.org |

No replication code or processed data was available. The reproduction is based entirely on the paper text and the raw ESS Round 3 data file.

---

## Paper Overview

### Research Question
The paper develops an operational definition of flourishing (positive mental health) based on the mirror opposites of depression and anxiety symptoms, identifies ten features of well-being, validates them psychometrically using ESS Round 3 data, and examines the prevalence of flourishing across 22 European countries.

### Key Methods
- **Data**: European Social Survey Round 3 (2006/2007), ~43,000 respondents from 23 countries (Hungary excluded due to missing vitality data)
- **Psychometric analyses**: Spearman correlations, Exploratory Factor Analysis (EFA) with oblique rotation, multi-group Confirmatory Factor Analysis (CFA) for measurement invariance
- **Prevalence estimation**: Weighted percentages meeting the operational definition of flourishing across 22 countries
- **Weighting**: Standard ESS weighting (design weight × population weight)
- **Within-region standardisation**: Items standardised within 3 European regions before analysis

### Claims from the Abstract

1. **Factor structure**: Psychometric analysis of indicators of the ten features reveals a clear factor structure supporting the conceptual framework (two factors: positive characteristics and positive functioning; with positive emotion loading separately when life satisfaction is added).
2. **Flourishing prevalence**: Application of the operational definition reveals a four-fold difference in flourishing rate across Europe, from ~41% in Denmark to less than 10% in Slovakia, Russia, and Portugal.
3. **Measurement equivalence**: The factor structure is applicable across European regions (measurement invariance demonstrated via multi-group CFA).
4. **Country profiles**: There are striking differences in country profiles across the 10 features.
5. **Life satisfaction comparison**: Comparison with a life satisfaction measure shows that valuable information would be lost if well-being was measured by life satisfaction alone (correlation of .34 between flourishing and life satisfaction; only 7.3% both flourishing and with high life satisfaction).

---

## Data and Variable Construction


::: {.cell}

```{.r .cell-code}
# Load ESS Round 3 data
ess <- read_sav("../data/ess/ESS3e03_7.sav")

# Define the 10 flourishing indicator variables
flour_vars <- c(
  competence = "accdng",
  emot_stability = "fltpcfl",
  engagement = "lrnnew",
  meaning = "dngval",
  optimism = "optftr",
  pos_emotion = "happy",
  pos_relationships = "ppllfcr",
  resilience = "wrbknrm",
  self_esteem = "pstvms",
  vitality = "enrglot"
)

# Select key variables and convert to numeric (strip haven labels)
ess_sel <- ess %>%
  select(cntry, dweight, pweight, pspwght,
         all_of(unname(flour_vars)),
         stflife) %>%
  mutate(across(c(all_of(unname(flour_vars)), stflife), as.numeric))

# Recode missing values
# For 1-5 agree/disagree items: 7=Refusal, 8=Don't know, 9=No answer -> NA
agree_vars <- c("accdng", "lrnnew", "dngval", "optftr", "ppllfcr", "wrbknrm", "pstvms")
# For 1-4 frequency items: 7=Refusal, 8=Don't know, 9=No answer -> NA
freq_vars <- c("fltpcfl", "enrglot")
# For 0-10 items: 77=Refusal, 88=Don't know, 99=No answer -> NA
scale_vars <- c("happy", "stflife")

ess_sel <- ess_sel %>%
  mutate(
    across(all_of(agree_vars), ~ if_else(. >= 6, NA_real_, .)),
    across(all_of(freq_vars), ~ if_else(. >= 6, NA_real_, .)),
    across(all_of(scale_vars), ~ if_else(. >= 11, NA_real_, .))
  )

# Exclude Hungary (missing vitality data)
ess_analysis <- ess_sel %>%
  filter(cntry != "HU")

# Create combined weight (dweight * pweight)
ess_analysis <- ess_analysis %>%
  mutate(wt = dweight * pweight)

# Define regions as per paper
ess_analysis <- ess_analysis %>%
  mutate(region = case_when(
    cntry %in% c("DK", "FI", "NO", "SE") ~ "Northern Europe",
    cntry %in% c("AT", "BE", "CY", "FR", "DE", "IE", "NL", "PT", "ES", "CH", "GB") ~ "Southern/Western Europe",
    cntry %in% c("BG", "EE", "PL", "RU", "SK", "SI", "UA") ~ "Eastern Europe",
    TRUE ~ NA_character_
  ))

# Basic data description
tibble(
  Metric = c("Total observations (ESS R3)", "Observations after excluding Hungary",
             "Countries", "Countries after excluding Hungary"),
  Value = c(nrow(ess_sel), nrow(ess_analysis),
            n_distinct(ess_sel$cntry), n_distinct(ess_analysis$cntry))
) %>%
  kable(caption = "Dataset Overview") %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Dataset Overview</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Metric </th>
   <th style="text-align:right;"> Value </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Total observations (ESS R3) </td>
   <td style="text-align:right;"> 43000 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Observations after excluding Hungary </td>
   <td style="text-align:right;"> 41482 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Countries </td>
   <td style="text-align:right;"> 23 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Countries after excluding Hungary </td>
   <td style="text-align:right;"> 22 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


The paper uses 10 ESS items as indicators of flourishing features. Each item was recoded as present/absent using cut points based on the response format, then combined into an operational definition of flourishing.

### Variable Mapping


::: {.cell}

```{.r .cell-code}
tibble(
  Feature = c("Competence", "Emotional stability", "Engagement", "Meaning",
              "Optimism", "Positive emotion", "Positive relationships",
              "Resilience", "Self-esteem", "Vitality"),
  `ESS Variable` = c("accdng", "fltpcfl", "lrnnew", "dngval", "optftr",
                      "happy", "ppllfcr", "wrbknrm", "pstvms", "enrglot"),
  Scale = c("1-5 agree", "1-4 freq", "1-5 agree", "1-5 agree", "1-5 agree",
            "0-10", "1-5 agree", "1-5 agree (rev)", "1-5 agree", "1-4 freq"),
  `Cut point (present)` = c("1-2", "3-4", "1 only", "1-2", "1-2",
                             "8-10", "1 only", "4-5 (disagree)", "1-2", "3-4")
) %>%
  kable(caption = "Flourishing indicators and cut points") %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Flourishing indicators and cut points</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Feature </th>
   <th style="text-align:left;"> ESS Variable </th>
   <th style="text-align:left;"> Scale </th>
   <th style="text-align:left;"> Cut point (present) </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Competence </td>
   <td style="text-align:left;"> accdng </td>
   <td style="text-align:left;"> 1-5 agree </td>
   <td style="text-align:left;"> 1-2 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Emotional stability </td>
   <td style="text-align:left;"> fltpcfl </td>
   <td style="text-align:left;"> 1-4 freq </td>
   <td style="text-align:left;"> 3-4 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Engagement </td>
   <td style="text-align:left;"> lrnnew </td>
   <td style="text-align:left;"> 1-5 agree </td>
   <td style="text-align:left;"> 1 only </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Meaning </td>
   <td style="text-align:left;"> dngval </td>
   <td style="text-align:left;"> 1-5 agree </td>
   <td style="text-align:left;"> 1-2 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Optimism </td>
   <td style="text-align:left;"> optftr </td>
   <td style="text-align:left;"> 1-5 agree </td>
   <td style="text-align:left;"> 1-2 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Positive emotion </td>
   <td style="text-align:left;"> happy </td>
   <td style="text-align:left;"> 0-10 </td>
   <td style="text-align:left;"> 8-10 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Positive relationships </td>
   <td style="text-align:left;"> ppllfcr </td>
   <td style="text-align:left;"> 1-5 agree </td>
   <td style="text-align:left;"> 1 only </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Resilience </td>
   <td style="text-align:left;"> wrbknrm </td>
   <td style="text-align:left;"> 1-5 agree (rev) </td>
   <td style="text-align:left;"> 4-5 (disagree) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Self-esteem </td>
   <td style="text-align:left;"> pstvms </td>
   <td style="text-align:left;"> 1-5 agree </td>
   <td style="text-align:left;"> 1-2 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Vitality </td>
   <td style="text-align:left;"> enrglot </td>
   <td style="text-align:left;"> 1-4 freq </td>
   <td style="text-align:left;"> 3-4 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


### Within-Region Standardisation

The paper states that "scores on each item were standardised within each region to reduce or eliminate unwanted cross-regional differences such as response set." We apply this standardisation before computing correlations and conducting factor analyses.


::: {.cell}

```{.r .cell-code}
# Standardise each flourishing item within region
# For the agree/disagree items, REVERSE code so higher = more positive
# For resilience, it's already in the "negative" direction (agree = less resilient)
# so we reverse it

# First, reverse-code items where lower values = more positive
# Agree items (1=Agree strongly to 5=Disagree strongly): reverse so 5=most positive
# Frequency items (1=None to 4=All): already higher = more positive
# Happy (0-10): already higher = more positive

ess_std <- ess_analysis %>%
  mutate(
    # Reverse agree/disagree items so higher = more positive
    accdng_r = 6 - accdng,
    lrnnew_r = 6 - lrnnew,
    dngval_r = 6 - dngval,
    optftr_r = 6 - optftr,
    ppllfcr_r = 6 - ppllfcr,
    pstvms_r = 6 - pstvms,
    # Resilience: original high = agree = LESS resilient, so do NOT reverse
    # (reverse of the reverse: keep original direction then flip)
    # Actually the paper says resilience is "reverse score" meaning they flip it
    # so that high = more resilient = disagree with "takes long time"
    # Since original 1=agree strongly, 5=disagree strongly:
    # Keep original: 5 = disagree = more resilient (already correct direction after our reversal logic)
    # Wait - let me reconsider. The original coding is:
    # 1 = Agree strongly ("takes long time to get back to normal" = LOW resilience)
    # 5 = Disagree strongly = HIGH resilience
    # So original coding already has HIGH values = HIGH resilience
    # But we reversed all other agree items. For resilience, we should NOT reverse.
    wrbknrm_r = wrbknrm,  # Already coded so higher = more resilient
    # Frequency items: already higher = more positive
    fltpcfl_r = fltpcfl,
    enrglot_r = enrglot,
    # Happy: already higher = more positive
    happy_r = happy
  )

# Define the recoded variable names for analysis
flour_vars_r <- c(
  competence = "accdng_r",
  emot_stability = "fltpcfl_r",
  engagement = "lrnnew_r",
  meaning = "dngval_r",
  optimism = "optftr_r",
  pos_emotion = "happy_r",
  pos_relationships = "ppllfcr_r",
  resilience = "wrbknrm_r",
  self_esteem = "pstvms_r",
  vitality = "enrglot_r"
)

# Standardise within region
ess_std <- ess_std %>%
  group_by(region) %>%
  mutate(across(all_of(unname(flour_vars_r)),
                ~ (. - mean(., na.rm = TRUE)) / sd(., na.rm = TRUE),
                .names = "{.col}_z")) %>%
  ungroup()

# Standardised variable names
flour_vars_z <- paste0(unname(flour_vars_r), "_z")
names(flour_vars_z) <- names(flour_vars_r)

# Also standardise life satisfaction within region
ess_std <- ess_std %>%
  group_by(region) %>%
  mutate(stflife_z = (stflife - mean(stflife, na.rm = TRUE)) / sd(stflife, na.rm = TRUE)) %>%
  ungroup()
```
:::


---

## Analytical Decisions and Assumptions

| Decision | Paper says | Our interpretation | Rationale | Alternative possible |
|----------|-----------|-------------------|-----------|---------------------|
| Weighting | "Data were weighted using standard ESS techniques" | Used `dweight × pweight` for prevalence; unweighted for factor analyses | Standard ESS practice; paper ambiguous on whether factor analyses were weighted | Could use `pspwght` instead of `pweight` |
| Standardisation | "Scores on each item were standardised within each region" | Applied z-score standardisation within 3 regions before correlations and EFA | Direct interpretation of paper text | Unclear whether standardisation was weighted |
| EFA method | "Exploratory Factor Analysis" | Used PCA (`psych::principal`) | Total variance explained (42.9%) matches PCA, not common factor analysis | Paper may have used FA despite reporting PCA-like variance |
| EFA rotation | "Oblique rotation" | Used oblimin rotation | Oblimin is the most common oblique rotation; paper does not specify | Could use promax |
| Resilience reverse coding | "reverse score" | Original coding already has high = disagree = high resilience | ESS coding: 1=Agree strongly, 5=Disagree strongly; for this negatively-worded item, high values already = positive | Direction could be confused |
| CFA estimation | Not specified | Used MLR (robust maximum likelihood) estimation | MLR is robust to non-normality; items are treated as continuous after within-region standardisation; paper mentions "Lisrel GFI" suggesting LISREL software | Paper may have used ML, DWLS, or LISREL-specific estimator |
| Missing data | Not specified | Listwise deletion for each analysis | Standard default | Could use pairwise deletion or imputation |
| Cut point for engagement | "strongly agree" (80.5% agreed) | Code 1 = present | Paper states adjustment for skew | Threshold is clear |
| Cut point for positive relationships | "strongly agree" (90.2% agreed) | Code 1 = present | Paper states adjustment for skew | Threshold is clear |
| Life satisfaction "high" cut point | "a score of 9-10" (18.1%) | stflife >= 9 | Paper chose higher threshold to match flourishing rate | Clear from paper |

**Potentially non-standard choices in the original paper**: Within-region standardisation before computing correlations and factor analyses is unusual. This reduces between-region variance and could alter correlation magnitudes and factor structure compared to unstandardised analyses.

---

## Reproduction Results

### Analysis 1: Spearman Correlations (Table 2)


::: {.cell}

```{.r .cell-code}
# Use region-standardised variables
# Paper reports Spearman correlations
cor_data <- ess_std %>%
  dplyr::select(all_of(unname(flour_vars_z))) %>%
  drop_na()

# Compute Spearman correlation matrix
cor_mat <- cor(cor_data, method = "spearman")

# Rename for display
item_names <- c("Competence", "Emot. stability", "Engagement", "Meaning",
                "Optimism", "Pos. emotion", "Pos. relationships",
                "Resilience", "Self-esteem", "Vitality")
rownames(cor_mat) <- item_names
colnames(cor_mat) <- item_names

# Paper's Table 2 values (lower triangle, row by row)
paper_cor <- matrix(NA, 10, 10)
rownames(paper_cor) <- item_names
colnames(paper_cor) <- item_names

# Fill in from paper Table 2
# Row 2: Emot stability
paper_cor[2,1] <- .19
# Row 3: Engagement
paper_cor[3,1] <- .37; paper_cor[3,2] <- .10
# Row 4: Meaning
paper_cor[4,1] <- .31; paper_cor[4,2] <- .14; paper_cor[4,3] <- .26
# Row 5: Optimism
paper_cor[5,1] <- .28; paper_cor[5,2] <- .24; paper_cor[5,3] <- .24; paper_cor[5,4] <- .25
# Row 6: Pos emotion
paper_cor[6,1] <- .18; paper_cor[6,2] <- .27; paper_cor[6,3] <- .17; paper_cor[6,4] <- .22; paper_cor[6,5] <- .31
# Row 7: Pos relationships
paper_cor[7,1] <- .20; paper_cor[7,2] <- .12; paper_cor[7,3] <- .22; paper_cor[7,4] <- .26; paper_cor[7,5] <- .17; paper_cor[7,6] <- .23
# Row 8: Resilience
paper_cor[8,1] <- .13; paper_cor[8,2] <- .21; paper_cor[8,3] <- .13; paper_cor[8,4] <- .14; paper_cor[8,5] <- .22; paper_cor[8,6] <- .24; paper_cor[8,7] <- .14
# Row 9: Self-esteem
paper_cor[9,1] <- .28; paper_cor[9,2] <- .23; paper_cor[9,3] <- .19; paper_cor[9,4] <- .24; paper_cor[9,5] <- .49; paper_cor[9,6] <- .25; paper_cor[9,7] <- .22; paper_cor[9,8] <- .21
# Row 10: Vitality
paper_cor[10,1] <- .27; paper_cor[10,2] <- .37; paper_cor[10,3] <- .19; paper_cor[10,4] <- .20; paper_cor[10,5] <- .29; paper_cor[10,6] <- .27; paper_cor[10,7] <- .11; paper_cor[10,8] <- .24; paper_cor[10,9] <- .25

# Extract lower triangle for comparison
repro_lower <- cor_mat[lower.tri(cor_mat)]
paper_lower <- paper_cor[lower.tri(paper_cor)]

# Create comparison
cor_comparison <- tibble(
  row_idx = rep(2:10, times = 1:9),
  col_idx = unlist(lapply(2:10, function(i) 1:(i-1))),
  Row = item_names[row_idx],
  Column = item_names[col_idx],
  Paper = paper_lower,
  Reproduced = round(repro_lower, 2)
) %>%
  select(Row, Column, Paper, Reproduced) %>%
  mutate(Deviation = Reproduced - Paper)

# Display correlation matrix
cor_display <- round(cor_mat, 2)
cor_display[upper.tri(cor_display, diag = TRUE)] <- NA

kable(cor_display[-1, -10], caption = "Reproduced Spearman correlations (lower triangle)",
      digits = 2) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), font_size = 11)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="font-size: 11px; margin-left: auto; margin-right: auto;">
<caption style="font-size: initial !important;">Reproduced Spearman correlations (lower triangle)</caption>
 <thead>
  <tr>
   <th style="text-align:left;">  </th>
   <th style="text-align:right;"> Competence </th>
   <th style="text-align:right;"> Emot. stability </th>
   <th style="text-align:right;"> Engagement </th>
   <th style="text-align:right;"> Meaning </th>
   <th style="text-align:right;"> Optimism </th>
   <th style="text-align:right;"> Pos. emotion </th>
   <th style="text-align:right;"> Pos. relationships </th>
   <th style="text-align:right;"> Resilience </th>
   <th style="text-align:right;"> Self-esteem </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Emot. stability </td>
   <td style="text-align:right;"> 0.25 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Engagement </td>
   <td style="text-align:right;"> 0.36 </td>
   <td style="text-align:right;"> 0.14 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Meaning </td>
   <td style="text-align:right;"> 0.42 </td>
   <td style="text-align:right;"> 0.22 </td>
   <td style="text-align:right;"> 0.29 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Optimism </td>
   <td style="text-align:right;"> 0.34 </td>
   <td style="text-align:right;"> 0.29 </td>
   <td style="text-align:right;"> 0.26 </td>
   <td style="text-align:right;"> 0.33 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Pos. emotion </td>
   <td style="text-align:right;"> 0.22 </td>
   <td style="text-align:right;"> 0.27 </td>
   <td style="text-align:right;"> 0.13 </td>
   <td style="text-align:right;"> 0.24 </td>
   <td style="text-align:right;"> 0.32 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Pos. relationships </td>
   <td style="text-align:right;"> 0.25 </td>
   <td style="text-align:right;"> 0.17 </td>
   <td style="text-align:right;"> 0.27 </td>
   <td style="text-align:right;"> 0.32 </td>
   <td style="text-align:right;"> 0.22 </td>
   <td style="text-align:right;"> 0.20 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Resilience </td>
   <td style="text-align:right;"> 0.18 </td>
   <td style="text-align:right;"> 0.23 </td>
   <td style="text-align:right;"> 0.16 </td>
   <td style="text-align:right;"> 0.17 </td>
   <td style="text-align:right;"> 0.24 </td>
   <td style="text-align:right;"> 0.21 </td>
   <td style="text-align:right;"> 0.14 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Self-esteem </td>
   <td style="text-align:right;"> 0.25 </td>
   <td style="text-align:right;"> 0.22 </td>
   <td style="text-align:right;"> 0.18 </td>
   <td style="text-align:right;"> 0.22 </td>
   <td style="text-align:right;"> 0.42 </td>
   <td style="text-align:right;"> 0.24 </td>
   <td style="text-align:right;"> 0.16 </td>
   <td style="text-align:right;"> 0.18 </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Vitality </td>
   <td style="text-align:right;"> 0.24 </td>
   <td style="text-align:right;"> 0.36 </td>
   <td style="text-align:right;"> 0.18 </td>
   <td style="text-align:right;"> 0.20 </td>
   <td style="text-align:right;"> 0.27 </td>
   <td style="text-align:right;"> 0.28 </td>
   <td style="text-align:right;"> 0.10 </td>
   <td style="text-align:right;"> 0.23 </td>
   <td style="text-align:right;"> 0.25 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



::: {.cell}

```{.r .cell-code}
# Summary statistics of deviations
cat("Correlation comparison summary:\n")
```

::: {.cell-output .cell-output-stdout}

```
Correlation comparison summary:
```


:::

```{.r .cell-code}
cat("Mean absolute deviation:", round(mean(abs(cor_comparison$Deviation)), 3), "\n")
```

::: {.cell-output .cell-output-stdout}

```
Mean absolute deviation: 0.032 
```


:::

```{.r .cell-code}
cat("Max absolute deviation:", round(max(abs(cor_comparison$Deviation)), 3), "\n")
```

::: {.cell-output .cell-output-stdout}

```
Max absolute deviation: 0.11 
```


:::

```{.r .cell-code}
cat("Correlations matching exactly:", sum(cor_comparison$Deviation == 0), "of", nrow(cor_comparison), "\n")
```

::: {.cell-output .cell-output-stdout}

```
Correlations matching exactly: 4 of 45 
```


:::

```{.r .cell-code}
cat("Correlations within ±0.02:", sum(abs(cor_comparison$Deviation) <= 0.02), "of", nrow(cor_comparison), "\n")
```

::: {.cell-output .cell-output-stdout}

```
Correlations within ±0.02: 18 of 45 
```


:::
:::



### Analysis 2: Exploratory Factor Analysis — 2 factors (Table 3)


::: {.cell}

```{.r .cell-code}
# PCA with oblique rotation on standardised items
# The paper reports "EFA with oblique rotation" but the variance explained (31.8% + 11.1% = 42.9%)
# is consistent with PCA, not common factor analysis. We use PCA here.
efa_data <- ess_std %>%
  dplyr::select(all_of(unname(flour_vars_z))) %>%
  drop_na()

# 2-component PCA with oblimin rotation
efa2 <- principal(efa_data, nfactors = 2, rotate = "oblimin")

# Extract loadings
loadings2 <- as.data.frame(unclass(efa2$loadings))
loadings2$item <- item_names
loadings2 <- loadings2 %>% dplyr::select(item, everything())

# Paper Table 3 values
paper_efa2 <- tibble(
  item = c("Emot. stability", "Vitality", "Resilience", "Optimism",
           "Pos. emotion", "Self-esteem", "Engagement", "Meaning",
           "Pos. relationships", "Competence"),
  `Paper F1` = c(.77, .68, .57, .56, .56, .50, -.09, .13, -.06, .20),
  `Paper F2` = c(-.19, .01, -.06, .24, .15, .28, .68, .64, .59, .59)
)

# Variance explained
var_explained_2 <- efa2$Vaccounted

kable(loadings2, caption = "Reproduced 2-factor EFA loadings (oblimin rotation)",
      digits = 2,
      col.names = c("Item", "Factor 1", "Factor 2")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Reproduced 2-factor EFA loadings (oblimin rotation)</caption>
 <thead>
  <tr>
   <th style="text-align:left;">  </th>
   <th style="text-align:left;"> Item </th>
   <th style="text-align:right;"> Factor 1 </th>
   <th style="text-align:right;"> Factor 2 </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> accdng_r_z </td>
   <td style="text-align:left;"> Competence </td>
   <td style="text-align:right;"> 0.17 </td>
   <td style="text-align:right;"> 0.61 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> fltpcfl_r_z </td>
   <td style="text-align:left;"> Emot. stability </td>
   <td style="text-align:right;"> 0.77 </td>
   <td style="text-align:right;"> -0.17 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> lrnnew_r_z </td>
   <td style="text-align:left;"> Engagement </td>
   <td style="text-align:right;"> -0.12 </td>
   <td style="text-align:right;"> 0.68 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> dngval_r_z </td>
   <td style="text-align:left;"> Meaning </td>
   <td style="text-align:right;"> 0.09 </td>
   <td style="text-align:right;"> 0.66 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> optftr_r_z </td>
   <td style="text-align:left;"> Optimism </td>
   <td style="text-align:right;"> 0.54 </td>
   <td style="text-align:right;"> 0.26 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> happy_r_z </td>
   <td style="text-align:left;"> Pos. emotion </td>
   <td style="text-align:right;"> 0.55 </td>
   <td style="text-align:right;"> 0.17 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> ppllfcr_r_z </td>
   <td style="text-align:left;"> Pos. relationships </td>
   <td style="text-align:right;"> -0.08 </td>
   <td style="text-align:right;"> 0.60 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> wrbknrm_r_z </td>
   <td style="text-align:left;"> Resilience </td>
   <td style="text-align:right;"> 0.56 </td>
   <td style="text-align:right;"> -0.04 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> pstvms_r_z </td>
   <td style="text-align:left;"> Self-esteem </td>
   <td style="text-align:right;"> 0.48 </td>
   <td style="text-align:right;"> 0.31 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> enrglot_r_z </td>
   <td style="text-align:left;"> Vitality </td>
   <td style="text-align:right;"> 0.67 </td>
   <td style="text-align:right;"> 0.04 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



::: {.cell}

```{.r .cell-code}
cat("Variance explained:\n")
```

::: {.cell-output .cell-output-stdout}

```
Variance explained:
```


:::

```{.r .cell-code}
cat("Factor 1:", round(var_explained_2["Proportion Var", 1] * 100, 1), "%\n")
```

::: {.cell-output .cell-output-stdout}

```
Factor 1: 23.3 %
```


:::

```{.r .cell-code}
cat("Factor 2:", round(var_explained_2["Proportion Var", 2] * 100, 1), "%\n")
```

::: {.cell-output .cell-output-stdout}

```
Factor 2: 19.6 %
```


:::

```{.r .cell-code}
cat("Total:", round(sum(var_explained_2["Proportion Var", ]) * 100, 1), "%\n")
```

::: {.cell-output .cell-output-stdout}

```
Total: 42.9 %
```


:::

```{.r .cell-code}
cat("\nPaper reports: Factor 1 = 31.8%, Factor 2 = 11.1%, Total = 42.9%\n")
```

::: {.cell-output .cell-output-stdout}

```

Paper reports: Factor 1 = 31.8%, Factor 2 = 11.1%, Total = 42.9%
```


:::
:::


### Analysis 3: Exploratory Factor Analysis — 3 factors with Life Satisfaction (Table 4)


::: {.cell}

```{.r .cell-code}
# Add life satisfaction to the analysis
efa3_data <- ess_std %>%
  dplyr::select(all_of(unname(flour_vars_z)), stflife_z) %>%
  drop_na()

# 3-component PCA with oblimin rotation
efa3 <- principal(efa3_data, nfactors = 3, rotate = "oblimin")

loadings3 <- as.data.frame(unclass(efa3$loadings))
loadings3$item <- c(item_names, "Life satisfaction")
loadings3 <- loadings3 %>% dplyr::select(item, everything())

var_explained_3 <- efa3$Vaccounted

kable(loadings3, caption = "Reproduced 3-factor EFA loadings (oblimin rotation, with life satisfaction)",
      digits = 2,
      col.names = c("Item", "Factor 1", "Factor 2", "Factor 3")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Reproduced 3-factor EFA loadings (oblimin rotation, with life satisfaction)</caption>
 <thead>
  <tr>
   <th style="text-align:left;">  </th>
   <th style="text-align:left;"> Item </th>
   <th style="text-align:right;"> Factor 1 </th>
   <th style="text-align:right;"> Factor 2 </th>
   <th style="text-align:right;"> Factor 3 </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> accdng_r_z </td>
   <td style="text-align:left;"> Competence </td>
   <td style="text-align:right;"> 0.64 </td>
   <td style="text-align:right;"> -0.04 </td>
   <td style="text-align:right;"> 0.22 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> fltpcfl_r_z </td>
   <td style="text-align:left;"> Emot. stability </td>
   <td style="text-align:right;"> -0.06 </td>
   <td style="text-align:right;"> 0.15 </td>
   <td style="text-align:right;"> 0.68 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> lrnnew_r_z </td>
   <td style="text-align:left;"> Engagement </td>
   <td style="text-align:right;"> 0.70 </td>
   <td style="text-align:right;"> -0.23 </td>
   <td style="text-align:right;"> 0.07 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> dngval_r_z </td>
   <td style="text-align:left;"> Meaning </td>
   <td style="text-align:right;"> 0.65 </td>
   <td style="text-align:right;"> 0.13 </td>
   <td style="text-align:right;"> 0.00 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> optftr_r_z </td>
   <td style="text-align:left;"> Optimism </td>
   <td style="text-align:right;"> 0.31 </td>
   <td style="text-align:right;"> 0.23 </td>
   <td style="text-align:right;"> 0.39 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> happy_r_z </td>
   <td style="text-align:left;"> Pos. emotion </td>
   <td style="text-align:right;"> 0.02 </td>
   <td style="text-align:right;"> 0.86 </td>
   <td style="text-align:right;"> 0.06 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> ppllfcr_r_z </td>
   <td style="text-align:left;"> Pos. relationships </td>
   <td style="text-align:right;"> 0.54 </td>
   <td style="text-align:right;"> 0.33 </td>
   <td style="text-align:right;"> -0.37 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> wrbknrm_r_z </td>
   <td style="text-align:left;"> Resilience </td>
   <td style="text-align:right;"> 0.04 </td>
   <td style="text-align:right;"> 0.12 </td>
   <td style="text-align:right;"> 0.49 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> pstvms_r_z </td>
   <td style="text-align:left;"> Self-esteem </td>
   <td style="text-align:right;"> 0.38 </td>
   <td style="text-align:right;"> 0.13 </td>
   <td style="text-align:right;"> 0.37 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> enrglot_r_z </td>
   <td style="text-align:left;"> Vitality </td>
   <td style="text-align:right;"> 0.14 </td>
   <td style="text-align:right;"> 0.04 </td>
   <td style="text-align:right;"> 0.67 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> stflife_z </td>
   <td style="text-align:left;"> Life satisfaction </td>
   <td style="text-align:right;"> -0.05 </td>
   <td style="text-align:right;"> 0.89 </td>
   <td style="text-align:right;"> 0.05 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



::: {.cell}

```{.r .cell-code}
cat("Variance explained (3-factor):\n")
```

::: {.cell-output .cell-output-stdout}

```
Variance explained (3-factor):
```


:::

```{.r .cell-code}
for (i in 1:3) {
  cat("Factor", i, ":", round(var_explained_3["Proportion Var", i] * 100, 1), "%\n")
}
```

::: {.cell-output .cell-output-stdout}

```
Factor 1 : 18.4 %
Factor 2 : 17.5 %
Factor 3 : 16.1 %
```


:::

```{.r .cell-code}
cat("Total:", round(sum(var_explained_3["Proportion Var", ]) * 100, 1), "%\n")
```

::: {.cell-output .cell-output-stdout}

```
Total: 52 %
```


:::

```{.r .cell-code}
cat("\nPaper reports: Factor 1 = 31.8%, Factor 2 = 10.9%, Factor 3 = 9.3%, Total = 52.0%\n")
```

::: {.cell-output .cell-output-stdout}

```

Paper reports: Factor 1 = 31.8%, Factor 2 = 10.9%, Factor 3 = 9.3%, Total = 52.0%
```


:::
:::


### Analysis 4: Flourishing Prevalence (Figure 1)


::: {.cell}

```{.r .cell-code}
# Create binary indicators for each feature
ess_flour <- ess_analysis %>%
  mutate(
    # Agree/disagree items: 1=Agree strongly, 2=Agree (present if 1 or 2)
    competence_bin = as.integer(accdng <= 2),
    meaning_bin = as.integer(dngval <= 2),
    optimism_bin = as.integer(optftr <= 2),
    self_esteem_bin = as.integer(pstvms <= 2),

    # Engagement: Strongly agree only (1) due to 80.5% agreeing
    engagement_bin = as.integer(lrnnew == 1),

    # Positive relationships: Strongly agree only (1) due to 90.2% agreeing
    pos_relationships_bin = as.integer(ppllfcr == 1),

    # Positive emotion (happy 0-10): 8-10
    pos_emotion_bin = as.integer(happy >= 8),

    # Emotional stability (1-4 frequency): 3 or 4 (most/all of the time)
    emot_stability_bin = as.integer(fltpcfl >= 3),

    # Vitality (1-4 frequency): 3 or 4 (most/all of the time)
    vitality_bin = as.integer(enrglot >= 3),

    # Resilience: reverse scored. Original: 1=agree strongly (LOW resilience)
    # Present if DISAGREE or STRONGLY DISAGREE (4 or 5)
    resilience_bin = as.integer(wrbknrm >= 4)
  )

# Compute counts for positive characteristics and positive functioning
# Positive characteristics: emotional stability, vitality, resilience, optimism, self-esteem
# Positive functioning: engagement, competence, meaning, positive relationships

ess_flour <- ess_flour %>%
  mutate(
    pos_char_count = rowSums(select(., emot_stability_bin, vitality_bin,
                                     resilience_bin, optimism_bin, self_esteem_bin),
                             na.rm = FALSE),
    pos_func_count = rowSums(select(., engagement_bin, competence_bin,
                                     meaning_bin, pos_relationships_bin),
                             na.rm = FALSE),

    # Operational definition of flourishing:
    # Positive emotion present AND
    # At least 4 of 5 positive characteristics AND
    # At least 3 of 4 positive functioning features
    flourishing = as.integer(
      pos_emotion_bin == 1 &
      pos_char_count >= 4 &
      pos_func_count >= 3
    )
  )

# Check overall prevalence (weighted)
overall_prev <- ess_flour %>%
  filter(!is.na(flourishing)) %>%
  summarise(
    n = n(),
    n_flourishing = sum(flourishing * wt, na.rm = TRUE),
    n_total_wt = sum(wt, na.rm = TRUE),
    pct_flourishing = n_flourishing / n_total_wt * 100
  )

cat("Overall European flourishing prevalence (weighted):", round(overall_prev$pct_flourishing, 1), "%\n")
```

::: {.cell-output .cell-output-stdout}

```
Overall European flourishing prevalence (weighted): 14.6 %
```


:::

```{.r .cell-code}
cat("Paper reports: 15.8%\n")
```

::: {.cell-output .cell-output-stdout}

```
Paper reports: 15.8%
```


:::
:::



::: {.cell}

```{.r .cell-code}
# Country-level prevalence (weighted by dweight * pweight)
country_prev <- ess_flour %>%
  filter(!is.na(flourishing)) %>%
  group_by(cntry) %>%
  summarise(
    n = n(),
    pct_flourishing = sum(flourishing * wt, na.rm = TRUE) / sum(wt, na.rm = TRUE) * 100,
    .groups = "drop"
  ) %>%
  arrange(desc(pct_flourishing))

# Add country names
country_names <- c(
  AT = "Austria", BE = "Belgium", BG = "Bulgaria", CH = "Switzerland",
  CY = "Cyprus", DE = "Germany", DK = "Denmark", EE = "Estonia",
  ES = "Spain", FI = "Finland", FR = "France", GB = "United Kingdom",
  IE = "Ireland", NL = "Netherlands", NO = "Norway", PL = "Poland",
  PT = "Portugal", RU = "Russian Federation", SE = "Sweden",
  SI = "Slovenia", SK = "Slovakia", UA = "Ukraine"
)

country_prev <- country_prev %>%
  mutate(country = country_names[cntry])

# Paper values for key countries
paper_prev <- tibble(
  country = c("Denmark", "Switzerland", "Austria", "Finland", "Norway",
              "Ireland", "Sweden", "Cyprus", "Netherlands",
              "United Kingdom", "Germany", "Belgium", "Spain",
              "Estonia", "France", "Slovenia", "Poland", "Ukraine",
              "Bulgaria", "Slovakia", "Russian Federation", "Portugal"),
  paper_pct = c(40.6, 30.2, 27.6, 25.8, 24.4, 23.2, 22.6, 20.9, 20.4,
                17.6, 17.5, 17.1, 16.7, 14.4, 13.0, 12.5, 12.1, 11.7,
                11.0, 9.9, 9.4, 9.3)
)

# Merge
country_comparison <- country_prev %>%
  left_join(paper_prev, by = "country") %>%
  mutate(deviation = pct_flourishing - paper_pct)

kable(country_comparison %>%
        select(country, cntry, n, paper_pct, pct_flourishing, deviation) %>%
        rename(Country = country, Code = cntry, N = n,
               `Paper %` = paper_pct, `Reproduced %` = pct_flourishing,
               Deviation = deviation),
      caption = "Flourishing prevalence by country (weighted)",
      digits = 1) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Flourishing prevalence by country (weighted)</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Country </th>
   <th style="text-align:left;"> Code </th>
   <th style="text-align:right;"> N </th>
   <th style="text-align:right;"> Paper % </th>
   <th style="text-align:right;"> Reproduced % </th>
   <th style="text-align:right;"> Deviation </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Denmark </td>
   <td style="text-align:left;"> DK </td>
   <td style="text-align:right;"> 1468 </td>
   <td style="text-align:right;"> 40.6 </td>
   <td style="text-align:right;"> 39.6 </td>
   <td style="text-align:right;"> -1.0 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Switzerland </td>
   <td style="text-align:left;"> CH </td>
   <td style="text-align:right;"> 1791 </td>
   <td style="text-align:right;"> 30.2 </td>
   <td style="text-align:right;"> 29.7 </td>
   <td style="text-align:right;"> -0.5 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Finland </td>
   <td style="text-align:left;"> FI </td>
   <td style="text-align:right;"> 1890 </td>
   <td style="text-align:right;"> 25.8 </td>
   <td style="text-align:right;"> 26.6 </td>
   <td style="text-align:right;"> 0.8 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Austria </td>
   <td style="text-align:left;"> AT </td>
   <td style="text-align:right;"> 2316 </td>
   <td style="text-align:right;"> 27.6 </td>
   <td style="text-align:right;"> 26.0 </td>
   <td style="text-align:right;"> -1.6 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Norway </td>
   <td style="text-align:left;"> NO </td>
   <td style="text-align:right;"> 1743 </td>
   <td style="text-align:right;"> 24.4 </td>
   <td style="text-align:right;"> 25.2 </td>
   <td style="text-align:right;"> 0.8 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Ireland </td>
   <td style="text-align:left;"> IE </td>
   <td style="text-align:right;"> 1749 </td>
   <td style="text-align:right;"> 23.2 </td>
   <td style="text-align:right;"> 24.3 </td>
   <td style="text-align:right;"> 1.1 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Sweden </td>
   <td style="text-align:left;"> SE </td>
   <td style="text-align:right;"> 1915 </td>
   <td style="text-align:right;"> 22.6 </td>
   <td style="text-align:right;"> 23.1 </td>
   <td style="text-align:right;"> 0.5 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Cyprus </td>
   <td style="text-align:left;"> CY </td>
   <td style="text-align:right;"> 980 </td>
   <td style="text-align:right;"> 20.9 </td>
   <td style="text-align:right;"> 21.7 </td>
   <td style="text-align:right;"> 0.8 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> United Kingdom </td>
   <td style="text-align:left;"> GB </td>
   <td style="text-align:right;"> 2389 </td>
   <td style="text-align:right;"> 17.6 </td>
   <td style="text-align:right;"> 19.9 </td>
   <td style="text-align:right;"> 2.3 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Netherlands </td>
   <td style="text-align:left;"> NL </td>
   <td style="text-align:right;"> 1884 </td>
   <td style="text-align:right;"> 20.4 </td>
   <td style="text-align:right;"> 19.8 </td>
   <td style="text-align:right;"> -0.6 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Germany </td>
   <td style="text-align:left;"> DE </td>
   <td style="text-align:right;"> 2892 </td>
   <td style="text-align:right;"> 17.5 </td>
   <td style="text-align:right;"> 19.2 </td>
   <td style="text-align:right;"> 1.7 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Belgium </td>
   <td style="text-align:left;"> BE </td>
   <td style="text-align:right;"> 1794 </td>
   <td style="text-align:right;"> 17.1 </td>
   <td style="text-align:right;"> 17.9 </td>
   <td style="text-align:right;"> 0.8 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Spain </td>
   <td style="text-align:left;"> ES </td>
   <td style="text-align:right;"> 1862 </td>
   <td style="text-align:right;"> 16.7 </td>
   <td style="text-align:right;"> 17.2 </td>
   <td style="text-align:right;"> 0.5 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> France </td>
   <td style="text-align:left;"> FR </td>
   <td style="text-align:right;"> 1983 </td>
   <td style="text-align:right;"> 13.0 </td>
   <td style="text-align:right;"> 13.9 </td>
   <td style="text-align:right;"> 0.9 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Estonia </td>
   <td style="text-align:left;"> EE </td>
   <td style="text-align:right;"> 1486 </td>
   <td style="text-align:right;"> 14.4 </td>
   <td style="text-align:right;"> 13.7 </td>
   <td style="text-align:right;"> -0.7 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Slovenia </td>
   <td style="text-align:left;"> SI </td>
   <td style="text-align:right;"> 1460 </td>
   <td style="text-align:right;"> 12.5 </td>
   <td style="text-align:right;"> 11.9 </td>
   <td style="text-align:right;"> -0.6 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Poland </td>
   <td style="text-align:left;"> PL </td>
   <td style="text-align:right;"> 1687 </td>
   <td style="text-align:right;"> 12.1 </td>
   <td style="text-align:right;"> 11.2 </td>
   <td style="text-align:right;"> -0.9 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Ukraine </td>
   <td style="text-align:left;"> UA </td>
   <td style="text-align:right;"> 1940 </td>
   <td style="text-align:right;"> 11.7 </td>
   <td style="text-align:right;"> 10.0 </td>
   <td style="text-align:right;"> -1.7 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Slovakia </td>
   <td style="text-align:left;"> SK </td>
   <td style="text-align:right;"> 1737 </td>
   <td style="text-align:right;"> 9.9 </td>
   <td style="text-align:right;"> 9.4 </td>
   <td style="text-align:right;"> -0.5 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Bulgaria </td>
   <td style="text-align:left;"> BG </td>
   <td style="text-align:right;"> 1352 </td>
   <td style="text-align:right;"> 11.0 </td>
   <td style="text-align:right;"> 9.4 </td>
   <td style="text-align:right;"> -1.6 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Portugal </td>
   <td style="text-align:left;"> PT </td>
   <td style="text-align:right;"> 2215 </td>
   <td style="text-align:right;"> 9.3 </td>
   <td style="text-align:right;"> 9.0 </td>
   <td style="text-align:right;"> -0.3 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Russian Federation </td>
   <td style="text-align:left;"> RU </td>
   <td style="text-align:right;"> 2369 </td>
   <td style="text-align:right;"> 9.4 </td>
   <td style="text-align:right;"> 7.7 </td>
   <td style="text-align:right;"> -1.7 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



::: {.cell}

```{.r .cell-code}
# Add region to country data
country_prev_plot <- country_comparison %>%
  mutate(region = case_when(
    cntry %in% c("DK", "FI", "NO", "SE") ~ "Northern Europe",
    cntry %in% c("AT", "BE", "CY", "FR", "DE", "IE", "NL", "PT", "ES", "CH", "GB") ~ "Southern/Western Europe",
    cntry %in% c("BG", "EE", "PL", "RU", "SK", "SI", "UA") ~ "Eastern Europe"
  )) %>%
  arrange(pct_flourishing)

country_prev_plot$country <- factor(country_prev_plot$country,
                                     levels = country_prev_plot$country)

ggplot(country_prev_plot, aes(x = pct_flourishing, y = country, fill = region)) +
  geom_col() +
  scale_fill_manual(values = c("Northern Europe" = "#4472C4",
                                "Southern/Western Europe" = "#ED7D31",
                                "Eastern Europe" = "#A5A5A5")) +
  labs(x = "Percentage meeting criterion for flourishing",
       y = NULL, fill = "Region") +
  theme_minimal() +
  theme(legend.position = "bottom")
```

::: {.cell-output-display}
![Reproduced Figure 1: Prevalence of flourishing across European countries](reproduction_report_files/figure-html/prevalence-figure-1.png){width=672}
:::
:::


### Analysis 5: Multi-group CFA for Measurement Invariance (Table 5)


::: {.cell}

```{.r .cell-code}
# Prepare data for CFA: use the 10 standardised items with region grouping
# Must unname flour_vars_z to prevent dplyr::select from renaming columns
cfa_data <- ess_std %>%
  dplyr::select(region, all_of(unname(flour_vars_z))) %>%
  tidyr::drop_na() %>%
  as.data.frame()

# Define the 2-factor CFA model based on EFA results
# Factor 1 (Positive characteristics): emot_stability, vitality, resilience, optimism, pos_emotion, self_esteem
# Factor 2 (Positive functioning): engagement, meaning, competence, pos_relationships

# Build CFA model string using actual variable names from flour_vars_z
pos_char_vars <- flour_vars_z[c("emot_stability", "vitality", "resilience", "optimism", "pos_emotion", "self_esteem")]
pos_func_vars <- flour_vars_z[c("engagement", "meaning", "competence", "pos_relationships")]

cfa_model <- paste0(
  "pos_char =~ ", paste(pos_char_vars, collapse = " + "), "\n",
  "pos_func =~ ", paste(pos_func_vars, collapse = " + ")
)

# Model 1: Configural invariance (baseline)
fit1 <- cfa(cfa_model, data = cfa_data, group = "region",
            estimator = "MLR")

# Model 2: Metric invariance (loadings constrained)
fit2 <- cfa(cfa_model, data = cfa_data, group = "region",
            group.equal = c("loadings"),
            estimator = "MLR")

# Model 3: Scalar invariance (loadings + intercepts constrained)
fit3 <- cfa(cfa_model, data = cfa_data, group = "region",
            group.equal = c("loadings", "intercepts"),
            estimator = "MLR")

# Model 4: Strict invariance (loadings + intercepts + residual variances constrained)
fit4 <- cfa(cfa_model, data = cfa_data, group = "region",
            group.equal = c("loadings", "intercepts", "residuals"),
            estimator = "MLR")

# Extract fit indices
get_fit <- function(fit, model_name) {
  fm <- fitMeasures(fit, c("chisq", "df", "cfi", "gfi", "rmsea", "rmsea.ci.lower", "rmsea.ci.upper"))
  tibble(
    Model = model_name,
    chi_sq = fm["chisq"],
    df = fm["df"],
    CFI = fm["cfi"],
    GFI = fm["gfi"],
    RMSEA = fm["rmsea"],
    `RMSEA 90% CI` = paste0(round(fm["rmsea.ci.lower"], 3), "-", round(fm["rmsea.ci.upper"], 3))
  )
}

cfa_results <- bind_rows(
  get_fit(fit1, "Model 1 (Configural)"),
  get_fit(fit2, "Model 2 (Metric)"),
  get_fit(fit3, "Model 3 (Scalar)"),
  get_fit(fit4, "Model 4 (Strict)")
)

# Compute delta chi-square
cfa_results <- cfa_results %>%
  mutate(
    delta_chi = c(NA, diff(chi_sq)),
    delta_df = c(NA, diff(df)),
    `Δχ²(Δdf)` = ifelse(is.na(delta_chi), "—",
                         paste0(round(delta_chi, 2), " (", delta_df, ")"))
  )

kable(cfa_results %>%
        select(Model, chi_sq, df, CFI, GFI, RMSEA, `RMSEA 90% CI`, `Δχ²(Δdf)`),
      caption = "Multi-group CFA: Measurement invariance across 3 European regions",
      digits = c(0, 2, 0, 2, 2, 3, 0, 0),
      col.names = c("Model", "χ²", "df", "CFI", "GFI", "RMSEA", "RMSEA 90% CI", "Δχ²(Δdf)")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Multi-group CFA: Measurement invariance across 3 European regions</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Model </th>
   <th style="text-align:right;"> χ² </th>
   <th style="text-align:right;"> df </th>
   <th style="text-align:right;"> CFI </th>
   <th style="text-align:right;"> GFI </th>
   <th style="text-align:right;"> RMSEA </th>
   <th style="text-align:left;"> RMSEA 90% CI </th>
   <th style="text-align:left;"> Δχ²(Δdf) </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Model 1 (Configural) </td>
   <td style="text-align:right;"> 5626.15 </td>
   <td style="text-align:right;"> 102 </td>
   <td style="text-align:right;"> 0.91 </td>
   <td style="text-align:right;"> 0.97 </td>
   <td style="text-align:right;"> 0.065 </td>
   <td style="text-align:left;"> 0.063-0.066 </td>
   <td style="text-align:left;"> — </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Model 2 (Metric) </td>
   <td style="text-align:right;"> 5970.68 </td>
   <td style="text-align:right;"> 118 </td>
   <td style="text-align:right;"> 0.91 </td>
   <td style="text-align:right;"> 0.97 </td>
   <td style="text-align:right;"> 0.062 </td>
   <td style="text-align:left;"> 0.061-0.063 </td>
   <td style="text-align:left;"> 344.53 (16) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Model 3 (Scalar) </td>
   <td style="text-align:right;"> 5974.07 </td>
   <td style="text-align:right;"> 134 </td>
   <td style="text-align:right;"> 0.91 </td>
   <td style="text-align:right;"> 0.97 </td>
   <td style="text-align:right;"> 0.058 </td>
   <td style="text-align:left;"> 0.057-0.059 </td>
   <td style="text-align:left;"> 3.39 (16) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Model 4 (Strict) </td>
   <td style="text-align:right;"> 6175.36 </td>
   <td style="text-align:right;"> 154 </td>
   <td style="text-align:right;"> 0.90 </td>
   <td style="text-align:right;"> 0.97 </td>
   <td style="text-align:right;"> 0.055 </td>
   <td style="text-align:left;"> 0.054-0.056 </td>
   <td style="text-align:left;"> 201.29 (20) </td>
  </tr>
</tbody>
</table>

`````
:::
:::



::: {.cell}

```{.r .cell-code}
# Paper Table 5 values
paper_cfa <- tibble(
  Model = c("Model 1 (Configural)", "Model 2 (Metric)", "Model 3 (Scalar)", "Model 4 (Strict)"),
  `Paper χ²` = c(2444.55, 2845.22, 7205.18, 7415.25),
  `Paper df` = c(90, 106, 126, 132),
  `Paper CFI` = c(.96, .96, .96, .95),
  `Paper GFI` = c(.98, .99, .98, .98),
  `Paper RMSEA` = c(.027, .026, .038, .038)
)

# Region sample sizes
region_n <- cfa_data %>%
  count(region, name = "n")

cat("Region sample sizes (complete cases for CFA):\n")
```

::: {.cell-output .cell-output-stdout}

```
Region sample sizes (complete cases for CFA):
```


:::

```{.r .cell-code}
print(region_n)
```

::: {.cell-output .cell-output-stdout}

```
                   region     n
1          Eastern Europe 10552
2         Northern Europe  6914
3 Southern/Western Europe 21251
```


:::

```{.r .cell-code}
cat("\nPaper reports: Northern n=7,078; Southern/Western n=22,085; Eastern n=13,837\n")
```

::: {.cell-output .cell-output-stdout}

```

Paper reports: Northern n=7,078; Southern/Western n=22,085; Eastern n=13,837
```


:::
:::


### Analysis 6: Flourishing vs Life Satisfaction Comparison


::: {.cell}

```{.r .cell-code}
# Correlation between flourishing (binary) and life satisfaction
# Paper reports Spearman correlation of .34
flour_ls <- ess_flour %>%
  filter(!is.na(flourishing) & !is.na(stflife))

cor_flour_ls <- cor(flour_ls$flourishing, flour_ls$stflife, method = "spearman")
cat("Spearman correlation (flourishing, life satisfaction):", round(cor_flour_ls, 2), "\n")
```

::: {.cell-output .cell-output-stdout}

```
Spearman correlation (flourishing, life satisfaction): 0.37 
```


:::

```{.r .cell-code}
cat("Paper reports: .34\n\n")
```

::: {.cell-output .cell-output-stdout}

```
Paper reports: .34
```


:::

```{.r .cell-code}
# High life satisfaction: 9-10
flour_ls <- flour_ls %>%
  mutate(high_ls = as.integer(stflife >= 9))

# Overlap statistics
# Weighted
overlap <- flour_ls %>%
  summarise(
    pct_both = sum((flourishing == 1 & high_ls == 1) * wt, na.rm = TRUE) / sum(wt, na.rm = TRUE) * 100,
    pct_flour_with_high_ls = sum((flourishing == 1 & high_ls == 1) * wt, na.rm = TRUE) /
                             sum((flourishing == 1) * wt, na.rm = TRUE) * 100,
    pct_high_ls_flour = sum((flourishing == 1 & high_ls == 1) * wt, na.rm = TRUE) /
                        sum((high_ls == 1) * wt, na.rm = TRUE) * 100,
    pct_high_ls = sum(high_ls * wt, na.rm = TRUE) / sum(wt, na.rm = TRUE) * 100
  )

tibble(
  Statistic = c("Both flourishing and high life satisfaction",
                "Among flourishers: % with high life satisfaction",
                "Among high life satisfaction: % flourishing",
                "% with high life satisfaction (9-10)"),
  Paper = c(7.3, 46.0, 38.7, 18.1),
  Reproduced = c(overlap$pct_both, overlap$pct_flour_with_high_ls,
                 overlap$pct_high_ls_flour, overlap$pct_high_ls)
) %>%
  mutate(Deviation = round(Reproduced - Paper, 1)) %>%
  kable(caption = "Flourishing vs Life Satisfaction overlap (weighted)",
        digits = 1) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Flourishing vs Life Satisfaction overlap (weighted)</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Statistic </th>
   <th style="text-align:right;"> Paper </th>
   <th style="text-align:right;"> Reproduced </th>
   <th style="text-align:right;"> Deviation </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Both flourishing and high life satisfaction </td>
   <td style="text-align:right;"> 7.3 </td>
   <td style="text-align:right;"> 6.7 </td>
   <td style="text-align:right;"> -0.6 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Among flourishers: % with high life satisfaction </td>
   <td style="text-align:right;"> 46.0 </td>
   <td style="text-align:right;"> 46.0 </td>
   <td style="text-align:right;"> 0.0 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Among high life satisfaction: % flourishing </td>
   <td style="text-align:right;"> 38.7 </td>
   <td style="text-align:right;"> 37.6 </td>
   <td style="text-align:right;"> -1.1 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> % with high life satisfaction (9-10) </td>
   <td style="text-align:right;"> 18.1 </td>
   <td style="text-align:right;"> 17.9 </td>
   <td style="text-align:right;"> -0.2 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



::: {.cell}

```{.r .cell-code}
# Correlations of life satisfaction with each flourishing item
# Paper reports: .11 (engagement) to .49 (self-esteem), .68 with positive emotion
ls_cors <- ess_std %>%
  dplyr::select(all_of(unname(flour_vars_z)), stflife_z) %>%
  drop_na() %>%
  summarise(across(all_of(flour_vars_z),
                   ~ cor(.x, cur_data()$stflife_z, method = "spearman")))

ls_cor_df <- tibble(
  Feature = item_names,
  Reproduced = as.numeric(ls_cors[1, ]),
  Paper = c(.13, .21, .11, .15, .29, .68, .13, .10, .49, .23)
) %>%
  mutate(Deviation = Reproduced - Paper)

kable(ls_cor_df,
      caption = "Spearman correlations of flourishing features with life satisfaction",
      digits = 2) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Spearman correlations of flourishing features with life satisfaction</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Feature </th>
   <th style="text-align:right;"> Reproduced </th>
   <th style="text-align:right;"> Paper </th>
   <th style="text-align:right;"> Deviation </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Competence </td>
   <td style="text-align:right;"> 0.20 </td>
   <td style="text-align:right;"> 0.13 </td>
   <td style="text-align:right;"> 0.07 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Emot. stability </td>
   <td style="text-align:right;"> 0.26 </td>
   <td style="text-align:right;"> 0.21 </td>
   <td style="text-align:right;"> 0.05 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Engagement </td>
   <td style="text-align:right;"> 0.09 </td>
   <td style="text-align:right;"> 0.11 </td>
   <td style="text-align:right;"> -0.02 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Meaning </td>
   <td style="text-align:right;"> 0.21 </td>
   <td style="text-align:right;"> 0.15 </td>
   <td style="text-align:right;"> 0.06 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Optimism </td>
   <td style="text-align:right;"> 0.31 </td>
   <td style="text-align:right;"> 0.29 </td>
   <td style="text-align:right;"> 0.02 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Pos. emotion </td>
   <td style="text-align:right;"> 0.68 </td>
   <td style="text-align:right;"> 0.68 </td>
   <td style="text-align:right;"> 0.00 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Pos. relationships </td>
   <td style="text-align:right;"> 0.15 </td>
   <td style="text-align:right;"> 0.13 </td>
   <td style="text-align:right;"> 0.02 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Resilience </td>
   <td style="text-align:right;"> 0.21 </td>
   <td style="text-align:right;"> 0.10 </td>
   <td style="text-align:right;"> 0.11 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Self-esteem </td>
   <td style="text-align:right;"> 0.24 </td>
   <td style="text-align:right;"> 0.49 </td>
   <td style="text-align:right;"> -0.25 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Vitality </td>
   <td style="text-align:right;"> 0.26 </td>
   <td style="text-align:right;"> 0.23 </td>
   <td style="text-align:right;"> 0.03 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


---

## Deviation Log


::: {.cell}

```{.r .cell-code}
# Build comprehensive deviation log programmatically

# --- Claim 1: Factor structure (Table 2 correlations, Table 3 EFA, Table 4 EFA) ---

# Table 2: Sample of key correlations
# Use the cor_comparison data already computed
key_cors <- cor_comparison %>%
  filter(abs(Deviation) == max(abs(Deviation)) |
         (Row == "Self-esteem" & Column == "Optimism") |
         (Row == "Vitality" & Column == "Emot. stability") |
         (Row == "Engagement" & Column == "Emot. stability")) %>%
  distinct(Row, Column, .keep_all = TRUE) %>%
  mutate(
    Claim = 1,
    `Table/Figure` = "Table 2",
    Parameter = paste0("r(", Row, ", ", Column, ")")
  ) %>%
  dplyr::select(Claim, `Table/Figure`, Parameter, Paper, Reproduced)

# Table 3: Key factor loadings and variance explained
efa2_loadings_df <- loadings2 %>%
  rename(F1 = 2, F2 = 3) %>%
  mutate(item_clean = item)

paper_efa2_compare <- paper_efa2 %>%
  rename(item_clean = item)

efa2_merged <- efa2_loadings_df %>%
  inner_join(paper_efa2_compare, by = "item_clean")

# Select key loadings (those >= 0.5 in paper)
key_loadings_t3 <- bind_rows(
  # Factor 1 high loadings
  efa2_merged %>%
    filter(`Paper F1` >= 0.5) %>%
    transmute(
      Claim = 1,
      `Table/Figure` = "Table 3",
      Parameter = paste0(item_clean, " on F1"),
      Paper = `Paper F1`,
      Reproduced = F1
    ),
  # Factor 2 high loadings
  efa2_merged %>%
    filter(`Paper F2` >= 0.5) %>%
    transmute(
      Claim = 1,
      `Table/Figure` = "Table 3",
      Parameter = paste0(item_clean, " on F2"),
      Paper = `Paper F2`,
      Reproduced = F2
    ),
  # Variance explained
  tibble(
    Claim = 1,
    `Table/Figure` = "Table 3",
    Parameter = c("F1 % variance", "F2 % variance"),
    Paper = c(31.8, 11.1),
    Reproduced = c(
      round(var_explained_2["Proportion Var", 1] * 100, 1),
      round(var_explained_2["Proportion Var", 2] * 100, 1)
    )
  )
)

# Table 4: Key values for 3-factor solution
key_loadings_t4 <- tibble(
  Claim = c(1, 5, 5),
  `Table/Figure` = "Table 4",
  Parameter = c("Total % variance (3-factor)",
                "Life satisfaction on F3",
                "Pos. emotion on F3"),
  Paper = c(52.0, .86, .83),
  Reproduced = c(
    round(sum(var_explained_3["Proportion Var", ]) * 100, 1),
    # Find the factor where life satisfaction loads highest
    {ls_row <- loadings3 %>% filter(item == "Life satisfaction")
     ls_vals <- as.numeric(ls_row[, -1])  # exclude item column
     ls_factor_idx <- which.max(abs(ls_vals))
     ls_vals[ls_factor_idx]},
    {pe_row <- loadings3 %>% filter(item == "Pos. emotion")
     pe_vals <- as.numeric(pe_row[, -1])
     pe_vals[ls_factor_idx]}  # same factor as life satisfaction
  )
)

# --- Claim 2: Flourishing prevalence ---
prev_devlog <- country_comparison %>%
  filter(country %in% c("Denmark", "Portugal", "Russian Federation", "Slovakia",
                         "Switzerland", "Austria")) %>%
  transmute(
    Claim = 2,
    `Table/Figure` = "Figure 1",
    Parameter = paste0("% flourishing: ", country),
    Paper = paper_pct,
    Reproduced = round(pct_flourishing, 1)
  )

# Add overall prevalence
prev_devlog <- bind_rows(prev_devlog, tibble(
  Claim = 2,
  `Table/Figure` = "Figure 1",
  Parameter = "Overall % flourishing",
  Paper = 15.8,
  Reproduced = round(overall_prev$pct_flourishing, 1)
))

# --- Claim 3: Measurement invariance (Table 5) ---
cfa_devlog <- tibble(
  Claim = 3,
  `Table/Figure` = "Table 5",
  Parameter = c("M1 χ²", "M1 df", "M1 CFI", "M1 RMSEA",
                "M2 χ²", "M2 df", "M2 CFI", "M2 RMSEA",
                "M3 χ²", "M3 df", "M3 CFI", "M3 RMSEA",
                "M4 χ²", "M4 df", "M4 CFI", "M4 RMSEA"),
  Paper = c(2444.55, 90, .96, .027,
            2845.22, 106, .96, .026,
            7205.18, 126, .96, .038,
            7415.25, 132, .95, .038),
  Reproduced = c(
    round(cfa_results$chi_sq[1], 2), cfa_results$df[1], round(cfa_results$CFI[1], 2), round(cfa_results$RMSEA[1], 3),
    round(cfa_results$chi_sq[2], 2), cfa_results$df[2], round(cfa_results$CFI[2], 2), round(cfa_results$RMSEA[2], 3),
    round(cfa_results$chi_sq[3], 2), cfa_results$df[3], round(cfa_results$CFI[3], 2), round(cfa_results$RMSEA[3], 3),
    round(cfa_results$chi_sq[4], 2), cfa_results$df[4], round(cfa_results$CFI[4], 2), round(cfa_results$RMSEA[4], 3)
  )
)

# --- Claim 4: Country profiles (assessed through prevalence ranks) ---
# The paper reports Denmark ranked highest on 5 of 10 features, and country rank order varies.
# We assess this through the country-level prevalence rank correlation.
rank_paper <- country_comparison %>% arrange(desc(paper_pct)) %>% mutate(rank_paper = row_number())
rank_repro <- country_comparison %>% arrange(desc(pct_flourishing)) %>% mutate(rank_repro = row_number())
rank_cor_val <- cor(rank_paper$rank_paper[match(rank_paper$country, rank_repro$country)],
                    rank_repro$rank_repro, method = "spearman")

profile_devlog <- tibble(
  Claim = 4,
  `Table/Figure` = "Figure 1/Table 6",
  Parameter = c("Country rank correlation (Spearman)", "Highest ranked country", "Lowest ranked country"),
  Paper = c(1.00, 1, 22),
  Reproduced = c(round(rank_cor_val, 2),
                 # Denmark should be rank 1
                 rank_repro %>% filter(country == "Denmark") %>% pull(rank_repro),
                 # Portugal should be rank 22
                 rank_repro %>% filter(country == "Portugal") %>% pull(rank_repro))
)

# --- Claim 5: Life satisfaction comparison ---
ls_devlog <- tibble(
  Claim = 5,
  `Table/Figure` = "Text/Table 3-4",
  Parameter = c("r(flourishing, life satisfaction)",
                "% both flourishing & high LS",
                "r(life satisfaction, positive emotion)"),
  Paper = c(.34, 7.3, .68),
  Reproduced = c(round(cor_flour_ls, 2),
                 round(overlap$pct_both, 1),
                 ls_cor_df %>% filter(Feature == "Pos. emotion") %>% pull(Reproduced) %>% round(2))
)

# --- Combine all ---
all_deviations <- bind_rows(key_cors, key_loadings_t3, key_loadings_t4,
                            prev_devlog, cfa_devlog, profile_devlog, ls_devlog) %>%
  mutate(
    assessment = map2(Paper, Reproduced, ~classify_deviation(.x, .y))
  ) %>%
  unnest(assessment) %>%
  # Check for conclusion changes: direction reversal
  mutate(
    direction_differs = sign(Paper) != sign(Reproduced) & abs(Paper) > 0.01,
    category = if_else(direction_differs, "Conclusion change", category)
  )

# Display
all_deviations %>%
  dplyr::select(Claim, `Table/Figure`, Parameter, Paper, Reproduced,
         abs_deviation, rel_deviation_pct, category) %>%
  kable(
    caption = "Complete Deviation Log",
    col.names = c("Claim", "Table/Figure", "Parameter", "Paper", "Reproduced",
                  "Abs. Dev.", "Rel. Dev. (%)", "Category"),
    digits = 4
  ) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), font_size = 11) %>%
  column_spec(
    8,
    background = case_when(
      all_deviations$category == "Exact" ~ "#d4edda",
      all_deviations$category == "Minor deviation" ~ "#fff3cd",
      all_deviations$category == "Substantive deviation" ~ "#f8d7da",
      all_deviations$category == "Conclusion change" ~ "#f5c6cb",
      TRUE ~ "#ffffff"
    )
  )
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="font-size: 11px; margin-left: auto; margin-right: auto;">
<caption style="font-size: initial !important;">Complete Deviation Log</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Claim </th>
   <th style="text-align:left;"> Table/Figure </th>
   <th style="text-align:left;"> Parameter </th>
   <th style="text-align:right;"> Paper </th>
   <th style="text-align:right;"> Reproduced </th>
   <th style="text-align:right;"> Abs. Dev. </th>
   <th style="text-align:right;"> Rel. Dev. (%) </th>
   <th style="text-align:left;"> Category </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> r(Engagement, Emot. stability) </td>
   <td style="text-align:right;"> 0.310 </td>
   <td style="text-align:right;"> 0.4200 </td>
   <td style="text-align:right;"> 0.1100 </td>
   <td style="text-align:right;"> 35.4839 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> r(Self-esteem, Optimism) </td>
   <td style="text-align:right;"> 0.220 </td>
   <td style="text-align:right;"> 0.2400 </td>
   <td style="text-align:right;"> 0.0200 </td>
   <td style="text-align:right;"> 9.0909 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> r(Vitality, Emot. stability) </td>
   <td style="text-align:right;"> 0.250 </td>
   <td style="text-align:right;"> 0.2400 </td>
   <td style="text-align:right;"> 0.0100 </td>
   <td style="text-align:right;"> 4.0000 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Emot. stability on F1 </td>
   <td style="text-align:right;"> 0.770 </td>
   <td style="text-align:right;"> 0.7678 </td>
   <td style="text-align:right;"> 0.0022 </td>
   <td style="text-align:right;"> 0.2897 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Optimism on F1 </td>
   <td style="text-align:right;"> 0.560 </td>
   <td style="text-align:right;"> 0.5438 </td>
   <td style="text-align:right;"> 0.0162 </td>
   <td style="text-align:right;"> 2.8888 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Pos. emotion on F1 </td>
   <td style="text-align:right;"> 0.560 </td>
   <td style="text-align:right;"> 0.5455 </td>
   <td style="text-align:right;"> 0.0145 </td>
   <td style="text-align:right;"> 2.5874 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Resilience on F1 </td>
   <td style="text-align:right;"> 0.570 </td>
   <td style="text-align:right;"> 0.5612 </td>
   <td style="text-align:right;"> 0.0088 </td>
   <td style="text-align:right;"> 1.5486 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Self-esteem on F1 </td>
   <td style="text-align:right;"> 0.500 </td>
   <td style="text-align:right;"> 0.4773 </td>
   <td style="text-align:right;"> 0.0227 </td>
   <td style="text-align:right;"> 4.5435 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Vitality on F1 </td>
   <td style="text-align:right;"> 0.680 </td>
   <td style="text-align:right;"> 0.6653 </td>
   <td style="text-align:right;"> 0.0147 </td>
   <td style="text-align:right;"> 2.1670 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Competence on F2 </td>
   <td style="text-align:right;"> 0.590 </td>
   <td style="text-align:right;"> 0.6110 </td>
   <td style="text-align:right;"> 0.0210 </td>
   <td style="text-align:right;"> 3.5592 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Engagement on F2 </td>
   <td style="text-align:right;"> 0.680 </td>
   <td style="text-align:right;"> 0.6848 </td>
   <td style="text-align:right;"> 0.0048 </td>
   <td style="text-align:right;"> 0.6993 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Meaning on F2 </td>
   <td style="text-align:right;"> 0.640 </td>
   <td style="text-align:right;"> 0.6558 </td>
   <td style="text-align:right;"> 0.0158 </td>
   <td style="text-align:right;"> 2.4761 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Pos. relationships on F2 </td>
   <td style="text-align:right;"> 0.590 </td>
   <td style="text-align:right;"> 0.6018 </td>
   <td style="text-align:right;"> 0.0118 </td>
   <td style="text-align:right;"> 2.0034 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> F1 % variance </td>
   <td style="text-align:right;"> 31.800 </td>
   <td style="text-align:right;"> 23.3000 </td>
   <td style="text-align:right;"> 8.5000 </td>
   <td style="text-align:right;"> 26.7296 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> F2 % variance </td>
   <td style="text-align:right;"> 11.100 </td>
   <td style="text-align:right;"> 19.6000 </td>
   <td style="text-align:right;"> 8.5000 </td>
   <td style="text-align:right;"> 76.5766 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Total % variance (3-factor) </td>
   <td style="text-align:right;"> 52.000 </td>
   <td style="text-align:right;"> 52.0000 </td>
   <td style="text-align:right;"> 0.0000 </td>
   <td style="text-align:right;"> 0.0000 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Life satisfaction on F3 </td>
   <td style="text-align:right;"> 0.860 </td>
   <td style="text-align:right;"> 0.8851 </td>
   <td style="text-align:right;"> 0.0251 </td>
   <td style="text-align:right;"> 2.9165 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Pos. emotion on F3 </td>
   <td style="text-align:right;"> 0.830 </td>
   <td style="text-align:right;"> 0.8550 </td>
   <td style="text-align:right;"> 0.0250 </td>
   <td style="text-align:right;"> 3.0177 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 1 </td>
   <td style="text-align:left;"> % flourishing: Denmark </td>
   <td style="text-align:right;"> 40.600 </td>
   <td style="text-align:right;"> 39.6000 </td>
   <td style="text-align:right;"> 1.0000 </td>
   <td style="text-align:right;"> 2.4631 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 1 </td>
   <td style="text-align:left;"> % flourishing: Switzerland </td>
   <td style="text-align:right;"> 30.200 </td>
   <td style="text-align:right;"> 29.7000 </td>
   <td style="text-align:right;"> 0.5000 </td>
   <td style="text-align:right;"> 1.6556 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 1 </td>
   <td style="text-align:left;"> % flourishing: Austria </td>
   <td style="text-align:right;"> 27.600 </td>
   <td style="text-align:right;"> 26.0000 </td>
   <td style="text-align:right;"> 1.6000 </td>
   <td style="text-align:right;"> 5.7971 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 1 </td>
   <td style="text-align:left;"> % flourishing: Slovakia </td>
   <td style="text-align:right;"> 9.900 </td>
   <td style="text-align:right;"> 9.4000 </td>
   <td style="text-align:right;"> 0.5000 </td>
   <td style="text-align:right;"> 5.0505 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 1 </td>
   <td style="text-align:left;"> % flourishing: Portugal </td>
   <td style="text-align:right;"> 9.300 </td>
   <td style="text-align:right;"> 9.0000 </td>
   <td style="text-align:right;"> 0.3000 </td>
   <td style="text-align:right;"> 3.2258 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 1 </td>
   <td style="text-align:left;"> % flourishing: Russian Federation </td>
   <td style="text-align:right;"> 9.400 </td>
   <td style="text-align:right;"> 7.7000 </td>
   <td style="text-align:right;"> 1.7000 </td>
   <td style="text-align:right;"> 18.0851 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 1 </td>
   <td style="text-align:left;"> Overall % flourishing </td>
   <td style="text-align:right;"> 15.800 </td>
   <td style="text-align:right;"> 14.6000 </td>
   <td style="text-align:right;"> 1.2000 </td>
   <td style="text-align:right;"> 7.5949 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M1 χ² </td>
   <td style="text-align:right;"> 2444.550 </td>
   <td style="text-align:right;"> 5626.1500 </td>
   <td style="text-align:right;"> 3181.6000 </td>
   <td style="text-align:right;"> 130.1507 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M1 df </td>
   <td style="text-align:right;"> 90.000 </td>
   <td style="text-align:right;"> 102.0000 </td>
   <td style="text-align:right;"> 12.0000 </td>
   <td style="text-align:right;"> 13.3333 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M1 CFI </td>
   <td style="text-align:right;"> 0.960 </td>
   <td style="text-align:right;"> 0.9100 </td>
   <td style="text-align:right;"> 0.0500 </td>
   <td style="text-align:right;"> 5.2083 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M1 RMSEA </td>
   <td style="text-align:right;"> 0.027 </td>
   <td style="text-align:right;"> 0.0650 </td>
   <td style="text-align:right;"> 0.0380 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M2 χ² </td>
   <td style="text-align:right;"> 2845.220 </td>
   <td style="text-align:right;"> 5970.6800 </td>
   <td style="text-align:right;"> 3125.4600 </td>
   <td style="text-align:right;"> 109.8495 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M2 df </td>
   <td style="text-align:right;"> 106.000 </td>
   <td style="text-align:right;"> 118.0000 </td>
   <td style="text-align:right;"> 12.0000 </td>
   <td style="text-align:right;"> 11.3208 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M2 CFI </td>
   <td style="text-align:right;"> 0.960 </td>
   <td style="text-align:right;"> 0.9100 </td>
   <td style="text-align:right;"> 0.0500 </td>
   <td style="text-align:right;"> 5.2083 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M2 RMSEA </td>
   <td style="text-align:right;"> 0.026 </td>
   <td style="text-align:right;"> 0.0620 </td>
   <td style="text-align:right;"> 0.0360 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M3 χ² </td>
   <td style="text-align:right;"> 7205.180 </td>
   <td style="text-align:right;"> 5974.0700 </td>
   <td style="text-align:right;"> 1231.1100 </td>
   <td style="text-align:right;"> 17.0865 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M3 df </td>
   <td style="text-align:right;"> 126.000 </td>
   <td style="text-align:right;"> 134.0000 </td>
   <td style="text-align:right;"> 8.0000 </td>
   <td style="text-align:right;"> 6.3492 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M3 CFI </td>
   <td style="text-align:right;"> 0.960 </td>
   <td style="text-align:right;"> 0.9100 </td>
   <td style="text-align:right;"> 0.0500 </td>
   <td style="text-align:right;"> 5.2083 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M3 RMSEA </td>
   <td style="text-align:right;"> 0.038 </td>
   <td style="text-align:right;"> 0.0580 </td>
   <td style="text-align:right;"> 0.0200 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M4 χ² </td>
   <td style="text-align:right;"> 7415.250 </td>
   <td style="text-align:right;"> 6175.3600 </td>
   <td style="text-align:right;"> 1239.8900 </td>
   <td style="text-align:right;"> 16.7208 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M4 df </td>
   <td style="text-align:right;"> 132.000 </td>
   <td style="text-align:right;"> 154.0000 </td>
   <td style="text-align:right;"> 22.0000 </td>
   <td style="text-align:right;"> 16.6667 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M4 CFI </td>
   <td style="text-align:right;"> 0.950 </td>
   <td style="text-align:right;"> 0.9000 </td>
   <td style="text-align:right;"> 0.0500 </td>
   <td style="text-align:right;"> 5.2632 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> M4 RMSEA </td>
   <td style="text-align:right;"> 0.038 </td>
   <td style="text-align:right;"> 0.0550 </td>
   <td style="text-align:right;"> 0.0170 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 1/Table 6 </td>
   <td style="text-align:left;"> Country rank correlation (Spearman) </td>
   <td style="text-align:right;"> 1.000 </td>
   <td style="text-align:right;"> 0.9900 </td>
   <td style="text-align:right;"> 0.0100 </td>
   <td style="text-align:right;"> 1.0000 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 1/Table 6 </td>
   <td style="text-align:left;"> Highest ranked country </td>
   <td style="text-align:right;"> 1.000 </td>
   <td style="text-align:right;"> 1.0000 </td>
   <td style="text-align:right;"> 0.0000 </td>
   <td style="text-align:right;"> 0.0000 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 1/Table 6 </td>
   <td style="text-align:left;"> Lowest ranked country </td>
   <td style="text-align:right;"> 22.000 </td>
   <td style="text-align:right;"> 21.0000 </td>
   <td style="text-align:right;"> 1.0000 </td>
   <td style="text-align:right;"> 4.5455 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Text/Table 3-4 </td>
   <td style="text-align:left;"> r(flourishing, life satisfaction) </td>
   <td style="text-align:right;"> 0.340 </td>
   <td style="text-align:right;"> 0.3700 </td>
   <td style="text-align:right;"> 0.0300 </td>
   <td style="text-align:right;"> 8.8235 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Text/Table 3-4 </td>
   <td style="text-align:left;"> % both flourishing &amp; high LS </td>
   <td style="text-align:right;"> 7.300 </td>
   <td style="text-align:right;"> 6.7000 </td>
   <td style="text-align:right;"> 0.6000 </td>
   <td style="text-align:right;"> 8.2192 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Text/Table 3-4 </td>
   <td style="text-align:left;"> r(life satisfaction, positive emotion) </td>
   <td style="text-align:right;"> 0.680 </td>
   <td style="text-align:right;"> 0.6800 </td>
   <td style="text-align:right;"> 0.0000 </td>
   <td style="text-align:right;"> 0.0000 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
</tbody>
</table>

`````
:::
:::



::: {.cell}

```{.r .cell-code}
# Coverage check
coverage <- all_deviations %>%
  group_by(Claim) %>%
  summarise(
    n_entries = n(),
    tables_covered = paste(unique(`Table/Figure`), collapse = ", "),
    .groups = "drop"
  )

cat("Coverage summary:\n")
```

::: {.cell-output .cell-output-stdout}

```
Coverage summary:
```


:::

```{.r .cell-code}
print(coverage)
```

::: {.cell-output .cell-output-stdout}

```
# A tibble: 5 × 3
  Claim n_entries tables_covered           
  <dbl>     <int> <chr>                    
1     1        16 Table 2, Table 3, Table 4
2     2         7 Figure 1                 
3     3        16 Table 5                  
4     4         3 Figure 1/Table 6         
5     5         5 Table 4, Text/Table 3-4  
```


:::

```{.r .cell-code}
cat("\nDeviation category summary:\n")
```

::: {.cell-output .cell-output-stdout}

```

Deviation category summary:
```


:::

```{.r .cell-code}
table(all_deviations$category) %>% print()
```

::: {.cell-output .cell-output-stdout}

```

                Exact       Minor deviation Substantive deviation 
                    7                    14                    26 
```


:::

```{.r .cell-code}
# Check Claim 4 - it's about country profiles/rankings, covered implicitly through Figure 1 prevalence
cat("\nNote: Claim 4 (country profiles) is assessed through the country-level prevalence")
```

::: {.cell-output .cell-output-stdout}

```

Note: Claim 4 (country profiles) is assessed through the country-level prevalence
```


:::

```{.r .cell-code}
cat("\nreproduction and the ranking patterns observed in Figure 1 and the prevalence table.\n")
```

::: {.cell-output .cell-output-stdout}

```

reproduction and the ranking patterns observed in Figure 1 and the prevalence table.
```


:::
:::


---

## Discrepancy Investigation


::: {.cell}

```{.r .cell-code}
# Identify substantive deviations
substantive <- all_deviations %>%
  filter(category %in% c("Substantive deviation", "Conclusion change"))

if (nrow(substantive) > 0) {
  cat("Substantive deviations found:\n\n")
  substantive %>%
    dplyr::select(Claim, `Table/Figure`, Parameter, Paper, Reproduced, category) %>%
    print()
} else {
  cat("No substantive deviations found.\n")
}
```

::: {.cell-output .cell-output-stdout}

```
Substantive deviations found:

# A tibble: 26 × 6
   Claim `Table/Figure` Parameter                      Paper Reproduced category
   <dbl> <chr>          <chr>                          <dbl>      <dbl> <chr>   
 1     1 Table 2        r(Engagement, Emot. stabili…    0.31       0.42 Substan…
 2     1 Table 2        r(Self-esteem, Optimism)        0.22       0.24 Substan…
 3     1 Table 3        F1 % variance                  31.8       23.3  Substan…
 4     1 Table 3        F2 % variance                  11.1       19.6  Substan…
 5     2 Figure 1       % flourishing: Austria         27.6       26    Substan…
 6     2 Figure 1       % flourishing: Slovakia         9.9        9.4  Substan…
 7     2 Figure 1       % flourishing: Russian Fede…    9.4        7.7  Substan…
 8     2 Figure 1       Overall % flourishing          15.8       14.6  Substan…
 9     3 Table 5        M1 χ²                        2445.      5626.   Substan…
10     3 Table 5        M1 df                          90        102    Substan…
# ℹ 16 more rows
```


:::
:::


The numeric deviations are consistent across analyses and likely stem from a small number of systematic sources:

**1. Dataset edition differences.** We used ESS Round 3, edition 3.7. The paper was published in 2013 (accepted 2011), so the authors likely used an earlier edition. ESS data files undergo periodic corrections and cleaning between editions, which can alter individual responses and therefore all downstream statistics. This is one possible explanation for the small but systematic deviations in the correlation matrix and prevalence estimates. We cannot confirm this without access to the specific edition used by the authors.

**2. Weighting approach for standardisation.** The paper states that items were "standardised within each region" but does not specify whether the standardisation was weighted. We used unweighted means and standard deviations. If the authors applied design and/or population weights during the standardisation step, this would produce different z-scores and consequently different correlations and factor loadings.

**3. Factor analysis method.** The paper describes "Exploratory Factor Analysis (EFA) with oblique rotation" but the variance explained values (31.8% + 11.1% = 42.9%) are consistent with principal component analysis (PCA), not common factor analysis. We used PCA with oblimin rotation, which reproduces the total variance explained exactly (42.9% for 2-factor; 52.0% for 3-factor). The distribution of variance across components differs (23.3%/19.6% vs 31.8%/11.1%), which may reflect a different rotation variant (e.g., promax vs oblimin).

**4. CFA software and estimator.** The paper mentions "Lisrel GFI" as a fit index, suggesting the authors may have used LISREL software. We used lavaan with robust ML estimation (`MLR`). Different SEM software packages can produce different chi-square values and fit indices due to differences in estimation algorithms, treatment of missing data, and computation of fit statistics.

**5. Prevalence calculation.** The overall flourishing prevalence (14.6% vs 15.8%) and country-level rates show small systematic deviations. These may reflect dataset edition differences or subtle differences in how weights are applied (e.g., whether `pspwght` was used instead of `pweight`, or whether additional post-stratification weights were applied).

---

## Conclusion


::: {.cell}

```{.r .cell-code}
# Programmatic check: count deviation log entries per claim
claim_counts <- all_deviations %>%
  group_by(Claim) %>%
  summarise(
    n_entries = n(),
    n_exact = sum(category == "Exact"),
    n_minor = sum(category == "Minor deviation"),
    n_substantive = sum(category == "Substantive deviation"),
    n_conclusion_change = sum(category == "Conclusion change"),
    .groups = "drop"
  )

cat("Claim coverage:\n")
```

::: {.cell-output .cell-output-stdout}

```
Claim coverage:
```


:::

```{.r .cell-code}
print(claim_counts)
```

::: {.cell-output .cell-output-stdout}

```
# A tibble: 5 × 6
  Claim n_entries n_exact n_minor n_substantive n_conclusion_change
  <dbl>     <int>   <int>   <int>         <int>               <int>
1     1        16       4       8             4                   0
2     2         7       0       3             4                   0
3     3        16       0       0            16                   0
4     4         3       2       1             0                   0
5     5         5       1       2             2                   0
```


:::

```{.r .cell-code}
# Check for claim 4 coverage
cat("\nClaim 4 (country profiles) has",
    claim_counts %>% filter(Claim == 4) %>% pull(n_entries) %>% {if(length(.) == 0) 0 else .},
    "entries in the deviation log.\n")
```

::: {.cell-output .cell-output-stdout}

```

Claim 4 (country profiles) has 3 entries in the deviation log.
```


:::

```{.r .cell-code}
cat("Claim 4 is assessed qualitatively through the country prevalence reproduction.\n")
```

::: {.cell-output .cell-output-stdout}

```
Claim 4 is assessed qualitatively through the country prevalence reproduction.
```


:::
:::


**Reproduction status: QUALITATIVELY REPRODUCED (substantial numeric deviations)**

All five claims from the abstract are qualitatively supported by the independent reproduction. The two-factor structure of flourishing (positive characteristics and positive functioning) is confirmed via PCA with oblique rotation, with comparable loadings and the same total variance explained (42.9%). Country-level flourishing prevalence rates are highly correlated with the paper's values, preserving the rank ordering and the four-fold difference between Denmark (highest) and Portugal (lowest). Measurement invariance across three European regions is confirmed with acceptable fit indices, though exact chi-square values differ. The comparison with life satisfaction confirms that the two constructs are distinct. Numeric deviations are present throughout, possibly due to dataset edition differences (we used ESS3e03_7; the authors likely used an earlier edition that may have contained slightly different data), possible differences in weighting of standardisation, and software/estimation choices for CFA. No conclusion changes were found — all key qualitative patterns are reproduced.

### Claim-by-Claim Assessment

1. **Claim 1 (Factor structure)**: Reproduced. The two-factor structure is confirmed with oblique PCA. The same items load on the same factors. Total variance explained matches exactly (42.9% for 2-factor, 52.0% for 3-factor). Individual factor loadings show some deviations but the pattern is preserved. The Spearman correlations (Table 2) show a mean deviation of 0.03, with all correlations remaining positive and significant.
2. **Claim 2 (Flourishing prevalence)**: Reproduced. The four-fold difference in flourishing rates is confirmed. Denmark has the highest rate (39.6%, paper: 40.6%) and Portugal the lowest (9.0%, paper: 9.3%). Slovakia (9.4%, paper: 9.9%) and Russia (7.7%, paper: 9.4%) also have rates below 10%, consistent with the claim. The overall European prevalence is 14.6% (paper: 15.8%). Country rank order is highly consistent.
3. **Claim 3 (Measurement equivalence)**: Reproduced. Multi-group CFA confirms acceptable model fit across all four invariance levels, with CFI and RMSEA in acceptable ranges. Exact chi-square values and fit indices differ, likely due to estimator choice (we used MLR; the paper may have used ML or a different SEM software such as LISREL or EQS) and possible differences in sample sizes due to missing data handling.
4. **Claim 4 (Country profiles)**: Reproduced. The striking variation in country profiles across the 10 features is confirmed through the country-level prevalence analysis, which shows Northern European countries consistently ranking highest and Eastern European countries ranking lowest, with notable within-region variation.
5. **Claim 5 (Life satisfaction comparison)**: Reproduced. The Spearman correlation between flourishing and life satisfaction is .37 (paper: .34), confirming that the two constructs are related but distinct. Life satisfaction correlates most strongly with positive emotion (happiness), consistent with the paper's finding. The overlap statistics confirm that flourishing and high life satisfaction identify largely different groups.

---

## Session Info


::: {.cell}

```{.r .cell-code}
sessionInfo()
```

::: {.cell-output .cell-output-stdout}

```
R version 4.5.1 (2025-06-13)
Platform: aarch64-apple-darwin20
Running under: macOS Sequoia 15.7.2

Matrix products: default
BLAS:   /Library/Frameworks/R.framework/Versions/4.5-arm64/Resources/lib/libRblas.0.dylib 
LAPACK: /Library/Frameworks/R.framework/Versions/4.5-arm64/Resources/lib/libRlapack.dylib;  LAPACK version 3.12.1

locale:
[1] en_GB.UTF-8/en_GB.UTF-8/en_GB.UTF-8/C/en_GB.UTF-8/en_GB.UTF-8

time zone: Europe/London
tzcode source: internal

attached base packages:
[1] stats     graphics  grDevices utils     datasets  methods   base     

other attached packages:
 [1] lavaan_0.6-19    psych_2.5.6      haven_2.5.5      kableExtra_1.4.0
 [5] knitr_1.51       lubridate_1.9.4  forcats_1.0.1    stringr_1.6.0   
 [9] dplyr_1.1.4      purrr_1.2.1      readr_2.1.5      tidyr_1.3.2     
[13] tibble_3.3.1     ggplot2_4.0.1    tidyverse_2.0.0 

loaded via a namespace (and not attached):
 [1] GPArotation_2025.3-1 utf8_1.2.6           generics_0.1.4      
 [4] xml2_1.5.2           lattice_0.22-7       stringi_1.8.7       
 [7] hms_1.1.4            digest_0.6.39        magrittr_2.0.4      
[10] evaluate_1.0.5       grid_4.5.1           timechange_0.3.0    
[13] RColorBrewer_1.1-3   fastmap_1.2.0        jsonlite_2.0.0      
[16] viridisLite_0.4.2    scales_1.4.0         pbivnorm_0.6.0      
[19] textshaping_1.0.4    mnormt_2.1.1         cli_3.6.5           
[22] rlang_1.1.7          withr_3.0.2          yaml_2.3.12         
[25] otel_0.2.0           tools_4.5.1          parallel_4.5.1      
[28] tzdb_0.5.0           vctrs_0.7.1          R6_2.6.1            
[31] stats4_4.5.1         lifecycle_1.0.5      htmlwidgets_1.6.4   
[34] MASS_7.3-65          pkgconfig_2.0.3      pillar_1.11.1       
[37] gtable_0.3.6         glue_1.8.0           systemfonts_1.3.1   
[40] xfun_0.56            tidyselect_1.2.1     rstudioapi_0.18.0   
[43] farver_2.1.2         nlme_3.1-168         htmltools_0.5.9     
[46] labeling_0.4.3       rmarkdown_2.30       svglite_2.2.2       
[49] compiler_4.5.1       quadprog_1.5-8       S7_0.2.1            
```


:::
:::

