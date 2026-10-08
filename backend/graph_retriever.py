from collections import deque

from .schema_graph import load_schema_graph


def table_from_node(node):
    """
    Convert:
        table:customers
        column:orders.customer_id

    into:
        customers
        orders
    """

    if node.startswith("table:"):
        return node.split(":", 1)[1]

    if node.startswith("column:"):
        column_path = node.split(":", 1)[1]
        return column_path.split(".", 1)[0]

    return None


def build_table_relationship_graph():
    """
    Convert the column-level schema graph into a
    table-level relationship graph.
    """

    schema_graph = load_schema_graph()

    table_graph = {}

    for node, edges in schema_graph.items():

        source_table = table_from_node(node)

        if not source_table:
            continue

        for edge in edges:

            target_table = table_from_node(edge["node"])

            if not target_table:
                continue

            if source_table == target_table:
                continue

            if source_table not in table_graph:
                table_graph[source_table] = set()

            table_graph[source_table].add(target_table)

    return table_graph


def expand_tables(initial_tables, max_hops=1):
    """
    Expand retrieved tables through the schema graph.

    Example:

        customers
             ↓
          orders
             ↓
        order_items
             ↓
          products

    max_hops=1:
        customers -> orders

    max_hops=2:
        customers -> orders -> order_items
    """

    graph = build_table_relationship_graph()

    visited = set(initial_tables)
    queue = deque()

    for table in initial_tables:
        queue.append((table, 0))

    while queue:

        current_table, depth = queue.popleft()

        if depth >= max_hops:
            continue

        for neighbor in graph.get(current_table, set()):

            if neighbor in visited:
                continue

            visited.add(neighbor)

            queue.append(
                (neighbor, depth + 1)
            )

    return sorted(visited)


def print_table_graph():

    graph = build_table_relationship_graph()

    print("\nTABLE RELATIONSHIP GRAPH")
    print("=" * 60)

    for table, neighbors in sorted(graph.items()):

        print(f"\n{table}")

        for neighbor in sorted(neighbors):

            print(f"  --> {neighbor}")


if __name__ == "__main__":

    print_table_graph()

    print("\nGRAPH EXPANSION TEST")
    print("=" * 60)

    tests = [
        ["customers"],
        ["orders"],
        ["products"],
        ["customers", "products"],
    ]

    for tables in tests:

        print(f"\nStarting tables: {tables}")

        expanded = expand_tables(
            tables,
            max_hops=2
        )

        print(f"Expanded tables: {expanded}")