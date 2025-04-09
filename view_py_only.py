import os

def print_py_files(path, prefix=''):
    for root, dirs, files in os.walk(path):
        level = root.replace(path, '').count(os.sep)
        indent = '│   ' * level + '├── '
        print(f"{indent}{os.path.basename(root)}/")
        subindent = '│   ' * (level + 1)
        for f in sorted(files):
            if f.endswith('.py'):
                print(f"{subindent}└── {f}")

print("📁 app/")
print_py_files("app")
