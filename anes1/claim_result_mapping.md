# Claim-Result Mapping: Iyengar & Krupenkin (2018) "The Strengthening of Partisan Affect"

## Data Sources
- **ANES Time Series Cumulative Data File** (anes_timeseries_cdf_spss_20260205.sav) — for all longitudinal analyses
- **ANES 2016 Time Series** (anes_timeseries_2016.sav) — for 2016 mode effects (Table 1)

## Open Materials
- **Replication code**: Not available
- **Supplementary appendix**: Available at Stanford PCL (https://pcl.sites.stanford.edu/sites/g/files/sbiybj22066/files/media/file/iyengar-app-strengthening.pdf)
- **Raw data**: Publicly available from ANES (electionstudies.org)

## Claims from the Abstract

### Claim 1: Partisans feel more negatively about the opposing party
**Verbatim**: "we find that partisans not only feel more negatively about the opposing party"
**Location**: Figures 1–5, Table 1 (mode effects as supplementary evidence)
**Key values**:
- Figure 1: Out-party feeling thermometer means by year (1978–2016); in-party means ~70 stable; out-party declined from ~45 (1988) to ~25 (2016)
- Specific text values: Out-party therm 2016 = 25.99, 2012 = 27.31, 1988 = 45.54 (p. 203)
- Figure 3: % out-party therm = 0 went from 8% (2000) to 21% (2016) (p. 203)
- Table 1: Mode effects on net polarization (in-party minus out-party): Feel Therm FtF = 33.90, Online = 43.27, p < 0.001; Affect FtF = 2.22, Online = 2.55, p < 0.001; Trait FtF = 7.77, Online = 8.96, p < 0.001

### Claim 2: Negativity has become more consistent
**Verbatim**: "this negativity has become more consistent"
**Location**: Figures 6–11
**Key values** (from text p. 208–210):
- Figure 6 top: Opposing party therm correlation: −0.22 (1980) → more than doubled to −0.58 (2016)
- Figure 6 top: Opposing candidate therm correlation: −0.30 (1980) → −0.51 (2016)
- Figure 6 bottom: Intra-party therm correlation (Dem): ~0.6 → 0.75; (Rep): ~0.6 → 0.65
- Figure 7: Net Dem-Rep candidate affect correlation: −0.3 (1980) → −0.7 (2012)
- Figure 8: Within-candidate positive-negative affect correlation: −0.3 → −0.5
- Figure 9: Dem-Rep candidate trait correlation: −0.2 (1980s) → −0.6 (2016)
- Figure 10: Within-candidate trait correlation: ~0.4 (1980) → ~0.8 (2016)
- Figure 12: Partisanship-affect correlation averaged: ~0.6 (1980) → ~0.8 (2012)

### Claim 3: Partisan animus began to rise in 1980s and has grown dramatically over past two decades
**Verbatim**: "while partisan animus began to rise in the 1980s, it has grown dramatically over the past two decades"
**Location**: Figures 1, 2, 3
**Key values**: Same as Claim 1 — trend analysis of thermometer means over time. Also Figure 2 distribution shifts (2004–2016) and Figure 3 percentage breakdowns.

### Claim 4: As partisan affect intensified, it is more structured — ingroup favoritism increasingly associated with outgroup animus
**Verbatim**: "As partisan affect has intensified, it is also more structured; ingroup favoritism is increasingly associated with outgroup animus"
**Location**: Figures 6–12
**Key values**: Same correlation time series as Claim 2. Key evidence is strengthening negative correlations between in-party and out-party evaluations.

### Claim 5: Hostility toward opposing party has eclipsed positive affect as a motive for political participation
**Verbatim**: "hostility toward the opposing party has eclipsed positive affect for ones' own party as a motive for political participation"
**Location**: Table 2, Figure 13
**Key values from Table 2**:
- Model 1 (Voting logit): Year = 0.070*** (0.006), In-party Therm = 0.577*** (0.143), In-party Therm × Year = −0.0003*** (0.0001), Out-party Therm = 0.920*** (0.122), Out-party Therm × Year = −0.0005*** (0.0001), Strong Democrat = ref, Weak Democrat = −0.645*** (0.050), Indep-Dem = −0.778*** (0.055), Indep-Rep = −0.548*** (0.060), Weak Rep = −0.566*** (0.057), Strong Rep = 0.221*** (0.064), Constant = −139.274*** (11.802), N = 26,607, Log Likelihood = −13,090.090, AIC = 26,226.170
- Model 2 (Nonvoting Participation): Year = 0.029*** (0.003), In-party Therm = 0.239*** (0.077), In-party Therm × Year = −0.0001*** (0.00004), Out-party Therm = 0.447*** (0.064), Out-party Therm × Year = −0.0002*** (0.00003), Strong Dem = ref, Weak Dem = −0.566*** (0.027), Indep-Dem = −0.383*** (0.029), Indep-Rep = −0.382*** (0.031), Weak Rep = −0.470*** (0.030), Strong Rep = 0.017 (0.025), Constant = −59.363*** (6.555), N = 26,460, Log Likelihood = −30,921.410, AIC = 61,888.810
- Text values (p. 213–214): In 1980, warm (100) in-party therm → +8% voting probability vs neutral (50); hostile (0) out-party → −3% voting probability. By 2016, in-party 50→100 had no effect on turnout; out-party 50→0 increased voting by 8%.
- Nonvoting: 1980 out-party negativity → 0.1 increase; by 2016 → 0.4 increase (fourfold).

## Parameter Registry

### Table 1 Parameters (Claim 1)
| Parameter | Paper Value |
|-----------|-------------|
| Feel Therm - FtF mean | 33.90 |
| Feel Therm - Online mean | 43.27 |
| Feel Therm - p-value | < 0.001 |
| Affect - FtF mean | 2.22 |
| Affect - Online mean | 2.55 |
| Affect - p-value | < 0.001 |
| Trait - FtF mean | 7.77 |
| Trait - Online mean | 8.96 |
| Trait - p-value | < 0.001 |

### Table 2 Model 1 Parameters (Claim 5)
| Parameter | Paper Value |
|-----------|-------------|
| Year | 0.070 (0.006) |
| In-party Therm | 0.577 (0.143) |
| In-party Therm × Year | −0.0003 (0.0001) |
| Out-party Therm | 0.920 (0.122) |
| Out-party Therm × Year | −0.0005 (0.0001) |
| Weak Democrat | −0.645 (0.050) |
| Indep-Dem | −0.778 (0.055) |
| Indep-Rep | −0.548 (0.060) |
| Weak Rep | −0.566 (0.057) |
| Strong Rep | 0.221 (0.064) |
| Constant | −139.274 (11.802) |
| N | 26,607 |
| Log Likelihood | −13,090.090 |
| AIC | 26,226.170 |

### Table 2 Model 2 Parameters (Claim 5)
| Parameter | Paper Value |
|-----------|-------------|
| Year | 0.029 (0.003) |
| In-party Therm | 0.239 (0.077) |
| In-party Therm × Year | −0.0001 (0.00004) |
| Out-party Therm | 0.447 (0.064) |
| Out-party Therm × Year | −0.0002 (0.00003) |
| Weak Democrat | −0.566 (0.027) |
| Indep-Dem | −0.383 (0.029) |
| Indep-Rep | −0.382 (0.031) |
| Weak Rep | −0.470 (0.030) |
| Strong Rep | 0.017 (0.025) |
| Constant | −59.363 (6.555) |
| N | 26,460 |
| Log Likelihood | −30,921.410 |
| AIC | 61,888.810 |

### Figure-based Parameters (Claims 1–4)
| Parameter | Source | Paper Value |
|-----------|--------|-------------|
| Out-party therm mean 2016 | Fig 1, p.203 | 25.99 |
| Out-party therm mean 2012 | Fig 1, p.203 | 27.31 |
| Out-party therm mean 1988 | Fig 1, p.203 | 45.54 |
| % out-party therm = 0, 2000 | Fig 3, p.203 | 8% |
| % out-party therm = 0, 2016 | Fig 3, p.203 | 21% |
| Opposing party therm corr 1980 | Fig 6, p.208 | −0.22 |
| Opposing party therm corr 2016 | Fig 6, p.208 | −0.58 |
| Opposing cand therm corr 1980 | Fig 6, p.208 | −0.30 |
| Opposing cand therm corr 2016 | Fig 6, p.208 | −0.51 |
| Intra-party therm corr Dem ~2016 | Fig 6, p.208 | ~0.75 |
| Intra-party therm corr Rep ~2016 | Fig 6, p.208 | ~0.65 |
| Net Dem-Rep cand affect corr 1980 | Fig 7, p.208 | ~−0.3 |
| Net Dem-Rep cand affect corr 2012 | Fig 7, p.208-209 | ~−0.7 |
| Partisanship-affect corr avg 1980 | Fig 12, p.210 | ~0.6 |
| Partisanship-affect corr avg 2012 | Fig 12, p.210 | ~0.8 |

## Analytical Decisions to Watch
1. **Party ID classification**: "independent leaners" classified as partisans (7-point → 4-point: Strong D = 1, Weak/Lean D = 2, Weak/Lean R = 3, Strong R = 4)
2. **Exclusion of independents and minor party identifiers**: Only partisans (including leaners) included
3. **Affect items**: In 2016, ANES changed affect items to 5-point scale; authors EXCLUDE 2016 from affect time series (footnote 1, p.203)
4. **Trait rescaling**: −2 (not well at all) to 2 (extremely well), averaged across traits per candidate
5. **Net affect**: positive affect average minus negative affect average (yes=1, no=0)
6. **Thermometer "polarization" for Table 1**: In-party rating minus out-party rating
7. **Demographics in Table 2**: Age, gender, race, year of survey, education (footnote 3, p.212)
8. **Predicted probabilities** (Figure 13): Using mean age, modal values of other covariates (footnote 4, p.212)
9. **Nonvoting participation**: Sum of 5 behaviors (rally, donate, mobilize, sticker/button, work for party/candidate)
10. **Participation model**: Binomial logit regression (footnote 4)
11. **The paper does not mention using survey weights** — this is a notable omission for ANES data
