import argparse
from .config import set_default_model, get_default_model, set_api_key
from .models import get_provider_from_model
from .providers import openai, mistral, venice

def main():
    parser = argparse.ArgumentParser(description="cmdai: AI Command-Line Tool")
    parser.add_argument('-q', '--query', type=str, help='Question to ask the AI')
    parser.add_argument('-m', '--model', type=str, help='Model to use for this query')
    parser.add_argument('-d', '--default-model', type=str, help='Set the default model')
    parser.add_argument('-s', '--set-key', nargs=2, metavar=('provider', 'api_key'),
                        help='Set an API key for a provider (e.g., openai, mistral, venice)')

    args = parser.parse_args()

    if args.set_key:
        provider, api_key = args.set_key
        set_api_key(provider, api_key)
        print(f"API key for {provider} set successfully.")
    elif args.default_model:
        set_default_model(args.default_model)
        print(f"Default model set to {args.default_model}")
    elif args.query:
        model = args.model if args.model else get_default_model()
        provider = get_provider_from_model(model)
        if provider == 'openai':
            answer = openai.get_response(args.query, model)
        elif provider == 'mistral':
            answer = mistral.get_response(args.query, model)
        elif provider == 'venice':
            answer = venice.get_response(args.query, model)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
        print(answer)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
