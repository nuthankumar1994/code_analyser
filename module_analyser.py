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