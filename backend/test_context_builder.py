from .context_builder import build_context_prompt


if __name__ == "__main__":

    query = "Which customers spent the most money?"

    prompt = build_context_prompt(query)

    print("\n")
    print("=" * 80)
    print("FINAL RETRIEVED CONTEXT")
    print("=" * 80)

    print(prompt)