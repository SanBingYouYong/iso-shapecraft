import os

PROMPTS_DIR = os.path.join(os.path.dirname(__file__), '../prompts')

def read_markdown_prompts(directory=PROMPTS_DIR):
    markdown_files = {}
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                markdown_files[os.path.splitext(filename)[0]] = file.read()
    return markdown_files

if __name__ == "__main__":
    markdown_files_dict = read_markdown_prompts(PROMPTS_DIR)
    print(markdown_files_dict["0_task_decomposition"])