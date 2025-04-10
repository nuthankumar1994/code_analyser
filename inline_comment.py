
        
import os
import ast
import openai  # assumes you've set up your API key
import difflib
from impact_report import find_affected_functions

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
    affected = find_affected_functions(graph, changed_func)

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