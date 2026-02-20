# Claim-Result Mapping: Bimber et al. (2014)

**Paper**: Bimber, B., Cantijoch Cunill, M., Copeland, L., & Gibson, R. (2014). Digital Media and Political Participation: The Moderating Role of Political Interest Across Acts and Over Time. *Social Science Computer Review*, 1-22. DOI: 10.1177/0894439314526559

**Data**: British Election Studies (BES) cross-sectional surveys from 2001, 2005, and 2010.

## Data Sources

- **BES 2001**: Cross-sectional face-to-face survey (available as `bes_2001.por`)
- **BES 2005**: Cross-sectional face-to-face survey (available as `bes_2005_face-to-face.sav`)
- **BES 2010**: Cross-sectional survey (available as `bes_2010_survey_data.sav`)

## Claims from the Abstract

### Claim 1: Digital media use is positively and consistently associated with political talk for those lower in political interest
- **Verbatim**: "We find that digital media use is positively and consistently associated with political talk for those lower in political interest."
- **Location**: Table 5 (interaction models), discussed on p. 15-16
- **Key statistics**: Negative interaction terms (Internet info × Political interest) in all three years; Internet info main effect positive and significant in interaction models
- **Method**: OLS regression with interaction terms, all 3 years

### Claim 2: For voting, a similar relationship that appears to be strengthening over time
- **Verbatim**: "For voting, we find a similar relationship that appears to be strengthening over time."
- **Location**: Table 2 (interaction models), Figure 1, discussed on p. 11-14
- **Key statistics**: Interaction term not significant in any year; but predicted probabilities show digital media associated with voting more for low-interest citizens; main effect of Internet info grows from non-significant (2001) to significant (2005, 2010)
- **Method**: Logistic regression (odds ratios), predicted probabilities via Clarify

### Claim 3: For elite-directed acts (donating money and working for a party), highly variable moderating effect of political interest
- **Verbatim**: "For the elite-directed acts of donating money and working for a party, we find a highly variable moderating effect of political interest that can be positive, negative, or nonexistent."
- **Location**: Table 3 (donating, OLS), Table 4 (working for party, negative binomial), discussed on p. 13-15
- **Key statistics**:
  - Donating: Interaction negative & significant in 2001 (β = -0.460***), positive & significant in 2005 (β = 0.144*), non-significant in 2010 (β = 0.048)
  - Working for party: Interaction non-significant in 2001 & 2005, negative & significant in 2010 (β = -0.092*)
- **Method**: OLS regression (donating), negative binomial regression (working for party)

## Tables to Reproduce

### Table 1: Descriptive Statistics
- Means, SDs, Min, Max for all variables across all 3 years
- Sample sizes: 2001 ≈ 1463-1479, 2005 ≈ 3514-3595, 2010 ≈ 2308-2357

### Table 2: Logistic Regression - Voting (6 models: 3 main effect + 3 interaction)
- **Cell entries are odds ratios** with SEs in parentheses
- Model fit: LR χ²(9), Pseudo R²
- Data weighted to reflect general population parameters
- N: 2001=1,463; 2005=3,594; 2010=2,357

### Table 3: OLS Regression - Donating Money (6 models)
- Cell entries are coefficients with SEs
- Model fit: R², Adjusted R²
- N: 2001=1,478; 2005=3,514; 2010=2,308

### Table 4: Negative Binomial Regression - Working for a Party (6 models)
- Cell entries are coefficients with SEs
- Model fit: Nagelkerke R², α (dispersion), χ²
- N: 2001=1,462; 2005=3,595; 2010=2,354

### Table 5: OLS Regression - Discussing Politics (6 models)
- Cell entries are coefficients with SEs
- Model fit: R², Adjusted R²
- N: 2001=1,479; 2005=3,514; 2010=2,313

## Variable Specifications

| Variable | Description | Coding | Scale |
|----------|-------------|--------|-------|
| Education | Highest level completed | 1-5 Likert | 1-5 |
| Age | Age in years | Continuous | ~18-95 |
| Income | Annual household income | 1-15 scale | 1-15 |
| Male | Gender | 0=female, 1=male | Binary |
| Party contact | Contacted by party | 0=no, 1=yes | Binary |
| Political efficacy | Influence on politics | 0-10 scale | 0-10 |
| Political interest | Interest in politics | 0 (none) to 4 (a great deal) | 0-4 |
| Internet information | Internet use for election info | 0 (not at all) to 3 (a great deal) | 0-3 |
| Vote | Whether voted | 0=no, 1=yes | Binary |
| Work for party | Likelihood of working for party | 0-10 scale | 0-10 |
| Donate money | Likelihood of donating | 0-10 scale | 0-10 |
| Discuss politics | Likelihood of discussing politics | 0-10 scale | 0-10 |

**Notes**:
- In 2001, party contact question was "Were you telephoned by a Canvasser?" (footnote 2)
- Education is a 5-point Likert (1-5); Income is a 15-point scale (1-15) (footnote 1)
- Political interest: 5-point Likert 0=none at all to 4=a great deal
- Internet info: 4-point scale 0=not at all to 3=a great deal
- All analyses weighted per BES specifications

## Parameter Registry (Claim-Relevant Parameters)

### Claim 1 (Political talk & digital media for low-interest citizens)
- Table 5 Interaction models (2001, 2005, 2010):
  - Internet info coefficient
  - Political interest coefficient
  - Interaction (Internet info × Political interest) coefficient
  - R², Adjusted R², N

### Claim 2 (Voting relationship strengthening over time)
- Table 2 Main effect models (2001, 2005, 2010):
  - Internet info OR
- Table 2 Interaction models (2001, 2005, 2010):
  - Internet info OR
  - Interaction OR
  - N, Pseudo R²

### Claim 3 (Variable moderating effect for elite-directed acts)
- Table 3 Interaction models (2001, 2005, 2010):
  - Internet info coefficient
  - Interaction coefficient
  - N, R²
- Table 4 Interaction models (2001, 2005, 2010):
  - Internet info coefficient
  - Interaction coefficient
  - N, Nagelkerke R²

## Flags / Potentially Questionable Choices

1. **OLS for bounded ordinal outcomes**: The paper uses OLS for 0-10 likelihood scales (donating, discussing politics). While they note testing ordered logit and negative binomial and finding OLS "robust," these are clearly bounded ordinal variables. The choice of OLS over ordinal models is a pragmatic but debatable decision.

2. **Negative binomial for working for party**: The paper switches to negative binomial only for this one DV due to many zeros and non-normal residuals. This is reasonable but means the four DVs use three different estimation methods, complicating comparisons.

3. **No correction for multiple testing**: 24 regression models are estimated with no adjustment for multiple comparisons.

4. **Interaction interpretation in logistic models**: The paper reports odds ratios for all terms including the interaction in logistic models (Table 2). Interaction terms in logistic regression on the odds ratio scale can be misleading — the multiplicative interaction of odds ratios does not straightforwardly correspond to moderation on the probability scale. The predicted probability analysis (Figure 1) partially addresses this.

5. **Weight variable not specified**: The paper states "We weighted all analyses in accordance with BES specifications to reflect general population parameters" but does not specify which weight variable was used.
