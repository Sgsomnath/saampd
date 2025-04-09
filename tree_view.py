import os

def print_tree(startpath, prefix=''):
    files = sorted(os.listdir(startpath))
    for idx, file in enumerate(files):
        path = os.path.join(startpath, file)
        is_last = idx == len(files) - 1
        connector = '└── ' if is_last else '├── '
        print(prefix + connector + file)
        if os.path.isdir(path):
            extension = '    ' if is_last else '│   '
            print_tree(path, prefix + extension)

print("📁 app/")
print_tree("app")
