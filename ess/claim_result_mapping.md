# Claim-Result Mapping: Huppert & So (2013)

**Paper**: Huppert, F. A., & So, T. T. C. (2013). Flourishing Across Europe: Application of a New Conceptual Framework for Defining Well-Being. *Social Indicators Research*, 110, 837–861.

**Data**: European Social Survey Round 3 (2006/2007), ESS3e03_7.sav

## Data Sources

- ESS Round 3 integrated file (edition 3.7)
- 23 countries, ~43,000 respondents
- Hungary excluded due to missing vitality data → 22 countries for analysis

## Claims from the Abstract

### Claim 1: Factor structure reveals hedonic and eudaimonic dimensions
**Verbatim**: "By examining internationally agreed criteria for depression and anxiety (DSM and ICD classifications), and defining the opposite of each symptom, we identify ten features of positive well-being [...] an operational definition of flourishing is developed, based on psychometric analysis of indicators of these ten features"

**Location**: Tables 2, 3, 4 (pp. 845-846)
**Key values to reproduce**:
- Table 2: Spearman correlation matrix (45 pairwise correlations)
- Table 3: 2-factor EFA with oblique rotation, 43% variance explained
  - Factor 1 (31.8%): emotional stability .77, vitality .68, resilience .57, optimism .56, happiness .56, self-esteem .50
  - Factor 2 (11.1%): engagement .68, meaning .64, competence .59, positive relationships .59
- Table 4: 3-factor EFA with life satisfaction added, 52.0% total variance
  - Factor 3 (9.3%): life satisfaction .86, positive emotion .83

**Statistical method**: Spearman correlations; Exploratory Factor Analysis with oblique rotation
**Parameter registry**: Factor loadings ≥0.5 on primary factor, variance explained percentages

### Claim 2: Four-fold difference in flourishing prevalence across Europe
**Verbatim**: "a four-fold difference in flourishing rate, from 41% in Denmark to less than 10% in Slovakia, Russia and Portugal"

**Location**: Figure 1, p. 848; text p. 848
**Key values to reproduce**:
- Denmark: 40.6% (highest)
- Portugal: 9.3% (lowest)
- Slovakia: 9.9%
- Russian Federation: 9.4%
- Overall European prevalence: 15.8%

**Statistical method**: Weighted prevalence calculation using the operational definition of flourishing
**Operational definition**: Positive emotion present + all but one of the 5 "positive characteristics" (emotional stability, vitality, resilience, optimism, self-esteem) + all but one of the 4 "positive functioning" features (engagement, meaning, competence, positive relationships)

**Cut points for feature presence**:
- Agree/disagree items (1-5): "Agree" or "Strongly agree" (i.e., 1 or 2), except:
  - Engagement: "Strongly agree" only (1) because 80.5% agreed
  - Positive relationships: "Strongly agree" only (1) because 90.2% agreed
- Positive emotion (happy, 0-10): 8-10 (positive skew, median 7-8)
- Emotional stability & Vitality (1-4 frequency): "All or almost all of the time" or "Most of the time" (3 or 4)
- Resilience: REVERSE scored, then same as agree/disagree (disagree or strongly disagree with original = 4 or 5)

**Parameter registry**: Country-level flourishing prevalence (%) for all 22 countries

### Claim 3: Measurement equivalence across European regions
**Verbatim** (implied): Applied the definition to "23 countries which participated in the European Social Survey (Round 3)"

**Location**: Table 5, p. 847
**Key values to reproduce**:
- Model 1 (configural): χ²=2444.55, df=90, CFI=.96, GFI=.98, RMSEA=.027 (.026-.028)
- Model 2 (metric): χ²=2845.22, df=106, CFI=.96, GFI=.99, RMSEA=.026 (.025-.027)
- Model 3 (scalar): χ²=7205.18, df=126, CFI=.96, GFI=.98, RMSEA=.038 (.037-.039)
- Model 4 (strict): χ²=7415.25, df=132, CFI=.95, GFI=.98, RMSEA=.038 (.037-.038)

**Statistical method**: Multi-group CFA with SEM, 3 regions (Northern, Southern/Western, Eastern Europe)
**Regions**:
- Northern Europe (n=7,078): Denmark, Finland, Norway, Sweden
- Southern/Western Europe (n=22,085): Austria, Belgium, Cyprus, France, Germany, Ireland, Netherlands, Portugal, Spain, Switzerland, United Kingdom
- Eastern Europe (n=13,837): Bulgaria, Estonia, Poland, Russian Federation, Slovakia, Slovenia, Ukraine

**Parameter registry**: χ², df, CFI, GFI, RMSEA for all 4 models; Δχ²(Δdf) for models 2-4

### Claim 4: Striking differences in country profiles across features
**Verbatim**: "There are also striking differences in country profiles across the 10 features"

**Location**: Table 6, Figure 2 (pp. 849-851)
**Key values to reproduce**: Country rankings on each feature (Table 6)
**Statistical method**: Weighted percentage meeting criterion for each feature, ranked across countries

**Parameter registry**: Selected country rankings (Denmark, Portugal, Slovakia top/bottom positions)

### Claim 5: Life satisfaction is insufficient measure of well-being
**Verbatim**: "Comparison with a life satisfaction measure shows that valuable information would be lost if well-being was measured by life satisfaction"

**Location**: pp. 844, 847; Tables 3-4
**Key values to reproduce**:
- Spearman correlation between flourishing and life satisfaction: .34 (p < .01)
- Life satisfaction correlated .68 with positive emotion (happiness)
- Correlations of life satisfaction with other flourishing items: .11 (engagement) to .49 (self-esteem)
- 7.3% both flourishing and high life satisfaction
- Among flourishers: 46.0% had high life satisfaction
- Among those with high life satisfaction: 38.7% were flourishing
- High life satisfaction cut point: 9-10 on 0-10 scale (18.1% of sample)

**Parameter registry**: Correlation flourishing-life satisfaction, overlap percentages, factor loadings in 3-factor solution (Table 4)

## Analytical Decisions to Watch

1. **Weighting**: Paper says "Data were weighted using standard ESS techniques" — likely dweight × pweight
2. **Standardisation within regions**: "Scores on each item were standardised within each region" before analyses — this is a notable step that could affect correlations and factor structure
3. **Cut points**: The specific cut points for each item are crucial and detailed in the paper
4. **Factor analysis method**: "Exploratory Factor Analysis (EFA) with oblique rotation" — specific rotation method not named (promax? oblimin?)
5. **Missing data handling**: Not specified — listwise deletion assumed
6. **Happiness item**: Paper uses "Taking all things together, how happy would you say you are?" — this is the core ESS happiness item (`happy`), not from the well-being module

## Potentially Questionable Analytical Choices

1. **Within-region standardisation**: Standardising items within geographic regions before computing correlations and factor analyses could introduce artifacts and is not standard practice. The rationale given (reducing response set differences) is reasonable but the approach is unusual.
2. **Single-item indicators**: Using only one item per construct is acknowledged as a limitation but could affect factor structure reliability.
3. **Cut-point selection**: The method for choosing cut-points (response format-based, adjusted for skew) is somewhat ad hoc.
