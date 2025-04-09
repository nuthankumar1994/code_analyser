import ast
import os

class ModuleAnalyzer(ast.NodeVisitor):
    def __init__(self, filename):
        self.filename = filename
        self.classes = []
        self.functions = []
        self.calls = []

    def visit_FunctionDef(self, node):
        self.functions.append((node.name, node.lineno))
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.append((node.name, node.lineno))
        self.generic_visit(node)

    def visit_Call(self, node):
        # Collect function calls
        if isinstance(node.func, ast.Name):
            self.calls.append((node.func.id, node.lineno))
        elif isinstance(node.func, ast.Attribute):
            self.calls.append((f"{ast.unparse(node.func)}", node.lineno))
        self.generic_visit(node)


def analyze_python_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    tree = ast.parse(source, filename=file_path)
    analyzer = ModuleAnalyzer(file_path)
    analyzer.visit(tree)
    return {
        'file': file_path,
        'classes': analyzer.classes,
        'functions': analyzer.functions,
        'calls': analyzer.calls,
    }

def analyze_project(root_dir):
    project_info = []
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".py"):
                full_path = os.path.join(dirpath, file)
                info = analyze_python_file(full_path)
                project_info.append(info)
    return project_info


# Run on your project
# if __name__ == "__main__":
#     project_path = "demo1"
#     results = analyze_project(project_path)

#     for file_data in results:
#         print(f"\n📄 {file_data['file']}")
#         print("  🔹 Classes:", file_data['classes'])
#         print("  🔹 Functions:", file_data['functions'])
#         print("  🔹 Calls:", file_data['calls'])


import ast
import os
import networkx as nx
import matplotlib.pyplot as plt

class FunctionCallTracker(ast.NodeVisitor):
    def __init__(self, file_path):
        self.file_path = file_path
        self.module = os.path.splitext(os.path.basename(file_path))[0]
        self.definitions = []  # (func_name, line, full_name)
        self.calls = []        # (caller, callee, line)

        self.current_function = None

    def visit_FunctionDef(self, node):
        full_name = f"{self.module}.{node.name}"
        self.definitions.append((node.name, node.lineno, full_name))
        self.current_function = full_name
        self.generic_visit(node)
        self.current_function = None

    def visit_Call(self, node):
        if self.current_function:
            if isinstance(node.func, ast.Name):
                called = node.func.id
            elif isinstance(node.func, ast.Attribute):
                called = ast.unparse(node.func)
            else:
                called = "unknown"

            self.calls.append((self.current_function, called, node.lineno))
        self.generic_visit(node)


def parse_project_for_calls(project_path):
    all_defs = []
    all_calls = []

    for dirpath, _, filenames in os.walk(project_path):
        for file in filenames:
            if file.endswith(".py"):
                file_path = os.path.join(dirpath, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=file_path)
                    tracker = FunctionCallTracker(file_path)
                    tracker.visit(tree)
                    all_defs.extend(tracker.definitions)
                    all_calls.extend(tracker.calls)

    return all_defs, all_calls


def build_dependency_graph(definitions, calls):
    G = nx.DiGraph()

    defined_funcs = {name for _, _, name in definitions}
    
    for defn in defined_funcs:
        G.add_node(defn)

    for caller, callee, _ in calls:
        # Try to resolve callee to fully-qualified name
        matches = [f for f in defined_funcs if f.endswith(f".{callee}")]
        if matches:
            callee_full = matches[0]
            G.add_edge(caller, callee_full)

    return G


def visualize_graph(G):
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="skyblue", font_size=10, font_weight='bold')
    plt.title("Function Dependency Graph")
    plt.show()


if __name__ == "__main__":
    project_dir = "demo1"
    defs, calls = parse_project_for_calls(project_dir)
    G = build_dependency_graph(defs, calls)

    print("Dependencies:")
    for u, v in G.edges():
        print(f"{u} → {v}")

    visualize_graph(G)


import networkx as nx

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


import networkx as nx

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


import networkx as nx

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


# Example usage
if __name__ == "__main__":
    # Load or reuse your graph from the previous step
    # from your_previous_dependency_graph_script import parse_project_for_calls, build_dependency_graph

    project_dir = "path/to/your/project"
    defs, calls = parse_project_for_calls(project_dir)
    G = build_dependency_graph(defs, calls)

    # Function you're changing
    changed_func = "module1.foo"
    generate_impact_report(G, changed_func)

import os
import ast
import hashlib

def compute_code_hash(node):
    try:
        return hashlib.md5(ast.unparse(node).encode()).hexdigest()
    except Exception:
        return None

class DefinitionExtractor(ast.NodeVisitor):
    def __init__(self, module_name):
        self.module = module_name
        self.definitions = {}  # { full_name: hash }

    def visit_FunctionDef(self, node):
        full_name = f"{self.module}.{node.name}"
        self.definitions[full_name] = compute_code_hash(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        full_name = f"{self.module}.{node.name}"
        self.definitions[full_name] = compute_code_hash(node)
        self.generic_visit(node)

def get_py_files(root_dir):
    py_files = {}
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            if file.endswith(".py"):
                rel_path = os.path.relpath(os.path.join(dirpath, file), root_dir)
                py_files[rel_path] = os.path.join(dirpath, file)
    return py_files

def extract_definitions(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        source = f.read()
    module_name = os.path.splitext(os.path.basename(file_path))[0]
    tree = ast.parse(source, filename=file_path)
    extractor = DefinitionExtractor(module_name)
    extractor.visit(tree)
    return extractor.definitions

def detect_changed_definitions(dir1, dir2):
    files1 = get_py_files(dir1)
    files2 = get_py_files(dir2)

    changed_defs = []

    for rel_path in files2:
        path1 = files1.get(rel_path)
        path2 = files2[rel_path]

        defs1 = extract_definitions(path1) if path1 else {}
        defs2 = extract_definitions(path2)

        for name, hash2 in defs2.items():
            if name not in defs1:
                changed_defs.append(name)
            elif defs1[name] != hash2:
                changed_defs.append(name)

    return changed_defs


# Example usage
if __name__ == "__main__":
    old_version = "path/to/old_project"
    new_version = "path/to/new_project"

    changed = detect_changed_definitions(old_version, new_version)

    print("🔍 Changed definitions in project:")
    for name in changed:
        print(f" - {name}")
        
import os
import ast
import openai  # assumes you've set up your API key
import difflib

def insert_inline_comment(file_path, line_number, comment):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    if line_number <= len(lines):
        lines.insert(line_number, f"# GPT Insight: {comment}\n")
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        print(f"✅ Inserted comment in {file_path} at line {line_number}")
    else:
        print(f"⚠️ Could not insert comment, line {line_number} out of range in {file_path}")

def gpt_explain_change(changed_func, caller_func, line_number):
    prompt = (
        f"Function `{changed_func}` has been modified. "
        f"`{caller_func}` calls it at line {line_number}. "
        "What could be the potential impact of this change?"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You're a code review assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()


def analyze_and_comment(changed_func, graph, project_root):
    affected = get_affected_functions(graph, changed_func)

    for func in affected:
        # Example: func = module2.bar
        module, func_name = func.split('.')
        file_path = find_file_by_module(project_root, module)

        if not file_path:
            continue

        # Find the line where changed_func is called inside this file
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()
        tree = ast.parse(source)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                called = ast.unparse(node.func)
                if changed_func.endswith(called):
                    # Use GPT to explain
                    explanation = gpt_explain_change(changed_func, func, node.lineno)
                    insert_inline_comment(file_path, node.lineno, explanation)
                    break


def find_file_by_module(project_dir, module_name):
    for dirpath, _, filenames in os.walk(project_dir):
        for f in filenames:
            if f.endswith(".py") and f.startswith(module_name):
                return os.path.join(dirpath, f)
    return None