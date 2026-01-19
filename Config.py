
LLM_API_CREDENTIALS = {
    "openai": "OPENAI_API_KEY_PLACEHOLDER",
    "gemini": "GEMINI_API_KEY_PLACEHOLDER",
    "claude": "CLAUDE_API_KEY_PLACEHOLDER"
}

EXPERIMENT_SETTINGS = {
    # Controls randomness in model responses
    "sampling_temperature": 0.7,

    # Upper bound on generated tokens per response
    "response_token_limit": 1000,

    # Number of times each prompt is re-run to account for stochasticity
    "num_trials_per_prompt": 5,

    # LLMs included in the comparative bias analysis
    "model_registry": [
        "gpt-4",
        "gemini-pro",
        "claude-3-sonnet"
    ],

    # Cooldown period (seconds) between API calls to avoid rate limiting
    "request_pause_seconds": 2
}
