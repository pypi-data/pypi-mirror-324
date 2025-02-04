from pathlib import Path

# Define the exclusion list
EXCLUDED_FILES = {
    "*.env",
    "*.log",
    "*.tmp",
    "*.bak",
    "*.swp",
    "*.swo",
    "*.orig",
    "*.iml",
    "*.key",
    "*.pem",
    "*.crt",
    "*.p12",
    "*.py[cod]",
    "*.class",
    "*.exe",
    "*.dll",
    "*.so",
    "*.tgz",
    "*.gz",
    "*.DS_Store",
    "*.AppleDouble",
    "*.LSOverride",
    "npm-debug.log*",
    "*.pytest_cache",
    ".nyc_output",
    "go.sum",
    "*.h5",
    "*.pb",
    "*.ckpt",
}

EXCLUDED_FOLDERS = {
    "node_modules",
    "dist",
    "build",
    "out",
    "__pycache__",
    "logs",
    ".vscode",
    ".idea",
    ".git",
    ".next",
    ".parcel-cache",
    ".expo",
    ".firebase",
    ".docker",
    "test-results",
    "coverage",
    ".sass-cache",
    "debug",
    "tmp",
    ".trash",
    ".bundle",
    "target",
    "vendor",
    ".settings",
}


# Function to build a trie for folder exclusions
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, path: str):
        node = self.root
        for part in path.split("/"):
            if part not in node.children:
                node.children[part] = TrieNode()
            node = node.children[part]
        node.is_end = True

    def starts_with(self, path: str) -> bool:
        node = self.root
        for part in path.split("/"):
            if part not in node.children:
                return False
            node = node.children[part]
        return True


# Build the folder exclusion trie
folder_trie = Trie()
for folder in EXCLUDED_FOLDERS:
    folder_trie.insert(folder)


# Check if a file is among the excluded file list
def file_excluded(file, excluded_files: list):
    file_name = file.name
    file_suffix = file.suffix
    for pattern in excluded_files:
        if file_name and file_name.endswith(pattern.strip("*")):
            return True
        if file_suffix and file_suffix == pattern.strip("*"):
            return True


# Efficient file and folder filtering
def get_general_project_files(base_path: Path) -> list[str]:
    """
    Get a list of project files, excluding files and folders based on predefined rules.
    """
    all_files = []

    for file in base_path.rglob("*"):
        # Skip directories based on the folder trie
        if file.is_dir() and folder_trie.starts_with(str(file.relative_to(base_path))):
            continue

        # Skip files based on excluded patterns
        if file.is_file():
            if file_excluded(file, EXCLUDED_FILES):
                continue
            all_files.append(str(file.relative_to(base_path)))

    return all_files
