from backend.llm_generator import generate_code

if __name__ == "__main__":
    brief = "Hello World webpage with a flower on top"
    files = generate_code(brief, push_to_github=True)

    for filename, content in files.items():
        print(f"--- {filename} ---")
        print(content)
        print("\n")
