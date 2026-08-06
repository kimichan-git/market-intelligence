import os

def create_structure():
    folders = [
        "data/raw",
        "data/processed",
        "src/fetchers",
        "src/processors",
        "src/analytics",
        "src/charts",
        "src/summaries",
        "app",
        "reports",
        "config",
        "notebooks",
        "tests"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        # Create an __init__.py for python packages
        if folder.startswith("src") or folder == "app":
            with open(os.path.join(folder, "__init__.py"), "w") as f:
                pass
        print(f"Created: {folder}")

    files = {
        "requirements.txt": "yfinance\nfredapi\npandas\nnumpy\nplotly\nstreamlit\npython-dotenv\npytest\n",
        "README.md": "# Market Intelligence Platform\n\nPersonal learning project for market data visualization.",
        ".gitignore": "data/\n.env\n__pycache__/\n*.pyc\n.streamlit/\n",
        "app/main.py": "import streamlit as st\n\nst.title('Market Intelligence Dashboard')\nst.write('Welcome to your personal market intelligence platform.')\n"
    }

    for path, content in files.items():
        with open(path, "w") as f:
            f.write(content)
        print(f"Created: {path}")

if __name__ == "__main__":
    create_structure()
    print("\nProject structure initialized successfully!")
