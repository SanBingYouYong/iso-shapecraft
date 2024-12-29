import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('GPT'))

def llm_request(prompt: str, model: str = "gpt-4o-mini") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    output = response.choices[0].message.content
    return output


# Example usage
if __name__ == "__main__":
    prompt = "What is the capital of France?"
    response = llm_request(prompt)
    print(f"Response: '{response}'")
    with open("output.txt", "w") as f:
        f.write(response)