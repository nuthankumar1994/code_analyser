import networkx as nx
from dependency_graph import parse_project_for_calls, build_dependency_graph
from inline_comment import insert_inline_comment, find_file_by_module
import ast

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


def generate_impact_report(graph, change, project_root):
    changed_function = change['name']
    if changed_function not in graph.nodes:
        print(f"❌ Function {changed_function} not found in the graph.")
        return
    report = ""
    diff = ""
    affected = find_affected_functions(graph, changed_function)
    if change['diff'] != []:
        diff = "\n".join(change['diff'])
    else:
        diff = ""
    print(f"\n📝 Impact Report for Change in: {changed_function}")
    if not affected:
        report = f"""✅ No downstream functions are affected. .\n{diff}""" 
    else:
        report = f"""⚠️ Affected functions total {len(affected)} and they are {sorted(affected)}): .\n{diff}"""
    module, func_name = changed_function.split('.')
    file_path = find_file_by_module(project_root, module)
    if not file_path:
        print(f"⚠️ Could not find file for {changed_function}")
        return None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    tree = ast.parse(source)
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if changed_function.endswith(node.name):
                insert_inline_comment(file_path, node.lineno, report)