from ollama import chat

def load_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("This file doesn't exist")
    except OSError:
        print("An error occurred when trying to read the file")

def build_prompt(brief):
    # Let the AI help me modify the system_prompt & user_prompt.
    system_prompt = """
    You are a requirements assistant.
    Read the customer project brief and extract all software‑system requirements as plain human‑readable English text.
    Do NOT output JSON, do NOT use markdown tables or code blocks.
    Write out each requirement clearly in natural language.
    Only use information present in the brief, do not invent extra features.
    """

    user_prompt = f"""
    Customer brief text:
    \"\"\"{brief}\"\"\"
    Please extract all software requirements from the above brief.
    """
    return system_prompt, user_prompt

def ask_qwen(system_prompt, user_prompt):
    response = chat(
        model='qwen3:8b',
        messages=[
            {"role":"system", "content": system_prompt},
            {"role":"user", "content": user_prompt}
        ]
    )
    return response.message.content

def save_result(result, filename):
    with open(filename, 'w')as file:
        file.write(result)

def main():
    brief = load_file("brief.txt")

    system_prompt, user_prompt = build_prompt(brief)

    result = ask_qwen(system_prompt, user_prompt)

    save_result(result, "robot_requirements.txt")

    print("执行结束")


if __name__ == '__main__':
    main()
