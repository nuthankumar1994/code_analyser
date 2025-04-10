import networkx as nx
from dependency_graph import parse_project_for_calls, build_dependency_graph
def find_affected_functions(graph, changed_function):
    # Perform reverse DFS to find all dependents
    affected = set()

    def dfs(node):
        for dependent in graph.predecessors(node):
            if dependent not in affected:
                affected.add(dependent)
                dfs(dependent)

    dfs(changed_function)
    return affected


def generate_impact_report(graph, changed_function):
    if changed_function not in graph.nodes:
        print(f"❌ Function {changed_function} not found in the graph.")
        return

    affected = find_affected_functions(graph, changed_function)

    print(f"\n📝 Impact Report for Change in: {changed_function}")
    if not affected:
        print("✅ No downstream functions are affected.")
    else:
        print(f"⚠️ Affected functions ({len(affected)}):")
        for func in sorted(affected):
            print(f" - {func}")


if __name__ == "__main__":
    project_dir = "demo1"
    defs, calls = parse_project_for_calls(project_dir)
    G = build_dependency_graph(defs, calls)

    # Function you're changing
    changed_func = "module_1.foo"
    generate_impact_report(G, changed_func)