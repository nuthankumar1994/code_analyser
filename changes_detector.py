import os
import ast
import hashlib
import difflib
from typing import List, Dict
def compute_code_hash(node):
    try:
        return hashlib.md5(ast.unparse(node).encode()).hexdigest()
    except Exception:
        return None

class DefinitionExtractor(ast.NodeVisitor):
    def __init__(self, module_name):
        self.module = module_name
        self.definitions = {}  # { full_name: hash }
        self.imports = []
        self.calls = []
        
    def visit_FunctionDef(self, node):
        full_name = f"{self.module}.{node.name}"
        self.definitions[full_name] = {}
        self.definitions[full_name]['hash'] = compute_code_hash(node)
        self.definitions[full_name]['type'] = 'function'
        self.definitions[full_name]['lineno'] = node.lineno
        self.definitions[full_name]['end_lineno'] = node.end_lineno
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        full_name = f"{self.module}.{node.name}"
        self.definitions[full_name] = {}
        self.definitions[full_name]['hash'] = compute_code_hash(node)
        self.definitions[full_name]['type'] = 'class'
        self.definitions[full_name]['lineno'] = node.lineno
        self.definitions[full_name]['end_lineno'] = node.end_lineno
        self.generic_visit(node)
    
    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
    
    def visit_ImportFrom(self, node):
        if node.module:
            self.imports.append(node.module)
    
    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.calls.append({
                "function": node.func.id,
                "lineno": node.lineno
            })
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
        
        with open(path1, "r", encoding="utf-8") as f:
            original_code = f.read()
        with open(path2, "r", encoding="utf-8") as f:
            modified_code = f.read()

        original_lines = original_code.splitlines()
        modified_lines = modified_code.splitlines()
        
        for name, hash2 in defs2.items():
            if name not in defs1:
                changed_defs.append(name)
            elif defs1[name]['hash'] != hash2['hash']:
                start = defs2[name]['lineno'] - 1
                end = defs2.get('end_lineno', start + 1)
                snippet_diff = difflib.unified_diff(
                    original_lines[start:end] if original_lines != None else [],
                    modified_lines[start:end] if modified_lines != None else [],
                    fromfile=path1,
                    tofile=path2,
                    lineterm=''
                ) 
                changed_defs.append({"name": name, "type": hash2['type'], "diff": list(snippet_diff)})

    return changed_defs


# Example usage
if __name__ == "__main__":
    old_version = "demo1"
    new_version = "demo2"

    changed = detect_changed_definitions(old_version, new_version)

    print("🔍 Changed definitions in project:")
    for name in changed:
        print(f" - {name}")