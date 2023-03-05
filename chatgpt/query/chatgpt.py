import openai


def main(
        api_key: str,
        query: str,
):
    # Set up the OpenAI API client
    if api_key is None:
        try:
            with open("api.key", "rt") as f:
                api_key = f.read()
                api_key = api_key.strip().replace("\n", "")
        except FileNotFoundError:
            raise FileNotFoundError("""
            Please create a file named api.key with your OpenAI API key in it.
            or pass the key as an argument(-k|--api-key)
            """)

    openai.api_key = api_key

    model: dict
    gtp3_model = {
        "name": "text-davinci-003",
        "max_token": 4_000,
    }
    # codex_model = {
    #     "name": "code-davinci-002",
    #     "max_token": 8_000,
    # }

    model = gtp3_model

    # https://platform.openai.com/docs/api-reference/completions/create
    completion = openai.Completion.create(
        # https://platform.openai.com/docs/models
        engine=model["name"],
        max_tokens=model["max_token"],
        prompt=query,
        n=1,
        stop=None,
        # https://towardsdatascience.com/how-to-sample-from-language-models-682bceb97277
        temperature=0.1,  # 0.0 to 1.0: 0.0 is the least creative. 1.0 is the most creative.
    )

    response = completion.choices[0].text
    print(response)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="""
    Query to ChatGPT
    """)
    parser.add_argument('-k', '--api-key', metavar='<str>', required=False,
                        default=None, type=str,
                        help='OpenAI API Key')
    parser.add_argument('-q', '--query', metavar='<str>', required=False,
                        default="What is the population of the world?", type=str,
                        help='Query')

    args = parser.parse_args()
    main(
        api_key=args.api_key,
        query=args.query,
    )
