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
    
    def visit_ClassDef(self, node):
        full_name = f"{self.module}.{node.name}"
        self.definitions.append((node.name, node.lineno, full_name))
        self.current_function = full_name
        self.generic_visit(node)

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

    # visualize_graph(G)