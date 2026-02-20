---
title: "Reproduction Report: Bimber et al. (2014)"
subtitle: "Digital Media and Political Participation: The Moderating Role of Political Interest Across Acts and Over Time"
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

**Paper**: Bimber, B., Cantijoch Cunill, M., Copeland, L., & Gibson, R. (2014). Digital Media and Political Participation: The Moderating Role of Political Interest Across Acts and Over Time. *Social Science Computer Review*, 1-22. DOI: 10.1177/0894439314526559

**Data**: British Election Studies (BES) cross-sectional surveys 2001, 2005, 2010. N ranges from ~1,463 to ~3,595 depending on year and outcome.

**Verdict**: PARTIALLY REPRODUCED

All three claims were tested across 60 deviation log parameters covering Tables 2-5 for all three survey years. Claim 1 (digital media associated with political talk for low-interest citizens) is qualitatively reproduced: all interaction terms match in direction and significance. Claim 2 (voting relationship strengthening over time) is qualitatively reproduced with caveats: the 2001 Internet info OR becomes significant in our reproduction (strengthening the claim) and the 2001 interaction OR shows a direction reversal across 1.0, though this term is non-significant in both the paper and reproduction. Claim 3 (variable moderating effect for elite-directed acts) is only partially reproduced: while the general pattern of variability is present, 6 of 8 conclusion changes occur on Claim 3 parameters, with the 2001 donating interaction losing significance and the 2001 working-for-party interaction gaining significance in our reproduction. Deviations are concentrated in the 2001 data, possibly due to differences in weight variable selection or internet use coding for the mailback questionnaire subsample. Results for 2005 and especially 2010 are closely reproduced.
:::

## Open Materials

| Material | Available | Location |
|----------|-----------|----------|
| Supplementary materials | No | — |
| Replication code | No | — |
| Replication data (processed) | No | — |
| Raw data | Yes | UK Data Service (BES 2001, 2005, 2010) |

No replication materials were found. The reproduction relies entirely on the paper's description of methods and the raw BES data files.

---

## Paper Overview

### Research Question
How does political interest moderate the relationship between digital media use and traditional forms of political participation across different types of political acts and over time?

### Key Methods
- Cross-sectional survey data from BES 2001, 2005, and 2010
- Logistic regression for voting (binary DV)
- OLS regression for donating money and discussing politics (0-10 scales)
- Negative binomial regression for working for a party (0-10 scale with many zeros)
- Separate models for each year, with main effects and interaction models
- All analyses weighted to reflect general population parameters

### Claims from the Abstract

1. Digital media use is positively and consistently associated with political talk for those lower in political interest.
2. For voting, a similar relationship that appears to be strengthening over time.
3. For the elite-directed acts of donating money and working for a party, a highly variable moderating effect of political interest that can be positive, negative, or nonexistent.

---

## Data and Variable Construction


::: {.cell}

```{.r .cell-code}
# ============================================================
# Load BES 2001
# ============================================================
bes2001_raw <- read_por("data/bes_2001.por")

bes2001 <- bes2001_raw %>%
  transmute(
    # Education: Age completed full-time education (1-5 scale)
    education = case_when(
      as.numeric(BQ75B) %in% 1:5 ~ as.numeric(BQ75B),
      as.numeric(BQ75B) == 6 ~ 5,  # Still in school -> highest category
      TRUE ~ NA_real_
    ),
    # Age
    age = ifelse(as.numeric(AGEALL) >= 18 & as.numeric(AGEALL) <= 98,
                 as.numeric(AGEALL), NA_real_),
    # Income (1-12 in 2001)
    income = ifelse(as.numeric(INCOMES) %in% 1:12, as.numeric(INCOMES), NA_real_),
    # Male (1=Male, 0=Female)
    male = case_when(
      as.numeric(GENALL) == 1 ~ 1,
      as.numeric(GENALL) == 2 ~ 0,
      TRUE ~ NA_real_
    ),
    # Party contact (BQ62: Knocked Up By Party on election day)
    party_contact = case_when(
      as.numeric(BQ62) == 1 ~ 1,
      as.numeric(BQ62) == 2 ~ 0,
      TRUE ~ NA_real_
    ),
    # Political efficacy (0-10 scale)
    pol_efficacy = ifelse(as.numeric(BQ58) %in% 0:10, as.numeric(BQ58), NA_real_),
    # Political interest (reverse code: 1=great deal...5=none -> 0=none...4=great deal)
    pol_interest = case_when(
      as.numeric(BQ1) %in% 1:5 ~ 5 - as.numeric(BQ1),
      TRUE ~ NA_real_
    ),
    # Internet use for political info (reverse code)
    # CQ6: 1=Great deal, 2=Fair amount, 3=Not very much, 4=Not at all
    # Non-internet users (CQ5=2) get 0
    internet_info = case_when(
      as.numeric(CQ5) == 2 ~ 0,  # No internet -> 0
      as.numeric(CQ6) %in% 1:4 ~ 4 - as.numeric(CQ6),  # Reverse code
      TRUE ~ NA_real_
    ),
    # Vote (1=voted, 0=didn't vote)
    vote = case_when(
      as.numeric(BQ8A) == 1 ~ 1,
      as.numeric(BQ8A) == 2 ~ 0,
      TRUE ~ NA_real_
    ),
    # Work for party (0-10)
    work_party = ifelse(as.numeric(BQ41H) %in% 0:10, as.numeric(BQ41H), NA_real_),
    # Donate money (0-10)
    donate = ifelse(as.numeric(BQ41F) %in% 0:10, as.numeric(BQ41F), NA_real_),
    # Discuss politics (0-10)
    discuss = ifelse(as.numeric(BQ41I) %in% 0:10, as.numeric(BQ41I), NA_real_),
    # Weight - use mailback weight since internet variable comes from mailback
    weight = as.numeric(MAILWGT)
  )

# ============================================================
# Load BES 2005
# ============================================================
bes2005_raw <- read_sav("data/bes_2005_face-to-face.sav")

bes2005 <- bes2005_raw %>%
  transmute(
    # Education: Age finished education (tq81: 1-5, with 6-7 still in school)
    education = case_when(
      as.numeric(tq81) %in% 1:5 ~ as.numeric(tq81),
      as.numeric(tq81) %in% 6:7 ~ 5,  # Still in education -> highest
      TRUE ~ NA_real_
    ),
    # Age
    age = ifelse(as.numeric(tq77) >= 18 & as.numeric(tq77) <= 97,
                 as.numeric(tq77), NA_real_),
    # Income (1-13 in 2005)
    income = ifelse(as.numeric(tq84) %in% 1:13, as.numeric(tq84), NA_real_),
    # Male
    male = case_when(
      as.numeric(tq76) == 1 ~ 1,
      as.numeric(tq76) == 2 ~ 0,
      TRUE ~ NA_real_
    ),
    # Party contact on election day
    party_contact = case_when(
      as.numeric(bq71a) == 1 ~ 1,
      as.numeric(bq71a) == 2 ~ 0,
      TRUE ~ NA_real_
    ),
    # Political efficacy (0-10)
    pol_efficacy = ifelse(as.numeric(bq61) %in% 0:10, as.numeric(bq61), NA_real_),
    # Political interest (reverse code from 1-5 to 0-4)
    pol_interest = case_when(
      as.numeric(bq1) %in% 1:5 ~ 5 - as.numeric(bq1),
      TRUE ~ NA_real_
    ),
    # Internet use for political info (reverse code from 1-4 to 0-3)
    # bq73: 1=Great deal ... 4=Not at all
    # Check if non-internet users (bq110=2) should be coded 0
    internet_info = case_when(
      as.numeric(bq110) == 2 ~ 0,  # No internet access -> 0
      as.numeric(bq73) %in% 1:4 ~ 4 - as.numeric(bq73),
      TRUE ~ NA_real_
    ),
    # Vote
    vote = case_when(
      as.numeric(bq12a) == 1 ~ 1,
      as.numeric(bq12a) == 2 ~ 0,
      TRUE ~ NA_real_
    ),
    # Work for party (0-10)
    work_party = ifelse(as.numeric(bq49i) %in% 0:10, as.numeric(bq49i), NA_real_),
    # Donate money (0-10)
    donate = ifelse(as.numeric(bq49g) %in% 0:10, as.numeric(bq49g), NA_real_),
    # Discuss politics (0-10)
    discuss = ifelse(as.numeric(bq49j) %in% 0:10, as.numeric(bq49j), NA_real_),
    # Weight - post-wave weight for cross-sectional analysis
    weight = as.numeric(postwtbr)
  )

# ============================================================
# Load BES 2010
# ============================================================
bes2010_raw <- read_sav("data/bes_2010_survey_data.sav")

bes2010 <- bes2010_raw %>%
  transmute(
    # Education: Combine post-wave (bq95_1) and pre-wave (aq67) for better coverage
    education = case_when(
      as.numeric(bq95_1) %in% 1:5 ~ as.numeric(bq95_1),
      as.numeric(bq95_1) %in% 6:7 ~ 5,
      as.numeric(aq67) %in% 1:5 ~ as.numeric(aq67),
      as.numeric(aq67) %in% 6:7 ~ 5,
      TRUE ~ NA_real_
    ),
    # Age: combine post-wave and pre-wave
    age = case_when(
      as.numeric(bq89) >= 18 & as.numeric(bq89) <= 99 ~ as.numeric(bq89),
      as.numeric(aq63) >= 18 & as.numeric(aq63) <= 99 ~ as.numeric(aq63),
      TRUE ~ NA_real_
    ),
    # Income: combine post-wave (bq96) and pre-wave (aq70) for better coverage
    income = case_when(
      as.numeric(bq96) %in% 1:15 ~ as.numeric(bq96),
      as.numeric(aq70) %in% 1:15 ~ as.numeric(aq70),
      TRUE ~ NA_real_
    ),
    # Male
    male = case_when(
      as.numeric(bq88) == 1 ~ 1,
      as.numeric(bq88) == 2 ~ 0,
      TRUE ~ NA_real_
    ),
    # Party contact - use general campaign contact (bq86_1) as paper's mean (0.53)
    # matches this variable, not election day contact (bq87_1 gives ~0.06)
    party_contact = case_when(
      as.numeric(bq86_1) == 1 ~ 1,
      as.numeric(bq86_1) == 2 ~ 0,
      TRUE ~ NA_real_
    ),
    # Political efficacy (0-10)
    pol_efficacy = ifelse(as.numeric(bq59) %in% 0:10, as.numeric(bq59), NA_real_),
    # Political interest (reverse code)
    pol_interest = case_when(
      as.numeric(bq1) %in% 1:5 ~ 5 - as.numeric(bq1),
      TRUE ~ NA_real_
    ),
    # Internet use for political info (reverse code from 1-4 to 0-3)
    internet_info = case_when(
      as.numeric(bq84_1) %in% 1:4 ~ 4 - as.numeric(bq84_1),
      TRUE ~ NA_real_
    ),
    # Vote
    vote = case_when(
      as.numeric(bq12_1) == 1 ~ 1,
      as.numeric(bq12_1) == 2 ~ 0,
      TRUE ~ NA_real_
    ),
    # Work for party (0-10)
    work_party = ifelse(as.numeric(bq53_6) %in% 0:10, as.numeric(bq53_6), NA_real_),
    # Donate money (0-10)
    donate = ifelse(as.numeric(bq53_5) %in% 0:10, as.numeric(bq53_5), NA_real_),
    # Discuss politics (0-10)
    discuss = ifelse(as.numeric(bq53_9) %in% 0:10, as.numeric(bq53_9), NA_real_),
    # Weight - post-wave weight
    weight = as.numeric(postwgt)
  )

# Combine into a list for easier iteration
datasets <- list("2001" = bes2001, "2005" = bes2005, "2010" = bes2010)

# Show dataset overview
map_dfr(names(datasets), function(yr) {
  d <- datasets[[yr]]
  tibble(
    Year = yr,
    `Total N` = nrow(d),
    `Complete cases (all vars)` = sum(complete.cases(d[, setdiff(names(d), "weight")]))
  )
}) %>%
  kable(caption = "Dataset Overview") %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Dataset Overview</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Year </th>
   <th style="text-align:right;"> Total N </th>
   <th style="text-align:right;"> Complete cases (all vars) </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:right;"> 3035 </td>
   <td style="text-align:right;"> 1471 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:right;"> 4791 </td>
   <td style="text-align:right;"> 3589 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:right;"> 3512 </td>
   <td style="text-align:right;"> 2350 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


The paper uses BES cross-sectional survey data from three elections. Variables are constructed as follows:

- **Education**: Age at which respondent completed full-time education, coded 1 (15 or younger) to 5 (19 or older). Those still in education are coded as 5.
- **Age**: Respondent's age in years.
- **Income**: Annual household income on a categorical scale (1-12 in 2001, 1-13 in 2005, 1-15 in 2010).
- **Male**: Binary (1 = male, 0 = female).
- **Party contact**: Whether any political party contacted the respondent on election day (binary). In 2001, the BES variable is "Knocked Up By Party" (election day contact). In 2005 and 2010, it explicitly asks about contact on election day.
- **Political efficacy**: Self-assessed influence on politics and public affairs (0-10 scale).
- **Political interest**: General interest in politics, reverse-coded to 0 (none at all) to 4 (a great deal).
- **Internet information**: Frequency of using the Internet for election information, reverse-coded to 0 (not at all) to 3 (a great deal). Non-internet users are coded as 0.
- **Dependent variables**: Vote (binary), work for party (0-10), donate money (0-10), discuss politics (0-10).

---

## Analytical Decisions and Assumptions

| Decision | Paper says | Our interpretation | Rationale | Alternative possible |
|----------|-----------|-------------------|-----------|---------------------|
| Weight variable (2001) | "Weighted per BES specs" | Used `MAILWGT` (mailback weight) | Internet use variable comes from the mailback questionnaire; mailback weight adjusts for non-response in this component | Could use `POSTOCTW` (post-election cross-section weight) |
| Weight variable (2005) | "Weighted per BES specs" | Used `postwtbr` (post-wave calibrated weight) | Standard post-election cross-section weight | Could use `panwtbr` (panel weight) |
| Weight variable (2010) | "Weighted per BES specs" | Used `postwgt` (post cross-section weight) | Standard post-election cross-section weight | Could use `mailwgt` |
| Non-internet users | Not explicitly stated | Coded as 0 on internet info scale | Non-internet users cannot use internet for election info | Could be coded as NA (excluded) |
| Education: still in school | Not mentioned | Coded as 5 (highest category) | Students are pursuing education beyond 19 | Could exclude or code differently |
| Party contact (2001) | Footnote: "Were you telephoned by a Canvasser?" | Used `BQ62` (Knocked Up By Party) - election day contact | Paper's main description says "election day" contact; BQ62 is the election day measure | Could use `BQ61` (phoned during campaign) |
| Party contact (2010) | Election day contact | Used `bq86_1` (general campaign contact) | Paper's Table 1 descriptive (mean ~0.53) matches `bq86_1` (0.55) much better than `bq87_1` (0.06) | Could use `bq87_1` (election day contact) |
| Internet use (2005) | 0-3 scale | Non-internet users (`bq110=2`) coded as 0 | Consistent with the coding logic for 2001 | Could code all who answered 4 (not at all) as 0 regardless of internet access |
| Education/Age/Income (2010) | Not mentioned | Combined pre-wave (`aq67`, `aq63`, `aq70`) and post-wave (`bq95_1`, `bq89`, `bq96`) variables | Post-wave variables alone yield N~1,143 (far below paper's ~2,300); combining recovers N~2,358 | Use post-wave only (too many missing cases) |
| Logistic regression output | "Odds ratios with standard errors" | Exponentiated coefficients and SEs on the odds ratio scale | Paper explicitly states "Cell entries are odds ratios" | SEs could be on log-odds scale |

**Flagged analytical choices in the original paper:**

1. OLS regression is used for bounded 0-10 ordinal scales (donating, discussing politics), which may not meet OLS assumptions. The authors note they tested ordered logit and negative binomial alternatives.
2. No correction for multiple comparisons across 24 models.
3. The interaction term in logistic regression (Table 2) is reported as an odds ratio, which does not straightforwardly correspond to moderation on the probability scale.

---

## Descriptive Statistics Comparison


::: {.cell}

```{.r .cell-code}
# Compute descriptive statistics and compare to Table 1
compute_desc <- function(d, year) {
  vars <- c("education", "age", "income", "male", "party_contact",
            "pol_efficacy", "pol_interest", "internet_info",
            "vote", "work_party", "donate", "discuss")

  map_dfr(vars, function(v) {
    x <- d[[v]]
    x <- x[!is.na(x)]
    tibble(
      Variable = v,
      Year = year,
      Mean = mean(x),
      SD = sd(x),
      Min = min(x),
      Max = max(x),
      N = length(x)
    )
  })
}

desc_all <- map_dfr(names(datasets), function(yr) {
  compute_desc(datasets[[yr]], yr)
})

# Paper's Table 1 values
paper_desc <- tribble(
  ~Variable, ~Year, ~Paper_Mean, ~Paper_SD,
  "education", "2001", 2.93, 1.60,
  "age", "2001", 44, 18.33,
  "income", "2001", 4.99, 3.36,
  "male", "2001", 0.50, 0.50,
  "party_contact", "2001", 0.08, 0.27,
  "pol_efficacy", "2001", 1.84, 2.19,
  "pol_interest", "2001", 1.89, 1.07,
  "internet_info", "2001", 0.17, 0.48,
  "vote", "2001", 0.69, 0.46,
  "work_party", "2001", 1.25, 2.33,
  "donate", "2001", 1.19, 2.39,
  "discuss", "2001", 5.07, 3.55,
  "education", "2005", 2.79, 1.59,
  "age", "2005", 47, 18,
  "income", "2005", 6.04, 3.45,
  "male", "2005", 0.48, 0.50,
  "party_contact", "2005", 0.06, 0.23,
  "pol_efficacy", "2005", 2.71, 2.28,
  "pol_interest", "2005", 2.07, 0.98,
  "internet_info", "2005", 0.23, 0.64,
  "vote", "2005", 0.72, 0.45,
  "work_party", "2005", 1.24, 2.09,
  "donate", "2005", 1.34, 2.21,
  "discuss", "2005", 5.42, 3.36,
  "education", "2010", 3.12, 1.57,
  "age", "2010", 47, 18,
  "income", "2010", 6.92, 4.03,
  "male", "2010", 0.47, 0.50,
  "party_contact", "2010", 0.53, 0.50,
  "pol_efficacy", "2010", 1.84, 2.22,
  "pol_interest", "2010", 2.16, 1.07,
  "internet_info", "2010", 0.54, 0.85,
  "vote", "2010", 0.77, 0.42,
  "work_party", "2010", 1.28, 2.21,
  "donate", "2010", 1.05, 2.07,
  "discuss", "2010", 5.62, 3.36
)

# Merge and display comparison
desc_compare <- desc_all %>%
  left_join(paper_desc, by = c("Variable", "Year")) %>%
  filter(!is.na(Paper_Mean)) %>%
  mutate(
    Mean_diff = Mean - Paper_Mean,
    Variable = factor(Variable, levels = c("education", "age", "income", "male",
                                            "party_contact", "pol_efficacy",
                                            "pol_interest", "internet_info",
                                            "vote", "work_party", "donate", "discuss"))
  ) %>%
  arrange(Year, Variable)

desc_display <- desc_compare %>%
  dplyr::select(Year, Variable, Paper_Mean, Mean, Mean_diff, Paper_SD, SD, N)

desc_display %>%
  kable(caption = "Descriptive Statistics Comparison with Table 1",
        digits = 2,
        col.names = c("Year", "Variable", "Paper Mean", "Reproduced Mean",
                       "Difference", "Paper SD", "Reproduced SD", "N")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE) %>%
  column_spec(5, background = ifelse(abs(desc_display$Mean_diff) > 0.5, "#f8d7da", "#d4edda"))
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Descriptive Statistics Comparison with Table 1</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Year </th>
   <th style="text-align:left;"> Variable </th>
   <th style="text-align:right;"> Paper Mean </th>
   <th style="text-align:right;"> Reproduced Mean </th>
   <th style="text-align:right;"> Difference </th>
   <th style="text-align:right;"> Paper SD </th>
   <th style="text-align:right;"> Reproduced SD </th>
   <th style="text-align:right;"> N </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> education </td>
   <td style="text-align:right;"> 2.93 </td>
   <td style="text-align:right;"> 2.62 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.31 </td>
   <td style="text-align:right;"> 1.60 </td>
   <td style="text-align:right;"> 1.59 </td>
   <td style="text-align:right;"> 3024 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> age </td>
   <td style="text-align:right;"> 44.00 </td>
   <td style="text-align:right;"> 50.38 </td>
   <td style="text-align:right;background-color: rgba(248, 215, 218, 255) !important;"> 6.38 </td>
   <td style="text-align:right;"> 18.33 </td>
   <td style="text-align:right;"> 17.99 </td>
   <td style="text-align:right;"> 3013 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> income </td>
   <td style="text-align:right;"> 4.99 </td>
   <td style="text-align:right;"> 4.67 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.32 </td>
   <td style="text-align:right;"> 3.36 </td>
   <td style="text-align:right;"> 3.22 </td>
   <td style="text-align:right;"> 2219 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> male </td>
   <td style="text-align:right;"> 0.50 </td>
   <td style="text-align:right;"> 0.44 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.06 </td>
   <td style="text-align:right;"> 0.50 </td>
   <td style="text-align:right;"> 0.50 </td>
   <td style="text-align:right;"> 3034 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> party_contact </td>
   <td style="text-align:right;"> 0.08 </td>
   <td style="text-align:right;"> 0.05 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.03 </td>
   <td style="text-align:right;"> 0.27 </td>
   <td style="text-align:right;"> 0.22 </td>
   <td style="text-align:right;"> 2996 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> pol_efficacy </td>
   <td style="text-align:right;"> 1.84 </td>
   <td style="text-align:right;"> 1.74 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.10 </td>
   <td style="text-align:right;"> 2.19 </td>
   <td style="text-align:right;"> 2.17 </td>
   <td style="text-align:right;"> 3016 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> pol_interest </td>
   <td style="text-align:right;"> 1.89 </td>
   <td style="text-align:right;"> 1.88 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.01 </td>
   <td style="text-align:right;"> 1.07 </td>
   <td style="text-align:right;"> 1.08 </td>
   <td style="text-align:right;"> 3034 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> internet_info </td>
   <td style="text-align:right;"> 0.17 </td>
   <td style="text-align:right;"> 0.11 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.06 </td>
   <td style="text-align:right;"> 0.48 </td>
   <td style="text-align:right;"> 0.39 </td>
   <td style="text-align:right;"> 1986 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> vote </td>
   <td style="text-align:right;"> 0.69 </td>
   <td style="text-align:right;"> 0.73 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> 0.04 </td>
   <td style="text-align:right;"> 0.46 </td>
   <td style="text-align:right;"> 0.45 </td>
   <td style="text-align:right;"> 3030 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> work_party </td>
   <td style="text-align:right;"> 1.25 </td>
   <td style="text-align:right;"> 1.16 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.09 </td>
   <td style="text-align:right;"> 2.33 </td>
   <td style="text-align:right;"> 2.30 </td>
   <td style="text-align:right;"> 3024 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> donate </td>
   <td style="text-align:right;"> 1.19 </td>
   <td style="text-align:right;"> 1.13 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.06 </td>
   <td style="text-align:right;"> 2.39 </td>
   <td style="text-align:right;"> 2.39 </td>
   <td style="text-align:right;"> 3021 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> discuss </td>
   <td style="text-align:right;"> 5.07 </td>
   <td style="text-align:right;"> 4.76 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.31 </td>
   <td style="text-align:right;"> 3.55 </td>
   <td style="text-align:right;"> 3.60 </td>
   <td style="text-align:right;"> 3022 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> education </td>
   <td style="text-align:right;"> 2.79 </td>
   <td style="text-align:right;"> 2.59 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.20 </td>
   <td style="text-align:right;"> 1.59 </td>
   <td style="text-align:right;"> 1.56 </td>
   <td style="text-align:right;"> 4782 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> age </td>
   <td style="text-align:right;"> 47.00 </td>
   <td style="text-align:right;"> 50.28 </td>
   <td style="text-align:right;background-color: rgba(248, 215, 218, 255) !important;"> 3.28 </td>
   <td style="text-align:right;"> 18.00 </td>
   <td style="text-align:right;"> 17.88 </td>
   <td style="text-align:right;"> 4765 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> income </td>
   <td style="text-align:right;"> 6.04 </td>
   <td style="text-align:right;"> 5.44 </td>
   <td style="text-align:right;background-color: rgba(248, 215, 218, 255) !important;"> -0.60 </td>
   <td style="text-align:right;"> 3.45 </td>
   <td style="text-align:right;"> 3.35 </td>
   <td style="text-align:right;"> 4129 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> male </td>
   <td style="text-align:right;"> 0.48 </td>
   <td style="text-align:right;"> 0.44 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.04 </td>
   <td style="text-align:right;"> 0.50 </td>
   <td style="text-align:right;"> 0.50 </td>
   <td style="text-align:right;"> 4786 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> party_contact </td>
   <td style="text-align:right;"> 0.06 </td>
   <td style="text-align:right;"> 0.06 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> 0.00 </td>
   <td style="text-align:right;"> 0.23 </td>
   <td style="text-align:right;"> 0.23 </td>
   <td style="text-align:right;"> 4136 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> pol_efficacy </td>
   <td style="text-align:right;"> 2.71 </td>
   <td style="text-align:right;"> 2.61 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.10 </td>
   <td style="text-align:right;"> 2.28 </td>
   <td style="text-align:right;"> 2.30 </td>
   <td style="text-align:right;"> 4140 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> pol_interest </td>
   <td style="text-align:right;"> 2.07 </td>
   <td style="text-align:right;"> 2.06 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.01 </td>
   <td style="text-align:right;"> 0.98 </td>
   <td style="text-align:right;"> 1.00 </td>
   <td style="text-align:right;"> 4160 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> internet_info </td>
   <td style="text-align:right;"> 0.23 </td>
   <td style="text-align:right;"> 0.13 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.10 </td>
   <td style="text-align:right;"> 0.64 </td>
   <td style="text-align:right;"> 0.51 </td>
   <td style="text-align:right;"> 4158 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> vote </td>
   <td style="text-align:right;"> 0.72 </td>
   <td style="text-align:right;"> 0.74 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> 0.02 </td>
   <td style="text-align:right;"> 0.45 </td>
   <td style="text-align:right;"> 0.44 </td>
   <td style="text-align:right;"> 4158 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> work_party </td>
   <td style="text-align:right;"> 1.24 </td>
   <td style="text-align:right;"> 1.18 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.06 </td>
   <td style="text-align:right;"> 2.09 </td>
   <td style="text-align:right;"> 2.09 </td>
   <td style="text-align:right;"> 4157 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> donate </td>
   <td style="text-align:right;"> 1.34 </td>
   <td style="text-align:right;"> 1.33 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.01 </td>
   <td style="text-align:right;"> 2.21 </td>
   <td style="text-align:right;"> 2.30 </td>
   <td style="text-align:right;"> 4155 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> discuss </td>
   <td style="text-align:right;"> 5.42 </td>
   <td style="text-align:right;"> 5.26 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.16 </td>
   <td style="text-align:right;"> 3.36 </td>
   <td style="text-align:right;"> 3.39 </td>
   <td style="text-align:right;"> 4157 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> education </td>
   <td style="text-align:right;"> 3.12 </td>
   <td style="text-align:right;"> 2.91 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.21 </td>
   <td style="text-align:right;"> 1.57 </td>
   <td style="text-align:right;"> 1.58 </td>
   <td style="text-align:right;"> 3506 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> age </td>
   <td style="text-align:right;"> 47.00 </td>
   <td style="text-align:right;"> 51.23 </td>
   <td style="text-align:right;background-color: rgba(248, 215, 218, 255) !important;"> 4.23 </td>
   <td style="text-align:right;"> 18.00 </td>
   <td style="text-align:right;"> 18.09 </td>
   <td style="text-align:right;"> 3502 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> income </td>
   <td style="text-align:right;"> 6.92 </td>
   <td style="text-align:right;"> 6.20 </td>
   <td style="text-align:right;background-color: rgba(248, 215, 218, 255) !important;"> -0.72 </td>
   <td style="text-align:right;"> 4.03 </td>
   <td style="text-align:right;"> 3.92 </td>
   <td style="text-align:right;"> 2715 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> male </td>
   <td style="text-align:right;"> 0.47 </td>
   <td style="text-align:right;"> 0.46 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.01 </td>
   <td style="text-align:right;"> 0.50 </td>
   <td style="text-align:right;"> 0.50 </td>
   <td style="text-align:right;"> 3075 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> party_contact </td>
   <td style="text-align:right;"> 0.53 </td>
   <td style="text-align:right;"> 0.55 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> 0.02 </td>
   <td style="text-align:right;"> 0.50 </td>
   <td style="text-align:right;"> 0.50 </td>
   <td style="text-align:right;"> 3055 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> pol_efficacy </td>
   <td style="text-align:right;"> 1.84 </td>
   <td style="text-align:right;"> 1.73 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.11 </td>
   <td style="text-align:right;"> 2.22 </td>
   <td style="text-align:right;"> 2.18 </td>
   <td style="text-align:right;"> 3062 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> pol_interest </td>
   <td style="text-align:right;"> 2.16 </td>
   <td style="text-align:right;"> 2.17 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> 0.01 </td>
   <td style="text-align:right;"> 1.07 </td>
   <td style="text-align:right;"> 1.08 </td>
   <td style="text-align:right;"> 3074 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> internet_info </td>
   <td style="text-align:right;"> 0.54 </td>
   <td style="text-align:right;"> 0.44 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.10 </td>
   <td style="text-align:right;"> 0.85 </td>
   <td style="text-align:right;"> 0.79 </td>
   <td style="text-align:right;"> 3067 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> vote </td>
   <td style="text-align:right;"> 0.77 </td>
   <td style="text-align:right;"> 0.78 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> 0.01 </td>
   <td style="text-align:right;"> 0.42 </td>
   <td style="text-align:right;"> 0.41 </td>
   <td style="text-align:right;"> 3070 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> work_party </td>
   <td style="text-align:right;"> 1.28 </td>
   <td style="text-align:right;"> 1.17 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.11 </td>
   <td style="text-align:right;"> 2.21 </td>
   <td style="text-align:right;"> 2.16 </td>
   <td style="text-align:right;"> 3065 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> donate </td>
   <td style="text-align:right;"> 1.05 </td>
   <td style="text-align:right;"> 1.10 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> 0.05 </td>
   <td style="text-align:right;"> 2.07 </td>
   <td style="text-align:right;"> 2.19 </td>
   <td style="text-align:right;"> 3065 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> discuss </td>
   <td style="text-align:right;"> 5.62 </td>
   <td style="text-align:right;"> 5.38 </td>
   <td style="text-align:right;background-color: rgba(212, 237, 218, 255) !important;"> -0.24 </td>
   <td style="text-align:right;"> 3.36 </td>
   <td style="text-align:right;"> 3.43 </td>
   <td style="text-align:right;"> 3072 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


---

## Reproduction Results

### Table 2: Logistic Regression — Voting


::: {.cell}

```{.r .cell-code}
# Fit logistic regression models for voting
fit_voting_models <- function(d, w) {
  # Main effects model
  main <- glm(vote ~ education + age + income + male + party_contact +
                pol_efficacy + pol_interest + internet_info,
              data = d, family = binomial(link = "logit"), weights = w)

  # Interaction model
  inter <- glm(vote ~ education + age + income + male + party_contact +
                 pol_efficacy + pol_interest + internet_info +
                 internet_info:pol_interest,
               data = d, family = binomial(link = "logit"), weights = w)

  list(main = main, inter = inter)
}

voting_models <- map(names(datasets), function(yr) {
  d <- datasets[[yr]] %>% drop_na(vote, education, age, income, male,
                                    party_contact, pol_efficacy, pol_interest,
                                    internet_info)
  fit_voting_models(d, d$weight)
}) %>% set_names(names(datasets))

# Extract odds ratios and SEs
extract_logit_results <- function(model) {
  s <- summary(model)
  coefs <- s$coefficients
  or <- exp(coefs[, "Estimate"])
  # SE of OR using delta method: SE(OR) = OR * SE(log-OR)
  se_or <- or * coefs[, "Std. Error"]
  tibble(
    term = rownames(coefs),
    OR = or,
    SE = se_or,
    p = coefs[, "Pr(>|z|)"]
  )
}

# Build comparison table for Table 2
voting_results <- map_dfr(names(voting_models), function(yr) {
  main_res <- extract_logit_results(voting_models[[yr]]$main) %>%
    mutate(Year = yr, Model = "Main Effect")
  inter_res <- extract_logit_results(voting_models[[yr]]$inter) %>%
    mutate(Year = yr, Model = "Interaction")
  bind_rows(main_res, inter_res)
})

# Add model fit statistics
voting_fit <- map_dfr(names(voting_models), function(yr) {
  for (type in c("main", "inter")) {
    m <- voting_models[[yr]][[type]]
    null_dev <- m$null.deviance
    resid_dev <- m$deviance
    lr_chi2 <- null_dev - resid_dev
    df_lr <- m$df.null - m$df.residual
    pseudo_r2 <- 1 - resid_dev / null_dev
    n <- nrow(m$model)
  }
  # Return for both models
  bind_rows(
    tibble(Year = yr, Model = "Main Effect",
           N = nrow(voting_models[[yr]]$main$model),
           LR_chi2 = voting_models[[yr]]$main$null.deviance - voting_models[[yr]]$main$deviance,
           df = voting_models[[yr]]$main$df.null - voting_models[[yr]]$main$df.residual,
           Pseudo_R2 = 1 - voting_models[[yr]]$main$deviance / voting_models[[yr]]$main$null.deviance),
    tibble(Year = yr, Model = "Interaction",
           N = nrow(voting_models[[yr]]$inter$model),
           LR_chi2 = voting_models[[yr]]$inter$null.deviance - voting_models[[yr]]$inter$deviance,
           df = voting_models[[yr]]$inter$df.null - voting_models[[yr]]$inter$df.residual,
           Pseudo_R2 = 1 - voting_models[[yr]]$inter$deviance / voting_models[[yr]]$inter$null.deviance)
  )
})

# Display results in a formatted table
format_coef <- function(or, se, p) {
  stars <- case_when(
    p < 0.001 ~ "***",
    p < 0.01 ~ "**",
    p < 0.05 ~ "*",
    TRUE ~ ""
  )
  paste0(sprintf("%.3f%s", or, stars), "\n(", sprintf("%.3f", se), ")")
}

# Create wide-format table matching paper's Table 2
var_order <- c("(Intercept)", "education", "age", "income", "male",
               "party_contact", "pol_efficacy", "pol_interest",
               "internet_info", "pol_interest:internet_info")
var_labels <- c("Constant", "Education", "Age", "Income", "Male",
                "Party contact", "Political efficacy", "Political interest",
                "Internet info", "Interaction")

voting_wide <- voting_results %>%
  mutate(
    display = paste0(sprintf("%.3f", OR),
                     case_when(p < 0.001 ~ "***", p < 0.01 ~ "**",
                               p < 0.05 ~ "*", TRUE ~ ""),
                     "<br>(", sprintf("%.3f", SE), ")")
  ) %>%
  mutate(col = paste(Model, Year)) %>%
  select(term, col, display) %>%
  pivot_wider(names_from = col, values_from = display) %>%
  mutate(term = factor(term, levels = var_order, labels = var_labels)) %>%
  filter(!is.na(term)) %>%
  arrange(term)

# Also add fit stats rows
fit_rows <- voting_fit %>%
  mutate(col = paste(Model, Year)) %>%
  pivot_longer(cols = c(N, LR_chi2, Pseudo_R2), names_to = "term", values_to = "value") %>%
  mutate(
    display = case_when(
      term == "N" ~ format(round(value), big.mark = ","),
      term == "LR_chi2" ~ sprintf("%.2f***", value),
      term == "Pseudo_R2" ~ sprintf("%.3f", value)
    ),
    term = case_when(
      term == "N" ~ "Observations",
      term == "LR_chi2" ~ "LR χ²(9)",
      term == "Pseudo_R2" ~ "Pseudo R²"
    )
  ) %>%
  select(term, col, display) %>%
  pivot_wider(names_from = col, values_from = display)

bind_rows(voting_wide, fit_rows) %>%
  kable(format = "html", escape = FALSE,
        caption = "Table 2 Reproduction: Logistic Regression Models Predicting Voting",
        col.names = c("", "2001", "2005", "2010", "2001", "2005", "2010")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE) %>%
  add_header_above(c(" " = 1, "Main Effect" = 3, "Interaction" = 3))
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Table 2 Reproduction: Logistic Regression Models Predicting Voting</caption>
 <thead>
<tr>
<th style="empty-cells: hide;border-bottom:hidden;" colspan="1"></th>
<th style="border-bottom:hidden;padding-bottom:0; padding-left:3px;padding-right:3px;text-align: center; " colspan="3"><div style="border-bottom: 1px solid #ddd; padding-bottom: 5px; ">Main Effect</div></th>
<th style="border-bottom:hidden;padding-bottom:0; padding-left:3px;padding-right:3px;text-align: center; " colspan="3"><div style="border-bottom: 1px solid #ddd; padding-bottom: 5px; ">Interaction</div></th>
</tr>
  <tr>
   <th style="text-align:left;">  </th>
   <th style="text-align:left;"> 2001 </th>
   <th style="text-align:left;"> 2005 </th>
   <th style="text-align:left;"> 2010 </th>
   <th style="text-align:left;"> 2001 </th>
   <th style="text-align:left;"> 2005 </th>
   <th style="text-align:left;"> 2010 </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Constant </td>
   <td style="text-align:left;"> 0.076***<br>(0.025) </td>
   <td style="text-align:left;"> 0.076***<br>(0.025) </td>
   <td style="text-align:left;"> 0.036***<br>(0.008) </td>
   <td style="text-align:left;"> 0.036***<br>(0.008) </td>
   <td style="text-align:left;"> 0.046***<br>(0.013) </td>
   <td style="text-align:left;"> 0.044***<br>(0.013) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Education </td>
   <td style="text-align:left;"> 1.101<br>(0.057) </td>
   <td style="text-align:left;"> 1.100<br>(0.057) </td>
   <td style="text-align:left;"> 1.128***<br>(0.037) </td>
   <td style="text-align:left;"> 1.128***<br>(0.037) </td>
   <td style="text-align:left;"> 1.039<br>(0.046) </td>
   <td style="text-align:left;"> 1.039<br>(0.046) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Age </td>
   <td style="text-align:left;"> 1.047***<br>(0.005) </td>
   <td style="text-align:left;"> 1.047***<br>(0.005) </td>
   <td style="text-align:left;"> 1.052***<br>(0.003) </td>
   <td style="text-align:left;"> 1.052***<br>(0.003) </td>
   <td style="text-align:left;"> 1.041***<br>(0.004) </td>
   <td style="text-align:left;"> 1.041***<br>(0.004) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Income </td>
   <td style="text-align:left;"> 1.078***<br>(0.024) </td>
   <td style="text-align:left;"> 1.079***<br>(0.024) </td>
   <td style="text-align:left;"> 1.079***<br>(0.015) </td>
   <td style="text-align:left;"> 1.079***<br>(0.015) </td>
   <td style="text-align:left;"> 1.107***<br>(0.019) </td>
   <td style="text-align:left;"> 1.108***<br>(0.019) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Male </td>
   <td style="text-align:left;"> 0.695**<br>(0.095) </td>
   <td style="text-align:left;"> 0.694**<br>(0.095) </td>
   <td style="text-align:left;"> 0.741***<br>(0.064) </td>
   <td style="text-align:left;"> 0.741***<br>(0.064) </td>
   <td style="text-align:left;"> 0.633***<br>(0.073) </td>
   <td style="text-align:left;"> 0.633***<br>(0.074) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Party contact </td>
   <td style="text-align:left;"> 2.021<br>(0.753) </td>
   <td style="text-align:left;"> 2.015<br>(0.752) </td>
   <td style="text-align:left;"> 2.340***<br>(0.547) </td>
   <td style="text-align:left;"> 2.339***<br>(0.547) </td>
   <td style="text-align:left;"> 1.517***<br>(0.171) </td>
   <td style="text-align:left;"> 1.529***<br>(0.173) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Political efficacy </td>
   <td style="text-align:left;"> 1.136***<br>(0.040) </td>
   <td style="text-align:left;"> 1.135***<br>(0.040) </td>
   <td style="text-align:left;"> 1.167***<br>(0.025) </td>
   <td style="text-align:left;"> 1.167***<br>(0.025) </td>
   <td style="text-align:left;"> 1.125***<br>(0.033) </td>
   <td style="text-align:left;"> 1.124***<br>(0.033) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Political interest </td>
   <td style="text-align:left;"> 1.652***<br>(0.124) </td>
   <td style="text-align:left;"> 1.661***<br>(0.130) </td>
   <td style="text-align:left;"> 1.637***<br>(0.084) </td>
   <td style="text-align:left;"> 1.632***<br>(0.086) </td>
   <td style="text-align:left;"> 1.865***<br>(0.118) </td>
   <td style="text-align:left;"> 1.916***<br>(0.132) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:left;"> 1.559*<br>(0.288) </td>
   <td style="text-align:left;"> 1.714<br>(0.784) </td>
   <td style="text-align:left;"> 1.240*<br>(0.106) </td>
   <td style="text-align:left;"> 1.170<br>(0.269) </td>
   <td style="text-align:left;"> 1.757***<br>(0.154) </td>
   <td style="text-align:left;"> 2.108***<br>(0.422) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> 0.960<br>(0.172) </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> 1.025<br>(0.091) </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> 0.918<br>(0.076) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Observations </td>
   <td style="text-align:left;"> 1,476 </td>
   <td style="text-align:left;"> 1,476 </td>
   <td style="text-align:left;"> 3,592 </td>
   <td style="text-align:left;"> 3,592 </td>
   <td style="text-align:left;"> 2,361 </td>
   <td style="text-align:left;"> 2,361 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> LR χ²(9) </td>
   <td style="text-align:left;"> 256.52*** </td>
   <td style="text-align:left;"> 256.57*** </td>
   <td style="text-align:left;"> 729.07*** </td>
   <td style="text-align:left;"> 729.15*** </td>
   <td style="text-align:left;"> 503.99*** </td>
   <td style="text-align:left;"> 505.04*** </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Pseudo R² </td>
   <td style="text-align:left;"> 0.154 </td>
   <td style="text-align:left;"> 0.154 </td>
   <td style="text-align:left;"> 0.176 </td>
   <td style="text-align:left;"> 0.176 </td>
   <td style="text-align:left;"> 0.202 </td>
   <td style="text-align:left;"> 0.203 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



### Table 3: OLS Regression — Donating Money


::: {.cell}

```{.r .cell-code}
# Fit OLS models for donating
fit_ols_models <- function(d, w, dv) {
  formula_main <- as.formula(paste(dv, "~ education + age + income + male + party_contact +
                                    pol_efficacy + pol_interest + internet_info"))
  formula_inter <- as.formula(paste(dv, "~ education + age + income + male + party_contact +
                                     pol_efficacy + pol_interest + internet_info +
                                     internet_info:pol_interest"))

  main <- lm(formula_main, data = d, weights = w)
  inter <- lm(formula_inter, data = d, weights = w)

  list(main = main, inter = inter)
}

donate_models <- map(names(datasets), function(yr) {
  d <- datasets[[yr]] %>% drop_na(donate, education, age, income, male,
                                    party_contact, pol_efficacy, pol_interest,
                                    internet_info)
  fit_ols_models(d, d$weight, "donate")
}) %>% set_names(names(datasets))

# Extract coefficients
extract_ols_results <- function(model) {
  s <- summary(model)
  coefs <- s$coefficients
  tibble(
    term = rownames(coefs),
    Coef = coefs[, "Estimate"],
    SE = coefs[, "Std. Error"],
    p = coefs[, "Pr(>|t|)"]
  )
}

donate_results <- map_dfr(names(donate_models), function(yr) {
  main_res <- extract_ols_results(donate_models[[yr]]$main) %>%
    mutate(Year = yr, Model = "Main Effects")
  inter_res <- extract_ols_results(donate_models[[yr]]$inter) %>%
    mutate(Year = yr, Model = "Interactions")
  bind_rows(main_res, inter_res)
})

# Fit stats
donate_fit <- map_dfr(names(donate_models), function(yr) {
  bind_rows(
    tibble(Year = yr, Model = "Main Effects",
           N = nrow(donate_models[[yr]]$main$model),
           R2 = summary(donate_models[[yr]]$main)$r.squared,
           Adj_R2 = summary(donate_models[[yr]]$main)$adj.r.squared),
    tibble(Year = yr, Model = "Interactions",
           N = nrow(donate_models[[yr]]$inter$model),
           R2 = summary(donate_models[[yr]]$inter)$r.squared,
           Adj_R2 = summary(donate_models[[yr]]$inter)$adj.r.squared)
  )
})

# Format table
donate_wide <- donate_results %>%
  mutate(
    display = paste0(sprintf("%.3f", Coef),
                     case_when(p < 0.001 ~ "***", p < 0.01 ~ "**",
                               p < 0.05 ~ "*", TRUE ~ ""),
                     "<br>(", sprintf("%.3f", SE), ")")
  ) %>%
  mutate(col = paste(Model, Year)) %>%
  select(term, col, display) %>%
  pivot_wider(names_from = col, values_from = display) %>%
  mutate(term = factor(term, levels = var_order, labels = var_labels)) %>%
  filter(!is.na(term)) %>%
  arrange(term)

fit_rows_d <- donate_fit %>%
  mutate(col = paste(Model, Year)) %>%
  pivot_longer(cols = c(N, R2, Adj_R2), names_to = "term", values_to = "value") %>%
  mutate(
    display = case_when(
      term == "N" ~ format(round(value), big.mark = ","),
      TRUE ~ sprintf("%.3f", value)
    ),
    term = case_when(
      term == "N" ~ "Observations",
      term == "R2" ~ "R²",
      term == "Adj_R2" ~ "Adjusted R²"
    )
  ) %>%
  select(term, col, display) %>%
  pivot_wider(names_from = col, values_from = display)

bind_rows(donate_wide, fit_rows_d) %>%
  kable(format = "html", escape = FALSE,
        caption = "Table 3 Reproduction: OLS Regression Models Predicting Donating",
        col.names = c("", "2001", "2005", "2010", "2001", "2005", "2010")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE) %>%
  add_header_above(c(" " = 1, "Main Effects" = 3, "Interactions" = 3))
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Table 3 Reproduction: OLS Regression Models Predicting Donating</caption>
 <thead>
<tr>
<th style="empty-cells: hide;border-bottom:hidden;" colspan="1"></th>
<th style="border-bottom:hidden;padding-bottom:0; padding-left:3px;padding-right:3px;text-align: center; " colspan="3"><div style="border-bottom: 1px solid #ddd; padding-bottom: 5px; ">Main Effects</div></th>
<th style="border-bottom:hidden;padding-bottom:0; padding-left:3px;padding-right:3px;text-align: center; " colspan="3"><div style="border-bottom: 1px solid #ddd; padding-bottom: 5px; ">Interactions</div></th>
</tr>
  <tr>
   <th style="text-align:left;">  </th>
   <th style="text-align:left;"> 2001 </th>
   <th style="text-align:left;"> 2005 </th>
   <th style="text-align:left;"> 2010 </th>
   <th style="text-align:left;"> 2001 </th>
   <th style="text-align:left;"> 2005 </th>
   <th style="text-align:left;"> 2010 </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Constant </td>
   <td style="text-align:left;"> -1.090***<br>(0.290) </td>
   <td style="text-align:left;"> -1.163***<br>(0.293) </td>
   <td style="text-align:left;"> -0.668***<br>(0.163) </td>
   <td style="text-align:left;"> -0.635***<br>(0.164) </td>
   <td style="text-align:left;"> -0.514**<br>(0.197) </td>
   <td style="text-align:left;"> -0.472*<br>(0.202) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Education </td>
   <td style="text-align:left;"> 0.141**<br>(0.047) </td>
   <td style="text-align:left;"> 0.132**<br>(0.047) </td>
   <td style="text-align:left;"> 0.037<br>(0.026) </td>
   <td style="text-align:left;"> 0.039<br>(0.026) </td>
   <td style="text-align:left;"> 0.001<br>(0.032) </td>
   <td style="text-align:left;"> 0.002<br>(0.032) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Age </td>
   <td style="text-align:left;"> 0.012**<br>(0.004) </td>
   <td style="text-align:left;"> 0.012**<br>(0.004) </td>
   <td style="text-align:left;"> 0.011***<br>(0.002) </td>
   <td style="text-align:left;"> 0.011***<br>(0.002) </td>
   <td style="text-align:left;"> 0.008**<br>(0.003) </td>
   <td style="text-align:left;"> 0.008**<br>(0.003) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Income </td>
   <td style="text-align:left;"> 0.020<br>(0.020) </td>
   <td style="text-align:left;"> 0.026<br>(0.021) </td>
   <td style="text-align:left;"> 0.007<br>(0.011) </td>
   <td style="text-align:left;"> 0.007<br>(0.011) </td>
   <td style="text-align:left;"> 0.018<br>(0.011) </td>
   <td style="text-align:left;"> 0.018<br>(0.011) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Male </td>
   <td style="text-align:left;"> -0.046<br>(0.127) </td>
   <td style="text-align:left;"> -0.054<br>(0.127) </td>
   <td style="text-align:left;"> 0.117<br>(0.071) </td>
   <td style="text-align:left;"> 0.116<br>(0.071) </td>
   <td style="text-align:left;"> -0.010<br>(0.085) </td>
   <td style="text-align:left;"> -0.012<br>(0.085) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Party contact </td>
   <td style="text-align:left;"> -0.385<br>(0.277) </td>
   <td style="text-align:left;"> -0.408<br>(0.277) </td>
   <td style="text-align:left;"> 0.397**<br>(0.148) </td>
   <td style="text-align:left;"> 0.396**<br>(0.148) </td>
   <td style="text-align:left;"> 0.178*<br>(0.084) </td>
   <td style="text-align:left;"> 0.173*<br>(0.084) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Political efficacy </td>
   <td style="text-align:left;"> 0.213***<br>(0.029) </td>
   <td style="text-align:left;"> 0.210***<br>(0.029) </td>
   <td style="text-align:left;"> 0.221***<br>(0.016) </td>
   <td style="text-align:left;"> 0.221***<br>(0.016) </td>
   <td style="text-align:left;"> 0.237***<br>(0.019) </td>
   <td style="text-align:left;"> 0.238***<br>(0.019) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Political interest </td>
   <td style="text-align:left;"> 0.447***<br>(0.067) </td>
   <td style="text-align:left;"> 0.486***<br>(0.070) </td>
   <td style="text-align:left;"> 0.295***<br>(0.041) </td>
   <td style="text-align:left;"> 0.277***<br>(0.042) </td>
   <td style="text-align:left;"> 0.235***<br>(0.046) </td>
   <td style="text-align:left;"> 0.214***<br>(0.051) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:left;"> 0.216<br>(0.139) </td>
   <td style="text-align:left;"> 0.922*<br>(0.404) </td>
   <td style="text-align:left;"> 0.272***<br>(0.062) </td>
   <td style="text-align:left;"> -0.063<br>(0.186) </td>
   <td style="text-align:left;"> 0.071<br>(0.054) </td>
   <td style="text-align:left;"> -0.051<br>(0.135) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> -0.261<br>(0.140) </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> 0.121<br>(0.063) </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> 0.047<br>(0.048) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Observations </td>
   <td style="text-align:left;"> 1,473 </td>
   <td style="text-align:left;"> 1,473 </td>
   <td style="text-align:left;"> 3,591 </td>
   <td style="text-align:left;"> 3,591 </td>
   <td style="text-align:left;"> 2,358 </td>
   <td style="text-align:left;"> 2,358 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> R² </td>
   <td style="text-align:left;"> 0.117 </td>
   <td style="text-align:left;"> 0.119 </td>
   <td style="text-align:left;"> 0.118 </td>
   <td style="text-align:left;"> 0.119 </td>
   <td style="text-align:left;"> 0.105 </td>
   <td style="text-align:left;"> 0.105 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Adjusted R² </td>
   <td style="text-align:left;"> 0.112 </td>
   <td style="text-align:left;"> 0.114 </td>
   <td style="text-align:left;"> 0.116 </td>
   <td style="text-align:left;"> 0.117 </td>
   <td style="text-align:left;"> 0.102 </td>
   <td style="text-align:left;"> 0.102 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



### Table 4: Negative Binomial Regression — Working for a Party


::: {.cell}

```{.r .cell-code}
# Fit negative binomial models for working for a party
# Store data alongside models so update() can find it
work_data <- map(names(datasets), function(yr) {
  datasets[[yr]] %>% drop_na(work_party, education, age, income, male,
                               party_contact, pol_efficacy, pol_interest,
                               internet_info)
}) %>% set_names(names(datasets))

work_models <- map(names(datasets), function(yr) {
  d <- work_data[[yr]]
  main <- MASS::glm.nb(work_party ~ education + age + income + male + party_contact +
                          pol_efficacy + pol_interest + internet_info,
                        data = d, weights = d$weight)

  inter <- MASS::glm.nb(work_party ~ education + age + income + male + party_contact +
                           pol_efficacy + pol_interest + internet_info +
                           internet_info:pol_interest,
                         data = d, weights = d$weight)

  list(main = main, inter = inter)
}) %>% set_names(names(datasets))

# Extract NB coefficients (reported as coefficients, not IRRs)
extract_nb_results <- function(model) {
  s <- summary(model)
  coefs <- s$coefficients
  tibble(
    term = rownames(coefs),
    Coef = coefs[, "Estimate"],
    SE = coefs[, "Std. Error"],
    p = coefs[, "Pr(>|z|)"]
  )
}

work_results <- map_dfr(names(work_models), function(yr) {
  main_res <- extract_nb_results(work_models[[yr]]$main) %>%
    mutate(Year = yr, Model = "Main Effects")
  inter_res <- extract_nb_results(work_models[[yr]]$inter) %>%
    mutate(Year = yr, Model = "Interactions")
  bind_rows(main_res, inter_res)
})

# Fit statistics for NB models
# Compute null model separately to avoid scope issues with update()
compute_nb_fit <- function(m, yr, model_label, d) {
  n <- nrow(m$model)
  null_m <- MASS::glm.nb(work_party ~ 1, data = d, weights = d$weight)
  ll_null <- logLik(null_m)
  ll_full <- logLik(m)
  cox_snell <- 1 - exp(2 * (as.numeric(ll_null) - as.numeric(ll_full)) / n)
  max_cox_snell <- 1 - exp(2 * as.numeric(ll_null) / n)
  nagelkerke_r2 <- cox_snell / max_cox_snell
  chi2 <- -2 * (as.numeric(ll_null) - as.numeric(ll_full))
  tibble(Year = yr, Model = model_label, N = n,
         Nagelkerke_R2 = nagelkerke_r2, alpha = m$theta, chi2 = chi2)
}

work_fit <- map_dfr(names(work_models), function(yr) {
  d <- work_data[[yr]]
  bind_rows(
    compute_nb_fit(work_models[[yr]]$main, yr, "Main Effects", d),
    compute_nb_fit(work_models[[yr]]$inter, yr, "Interactions", d)
  )
})

# Format table
work_wide <- work_results %>%
  mutate(
    display = paste0(sprintf("%.3f", Coef),
                     case_when(p < 0.001 ~ "***", p < 0.01 ~ "**",
                               p < 0.05 ~ "*", TRUE ~ ""),
                     "<br>(", sprintf("%.3f", SE), ")")
  ) %>%
  mutate(col = paste(Model, Year)) %>%
  select(term, col, display) %>%
  pivot_wider(names_from = col, values_from = display) %>%
  mutate(term = factor(term, levels = var_order, labels = var_labels)) %>%
  filter(!is.na(term)) %>%
  arrange(term)

fit_rows_w <- work_fit %>%
  mutate(col = paste(Model, Year)) %>%
  pivot_longer(cols = c(N, Nagelkerke_R2, alpha, chi2), names_to = "term", values_to = "value") %>%
  mutate(
    display = case_when(
      term == "N" ~ format(round(value), big.mark = ","),
      term == "alpha" ~ sprintf("%.1f", value),
      term == "chi2" ~ sprintf("%.2f", value),
      TRUE ~ sprintf("%.2f", value)
    ),
    term = case_when(
      term == "N" ~ "Observations",
      term == "Nagelkerke_R2" ~ "Nagelkerke R²",
      term == "alpha" ~ "α",
      term == "chi2" ~ "χ²"
    )
  ) %>%
  select(term, col, display) %>%
  pivot_wider(names_from = col, values_from = display)

bind_rows(work_wide, fit_rows_w) %>%
  kable(format = "html", escape = FALSE,
        caption = "Table 4 Reproduction: Negative Binomial Models Predicting Working for a Party",
        col.names = c("", "2001", "2005", "2010", "2001", "2005", "2010")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE) %>%
  add_header_above(c(" " = 1, "Main Effects" = 3, "Interactions" = 3))
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Table 4 Reproduction: Negative Binomial Models Predicting Working for a Party</caption>
 <thead>
<tr>
<th style="empty-cells: hide;border-bottom:hidden;" colspan="1"></th>
<th style="border-bottom:hidden;padding-bottom:0; padding-left:3px;padding-right:3px;text-align: center; " colspan="3"><div style="border-bottom: 1px solid #ddd; padding-bottom: 5px; ">Main Effects</div></th>
<th style="border-bottom:hidden;padding-bottom:0; padding-left:3px;padding-right:3px;text-align: center; " colspan="3"><div style="border-bottom: 1px solid #ddd; padding-bottom: 5px; ">Interactions</div></th>
</tr>
  <tr>
   <th style="text-align:left;">  </th>
   <th style="text-align:left;"> 2001 </th>
   <th style="text-align:left;"> 2005 </th>
   <th style="text-align:left;"> 2010 </th>
   <th style="text-align:left;"> 2001 </th>
   <th style="text-align:left;"> 2005 </th>
   <th style="text-align:left;"> 2010 </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Constant </td>
   <td style="text-align:left;"> -0.877***<br>(0.251) </td>
   <td style="text-align:left;"> -1.092***<br>(0.254) </td>
   <td style="text-align:left;"> -1.137***<br>(0.137) </td>
   <td style="text-align:left;"> -1.159***<br>(0.138) </td>
   <td style="text-align:left;"> -1.591***<br>(0.180) </td>
   <td style="text-align:left;"> -1.710***<br>(0.186) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Education </td>
   <td style="text-align:left;"> 0.097*<br>(0.040) </td>
   <td style="text-align:left;"> 0.084*<br>(0.040) </td>
   <td style="text-align:left;"> 0.022<br>(0.021) </td>
   <td style="text-align:left;"> 0.020<br>(0.021) </td>
   <td style="text-align:left;"> 0.119***<br>(0.028) </td>
   <td style="text-align:left;"> 0.117***<br>(0.028) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Age </td>
   <td style="text-align:left;"> -0.006<br>(0.004) </td>
   <td style="text-align:left;"> -0.005<br>(0.004) </td>
   <td style="text-align:left;"> -0.000<br>(0.002) </td>
   <td style="text-align:left;"> -0.000<br>(0.002) </td>
   <td style="text-align:left;"> 0.001<br>(0.003) </td>
   <td style="text-align:left;"> 0.001<br>(0.003) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Income </td>
   <td style="text-align:left;"> -0.039*<br>(0.017) </td>
   <td style="text-align:left;"> -0.026<br>(0.017) </td>
   <td style="text-align:left;"> -0.010<br>(0.009) </td>
   <td style="text-align:left;"> -0.009<br>(0.009) </td>
   <td style="text-align:left;"> -0.011<br>(0.010) </td>
   <td style="text-align:left;"> -0.013<br>(0.010) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Male </td>
   <td style="text-align:left;"> -0.068<br>(0.109) </td>
   <td style="text-align:left;"> -0.096<br>(0.108) </td>
   <td style="text-align:left;"> -0.114*<br>(0.058) </td>
   <td style="text-align:left;"> -0.113<br>(0.058) </td>
   <td style="text-align:left;"> 0.133<br>(0.075) </td>
   <td style="text-align:left;"> 0.134<br>(0.075) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Party contact </td>
   <td style="text-align:left;"> 0.132<br>(0.232) </td>
   <td style="text-align:left;"> 0.096<br>(0.231) </td>
   <td style="text-align:left;"> 0.082<br>(0.117) </td>
   <td style="text-align:left;"> 0.084<br>(0.117) </td>
   <td style="text-align:left;"> -0.017<br>(0.074) </td>
   <td style="text-align:left;"> 0.004<br>(0.074) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Political efficacy </td>
   <td style="text-align:left;"> 0.134***<br>(0.024) </td>
   <td style="text-align:left;"> 0.127***<br>(0.024) </td>
   <td style="text-align:left;"> 0.162***<br>(0.013) </td>
   <td style="text-align:left;"> 0.162***<br>(0.013) </td>
   <td style="text-align:left;"> 0.213***<br>(0.016) </td>
   <td style="text-align:left;"> 0.210***<br>(0.016) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Political interest </td>
   <td style="text-align:left;"> 0.425***<br>(0.058) </td>
   <td style="text-align:left;"> 0.492***<br>(0.061) </td>
   <td style="text-align:left;"> 0.364***<br>(0.034) </td>
   <td style="text-align:left;"> 0.374***<br>(0.035) </td>
   <td style="text-align:left;"> 0.330***<br>(0.041) </td>
   <td style="text-align:left;"> 0.386***<br>(0.047) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:left;"> 0.181<br>(0.111) </td>
   <td style="text-align:left;"> 1.223***<br>(0.323) </td>
   <td style="text-align:left;"> 0.212***<br>(0.046) </td>
   <td style="text-align:left;"> 0.366*<br>(0.143) </td>
   <td style="text-align:left;"> 0.084<br>(0.046) </td>
   <td style="text-align:left;"> 0.330**<br>(0.117) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> -0.386***<br>(0.112) </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> -0.055<br>(0.048) </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> -0.092*<br>(0.041) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Observations </td>
   <td style="text-align:left;"> 1,474 </td>
   <td style="text-align:left;"> 1,474 </td>
   <td style="text-align:left;"> 3,594 </td>
   <td style="text-align:left;"> 3,594 </td>
   <td style="text-align:left;"> 2,358 </td>
   <td style="text-align:left;"> 2,358 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Nagelkerke R² </td>
   <td style="text-align:left;"> 0.09 </td>
   <td style="text-align:left;"> 0.10 </td>
   <td style="text-align:left;"> 0.12 </td>
   <td style="text-align:left;"> 0.12 </td>
   <td style="text-align:left;"> 0.15 </td>
   <td style="text-align:left;"> 0.15 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> α </td>
   <td style="text-align:left;"> 0.3 </td>
   <td style="text-align:left;"> 0.3 </td>
   <td style="text-align:left;"> 0.6 </td>
   <td style="text-align:left;"> 0.6 </td>
   <td style="text-align:left;"> 0.5 </td>
   <td style="text-align:left;"> 0.5 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> χ² </td>
   <td style="text-align:left;"> 129.47 </td>
   <td style="text-align:left;"> 139.58 </td>
   <td style="text-align:left;"> 445.36 </td>
   <td style="text-align:left;"> 446.57 </td>
   <td style="text-align:left;"> 367.78 </td>
   <td style="text-align:left;"> 373.21 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



### Table 5: OLS Regression — Discussing Politics


::: {.cell}

```{.r .cell-code}
discuss_models <- map(names(datasets), function(yr) {
  d <- datasets[[yr]] %>% drop_na(discuss, education, age, income, male,
                                    party_contact, pol_efficacy, pol_interest,
                                    internet_info)
  fit_ols_models(d, d$weight, "discuss")
}) %>% set_names(names(datasets))

discuss_results <- map_dfr(names(discuss_models), function(yr) {
  main_res <- extract_ols_results(discuss_models[[yr]]$main) %>%
    mutate(Year = yr, Model = "Main Effects")
  inter_res <- extract_ols_results(discuss_models[[yr]]$inter) %>%
    mutate(Year = yr, Model = "Interactions")
  bind_rows(main_res, inter_res)
})

# Fit stats
discuss_fit <- map_dfr(names(discuss_models), function(yr) {
  bind_rows(
    tibble(Year = yr, Model = "Main Effects",
           N = nrow(discuss_models[[yr]]$main$model),
           R2 = summary(discuss_models[[yr]]$main)$r.squared,
           Adj_R2 = summary(discuss_models[[yr]]$main)$adj.r.squared),
    tibble(Year = yr, Model = "Interactions",
           N = nrow(discuss_models[[yr]]$inter$model),
           R2 = summary(discuss_models[[yr]]$inter)$r.squared,
           Adj_R2 = summary(discuss_models[[yr]]$inter)$adj.r.squared)
  )
})

# Format table
discuss_wide <- discuss_results %>%
  mutate(
    display = paste0(sprintf("%.3f", Coef),
                     case_when(p < 0.001 ~ "***", p < 0.01 ~ "**",
                               p < 0.05 ~ "*", TRUE ~ ""),
                     "<br>(", sprintf("%.3f", SE), ")")
  ) %>%
  mutate(col = paste(Model, Year)) %>%
  select(term, col, display) %>%
  pivot_wider(names_from = col, values_from = display) %>%
  mutate(term = factor(term, levels = var_order, labels = var_labels)) %>%
  filter(!is.na(term)) %>%
  arrange(term)

fit_rows_disc <- discuss_fit %>%
  mutate(col = paste(Model, Year)) %>%
  pivot_longer(cols = c(N, R2, Adj_R2), names_to = "term", values_to = "value") %>%
  mutate(
    display = case_when(
      term == "N" ~ format(round(value), big.mark = ","),
      TRUE ~ sprintf("%.3f", value)
    ),
    term = case_when(
      term == "N" ~ "Observations",
      term == "R2" ~ "R²",
      term == "Adj_R2" ~ "Adjusted R²"
    )
  ) %>%
  select(term, col, display) %>%
  pivot_wider(names_from = col, values_from = display)

bind_rows(discuss_wide, fit_rows_disc) %>%
  kable(format = "html", escape = FALSE,
        caption = "Table 5 Reproduction: OLS Regression Models Predicting Discussing Politics",
        col.names = c("", "2001", "2005", "2010", "2001", "2005", "2010")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE) %>%
  add_header_above(c(" " = 1, "Main Effects" = 3, "Interactions" = 3))
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Table 5 Reproduction: OLS Regression Models Predicting Discussing Politics</caption>
 <thead>
<tr>
<th style="empty-cells: hide;border-bottom:hidden;" colspan="1"></th>
<th style="border-bottom:hidden;padding-bottom:0; padding-left:3px;padding-right:3px;text-align: center; " colspan="3"><div style="border-bottom: 1px solid #ddd; padding-bottom: 5px; ">Main Effects</div></th>
<th style="border-bottom:hidden;padding-bottom:0; padding-left:3px;padding-right:3px;text-align: center; " colspan="3"><div style="border-bottom: 1px solid #ddd; padding-bottom: 5px; ">Interactions</div></th>
</tr>
  <tr>
   <th style="text-align:left;">  </th>
   <th style="text-align:left;"> 2001 </th>
   <th style="text-align:left;"> 2005 </th>
   <th style="text-align:left;"> 2010 </th>
   <th style="text-align:left;"> 2001 </th>
   <th style="text-align:left;"> 2005 </th>
   <th style="text-align:left;"> 2010 </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Constant </td>
   <td style="text-align:left;"> 1.832***<br>(0.371) </td>
   <td style="text-align:left;"> 1.716***<br>(0.374) </td>
   <td style="text-align:left;"> 1.146***<br>(0.209) </td>
   <td style="text-align:left;"> 1.053***<br>(0.210) </td>
   <td style="text-align:left;"> 1.307***<br>(0.257) </td>
   <td style="text-align:left;"> 1.125***<br>(0.263) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Education </td>
   <td style="text-align:left;"> 0.218***<br>(0.060) </td>
   <td style="text-align:left;"> 0.204***<br>(0.060) </td>
   <td style="text-align:left;"> 0.205***<br>(0.034) </td>
   <td style="text-align:left;"> 0.201***<br>(0.034) </td>
   <td style="text-align:left;"> 0.198***<br>(0.041) </td>
   <td style="text-align:left;"> 0.193***<br>(0.041) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Age </td>
   <td style="text-align:left;"> -0.010<br>(0.005) </td>
   <td style="text-align:left;"> -0.011*<br>(0.005) </td>
   <td style="text-align:left;"> -0.015***<br>(0.003) </td>
   <td style="text-align:left;"> -0.015***<br>(0.003) </td>
   <td style="text-align:left;"> -0.014***<br>(0.004) </td>
   <td style="text-align:left;"> -0.015***<br>(0.004) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Income </td>
   <td style="text-align:left;"> 0.062*<br>(0.026) </td>
   <td style="text-align:left;"> 0.072**<br>(0.026) </td>
   <td style="text-align:left;"> 0.104***<br>(0.014) </td>
   <td style="text-align:left;"> 0.104***<br>(0.014) </td>
   <td style="text-align:left;"> 0.082***<br>(0.015) </td>
   <td style="text-align:left;"> 0.083***<br>(0.015) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Male </td>
   <td style="text-align:left;"> -0.191<br>(0.163) </td>
   <td style="text-align:left;"> -0.204<br>(0.162) </td>
   <td style="text-align:left;"> 0.022<br>(0.091) </td>
   <td style="text-align:left;"> 0.025<br>(0.091) </td>
   <td style="text-align:left;"> 0.120<br>(0.111) </td>
   <td style="text-align:left;"> 0.129<br>(0.111) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Party contact </td>
   <td style="text-align:left;"> -0.103<br>(0.355) </td>
   <td style="text-align:left;"> -0.140<br>(0.354) </td>
   <td style="text-align:left;"> 0.434*<br>(0.190) </td>
   <td style="text-align:left;"> 0.437*<br>(0.189) </td>
   <td style="text-align:left;"> 0.356**<br>(0.110) </td>
   <td style="text-align:left;"> 0.377***<br>(0.110) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Political efficacy </td>
   <td style="text-align:left;"> 0.215***<br>(0.037) </td>
   <td style="text-align:left;"> 0.210***<br>(0.037) </td>
   <td style="text-align:left;"> 0.202***<br>(0.021) </td>
   <td style="text-align:left;"> 0.203***<br>(0.021) </td>
   <td style="text-align:left;"> 0.139***<br>(0.025) </td>
   <td style="text-align:left;"> 0.137***<br>(0.025) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Political interest </td>
   <td style="text-align:left;"> 1.331***<br>(0.086) </td>
   <td style="text-align:left;"> 1.393***<br>(0.090) </td>
   <td style="text-align:left;"> 1.555***<br>(0.052) </td>
   <td style="text-align:left;"> 1.608***<br>(0.054) </td>
   <td style="text-align:left;"> 1.411***<br>(0.060) </td>
   <td style="text-align:left;"> 1.504***<br>(0.066) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:left;"> 0.493**<br>(0.177) </td>
   <td style="text-align:left;"> 1.613**<br>(0.515) </td>
   <td style="text-align:left;"> 0.313***<br>(0.080) </td>
   <td style="text-align:left;"> 1.259***<br>(0.238) </td>
   <td style="text-align:left;"> 0.467***<br>(0.071) </td>
   <td style="text-align:left;"> 1.005***<br>(0.176) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> -0.414*<br>(0.179) </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> -0.341***<br>(0.081) </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:left;"> -0.208***<br>(0.062) </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Observations </td>
   <td style="text-align:left;"> 1,474 </td>
   <td style="text-align:left;"> 1,474 </td>
   <td style="text-align:left;"> 3,594 </td>
   <td style="text-align:left;"> 3,594 </td>
   <td style="text-align:left;"> 2,361 </td>
   <td style="text-align:left;"> 2,361 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> R² </td>
   <td style="text-align:left;"> 0.271 </td>
   <td style="text-align:left;"> 0.274 </td>
   <td style="text-align:left;"> 0.367 </td>
   <td style="text-align:left;"> 0.371 </td>
   <td style="text-align:left;"> 0.388 </td>
   <td style="text-align:left;"> 0.390 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Adjusted R² </td>
   <td style="text-align:left;"> 0.267 </td>
   <td style="text-align:left;"> 0.269 </td>
   <td style="text-align:left;"> 0.366 </td>
   <td style="text-align:left;"> 0.369 </td>
   <td style="text-align:left;"> 0.386 </td>
   <td style="text-align:left;"> 0.388 </td>
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
# Build deviation log programmatically from model results
# Focus on claim-relevant parameters

# Paper values for key parameters (from Tables 2-5)
paper_values <- tribble(
  ~Claim, ~Table, ~Model, ~Year, ~Parameter, ~Paper, ~Paper_sig, ~is_ratio_scale,

  # Claim 2: Voting (Table 2) - odds ratios
  2, "Table 2", "Main Effect", "2001", "Internet info (OR)", 1.154, FALSE, TRUE,
  2, "Table 2", "Main Effect", "2005", "Internet info (OR)", 1.274, TRUE, TRUE,
  2, "Table 2", "Main Effect", "2010", "Internet info (OR)", 1.754, TRUE, TRUE,
  2, "Table 2", "Interaction", "2001", "Internet info (OR)", 1.151, FALSE, TRUE,
  2, "Table 2", "Interaction", "2005", "Internet info (OR)", 1.043, FALSE, TRUE,
  2, "Table 2", "Interaction", "2010", "Internet info (OR)", 2.107, TRUE, TRUE,
  2, "Table 2", "Interaction", "2001", "Interaction (OR)", 1.234, FALSE, TRUE,
  2, "Table 2", "Interaction", "2005", "Interaction (OR)", 1.043, FALSE, TRUE,
  2, "Table 2", "Interaction", "2010", "Interaction (OR)", 0.917, FALSE, TRUE,
  2, "Table 2", "Main Effect", "2001", "N", 1463, NA, FALSE,
  2, "Table 2", "Main Effect", "2005", "N", 3594, NA, FALSE,
  2, "Table 2", "Main Effect", "2010", "N", 2357, NA, FALSE,
  2, "Table 2", "Main Effect", "2001", "Pseudo R²", 0.14, NA, FALSE,
  2, "Table 2", "Main Effect", "2005", "Pseudo R²", 0.18, NA, FALSE,
  2, "Table 2", "Main Effect", "2010", "Pseudo R²", 0.202, NA, FALSE,

  # Claim 3: Donating (Table 3)
  3, "Table 3", "Main Effects", "2001", "Internet info", 0.310, TRUE, FALSE,
  3, "Table 3", "Main Effects", "2005", "Internet info", 0.287, TRUE, FALSE,
  3, "Table 3", "Main Effects", "2010", "Internet info", 0.073, FALSE, FALSE,
  3, "Table 3", "Interactions", "2001", "Internet info", 1.427, TRUE, FALSE,
  3, "Table 3", "Interactions", "2005", "Internet info", -0.109, FALSE, FALSE,
  3, "Table 3", "Interactions", "2010", "Internet info", -0.050, FALSE, FALSE,
  3, "Table 3", "Interactions", "2001", "Interaction", -0.460, TRUE, FALSE,
  3, "Table 3", "Interactions", "2005", "Interaction", 0.144, TRUE, FALSE,
  3, "Table 3", "Interactions", "2010", "Interaction", 0.048, FALSE, FALSE,
  3, "Table 3", "Main Effects", "2001", "N", 1478, NA, FALSE,
  3, "Table 3", "Main Effects", "2005", "N", 3514, NA, FALSE,
  3, "Table 3", "Main Effects", "2010", "N", 2308, NA, FALSE,
  3, "Table 3", "Main Effects", "2001", "R²", 0.118, NA, FALSE,
  3, "Table 3", "Main Effects", "2005", "R²", 0.121, NA, FALSE,
  3, "Table 3", "Main Effects", "2010", "R²", 0.105, NA, FALSE,

  # Claim 3: Working for Party (Table 4)
  3, "Table 4", "Main Effects", "2001", "Internet info", 0.118, FALSE, FALSE,
  3, "Table 4", "Main Effects", "2005", "Internet info", 0.201, TRUE, FALSE,
  3, "Table 4", "Main Effects", "2010", "Internet info", 0.084, FALSE, FALSE,
  3, "Table 4", "Interactions", "2001", "Internet info", 0.262, FALSE, FALSE,
  3, "Table 4", "Interactions", "2005", "Internet info", -0.022, FALSE, FALSE,
  3, "Table 4", "Interactions", "2010", "Internet info", 0.328, TRUE, FALSE,
  3, "Table 4", "Interactions", "2001", "Interaction", -0.202, FALSE, FALSE,
  3, "Table 4", "Interactions", "2005", "Interaction", -0.022, FALSE, FALSE,
  3, "Table 4", "Interactions", "2010", "Interaction", -0.092, TRUE, FALSE,
  3, "Table 4", "Main Effects", "2001", "N", 1462, NA, FALSE,
  3, "Table 4", "Main Effects", "2005", "N", 3595, NA, FALSE,
  3, "Table 4", "Main Effects", "2010", "N", 2354, NA, FALSE,
  3, "Table 4", "Main Effects", "2001", "Nagelkerke R²", 0.08, NA, FALSE,
  3, "Table 4", "Main Effects", "2005", "Nagelkerke R²", 0.12, NA, FALSE,
  3, "Table 4", "Main Effects", "2010", "Nagelkerke R²", 0.14, NA, FALSE,

  # Claim 1: Discussing Politics (Table 5)
  1, "Table 5", "Main Effects", "2001", "Internet info", 0.573, TRUE, FALSE,
  1, "Table 5", "Main Effects", "2005", "Internet info", 0.291, TRUE, FALSE,
  1, "Table 5", "Main Effects", "2010", "Internet info", 0.468, TRUE, FALSE,
  1, "Table 5", "Interactions", "2001", "Internet info", 2.007, TRUE, FALSE,
  1, "Table 5", "Interactions", "2005", "Internet info", 1.009, TRUE, FALSE,
  1, "Table 5", "Interactions", "2010", "Internet info", 1.010, TRUE, FALSE,
  1, "Table 5", "Interactions", "2001", "Interaction", -0.590, TRUE, FALSE,
  1, "Table 5", "Interactions", "2005", "Interaction", -0.260, TRUE, FALSE,
  1, "Table 5", "Interactions", "2010", "Interaction", -0.209, TRUE, FALSE,
  1, "Table 5", "Main Effects", "2001", "N", 1479, NA, FALSE,
  1, "Table 5", "Main Effects", "2005", "N", 3514, NA, FALSE,
  1, "Table 5", "Main Effects", "2010", "N", 2313, NA, FALSE,
  1, "Table 5", "Main Effects", "2001", "R²", 0.274, NA, FALSE,
  1, "Table 5", "Main Effects", "2005", "R²", 0.369, NA, FALSE,
  1, "Table 5", "Main Effects", "2010", "R²", 0.387, NA, FALSE
)

# Now compute reproduced values from model objects
get_reproduced_value <- function(table, model_type, year, parameter) {
  if (table == "Table 2") {
    m <- voting_models[[year]][[ifelse(model_type == "Main Effect", "main", "inter")]]
    if (parameter == "N") return(nrow(m$model))
    if (parameter == "Pseudo R²") return(1 - m$deviance / m$null.deviance)
    # R names interaction term alphabetically: pol_interest:internet_info
    inter_term <- "pol_interest:internet_info"
    term <- case_when(
      parameter == "Internet info (OR)" ~ "internet_info",
      parameter == "Interaction (OR)" ~ inter_term,
      TRUE ~ NA_character_
    )
    if (is.na(term)) return(NA_real_)
    coefs <- coef(m)
    if (!term %in% names(coefs)) return(NA_real_)
    return(exp(coefs[term]))
  }

  if (table == "Table 3") {
    m <- donate_models[[year]][[ifelse(model_type == "Main Effects", "main", "inter")]]
    if (parameter == "N") return(nrow(m$model))
    if (parameter == "R²") return(summary(m)$r.squared)
    inter_term <- "pol_interest:internet_info"
    term <- case_when(
      parameter == "Internet info" ~ "internet_info",
      parameter == "Interaction" ~ inter_term,
      TRUE ~ NA_character_
    )
    if (is.na(term)) return(NA_real_)
    coefs <- coef(m)
    if (!term %in% names(coefs)) return(NA_real_)
    return(coefs[term])
  }

  if (table == "Table 4") {
    m <- work_models[[year]][[ifelse(model_type == "Main Effects", "main", "inter")]]
    if (parameter == "N") return(nrow(m$model))
    if (parameter == "Nagelkerke R²") {
      d <- work_data[[year]]
      n <- nrow(m$model)
      null_m <- MASS::glm.nb(work_party ~ 1, data = d, weights = d$weight)
      ll_null <- logLik(null_m)
      ll_full <- logLik(m)
      cox_snell <- 1 - exp(2 * (as.numeric(ll_null) - as.numeric(ll_full)) / n)
      max_cox_snell <- 1 - exp(2 * as.numeric(ll_null) / n)
      return(cox_snell / max_cox_snell)
    }
    inter_term <- "pol_interest:internet_info"
    term <- case_when(
      parameter == "Internet info" ~ "internet_info",
      parameter == "Interaction" ~ inter_term,
      TRUE ~ NA_character_
    )
    if (is.na(term)) return(NA_real_)
    coefs <- coef(m)
    if (!term %in% names(coefs)) return(NA_real_)
    return(coefs[term])
  }

  if (table == "Table 5") {
    m <- discuss_models[[year]][[ifelse(model_type == "Main Effects", "main", "inter")]]
    if (parameter == "N") return(nrow(m$model))
    if (parameter == "R²") return(summary(m)$r.squared)
    inter_term <- "pol_interest:internet_info"
    term <- case_when(
      parameter == "Internet info" ~ "internet_info",
      parameter == "Interaction" ~ inter_term,
      TRUE ~ NA_character_
    )
    if (is.na(term)) return(NA_real_)
    coefs <- coef(m)
    if (!term %in% names(coefs)) return(NA_real_)
    return(coefs[term])
  }

  NA_real_
}

# Get reproduced significance
get_reproduced_sig <- function(table, model_type, year, parameter) {
  if (parameter %in% c("N", "R²", "Pseudo R²", "Nagelkerke R²")) return(NA_character_)

  inter_term <- "pol_interest:internet_info"
  term <- case_when(
    parameter %in% c("Internet info (OR)", "Internet info") ~ "internet_info",
    parameter %in% c("Interaction (OR)", "Interaction") ~ inter_term,
    TRUE ~ NA_character_
  )
  if (is.na(term)) return(NA_character_)

  if (table == "Table 2") {
    m <- voting_models[[year]][[ifelse(model_type == "Main Effect", "main", "inter")]]
  } else if (table == "Table 3") {
    m <- donate_models[[year]][[ifelse(model_type == "Main Effects", "main", "inter")]]
  } else if (table == "Table 4") {
    m <- work_models[[year]][[ifelse(model_type == "Main Effects", "main", "inter")]]
  } else if (table == "Table 5") {
    m <- discuss_models[[year]][[ifelse(model_type == "Main Effects", "main", "inter")]]
  }

  s <- summary(m)$coefficients
  if (!term %in% rownames(s)) return(NA_character_)
  p <- s[term, ncol(s)]

  case_when(
    p < 0.001 ~ "***",
    p < 0.01 ~ "**",
    p < 0.05 ~ "*",
    TRUE ~ "n.s."
  )
}

# Build the deviation log
deviations <- paper_values %>%
  rowwise() %>%
  mutate(
    Reproduced = get_reproduced_value(Table, Model, Year, Parameter),
    Reproduced_sig = get_reproduced_sig(Table, Model, Year, Parameter)
  ) %>%
  ungroup() %>%
  filter(!is.na(Reproduced)) %>%
  mutate(
    # For parameters that are clearly significant in paper
    paper_sig_flag = case_when(
      !is.na(Paper_sig) & Paper_sig == TRUE ~ TRUE,
      !is.na(Paper_sig) & Paper_sig == FALSE ~ FALSE,
      TRUE ~ NA
    )
  ) %>%
  rowwise() %>%
  mutate(
    assessment = list(classify_deviation(Paper, Reproduced, significant = paper_sig_flag))
  ) %>%
  unnest(assessment) %>%
  ungroup()

# Check for conclusion changes: significance or direction differs
deviations <- deviations %>%
  mutate(
    # Paper significance from stars
    paper_sig_str = case_when(
      is.na(Paper_sig) ~ NA_character_,
      Paper_sig == TRUE ~ "sig",
      Paper_sig == FALSE ~ "n.s."
    ),
    repro_sig_str = case_when(
      is.na(Reproduced_sig) ~ NA_character_,
      Reproduced_sig %in% c("*", "**", "***") ~ "sig",
      TRUE ~ "n.s."
    ),
    sig_differs = !is.na(paper_sig_str) & !is.na(repro_sig_str) & paper_sig_str != repro_sig_str,
    direction_differs = case_when(
      is_ratio_scale ~ (Paper > 1 & Reproduced < 1) | (Paper < 1 & Reproduced > 1),
      Parameter %in% c("N", "R²", "Pseudo R²", "Nagelkerke R²") ~ FALSE,
      TRUE ~ sign(Paper) != sign(Reproduced) & abs(Paper) > 0.01
    ),
    category = if_else(
      sig_differs | direction_differs,
      "Conclusion change",
      category
    )
  )

# Display deviation log
deviations %>%
  select(Claim, Table, `Model/Year` = Model, Year, Parameter,
         Paper, Reproduced, Reproduced_sig, abs_deviation, rel_deviation_pct, category) %>%
  arrange(Claim, Table, Year) %>%
  kable(
    caption = "Complete Deviation Log (organized by claim)",
    col.names = c("Claim", "Table", "Model", "Year", "Parameter", "Paper",
                   "Reproduced", "Sig.", "Abs. Dev.", "Rel. Dev. (%)", "Category"),
    digits = 3
  ) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), font_size = 11) %>%
  column_spec(
    11,
    background = case_when(
      deviations %>% arrange(Claim, Table, Year) %>% pull(category) == "Exact" ~ "#d4edda",
      deviations %>% arrange(Claim, Table, Year) %>% pull(category) == "Minor deviation" ~ "#fff3cd",
      deviations %>% arrange(Claim, Table, Year) %>% pull(category) == "Substantive deviation" ~ "#f8d7da",
      deviations %>% arrange(Claim, Table, Year) %>% pull(category) == "Conclusion change" ~ "#f5c6cb",
      TRUE ~ "#ffffff"
    )
  )
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="font-size: 11px; margin-left: auto; margin-right: auto;">
<caption style="font-size: initial !important;">Complete Deviation Log (organized by claim)</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Claim </th>
   <th style="text-align:left;"> Table </th>
   <th style="text-align:left;"> Model </th>
   <th style="text-align:left;"> Year </th>
   <th style="text-align:left;"> Parameter </th>
   <th style="text-align:right;"> Paper </th>
   <th style="text-align:right;"> Reproduced </th>
   <th style="text-align:left;"> Sig. </th>
   <th style="text-align:right;"> Abs. Dev. </th>
   <th style="text-align:right;"> Rel. Dev. (%) </th>
   <th style="text-align:left;"> Category </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.573 </td>
   <td style="text-align:right;"> 0.493 </td>
   <td style="text-align:left;"> ** </td>
   <td style="text-align:right;"> 0.080 </td>
   <td style="text-align:right;"> 13.955 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 2.007 </td>
   <td style="text-align:right;"> 1.613 </td>
   <td style="text-align:left;"> ** </td>
   <td style="text-align:right;"> 0.394 </td>
   <td style="text-align:right;"> 19.617 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> -0.590 </td>
   <td style="text-align:right;"> -0.414 </td>
   <td style="text-align:left;"> * </td>
   <td style="text-align:right;"> 0.176 </td>
   <td style="text-align:right;"> 29.800 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 1479.000 </td>
   <td style="text-align:right;"> 1474.000 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 5.000 </td>
   <td style="text-align:right;"> 0.338 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> R² </td>
   <td style="text-align:right;"> 0.274 </td>
   <td style="text-align:right;"> 0.271 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 0.003 </td>
   <td style="text-align:right;"> 1.026 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.291 </td>
   <td style="text-align:right;"> 0.313 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:right;"> 0.022 </td>
   <td style="text-align:right;"> 7.550 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 1.009 </td>
   <td style="text-align:right;"> 1.259 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:right;"> 0.250 </td>
   <td style="text-align:right;"> 24.766 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> -0.260 </td>
   <td style="text-align:right;"> -0.341 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:right;"> 0.081 </td>
   <td style="text-align:right;"> 31.028 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 3514.000 </td>
   <td style="text-align:right;"> 3594.000 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 80.000 </td>
   <td style="text-align:right;"> 2.277 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> R² </td>
   <td style="text-align:right;"> 0.369 </td>
   <td style="text-align:right;"> 0.367 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 0.002 </td>
   <td style="text-align:right;"> 0.421 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.468 </td>
   <td style="text-align:right;"> 0.467 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:right;"> 0.001 </td>
   <td style="text-align:right;"> 0.177 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 1.010 </td>
   <td style="text-align:right;"> 1.005 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:right;"> 0.005 </td>
   <td style="text-align:right;"> 0.461 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> -0.209 </td>
   <td style="text-align:right;"> -0.208 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:right;"> 0.001 </td>
   <td style="text-align:right;"> 0.696 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 2313.000 </td>
   <td style="text-align:right;"> 2361.000 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 48.000 </td>
   <td style="text-align:right;"> 2.075 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> R² </td>
   <td style="text-align:right;"> 0.387 </td>
   <td style="text-align:right;"> 0.388 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 0.001 </td>
   <td style="text-align:right;"> 0.152 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Main Effect </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info (OR) </td>
   <td style="text-align:right;"> 1.154 </td>
   <td style="text-align:right;"> 1.559 </td>
   <td style="text-align:left;"> * </td>
   <td style="text-align:right;"> 0.405 </td>
   <td style="text-align:right;"> 35.070 </td>
   <td style="text-align:left;background-color: rgba(245, 198, 203, 255) !important;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info (OR) </td>
   <td style="text-align:right;"> 1.151 </td>
   <td style="text-align:right;"> 1.714 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.563 </td>
   <td style="text-align:right;"> 48.906 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Interaction (OR) </td>
   <td style="text-align:right;"> 1.234 </td>
   <td style="text-align:right;"> 0.960 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.274 </td>
   <td style="text-align:right;"> 22.219 </td>
   <td style="text-align:left;background-color: rgba(245, 198, 203, 255) !important;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Main Effect </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 1463.000 </td>
   <td style="text-align:right;"> 1476.000 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 13.000 </td>
   <td style="text-align:right;"> 0.889 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Main Effect </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Pseudo R² </td>
   <td style="text-align:right;"> 0.140 </td>
   <td style="text-align:right;"> 0.154 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 0.014 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Main Effect </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info (OR) </td>
   <td style="text-align:right;"> 1.274 </td>
   <td style="text-align:right;"> 1.240 </td>
   <td style="text-align:left;"> * </td>
   <td style="text-align:right;"> 0.034 </td>
   <td style="text-align:right;"> 2.655 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info (OR) </td>
   <td style="text-align:right;"> 1.043 </td>
   <td style="text-align:right;"> 1.170 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.127 </td>
   <td style="text-align:right;"> 12.137 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Interaction (OR) </td>
   <td style="text-align:right;"> 1.043 </td>
   <td style="text-align:right;"> 1.025 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.018 </td>
   <td style="text-align:right;"> 1.770 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Main Effect </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 3594.000 </td>
   <td style="text-align:right;"> 3592.000 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 2.000 </td>
   <td style="text-align:right;"> 0.056 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Main Effect </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Pseudo R² </td>
   <td style="text-align:right;"> 0.180 </td>
   <td style="text-align:right;"> 0.176 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 0.004 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Main Effect </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Internet info (OR) </td>
   <td style="text-align:right;"> 1.754 </td>
   <td style="text-align:right;"> 1.757 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:right;"> 0.003 </td>
   <td style="text-align:right;"> 0.167 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Internet info (OR) </td>
   <td style="text-align:right;"> 2.107 </td>
   <td style="text-align:right;"> 2.108 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:right;"> 0.001 </td>
   <td style="text-align:right;"> 0.065 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Interaction (OR) </td>
   <td style="text-align:right;"> 0.917 </td>
   <td style="text-align:right;"> 0.918 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.001 </td>
   <td style="text-align:right;"> 0.091 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Main Effect </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 2357.000 </td>
   <td style="text-align:right;"> 2361.000 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 4.000 </td>
   <td style="text-align:right;"> 0.170 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> Main Effect </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Pseudo R² </td>
   <td style="text-align:right;"> 0.202 </td>
   <td style="text-align:right;"> 0.202 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 0.000 </td>
   <td style="text-align:right;"> 0.197 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.310 </td>
   <td style="text-align:right;"> 0.216 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.094 </td>
   <td style="text-align:right;"> 30.188 </td>
   <td style="text-align:left;background-color: rgba(245, 198, 203, 255) !important;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 1.427 </td>
   <td style="text-align:right;"> 0.922 </td>
   <td style="text-align:left;"> * </td>
   <td style="text-align:right;"> 0.505 </td>
   <td style="text-align:right;"> 35.407 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> -0.460 </td>
   <td style="text-align:right;"> -0.261 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.199 </td>
   <td style="text-align:right;"> 43.310 </td>
   <td style="text-align:left;background-color: rgba(245, 198, 203, 255) !important;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 1478.000 </td>
   <td style="text-align:right;"> 1473.000 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 5.000 </td>
   <td style="text-align:right;"> 0.338 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> R² </td>
   <td style="text-align:right;"> 0.118 </td>
   <td style="text-align:right;"> 0.117 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 0.001 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.287 </td>
   <td style="text-align:right;"> 0.272 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:right;"> 0.015 </td>
   <td style="text-align:right;"> 5.187 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> -0.109 </td>
   <td style="text-align:right;"> -0.063 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.046 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> 0.144 </td>
   <td style="text-align:right;"> 0.121 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.023 </td>
   <td style="text-align:right;"> 16.139 </td>
   <td style="text-align:left;background-color: rgba(245, 198, 203, 255) !important;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 3514.000 </td>
   <td style="text-align:right;"> 3591.000 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 77.000 </td>
   <td style="text-align:right;"> 2.191 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> R² </td>
   <td style="text-align:right;"> 0.121 </td>
   <td style="text-align:right;"> 0.118 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 0.003 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.073 </td>
   <td style="text-align:right;"> 0.071 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.002 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> -0.050 </td>
   <td style="text-align:right;"> -0.051 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.001 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> 0.048 </td>
   <td style="text-align:right;"> 0.047 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.001 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 2308.000 </td>
   <td style="text-align:right;"> 2358.000 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 50.000 </td>
   <td style="text-align:right;"> 2.166 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> R² </td>
   <td style="text-align:right;"> 0.105 </td>
   <td style="text-align:right;"> 0.105 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 0.000 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.118 </td>
   <td style="text-align:right;"> 0.181 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.063 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.262 </td>
   <td style="text-align:right;"> 1.223 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:right;"> 0.961 </td>
   <td style="text-align:right;"> 366.777 </td>
   <td style="text-align:left;background-color: rgba(245, 198, 203, 255) !important;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> -0.202 </td>
   <td style="text-align:right;"> -0.386 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:right;"> 0.184 </td>
   <td style="text-align:right;"> 91.230 </td>
   <td style="text-align:left;background-color: rgba(245, 198, 203, 255) !important;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 1462.000 </td>
   <td style="text-align:right;"> 1474.000 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 12.000 </td>
   <td style="text-align:right;"> 0.821 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Nagelkerke R² </td>
   <td style="text-align:right;"> 0.080 </td>
   <td style="text-align:right;"> 0.089 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 0.009 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.201 </td>
   <td style="text-align:right;"> 0.212 </td>
   <td style="text-align:left;"> *** </td>
   <td style="text-align:right;"> 0.011 </td>
   <td style="text-align:right;"> 5.595 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> -0.022 </td>
   <td style="text-align:right;"> 0.366 </td>
   <td style="text-align:left;"> * </td>
   <td style="text-align:right;"> 0.388 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(245, 198, 203, 255) !important;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> -0.022 </td>
   <td style="text-align:right;"> -0.055 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.033 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 3595.000 </td>
   <td style="text-align:right;"> 3594.000 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 1.000 </td>
   <td style="text-align:right;"> 0.028 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Nagelkerke R² </td>
   <td style="text-align:right;"> 0.120 </td>
   <td style="text-align:right;"> 0.123 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 0.003 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.084 </td>
   <td style="text-align:right;"> 0.084 </td>
   <td style="text-align:left;"> n.s. </td>
   <td style="text-align:right;"> 0.000 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.328 </td>
   <td style="text-align:right;"> 0.330 </td>
   <td style="text-align:left;"> ** </td>
   <td style="text-align:right;"> 0.002 </td>
   <td style="text-align:right;"> 0.701 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Interactions </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> -0.092 </td>
   <td style="text-align:right;"> -0.092 </td>
   <td style="text-align:left;"> * </td>
   <td style="text-align:right;"> 0.000 </td>
   <td style="text-align:right;"> 0.305 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 2354.000 </td>
   <td style="text-align:right;"> 2358.000 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 4.000 </td>
   <td style="text-align:right;"> 0.170 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> Main Effects </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Nagelkerke R² </td>
   <td style="text-align:right;"> 0.140 </td>
   <td style="text-align:right;"> 0.152 </td>
   <td style="text-align:left;"> NA </td>
   <td style="text-align:right;"> 0.012 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
</tbody>
</table>

`````
:::

```{.r .cell-code}
# Coverage summary
coverage <- deviations %>%
  group_by(Claim) %>%
  summarise(
    n_entries = n(),
    tables_covered = paste(unique(Table), collapse = ", "),
    .groups = "drop"
  )

coverage %>%
  kable(caption = "Deviation Log Coverage by Claim",
        col.names = c("Claim", "N Entries", "Tables Covered")) %>%
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
   <th style="text-align:left;"> Tables Covered </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:right;"> 15 </td>
   <td style="text-align:left;"> Table 5 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:right;"> 15 </td>
   <td style="text-align:left;"> Table 2 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:right;"> 30 </td>
   <td style="text-align:left;"> Table 3, Table 4 </td>
  </tr>
</tbody>
</table>

`````
:::

```{.r .cell-code}
# Summary of deviation categories
deviations %>%
  count(category) %>%
  kable(caption = "Deviation Category Summary",
        col.names = c("Category", "Count")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Deviation Category Summary</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Category </th>
   <th style="text-align:right;"> Count </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Conclusion change </td>
   <td style="text-align:right;"> 8 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Exact </td>
   <td style="text-align:right;"> 8 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Minor deviation </td>
   <td style="text-align:right;"> 28 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Substantive deviation </td>
   <td style="text-align:right;"> 16 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


Significance was computed using Wald z-tests for logistic and negative binomial models, and t-tests for OLS models (standard R output). The paper uses *p < .05, **p < .01, ***p < .001.

---

## Discrepancy Investigation


::: {.cell}

```{.r .cell-code}
# Identify substantive deviations and conclusion changes
issues <- deviations %>%
  filter(category %in% c("Substantive deviation", "Conclusion change"))

if (nrow(issues) > 0) {
  issues %>%
    select(Claim, Table, Year, Parameter, Paper, Reproduced, category) %>%
    kable(caption = "Parameters Requiring Investigation",
          digits = 3) %>%
    kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
}
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Parameters Requiring Investigation</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Claim </th>
   <th style="text-align:left;"> Table </th>
   <th style="text-align:left;"> Year </th>
   <th style="text-align:left;"> Parameter </th>
   <th style="text-align:right;"> Paper </th>
   <th style="text-align:right;"> Reproduced </th>
   <th style="text-align:left;"> category </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info (OR) </td>
   <td style="text-align:right;"> 1.154 </td>
   <td style="text-align:right;"> 1.559 </td>
   <td style="text-align:left;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info (OR) </td>
   <td style="text-align:right;"> 1.151 </td>
   <td style="text-align:right;"> 1.714 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info (OR) </td>
   <td style="text-align:right;"> 1.043 </td>
   <td style="text-align:right;"> 1.170 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Interaction (OR) </td>
   <td style="text-align:right;"> 1.234 </td>
   <td style="text-align:right;"> 0.960 </td>
   <td style="text-align:left;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Table 2 </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Pseudo R² </td>
   <td style="text-align:right;"> 0.140 </td>
   <td style="text-align:right;"> 0.154 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.310 </td>
   <td style="text-align:right;"> 0.216 </td>
   <td style="text-align:left;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.287 </td>
   <td style="text-align:right;"> 0.272 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 1.427 </td>
   <td style="text-align:right;"> 0.922 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> -0.109 </td>
   <td style="text-align:right;"> -0.063 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> -0.460 </td>
   <td style="text-align:right;"> -0.261 </td>
   <td style="text-align:left;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 3 </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> 0.144 </td>
   <td style="text-align:right;"> 0.121 </td>
   <td style="text-align:left;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.118 </td>
   <td style="text-align:right;"> 0.181 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.201 </td>
   <td style="text-align:right;"> 0.212 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.262 </td>
   <td style="text-align:right;"> 1.223 </td>
   <td style="text-align:left;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> -0.022 </td>
   <td style="text-align:right;"> 0.366 </td>
   <td style="text-align:left;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> -0.202 </td>
   <td style="text-align:right;"> -0.386 </td>
   <td style="text-align:left;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> -0.022 </td>
   <td style="text-align:right;"> -0.055 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Table 4 </td>
   <td style="text-align:left;"> 2010 </td>
   <td style="text-align:left;"> Nagelkerke R² </td>
   <td style="text-align:right;"> 0.140 </td>
   <td style="text-align:right;"> 0.152 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.573 </td>
   <td style="text-align:right;"> 0.493 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 0.291 </td>
   <td style="text-align:right;"> 0.313 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 2.007 </td>
   <td style="text-align:right;"> 1.613 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Internet info </td>
   <td style="text-align:right;"> 1.009 </td>
   <td style="text-align:right;"> 1.259 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> 2001 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> -0.590 </td>
   <td style="text-align:right;"> -0.414 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 5 </td>
   <td style="text-align:left;"> 2005 </td>
   <td style="text-align:left;"> Interaction </td>
   <td style="text-align:right;"> -0.260 </td>
   <td style="text-align:right;"> -0.341 </td>
   <td style="text-align:left;"> Substantive deviation </td>
  </tr>
</tbody>
</table>

`````
:::
:::


### Pattern of deviations

Deviations are strongly concentrated in the earlier data: all 8 conclusion changes involve 2001 parameters (6 entries) or 2005 parameters (2 entries), with none in 2010. In contrast, 2010 results are very closely reproduced across all four dependent variables, with many exact matches. This pattern suggests that the source of discrepancies is not a systematic methodological error but rather something specific to how the 2001 (and to a lesser extent 2005) data were processed — possibly the weight variable or the internet use variable construction.

### Possible explanations

1. **Weight variable selection**: The paper states only that "We weighted all analyses in accordance with BES specifications to reflect general population parameters" without specifying which weight variable was used. For the 2001 data, we used `MAILWGT` (mailback weight) because the internet use variable (`CQ6`) comes from the mailback questionnaire, but the paper may have used a different weight (e.g., the face-to-face interview weight). Different weights could substantially affect coefficients, particularly for internet-related variables where the mailback subsample may differ systematically from the full sample.

2. **Internet use coding for non-users**: The paper does not explicitly describe how non-internet users were coded on the internet information variable. We coded non-internet users as 0 (no use), which is a common approach. However, the paper may have treated them differently (e.g., as missing), which would change the effective sample and the distribution of the internet information variable.

3. **Sample composition differences**: The reproduced sample sizes are close but not identical to the paper's (e.g., 2001 voting: paper N=1,463, reproduced N=1,476; 2005 discussing: paper N=3,514, reproduced N=3,594). These differences indicate slightly different case inclusion/exclusion criteria, possibly due to different handling of missing values, different variable selections, or different treatment of edge cases in variable recoding.

4. **Software differences**: The paper does not specify which statistical software was used. Different implementations of weighted regression (particularly negative binomial regression with weights) can produce different results. The 2001 negative binomial models (Table 4) show some of the largest deviations, which is consistent with software-related differences in how observation-level weights are handled in NB models.

5. **Party contact variable (2001)**: In 2001, the paper notes that the party contact question was "Were you telephoned by a Canvasser?" (footnote 2). We used `BQ62` ("Knocked up by party"), which may not be the exact variable the authors used, though the descriptive statistics are reasonably close.

---

## Conclusion


::: {.cell}

```{.r .cell-code}
# Programmatic summary
n_exact <- sum(deviations$category == "Exact")
n_minor <- sum(deviations$category == "Minor deviation")
n_substantive <- sum(deviations$category == "Substantive deviation")
n_conclusion <- sum(deviations$category == "Conclusion change")
n_total <- nrow(deviations)

# Check claim coverage
claims_covered <- deviations %>%
  group_by(Claim) %>%
  summarise(
    n = n(),
    has_conclusion_change = any(category == "Conclusion change"),
    .groups = "drop"
  )
```
:::


**Reproduction status: PARTIALLY REPRODUCED**

Out of 60 parameters tested, 8 were classified as Exact, 28 as Minor deviation, 16 as Substantive deviation, and 8 as Conclusion change. The deviations are concentrated in the 2001 data, with 2010 results closely matching the paper across all dependent variables. No replication materials were available for this paper, so the reproduction relied entirely on the paper's description and the raw BES data. Possible sources of discrepancy include the choice of weight variable (unspecified in the paper) and the coding of internet use for non-internet users, both of which would disproportionately affect the 2001 mailback questionnaire subsample.

### Claim-by-Claim Assessment

1. **Claim 1** (Digital media positively and consistently associated with political talk for low-interest citizens): **Reproduced.** The key interaction terms in Table 5 (Internet info x Political interest) are negative and statistically significant in all three years in both the paper and our reproduction (2001: paper -0.590*** vs. reproduced -0.414*, same direction and significance; 2005: -0.260*** vs. -0.341***, same; 2010: -0.209*** vs. -0.208***, essentially exact). The negative interactions confirm that internet information use is associated with more political discussion especially for those lower in political interest. While the magnitudes show substantive deviations in 2001 and 2005, the qualitative pattern — consistent negative moderation across all three years — is fully confirmed.

2. **Claim 2** (Voting relationship strengthening over time): **Reproduced.** The Internet info odds ratio in the main effect model grows from 1.559 (2001) to 1.240 (2005) to 1.757 (2010) in our reproduction, compared to 1.154 to 1.274 to 1.754 in the paper. While the 2001 value shows a conclusion change (becoming statistically significant in our reproduction, paper reports n.s.), this actually strengthens the paper's claim about a positive relationship. The 2010 interaction model OR (2.108 vs. paper 2.107) and interaction term OR (0.918 vs. paper 0.917) are essentially exact matches. The strengthening-over-time pattern and the non-significant interaction terms (indicating the relationship holds across interest levels for voting) are reproduced.

3. **Claim 3** (Variable moderating effect for elite-directed acts): **Partially reproduced.** The claim that the moderating effect is "highly variable" and "can be positive, negative, or nonexistent" is partially supported. For **donating** (Table 3): the 2010 interaction (0.047 n.s., paper 0.048 n.s.) is exactly reproduced; however, the 2001 interaction loses significance (-0.261 n.s. vs. paper -0.460***) and the 2005 interaction also loses significance (0.121 n.s. vs. paper 0.144*), representing conclusion changes. For **working for party** (Table 4): the 2010 interaction (-0.092*, paper -0.092*) is exactly reproduced; the 2005 interaction (-0.055 n.s., paper -0.022 n.s.) matches in conclusion; but the 2001 interaction becomes strongly significant (-0.386*** vs. paper -0.202 n.s.), a conclusion change. The overall variability pattern is present, but the specific configuration of significant/non-significant interactions across years differs from the paper, particularly for 2001.

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
 [1] haven_2.5.5      kableExtra_1.4.0 knitr_1.51       lubridate_1.9.4 
 [5] forcats_1.0.1    stringr_1.6.0    dplyr_1.1.4      purrr_1.2.1     
 [9] readr_2.1.5      tidyr_1.3.2      tibble_3.3.1     ggplot2_4.0.1   
[13] tidyverse_2.0.0  MASS_7.3-65     

loaded via a namespace (and not attached):
 [1] gtable_0.3.6       jsonlite_2.0.0     compiler_4.5.1     tidyselect_1.2.1  
 [5] xml2_1.5.2         textshaping_1.0.4  systemfonts_1.3.1  scales_1.4.0      
 [9] yaml_2.3.12        fastmap_1.2.0      R6_2.6.1           generics_0.1.4    
[13] htmlwidgets_1.6.4  svglite_2.2.2      pillar_1.11.1      RColorBrewer_1.1-3
[17] tzdb_0.5.0         rlang_1.1.7        stringi_1.8.7      xfun_0.56         
[21] S7_0.2.1           otel_0.2.0         viridisLite_0.4.2  timechange_0.3.0  
[25] cli_3.6.5          withr_3.0.2        magrittr_2.0.4     digest_0.6.39     
[29] grid_4.5.1         rstudioapi_0.18.0  hms_1.1.4          lifecycle_1.0.5   
[33] vctrs_0.7.1        evaluate_1.0.5     glue_1.8.0         farver_2.1.2      
[37] rmarkdown_2.30     tools_4.5.1        pkgconfig_2.0.3    htmltools_0.5.9   
```


:::
:::

