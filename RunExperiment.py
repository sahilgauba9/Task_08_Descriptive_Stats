import json
import time
from pathlib import Path
from config import API_KEYS

# Import LLM SDKs
from openai import OpenAI
import google.generativeai as genai
from anthropic import Anthropic


class ExperimentRunner:
    """
    Runs bias detection experiments by querying multiple LLMs
    using predefined prompt variations and logging structured outputs.
    """

    def __init__(self, repetitions=5, delay=2):
        self.repetitions = repetitions
        self.delay = delay
        self.responses = []

        self._setup_clients()

    def _setup_clients(self):
        """Initialize API clients for all LLM providers."""
        # OpenAI GPT
        self.openai_client = OpenAI(api_key=API_KEYS['openai'])

        # Google Gemini
        genai.configure(api_key=API_KEYS['gemini'])
        self.gemini_model = genai.GenerativeModel("gemini-pro")

        # Anthropic Claude
        self.claude_client = Anthropic(api_key=API_KEYS['claude'])

    # -------------------------
    # Model query functions
    # -------------------------

    def query_openai(self, prompt, repetition):
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            return {
                "model": "chatgpt-4",
                "prompt": prompt,
                "response": response.choices[0].message.content,
                "repetition": repetition,
                "timestamp": time.time()
            }
        except Exception as e:
            return {"model": "chatgpt-4", "prompt": prompt, "error": str(e), "repetition": repetition, "timestamp": time.time()}

    def query_gemini(self, prompt, repetition):
        try:
            response = self.gemini_model.generate_content(prompt)
            return {
                "model": "gemini-pro",
                "prompt": prompt,
                "response": response.text,
                "repetition": repetition,
                "timestamp": time.time()
            }
        except Exception as e:
            return {"model": "gemini-pro", "prompt": prompt, "error": str(e), "repetition": repetition, "timestamp": time.time()}

    def query_claude(self, prompt, repetition):
        try:
            response = self.claude_client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return {
                "model": "claude-3-sonnet",
                "prompt": prompt,
                "response": response.content[0].text,
                "repetition": repetition,
                "timestamp": time.time()
            }
        except Exception as e:
            return {"model": "claude-3-sonnet", "prompt": prompt, "error": str(e), "repetition": repetition, "timestamp": time.time()}

    # -------------------------
    # Experiment runner
    # -------------------------

    def run_experiment(self):
        """Execute all prompts on all models and log responses."""
        # Ensure data directory exists
        Path("data").mkdir(exist_ok=True)

        # Load prompt templates
        with open("prompts/prompt_templates.json", "r") as f:
            prompts = json.load(f)

        # List of models
        model_functions = [
            self.query_openai,
            self.query_gemini,
            self.query_claude
        ]

        # Iterate over prompts and models
        for prompt_id, prompt_text in prompts.items():
            for model_func in model_functions:
                for rep in range(self.repetitions):
                    print(f"Running {prompt_id} | {model_func.__name__} | repetition {rep+1}/{self.repetitions}")

                    result = model_func(prompt_text, rep)
                    result["prompt_id"] = prompt_id
                    self.responses.append(result)

                    # Respect API rate limits
                    time.sleep(self.delay)

        # Save all responses
        with open("data/raw_responses.json", "w") as f:
            json.dump(self.responses, f, indent=2)

        print(f"✅ Completed experiment: {len(self.responses)} responses saved.")


if __name__ == "__main__":
    runner = ExperimentRunner()
    runner.run_experiment()
