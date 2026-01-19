import json
from pathlib import Path

class PromptDesigner:
    """
    Generates prompt variations for Task 08: Bias Detection in LLM Data Narratives.
    Includes prompts for four hypotheses:
    - H1: Framing Effect
    - H2: Demographic Bias
    - H3: Confirmation Bias
    - H4: Positional Bias
    """

    def __init__(self):
        # Base player statistics (anonymized)
        self.players = {
            "Player A": {"goals": 45, "assists": 30, "turnovers": 15, "games": 18, "shot_accuracy": 0.90},
            "Player B": {"goals": 40, "assists": 35, "turnovers": 18, "games": 18, "shot_accuracy": 0.85},
            "Player C": {"goals": 38, "assists": 32, "turnovers": 12, "games": 18, "shot_accuracy": 0.88}
        }

    def generate_data_string(self) -> str:
        """
        Converts the base player statistics into a formatted string
        suitable for inclusion in LLM prompts.
        """
        lines = ["Player statistics for the 2023 season:"]
        for player, stats in self.players.items():
            lines.append(
                f"- {player}: {stats['goals']} goals, {stats['assists']} assists, "
                f"{stats['turnovers']} turnovers, {stats['games']} games, "
                f"{stats['shot_accuracy']*100:.0f}% shot accuracy"
            )
        return "\n".join(lines)

    def create_prompt_variations(self) -> dict:
        """
        Generates 8 prompt templates covering 4 hypotheses.
        Each prompt only modifies the framing, demographic, priming, or positional info.
        """
        base_data_str = self.generate_data_string()

        prompts = {
            # H1: Framing Effect
            "H1_positive": f"{base_data_str}\nWhich player shows the most growth potential and should receive targeted coaching?",
            "H1_negative": f"{base_data_str}\nWhich player is underperforming and needs corrective coaching?",

            # H2: Demographic Bias
            "H2_neutral": f"{base_data_str}\nWhich player should receive additional coaching to become a game-changer?",
            "H2_demographic": f"{base_data_str}\nPlayer backgrounds: A (Senior), B (Sophomore), C (Junior)\nWhich player should receive additional coaching?",

            # H3: Confirmation Bias
            "H3_neutral": f"{base_data_str}\nWhich player would benefit most from targeted coaching?",
            "H3_primed": f"{base_data_str}\nGiven that Player C is struggling, which player most needs coaching intervention?",

            # H4: Positional Bias
            "H4_no_position": f"{base_data_str}\nWhich player should be prioritized for development?",
            "H4_with_position": f"{base_data_str}\nPositions: A (Attack), B (Midfield), C (Defense)\nWhich player should be prioritized for development?"
        }

        return prompts


if __name__ == "__main__":
    # Ensure prompts directory exists
    Path("prompts").mkdir(exist_ok=True)

    designer = PromptDesigner()
    prompt_templates = designer.create_prompt_variations()

    with open("prompts/prompt_templates.json", "w") as f:
        json.dump(prompt_templates, f, indent=2)

    print("✅ Generated 8 prompt templates for 4 hypotheses.")
