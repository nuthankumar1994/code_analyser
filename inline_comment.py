
        
import os
import ast
import astunparse

def find_file_by_module(project_dir, module_name):
    for dirpath, _, filenames in os.walk(project_dir):
        for f in filenames:
            if f.endswith(".py") and f.startswith(module_name):
                return os.path.join(dirpath, f)
    return None
class DocstringWriter(ast.NodeTransformer):
    def __init__(self, target_line, comment):
        self.target_line = target_line
        self.comment = comment

    def visit_FunctionDef(self, node):
        if node.lineno == self.target_line:
            docstring = ast.get_docstring(node)
            new_docstring_node = make_docstring_node(docstring, self.comment)
            if docstring:
                node.body[0] = new_docstring_node
            else:
                node.body.insert(0, new_docstring_node)
        return node
    
    def visit_ClassDef(self, node):
        if node.lineno == self.target_line:
            docstring = ast.get_docstring(node)
            new_docstring_node = make_docstring_node(docstring, self.comment)
            if docstring:
                node.body[0] = new_docstring_node
            else:
                node.body.insert(0, new_docstring_node)
        return node


def make_docstring_node(docstring, comment):
    if docstring is None:
        content = f"""Insight: {comment}""" 
    else:
        content = docstring + f"""{comment}"""
    s = ast.Constant(content)
    return ast.Expr(value=s)


def insert_inline_comment(file_path, line_number, comment):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)
    transformer = DocstringWriter(line_number, comment)
    modified_tree = transformer.visit(tree)
    ast.fix_missing_locations(modified_tree)

    new_source = astunparse.unparse(modified_tree)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_source)

    print(f"✅ Inserted docstring comment in {file_path} at function starting on line {line_number}")