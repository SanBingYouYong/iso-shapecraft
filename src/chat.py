import os
from openai import OpenAI
from dotenv import load_dotenv
import base64

load_dotenv()
client = OpenAI(api_key=os.getenv('GPT'))

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def llm_request(prompt: str, model: str="gpt-4o-mini") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    output = response.choices[0].message.content
    return output

def vlm_request(prompt: str, image_path, model: str="gpt-4o-mini", img_format: str="png") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/{img_format};base64,{encode_image(image_path)}"},
                    },
                ],
            }
        ],
    )
    return response.choices[0].message.content


# Example usage
if __name__ == "__main__":
    prompt = "Briefly describe this 3D model."
    img_path = "test.png"
    # response = llm_request(prompt)
    response = vlm_request(prompt, encode_image(img_path))
    print(f"Response: '{response}'")
    with open("output.txt", "w") as f:
        f.write(response)