# Claim-Result Mapping: Munzert & Bauer (2013)

**Paper**: Munzert, S. & Bauer, P.C. (2013). Political Depolarization in German Public Opinion, 1980–2010. *Political Science Research and Methods*, 1(1), 67–89.

**Data sources**:
- ALLBUS Cumulation 1980–2008 (ZA4572) — `data/allbus/ZA4572_allbus_cumulation_to_2008.sav`
- ALLBUS Cumulation 1980–2010 (ZA4576) — `data/allbus/ZA4576_allbus_cumulation_to_2010.sav`
- ALLBUS 2010 individual wave (ZA4610) — `data/allbus/ZA4610_v1-1-0_2010.sav`

## Claims from the Abstract

1. **POP as alignment**: "Public opinion polarization is conceptualized and measured as alignment of attitudes across multiple issue dimensions using pairwise correlations."
   - Location: Methodology section (pp. 69–75), Table 2
   - Values: Pairwise Pearson correlations between attitude scales as DV in multilevel models; 806 pair-year observations across 252 unique pairs
   - Method: Multilevel models (varying intercept, varying slope) with time (decades, centered 1994) as predictor

2. **Overall decrease**: "Public opinion polarization has decreased over the last three decades in Germany."
   - Location: Table 2 Model A
   - Values: Intercept = 0.19 (SE 0.01), Time trend = −0.04 (SE 0.00)
   - Method: Multilevel model with all 252 pairs, no grouping

3. **Dimension-specific patterns**: Multilevel models reveal general and dimension-specific levels and trends in attitude alignment.
   - Location: Table 2 Models B and C
   - Values (Model B): Intercept = 0.14 (0.01), Within dimension = 0.18 (0.01), Time = −0.04 (0.00), Time × Within = 0.02 (0.01)
   - Values (Model C): Intercept = 0.36 (0.02), Gender = baseline, Moral = −0.12 (0.03), Distribution = −0.07 (0.02), Immigration = 0.01 (0.03), Mixed = −0.22 (0.02), Time = 0.04 (0.01), Time × Gender = baseline, Time × Moral = −0.09 (0.03), Time × Distribution = −0.08 (0.01), Time × Immigration = −0.08 (0.01), Time × Mixed = −0.07 (0.01)
   - Method: Model B adds within-dimension indicator; Model C adds dimension type indicators and time interactions

4. **Highly educated/politically interested depolarize more**: "highly educated and more politically interested people have become less polarized over time"
   - Location: Figure 4 (sub-group analysis), pp. 79–80
   - Values: Steeper negative overall trends for highly educated and politically interested sub-groups
   - Method: Separate multilevel models (Model A specification) run on sub-samples

5. **Gender issues increase**: "polarization seems to have increased in attitudes regarding gender issues"
   - Location: Table 2 Model C (Time = 0.04, which is the gender baseline time trend), Figure 3
   - Values: Gender dimension shows positive time trend (0.04 per decade); all other dimensions show negative net trends
   - Method: Model C — time trend for gender dimension = 0.04 (0.01)

## Parameter Registry

### Table 2, Model A (Claim 2)
- Intercept: 0.19
- Time (decades): −0.04
- Residual variance σ²_α: 0.01
- Residual variance σ²_β: 0.00
- Residual variance σ²_ε: 0.00
- N observations: 806
- N item pairs: 252

### Table 2, Model B (Claim 3)
- Intercept: 0.14
- Within dimension pairs: 0.18
- Time (decades): −0.04
- Time × Within dimension: 0.02
- Residual variance σ²_α: 0.01
- Residual variance σ²_β: 0.00
- Residual variance σ²_ε: 0.00

### Table 2, Model C (Claims 3, 5)
- Intercept: 0.36
- Gender: baseline
- Moral: −0.12
- Distribution: −0.07
- Immigration: 0.01
- Mixed: −0.22
- Time (decades): 0.04
- Time × Gender: baseline
- Time × Moral: −0.09
- Time × Distribution: −0.08
- Time × Immigration: −0.08
- Time × Mixed: −0.07
- Residual variance σ²_α: 0.00
- Residual variance σ²_β: 0.00
- Residual variance σ²_ε: 0.00

### Figure 4 / Sub-group analysis (Claim 4)
- Overall time trends for education sub-groups (more vs. less educated)
- Overall time trends for political interest sub-groups (more vs. less interested)
- Direction and relative magnitude of trends

## Analytical Choices to Flag

1. **Item classification into dimensions**: Done by 7 raters using "manual exploratory factor analysis." Disagreements existed for some immigration items. Authors kept all items in 4-dimension solution. This is subjective and potentially consequential.

2. **Reverse coding**: Items formulated negatively were reversed so that answer categories follow the direction of the respective dimension (liberal → conservative). The exact recoding decisions are not fully documented.

3. **Correlation as DV without transformation**: Pearson correlations have natural bounds at −1 and 1, but authors model them with linear multilevel models without Fisher z-transformation. They justify this by noting observed correlations are far from the bounds.

4. **Time variable**: Rescaled to decades and centered at 1994. This is clearly stated.

5. **Pairwise-complete correlations**: The unit of observation is issue pairs, not individuals. Correlations are computed for each pair in each wave where both items were asked.

6. **Sub-group definitions**: Footnote 14 defines more educated = Abitur (academic high school diploma); less educated = no certificate or at most secondary education. Political interest: very strongly or strongly interested vs. hardly or no interest. Income: >2000 euros = high, <500 euros = low.
