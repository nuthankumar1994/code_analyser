from changes_detector import detect_changed_definitions
from impact_report import parse_project_for_calls, generate_impact_report
from dependency_graph import build_dependency_graph

old_version = "demo1"
new_version = "demo2"

changed = detect_changed_definitions(old_version, new_version)

print("🔍 Changed definitions in project:")
for name in changed:
    print(f" - {name}")

defs, calls = parse_project_for_calls(old_version)
G = build_dependency_graph(defs, calls)

for change in changed:
    generate_impact_report(G, change, new_version)

