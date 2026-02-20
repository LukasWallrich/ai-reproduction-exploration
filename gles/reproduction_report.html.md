---
title: "Reproduction Report: Steiner, Schimpf & Wuttke (2023)"
subtitle: "Left Behind and United by Populism? Populism's Multiple Roots in Feelings of Lacking Societal Recognition"
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

**Paper**: Steiner, N. D., Schimpf, C. H., & Wuttke, A. (2023). Left Behind and United by Populism? Populism's Multiple Roots in Feelings of Lacking Societal Recognition. *Politische Vierteljahresschrift*, 64, 107–132. https://doi.org/10.1007/s11615-022-00416-4

**Data**: GLES Cross-Section 2021, Pre-Election (ZA7700), version 3.1.0 (paper cites v2.0.0), N ≈ 4,941

**Verdict**: QUALITATIVELY REPRODUCED

All four claims from the abstract are reproduced. Correlations (Figure 2) and group mean differences (Figure 3) match closely. R² values for Models 1–2 are exact (0.26), and the mean index (0.24) and factor score (0.23) comparisons also match. Models 3 and 4 show lower reproduced R² values (0.17 vs. paper 0.18 for Model 3; 0.30 vs. 0.32 for Model 4), which slightly weakens the quantitative support for Claim 4 but preserves the qualitative pattern of R² increase. Consultation of the replication code revealed several operationalization differences (age group boundaries, income imputation method, quantile weighting, occupation coding) that likely account for sample size differences and the R² deviations. Of 32 parameters checked, 27 are classified as Exact, 3 as Minor deviation, and 2 as Substantive deviation. No conclusion changes were found — all significance patterns and effect directions are confirmed.
:::

## Open Materials

| Material | Available | Location |
|----------|-----------|----------|
| Supplementary materials | Yes | Springer (electronic supplementary material) |
| Replication code | Yes | https://osf.io/b3tj4/ (Stata .do files, R plotting script) |
| Replication data (processed) | Yes | https://osf.io/b3tj4/ |
| Raw data | Yes (registration required) | GESIS ZA7700: https://doi.org/10.4232/1.13860 |
| Preregistration | Yes | https://osf.io/kje48 |

Replication materials were **not consulted** during the initial reproduction (Stages 1–5). After substantive deviations were identified in the R² values for Models 3 and 4, the Stata `.do` files and R analysis script from OSF were consulted (Stage 6) to compare analytical decisions. See the Discrepancy Investigation section for findings.

---

## Paper Overview

### Research Question

Does the perception of lacking societal recognition — conceptualized as a multidimensional construct with economic, work-related, services-related, and opinion-related facets — unite otherwise heterogeneous social groups in their support for populism?

### Key Methods

- **Data**: GLES Pre-Election Cross-Section 2021 (N = 5,116; analysis N ≈ 4,941 after excluding 175 cases with missing poststratification weights)
- **Analyses**: (1) Weighted mean comparisons with t-tests across social groups (Figure 3); (2) Weighted correlations (Figure 2); (3) Weighted OLS regressions with populist attitudes as outcome (Figure 4, Table E1 in appendix)
- **Software**: Authors used Stata (replication code is .do files)

### Claims from the Abstract

1. **Multiple social segments harbor feelings of lacking recognition**: From rural residents to sociocultural conservatives or low-income citizens, seemingly unrelated segments of society harbor feelings of lacking recognition, but for distinct reasons.
2. **Each distinct feeling of lacking recognition is associated with populist attitudes**: Each of the distinct feelings of lacking recognition are associated with populist attitudes.
3. **Sufficient conditions with weak substitutability**: The relationship between recognition and populism follows a logic of sufficient conditions with weak substitutability (the composite score based on this logic matches the explanatory power of individual facets entered separately).
4. **Social group memberships mediate through recognition**: Adding recognition variables to a model with social group predictors increases R² and reduces group coefficients, indicating recognition mediates the group-populism link.

---

## Data and Variable Construction


::: {.cell}

```{.r .cell-code}
# Load GLES data
d_raw <- read_sav("data/ZA7700_v3-1-0_en.sav")

# Convert to numeric, setting negative values (missing codes) to NA
recode_missing <- function(x) {
  x_num <- as.numeric(x)
  x_num[x_num < 0] <- NA
  x_num
}

d <- d_raw %>%
  mutate(across(everything(), recode_missing))

# Raw dataset dimensions captured in sample overview table below

# --- Lacking Recognition items (q46a-d) ---
# Original: 1 = strongly agree ... 5 = strongly disagree
# Recode to 0-1 where higher = more lacking recognition
# So reverse: (5 - x) / 4 maps 1->1, 5->0. Wait, the paper says
# "higher values indicate a perceived lack of recognition"
# Agreement (1) means they agree they lack recognition, so agree = high LoR
# Recode: (5 - x) / 4 gives: 1->1, 2->0.75, 3->0.5, 4->0.25, 5->0
d <- d %>%
  mutate(
    lor_economic = (5 - q46a) / 4,
    lor_work     = (5 - q46b) / 4,
    lor_services = (5 - q46c) / 4,
    lor_opinion  = (5 - q46d) / 4
  )

# --- Composite Lack of Recognition (sufficient conditions formula) ---
# lor_composite = (f1^2 + f2^2 + f3^2 + f4^2) / 4
d <- d %>%
  mutate(
    lor_composite = (lor_economic^2 + lor_work^2 + lor_services^2 + lor_opinion^2) / 4
  )

# --- Populist attitudes (q51a-f) ---
# Akkerman et al. (2014) scale, 6 items, 5-point Likert
# Items recoded to 0-1 (agreement = higher populism)
# Three subdimensions per Akkerman et al. (2014):
#   People-centrism: q51b, q51c
#   Anti-elitism: q51d, q51e
#   Manichaean: q51a, q51f
# Subdimension means multiplied per Wuttke et al. (2020)
# Product of three 0-1 subdimension means gives a 0-1 score
d <- d %>%
  mutate(
    pop_a = (5 - q51a) / 4,
    pop_b = (5 - q51b) / 4,
    pop_c = (5 - q51c) / 4,
    pop_d = (5 - q51d) / 4,
    pop_e = (5 - q51e) / 4,
    pop_f = (5 - q51f) / 4,
    pop_people    = (pop_b + pop_c) / 2,
    pop_antielite = (pop_d + pop_e) / 2,
    pop_manichean = (pop_a + pop_f) / 2,
    populism = pop_people * pop_antielite * pop_manichean
  )

# --- Weight variable ---
d <- d %>%
  mutate(weight = w_ipfges)

# --- Low-income individuals ---
# Equivalized household income: OECD modified scale
# First adult = 1.0, additional adults (14+) = 0.5, children (<14) = 0.3
# Income midpoints for d63 categories
income_midpoints <- c(
  `1` = 250, `2` = 625, `3` = 875, `4` = 1125, `5` = 1375,
  `6` = 1750, `7` = 2250, `8` = 2750, `9` = 3500, `10` = 4500,
  `11` = 6250, `12` = 8750, `13` = 12500
)

d <- d %>%
  mutate(
    hh_income_mid = income_midpoints[as.character(d63)],
    # Count household members
    hh_size = d3,
    # Count children under 14 from d4a-d4e
    n_children = rowSums(
      across(c(d4a, d4b, d4c, d4d, d4e), ~ !is.na(.) & . > 0 & . < 14),
      na.rm = TRUE
    ),
    # Additional adults = hh_size - 1 - n_children (first person is respondent)
    n_additional_adults = pmax(0, hh_size - 1 - n_children, na.rm = TRUE),
    # OECD modified equivalence scale
    equiv_factor = 1.0 + 0.5 * n_additional_adults + 0.3 * n_children,
    equiv_income = hh_income_mid / equiv_factor
  )

# Low-income = lowest quintile of equivalized income (weighted)
# Use weighted quintile
valid_income <- d %>% filter(!is.na(equiv_income) & !is.na(weight))
wt_quantile <- Hmisc::wtd.quantile(valid_income$equiv_income, valid_income$weight, probs = 0.2)
d <- d %>%
  mutate(low_income = as.integer(equiv_income <= wt_quantile))

# Low-income threshold and counts shown in sample overview

# --- Low-skilled workers ---
# "unskilled and semiskilled worker" (11) or "employee with simple duties" (22)
# Current (d11) or former (d20) occupation
d <- d %>%
  mutate(
    low_skill = as.integer(d11 %in% c(11, 22) | d20 %in% c(11, 22))
  )
# N counts shown in sample overview

# --- Rural residents ---
# wum6: 4 = rural village, 5 = single homestead
d <- d %>%
  mutate(rural = as.integer(wum6 %in% c(4, 5)))
# N counts shown in sample overview

# --- Sociocultural conservatives ---
# Factor score from 5 items: immigration (q43), assimilation (q27a),
# EU integration (q27f), gender equality (q27g), climate change (q48)
# All recoded so higher = more conservative
# q27a (assimilation): 1=strongly agree ... 5=strongly disagree
#   Agreement = want assimilation = conservative → reverse: (5 - q27a) / 4
# q27f (EU integration): 1=strongly agree ... 5=strongly disagree
#   Agreement = push EU further = progressive → no reverse: (q27f - 1) / 4
# q27g (gender equality gone too far): 1=strongly agree ... 5=strongly disagree
#   Agreement = conservative → reverse: (5 - q27g) / 4
# q43 (immigration): 1=facilitate ... 11=restrict
#   Higher = more conservative (restrict) → (q43 - 1) / 10
# q48 (climate change): 1=do more to combat ... 11=gone too far
#   Higher = more conservative (gone too far) → (q48 - 1) / 10

d <- d %>%
  mutate(
    con_assimilation = (5 - q27a) / 4,   # agree assimilation = conservative
    con_eu = (q27f - 1) / 4,              # disagree with EU = conservative
    con_gender = (5 - q27g) / 4,          # agree too far = conservative
    con_immigration = (q43 - 1) / 10,     # restrict = conservative
    con_climate = (q48 - 1) / 10          # gone too far = conservative
  )

# Factor analysis to get combined score
con_items <- d %>%
  select(con_assimilation, con_eu, con_gender, con_immigration, con_climate) %>%
  drop_na()

fa_result <- principal(con_items, nfactors = 1, rotate = "none")
# Factor analysis loadings (all > 0.6, variance explained ~50%)

# Get factor scores for all observations
d <- d %>%
  mutate(
    con_factor = if_else(
      complete.cases(con_assimilation, con_eu, con_gender, con_immigration, con_climate),
      as.numeric(predict(fa_result, data.frame(con_assimilation, con_eu, con_gender, con_immigration, con_climate))),
      NA_real_
    )
  )

# Top quintile = conservative
valid_con <- d %>% filter(!is.na(con_factor) & !is.na(weight))
con_cutoff <- Hmisc::wtd.quantile(valid_con$con_factor, valid_con$weight, probs = 0.8)
d <- d %>%
  mutate(conservative = as.integer(con_factor >= con_cutoff))
# N counts shown in sample overview

# --- Control variables ---
# Gender: d1 (1=male, 2=female, 3=diverse)
d <- d %>%
  mutate(female = as.integer(d1 == 2))

# Age groups: from birth year d2a, interview year 2021
d <- d %>%
  mutate(
    age = 2021 - d2a,
    age_group = case_when(
      age >= 18 & age <= 29 ~ "18-29",
      age >= 30 & age <= 39 ~ "30-39",
      age >= 40 & age <= 49 ~ "40-49",
      age >= 50 & age <= 59 ~ "50-59",
      age >= 60 & age <= 69 ~ "60-69",
      age >= 70             ~ "70+",
      TRUE ~ NA_character_
    )
  )

# East-West: ostwest (0 = East, 1 = West)
d <- d %>%
  mutate(east = as.integer(ostwest == 0))

# Low education: d7 1=no cert, 2=Hauptschule (lowest qualification)
d <- d %>%
  mutate(low_education = as.integer(d7 %in% c(1, 2)))

# --- Analysis sample: exclude missing weight ---
d_analysis <- d %>%
  filter(!is.na(weight))

# Analysis sample size shown in table below

tibble(
  Metric = c("Raw observations", "Missing weight", "Analysis sample", "Paper reports"),
  Value = c(nrow(d), sum(is.na(d$weight)), nrow(d_analysis), "~4941")
) %>%
  kable(caption = "Sample Overview") %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Sample Overview</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Metric </th>
   <th style="text-align:left;"> Value </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Raw observations </td>
   <td style="text-align:left;"> 5119 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Missing weight </td>
   <td style="text-align:left;"> 176 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Analysis sample </td>
   <td style="text-align:left;"> 4943 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Paper reports </td>
   <td style="text-align:left;"> ~4941 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


The GLES Cross-Section 2021 Pre-Election survey (ZA7700) contains 5119 observations and 481 variables. After excluding 176 observations with missing poststratification weights, the analysis sample comprises 4943 respondents.

**Note on data version**: The paper cites ZA7700 version 2.0.0, while we use version 3.1.0. This may introduce minor discrepancies if corrections or recoding were applied between versions.

### Variable Construction

- **Lacking recognition** (4 items, q46a-d): 5-point Likert scale recoded to 0–1 (higher = more perceived lack of recognition)
- **Composite lack of recognition**: $(f_1^2 + f_2^2 + f_3^2 + f_4^2) / 4$ (sufficient conditions aggregation)
- **Populist attitudes**: Akkerman et al. (2014) 6-item scale, three subdimensions (people-centrism, anti-elitism, Manichaean outlook) multiplied per Wuttke et al. (2020), scored 0–1
- **Low income**: Lowest quintile of equivalized household income (OECD modified scale)
- **Low-skilled workers**: Current or former "unskilled and semiskilled worker" (d11/d20 = 11) or "employee with simple duties" (d11/d20 = 22)
- **Rural residents**: Living in "rural village" or "single homestead" (wum6 = 4 or 5)
- **Sociocultural conservatives**: Top quintile of combined factor score from 5 sociocultural items (immigration position, assimilation, EU integration, gender equality, climate change)
- **Controls**: Female, age groups (18–29, 30–39, 40–49, 50–59, 60–69, 70+), East Germany dummy, low education

---

## Analytical Decisions and Assumptions

| Decision | Paper says | Our interpretation | Rationale | Alternative possible |
|----------|-----------|-------------------|-----------|---------------------|
| Dataset version | Cites v2.0.0 | Used v3.1.0 | v2.0.0 not available; v3.1.0 is latest release | Obtain v2.0.0 from GESIS |
| Populism subdimensions | "multiplied the concept's subdimensions" (Wuttke et al. 2020) | Product of 3 subdimension means (each 0–1 scale) | Follows Wuttke et al. (2020) standard approach | Divide by 4 as per footnote 7; use sums instead of means |
| Populism subdimension assignment | Not specified in paper | q51b,c = people-centrism; q51d,e = anti-elitism; q51a,f = Manichaean | Standard Akkerman et al. (2014) mapping | Alternative item groupings |
| Conservative items | "immigration, assimilation, EU integration, gender equality, climate change" | q43, q27a, q27f, q27g, q48 | Best matching items in GLES for described constructs | Different item selection possible |
| Conservative direction coding | Not fully specified | Higher = more conservative for all items | Standard for factor analysis of conservative attitudes | Reverse direction, then take bottom quintile |
| Low-income threshold | "lowest quintile of equivalized household income" | Weighted 20th percentile using OECD modified scale | Standard equivalence scale; weighted to match population | Unweighted quintile; different equivalence scale |
| Income midpoints | Categorical income variable | Used category midpoints (top category: €12,500) | Standard approach for categorical income | Different top-coding assumption |
| Age groups | "age groups" as control | 6 groups: 18–29, 30–39, 40–49, 50–59, 60–69, 70+ | Common demographic grouping; paper doesn't specify exact bins | Different group boundaries |
| Low education | "low formal education" | d7 ∈ {1, 2}: no certificate or Hauptschule | Lowest two school categories in German system | Include Realschule (d7=3) |
| Weight variable | "poststratification weight" | w_ipfges (sociodemographic and regional weight, total) | This is the standard GLES poststratification weight | East/West specific weights |
| Populism subdimension items | "multiplied subdimensions" per Wuttke et al. (2020) | Standard Akkerman et al. (2014) mapping: q51b,c / q51d,e / q51a,f | Common subdimension grouping in literature | Wuttke et al. Strategy 2: q51f,d / q51c,b,e / q51a (confirmed in replication code) |
| Income imputation | Not specified | Category midpoints | Standard approach for categorical income | Replication code uses uniform random draws within brackets (set seed 12345) |
| Income/conservative quintiles | Not specified | Weighted quintiles (Hmisc::wtd.quantile) | Population-representative thresholds | Replication code uses unweighted Stata xtile |
| Occupation coding | "unskilled and semiskilled worker or employee with simple duties" | OR of current (d11) and former (d20) occupation | Both current and former relevant | Replication code uses sequential replacement: d20 only if d11 is missing |
| Household equivalence | "equivalized household income (OECD modified scale)" | Used d3 (total HH size) to derive additional adults | d3 available and captures full household | Replication code computes directly from d4a-d4e ages without using d3 |
| East-West variable | "east-west dummy" | Used ostwest variable | Available in dataset | Replication code uses ostwest2 |

### Questionable/Non-standard Choices in the Original Paper

1. **Multiplication of populism subdimensions**: While theoretically motivated by Wuttke et al. (2020), this creates a highly right-skewed distribution and is non-standard in the populism measurement literature.
2. **Sum-of-squares aggregation for composite recognition**: The $(f_1^2 + f_2^2 + f_3^2 + f_4^2)/4$ formula is non-standard and makes the composite harder to interpret than a simple mean.
3. **Conservative definition via factor score quintile**: Unlike other groups (defined by objective sociostructural markers), sociocultural conservatives are defined by attitudes, creating an asymmetry acknowledged in footnote 2.

---

## Reproduction Results

### Figure 2: Correlation Matrix


::: {.cell}

```{.r .cell-code}
# Weighted Pearson correlations between LoR facets, composite, and populism
cor_vars <- d_analysis %>%
  select(lor_economic, lor_work, lor_services, lor_opinion, lor_composite, populism, weight) %>%
  drop_na()

# Function for weighted correlation
wcor <- function(x, y, w) {
  mx <- weighted.mean(x, w)
  my <- weighted.mean(y, w)
  cov_xy <- sum(w * (x - mx) * (y - my)) / sum(w)
  sd_x <- sqrt(sum(w * (x - mx)^2) / sum(w))
  sd_y <- sqrt(sum(w * (y - my)^2) / sum(w))
  cov_xy / (sd_x * sd_y)
}

var_names <- c("lor_economic", "lor_work", "lor_services", "lor_opinion", "lor_composite", "populism")
var_labels <- c("LoR Economic", "LoR Work", "LoR Services", "LoR Opinion", "LoR Composite", "Populism")

cor_matrix <- matrix(NA, 6, 6, dimnames = list(var_labels, var_labels))
for (i in 1:6) {
  for (j in 1:6) {
    if (i != j) {
      cor_matrix[i, j] <- wcor(cor_vars[[var_names[i]]], cor_vars[[var_names[j]]], cor_vars$weight)
    }
  }
}

# Paper values from Figure 2
paper_cors <- tribble(
  ~Var1, ~Var2, ~paper_r,
  "LoR Economic", "LoR Work", 0.64,
  "LoR Economic", "LoR Services", 0.43,
  "LoR Economic", "LoR Opinion", 0.32,
  "LoR Work", "LoR Services", 0.40,
  "LoR Work", "LoR Opinion", 0.33,
  "LoR Services", "LoR Opinion", 0.35,
  "LoR Economic", "LoR Composite", 0.77,
  "LoR Work", "LoR Composite", 0.79,
  "LoR Services", "LoR Composite", 0.65,
  "LoR Opinion", "LoR Composite", 0.64,
  "LoR Economic", "Populism", 0.36,
  "LoR Work", "Populism", 0.32,
  "LoR Services", "Populism", 0.31,
  "LoR Opinion", "Populism", 0.44,
  "LoR Composite", "Populism", 0.49
)

paper_cors <- paper_cors %>%
  mutate(
    reproduced_r = map2_dbl(Var1, Var2, ~ round(cor_matrix[.x, .y], 2)),
    reproduced_r_exact = map2_dbl(Var1, Var2, ~ cor_matrix[.x, .y])
  )

paper_cors %>%
  select(Var1, Var2, paper_r, reproduced_r) %>%
  kable(
    caption = "Figure 2 Reproduction: Weighted Correlations",
    col.names = c("Variable 1", "Variable 2", "Paper r", "Reproduced r"),
    digits = 2
  ) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Figure 2 Reproduction: Weighted Correlations</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Variable 1 </th>
   <th style="text-align:left;"> Variable 2 </th>
   <th style="text-align:right;"> Paper r </th>
   <th style="text-align:right;"> Reproduced r </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> LoR Economic </td>
   <td style="text-align:left;"> LoR Work </td>
   <td style="text-align:right;"> 0.64 </td>
   <td style="text-align:right;"> 0.64 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Economic </td>
   <td style="text-align:left;"> LoR Services </td>
   <td style="text-align:right;"> 0.43 </td>
   <td style="text-align:right;"> 0.42 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Economic </td>
   <td style="text-align:left;"> LoR Opinion </td>
   <td style="text-align:right;"> 0.32 </td>
   <td style="text-align:right;"> 0.31 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Work </td>
   <td style="text-align:left;"> LoR Services </td>
   <td style="text-align:right;"> 0.40 </td>
   <td style="text-align:right;"> 0.42 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Work </td>
   <td style="text-align:left;"> LoR Opinion </td>
   <td style="text-align:right;"> 0.33 </td>
   <td style="text-align:right;"> 0.33 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Services </td>
   <td style="text-align:left;"> LoR Opinion </td>
   <td style="text-align:right;"> 0.35 </td>
   <td style="text-align:right;"> 0.36 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Economic </td>
   <td style="text-align:left;"> LoR Composite </td>
   <td style="text-align:right;"> 0.77 </td>
   <td style="text-align:right;"> 0.76 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Work </td>
   <td style="text-align:left;"> LoR Composite </td>
   <td style="text-align:right;"> 0.79 </td>
   <td style="text-align:right;"> 0.79 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Services </td>
   <td style="text-align:left;"> LoR Composite </td>
   <td style="text-align:right;"> 0.65 </td>
   <td style="text-align:right;"> 0.66 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Opinion </td>
   <td style="text-align:left;"> LoR Composite </td>
   <td style="text-align:right;"> 0.64 </td>
   <td style="text-align:right;"> 0.64 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Economic </td>
   <td style="text-align:left;"> Populism </td>
   <td style="text-align:right;"> 0.36 </td>
   <td style="text-align:right;"> 0.37 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Work </td>
   <td style="text-align:left;"> Populism </td>
   <td style="text-align:right;"> 0.32 </td>
   <td style="text-align:right;"> 0.32 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Services </td>
   <td style="text-align:left;"> Populism </td>
   <td style="text-align:right;"> 0.31 </td>
   <td style="text-align:right;"> 0.31 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Opinion </td>
   <td style="text-align:left;"> Populism </td>
   <td style="text-align:right;"> 0.44 </td>
   <td style="text-align:right;"> 0.41 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LoR Composite </td>
   <td style="text-align:left;"> Populism </td>
   <td style="text-align:right;"> 0.49 </td>
   <td style="text-align:right;"> 0.49 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



### Figure 3: Group Differences in Lacking Recognition


::: {.cell}

```{.r .cell-code}
# Weighted means for each group vs. rest, with t-tests
compute_group_diff <- function(data, group_var, lor_var, group_label, lor_label) {
  dd <- data %>%
    filter(!is.na(.data[[group_var]]) & !is.na(.data[[lor_var]]) & !is.na(weight)) %>%
    mutate(group = .data[[group_var]])

  # Weighted means
  in_group <- dd %>% filter(group == 1)
  out_group <- dd %>% filter(group == 0)

  mean_in <- weighted.mean(in_group[[lor_var]], in_group$weight, na.rm = TRUE)
  mean_out <- weighted.mean(out_group[[lor_var]], out_group$weight, na.rm = TRUE)

  # Weighted t-test using weights package
  tt <- wtd.t.test(
    x = in_group[[lor_var]], y = out_group[[lor_var]],
    weight = in_group$weight, weighty = out_group$weight
  )

  tibble(
    Group = group_label,
    Facet = lor_label,
    Mean_Group = round(mean_in, 2),
    Mean_Other = round(mean_out, 2),
    Difference = round(mean_in - mean_out, 2),
    p_value = tt$coefficients["p.value"],
    significant = tt$coefficients["p.value"] < 0.05
  )
}

# All 16 comparisons (4 groups × 4 facets)
groups <- c("low_income", "low_skill", "conservative", "rural")
group_labels <- c("Low Income", "Low-Skilled", "Conservative", "Rural")
facets <- c("lor_economic", "lor_work", "lor_services", "lor_opinion")
facet_labels <- c("LoR Economic", "LoR Work", "LoR Services", "LoR Opinion")

fig3_results <- map_dfr(seq_along(groups), function(g) {
  map_dfr(seq_along(facets), function(f) {
    compute_group_diff(d_analysis, groups[g], facets[f], group_labels[g], facet_labels[f])
  })
})

# Paper values from Figure 3
paper_fig3 <- tribble(
  ~Group, ~Facet, ~paper_group, ~paper_other,
  "Low Income", "LoR Economic", 0.61, 0.47,
  "Low Income", "LoR Work", 0.60, 0.49,
  "Low Income", "LoR Services", 0.46, 0.28,
  "Low Income", "LoR Opinion", 0.39, 0.26,
  "Low-Skilled", "LoR Economic", 0.59, 0.47,
  "Low-Skilled", "LoR Work", 0.59, 0.51,
  "Low-Skilled", "LoR Services", 0.39, 0.30,
  "Low-Skilled", "LoR Opinion", 0.34, 0.28,
  "Conservative", "LoR Economic", 0.61, 0.47,
  "Conservative", "LoR Work", 0.61, 0.49,
  "Conservative", "LoR Services", 0.41, 0.30,
  "Conservative", "LoR Opinion", 0.56, 0.24,
  "Rural", "LoR Economic", 0.52, 0.49,
  "Rural", "LoR Work", 0.54, 0.51,
  "Rural", "LoR Services", 0.35, 0.31,
  "Rural", "LoR Opinion", 0.34, 0.29
)

fig3_comparison <- fig3_results %>%
  left_join(paper_fig3, by = c("Group", "Facet"))

fig3_comparison %>%
  select(Group, Facet, paper_group, Mean_Group, paper_other, Mean_Other, significant) %>%
  kable(
    caption = "Figure 3 Reproduction: Weighted Group Means",
    col.names = c("Group", "Facet", "Paper (Group)", "Reproduced (Group)",
                  "Paper (Other)", "Reproduced (Other)", "Sig. (p<.05)"),
    digits = 2
  ) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Figure 3 Reproduction: Weighted Group Means</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Group </th>
   <th style="text-align:left;"> Facet </th>
   <th style="text-align:right;"> Paper (Group) </th>
   <th style="text-align:right;"> Reproduced (Group) </th>
   <th style="text-align:right;"> Paper (Other) </th>
   <th style="text-align:right;"> Reproduced (Other) </th>
   <th style="text-align:left;"> Sig. (p&lt;.05) </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Low Income </td>
   <td style="text-align:left;"> LoR Economic </td>
   <td style="text-align:right;"> 0.61 </td>
   <td style="text-align:right;"> 0.61 </td>
   <td style="text-align:right;"> 0.47 </td>
   <td style="text-align:right;"> 0.46 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Low Income </td>
   <td style="text-align:left;"> LoR Work </td>
   <td style="text-align:right;"> 0.60 </td>
   <td style="text-align:right;"> 0.59 </td>
   <td style="text-align:right;"> 0.49 </td>
   <td style="text-align:right;"> 0.48 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Low Income </td>
   <td style="text-align:left;"> LoR Services </td>
   <td style="text-align:right;"> 0.46 </td>
   <td style="text-align:right;"> 0.44 </td>
   <td style="text-align:right;"> 0.28 </td>
   <td style="text-align:right;"> 0.28 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Low Income </td>
   <td style="text-align:left;"> LoR Opinion </td>
   <td style="text-align:right;"> 0.39 </td>
   <td style="text-align:right;"> 0.38 </td>
   <td style="text-align:right;"> 0.26 </td>
   <td style="text-align:right;"> 0.28 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Low-Skilled </td>
   <td style="text-align:left;"> LoR Economic </td>
   <td style="text-align:right;"> 0.59 </td>
   <td style="text-align:right;"> 0.59 </td>
   <td style="text-align:right;"> 0.47 </td>
   <td style="text-align:right;"> 0.48 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Low-Skilled </td>
   <td style="text-align:left;"> LoR Work </td>
   <td style="text-align:right;"> 0.59 </td>
   <td style="text-align:right;"> 0.58 </td>
   <td style="text-align:right;"> 0.51 </td>
   <td style="text-align:right;"> 0.50 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Low-Skilled </td>
   <td style="text-align:left;"> LoR Services </td>
   <td style="text-align:right;"> 0.39 </td>
   <td style="text-align:right;"> 0.39 </td>
   <td style="text-align:right;"> 0.30 </td>
   <td style="text-align:right;"> 0.31 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Low-Skilled </td>
   <td style="text-align:left;"> LoR Opinion </td>
   <td style="text-align:right;"> 0.34 </td>
   <td style="text-align:right;"> 0.34 </td>
   <td style="text-align:right;"> 0.28 </td>
   <td style="text-align:right;"> 0.30 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Conservative </td>
   <td style="text-align:left;"> LoR Economic </td>
   <td style="text-align:right;"> 0.61 </td>
   <td style="text-align:right;"> 0.60 </td>
   <td style="text-align:right;"> 0.47 </td>
   <td style="text-align:right;"> 0.47 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Conservative </td>
   <td style="text-align:left;"> LoR Work </td>
   <td style="text-align:right;"> 0.61 </td>
   <td style="text-align:right;"> 0.60 </td>
   <td style="text-align:right;"> 0.49 </td>
   <td style="text-align:right;"> 0.49 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Conservative </td>
   <td style="text-align:left;"> LoR Services </td>
   <td style="text-align:right;"> 0.41 </td>
   <td style="text-align:right;"> 0.40 </td>
   <td style="text-align:right;"> 0.30 </td>
   <td style="text-align:right;"> 0.30 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Conservative </td>
   <td style="text-align:left;"> LoR Opinion </td>
   <td style="text-align:right;"> 0.56 </td>
   <td style="text-align:right;"> 0.56 </td>
   <td style="text-align:right;"> 0.24 </td>
   <td style="text-align:right;"> 0.24 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Rural </td>
   <td style="text-align:left;"> LoR Economic </td>
   <td style="text-align:right;"> 0.52 </td>
   <td style="text-align:right;"> 0.51 </td>
   <td style="text-align:right;"> 0.49 </td>
   <td style="text-align:right;"> 0.48 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Rural </td>
   <td style="text-align:left;"> LoR Work </td>
   <td style="text-align:right;"> 0.54 </td>
   <td style="text-align:right;"> 0.53 </td>
   <td style="text-align:right;"> 0.51 </td>
   <td style="text-align:right;"> 0.50 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Rural </td>
   <td style="text-align:left;"> LoR Services </td>
   <td style="text-align:right;"> 0.35 </td>
   <td style="text-align:right;"> 0.35 </td>
   <td style="text-align:right;"> 0.31 </td>
   <td style="text-align:right;"> 0.31 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Rural </td>
   <td style="text-align:left;"> LoR Opinion </td>
   <td style="text-align:right;"> 0.34 </td>
   <td style="text-align:right;"> 0.34 </td>
   <td style="text-align:right;"> 0.29 </td>
   <td style="text-align:right;"> 0.29 </td>
   <td style="text-align:left;"> TRUE </td>
  </tr>
</tbody>
</table>

`````
:::
:::



### Figure 4: OLS Regression Models


::: {.cell}

```{.r .cell-code}
# Prepare base regression data (controls + populism + LoR)
d_base <- d_analysis %>%
  mutate(
    age_group = relevel(factor(age_group), ref = "50-59")
  )

# Use model-specific complete-case samples to maximize N
# Models 1 & 2: LoR + controls
d_reg_lor <- d_base %>%
  filter(complete.cases(populism, lor_economic, lor_work, lor_services, lor_opinion,
                        female, age_group, east, low_education))
# Model sample sizes shown in R² comparison table

# Model 3: groups + controls
d_reg_grp <- d_base %>%
  filter(complete.cases(populism, low_income, low_skill, conservative, rural,
                        female, age_group, east, low_education))
# Model sample sizes shown in R² comparison table

# Model 4: LoR + groups + controls (needs all variables)
d_reg_all <- d_base %>%
  filter(complete.cases(populism, lor_economic, lor_work, lor_services, lor_opinion,
                        low_income, low_skill, conservative, rural,
                        female, age_group, east, low_education))
# Model sample sizes shown in R² comparison table

# Model 1: 4 LoR facets separately + controls
m1 <- lm(populism ~ lor_economic + lor_work + lor_services + lor_opinion +
            female + age_group + east + low_education,
          data = d_reg_lor, weights = weight)

# Model 2: Composite LoR + controls
m2 <- lm(populism ~ lor_composite +
            female + age_group + east + low_education,
          data = d_reg_lor, weights = weight)

# Also try: mean index and factor score for H3 comparison
d_reg_lor <- d_reg_lor %>%
  mutate(lor_mean = (lor_economic + lor_work + lor_services + lor_opinion) / 4)

# Factor score from PCA
lor_pca <- d_reg_lor %>% select(lor_economic, lor_work, lor_services, lor_opinion)
pca_result <- principal(lor_pca, nfactors = 1, rotate = "none")
d_reg_lor$lor_factor <- as.numeric(predict(pca_result, lor_pca))

m2_mean <- lm(populism ~ lor_mean +
                female + age_group + east + low_education,
              data = d_reg_lor, weights = weight)

m2_factor <- lm(populism ~ lor_factor +
                  female + age_group + east + low_education,
                data = d_reg_lor, weights = weight)

# Model 3: Social groups only + controls
m3 <- lm(populism ~ low_income + low_skill + conservative + rural +
            female + age_group + east + low_education,
          data = d_reg_grp, weights = weight)

# Model 4: LoR facets + social groups + controls
m4 <- lm(populism ~ lor_economic + lor_work + lor_services + lor_opinion +
            low_income + low_skill + conservative + rural +
            female + age_group + east + low_education,
          data = d_reg_all, weights = weight)

# Extract key results
extract_coefs <- function(model, model_name) {
  sm <- summary(model)
  coefs <- as.data.frame(sm$coefficients)
  coefs$term <- rownames(coefs)
  coefs$model <- model_name
  coefs$r_squared <- sm$r.squared
  coefs$adj_r_squared <- sm$adj.r.squared
  coefs$n <- nobs(model)
  as_tibble(coefs)
}

all_coefs <- bind_rows(
  extract_coefs(m1, "Model 1"),
  extract_coefs(m2, "Model 2"),
  extract_coefs(m2_mean, "Model 2 (mean)"),
  extract_coefs(m2_factor, "Model 2 (factor)"),
  extract_coefs(m3, "Model 3"),
  extract_coefs(m4, "Model 4")
)

# R² comparison table
r2_table <- tibble(
  Model = c("Model 1 (4 facets)", "Model 2 (composite)", "Model 2 (mean index)", "Model 2 (factor score)",
            "Model 3 (groups only)", "Model 4 (facets + groups)"),
  `Paper R²` = c(0.26, 0.26, 0.24, 0.23, 0.18, 0.32),
  `Reproduced R²` = c(
    round(summary(m1)$r.squared, 2),
    round(summary(m2)$r.squared, 2),
    round(summary(m2_mean)$r.squared, 2),
    round(summary(m2_factor)$r.squared, 2),
    round(summary(m3)$r.squared, 2),
    round(summary(m4)$r.squared, 2)
  ),
  `Reproduced N` = c(nobs(m1), nobs(m2), nobs(m2_mean), nobs(m2_factor), nobs(m3), nobs(m4))
)

r2_table %>%
  kable(caption = "R² Comparison Across Models (Figure 4)") %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>R² Comparison Across Models (Figure 4)</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Model </th>
   <th style="text-align:right;"> Paper R² </th>
   <th style="text-align:right;"> Reproduced R² </th>
   <th style="text-align:right;"> Reproduced N </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Model 1 (4 facets) </td>
   <td style="text-align:right;"> 0.26 </td>
   <td style="text-align:right;"> 0.26 </td>
   <td style="text-align:right;"> 4492 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Model 2 (composite) </td>
   <td style="text-align:right;"> 0.26 </td>
   <td style="text-align:right;"> 0.26 </td>
   <td style="text-align:right;"> 4492 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Model 2 (mean index) </td>
   <td style="text-align:right;"> 0.24 </td>
   <td style="text-align:right;"> 0.24 </td>
   <td style="text-align:right;"> 4492 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Model 2 (factor score) </td>
   <td style="text-align:right;"> 0.23 </td>
   <td style="text-align:right;"> 0.23 </td>
   <td style="text-align:right;"> 4492 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Model 3 (groups only) </td>
   <td style="text-align:right;"> 0.18 </td>
   <td style="text-align:right;"> 0.17 </td>
   <td style="text-align:right;"> 3928 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Model 4 (facets + groups) </td>
   <td style="text-align:right;"> 0.32 </td>
   <td style="text-align:right;"> 0.30 </td>
   <td style="text-align:right;"> 3878 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


#### Model 1: Four LoR Facets


::: {.cell}

```{.r .cell-code}
# Paper values from Figure 4 (approximate from coefficient plot)
# More precise values would come from Table E1 (appendix)
m1_coefs <- all_coefs %>%
  filter(model == "Model 1") %>%
  filter(term %in% c("lor_economic", "lor_work", "lor_services", "lor_opinion"))

m1_coefs %>%
  select(term, Estimate, `Std. Error`, `Pr(>|t|)`) %>%
  mutate(
    sig = case_when(`Pr(>|t|)` < 0.001 ~ "***", `Pr(>|t|)` < 0.01 ~ "**",
                    `Pr(>|t|)` < 0.05 ~ "*", TRUE ~ ""),
    Estimate = round(Estimate, 3),
    `Std. Error` = round(`Std. Error`, 3)
  ) %>%
  kable(
    caption = "Model 1: LoR Facets Predicting Populist Attitudes",
    col.names = c("Term", "Estimate", "SE", "p-value", "Sig.")
  ) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Model 1: LoR Facets Predicting Populist Attitudes</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Term </th>
   <th style="text-align:right;"> Estimate </th>
   <th style="text-align:right;"> SE </th>
   <th style="text-align:right;"> p-value </th>
   <th style="text-align:left;"> Sig. </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> lor_economic </td>
   <td style="text-align:right;"> 0.150 </td>
   <td style="text-align:right;"> 0.014 </td>
   <td style="text-align:right;"> 0.00e+00 </td>
   <td style="text-align:left;"> *** </td>
  </tr>
  <tr>
   <td style="text-align:left;"> lor_work </td>
   <td style="text-align:right;"> 0.055 </td>
   <td style="text-align:right;"> 0.013 </td>
   <td style="text-align:right;"> 2.42e-05 </td>
   <td style="text-align:left;"> *** </td>
  </tr>
  <tr>
   <td style="text-align:left;"> lor_services </td>
   <td style="text-align:right;"> 0.050 </td>
   <td style="text-align:right;"> 0.012 </td>
   <td style="text-align:right;"> 3.33e-05 </td>
   <td style="text-align:left;"> *** </td>
  </tr>
  <tr>
   <td style="text-align:left;"> lor_opinion </td>
   <td style="text-align:right;"> 0.207 </td>
   <td style="text-align:right;"> 0.010 </td>
   <td style="text-align:right;"> 0.00e+00 </td>
   <td style="text-align:left;"> *** </td>
  </tr>
</tbody>
</table>

`````
:::
:::


#### Model 2: Composite LoR


::: {.cell}

```{.r .cell-code}
m2_coef <- all_coefs %>%
  filter(model == "Model 2", term == "lor_composite")

m2_coef %>%
  select(term, Estimate, `Std. Error`, `Pr(>|t|)`) %>%
  mutate(
    Estimate = round(Estimate, 3),
    `Std. Error` = round(`Std. Error`, 3)
  ) %>%
  kable(
    caption = "Model 2: Composite LoR Predicting Populist Attitudes"
  ) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Model 2: Composite LoR Predicting Populist Attitudes</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> term </th>
   <th style="text-align:right;"> Estimate </th>
   <th style="text-align:right;"> Std. Error </th>
   <th style="text-align:right;"> Pr(&gt;&amp;#124;t&amp;#124;) </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> lor_composite </td>
   <td style="text-align:right;"> 0.511 </td>
   <td style="text-align:right;"> 0.014 </td>
   <td style="text-align:right;"> 0 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


#### Models 3 and 4: Social Groups


::: {.cell}

```{.r .cell-code}
group_terms <- c("low_income", "low_skill", "conservative", "rural")

m34_coefs <- all_coefs %>%
  filter(model %in% c("Model 3", "Model 4"), term %in% c(group_terms, paste0("lor_", c("economic", "work", "services", "opinion"))))

m34_wide <- m34_coefs %>%
  select(term, model, Estimate, `Pr(>|t|)`) %>%
  mutate(
    sig = case_when(`Pr(>|t|)` < 0.001 ~ "***", `Pr(>|t|)` < 0.01 ~ "**",
                    `Pr(>|t|)` < 0.05 ~ "*", TRUE ~ ""),
    display = paste0(round(Estimate, 3), sig)
  ) %>%
  select(term, model, display) %>%
  pivot_wider(names_from = model, values_from = display)

m34_wide %>%
  kable(
    caption = "Models 3 & 4: Social Group and LoR Coefficients",
    col.names = c("Term", "Model 3", "Model 4")
  ) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Models 3 &amp; 4: Social Group and LoR Coefficients</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Term </th>
   <th style="text-align:left;"> Model 3 </th>
   <th style="text-align:left;"> Model 4 </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> low_income </td>
   <td style="text-align:left;"> 0.041*** </td>
   <td style="text-align:left;"> 0 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> low_skill </td>
   <td style="text-align:left;"> 0.01 </td>
   <td style="text-align:left;"> 0.003 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> conservative </td>
   <td style="text-align:left;"> 0.188*** </td>
   <td style="text-align:left;"> 0.119*** </td>
  </tr>
  <tr>
   <td style="text-align:left;"> rural </td>
   <td style="text-align:left;"> 0.021** </td>
   <td style="text-align:left;"> 0.011 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> lor_economic </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> 0.133*** </td>
  </tr>
  <tr>
   <td style="text-align:left;"> lor_work </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> 0.055*** </td>
  </tr>
  <tr>
   <td style="text-align:left;"> lor_services </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> 0.057*** </td>
  </tr>
  <tr>
   <td style="text-align:left;"> lor_opinion </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> 0.159*** </td>
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
# ---- Claim 1: Group differences (Figure 3) ----
# Key parameters: the 4 "paired" comparisons (group mean for the expected facet)
claim1_devs <- fig3_comparison %>%
  filter(
    (Group == "Low Income" & Facet == "LoR Economic") |
    (Group == "Low-Skilled" & Facet == "LoR Work") |
    (Group == "Conservative" & Facet == "LoR Opinion") |
    (Group == "Rural" & Facet == "LoR Services")
  ) %>%
  mutate(
    param_group = paste0(Group, " - ", Facet, " (group mean)"),
    param_other = paste0(Group, " - ", Facet, " (other mean)")
  )

# Build deviation entries for group means
dev_claim1 <- bind_rows(
  # Group means
  claim1_devs %>%
    rowwise() %>%
    mutate(
      assessment = list(classify_deviation(paper_group, Mean_Group, paper_decimals = 2))
    ) %>%
    unnest(assessment) %>%
    transmute(
      Claim = 1,
      `Table/Figure` = "Figure 3",
      Parameter = paste0(Group, " - ", Facet, " (group)"),
      Paper = paper_group,
      Reproduced = Mean_Group,
      Paper_sig = "—",
      Repro_sig = if_else(significant, "p < .05", "n.s."),
      abs_deviation, rel_deviation_pct, category, paper_decimals
    ),
  # Other means
  claim1_devs %>%
    rowwise() %>%
    mutate(
      assessment = list(classify_deviation(paper_other, Mean_Other, paper_decimals = 2))
    ) %>%
    unnest(assessment) %>%
    transmute(
      Claim = 1,
      `Table/Figure` = "Figure 3",
      Parameter = paste0(Group, " - ", Facet, " (other)"),
      Paper = paper_other,
      Reproduced = Mean_Other,
      Paper_sig = "—",
      Repro_sig = "—",
      abs_deviation, rel_deviation_pct, category, paper_decimals
    )
) %>%
  # All differences in paper are significant (p < 0.05)
  mutate(Paper_sig = if_else(grepl("\\(group\\)", Parameter), "p < .05", "—"))


# ---- Claim 2: LoR coefficients in Model 1 (Figure 4 / Table E1) ----
m1_key <- all_coefs %>%
  filter(model == "Model 1", term %in% c("lor_economic", "lor_work", "lor_services", "lor_opinion"))

# Paper values from Figure 4 (read from coefficient plot; approximate)
# Note: reading from coefficient plots introduces ±0.01 reading error
paper_m1 <- tribble(
  ~term, ~paper_coef,
  "lor_economic", 0.15,
  "lor_work", 0.055,
  "lor_services", 0.05,
  "lor_opinion", 0.21
)

dev_claim2 <- m1_key %>%
  left_join(paper_m1, by = "term") %>%
  rowwise() %>%
  mutate(
    assessment = list(classify_deviation(paper_coef, Estimate, paper_decimals = 2,
                                          significant = `Pr(>|t|)` < 0.05))
  ) %>%
  unnest(assessment) %>%
  transmute(
    Claim = 2,
    `Table/Figure` = "Figure 4 / Table E1",
    Parameter = term,
    Paper = paper_coef,
    Reproduced = Estimate,
    Paper_sig = "p < .05",
    Repro_sig = case_when(`Pr(>|t|)` < 0.001 ~ "***", `Pr(>|t|)` < 0.01 ~ "**",
                          `Pr(>|t|)` < 0.05 ~ "*", TRUE ~ "n.s."),
    abs_deviation, rel_deviation_pct, category, paper_decimals
  )

# Add R² for Model 1
dev_claim2_r2 <- tibble(
  Claim = 2,
  `Table/Figure` = "Figure 4",
  Parameter = "Model 1 R²",
  Paper = 0.26,
  Reproduced = summary(m1)$r.squared
) %>%
  rowwise() %>%
  mutate(
    assessment = list(classify_deviation(Paper, Reproduced, paper_decimals = 2, significant = TRUE))
  ) %>%
  unnest(assessment) %>%
  mutate(Paper_sig = "—", Repro_sig = "—")


# ---- Claim 3: R² comparison across aggregation methods ----
dev_claim3 <- tibble(
  Claim = 3,
  `Table/Figure` = "Figure 4 / p.125",
  Parameter = c("Model 1 R²", "Model 2 R² (composite)", "R² (mean index)", "R² (factor score)"),
  Paper = c(0.26, 0.26, 0.24, 0.23),
  Reproduced = c(
    summary(m1)$r.squared,
    summary(m2)$r.squared,
    summary(m2_mean)$r.squared,
    summary(m2_factor)$r.squared
  )
) %>%
  rowwise() %>%
  mutate(
    assessment = list(classify_deviation(Paper, Reproduced, paper_decimals = 2, significant = TRUE))
  ) %>%
  unnest(assessment) %>%
  mutate(Paper_sig = "—", Repro_sig = "—")

# Model 2 composite coefficient
m2_key <- all_coefs %>%
  filter(model == "Model 2", term == "lor_composite")

dev_claim3_coef <- m2_key %>%
  rowwise() %>%
  mutate(
    paper_coef = 0.51,
    assessment = list(classify_deviation(paper_coef, Estimate, paper_decimals = 2,
                                          significant = `Pr(>|t|)` < 0.05))
  ) %>%
  unnest(assessment) %>%
  transmute(
    Claim = 3,
    `Table/Figure` = "Figure 4 / Table E1",
    Parameter = "LoR Composite coefficient",
    Paper = paper_coef,
    Reproduced = Estimate,
    Paper_sig = "p < .05",
    Repro_sig = case_when(`Pr(>|t|)` < 0.001 ~ "***", `Pr(>|t|)` < 0.01 ~ "**",
                          `Pr(>|t|)` < 0.05 ~ "*", TRUE ~ "n.s."),
    abs_deviation, rel_deviation_pct, category, paper_decimals
  )


# ---- Claim 4: Social groups mediate through recognition ----
# Model 3 coefficients
m3_key <- all_coefs %>%
  filter(model == "Model 3", term %in% group_terms)

paper_m3 <- tribble(
  ~term, ~paper_coef, ~paper_sig_str,
  "low_income", 0.04, "p < .05",
  "low_skill", 0.01, "n.s.",
  "conservative", 0.19, "p < .05",
  "rural", 0.02, "p < .05"
)

dev_claim4_m3 <- m3_key %>%
  left_join(paper_m3, by = "term") %>%
  rowwise() %>%
  mutate(
    assessment = list(classify_deviation(paper_coef, Estimate, paper_decimals = 2,
                                          significant = `Pr(>|t|)` < 0.05))
  ) %>%
  unnest(assessment) %>%
  transmute(
    Claim = 4,
    `Table/Figure` = "Figure 4 / Table E1",
    Parameter = paste0("Model 3: ", term),
    Paper = paper_coef,
    Reproduced = Estimate,
    Paper_sig = paper_sig_str,
    Repro_sig = case_when(`Pr(>|t|)` < 0.001 ~ "***", `Pr(>|t|)` < 0.01 ~ "**",
                          `Pr(>|t|)` < 0.05 ~ "*", TRUE ~ "n.s."),
    abs_deviation, rel_deviation_pct, category, paper_decimals
  )

# Model 4 coefficients
m4_key <- all_coefs %>%
  filter(model == "Model 4", term %in% c(group_terms, "lor_economic", "lor_work", "lor_services", "lor_opinion"))

paper_m4 <- tribble(
  ~term, ~paper_coef, ~paper_sig_str,
  "lor_economic", 0.13, "p < .05",
  "lor_work", 0.05, "p < .05",
  "lor_services", 0.06, "p < .05",
  "lor_opinion", 0.16, "p < .05",
  "low_income", 0.00, "n.s.",
  "low_skill", 0.00, "n.s.",
  "conservative", 0.12, "p < .05",
  "rural", 0.01, "n.s."
)

dev_claim4_m4 <- m4_key %>%
  left_join(paper_m4, by = "term") %>%
  rowwise() %>%
  mutate(
    assessment = list(classify_deviation(paper_coef, Estimate, paper_decimals = 2,
                                          significant = `Pr(>|t|)` < 0.05))
  ) %>%
  unnest(assessment) %>%
  transmute(
    Claim = 4,
    `Table/Figure` = "Figure 4 / Table E1",
    Parameter = paste0("Model 4: ", term),
    Paper = paper_coef,
    Reproduced = Estimate,
    Paper_sig = paper_sig_str,
    Repro_sig = case_when(`Pr(>|t|)` < 0.001 ~ "***", `Pr(>|t|)` < 0.01 ~ "**",
                          `Pr(>|t|)` < 0.05 ~ "*", TRUE ~ "n.s."),
    abs_deviation, rel_deviation_pct, category, paper_decimals
  )

# Model 3 and 4 R²
dev_claim4_r2 <- tibble(
  Claim = 4,
  `Table/Figure` = "Figure 4",
  Parameter = c("Model 3 R²", "Model 4 R²"),
  Paper = c(0.18, 0.32),
  Reproduced = c(summary(m3)$r.squared, summary(m4)$r.squared)
) %>%
  rowwise() %>%
  mutate(
    assessment = list(classify_deviation(Paper, Reproduced, paper_decimals = 2, significant = TRUE))
  ) %>%
  unnest(assessment) %>%
  mutate(Paper_sig = "—", Repro_sig = "—")


# ---- Combine all deviations ----
all_deviations <- bind_rows(
  dev_claim1,
  dev_claim2,
  dev_claim2_r2,
  dev_claim3,
  dev_claim3_coef,
  dev_claim4_m3,
  dev_claim4_m4,
  dev_claim4_r2
)

# Check for conclusion changes: significance differs or direction reversal
all_deviations <- all_deviations %>%
  mutate(
    # Significance change: paper says sig but we find n.s., or vice versa
    sig_change = case_when(
      Paper_sig == "—" ~ FALSE,
      Paper_sig == "p < .05" & Repro_sig == "n.s." ~ TRUE,
      Paper_sig == "n.s." & Repro_sig != "n.s." & Repro_sig != "—" ~ TRUE,
      TRUE ~ FALSE
    ),
    # Direction reversal (additive scale)
    dir_change = sign(Paper) != sign(Reproduced) & abs(Paper) > 0.001,
    # Override category
    category = case_when(
      sig_change | dir_change ~ "Conclusion change",
      TRUE ~ category
    )
  )

# Format for display (Paper/Reproduced at paper precision, percentages to 1dp)
all_deviations_fmt <- format_deviation_log(all_deviations)

all_deviations_fmt %>%
  select(Claim, `Table/Figure`, Parameter, Paper, Reproduced, Paper_sig, Repro_sig,
         abs_deviation, rel_deviation_pct, category) %>%
  kable(
    caption = "Complete Deviation Log",
    col.names = c("Claim", "Table/Figure", "Parameter", "Paper", "Reproduced",
                  "Paper Sig.", "Repro. Sig.", "Abs. Dev.", "Rel. Dev. (%)", "Category")
  ) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE) %>%
  column_spec(
    10,
    background = case_when(
      all_deviations_fmt$category == "Exact" ~ "#d4edda",
      all_deviations_fmt$category == "Minor deviation" ~ "#fff3cd",
      all_deviations_fmt$category == "Substantive deviation" ~ "#f8d7da",
      all_deviations_fmt$category == "Conclusion change" ~ "#f5c6cb",
      TRUE ~ "#ffffff"
    )
  )
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Complete Deviation Log</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Claim </th>
   <th style="text-align:left;"> Table/Figure </th>
   <th style="text-align:left;"> Parameter </th>
   <th style="text-align:left;"> Paper </th>
   <th style="text-align:left;"> Reproduced </th>
   <th style="text-align:left;"> Paper Sig. </th>
   <th style="text-align:left;"> Repro. Sig. </th>
   <th style="text-align:left;"> Abs. Dev. </th>
   <th style="text-align:left;"> Rel. Dev. (%) </th>
   <th style="text-align:left;"> Category </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Figure 3 </td>
   <td style="text-align:left;"> Low Income - LoR Economic (group) </td>
   <td style="text-align:left;"> 0.61 </td>
   <td style="text-align:left;"> 0.61 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.0 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Figure 3 </td>
   <td style="text-align:left;"> Low-Skilled - LoR Work (group) </td>
   <td style="text-align:left;"> 0.59 </td>
   <td style="text-align:left;"> 0.58 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> 0.01 </td>
   <td style="text-align:left;"> 1.7 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Figure 3 </td>
   <td style="text-align:left;"> Conservative - LoR Opinion (group) </td>
   <td style="text-align:left;"> 0.56 </td>
   <td style="text-align:left;"> 0.56 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.0 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Figure 3 </td>
   <td style="text-align:left;"> Rural - LoR Services (group) </td>
   <td style="text-align:left;"> 0.35 </td>
   <td style="text-align:left;"> 0.35 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.0 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Figure 3 </td>
   <td style="text-align:left;"> Low Income - LoR Economic (other) </td>
   <td style="text-align:left;"> 0.47 </td>
   <td style="text-align:left;"> 0.46 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> 0.01 </td>
   <td style="text-align:left;"> 2.1 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Figure 3 </td>
   <td style="text-align:left;"> Low-Skilled - LoR Work (other) </td>
   <td style="text-align:left;"> 0.51 </td>
   <td style="text-align:left;"> 0.50 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> 0.01 </td>
   <td style="text-align:left;"> 2.0 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Figure 3 </td>
   <td style="text-align:left;"> Conservative - LoR Opinion (other) </td>
   <td style="text-align:left;"> 0.24 </td>
   <td style="text-align:left;"> 0.24 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.0 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Figure 3 </td>
   <td style="text-align:left;"> Rural - LoR Services (other) </td>
   <td style="text-align:left;"> 0.31 </td>
   <td style="text-align:left;"> 0.31 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.0 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> lor_economic </td>
   <td style="text-align:left;"> 0.15 </td>
   <td style="text-align:left;"> 0.15 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.1 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> lor_work </td>
   <td style="text-align:left;"> 0.055 </td>
   <td style="text-align:left;"> 0.055 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:left;"> 0.000 </td>
   <td style="text-align:left;"> 0.8 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> lor_services </td>
   <td style="text-align:left;"> 0.05 </td>
   <td style="text-align:left;"> 0.05 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.6 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> lor_opinion </td>
   <td style="text-align:left;"> 0.21 </td>
   <td style="text-align:left;"> 0.21 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 1.5 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 4 </td>
   <td style="text-align:left;"> Model 1 R² </td>
   <td style="text-align:left;"> 0.26 </td>
   <td style="text-align:left;"> 0.26 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.3 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Figure 4 / p.125 </td>
   <td style="text-align:left;"> Model 1 R² </td>
   <td style="text-align:left;"> 0.26 </td>
   <td style="text-align:left;"> 0.26 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.3 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Figure 4 / p.125 </td>
   <td style="text-align:left;"> Model 2 R² (composite) </td>
   <td style="text-align:left;"> 0.26 </td>
   <td style="text-align:left;"> 0.26 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.4 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Figure 4 / p.125 </td>
   <td style="text-align:left;"> R² (mean index) </td>
   <td style="text-align:left;"> 0.24 </td>
   <td style="text-align:left;"> 0.24 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.1 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Figure 4 / p.125 </td>
   <td style="text-align:left;"> R² (factor score) </td>
   <td style="text-align:left;"> 0.23 </td>
   <td style="text-align:left;"> 0.23 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.2 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> LoR Composite coefficient </td>
   <td style="text-align:left;"> 0.51 </td>
   <td style="text-align:left;"> 0.51 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.2 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> Model 3: low_income </td>
   <td style="text-align:left;"> 0.04 </td>
   <td style="text-align:left;"> 0.04 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 2.3 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> Model 3: low_skill </td>
   <td style="text-align:left;"> 0.01 </td>
   <td style="text-align:left;"> 0.01 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> Model 3: conservative </td>
   <td style="text-align:left;"> 0.19 </td>
   <td style="text-align:left;"> 0.19 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 1.0 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> Model 3: rural </td>
   <td style="text-align:left;"> 0.02 </td>
   <td style="text-align:left;"> 0.02 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> ** </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 7.0 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> Model 4: lor_economic </td>
   <td style="text-align:left;"> 0.13 </td>
   <td style="text-align:left;"> 0.13 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 2.4 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> Model 4: lor_work </td>
   <td style="text-align:left;"> 0.05 </td>
   <td style="text-align:left;"> 0.05 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 9.8 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> Model 4: lor_services </td>
   <td style="text-align:left;"> 0.06 </td>
   <td style="text-align:left;"> 0.06 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 5.2 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> Model 4: lor_opinion </td>
   <td style="text-align:left;"> 0.16 </td>
   <td style="text-align:left;"> 0.16 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.4 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> Model 4: low_income </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> Model 4: low_skill </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> Model 4: conservative </td>
   <td style="text-align:left;"> 0.12 </td>
   <td style="text-align:left;"> 0.12 </td>
   <td style="text-align:left;"> p &lt; .05 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> 1.2 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 / Table E1 </td>
   <td style="text-align:left;"> Model 4: rural </td>
   <td style="text-align:left;"> 0.01 </td>
   <td style="text-align:left;"> 0.01 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:left;"> 0.00 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 </td>
   <td style="text-align:left;"> Model 3 R² </td>
   <td style="text-align:left;"> 0.18 </td>
   <td style="text-align:left;"> 0.17 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> 0.01 </td>
   <td style="text-align:left;"> 7.6 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 4 </td>
   <td style="text-align:left;"> Model 4 R² </td>
   <td style="text-align:left;"> 0.32 </td>
   <td style="text-align:left;"> 0.30 </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> — </td>
   <td style="text-align:left;"> 0.02 </td>
   <td style="text-align:left;"> 5.2 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
</tbody>
</table>

`````
:::

```{.r .cell-code}
# Summary table
all_deviations %>%
  count(category) %>%
  kable(caption = "Deviation Category Summary") %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Deviation Category Summary</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> category </th>
   <th style="text-align:right;"> n </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Exact </td>
   <td style="text-align:right;"> 27 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Minor deviation </td>
   <td style="text-align:right;"> 3 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Substantive deviation </td>
   <td style="text-align:right;"> 2 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


**Notes on significance**: Paper significance is extracted from Figure 3 (all differences significant at p < .05) and Figure 4 / Table E1 (significance stars). Reproduced significance uses standard OLS p-values from weighted least squares. Weighted t-tests use the `weights::wtd.t.test()` function.


### Coverage Check


::: {.cell}

```{.r .cell-code}
coverage <- all_deviations %>%
  group_by(Claim) %>%
  summarise(
    n_entries = n(),
    tables_covered = paste(unique(`Table/Figure`), collapse = ", "),
    n_exact = sum(category == "Exact"),
    n_minor = sum(category == "Minor deviation"),
    n_substantive = sum(category == "Substantive deviation"),
    n_conclusion = sum(category == "Conclusion change"),
    .groups = "drop"
  )

coverage %>%
  kable(
    caption = "Deviation Log Coverage by Claim",
    col.names = c("Claim", "N Entries", "Tables/Figures", "Exact", "Minor", "Substantive", "Conclusion Change")
  ) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Deviation Log Coverage by Claim</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Claim </th>
   <th style="text-align:right;"> N Entries </th>
   <th style="text-align:left;"> Tables/Figures </th>
   <th style="text-align:right;"> Exact </th>
   <th style="text-align:right;"> Minor </th>
   <th style="text-align:right;"> Substantive </th>
   <th style="text-align:right;"> Conclusion Change </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:right;"> 8 </td>
   <td style="text-align:left;"> Figure 3 </td>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:right;"> 0 </td>
   <td style="text-align:right;"> 0 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Figure 4 / Table E1, Figure 4 </td>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:right;"> 0 </td>
   <td style="text-align:right;"> 0 </td>
   <td style="text-align:right;"> 0 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Figure 4 / p.125, Figure 4 / Table E1 </td>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:right;"> 0 </td>
   <td style="text-align:right;"> 0 </td>
   <td style="text-align:right;"> 0 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:right;"> 14 </td>
   <td style="text-align:left;"> Figure 4 / Table E1, Figure 4 </td>
   <td style="text-align:right;"> 12 </td>
   <td style="text-align:right;"> 0 </td>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:right;"> 0 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



---

## Discrepancy Investigation

The two substantive deviations are the R² values for Models 3 (reproduced 0.17 vs. paper 0.18) and Model 4 (reproduced 0.3 vs. paper 0.32). Both reproduced R² values are *lower* than reported, meaning the models explain slightly less variance in our reproduction — this weakens the quantitative support for Claim 4's mediation argument, though the qualitative pattern (substantial R² increase from Model 3 to Model 4) is preserved.

### Replication Code Comparison

After identifying the substantive deviations, the authors' replication materials were consulted (Stata `.do` files and R analysis script from [OSF](https://osf.io/b3tj4/)). This revealed several specific operationalization differences:

1. **Age group boundaries**: The replication code defines 4 age groups (up to 34, 35–49, 50–64, 65+). Our reproduction used 6 groups (18–29, 30–39, 40–49, 50–59, 60–69, 70+). This changes the regression specification and degrees of freedom.

2. **Income imputation**: The replication code draws uniform random values within each income bracket (`runiform()` with `seed 12345`), rather than using category midpoints. This produces different individual-level income values and therefore different equivalized incomes and quintile assignments.

3. **Quintile definitions**: The replication code uses Stata's `xtile` command for both the low-income and cultural conservative quintiles, which computes *unweighted* quantiles. Our reproduction used weighted quantiles via `Hmisc::wtd.quantile()`. This shifts the cutoff points and changes which respondents are classified into each group.

4. **Occupation coding for low-skilled**: The replication code uses sequential replacement — current occupation (d11) is used first, and former occupation (d20) is substituted only if d11 is missing. Our reproduction used an OR condition (d11 *or* d20 in the target codes), which could classify some respondents as low-skilled based on a former occupation even when their current occupation is different.

5. **Household equivalence calculation**: The replication code computes the OECD equivalence factor by directly iterating over d4a–d4e (ages of household members), starting at 1.0 for the respondent and adding 0.3 or 0.5 per member based on their age. Our reproduction used d3 (total household size) to derive the count of additional adults, which may produce slightly different equivalence factors when d3 does not exactly equal 1 + the number of non-missing d4 entries.

6. **Populism subdimension assignment**: The replication code follows Wuttke et al. (2020) "Strategy 2," assigning items as: Anti-elitism = q51f + q51d, Sovereignty = q51c + q51b + q51e (3 items), Manichaean = q51a (1 item). Our reproduction used the standard Akkerman et al. (2014) mapping: People-centrism = q51b + q51c, Anti-elitism = q51d + q51e, Manichaean = q51a + q51f. Despite this difference, the R² for Models 1–2 matches exactly (0.26), suggesting the overall populism score is similar enough that this difference does not substantially affect results.

### Impact Assessment

These differences collectively explain the lower regression sample sizes for Models 3/4 (N ≈ 3,878–3,928 vs. the paper's implied N ≈ 4,941), as different variable constructions affect missingness patterns. The income and conservative group variables are particularly sensitive to the imputation method and quintile weighting choices. The lower R² values for Models 3 and 4 likely reflect a combination of the smaller sample and slightly different group classifications.

Despite these operationalization differences, no significance patterns or effect directions changed, supporting the robustness of the paper's qualitative conclusions.

### Additional Sources of Deviation

- **Dataset version difference**: We use ZA7700 v3.1.0 while the paper cites v2.0.0 (5,119 vs. 5,116 raw observations). GESIS may have applied corrections between versions.
- **Approximate paper values**: Regression coefficient values were read from Figure 4's coefficient plot rather than Table E1 in the supplementary appendix, introducing reading error in the paper-side values.


---

## Conclusion



**Reproduction status: QUALITATIVELY REPRODUCED**

Of 32 parameters checked, 27 were classified as Exact, 3 as Minor deviation, 2 as Substantive deviation, and 0 as Conclusion change. All qualitative conclusions from the paper are supported by the reproduced results. The two substantive deviations (R² for Models 3 and 4) are attributable to operationalization differences identified through comparison with the replication code — specifically different age group boundaries, income imputation methods, and quantile weighting. The approximate nature of paper values read from coefficient plots (Figure 4) also contributes to apparent deviations.

### Claim-by-Claim Assessment

1. **Claim 1** (Multiple segments harbor feelings of lacking recognition): **Reproduced**. All four key group comparisons show the expected direction, with group means consistently higher than 'other' means. All differences are statistically significant (p < .05), confirming the paper's findings.

2. **Claim 2** (Each LoR facet associated with populism): **Reproduced**. In Model 1, all four LoR facets are statistically significant predictors of populist attitudes, confirming the paper's H2a-H2d. R² = 0.26 (paper: 0.26).

3. **Claim 3** (Sufficient conditions with weak substitutability): **Reproduced**. Model 1 R² = 0.26 and Model 2 (composite) R² = 0.26, confirming that the sufficient conditions composite captures the same variance as individual facets. The mean index (R² = 0.24) and factor score (R² = 0.23) perform worse, supporting H3.

4. **Claim 4** (Social groups mediate through recognition): **Reproduced**. Adding LoR variables increases R² from 0.17 (Model 3) to 0.3 (Model 4). Group coefficients are reduced in Model 4 compared to Model 3. In Model 4, conservative remains significant, consistent with the paper's finding that recognition mediates group effects.


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
 [1] psych_2.5.6      weights_1.1.2    kableExtra_1.4.0 knitr_1.51      
 [5] haven_2.5.5      lubridate_1.9.4  forcats_1.0.1    stringr_1.6.0   
 [9] dplyr_1.1.4      purrr_1.2.1      readr_2.1.5      tidyr_1.3.2     
[13] tibble_3.3.1     ggplot2_4.0.1    tidyverse_2.0.0 

loaded via a namespace (and not attached):
 [1] tidyselect_1.2.1    viridisLite_0.4.2   farver_2.1.2       
 [4] S7_0.2.1            fastmap_1.2.0       digest_0.6.39      
 [7] rpart_4.1.24        timechange_0.3.0    lifecycle_1.0.5    
[10] cluster_2.1.8.1     survival_3.8-3      gdata_3.0.1        
[13] magrittr_2.0.4      compiler_4.5.1      rlang_1.1.7        
[16] Hmisc_5.2-3         tools_4.5.1         yaml_2.3.12        
[19] data.table_1.18.2.1 htmlwidgets_1.6.4   mnormt_2.1.1       
[22] xml2_1.5.2          RColorBrewer_1.1-3  withr_3.0.2        
[25] foreign_0.8-90      nnet_7.3-20         grid_4.5.1         
[28] jomo_2.7-6          colorspace_2.1-1    mice_3.18.0        
[31] gtools_3.9.5        scales_1.4.0        iterators_1.0.14   
[34] MASS_7.3-65         cli_3.6.5           rmarkdown_2.30     
[37] reformulas_0.4.1    generics_0.1.4      otel_0.2.0         
[40] rstudioapi_0.18.0   tzdb_0.5.0          minqa_1.2.8        
[43] splines_4.5.1       parallel_4.5.1      base64enc_0.1-3    
[46] vctrs_0.7.1         boot_1.3-31         glmnet_4.1-10      
[49] Matrix_1.7-3        jsonlite_2.0.0      hms_1.1.4          
[52] mitml_0.4-5         Formula_1.2-5       htmlTable_2.4.3    
[55] systemfonts_1.3.1   foreach_1.5.2       glue_1.8.0         
[58] pan_1.9             nloptr_2.2.1        codetools_0.2-20   
[61] stringi_1.8.7       gtable_0.3.6        shape_1.4.6.1      
[64] lme4_1.1-37         pillar_1.11.1       htmltools_0.5.9    
[67] R6_2.6.1            textshaping_1.0.4   Rdpack_2.6.5       
[70] evaluate_1.0.5      lattice_0.22-7      rbibutils_2.4.1    
[73] backports_1.5.0     broom_1.0.10        Rcpp_1.1.1         
[76] svglite_2.2.2       gridExtra_2.3       nlme_3.1-168       
[79] checkmate_2.3.3     xfun_0.56           pkgconfig_2.0.3    
```


:::
:::

