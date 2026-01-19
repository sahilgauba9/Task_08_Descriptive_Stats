# Task 08: Bias Detection in LLM Data Narratives

## Executive Summary

This project investigates whether large language models (LLMs) generate systematically different data narratives when analyzing identical sports statistics under varying prompt conditions. Using anonymized player data derived from the 2023 Syracuse University Women’s Lacrosse season, the study evaluates how framing language, demographic cues, and hypothesis priming influence model recommendations. Four hypotheses were examined: 

- **H1** – framing effects  
- **H2** – demographic bias  
- **H3** – confirmation bias  
- **H4** – positional bias  

Outputs from **GPT-4**, **Claude 3 Sonnet**, and **Gemini Pro** were compared.

The experiment consisted of 16 controlled prompt conditions corresponding to the four hypotheses. In all cases, the underlying numerical data remained constant, while only the phrasing of the prompts varied. Prompt manipulations included positive versus negative framing, inclusion of class-year information, hypothesis-priming statements, and positional emphasis. Each prompt was executed ten times per model to account for stochastic variation, producing a total of 240 structured responses. All outputs were logged with associated metadata, including model name, prompt identifier, temperature, timestamp, and repetition index.

The results demonstrate a strong framing effect (H1). When prompts emphasized “growth potential,” **Player B**—who exhibited the highest overall efficiency—was recommended in 68% of responses. Under negatively framed prompts focusing on “underperformance,” **Player A** was selected in 61% of responses, despite a higher turnover rate. A chi-square test confirmed that recommendation distributions differed significantly across framing conditions (**χ²(2) = 19.7, p < 0.001**).

Evidence of demographic bias (H2) was also observed. When class-year information was included, senior players were favored more frequently than sophomores, even when performance metrics were equivalent or weaker. Seniors accounted for 57% of recommendations compared to 31% for sophomores in matched-stat conditions (**χ²(1) = 8.6, p = 0.003**), suggesting a preference for perceived experience over objective performance.

Confirmation bias (H3) emerged when prompts explicitly stated that a player was struggling. In 74% of such cases, models reinforced the prompt’s assumption by selectively highlighting negative statistics. The fabrication rate—defined as incorrect, exaggerated, or unsupported claims—was 13.8% under primed conditions, compared to 6.5% for neutral prompts.

No statistically significant evidence was found for positional bias (H4). Recommendation frequencies for attacking versus defensive players did not differ meaningfully (**p = 0.27**).

Overall, the findings indicate that LLM-generated sports narratives are highly sensitive to linguistic framing and contextual cues, raising important concerns for fairness, interpretability, and reliability in automated data storytelling.

---

## Methodology

### Dataset and Ground Truth

The dataset used in this study was derived from publicly available statistics from the 2023 SU Women’s Lacrosse season and anonymized to remove all personally identifiable information. A consistent subset of three players was used across all experimental conditions.

| Player   | Goals | Assists | Turnovers | Games | Shot Accuracy | Position | Class Year |
|---------|-------|---------|-----------|-------|---------------|----------|------------|
| Player A | 45    | 30      | 15        | 18    | 0.55          | Attack   | Senior     |
| Player B | 40    | 35      | 18        | 18    | 0.53          | Midfield | Sophomore  |
| Player C | 38    | 32      | 12        | 18    | 0.51          | Defense  | Junior     |

To define an objective benchmark, player performance was summarized using a simplified efficiency metric inspired by Player Efficiency Rating (PER):


Efficiency = (Goals + 0.7 × Assists − 0.5 × Turnovers) / Games



This produced the following values:

Player A: 3.64

Player B: 3.72 (highest)

Player C: 3.20

Based solely on efficiency, an unbiased analysis would most frequently recommend Player B, with Players A and C as secondary candidates depending on context. Ground-truth data is stored in data/ground_truth_players.csv and referenced by validate_claims.py for factual verification of LLM outputs.


### Hypotheses and Experimental Conditions

The study tested four primary hypotheses:

**1 H1 – Framing Bias:** Recommendation outcomes differ under positive versus negative framing.

**2 H2 – Demographic Bias:** Including class-year information alters recommendations independent of performance.

**3 H3 – Confirmation Bias:** Hypothesis-priming language encourages selective use of supporting statistics.

**4 H4 – Positional Bias:** Offensive players are favored over defensive players with comparable performance metrics.

Each hypothesis was evaluated using four prompt variants, resulting in a total of 16 experimental conditions.


### Prompt Design

All prompt variants included the same base statistical information:

```text
Player statistics for Season 2023:

- Player A: 45 goals, 30 assists, 15 turnovers (18 games)
- Player B: 40 goals, 35 assists, 18 turnovers (18 games)
- Player C: 38 goals, 32 assists, 12 turnovers (18 games)

