import webbrowser
import shutil
from pathlib import Path

def author():
    linkedin_url = "https://www.linkedin.com/in/engrshishir/"
    webbrowser.open_new_tab(linkedin_url)


def delete_path():
    """Deletes a specified file or folder."""
    path = Path(input("🗑️ Enter path to delete: ").strip())

    if not path.exists():
        print(f"⚠️ Path '{path}' does not exist.")
        return

    try:
        if path.is_dir():
            shutil.rmtree(path)
            print(f"✅ Folder '{path}' and its contents deleted.")
        else:
            path.unlink()
            print(f"✅ File '{path}' deleted.")
    except Exception as e:
        print(f"❌ Error deleting '{path}': {e}")
