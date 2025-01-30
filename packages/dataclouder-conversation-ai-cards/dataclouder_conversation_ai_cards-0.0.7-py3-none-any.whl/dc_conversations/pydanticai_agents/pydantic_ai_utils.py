from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel

import os


def get_model(provider: str, model: str = None):
    if provider == 'openai':
        if model is None:
            model = 'o1-mini'
        return f'openai:{model}'
    elif provider == 'anthropic':
        if model is None:
            model = 'claude-3-5-haiku-latest'
        return f'anthropic:{model}'
    elif provider == 'groq':
        if model is None:
            model = 'llama-3.1-8b-instant'
        return f'groq:{model}'
    elif provider == 'openrouter':
        # TODO: check if this is the correct way to do it
        if model is None:
            model = 'gryphe/mythomax-l2-13b:free'
        return OpenAIModel( model, base_url='https://openrouter.ai/api/v1', api_key=os.getenv('OPENROUTER_API_KEY'))
    else:
        raise ValueError(f'Provider {provider} not supported')
