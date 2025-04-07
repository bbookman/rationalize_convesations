import openai
import toml

# Load API key from config.toml
config = toml.load("config.toml")
api_key = config["openai"]["api_key"]

# Test OpenAI connection
def test_openai():
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Summarize the importance of AI in productivity."}
        ],
        api_key=api_key
    )
    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    print("Testing OpenAI API...")
    print(test_openai())
