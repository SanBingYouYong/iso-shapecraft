import os
from openai import OpenAI
from dotenv import load_dotenv
import base64

from typing import Tuple

load_dotenv()
client = OpenAI(api_key=os.getenv('GPT'))

MODEL = "gpt-4o-mini"

def deepseek(prompt: str):
    client = OpenAI(api_key=os.getenv('deepseek'), base_url="https://api.deepseek.com")

    response = client.chat.completions.create(
        model="deepseek-reasoner",  # r1, kinda slow, or deepseek-chat for v3
        messages=[
            {"role": "user", "content": prompt},
        ],
        stream=False
    )

    print(response.choices[0].message.content)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def llm_request(prompt: str, model: str=MODEL) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    output = response.choices[0].message.content
    return output

def llm_with_history(prompt: str, history: list, model: str=MODEL) -> Tuple[str, list]:
    response = client.chat.completions.create(
        model=model,
        messages=[
            *history,
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    history.append({"role": "user", "content": prompt})
    output = response.choices[0].message.content
    history.append({"role": "assistant", "content": output})
    return output, history

def vlm_request(prompt: str, image_path, model: str=MODEL, img_format: str="png") -> str:
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

def vlm_multi_img(prompt: str, image_paths: list, model: str=MODEL, img_format: str="png") -> str:
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
                    *[
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/{img_format};base64,{encode_image(image_path)}"},
                        }
                        for image_path in image_paths
                    ],
                ],
            }
        ],
    )
    return response.choices[0].message.content


# Example usage
if __name__ == "__main__":
    # prompt = "Briefly describe this 3D model."
    # img_path = "test.png"
    # # response = llm_request(prompt)
    # response = vlm_request(prompt, encode_image(img_path))
    # print(f"Response: '{response}'")
    # with open("output.txt", "w") as f:
    #     f.write(response)
    prompt = """# Shape Synthesis Instruction

**Objective:** Generate a code snippet in the target programming language to produce the 3D shape described. The generated code should:
1. Align with the shape description.
2. Be syntactically correct, functional, can be executed stand-alone or be called as a method. 
3. Focus on the current shape, ignore other unrelated descriptions.

**Output Format:** 
```openscad
your code here
```

# Shape Description
"""
    prompt += """A cylindrical coffee mug with a handle on the side."""
    print(prompt)
    # response, history = llm_with_history(prompt, [])
    response = deepseek(prompt)
    print(response)