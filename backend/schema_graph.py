from collections import defaultdict
from .database import get_connection


def load_schema_graph():
    """
    Build a graph of the PostgreSQL database schema.

    Nodes:
        table:<table_name>
        column:<table_name>.<column_name>

    Edges:
        table -> column
        foreign-key column -> referenced column
    """

    graph = defaultdict(list)

    with get_connection() as conn:
        with conn.cursor() as cur:

            # Get all columns
            cur.execute("""
                SELECT
                    table_name,
                    column_name,
                    data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
                ORDER BY table_name, ordinal_position;
            """)

            columns = cur.fetchall()

            for table_name, column_name, data_type in columns:
                table_node = f"table:{table_name}"
                column_node = f"column:{table_name}.{column_name}"

                graph[table_node].append({
                    "node": column_node,
                    "relationship": "HAS_COLUMN"
                })

                graph[column_node].append({
                    "node": table_node,
                    "relationship": "BELONGS_TO"
                })

            # Get foreign-key relationships
            cur.execute("""
                SELECT
                    tc.table_name AS source_table,
                    kcu.column_name AS source_column,
                    ccu.table_name AS target_table,
                    ccu.column_name AS target_column
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                    ON tc.constraint_name = ccu.constraint_name
                    AND tc.table_schema = ccu.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                  AND tc.table_schema = 'public';
            """)

            foreign_keys = cur.fetchall()

            for (
                source_table,
                source_column,
                target_table,
                target_column
            ) in foreign_keys:

                source_node = (
                    f"column:{source_table}.{source_column}"
                )

                target_node = (
                    f"column:{target_table}.{target_column}"
                )

                graph[source_node].append({
                    "node": target_node,
                    "relationship": "REFERENCES"
                })

                graph[target_node].append({
                    "node": source_node,
                    "relationship": "REFERENCED_BY"
                })

    return graph


def print_schema_graph():
    graph = load_schema_graph()

    print("\nDATABASE SCHEMA GRAPH")
    print("=" * 60)

    for node, edges in graph.items():
        print(f"\n{node}")

        for edge in edges:
            print(
                f"  --[{edge['relationship']}]--> "
                f"{edge['node']}"
            )


if __name__ == "__main__":
    print_schema_graph()