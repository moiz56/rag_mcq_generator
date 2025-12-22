import argparse

# File paths 
MATH_11_PATH = "markdown\MATH 11.md"
MATH_12_PATH = "markdown\MATH 12.md"
PHYSICS_11_PATH = "markdown\PHYSICS 11.md"
PHYSICS_12_PATH = "markdown\PHYSICS 12.md"


def read_file(file_path: str) -> str:
    """Reads a text/markdown file and returns its contents."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Error reading file {file_path}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read and display a text/markdown file.")
    parser.add_argument(
        "filepath",
        type=str,
        help="Path to the file to read (e.g., 'MATH 11.md')"
    )

    args = parser.parse_args()

    content = read_file(args.filepath)
    print(content[:200])  # Print first 200 characters
