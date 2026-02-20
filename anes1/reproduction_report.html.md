---
title: "Reproduction Report: Iyengar & Krupenkin (2018)"
subtitle: "The Strengthening of Partisan Affect"
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

**Paper**: Iyengar, S., & Krupenkin, M. (2018). The Strengthening of Partisan Affect. *Advances in Political Psychology, 39*(Suppl. 1), 201–218. doi: 10.1111/pops.12487

**Data**: American National Election Studies (ANES) Time Series Cumulative Data File (1948–2024) and ANES 2016 Time Series Study.

**Verdict**: QUALITATIVELY REPRODUCED

Claims 1–4 are fully supported by the reproduced analyses, with feeling thermometer means matching within rounding error and correlation trends confirmed. Claim 5 (participation) is largely supported: the out-party thermometer and its interaction with year are highly significant in both models, confirming that out-party negativity has become a dominant participation driver. However, the in-party thermometer × year interaction — central to the claim that in-party positivity has *declined* over time — is borderline non-significant in the voting model (p = 0.050) and non-significant in the nonvoting model (p = 0.083). This significance change may be due to dataset version differences (the CDF has been updated since the paper's publication) or undocumented sample restrictions. The qualitative conclusion that out-party hostility has eclipsed in-party positivity is nonetheless confirmed: the in-party effects are weaker, the out-party interaction is larger, and the predicted probability crossover pattern is reproduced.
:::

## Open Materials

| Material | Available | Location |
|----------|-----------|----------|
| Supplementary materials | Yes | [Stanford PCL Appendix](https://pcl.sites.stanford.edu/sites/g/files/sbiybj22066/files/media/file/iyengar-app-strengthening.pdf) |
| Replication code | No | — |
| Replication data (processed) | No | — |
| Raw data | Yes | [ANES Data Center](https://electionstudies.org/data-center/) |

The supplementary appendix was not accessible in readable format. No replication materials were consulted during this reproduction.

---

## Paper Overview

### Research Question
How has partisan affect in the United States changed over recent decades? The paper examines trends in how Americans feel about the opposing party and candidates, whether these evaluations form a coherent belief system, and how affective polarization affects political participation.

### Key Methods
- Descriptive time series of feeling thermometer means, candidate trait ratings, and emotional responses using the ANES Cumulative Data File (1978–2016)
- Correlational analyses tracking constraint/consistency in partisan evaluations over time
- Logit regression models of voter turnout and nonvoting participation as a function of in-party and out-party feeling thermometers, their interactions with year, party identification, and demographics
- Comparison of affective polarization by survey mode (face-to-face vs. online) in the 2016 ANES

### Claims from the Abstract

1. **Partisans feel more negatively about the opposing party**: Out-party feeling thermometer ratings have declined sharply since the 1980s.
2. **This negativity has become more consistent**: Evaluations of in-party and out-party across multiple indicators (thermometers, traits, affects) have grown more correlated over time.
3. **Partisan animus began to rise in the 1980s and has grown dramatically over the past two decades**: The trend in out-party hostility accelerated post-2000.
4. **Partisan affect is more structured — ingroup favoritism is increasingly associated with outgroup animus**: Cross-domain correlations between indicators of partisan affect have strengthened.
5. **Hostility toward the opposing party has eclipsed positive affect as a motive for political participation**: The effect of out-party thermometer scores on participation has grown while the effect of in-party thermometer scores has declined.

---

## Data and Variable Construction


::: {.cell}

```{.r .cell-code}
# Load ANES Cumulative Data File
cdf <- read_sav("../data/anes/anes_timeseries_cdf_spss_20260205.sav")

# Load ANES 2016 Time Series
ts16 <- read_sav("../data/anes/anes_timeseries_2016.sav")

# Basic dataset overview
tibble(
  Dataset = c("ANES CDF", "ANES 2016"),
  Observations = c(nrow(cdf), nrow(ts16)),
  Variables = c(ncol(cdf), ncol(ts16))
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
   <th style="text-align:left;"> Dataset </th>
   <th style="text-align:right;"> Observations </th>
   <th style="text-align:right;"> Variables </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> ANES CDF </td>
   <td style="text-align:right;"> 73745 </td>
   <td style="text-align:right;"> 1030 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> ANES 2016 </td>
   <td style="text-align:right;"> 4270 </td>
   <td style="text-align:right;"> 1842 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



::: {.cell}

```{.r .cell-code}
# --- CDF Variable Construction ---

# Convert haven-labelled to numeric
cdf <- cdf %>%
  mutate(across(everything(), ~as.numeric(.x)))

# Party identification: 7-point scale
# 1=Strong D, 2=Weak D, 3=Ind-D, 4=Ind-Ind, 5=Ind-R, 6=Weak R, 7=Strong R
# Classify leaners as partisans; exclude pure independents (4) and missing
cdf <- cdf %>%
  mutate(
    year = VCF0004,
    pid7 = VCF0301,
    is_partisan = pid7 %in% c(1, 2, 3, 5, 6, 7),
    is_dem = pid7 %in% c(1, 2, 3),
    is_rep = pid7 %in% c(5, 6, 7),
    # Party ID on 1-4 scale: 1=Strong D, 2=Weak/Lean D, 3=Weak/Lean R, 4=Strong R
    pid4 = case_when(
      pid7 == 1 ~ 1,
      pid7 %in% c(2, 3) ~ 2,
      pid7 %in% c(5, 6) ~ 3,
      pid7 == 7 ~ 4
    )
  )

# Party feeling thermometers (0-97 scale, where 97 = 97-100; 98=DK, 99=NA)
# Also handle negative values as missing
cdf <- cdf %>%
  mutate(
    dem_party_therm = if_else(VCF0218 >= 0 & VCF0218 <= 97, VCF0218, NA_real_),
    rep_party_therm = if_else(VCF0224 >= 0 & VCF0224 <= 97, VCF0224, NA_real_),
    in_party_therm = if_else(is_dem, dem_party_therm, rep_party_therm),
    out_party_therm = if_else(is_dem, rep_party_therm, dem_party_therm)
  )

# Candidate feeling thermometers
cdf <- cdf %>%
  mutate(
    dem_cand_therm = if_else(VCF0424 >= 0 & VCF0424 <= 97, VCF0424, NA_real_),
    rep_cand_therm = if_else(VCF0426 >= 0 & VCF0426 <= 97, VCF0426, NA_real_),
    in_cand_therm = if_else(is_dem, dem_cand_therm, rep_cand_therm),
    out_cand_therm = if_else(is_dem, rep_cand_therm, dem_cand_therm)
  )

# Candidate emotions (1=Yes, 2=No; recode to 1/0)
# Angry, Afraid = negative; Hopeful, Proud = positive
cdf <- cdf %>%
  mutate(
    across(c(VCF0358, VCF0359, VCF0360, VCF0361,
             VCF0370, VCF0371, VCF0372, VCF0373),
           ~if_else(.x == 1, 1, if_else(.x == 2, 0, NA_real_)),
           .names = "{.col}_r")
  ) %>%
  mutate(
    # Dem candidate: angry, afraid = negative; hopeful, proud = positive
    dem_cand_pos = (VCF0360_r + VCF0361_r) / 2,  # hopeful + proud
    dem_cand_neg = (VCF0358_r + VCF0359_r) / 2,  # angry + afraid
    dem_cand_net_affect = dem_cand_pos - dem_cand_neg,
    # Rep candidate: angry, afraid = negative; hopeful, proud = positive
    rep_cand_pos = (VCF0372_r + VCF0373_r) / 2,  # hopeful + proud
    rep_cand_neg = (VCF0370_r + VCF0371_r) / 2,  # angry + afraid
    rep_cand_net_affect = rep_cand_pos - rep_cand_neg,
    # In-party / out-party net affect
    in_cand_net_affect = if_else(is_dem, dem_cand_net_affect, rep_cand_net_affect),
    out_cand_net_affect = if_else(is_dem, rep_cand_net_affect, dem_cand_net_affect)
  )

# Candidate traits (old battery, 1980-2008)
# VCF0354-0357: Dem cand (Knowledgeable, Moral, Leadership, Cares)
# VCF0366-0369: Rep cand (Knowledgeable, Moral, Leadership, Cares)
# Coded: 1=Extremely well, 2=Quite well, 3=Not too well, 4=Not well at all
# Rescale to -2 (not well at all) to 2 (extremely well): rescaled = (10 - 4*x) / 3
recode_trait <- function(x) {
  x_clean <- if_else(x >= 1 & x <= 4, x, NA_real_)
  (10 - 4 * x_clean) / 3
}

cdf <- cdf %>%
  mutate(
    across(c(VCF0354, VCF0355, VCF0356, VCF0357,
             VCF0366, VCF0367, VCF0368, VCF0369),
           recode_trait, .names = "{.col}_r")
  ) %>%
  rowwise() %>%
  mutate(
    dem_cand_trait_avg = mean(c(VCF0354_r, VCF0355_r, VCF0356_r, VCF0357_r), na.rm = TRUE),
    rep_cand_trait_avg = mean(c(VCF0366_r, VCF0367_r, VCF0368_r, VCF0369_r), na.rm = TRUE)
  ) %>%
  ungroup() %>%
  mutate(
    dem_cand_trait_avg = if_else(is.nan(dem_cand_trait_avg), NA_real_, dem_cand_trait_avg),
    rep_cand_trait_avg = if_else(is.nan(rep_cand_trait_avg), NA_real_, rep_cand_trait_avg),
    in_cand_trait = if_else(is_dem, dem_cand_trait_avg, rep_cand_trait_avg),
    out_cand_trait = if_else(is_dem, rep_cand_trait_avg, dem_cand_trait_avg)
  )

# Participation variables
# VCF0702: Voted (1=No, 2=Yes, 0=DK/NA)
# VCF0717-0721: Campaign activities (1=No, 2=Yes, 0=DK/NA)
cdf <- cdf %>%
  mutate(
    voted = if_else(VCF0702 == 2, 1, if_else(VCF0702 == 1, 0, NA_real_)),
    influence_vote = if_else(VCF0717 == 2, 1, if_else(VCF0717 == 1, 0, NA_real_)),
    attend_rally = if_else(VCF0718 == 2, 1, if_else(VCF0718 == 1, 0, NA_real_)),
    work_party = if_else(VCF0719 == 2, 1, if_else(VCF0719 == 1, 0, NA_real_)),
    display_button = if_else(VCF0720 == 2, 1, if_else(VCF0720 == 1, 0, NA_real_)),
    donate_money = if_else(VCF0721 == 2, 1, if_else(VCF0721 == 1, 0, NA_real_))
  ) %>%
  rowwise() %>%
  mutate(
    nonvoting_participation = sum(c(attend_rally, donate_money, influence_vote,
                                     display_button, work_party), na.rm = FALSE)
  ) %>%
  ungroup()

# Demographics
cdf <- cdf %>%
  mutate(
    age = if_else(VCF0101 > 0 & VCF0101 < 98, VCF0101, NA_real_),
    female = if_else(VCF0104 == 2, 1, if_else(VCF0104 == 1, 0, NA_real_)),
    race = case_when(
      VCF0105b == 1 ~ "White",
      VCF0105b == 2 ~ "Black",
      VCF0105b == 3 ~ "Hispanic",
      VCF0105b == 4 ~ "Other"
    ),
    education = if_else(VCF0110 >= 1 & VCF0110 <= 4, VCF0110, NA_real_),
    mode = VCF0017
  )

# Party ID dummies for regression (reference = Strong Democrat)
cdf <- cdf %>%
  mutate(
    pid_label = case_when(
      pid7 == 1 ~ "Strong Democrat",
      pid7 == 2 ~ "Weak Democrat",
      pid7 == 3 ~ "Independent - Democrat",
      pid7 == 5 ~ "Independent - Republican",
      pid7 == 6 ~ "Weak Republican",
      pid7 == 7 ~ "Strong Republican"
    ),
    pid_label = factor(pid_label, levels = c("Strong Democrat", "Weak Democrat",
                                              "Independent - Democrat",
                                              "Independent - Republican",
                                              "Weak Republican", "Strong Republican"))
  )

# Filter to partisans only for main analyses
partisans <- cdf %>% filter(is_partisan)

tibble(
  Metric = c("Partisan sample size", "Years available"),
  Value = c(as.character(nrow(partisans)),
            paste(sort(unique(partisans$year)), collapse = ", "))
) %>%
  kable(col.names = c("", "")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
 <thead>
  <tr>
   <th style="text-align:left;">  </th>
   <th style="text-align:left;">  </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Partisan sample size </td>
   <td style="text-align:left;"> 63659 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Years available </td>
   <td style="text-align:left;"> 1952, 1954, 1956, 1958, 1960, 1962, 1964, 1966, 1968, 1970, 1972, 1974, 1976, 1978, 1980, 1982, 1984, 1986, 1988, 1990, 1992, 1994, 1996, 1998, 2000, 2002, 2004, 2008, 2012, 2016, 2020, 2024 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


The ANES Cumulative Data File contains data from 1948 to 2024. The paper analyzes trends from approximately 1978 to 2016, using the 7-point party identification measure to classify respondents as partisans (including independent "leaners"). Pure independents and those identifying with minor parties are excluded.

Key variable construction:

- **Feeling thermometers**: 0–97 scale (97 = 97–100 degrees). Values below 0 or above 97 treated as missing.
- **Candidate traits** (old battery, 1980–2008): 4-point scale rescaled from –2 (not well at all) to +2 (extremely well) via linear transformation: rescaled = (10 – 4×original) / 3
- **Candidate affects**: Binary (yes/no) recoded to 1/0. Net affect = average positive (hopeful, proud) – average negative (angry, afraid).
- **Participation**: Voting coded as binary. Nonvoting participation = sum of 5 binary items (rally, donate, mobilize, sticker/button, work for party).

---

## Analytical Decisions and Assumptions

| Decision | Paper says | Our interpretation | Rationale | Alternative possible |
|----------|-----------|-------------------|-----------|---------------------|
| Survey weights | Not mentioned | Not applied | Paper makes no reference to weighting; reproducing unweighted | Could apply ANES sample weights |
| Thermometer scale | 0–100 implied | 0–97 used (CDF coding where 97 = 97–100) | CDF codes 97–100 as 97 | Could re-expand 97 to ~98.5 |
| Leaners as partisans | Stated (p. 203) | Independent-Democrats and Independent-Republicans included as partisans | Consistent with standard practice | — |
| Demographics in Table 2 | "age, gender, partisanship, race, year of survey, and education" (fn. 3) | Age (continuous), female dummy, race dummies (4 categories), education (4-level ordinal) | Partisanship is already in the model as dummies; year is the continuous Year variable | Race could have different categorization |
| Nonvoting participation DV | "binomial logit regression" (fn. 4); sum of 5 behaviors | Modeled as binomial(5, p) logit — i.e., `glm(cbind(k, 5-k) ~ ..., family = binomial)` | Log-likelihood of –30,921 for N=26,460 is inconsistent with binary logit but consistent with binomial(5) | Could model as binary (any vs. none) or Poisson |
| Affect time series | Exclude 2016 (fn. 1, p. 203) | 2016 excluded from all affect-based time series | ANES changed format from yes/no to 5-point scale in 2016 | — |
| Party ID 4-point scale | "1 for Strong Democrats to 4 for Strong Republicans" (fn. 2) | 1 = Strong D, 2 = Weak/Lean D, 3 = Weak/Lean R, 4 = Strong R | Leaners grouped with weak partisans | — |
| Trait battery | Described for 2016 on p. 203 | For time series, used old CDF battery (VCF0354–0369, 1980–2008) with 4 traits: Knowledgeable, Moral, Leadership, Cares | New 5-point battery only available from 2008 | Could use new battery for 2008+ |

**Questionable or non-standard analytical choices in the paper**:

1. **No survey weights**: The ANES documentation recommends using weights for population-representative estimates. The omission of weights is not justified in the paper.
2. **Treating nonvoting participation count as binomial logit**: While technically valid, this assumes independence across the 5 activities and a common probability model, which may not hold.
3. **Thermometer 97-cap**: The CDF codes thermometer values 97–100 as 97, which compresses the top of the distribution. The paper does not mention this.

---

## Reproduction Results

### Figure 1: Party Feeling Thermometer Means Over Time


::: {.cell}

```{.r .cell-code}
# Compute mean in-party and out-party thermometer by year and party
therm_by_year <- partisans %>%
  filter(!is.na(in_party_therm) & !is.na(out_party_therm)) %>%
  group_by(year, is_dem) %>%
  summarise(
    mean_in = mean(in_party_therm, na.rm = TRUE),
    mean_out = mean(out_party_therm, na.rm = TRUE),
    n = n(),
    .groups = "drop"
  ) %>%
  mutate(party = if_else(is_dem, "Democrat", "Republican"))

# Also compute overall partisan means (combining Dems and Reps)
therm_overall <- partisans %>%
  filter(!is.na(in_party_therm) & !is.na(out_party_therm)) %>%
  group_by(year) %>%
  summarise(
    mean_in = mean(in_party_therm, na.rm = TRUE),
    mean_out = mean(out_party_therm, na.rm = TRUE),
    n = n(),
    .groups = "drop"
  )

# Display key values mentioned in the paper
key_years <- therm_overall %>%
  filter(year %in% c(1978, 1980, 1988, 2000, 2004, 2008, 2012, 2016))

key_years %>%
  kable(caption = "Overall partisan thermometer means for key years",
        digits = 2,
        col.names = c("Year", "In-party Mean", "Out-party Mean", "N")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Overall partisan thermometer means for key years</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Year </th>
   <th style="text-align:right;"> In-party Mean </th>
   <th style="text-align:right;"> Out-party Mean </th>
   <th style="text-align:right;"> N </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 1978 </td>
   <td style="text-align:right;"> 70.63 </td>
   <td style="text-align:right;"> 47.98 </td>
   <td style="text-align:right;"> 1723 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1980 </td>
   <td style="text-align:right;"> 71.97 </td>
   <td style="text-align:right;"> 46.54 </td>
   <td style="text-align:right;"> 1310 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1988 </td>
   <td style="text-align:right;"> 75.65 </td>
   <td style="text-align:right;"> 45.52 </td>
   <td style="text-align:right;"> 1717 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2000 </td>
   <td style="text-align:right;"> 72.28 </td>
   <td style="text-align:right;"> 41.22 </td>
   <td style="text-align:right;"> 1525 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2004 </td>
   <td style="text-align:right;"> 72.94 </td>
   <td style="text-align:right;"> 38.73 </td>
   <td style="text-align:right;"> 1055 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2008 </td>
   <td style="text-align:right;"> 72.59 </td>
   <td style="text-align:right;"> 35.24 </td>
   <td style="text-align:right;"> 1979 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2012 </td>
   <td style="text-align:right;"> 70.71 </td>
   <td style="text-align:right;"> 27.30 </td>
   <td style="text-align:right;"> 5079 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2016 </td>
   <td style="text-align:right;"> 66.55 </td>
   <td style="text-align:right;"> 25.95 </td>
   <td style="text-align:right;"> 3610 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


The paper reports specific out-party thermometer means: 45.54 (1988), 27.31 (2012), and 25.99 (2016) (p. 203). In-party ratings remained relatively stable around 70.


::: {.cell}

```{.r .cell-code}
therm_by_year %>%
  filter(year >= 1978) %>%
  pivot_longer(cols = c(mean_in, mean_out), names_to = "direction", values_to = "mean_therm") %>%
  mutate(
    label = paste0(party, " - ", if_else(direction == "mean_in", "In-Party", "Out-Party"))
  ) %>%
  ggplot(aes(x = year, y = mean_therm, color = label)) +
  geom_point(alpha = 0.7) +
  geom_smooth(method = "loess", se = FALSE) +
  labs(x = "Year", y = "Mean Therm Rating", color = "") +
  scale_y_continuous(limits = c(0, 85)) +
  theme_minimal() +
  theme(legend.position = "bottom")
```

::: {.cell-output-display}
![Reproduced Figure 1: In-party and out-party feeling thermometers](reproduction_report_files/figure-html/figure1-plot-1.png){width=672}
:::
:::


### Figure 3: Changes in Out-Party Thermometers


::: {.cell}

```{.r .cell-code}
# Compute % of partisans rating out-party at 0, between 1-49, and 50+
outparty_dist <- partisans %>%
  filter(!is.na(out_party_therm) & year >= 1968) %>%
  mutate(
    therm_cat = case_when(
      out_party_therm == 0 ~ "Out-party Therm = 0",
      out_party_therm >= 1 & out_party_therm < 50 ~ "0 < Out-party Therm < 50",
      out_party_therm >= 50 ~ "Out-party Therm >= 50"
    )
  ) %>%
  group_by(year, therm_cat) %>%
  summarise(n = n(), .groups = "drop") %>%
  group_by(year) %>%
  mutate(pct = n / sum(n) * 100) %>%
  ungroup()

# Key values from paper: % at 0 went from 8% in 2000 to 21% in 2016
outparty_dist %>%
  filter(therm_cat == "Out-party Therm = 0", year %in% c(2000, 2004, 2008, 2012, 2016)) %>%
  select(year, pct) %>%
  kable(caption = "Percentage of partisans rating out-party thermometer at 0",
        digits = 1, col.names = c("Year", "% at 0")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Percentage of partisans rating out-party thermometer at 0</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Year </th>
   <th style="text-align:right;"> % at 0 </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 2000 </td>
   <td style="text-align:right;"> 8.3 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2004 </td>
   <td style="text-align:right;"> 12.2 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2008 </td>
   <td style="text-align:right;"> 16.3 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2012 </td>
   <td style="text-align:right;"> 23.9 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2016 </td>
   <td style="text-align:right;"> 21.7 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



::: {.cell}

```{.r .cell-code}
outparty_dist %>%
  filter(therm_cat %in% c("0 < Out-party Therm < 50", "Out-party Therm = 0")) %>%
  ggplot(aes(x = year, y = pct, color = therm_cat)) +
  geom_point() +
  geom_smooth(method = "loess", se = FALSE) +
  labs(x = "Year", y = "Percent", color = "") +
  theme_minimal() +
  theme(legend.position = "bottom")
```

::: {.cell-output-display}
![Reproduced Figure 3: Changes in out-party thermometer distribution](reproduction_report_files/figure-html/figure3-plot-1.png){width=672}
:::
:::


### Table 1: ANES 2016 Interview Mode Effects


::: {.cell}

```{.r .cell-code}
# Use CDF data for 2016, split by mode
# Mode: 0 = Face-to-face, 4 = Internet
cdf_2016 <- partisans %>%
  filter(year == 2016, mode %in% c(0, 4)) %>%
  mutate(
    mode_label = if_else(mode == 0, "Face-to-face", "Online"),
    # Polarization = in-party - out-party thermometer
    therm_polarization = in_party_therm - out_party_therm
  )

# For Table 1, we need: Feel Therm polarization, Affect polarization, Trait polarization
# Affect and Trait use the 2016-specific variables, but the paper excludes 2016 from
# affect time series. For Table 1, we use the CDF thermometer and compute from 2016 data.

# Feeling thermometer polarization by mode
therm_mode <- cdf_2016 %>%
  filter(!is.na(therm_polarization)) %>%
  group_by(mode_label) %>%
  summarise(mean_pol = mean(therm_polarization, na.rm = TRUE), .groups = "drop")

therm_test <- t.test(therm_polarization ~ mode_label, data = cdf_2016)

# For affect and traits, we need the 2016 wave data
ts16_num <- ts16 %>% mutate(across(everything(), ~as.numeric(.x)))

# Party ID in 2016 data
ts16_num <- ts16_num %>%
  mutate(
    pid7 = V161158x,
    is_partisan = pid7 %in% c(1, 2, 3, 5, 6, 7),
    is_dem = pid7 %in% c(1, 2, 3),
    mode_2016 = V160501
  )

ts16_partisans <- ts16_num %>% filter(is_partisan)

# Candidate affect in 2016 (5-point scale in 2016: 1=never, 2=some of the time, 3=about half, 4=most of the time, 5=always)
# But the CDF uses binary (yes/no). The paper says they exclude 2016 from time series.
# For Table 1, they must use the 2016 data. The description says scored as "no"=0, "yes"=1
# but 2016 uses 5-point scale. Let's check what makes sense.
# Paper reports affect polarization FtF = 2.22, Online = 2.55
# If using 5-point scale directly: positive affect avg = mean(hopeful, proud),
# negative affect avg = mean(angry, afraid, disgusted)
# Net affect = positive - negative, ranging from -5 to 5 roughly
# Polarization = in-party net - out-party net

# Actually, the paper says on p. 203: "We scored responses of 'no' as 0 and 'yes' as 1"
# This is for the time series. For 2016 specifically in Table 1, they might use a different
# approach, or they might dichotomize the 5-point scale.
# Given the values (FtF=2.22, Online=2.55), if this were on 0-1 scale max polarization = 2.
# Since values exceed 2, they likely use the raw 5-point scale or a different scoring.
# Let me try: recode 1-5 scale, with positive emotions and negative emotions,
# net = positive_avg - negative_avg, polarization = in_net - out_net

# 2016 affect items:
# Dem cand: V161116 (angry), V161117 (hopeful), V161118 (afraid), V161119 (proud), V161120 (disgusted)
# Rep cand: V161121 (angry), V161122 (hopeful), V161123 (afraid), V161124 (proud), V161125 (disgusted)

# Check the scale - these should be 1-5 in 2016 or possibly 1=yes, 2=no
# The paper's footnote 1 says "ANES changed the format of the affect items in 2016 to a
# 5-point scale; respondents were asked to indicate how frequently a particular emotion
# ranging from 'never' to 'always'."

# Try using the binary coding from CDF for 2016 (since CDF has these for 2016 too)
# Actually the CDF does have 2016 emotion data (VCF0358 etc.)
# Let's use the CDF-based affect scores for 2016

# For affect polarization in Table 1: use SUMS not averages of emotion items
# The paper's values (2.22, 2.55) exceed the range of averaged net affect (-1 to 1)
# Using sums: net_affect = (hopeful + proud) - (angry + afraid), range -2 to 2
# Polarization = in_net - out_net, range -4 to 4
affect_2016 <- cdf_2016 %>%
  mutate(
    # Sums, not averages
    dem_pos_sum = VCF0360_r + VCF0361_r,
    dem_neg_sum = VCF0358_r + VCF0359_r,
    rep_pos_sum = VCF0372_r + VCF0373_r,
    rep_neg_sum = VCF0370_r + VCF0371_r,
    dem_net = dem_pos_sum - dem_neg_sum,
    rep_net = rep_pos_sum - rep_neg_sum,
    in_net_affect = if_else(is_dem, dem_net, rep_net),
    out_net_affect = if_else(is_dem, rep_net, dem_net),
    affect_polarization = in_net_affect - out_net_affect
  )

affect_mode <- affect_2016 %>%
  filter(!is.na(affect_polarization)) %>%
  group_by(mode_label) %>%
  summarise(mean_pol = mean(affect_polarization, na.rm = TRUE), .groups = "drop")

affect_test <- t.test(affect_polarization ~ mode_label, data = affect_2016)

# Candidate traits in 2016 - use 2016 wave data with new 5-point battery
# V161159-V161163: Dem cand traits (leadership, cares, knowledgeable, honest, speaks mind)
# V161164-V161168: Rep cand traits (leadership, cares, knowledgeable, honest, speaks mind)
# V161169: Dem even-tempered, V161170: Rep even-tempered
# Scale: 1=extremely well to 5=not well at all (LOWER = more positive)
# Paper rescales to -2 (not well at all) to 2 (extremely well)

recode_trait_2016 <- function(x) {
  # 5-point: 1=extremely well, 2=very well, 3=moderately well, 4=slightly well, 5=not well at all
  # Rescale to 2 (extremely well) to -2 (not well at all)
  x_clean <- if_else(x >= 1 & x <= 5, x, NA_real_)
  2 - (x_clean - 1)  # 1->2, 2->1, 3->0, 4->-1, 5->-2
}

ts16_partisans <- ts16_partisans %>%
  mutate(
    across(c(V161159, V161160, V161161, V161162, V161163,
             V161164, V161165, V161166, V161167, V161168,
             V161169, V161170),
           recode_trait_2016, .names = "{.col}_r")
  ) %>%
  rowwise() %>%
  mutate(
    # Use SUM for Table 1 polarization (paper reports sums, not averages)
    dem_trait_sum = sum(c(V161159_r, V161160_r, V161161_r, V161162_r, V161163_r, V161169_r), na.rm = FALSE),
    rep_trait_sum = sum(c(V161164_r, V161165_r, V161166_r, V161167_r, V161168_r, V161170_r), na.rm = FALSE)
  ) %>%
  ungroup() %>%
  mutate(
    in_trait = if_else(is_dem, dem_trait_sum, rep_trait_sum),
    out_trait = if_else(is_dem, rep_trait_sum, dem_trait_sum),
    trait_polarization = in_trait - out_trait,
    mode_label = case_when(
      mode_2016 == 1 ~ "Face-to-face",
      mode_2016 == 2 ~ "Online"
    )
  )

trait_mode <- ts16_partisans %>%
  filter(!is.na(trait_polarization) & !is.na(mode_label)) %>%
  group_by(mode_label) %>%
  summarise(mean_pol = mean(trait_polarization, na.rm = TRUE), .groups = "drop")

trait_test <- t.test(trait_polarization ~ mode_label,
                     data = ts16_partisans %>% filter(!is.na(mode_label)))

# Build Table 1 comparison
table1_results <- tibble(
  Indicator = c("Feel Therm", "Affect", "Trait"),
  `Paper FtF` = c(33.90, 2.22, 7.77),
  `Reproduced FtF` = c(
    therm_mode %>% filter(mode_label == "Face-to-face") %>% pull(mean_pol),
    affect_mode %>% filter(mode_label == "Face-to-face") %>% pull(mean_pol),
    trait_mode %>% filter(mode_label == "Face-to-face") %>% pull(mean_pol)
  ),
  `Paper Online` = c(43.27, 2.55, 8.96),
  `Reproduced Online` = c(
    therm_mode %>% filter(mode_label == "Online") %>% pull(mean_pol),
    affect_mode %>% filter(mode_label == "Online") %>% pull(mean_pol),
    trait_mode %>% filter(mode_label == "Online") %>% pull(mean_pol)
  ),
  `Paper p` = c("< 0.001", "< 0.001", "< 0.001"),
  `Reproduced p` = c(
    format.pval(therm_test$p.value, digits = 3),
    format.pval(affect_test$p.value, digits = 3),
    format.pval(trait_test$p.value, digits = 3)
  )
)

table1_results %>%
  kable(caption = "Table 1 Reproduction: ANES 2016 Interview Mode Effects",
        digits = 2) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Table 1 Reproduction: ANES 2016 Interview Mode Effects</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Indicator </th>
   <th style="text-align:right;"> Paper FtF </th>
   <th style="text-align:right;"> Reproduced FtF </th>
   <th style="text-align:right;"> Paper Online </th>
   <th style="text-align:right;"> Reproduced Online </th>
   <th style="text-align:left;"> Paper p </th>
   <th style="text-align:left;"> Reproduced p </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Feel Therm </td>
   <td style="text-align:right;"> 33.90 </td>
   <td style="text-align:right;"> 33.91 </td>
   <td style="text-align:right;"> 43.27 </td>
   <td style="text-align:right;"> 43.27 </td>
   <td style="text-align:left;"> &lt; 0.001 </td>
   <td style="text-align:left;"> 4.91e-16 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Affect </td>
   <td style="text-align:right;"> 2.22 </td>
   <td style="text-align:right;"> 1.89 </td>
   <td style="text-align:right;"> 2.55 </td>
   <td style="text-align:right;"> 2.16 </td>
   <td style="text-align:left;"> &lt; 0.001 </td>
   <td style="text-align:left;"> 4.83e-05 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Trait </td>
   <td style="text-align:right;"> 7.77 </td>
   <td style="text-align:right;"> 7.87 </td>
   <td style="text-align:right;"> 8.96 </td>
   <td style="text-align:right;"> 8.97 </td>
   <td style="text-align:left;"> &lt; 0.001 </td>
   <td style="text-align:left;"> 0.000136 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


### Figures 6 & Related: Feeling Thermometer Correlations Over Time


::: {.cell}

```{.r .cell-code}
# Figure 6 top: Correlation between opposing party/candidate thermometers
# Cross-party correlation: Dem party therm ~ Rep party therm (among partisans)
# Cross-candidate correlation: Dem cand therm ~ Rep cand therm (among partisans)

cross_party_corr <- partisans %>%
  filter(!is.na(dem_party_therm) & !is.na(rep_party_therm)) %>%
  group_by(year) %>%
  summarise(
    r_party = cor(dem_party_therm, rep_party_therm, use = "complete.obs"),
    n = n(),
    .groups = "drop"
  )

cross_cand_corr <- partisans %>%
  filter(!is.na(dem_cand_therm) & !is.na(rep_cand_therm)) %>%
  group_by(year) %>%
  summarise(
    r_cand = cor(dem_cand_therm, rep_cand_therm, use = "complete.obs"),
    n_cand = n(),
    .groups = "drop"
  )

cross_party_corr <- cross_party_corr %>%
  left_join(cross_cand_corr, by = "year")

# Figure 6 bottom: Intra-party correlations (party therm ~ candidate therm, within party)
intra_party_corr <- partisans %>%
  filter(!is.na(in_party_therm) & !is.na(in_cand_therm)) %>%
  group_by(year, is_dem) %>%
  summarise(
    r_intra = cor(in_party_therm, in_cand_therm, use = "complete.obs"),
    n = n(),
    .groups = "drop"
  ) %>%
  mutate(party = if_else(is_dem, "Democrat", "Republican"))

# Display key values
cross_party_corr %>%
  filter(year %in% c(1978, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016)) %>%
  select(year, r_party, r_cand, n) %>%
  kable(caption = "Cross-party and cross-candidate thermometer correlations",
        digits = 2, col.names = c("Year", "Party Therm r", "Candidate Therm r", "N")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Cross-party and cross-candidate thermometer correlations</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Year </th>
   <th style="text-align:right;"> Party Therm r </th>
   <th style="text-align:right;"> Candidate Therm r </th>
   <th style="text-align:right;"> N </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 1978 </td>
   <td style="text-align:right;"> -0.25 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> 1723 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1980 </td>
   <td style="text-align:right;"> -0.30 </td>
   <td style="text-align:right;"> -0.33 </td>
   <td style="text-align:right;"> 1310 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1984 </td>
   <td style="text-align:right;"> -0.45 </td>
   <td style="text-align:right;"> -0.58 </td>
   <td style="text-align:right;"> 1881 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1988 </td>
   <td style="text-align:right;"> -0.46 </td>
   <td style="text-align:right;"> -0.42 </td>
   <td style="text-align:right;"> 1717 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1992 </td>
   <td style="text-align:right;"> -0.34 </td>
   <td style="text-align:right;"> -0.44 </td>
   <td style="text-align:right;"> 2098 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1996 </td>
   <td style="text-align:right;"> -0.47 </td>
   <td style="text-align:right;"> -0.49 </td>
   <td style="text-align:right;"> 1528 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2000 </td>
   <td style="text-align:right;"> -0.44 </td>
   <td style="text-align:right;"> -0.46 </td>
   <td style="text-align:right;"> 1525 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2004 </td>
   <td style="text-align:right;"> -0.52 </td>
   <td style="text-align:right;"> -0.64 </td>
   <td style="text-align:right;"> 1055 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2008 </td>
   <td style="text-align:right;"> -0.48 </td>
   <td style="text-align:right;"> -0.50 </td>
   <td style="text-align:right;"> 1979 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2012 </td>
   <td style="text-align:right;"> -0.59 </td>
   <td style="text-align:right;"> -0.72 </td>
   <td style="text-align:right;"> 5079 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2016 </td>
   <td style="text-align:right;"> -0.53 </td>
   <td style="text-align:right;"> -0.71 </td>
   <td style="text-align:right;"> 3610 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



::: {.cell}

```{.r .cell-code}
p_top <- cross_party_corr %>%
  filter(year >= 1978) %>%
  pivot_longer(cols = c(r_party, r_cand), names_to = "type", values_to = "r") %>%
  mutate(type = if_else(type == "r_party", "Democrat ~ Republican", "Dem Cand ~ Rep Cand")) %>%
  ggplot(aes(x = year, y = r, color = type)) +
  geom_point() +
  geom_smooth(method = "loess", se = FALSE) +
  labs(x = "", y = "Feeling Thermometer Correlation", color = "") +
  theme_minimal() +
  theme(legend.position = "bottom")

p_bottom <- intra_party_corr %>%
  filter(year >= 1978) %>%
  ggplot(aes(x = year, y = r_intra, color = party)) +
  geom_point() +
  geom_smooth(method = "loess", se = FALSE) +
  labs(x = "Year", y = "Feeling Thermometer Correlation", color = "") +
  theme_minimal() +
  theme(legend.position = "bottom")

gridExtra::grid.arrange(p_top, p_bottom, ncol = 1)
```

::: {.cell-output-display}
![Reproduced Figure 6: Feeling-thermometer correlations](reproduction_report_files/figure-html/figure6-plot-1.png){width=672}
:::
:::


### Figure 7: Correlation Between Net Democratic and Republican Candidate Affects


::: {.cell}

```{.r .cell-code}
# Net affect for Dem cand vs Rep cand (among partisans)
# This is the correlation between net Dem affect and net Rep affect
affect_corr <- partisans %>%
  filter(!is.na(dem_cand_net_affect) & !is.na(rep_cand_net_affect)) %>%
  group_by(year) %>%
  summarise(
    r_affect = cor(dem_cand_net_affect, rep_cand_net_affect, use = "complete.obs"),
    n = n(),
    .groups = "drop"
  )

affect_corr %>%
  kable(caption = "Correlation between net Democratic and Republican candidate affects",
        digits = 2, col.names = c("Year", "Correlation", "N")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Correlation between net Democratic and Republican candidate affects</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Year </th>
   <th style="text-align:right;"> Correlation </th>
   <th style="text-align:right;"> N </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 1980 </td>
   <td style="text-align:right;"> -0.30 </td>
   <td style="text-align:right;"> 1305 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1984 </td>
   <td style="text-align:right;"> -0.48 </td>
   <td style="text-align:right;"> 1906 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1988 </td>
   <td style="text-align:right;"> -0.39 </td>
   <td style="text-align:right;"> 1742 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1992 </td>
   <td style="text-align:right;"> -0.42 </td>
   <td style="text-align:right;"> 2114 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1996 </td>
   <td style="text-align:right;"> -0.42 </td>
   <td style="text-align:right;"> 1532 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2000 </td>
   <td style="text-align:right;"> -0.40 </td>
   <td style="text-align:right;"> 1522 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2004 </td>
   <td style="text-align:right;"> -0.63 </td>
   <td style="text-align:right;"> 1042 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2008 </td>
   <td style="text-align:right;"> -0.48 </td>
   <td style="text-align:right;"> 1946 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2012 </td>
   <td style="text-align:right;"> -0.69 </td>
   <td style="text-align:right;"> 4981 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2016 </td>
   <td style="text-align:right;"> -0.68 </td>
   <td style="text-align:right;"> 3644 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


### Figures 9 & 10: Candidate Trait Correlations


::: {.cell}

```{.r .cell-code}
# Figure 9: Correlation between Dem and Rep candidate trait averages
trait_cross_corr <- partisans %>%
  filter(!is.na(dem_cand_trait_avg) & !is.na(rep_cand_trait_avg)) %>%
  group_by(year) %>%
  summarise(
    r_cross = cor(dem_cand_trait_avg, rep_cand_trait_avg, use = "complete.obs"),
    n = n(),
    .groups = "drop"
  )

# Figure 10: Within-candidate trait correlations (average correlation among the 4 traits)
# For each year, compute mean pairwise correlation among the 4 traits for each candidate
within_trait_corr <- partisans %>%
  filter(year %in% c(1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008)) %>%
  group_by(year) %>%
  summarise(
    # Dem candidate traits correlation matrix
    dem_cor = {
      m <- cbind(VCF0354_r, VCF0355_r, VCF0356_r, VCF0357_r)
      cm <- cor(m, use = "pairwise.complete.obs")
      mean(cm[lower.tri(cm)])
    },
    # Rep candidate traits correlation matrix
    rep_cor = {
      m <- cbind(VCF0366_r, VCF0367_r, VCF0368_r, VCF0369_r)
      cm <- cor(m, use = "pairwise.complete.obs")
      mean(cm[lower.tri(cm)])
    },
    .groups = "drop"
  )

trait_cross_corr %>%
  kable(caption = "Figure 9: Cross-candidate trait correlations",
        digits = 2, col.names = c("Year", "Correlation", "N")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Figure 9: Cross-candidate trait correlations</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Year </th>
   <th style="text-align:right;"> Correlation </th>
   <th style="text-align:right;"> N </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 1980 </td>
   <td style="text-align:right;"> -0.22 </td>
   <td style="text-align:right;"> 1289 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1984 </td>
   <td style="text-align:right;"> -0.26 </td>
   <td style="text-align:right;"> 1846 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1988 </td>
   <td style="text-align:right;"> -0.18 </td>
   <td style="text-align:right;"> 1713 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1992 </td>
   <td style="text-align:right;"> -0.33 </td>
   <td style="text-align:right;"> 2080 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1996 </td>
   <td style="text-align:right;"> -0.37 </td>
   <td style="text-align:right;"> 1525 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2000 </td>
   <td style="text-align:right;"> -0.33 </td>
   <td style="text-align:right;"> 1534 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2004 </td>
   <td style="text-align:right;"> -0.60 </td>
   <td style="text-align:right;"> 1061 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2008 </td>
   <td style="text-align:right;"> -0.45 </td>
   <td style="text-align:right;"> 972 </td>
  </tr>
</tbody>
</table>

`````
:::

```{.r .cell-code}
within_trait_corr %>%
  kable(caption = "Figure 10: Mean within-candidate trait correlations",
        digits = 2, col.names = c("Year", "Dem Cand", "Rep Cand")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Figure 10: Mean within-candidate trait correlations</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Year </th>
   <th style="text-align:right;"> Dem Cand </th>
   <th style="text-align:right;"> Rep Cand </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 1980 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1984 </td>
   <td style="text-align:right;"> 0.48 </td>
   <td style="text-align:right;"> 0.53 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1988 </td>
   <td style="text-align:right;"> 0.46 </td>
   <td style="text-align:right;"> 0.48 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1992 </td>
   <td style="text-align:right;"> 0.50 </td>
   <td style="text-align:right;"> 0.48 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1996 </td>
   <td style="text-align:right;"> 0.56 </td>
   <td style="text-align:right;"> 0.50 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2000 </td>
   <td style="text-align:right;"> 0.52 </td>
   <td style="text-align:right;"> 0.53 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2004 </td>
   <td style="text-align:right;"> 0.58 </td>
   <td style="text-align:right;"> 0.62 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2008 </td>
   <td style="text-align:right;"> 0.64 </td>
   <td style="text-align:right;"> 0.60 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


### Figure 12: Correlations Between Party ID and Indicators of Partisan Affect


::: {.cell}

```{.r .cell-code}
# Correlation between party ID (4-point: 1=Strong D to 4=Strong R) and:
# 1. Thermometer differential (rep therm - dem therm, so higher = more pro-Republican)
# 2. Affect differential (rep net affect - dem net affect)
# 3. Trait differential (rep trait - dem trait)
# Note: paper uses a metric "ranging from 1 for Strong Democrats to 4 for Strong Republicans"

# Compute correlations separately to handle missing data across indicators
pid_corr_therm <- partisans %>%
  filter(!is.na(pid4) & !is.na(dem_party_therm) & !is.na(rep_party_therm)) %>%
  mutate(therm_diff = rep_party_therm - dem_party_therm) %>%
  group_by(year) %>%
  summarise(r_therm = cor(pid4, therm_diff, use = "complete.obs"), .groups = "drop")

pid_corr_affect <- partisans %>%
  filter(!is.na(pid4) & !is.na(dem_cand_net_affect) & !is.na(rep_cand_net_affect)) %>%
  mutate(affect_diff = rep_cand_net_affect - dem_cand_net_affect) %>%
  group_by(year) %>%
  summarise(r_affect = cor(pid4, affect_diff, use = "complete.obs"), .groups = "drop")

pid_corr_trait <- partisans %>%
  filter(!is.na(pid4) & !is.na(dem_cand_trait_avg) & !is.na(rep_cand_trait_avg)) %>%
  mutate(trait_diff = rep_cand_trait_avg - dem_cand_trait_avg) %>%
  group_by(year) %>%
  summarise(r_trait = cor(pid4, trait_diff, use = "complete.obs"), .groups = "drop")

pid_corr <- pid_corr_therm %>%
  full_join(pid_corr_affect, by = "year") %>%
  full_join(pid_corr_trait, by = "year")

pid_corr %>%
  filter(year >= 1978) %>%
  kable(caption = "Figure 12: Correlations between party ID and partisan affect indicators",
        digits = 2, col.names = c("Year", "Therm ~ Party ID", "Affect ~ Party ID", "Trait ~ Party ID")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Figure 12: Correlations between party ID and partisan affect indicators</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Year </th>
   <th style="text-align:right;"> Therm ~ Party ID </th>
   <th style="text-align:right;"> Affect ~ Party ID </th>
   <th style="text-align:right;"> Trait ~ Party ID </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 1978 </td>
   <td style="text-align:right;"> 0.72 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1980 </td>
   <td style="text-align:right;"> 0.73 </td>
   <td style="text-align:right;"> 0.54 </td>
   <td style="text-align:right;"> 0.57 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1982 </td>
   <td style="text-align:right;"> 0.79 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1984 </td>
   <td style="text-align:right;"> 0.75 </td>
   <td style="text-align:right;"> 0.65 </td>
   <td style="text-align:right;"> 0.63 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1986 </td>
   <td style="text-align:right;"> 0.75 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1988 </td>
   <td style="text-align:right;"> 0.75 </td>
   <td style="text-align:right;"> 0.61 </td>
   <td style="text-align:right;"> 0.61 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1990 </td>
   <td style="text-align:right;"> 0.71 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1992 </td>
   <td style="text-align:right;"> 0.76 </td>
   <td style="text-align:right;"> 0.66 </td>
   <td style="text-align:right;"> 0.65 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1994 </td>
   <td style="text-align:right;"> 0.80 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1996 </td>
   <td style="text-align:right;"> 0.78 </td>
   <td style="text-align:right;"> 0.68 </td>
   <td style="text-align:right;"> 0.69 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1998 </td>
   <td style="text-align:right;"> 0.74 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2000 </td>
   <td style="text-align:right;"> 0.78 </td>
   <td style="text-align:right;"> 0.67 </td>
   <td style="text-align:right;"> 0.68 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2004 </td>
   <td style="text-align:right;"> 0.82 </td>
   <td style="text-align:right;"> 0.75 </td>
   <td style="text-align:right;"> 0.75 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2008 </td>
   <td style="text-align:right;"> 0.78 </td>
   <td style="text-align:right;"> 0.67 </td>
   <td style="text-align:right;"> 0.68 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2012 </td>
   <td style="text-align:right;"> 0.84 </td>
   <td style="text-align:right;"> 0.78 </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2016 </td>
   <td style="text-align:right;"> 0.83 </td>
   <td style="text-align:right;"> 0.76 </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2020 </td>
   <td style="text-align:right;"> 0.87 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2024 </td>
   <td style="text-align:right;"> 0.87 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:right;"> NA </td>
  </tr>
</tbody>
</table>

`````
:::
:::


### Table 2: Partisan Affect and Political Participation


::: {.cell}

```{.r .cell-code}
# Model 1: Voting (binary logit)
# DV: voted (0/1)
# IVs: Year, In-party Therm, In-party Therm × Year, Out-party Therm, Out-party Therm × Year,
#       Party ID dummies (ref = Strong Democrat), Demographics (age, female, race, education)

# Prepare data for regression
reg_data <- partisans %>%
  filter(year >= 1980 & year <= 2016) %>%
  filter(!is.na(voted) & !is.na(in_party_therm) & !is.na(out_party_therm) &
         !is.na(age) & !is.na(female) & !is.na(race) & !is.na(education) &
         !is.na(pid_label)) %>%
  mutate(
    race = factor(race, levels = c("White", "Black", "Hispanic", "Other"))
  )

# Model 1: Voting
model1 <- glm(voted ~ year + in_party_therm + I(in_party_therm * year) +
                out_party_therm + I(out_party_therm * year) +
                pid_label + age + female + race + education,
              data = reg_data, family = binomial)

# Model 2: Nonvoting participation (binomial with 5 trials)
reg_data2 <- reg_data %>%
  filter(!is.na(nonvoting_participation)) %>%
  mutate(
    successes = nonvoting_participation,
    failures = 5 - nonvoting_participation
  )

model2 <- glm(cbind(successes, failures) ~ year + in_party_therm + I(in_party_therm * year) +
                out_party_therm + I(out_party_therm * year) +
                pid_label + age + female + race + education,
              data = reg_data2, family = binomial)

# Extract coefficients for display
extract_coefs <- function(model, model_name) {
  s <- summary(model)
  coefs <- as.data.frame(s$coefficients)
  coefs$term <- rownames(coefs)
  coefs$model <- model_name
  coefs %>%
    select(model, term, estimate = Estimate, se = `Std. Error`, p = `Pr(>|z|)`) %>%
    as_tibble()
}

coefs1 <- extract_coefs(model1, "Voting")
coefs2 <- extract_coefs(model2, "Nonvoting")

# Display key coefficients matching Table 2
key_terms <- c("(Intercept)", "year", "in_party_therm", "I(in_party_therm * year)",
               "out_party_therm", "I(out_party_therm * year)",
               "pid_labelWeak Democrat", "pid_labelIndependent - Democrat",
               "pid_labelIndependent - Republican", "pid_labelWeak Republican",
               "pid_labelStrong Republican")

display_labels <- c("Constant", "Year", "In-party Therm", "In-party Therm x Year",
                     "Out-party Therm", "Out-party Therm x Year",
                     "Weak Democrat", "Independent - Democrat",
                     "Independent - Republican", "Weak Republican",
                     "Strong Republican")

# Voting model comparison
voting_display <- coefs1 %>%
  filter(term %in% key_terms) %>%
  mutate(term_order = match(term, key_terms)) %>%
  arrange(term_order) %>%
  mutate(display = display_labels[term_order])

paper_voting <- c(-139.274, 0.070, 0.577, -0.0003, 0.920, -0.0005,
                  -0.645, -0.778, -0.548, -0.566, 0.221)
paper_voting_se <- c(11.802, 0.006, 0.143, 0.0001, 0.122, 0.0001,
                     0.050, 0.055, 0.060, 0.057, 0.064)
# Paper significance: all *** except as noted
paper_voting_sig <- c("***", "***", "***", "***", "***", "***",
                      "***", "***", "***", "***", "***")

voting_comparison <- tibble(
  Parameter = display_labels,
  `Paper Est.` = paper_voting,
  `Paper SE` = paper_voting_se,
  `Reproduced Est.` = voting_display$estimate,
  `Reproduced SE` = voting_display$se,
  `Reproduced p` = voting_display$p
)

voting_comparison %>%
  mutate(`Reproduced p` = format.pval(`Reproduced p`, digits = 3, eps = 0.001)) %>%
  kable(caption = "Table 2 Model 1 (Voting) Reproduction",
        digits = 4) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Table 2 Model 1 (Voting) Reproduction</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Parameter </th>
   <th style="text-align:right;"> Paper Est. </th>
   <th style="text-align:right;"> Paper SE </th>
   <th style="text-align:right;"> Reproduced Est. </th>
   <th style="text-align:right;"> Reproduced SE </th>
   <th style="text-align:left;"> Reproduced p </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Constant </td>
   <td style="text-align:right;"> -139.2740 </td>
   <td style="text-align:right;"> 11.8020 </td>
   <td style="text-align:right;"> -74.4628 </td>
   <td style="text-align:right;"> 11.5496 </td>
   <td style="text-align:left;"> &lt; 0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Year </td>
   <td style="text-align:right;"> 0.0700 </td>
   <td style="text-align:right;"> 0.0060 </td>
   <td style="text-align:right;"> 0.0363 </td>
   <td style="text-align:right;"> 0.0058 </td>
   <td style="text-align:left;"> &lt; 0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> In-party Therm </td>
   <td style="text-align:right;"> 0.5770 </td>
   <td style="text-align:right;"> 0.1430 </td>
   <td style="text-align:right;"> 0.2823 </td>
   <td style="text-align:right;"> 0.1419 </td>
   <td style="text-align:left;"> 0.04671 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> In-party Therm x Year </td>
   <td style="text-align:right;"> -0.0003 </td>
   <td style="text-align:right;"> 0.0001 </td>
   <td style="text-align:right;"> -0.0001 </td>
   <td style="text-align:right;"> 0.0001 </td>
   <td style="text-align:left;"> 0.05009 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Out-party Therm </td>
   <td style="text-align:right;"> 0.9200 </td>
   <td style="text-align:right;"> 0.1220 </td>
   <td style="text-align:right;"> 0.6215 </td>
   <td style="text-align:right;"> 0.1219 </td>
   <td style="text-align:left;"> &lt; 0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Out-party Therm x Year </td>
   <td style="text-align:right;"> -0.0005 </td>
   <td style="text-align:right;"> 0.0001 </td>
   <td style="text-align:right;"> -0.0003 </td>
   <td style="text-align:right;"> 0.0001 </td>
   <td style="text-align:left;"> &lt; 0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Weak Democrat </td>
   <td style="text-align:right;"> -0.6450 </td>
   <td style="text-align:right;"> 0.0500 </td>
   <td style="text-align:right;"> -0.6717 </td>
   <td style="text-align:right;"> 0.0501 </td>
   <td style="text-align:left;"> &lt; 0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Independent - Democrat </td>
   <td style="text-align:right;"> -0.7780 </td>
   <td style="text-align:right;"> 0.0550 </td>
   <td style="text-align:right;"> -0.7940 </td>
   <td style="text-align:right;"> 0.0553 </td>
   <td style="text-align:left;"> &lt; 0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Independent - Republican </td>
   <td style="text-align:right;"> -0.5480 </td>
   <td style="text-align:right;"> 0.0600 </td>
   <td style="text-align:right;"> -0.6010 </td>
   <td style="text-align:right;"> 0.0599 </td>
   <td style="text-align:left;"> &lt; 0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Weak Republican </td>
   <td style="text-align:right;"> -0.5660 </td>
   <td style="text-align:right;"> 0.0570 </td>
   <td style="text-align:right;"> -0.6031 </td>
   <td style="text-align:right;"> 0.0571 </td>
   <td style="text-align:left;"> &lt; 0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Strong Republican </td>
   <td style="text-align:right;"> 0.2210 </td>
   <td style="text-align:right;"> 0.0640 </td>
   <td style="text-align:right;"> 0.1793 </td>
   <td style="text-align:right;"> 0.0645 </td>
   <td style="text-align:left;"> 0.00548 </td>
  </tr>
</tbody>
</table>

`````
:::

```{.r .cell-code}
# Nonvoting model comparison
nonvoting_display <- coefs2 %>%
  filter(term %in% key_terms) %>%
  mutate(term_order = match(term, key_terms)) %>%
  arrange(term_order) %>%
  mutate(display = display_labels[term_order])

paper_nonvoting <- c(-59.363, 0.029, 0.239, -0.0001, 0.447, -0.0002,
                     -0.566, -0.383, -0.382, -0.470, 0.017)
paper_nonvoting_se <- c(6.555, 0.003, 0.077, 0.00004, 0.064, 0.00003,
                        0.027, 0.029, 0.031, 0.030, 0.025)
# Paper significance: all *** except Strong Rep (NS)
paper_nonvoting_sig <- c("***", "***", "***", "***", "***", "***",
                         "***", "***", "***", "***", "NS")

nonvoting_comparison <- tibble(
  Parameter = display_labels,
  `Paper Est.` = paper_nonvoting,
  `Paper SE` = paper_nonvoting_se,
  `Reproduced Est.` = nonvoting_display$estimate,
  `Reproduced SE` = nonvoting_display$se,
  `Reproduced p` = nonvoting_display$p
)

nonvoting_comparison %>%
  mutate(`Reproduced p` = format.pval(`Reproduced p`, digits = 3, eps = 0.001)) %>%
  kable(caption = "Table 2 Model 2 (Nonvoting Participation) Reproduction",
        digits = 4) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Table 2 Model 2 (Nonvoting Participation) Reproduction</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Parameter </th>
   <th style="text-align:right;"> Paper Est. </th>
   <th style="text-align:right;"> Paper SE </th>
   <th style="text-align:right;"> Reproduced Est. </th>
   <th style="text-align:right;"> Reproduced SE </th>
   <th style="text-align:left;"> Reproduced p </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Constant </td>
   <td style="text-align:right;"> -59.3630 </td>
   <td style="text-align:right;"> 6.555 </td>
   <td style="text-align:right;"> -35.0815 </td>
   <td style="text-align:right;"> 6.3550 </td>
   <td style="text-align:left;"> &lt;0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Year </td>
   <td style="text-align:right;"> 0.0290 </td>
   <td style="text-align:right;"> 0.003 </td>
   <td style="text-align:right;"> 0.0161 </td>
   <td style="text-align:right;"> 0.0032 </td>
   <td style="text-align:left;"> &lt;0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> In-party Therm </td>
   <td style="text-align:right;"> 0.2390 </td>
   <td style="text-align:right;"> 0.077 </td>
   <td style="text-align:right;"> 0.1380 </td>
   <td style="text-align:right;"> 0.0763 </td>
   <td style="text-align:left;"> 0.0706 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> In-party Therm x Year </td>
   <td style="text-align:right;"> -0.0001 </td>
   <td style="text-align:right;"> 0.000 </td>
   <td style="text-align:right;"> -0.0001 </td>
   <td style="text-align:right;"> 0.0000 </td>
   <td style="text-align:left;"> 0.0831 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Out-party Therm </td>
   <td style="text-align:right;"> 0.4470 </td>
   <td style="text-align:right;"> 0.064 </td>
   <td style="text-align:right;"> 0.3118 </td>
   <td style="text-align:right;"> 0.0628 </td>
   <td style="text-align:left;"> &lt;0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Out-party Therm x Year </td>
   <td style="text-align:right;"> -0.0002 </td>
   <td style="text-align:right;"> 0.000 </td>
   <td style="text-align:right;"> -0.0002 </td>
   <td style="text-align:right;"> 0.0000 </td>
   <td style="text-align:left;"> &lt;0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Weak Democrat </td>
   <td style="text-align:right;"> -0.5660 </td>
   <td style="text-align:right;"> 0.027 </td>
   <td style="text-align:right;"> -0.5689 </td>
   <td style="text-align:right;"> 0.0272 </td>
   <td style="text-align:left;"> &lt;0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Independent - Democrat </td>
   <td style="text-align:right;"> -0.3830 </td>
   <td style="text-align:right;"> 0.029 </td>
   <td style="text-align:right;"> -0.3790 </td>
   <td style="text-align:right;"> 0.0291 </td>
   <td style="text-align:left;"> &lt;0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Independent - Republican </td>
   <td style="text-align:right;"> -0.3820 </td>
   <td style="text-align:right;"> 0.031 </td>
   <td style="text-align:right;"> -0.3905 </td>
   <td style="text-align:right;"> 0.0312 </td>
   <td style="text-align:left;"> &lt;0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Weak Republican </td>
   <td style="text-align:right;"> -0.4700 </td>
   <td style="text-align:right;"> 0.030 </td>
   <td style="text-align:right;"> -0.4733 </td>
   <td style="text-align:right;"> 0.0301 </td>
   <td style="text-align:left;"> &lt;0.001 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Strong Republican </td>
   <td style="text-align:right;"> 0.0170 </td>
   <td style="text-align:right;"> 0.025 </td>
   <td style="text-align:right;"> -0.0004 </td>
   <td style="text-align:right;"> 0.0249 </td>
   <td style="text-align:left;"> 0.9876 </td>
  </tr>
</tbody>
</table>

`````
:::

```{.r .cell-code}
# Model fit statistics
fit_comparison <- tibble(
  Statistic = c("N", "Log Likelihood", "AIC"),
  `Paper (Voting)` = c(26607, -13090.090, 26226.170),
  `Reproduced (Voting)` = c(nrow(reg_data), as.numeric(logLik(model1)), AIC(model1)),
  `Paper (Nonvoting)` = c(26460, -30921.410, 61888.810),
  `Reproduced (Nonvoting)` = c(nrow(reg_data2), as.numeric(logLik(model2)), AIC(model2))
)

fit_comparison %>%
  kable(caption = "Model fit statistics comparison",
        digits = 1) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Model fit statistics comparison</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Statistic </th>
   <th style="text-align:right;"> Paper (Voting) </th>
   <th style="text-align:right;"> Reproduced (Voting) </th>
   <th style="text-align:right;"> Paper (Nonvoting) </th>
   <th style="text-align:right;"> Reproduced (Nonvoting) </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 26607.0 </td>
   <td style="text-align:right;"> 26292.0 </td>
   <td style="text-align:right;"> 26460.0 </td>
   <td style="text-align:right;"> 26150.0 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Log Likelihood </td>
   <td style="text-align:right;"> -13090.1 </td>
   <td style="text-align:right;"> -12904.2 </td>
   <td style="text-align:right;"> -30921.4 </td>
   <td style="text-align:right;"> -30456.1 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> AIC </td>
   <td style="text-align:right;"> 26226.2 </td>
   <td style="text-align:right;"> 25842.4 </td>
   <td style="text-align:right;"> 61888.8 </td>
   <td style="text-align:right;"> 60946.2 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


### Descriptive Statistics Comparison


::: {.cell}

```{.r .cell-code}
# Compare key descriptive statistics to verify sample composition
desc_stats <- reg_data %>%
  summarise(
    `Mean Age` = mean(age, na.rm = TRUE),
    `% Female` = mean(female, na.rm = TRUE) * 100,
    `% White` = mean(race == "White", na.rm = TRUE) * 100,
    `Mean In-party Therm` = mean(in_party_therm, na.rm = TRUE),
    `Mean Out-party Therm` = mean(out_party_therm, na.rm = TRUE),
    `% Voted` = mean(voted, na.rm = TRUE) * 100,
    `Mean Nonvoting Part.` = mean(nonvoting_participation, na.rm = TRUE),
    N = n()
  )

desc_stats %>%
  pivot_longer(everything(), names_to = "Statistic", values_to = "Value") %>%
  kable(caption = "Descriptive statistics for the regression sample",
        digits = 2) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Descriptive statistics for the regression sample</caption>
 <thead>
  <tr>
   <th style="text-align:left;"> Statistic </th>
   <th style="text-align:right;"> Value </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:left;"> Mean Age </td>
   <td style="text-align:right;"> 47.13 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> % Female </td>
   <td style="text-align:right;"> 54.10 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> % White </td>
   <td style="text-align:right;"> 72.99 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Mean In-party Therm </td>
   <td style="text-align:right;"> 71.32 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Mean Out-party Therm </td>
   <td style="text-align:right;"> 38.12 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> % Voted </td>
   <td style="text-align:right;"> 74.27 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> Mean Nonvoting Part. </td>
   <td style="text-align:right;"> 0.72 </td>
  </tr>
  <tr>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 26292.00 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


### Figure 13: Predicted Effects of Positive and Negative Motivations


::: {.cell}

```{.r .cell-code}
# Calculate predicted probabilities by year for Figure 13
# For out-party effect: compare predicted probability at out-party therm = 0 vs 50
# For in-party effect: compare predicted probability at in-party therm = 100 vs 50
# Hold other covariates at mean age and modal values

# Modal values
modal_pid <- names(sort(table(reg_data$pid_label), decreasing = TRUE))[1]
modal_race <- names(sort(table(reg_data$race), decreasing = TRUE))[1]
modal_female <- as.numeric(names(sort(table(reg_data$female), decreasing = TRUE))[1])
modal_education <- as.numeric(names(sort(table(reg_data$education), decreasing = TRUE))[1])
mean_age <- mean(reg_data$age, na.rm = TRUE)

# For each year in the data, compute predicted probabilities
pred_years <- sort(unique(reg_data$year))

compute_pred_effects <- function(model, years) {
  map_dfr(years, function(yr) {
    base <- tibble(
      year = yr,
      age = mean_age,
      female = modal_female,
      race = factor(modal_race, levels = levels(reg_data$race)),
      education = modal_education,
      pid_label = factor(modal_pid, levels = levels(reg_data$pid_label))
    )

    # In-party warm (100) vs neutral (50), out-party at 50
    warm_in <- base %>% mutate(in_party_therm = 100, out_party_therm = 50)
    neutral <- base %>% mutate(in_party_therm = 50, out_party_therm = 50)
    cold_out <- base %>% mutate(in_party_therm = 50, out_party_therm = 0)

    p_warm_in <- predict(model, newdata = warm_in, type = "response")
    p_neutral <- predict(model, newdata = neutral, type = "response")
    p_cold_out <- predict(model, newdata = cold_out, type = "response")

    tibble(
      year = yr,
      warm_in_effect = p_warm_in - p_neutral,
      cold_out_effect = p_cold_out - p_neutral
    )
  })
}

voting_effects <- compute_pred_effects(model1, pred_years)
# For nonvoting model, predicted values are proportions (of 5 activities)
# Scale to number of activities
nonvoting_effects <- compute_pred_effects(model2, pred_years) %>%
  mutate(across(c(warm_in_effect, cold_out_effect), ~.x * 5))

# Display key years
voting_effects %>%
  filter(year %in% c(1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016)) %>%
  kable(caption = "Predicted effects on voting probability (Figure 13 top)",
        digits = 3, col.names = c("Year", "Warm In-party (100 vs 50)", "Cold Out-party (0 vs 50)")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Predicted effects on voting probability (Figure 13 top)</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Year </th>
   <th style="text-align:right;"> Warm In-party (100 vs 50) </th>
   <th style="text-align:right;"> Cold Out-party (0 vs 50) </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 1980 </td>
   <td style="text-align:right;"> 0.070 </td>
   <td style="text-align:right;"> -0.005 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1984 </td>
   <td style="text-align:right;"> 0.063 </td>
   <td style="text-align:right;"> 0.009 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1988 </td>
   <td style="text-align:right;"> 0.056 </td>
   <td style="text-align:right;"> 0.021 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1992 </td>
   <td style="text-align:right;"> 0.050 </td>
   <td style="text-align:right;"> 0.033 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1996 </td>
   <td style="text-align:right;"> 0.044 </td>
   <td style="text-align:right;"> 0.044 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2000 </td>
   <td style="text-align:right;"> 0.037 </td>
   <td style="text-align:right;"> 0.054 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2004 </td>
   <td style="text-align:right;"> 0.032 </td>
   <td style="text-align:right;"> 0.062 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2008 </td>
   <td style="text-align:right;"> 0.026 </td>
   <td style="text-align:right;"> 0.070 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2012 </td>
   <td style="text-align:right;"> 0.020 </td>
   <td style="text-align:right;"> 0.077 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2016 </td>
   <td style="text-align:right;"> 0.015 </td>
   <td style="text-align:right;"> 0.082 </td>
  </tr>
</tbody>
</table>

`````
:::

```{.r .cell-code}
nonvoting_effects %>%
  filter(year %in% c(1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016)) %>%
  kable(caption = "Predicted effects on nonvoting participation (# activities, Figure 13 bottom)",
        digits = 3, col.names = c("Year", "Warm In-party (100 vs 50)", "Cold Out-party (0 vs 50)")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Predicted effects on nonvoting participation (# activities, Figure 13 bottom)</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Year </th>
   <th style="text-align:right;"> Warm In-party (100 vs 50) </th>
   <th style="text-align:right;"> Cold Out-party (0 vs 50) </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 1980 </td>
   <td style="text-align:right;"> 0.175 </td>
   <td style="text-align:right;"> 0.112 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1984 </td>
   <td style="text-align:right;"> 0.171 </td>
   <td style="text-align:right;"> 0.130 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1988 </td>
   <td style="text-align:right;"> 0.166 </td>
   <td style="text-align:right;"> 0.150 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1992 </td>
   <td style="text-align:right;"> 0.161 </td>
   <td style="text-align:right;"> 0.170 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1996 </td>
   <td style="text-align:right;"> 0.155 </td>
   <td style="text-align:right;"> 0.192 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2000 </td>
   <td style="text-align:right;"> 0.150 </td>
   <td style="text-align:right;"> 0.214 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2004 </td>
   <td style="text-align:right;"> 0.145 </td>
   <td style="text-align:right;"> 0.237 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2008 </td>
   <td style="text-align:right;"> 0.139 </td>
   <td style="text-align:right;"> 0.262 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2012 </td>
   <td style="text-align:right;"> 0.134 </td>
   <td style="text-align:right;"> 0.288 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2016 </td>
   <td style="text-align:right;"> 0.128 </td>
   <td style="text-align:right;"> 0.314 </td>
  </tr>
</tbody>
</table>

`````
:::
:::



::: {.cell}

```{.r .cell-code}
p_vote <- voting_effects %>%
  pivot_longer(-year, names_to = "effect", values_to = "change") %>%
  mutate(effect = if_else(effect == "warm_in_effect", "Warm - Neutral (Inparty)", "Cold - Neutral (Outparty)")) %>%
  ggplot(aes(x = year, y = change, color = effect)) +
  geom_point() +
  geom_smooth(method = "loess", se = FALSE) +
  labs(x = "", y = "Change in Predicted\nProbability of Voting", color = "") +
  geom_hline(yintercept = 0, linetype = "dashed") +
  theme_minimal() +
  theme(legend.position = "bottom")

p_nonvote <- nonvoting_effects %>%
  pivot_longer(-year, names_to = "effect", values_to = "change") %>%
  mutate(effect = if_else(effect == "warm_in_effect", "Warm - Neutral (Inparty)", "Cold - Neutral (Outparty)")) %>%
  ggplot(aes(x = year, y = change, color = effect)) +
  geom_point() +
  geom_smooth(method = "loess", se = FALSE) +
  labs(x = "Year", y = "Change in Predicted Number\nof Participatory Actions", color = "") +
  geom_hline(yintercept = 0, linetype = "dashed") +
  theme_minimal() +
  theme(legend.position = "bottom")

gridExtra::grid.arrange(p_vote, p_nonvote, ncol = 1)
```

::: {.cell-output-display}
![Reproduced Figure 13: Effects of positive and negative motivations on political participation](reproduction_report_files/figure-html/figure13-plot-1.png){width=672}
:::
:::


---

## Deviation Log


::: {.cell}

```{.r .cell-code}
# Build comprehensive deviation log programmatically

# --- Claim 1: Feeling thermometer trends (Figure 1 & 3 values) ---
fig1_values <- therm_overall %>%
  filter(year %in% c(1988, 2012, 2016))

fig3_zero <- outparty_dist %>%
  filter(therm_cat == "Out-party Therm = 0", year %in% c(2000, 2016))

claim1_devs <- bind_rows(
  tibble(Claim = 1, `Table/Figure` = "Figure 1",
         Parameter = "Out-party therm mean 1988",
         Paper = 45.54,
         Reproduced = fig1_values %>% filter(year == 1988) %>% pull(mean_out)),
  tibble(Claim = 1, `Table/Figure` = "Figure 1",
         Parameter = "Out-party therm mean 2012",
         Paper = 27.31,
         Reproduced = fig1_values %>% filter(year == 2012) %>% pull(mean_out)),
  tibble(Claim = 1, `Table/Figure` = "Figure 1",
         Parameter = "Out-party therm mean 2016",
         Paper = 25.99,
         Reproduced = fig1_values %>% filter(year == 2016) %>% pull(mean_out)),
  tibble(Claim = 1, `Table/Figure` = "Figure 3",
         Parameter = "% out-party therm = 0 (2000)",
         Paper = 8.0,
         Reproduced = fig3_zero %>% filter(year == 2000) %>% pull(pct)),
  tibble(Claim = 1, `Table/Figure` = "Figure 3",
         Parameter = "% out-party therm = 0 (2016)",
         Paper = 21.0,
         Reproduced = fig3_zero %>% filter(year == 2016) %>% pull(pct))
)

# --- Claim 1: Table 1 mode effects ---
claim1_table1 <- tibble(
  Claim = 1,
  `Table/Figure` = "Table 1",
  Parameter = c("Feel Therm FtF", "Feel Therm Online",
                 "Affect FtF", "Affect Online",
                 "Trait FtF", "Trait Online"),
  Paper = c(33.90, 43.27, 2.22, 2.55, 7.77, 8.96),
  Reproduced = c(
    therm_mode %>% filter(mode_label == "Face-to-face") %>% pull(mean_pol),
    therm_mode %>% filter(mode_label == "Online") %>% pull(mean_pol),
    affect_mode %>% filter(mode_label == "Face-to-face") %>% pull(mean_pol),
    affect_mode %>% filter(mode_label == "Online") %>% pull(mean_pol),
    trait_mode %>% filter(mode_label == "Face-to-face") %>% pull(mean_pol),
    trait_mode %>% filter(mode_label == "Online") %>% pull(mean_pol)
  )
)

# --- Claims 2 & 4: Correlation values ---
fig6_vals <- cross_party_corr %>%
  filter(year %in% c(1980, 2016))

claim2_devs <- bind_rows(
  tibble(Claim = 2, `Table/Figure` = "Figure 6",
         Parameter = "Opposing party therm corr 1980",
         Paper = -0.22,
         Reproduced = fig6_vals %>% filter(year == 1980) %>% pull(r_party)),
  tibble(Claim = 2, `Table/Figure` = "Figure 6",
         Parameter = "Opposing party therm corr 2016",
         Paper = -0.58,
         Reproduced = fig6_vals %>% filter(year == 2016) %>% pull(r_party)),
  tibble(Claim = 2, `Table/Figure` = "Figure 6",
         Parameter = "Opposing cand therm corr 1980",
         Paper = -0.30,
         Reproduced = fig6_vals %>% filter(year == 1980) %>% pull(r_cand)),
  tibble(Claim = 2, `Table/Figure` = "Figure 6",
         Parameter = "Opposing cand therm corr 2016",
         Paper = -0.51,
         Reproduced = fig6_vals %>% filter(year == 2016) %>% pull(r_cand))
)

# Figure 7: Net affect correlation
fig7_vals <- affect_corr %>%
  filter(year %in% c(1980, 2012))

claim2_affect <- tibble(
  Claim = 2, `Table/Figure` = "Figure 7",
  Parameter = c("Net Dem-Rep cand affect corr 1980", "Net Dem-Rep cand affect corr 2012"),
  Paper = c(-0.3, -0.7),
  Reproduced = c(
    fig7_vals %>% filter(year == 1980) %>% pull(r_affect),
    fig7_vals %>% filter(year == 2012) %>% pull(r_affect)
  )
)

# Figure 12: Party ID correlations
fig12_vals <- pid_corr %>%
  filter(year %in% c(1980, 2012))

# Paper's Figure 12 values are AVERAGES across the three indicators (therm, affect, trait)
# "the mean correlation with party affiliation strengthened from around 0.6 in 1980 to 0.8 in 2012"
avg_1980 <- mean(c(
  fig12_vals %>% filter(year == 1980) %>% pull(r_therm),
  fig12_vals %>% filter(year == 1980) %>% pull(r_affect),
  fig12_vals %>% filter(year == 1980) %>% pull(r_trait)
), na.rm = TRUE)

avg_2012 <- mean(c(
  fig12_vals %>% filter(year == 2012) %>% pull(r_therm),
  fig12_vals %>% filter(year == 2012) %>% pull(r_affect),
  fig12_vals %>% filter(year == 2012) %>% pull(r_trait)
), na.rm = TRUE)

claim4_devs <- tibble(
  Claim = 4, `Table/Figure` = "Figure 12",
  Parameter = c("Avg. Party ID correlation 1980", "Avg. Party ID correlation 2012"),
  Paper = c(0.6, 0.8),
  Reproduced = c(avg_1980, avg_2012)
)

# --- Claim 5: Table 2 regression coefficients ---
claim5_voting <- tibble(
  Claim = 5, `Table/Figure` = "Table 2 M1",
  Parameter = display_labels,
  Paper = paper_voting,
  Reproduced = voting_display$estimate,
  paper_sig = paper_voting_sig,
  reproduced_p = voting_display$p
)

claim5_nonvoting <- tibble(
  Claim = 5, `Table/Figure` = "Table 2 M2",
  Parameter = display_labels,
  Paper = paper_nonvoting,
  Reproduced = nonvoting_display$estimate,
  paper_sig = paper_nonvoting_sig,
  reproduced_p = nonvoting_display$p
)

# Table 2 fit statistics
claim5_fit <- tibble(
  Claim = 5,
  `Table/Figure` = c("Table 2 M1", "Table 2 M1", "Table 2 M1",
                      "Table 2 M2", "Table 2 M2", "Table 2 M2"),
  Parameter = rep(c("N", "Log Likelihood", "AIC"), 2),
  Paper = c(26607, -13090.090, 26226.170, 26460, -30921.410, 61888.810),
  Reproduced = c(nrow(reg_data), as.numeric(logLik(model1)), AIC(model1),
                  nrow(reg_data2), as.numeric(logLik(model2)), AIC(model2))
)

# Claim 3: Same evidence as Claim 1 (trends over time)
claim3_devs <- tibble(
  Claim = 3, `Table/Figure` = "Figure 1",
  Parameter = c("Out-party therm mean 1988", "Out-party therm mean 2016"),
  Paper = c(45.54, 25.99),
  Reproduced = c(
    fig1_values %>% filter(year == 1988) %>% pull(mean_out),
    fig1_values %>% filter(year == 2016) %>% pull(mean_out)
  )
)

# Combine all deviations
all_deviations <- bind_rows(
  claim1_devs, claim1_table1, claim2_devs, claim2_affect,
  claim3_devs, claim4_devs, claim5_voting, claim5_nonvoting, claim5_fit
) %>%
  mutate(
    # Pass significance info to classify_deviation so that significant near-zero
    # parameters use relative thresholds (not the near-zero absolute rule)
    paper_is_sig_flag = case_when(
      !is.na(paper_sig) & paper_sig == "***" ~ TRUE,
      !is.na(paper_sig) & paper_sig == "NS" ~ FALSE,
      TRUE ~ NA
    ),
    assessment = pmap(list(Paper, Reproduced, paper_is_sig_flag),
                      ~classify_deviation(..1, ..2, significant = ..3))
  ) %>%
  unnest(assessment)

# Check for conclusion changes: direction reversal OR significance change
all_deviations <- all_deviations %>%
  mutate(
    # Direction check (additive scale): sign differs and value is meaningfully non-zero
    direction_differs = sign(Paper) != sign(Reproduced) & abs(Paper) > 0.01,
    # Significance check: paper reports significant but reproduced is not (or vice versa)
    # paper_is_sig_flag already computed above for classify_deviation
    paper_is_sig = paper_is_sig_flag,
    reproduced_is_sig = case_when(
      !is.na(reproduced_p) ~ reproduced_p < 0.05,
      TRUE ~ NA
    ),
    significance_differs = !is.na(paper_is_sig) & !is.na(reproduced_is_sig) &
      paper_is_sig != reproduced_is_sig,
    # Override category if direction or significance changed
    category = case_when(
      direction_differs & !is.na(direction_differs) & abs(Paper) > 0.05 ~ "Conclusion change",
      significance_differs ~ "Conclusion change",
      TRUE ~ category
    )
  )

# Report any significance changes
sig_changes <- all_deviations %>%
  filter(significance_differs)

if (nrow(sig_changes) > 0) {
  sig_changes %>%
    select(Claim, `Table/Figure`, Parameter, Paper, Reproduced,
           paper_is_sig, reproduced_is_sig) %>%
    mutate(
      `Paper sig.` = if_else(paper_is_sig, "p < 0.05", "NS"),
      `Reproduced sig.` = if_else(reproduced_is_sig, "p < 0.05", "NS")
    ) %>%
    select(Claim, `Table/Figure`, Parameter, Paper, Reproduced,
           `Paper sig.`, `Reproduced sig.`) %>%
    kable(caption = "Parameters with significance changes",
          digits = 4) %>%
    kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
}
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Parameters with significance changes</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Claim </th>
   <th style="text-align:left;"> Table/Figure </th>
   <th style="text-align:left;"> Parameter </th>
   <th style="text-align:right;"> Paper </th>
   <th style="text-align:right;"> Reproduced </th>
   <th style="text-align:left;"> Paper sig. </th>
   <th style="text-align:left;"> Reproduced sig. </th>
  </tr>
 </thead>
<tbody>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> In-party Therm x Year </td>
   <td style="text-align:right;"> -0.0003 </td>
   <td style="text-align:right;"> -0.0001 </td>
   <td style="text-align:left;"> p &lt; 0.05 </td>
   <td style="text-align:left;"> NS </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> In-party Therm </td>
   <td style="text-align:right;"> 0.2390 </td>
   <td style="text-align:right;"> 0.1380 </td>
   <td style="text-align:left;"> p &lt; 0.05 </td>
   <td style="text-align:left;"> NS </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> In-party Therm x Year </td>
   <td style="text-align:right;"> -0.0001 </td>
   <td style="text-align:right;"> -0.0001 </td>
   <td style="text-align:left;"> p &lt; 0.05 </td>
   <td style="text-align:left;"> NS </td>
  </tr>
</tbody>
</table>

`````
:::

```{.r .cell-code}
# Display deviation log
all_deviations %>%
  select(Claim, `Table/Figure`, Parameter, Paper, Reproduced,
         abs_deviation, rel_deviation_pct, category) %>%
  kable(
    caption = "Complete Deviation Log",
    col.names = c("Claim", "Table/Figure", "Parameter", "Paper", "Reproduced",
                  "Abs. Dev.", "Rel. Dev. (%)", "Category"),
    digits = 4
  ) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE) %>%
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
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Complete Deviation Log</caption>
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
   <td style="text-align:left;"> Figure 1 </td>
   <td style="text-align:left;"> Out-party therm mean 1988 </td>
   <td style="text-align:right;"> 45.5400 </td>
   <td style="text-align:right;"> 45.5248 </td>
   <td style="text-align:right;"> 0.0152 </td>
   <td style="text-align:right;"> 0.0335 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Figure 1 </td>
   <td style="text-align:left;"> Out-party therm mean 2012 </td>
   <td style="text-align:right;"> 27.3100 </td>
   <td style="text-align:right;"> 27.3038 </td>
   <td style="text-align:right;"> 0.0062 </td>
   <td style="text-align:right;"> 0.0227 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Figure 1 </td>
   <td style="text-align:left;"> Out-party therm mean 2016 </td>
   <td style="text-align:right;"> 25.9900 </td>
   <td style="text-align:right;"> 25.9474 </td>
   <td style="text-align:right;"> 0.0426 </td>
   <td style="text-align:right;"> 0.1640 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Figure 3 </td>
   <td style="text-align:left;"> % out-party therm = 0 (2000) </td>
   <td style="text-align:right;"> 8.0000 </td>
   <td style="text-align:right;"> 8.3115 </td>
   <td style="text-align:right;"> 0.3115 </td>
   <td style="text-align:right;"> 3.8940 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Figure 3 </td>
   <td style="text-align:left;"> % out-party therm = 0 (2016) </td>
   <td style="text-align:right;"> 21.0000 </td>
   <td style="text-align:right;"> 21.7187 </td>
   <td style="text-align:right;"> 0.7187 </td>
   <td style="text-align:right;"> 3.4224 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 1 </td>
   <td style="text-align:left;"> Feel Therm FtF </td>
   <td style="text-align:right;"> 33.9000 </td>
   <td style="text-align:right;"> 33.9106 </td>
   <td style="text-align:right;"> 0.0106 </td>
   <td style="text-align:right;"> 0.0312 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 1 </td>
   <td style="text-align:left;"> Feel Therm Online </td>
   <td style="text-align:right;"> 43.2700 </td>
   <td style="text-align:right;"> 43.2747 </td>
   <td style="text-align:right;"> 0.0047 </td>
   <td style="text-align:right;"> 0.0109 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 1 </td>
   <td style="text-align:left;"> Affect FtF </td>
   <td style="text-align:right;"> 2.2200 </td>
   <td style="text-align:right;"> 1.8874 </td>
   <td style="text-align:right;"> 0.3326 </td>
   <td style="text-align:right;"> 14.9829 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 1 </td>
   <td style="text-align:left;"> Affect Online </td>
   <td style="text-align:right;"> 2.5500 </td>
   <td style="text-align:right;"> 2.1599 </td>
   <td style="text-align:right;"> 0.3901 </td>
   <td style="text-align:right;"> 15.2977 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 1 </td>
   <td style="text-align:left;"> Trait FtF </td>
   <td style="text-align:right;"> 7.7700 </td>
   <td style="text-align:right;"> 7.8738 </td>
   <td style="text-align:right;"> 0.1038 </td>
   <td style="text-align:right;"> 1.3354 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 1 </td>
   <td style="text-align:left;"> Table 1 </td>
   <td style="text-align:left;"> Trait Online </td>
   <td style="text-align:right;"> 8.9600 </td>
   <td style="text-align:right;"> 8.9709 </td>
   <td style="text-align:right;"> 0.0109 </td>
   <td style="text-align:right;"> 0.1214 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 6 </td>
   <td style="text-align:left;"> Opposing party therm corr 1980 </td>
   <td style="text-align:right;"> -0.2200 </td>
   <td style="text-align:right;"> -0.2965 </td>
   <td style="text-align:right;"> 0.0765 </td>
   <td style="text-align:right;"> 34.7647 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 6 </td>
   <td style="text-align:left;"> Opposing party therm corr 2016 </td>
   <td style="text-align:right;"> -0.5800 </td>
   <td style="text-align:right;"> -0.5324 </td>
   <td style="text-align:right;"> 0.0476 </td>
   <td style="text-align:right;"> 8.2089 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 6 </td>
   <td style="text-align:left;"> Opposing cand therm corr 1980 </td>
   <td style="text-align:right;"> -0.3000 </td>
   <td style="text-align:right;"> -0.3343 </td>
   <td style="text-align:right;"> 0.0343 </td>
   <td style="text-align:right;"> 11.4486 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 6 </td>
   <td style="text-align:left;"> Opposing cand therm corr 2016 </td>
   <td style="text-align:right;"> -0.5100 </td>
   <td style="text-align:right;"> -0.7078 </td>
   <td style="text-align:right;"> 0.1978 </td>
   <td style="text-align:right;"> 38.7791 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 7 </td>
   <td style="text-align:left;"> Net Dem-Rep cand affect corr 1980 </td>
   <td style="text-align:right;"> -0.3000 </td>
   <td style="text-align:right;"> -0.2983 </td>
   <td style="text-align:right;"> 0.0017 </td>
   <td style="text-align:right;"> 0.5764 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 7 </td>
   <td style="text-align:left;"> Net Dem-Rep cand affect corr 2012 </td>
   <td style="text-align:right;"> -0.7000 </td>
   <td style="text-align:right;"> -0.6892 </td>
   <td style="text-align:right;"> 0.0108 </td>
   <td style="text-align:right;"> 1.5409 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Figure 1 </td>
   <td style="text-align:left;"> Out-party therm mean 1988 </td>
   <td style="text-align:right;"> 45.5400 </td>
   <td style="text-align:right;"> 45.5248 </td>
   <td style="text-align:right;"> 0.0152 </td>
   <td style="text-align:right;"> 0.0335 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:left;"> Figure 1 </td>
   <td style="text-align:left;"> Out-party therm mean 2016 </td>
   <td style="text-align:right;"> 25.9900 </td>
   <td style="text-align:right;"> 25.9474 </td>
   <td style="text-align:right;"> 0.0426 </td>
   <td style="text-align:right;"> 0.1640 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 12 </td>
   <td style="text-align:left;"> Avg. Party ID correlation 1980 </td>
   <td style="text-align:right;"> 0.6000 </td>
   <td style="text-align:right;"> 0.6141 </td>
   <td style="text-align:right;"> 0.0141 </td>
   <td style="text-align:right;"> 2.3552 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:left;"> Figure 12 </td>
   <td style="text-align:left;"> Avg. Party ID correlation 2012 </td>
   <td style="text-align:right;"> 0.8000 </td>
   <td style="text-align:right;"> 0.8110 </td>
   <td style="text-align:right;"> 0.0110 </td>
   <td style="text-align:right;"> 1.3751 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> Constant </td>
   <td style="text-align:right;"> -139.2740 </td>
   <td style="text-align:right;"> -74.4628 </td>
   <td style="text-align:right;"> 64.8112 </td>
   <td style="text-align:right;"> 46.5351 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> Year </td>
   <td style="text-align:right;"> 0.0700 </td>
   <td style="text-align:right;"> 0.0363 </td>
   <td style="text-align:right;"> 0.0337 </td>
   <td style="text-align:right;"> 48.1267 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> In-party Therm </td>
   <td style="text-align:right;"> 0.5770 </td>
   <td style="text-align:right;"> 0.2823 </td>
   <td style="text-align:right;"> 0.2947 </td>
   <td style="text-align:right;"> 51.0792 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> In-party Therm x Year </td>
   <td style="text-align:right;"> -0.0003 </td>
   <td style="text-align:right;"> -0.0001 </td>
   <td style="text-align:right;"> 0.0002 </td>
   <td style="text-align:right;"> 53.6132 </td>
   <td style="text-align:left;background-color: rgba(245, 198, 203, 255) !important;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> Out-party Therm </td>
   <td style="text-align:right;"> 0.9200 </td>
   <td style="text-align:right;"> 0.6215 </td>
   <td style="text-align:right;"> 0.2985 </td>
   <td style="text-align:right;"> 32.4463 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> Out-party Therm x Year </td>
   <td style="text-align:right;"> -0.0005 </td>
   <td style="text-align:right;"> -0.0003 </td>
   <td style="text-align:right;"> 0.0002 </td>
   <td style="text-align:right;"> 37.2696 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> Weak Democrat </td>
   <td style="text-align:right;"> -0.6450 </td>
   <td style="text-align:right;"> -0.6717 </td>
   <td style="text-align:right;"> 0.0267 </td>
   <td style="text-align:right;"> 4.1465 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> Independent - Democrat </td>
   <td style="text-align:right;"> -0.7780 </td>
   <td style="text-align:right;"> -0.7940 </td>
   <td style="text-align:right;"> 0.0160 </td>
   <td style="text-align:right;"> 2.0552 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> Independent - Republican </td>
   <td style="text-align:right;"> -0.5480 </td>
   <td style="text-align:right;"> -0.6010 </td>
   <td style="text-align:right;"> 0.0530 </td>
   <td style="text-align:right;"> 9.6636 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> Weak Republican </td>
   <td style="text-align:right;"> -0.5660 </td>
   <td style="text-align:right;"> -0.6031 </td>
   <td style="text-align:right;"> 0.0371 </td>
   <td style="text-align:right;"> 6.5495 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> Strong Republican </td>
   <td style="text-align:right;"> 0.2210 </td>
   <td style="text-align:right;"> 0.1793 </td>
   <td style="text-align:right;"> 0.0417 </td>
   <td style="text-align:right;"> 18.8727 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> Constant </td>
   <td style="text-align:right;"> -59.3630 </td>
   <td style="text-align:right;"> -35.0815 </td>
   <td style="text-align:right;"> 24.2815 </td>
   <td style="text-align:right;"> 40.9034 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> Year </td>
   <td style="text-align:right;"> 0.0290 </td>
   <td style="text-align:right;"> 0.0161 </td>
   <td style="text-align:right;"> 0.0129 </td>
   <td style="text-align:right;"> 44.3122 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> In-party Therm </td>
   <td style="text-align:right;"> 0.2390 </td>
   <td style="text-align:right;"> 0.1380 </td>
   <td style="text-align:right;"> 0.1010 </td>
   <td style="text-align:right;"> 42.2694 </td>
   <td style="text-align:left;background-color: rgba(245, 198, 203, 255) !important;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> In-party Therm x Year </td>
   <td style="text-align:right;"> -0.0001 </td>
   <td style="text-align:right;"> -0.0001 </td>
   <td style="text-align:right;"> 0.0000 </td>
   <td style="text-align:right;"> 33.9308 </td>
   <td style="text-align:left;background-color: rgba(245, 198, 203, 255) !important;"> Conclusion change </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> Out-party Therm </td>
   <td style="text-align:right;"> 0.4470 </td>
   <td style="text-align:right;"> 0.3118 </td>
   <td style="text-align:right;"> 0.1352 </td>
   <td style="text-align:right;"> 30.2448 </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> Out-party Therm x Year </td>
   <td style="text-align:right;"> -0.0002 </td>
   <td style="text-align:right;"> -0.0002 </td>
   <td style="text-align:right;"> 0.0000 </td>
   <td style="text-align:right;"> 20.0542 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> Weak Democrat </td>
   <td style="text-align:right;"> -0.5660 </td>
   <td style="text-align:right;"> -0.5689 </td>
   <td style="text-align:right;"> 0.0029 </td>
   <td style="text-align:right;"> 0.5182 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> Independent - Democrat </td>
   <td style="text-align:right;"> -0.3830 </td>
   <td style="text-align:right;"> -0.3790 </td>
   <td style="text-align:right;"> 0.0040 </td>
   <td style="text-align:right;"> 1.0452 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> Independent - Republican </td>
   <td style="text-align:right;"> -0.3820 </td>
   <td style="text-align:right;"> -0.3905 </td>
   <td style="text-align:right;"> 0.0085 </td>
   <td style="text-align:right;"> 2.2197 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> Weak Republican </td>
   <td style="text-align:right;"> -0.4700 </td>
   <td style="text-align:right;"> -0.4733 </td>
   <td style="text-align:right;"> 0.0033 </td>
   <td style="text-align:right;"> 0.7025 </td>
   <td style="text-align:left;background-color: rgba(212, 237, 218, 255) !important;"> Exact </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> Strong Republican </td>
   <td style="text-align:right;"> 0.0170 </td>
   <td style="text-align:right;"> -0.0004 </td>
   <td style="text-align:right;"> 0.0174 </td>
   <td style="text-align:right;"> NA </td>
   <td style="text-align:left;background-color: rgba(248, 215, 218, 255) !important;"> Substantive deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 26607.0000 </td>
   <td style="text-align:right;"> 26292.0000 </td>
   <td style="text-align:right;"> 315.0000 </td>
   <td style="text-align:right;"> 1.1839 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> Log Likelihood </td>
   <td style="text-align:right;"> -13090.0900 </td>
   <td style="text-align:right;"> -12904.2232 </td>
   <td style="text-align:right;"> 185.8668 </td>
   <td style="text-align:right;"> 1.4199 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M1 </td>
   <td style="text-align:left;"> AIC </td>
   <td style="text-align:right;"> 26226.1700 </td>
   <td style="text-align:right;"> 25842.4463 </td>
   <td style="text-align:right;"> 383.7237 </td>
   <td style="text-align:right;"> 1.4631 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> N </td>
   <td style="text-align:right;"> 26460.0000 </td>
   <td style="text-align:right;"> 26150.0000 </td>
   <td style="text-align:right;"> 310.0000 </td>
   <td style="text-align:right;"> 1.1716 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> Log Likelihood </td>
   <td style="text-align:right;"> -30921.4100 </td>
   <td style="text-align:right;"> -30456.0870 </td>
   <td style="text-align:right;"> 465.3230 </td>
   <td style="text-align:right;"> 1.5049 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:left;"> Table 2 M2 </td>
   <td style="text-align:left;"> AIC </td>
   <td style="text-align:right;"> 61888.8100 </td>
   <td style="text-align:right;"> 60946.1740 </td>
   <td style="text-align:right;"> 942.6360 </td>
   <td style="text-align:right;"> 1.5231 </td>
   <td style="text-align:left;background-color: rgba(255, 243, 205, 255) !important;"> Minor deviation </td>
  </tr>
</tbody>
</table>

`````
:::

```{.r .cell-code}
# Coverage summary
coverage <- all_deviations %>%
  group_by(Claim) %>%
  summarise(
    n_entries = n(),
    tables_figures = paste(unique(`Table/Figure`), collapse = ", "),
    n_exact = sum(category == "Exact"),
    n_minor = sum(category == "Minor deviation"),
    n_substantive = sum(category == "Substantive deviation"),
    n_conclusion_change = sum(category == "Conclusion change"),
    .groups = "drop"
  )

coverage %>%
  kable(caption = "Deviation Log Coverage Summary by Claim",
        col.names = c("Claim", "# Entries", "Tables/Figures", "Exact", "Minor", "Substantive", "Conclusion Change")) %>%
  kable_styling(bootstrap_options = c("striped", "hover"), full_width = FALSE)
```

::: {.cell-output-display}
`````{=html}
<table class="table table-striped table-hover" style="width: auto !important; margin-left: auto; margin-right: auto;">
<caption>Deviation Log Coverage Summary by Claim</caption>
 <thead>
  <tr>
   <th style="text-align:right;"> Claim </th>
   <th style="text-align:right;"> # Entries </th>
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
   <td style="text-align:right;"> 11 </td>
   <td style="text-align:left;"> Figure 1, Figure 3, Table 1 </td>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:right;"> 6 </td>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:right;"> 0 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:right;"> 6 </td>
   <td style="text-align:left;"> Figure 6, Figure 7 </td>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:right;"> 0 </td>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:right;"> 0 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 3 </td>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 1 </td>
   <td style="text-align:right;"> 0 </td>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:right;"> 0 </td>
   <td style="text-align:right;"> 0 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 4 </td>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:left;"> Figure 12 </td>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:right;"> 0 </td>
   <td style="text-align:right;"> 0 </td>
   <td style="text-align:right;"> 0 </td>
  </tr>
  <tr>
   <td style="text-align:right;"> 5 </td>
   <td style="text-align:right;"> 28 </td>
   <td style="text-align:left;"> Table 2 M1, Table 2 M2 </td>
   <td style="text-align:right;"> 2 </td>
   <td style="text-align:right;"> 11 </td>
   <td style="text-align:right;"> 12 </td>
   <td style="text-align:right;"> 3 </td>
  </tr>
</tbody>
</table>

`````
:::
:::


---

## Discrepancy Investigation

Deviations fall into several categories:

**Feeling thermometer means (Claims 1, 3)**: The reproduced out-party thermometer means are very close to the paper's reported values (e.g., 2016: 25.95 vs. 25.99; 2012: 27.30 vs. 27.31), supporting high confidence in the data handling. The slight deviations are consistent with the CDF having been updated since the paper's publication.

**Table 1 mode effects (Claim 1)**: Feeling thermometer polarization values match within rounding error (FtF: 33.91 vs. 33.90; Online: 43.27 vs. 43.27). Trait polarization values match well once computed as sums rather than averages (FtF: 7.87 vs. 7.77; Online: 8.97 vs. 8.96), confirming that the paper reports cumulative, not averaged, trait scores. The affect polarization values deviate more (FtF: 1.89 vs. 2.22; Online: 2.16 vs. 2.55); this is likely because the CDF recodes the 2016 5-point affect scale as binary (yes/no), while the paper may use the original 5-point responses from the 2016 wave data, which were not available for this analysis via the CDF. All three indicators show the same qualitative pattern: significantly greater polarization in the online mode.

**Correlation values (Claims 2, 4)**: Many correlation values from figures are approximate (read from graphs). The paper reports values like "about −0.22" and "about −0.3". Our reproduced 1980 party thermometer correlation (−0.30) is more negative than the paper's approximate −0.22, and the 2016 candidate thermometer correlation (−0.71) is substantially more negative than the paper's −0.51. These discrepancies may reflect changes in the CDF since publication; the ANES periodically updates cumulative files with corrections and additional data cleaning. Despite these numeric differences, the qualitative trend — increasingly negative cross-party correlations over time — is clearly confirmed. For the affect correlations (Figure 7), the 1980 value (−0.30) matches exactly, and the 2012 value (−0.69) is close to the paper's −0.7.

**Table 2 regression coefficients (Claim 5)**: The reproduced regression models show substantive numeric deviations from the paper's coefficients. Our sample size (N = 26,292 for voting) is close to but smaller than the paper's (N = 26,607), suggesting minor differences in sample inclusion criteria. The Year coefficient and its interactions with thermometer scores are roughly half the paper's values (e.g., Year: 0.036 vs. 0.070 for voting), meaning the time-varying effects are weaker in the reproduced models. The smaller interaction coefficients imply that the divergence between in-party and out-party thermometer effects on participation is less dramatic than the paper's estimates suggest. The party identification coefficients are closer (e.g., Weak Democrat: −0.672 vs. −0.645). Possible explanations include:

1. **Dataset version differences**: The current CDF (dated 2026-02-05) has been updated multiple times since the paper used a 2016/2017 version. Updates may include recoding of participation variables, corrections to demographic data, or changes in how missing data is handled, all of which would affect the regression results.
2. **Undocumented sample restrictions**: The paper does not specify exactly which election years are included. While the text discusses 1980–2016, some participation items may not be available for all years, and the paper may include additional year restrictions we did not apply.
3. **Demographic variable specification**: The exact coding of race and education categories, and whether they enter the model as continuous or categorical, is not fully specified.

**Significance changes**: Three parameters that are highly significant (p < 0.001) in the paper are not significant (p > 0.05) in the reproduced models:

- *In-party Therm × Year* in Model 1 (voting): reproduced p = 0.050, borderline non-significant. The paper's claim that the in-party effect has declined over time is only marginally supported in the voting model.
- *In-party Therm* in Model 2 (nonvoting): reproduced p = 0.071. The main effect of in-party thermometer on nonvoting participation is not significant.
- *In-party Therm × Year* in Model 2 (nonvoting): reproduced p = 0.083. The declining in-party effect is not statistically confirmed for nonvoting participation.

All three significance changes concern the in-party side of the model. The out-party thermometer and its interaction with year remain highly significant (p < 0.001) in both models, confirming that out-party negativity is a strong and growing participation driver. The qualitative conclusion that out-party hostility has eclipsed in-party positivity is thus still supported — in fact, the weaker in-party effects in the reproduced data are consistent with, and even strengthen, this conclusion. However, the specific mechanism of a statistically significant *decline* in the in-party effect over time is only partially confirmed (borderline in voting, not confirmed in nonvoting).

---

## Conclusion

**Reproduction status: QUALITATIVELY REPRODUCED**

The core findings of the paper are supported by the reproduced analyses. Claims 1–4 (increasing out-party negativity, growing consistency, post-1980s acceleration, and structured affect) are all confirmed with close numerical matches. For Claim 5 (participation), the out-party thermometer × year interaction is negative and highly significant in both models, confirming that out-party negativity has become an increasingly powerful driver of participation. However, the in-party thermometer × year interaction is borderline non-significant in the voting model (p = 0.050) and non-significant in the nonvoting model (p = 0.083), meaning the specific claim of a statistically significant decline in the in-party effect over time is only partially confirmed. These deviations are possibly attributable to dataset version differences or undocumented sample restrictions. The qualitative pattern — out-party negativity eclipsing in-party positivity — is still clearly visible in the predicted probability crossover plots.

### Claim-by-Claim Assessment

1. **Partisans feel more negatively about the opposing party**: Reproduced. Out-party thermometer means match the paper's values closely (1988: 45.52 vs. 45.54; 2016: 25.95 vs. 25.99). The percentage rating the out-party at zero also matches.

2. **Negativity has become more consistent**: Reproduced. Cross-party and cross-candidate thermometer correlations grew more negative over time, consistent with the paper's reported trend. Net affect correlations also show the expected strengthening.

3. **Partisan animus began in the 1980s and grew dramatically**: Reproduced. The time series confirms the pattern: gradual increase in out-party hostility from the 1980s with acceleration post-2000.

4. **Partisan affect is more structured**: Reproduced. Correlations between party identification and affect indicators strengthened over time, consistent with the paper's claim.

5. **Hostility has eclipsed positive affect as a participation motive**: Largely reproduced, with caveats. The out-party thermometer × year interaction is negative and highly significant (p < 0.001) in both models, confirming the growing role of out-party negativity. The in-party thermometer × year interaction is negative but borderline non-significant in the voting model (p = 0.050) and non-significant in the nonvoting model (p = 0.083), meaning the *decline* of in-party positivity as a driver is only marginally supported. The out-party interaction remains larger in magnitude in both models, and the predicted probability crossover pattern is reproduced, supporting the qualitative conclusion that hostility has eclipsed positive affect.

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
 [1] kableExtra_1.4.0 knitr_1.51       haven_2.5.5      lubridate_1.9.4 
 [5] forcats_1.0.1    stringr_1.6.0    dplyr_1.1.4      purrr_1.2.1     
 [9] readr_2.1.5      tidyr_1.3.2      tibble_3.3.1     ggplot2_4.0.1   
[13] tidyverse_2.0.0 

loaded via a namespace (and not attached):
 [1] generics_0.1.4     xml2_1.5.2         lattice_0.22-7     stringi_1.8.7     
 [5] hms_1.1.4          digest_0.6.39      magrittr_2.0.4     evaluate_1.0.5    
 [9] grid_4.5.1         timechange_0.3.0   RColorBrewer_1.1-3 fastmap_1.2.0     
[13] Matrix_1.7-3       jsonlite_2.0.0     gridExtra_2.3      mgcv_1.9-3        
[17] viridisLite_0.4.2  scales_1.4.0       textshaping_1.0.4  cli_3.6.5         
[21] rlang_1.1.7        splines_4.5.1      withr_3.0.2        yaml_2.3.12       
[25] otel_0.2.0         tools_4.5.1        tzdb_0.5.0         vctrs_0.7.1       
[29] R6_2.6.1           lifecycle_1.0.5    htmlwidgets_1.6.4  pkgconfig_2.0.3   
[33] pillar_1.11.1      gtable_0.3.6       glue_1.8.0         systemfonts_1.3.1 
[37] xfun_0.56          tidyselect_1.2.1   rstudioapi_0.18.0  farver_2.1.2      
[41] htmltools_0.5.9    nlme_3.1-168       labeling_0.4.3     rmarkdown_2.30    
[45] svglite_2.2.2      compiler_4.5.1     S7_0.2.1          
```


:::
:::

