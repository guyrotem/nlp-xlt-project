import openai
import json


class OpenAi:
    def __init__(self):
        api_key = read_api_key_from_config()
        openai.api_key = api_key

    def complete(self, prompt):
        chat = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0,
            max_tokens=500,
        )
        return chat.choices[0].text


def read_api_key_from_config():
    with open('data/config.json') as config_file:
        config_json = json.load(config_file)
        api_key = config_json['apiKey']
        if api_key == "<<your openAI key>>":
            raise Exception('Please configure you API key!')
        return api_key
