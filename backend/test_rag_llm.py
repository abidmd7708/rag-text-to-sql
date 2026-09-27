from .llm import generate_sql


questions = [
    "Which customers spent the most money?",
    "Show all customers from Hyderabad.",
    "What are the top 3 most expensive products?",
    "How many products are there in each category?",
    "Show all completed orders.",
]


if __name__ == "__main__":

    for question in questions:

        print("\n")
        print("=" * 80)
        print("QUESTION")
        print("=" * 80)

        print(question)

        print("\n")
        print("=" * 80)
        print("GENERATED SQL")
        print("=" * 80)

        try:
            sql = generate_sql(question)
            print(sql)

        except Exception as error:
            print("ERROR:", error)