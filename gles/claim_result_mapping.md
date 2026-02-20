# Claim-Result Mapping: Steiner, Schimpf & Wuttke (2023)

## Paper
"Left Behind and United by Populism? Populism's Multiple Roots in Feelings of Lacking Societal Recognition"
*Politische Vierteljahresschrift* 64:107–132. https://doi.org/10.1007/s11615-022-00416-4

## Data Source
- **Dataset**: GLES Cross-Section 2021, Pre-Election (ZA7700)
- **Cited version**: 2.0.0
- **Available version**: 3.1.0 (version discrepancy to be documented)
- **Source**: GESIS, https://doi.org/10.4232/1.13860
- **N**: 5116 (paper reports); 175 excluded for missing poststratification weight → analysis N ~4941

## Open Materials
- **Preregistration**: https://osf.io/kje48
- **OSF repository**: https://osf.io/b3tj4/ — contains replication code (Stata .do files), R plotting script, and processed data (ZA6800, a different study number)
- **Supplementary appendix**: Available via Springer (electronic supplementary material)
- **Note**: Replication materials will NOT be consulted until Stage 6 (if needed)

## Claims from the Abstract

### Claim 1: Multiple social segments harbor feelings of lacking recognition
**Verbatim**: "from rural residents to sociocultural conservatives or low-income citizens, seemingly unrelated segments of society harbor feelings of lacking recognition, but for distinct reasons"

**Location**: Figure 3 (p. 123), supported by Table D1 in appendix
**Statistical method**: Weighted mean comparisons with t-tests (p < 0.05)
**Key results to reproduce**:
- Low-income individuals: higher lack of economic recognition (0.61 vs 0.47)
- Low-skilled workers: higher lack of work recognition (0.59 vs 0.51)
- Rural residents: higher lack of services recognition (0.52 vs 0.49; but small difference)
- Sociocultural conservatives: higher lack of opinion recognition (0.61 vs 0.45)
- All differences statistically significant at p < 0.05

**Parameter registry**: Mean values for each group comparison in Fig. 3 (16 comparisons across 4 groups × 4 facets), significance of each t-test

### Claim 2: Each distinct feeling of lacking recognition is associated with populist attitudes
**Verbatim**: "each of the distinct feelings of lacking recognition are associated with populist attitudes"

**Location**: Figure 4 (p. 125), Table E1 in appendix
**Statistical method**: OLS regression (Models 1-4), weighted
**Key results to reproduce**:
- **Model 1** (4 facets separately): All four LoR facets significant (p < 0.05), R² = 0.26
  - LoR Economic: coefficient ~0.09 (from Fig 4)
  - LoR Work: coefficient ~0.03
  - LoR Services: coefficient ~0.03
  - LoR Opinion: coefficient ~0.17
- **Model 2** (composite index): LoR composite significant, R² = 0.26
  - LoR Composite: coefficient ~0.42
- **Model 3** (social groups only): R² = 0.18
  - Low-Income, Low-Skill, Socio-Cultural Conservative, Rural coefficients
- **Model 4** (combined): R² = 0.32
  - All four LoR facets + social group variables
- Controls: gender, age groups, east-west dummy, low education

**Parameter registry**: All coefficients from Models 1-4 in Fig. 4/Table E1, R² values, sample sizes

### Claim 3: Populism's relationship with recognition follows a logic of sufficient conditions with weak substitutability
**Verbatim**: (implicit in abstract — "the study offers a novel conceptualization of 'feeling left behind'")

**Location**: Comparison of R² values across Models 1 and 2 (Fig 4, p. 125), and comparison with mean index (R² = 0.24) and factor score (R² = 0.23) noted in text (p. 125)
**Statistical method**: Comparison of R² from OLS models
**Key results to reproduce**:
- Model 1 (4 facets separately): R² = 0.26
- Model 2 (composite score with sufficient conditions formula): R² = 0.26
- Simple mean index: R² = 0.24
- Factor score: R² = 0.23
- The sufficient condition composite matches the R² of individual facets (0.26 = 0.26)

**Parameter registry**: R² for Models 1 and 2, R² for mean index model, R² for factor score model

### Claim 4: Social group memberships mediate through recognition
**Verbatim**: (implicit) — comparing Models 3 and 4 shows recognition mediates group effects

**Location**: Figure 4 Models 3 and 4 (p. 125)
**Statistical method**: Comparison of OLS regression coefficients
**Key results to reproduce**:
- Model 3 R² = 0.18; Model 4 R² = 0.32
- Social group coefficients decrease from Model 3 to Model 4
- In Model 3: only conservatives, low-income, and rural significant (not low-skilled)
- In Model 4: only conservatives remain significant

**Parameter registry**: Social group coefficients in Models 3 and 4, R² values

## Correlation Matrix (Figure 2)
- Economic-Work correlation: 0.64
- Economic-Services: 0.43
- Economic-Opinion: 0.32
- Work-Services: 0.40
- Work-Opinion: 0.33
- Services-Opinion: 0.35
- Composite-Economic: 0.77
- Composite-Work: 0.79
- Composite-Services: 0.65
- Composite-Opinion: 0.64
- Populism-Economic: 0.36
- Populism-Work: 0.32
- Populism-Services: 0.31
- Populism-Opinion: 0.44
- Populism-Composite: 0.49

## Key Methodological Details

### Variables
- **Lacking recognition** (4 items): 5-point Likert, coded 0 to 1 (higher = more lacking recognition)
  - Economic needs, Work, Services, Opinion
- **Composite lack of recognition**: (f1² + f2² + f3² + f4²) / 4 — sufficient conditions aggregation
- **Populist attitudes**: Akkerman et al. (2014) scale, subdimensions multiplied (Wuttke et al. 2020), scored 0-1
- **Low income**: lowest quintile of equivalized household income
- **Low-skilled workers**: "unskilled and semiskilled worker" or "employee with simple duties"
- **Rural residents**: living in rural villages or single homesteads
- **Sociocultural conservatives**: top quintile of combined factor score from 5 sociocultural items (immigration, assimilation, European integration, gender equality, climate change)
- **Controls**: education (low), gender, age groups, east-west residence dummy
- **Weight**: poststratification weight from GLES

### Analytical Decisions to Note
- 175 observations excluded for missing poststratification weight
- Populist attitudes computed by multiplying subdimensions (not averaging)
- Composite recognition uses sum-of-squares formula (sufficient conditions)
- Conservative group defined by factor analysis of 5 items, then top quintile
- Variable operationalizations detailed in Table A1 (appendix — not yet available to read)

## Unusual/Questionable Choices
1. **Multiplication of populism subdimensions**: The paper multiplies populism subdimensions rather than averaging. While justified by Wuttke et al. (2020), this is unusual and creates a highly right-skewed distribution.
2. **Sum-of-squares aggregation**: The composite recognition index uses (f1² + f2² + f3²+ f4²)/4, which is non-standard. While theoretically motivated, it makes the composite harder to interpret.
3. **Conservative definition via factor score quintile**: Unlike the other three groups (defined by objective markers), sociocultural conservatives are defined by attitudes. The paper acknowledges this asymmetry in footnote 2.
