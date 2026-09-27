import re


FORBIDDEN_KEYWORDS = [
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "GRANT",
    "REVOKE",
]


def clean_sql(sql):
    """
    Remove markdown code fences and extra whitespace.
    """

    sql = sql.strip()

    sql = re.sub(r"```sql", "", sql, flags=re.IGNORECASE)
    sql = re.sub(r"```", "", sql)

    return sql.strip()


def validate_sql(sql):

    sql = clean_sql(sql)

    if not sql:
        return False, "SQL query is empty."

    upper_sql = sql.upper()

    # Only allow SELECT queries
    if not upper_sql.startswith("SELECT"):
        return False, "Only SELECT queries are allowed."

    # Block multiple SQL statements
    statements = [statement.strip() for statement in sql.split(";") if statement.strip()]

    if len(statements) > 1:
        return False, "Multiple SQL statements are not allowed."

    # Block dangerous operations
    for keyword in FORBIDDEN_KEYWORDS:

        pattern = rf"\b{keyword}\b"

        if re.search(pattern, upper_sql):
            return False, f"Forbidden SQL keyword detected: {keyword}"

    return True, "SQL is valid."


if __name__ == "__main__":

    test_queries = [
        "SELECT name FROM customers LIMIT 5;",
        "DROP TABLE customers;",
        "DELETE FROM customers;",
        "SELECT name FROM customers; SELECT * FROM orders;",
    ]

    for query in test_queries:

        valid, message = validate_sql(query)

        print("\nSQL:", query)
        print("Valid:", valid)
        print("Message:", message)