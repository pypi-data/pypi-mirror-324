def get_provider_from_model(model_name):
    model_provider_map = {
        'gpt-4o-mini': 'openai',
        'mistral-model': 'mistral',
        'venice-model': 'venice',
        # Add other models and their providers here
    }
    return model_provider_map.get(model_name, 'openai')  # Default to 'openai' if not found
