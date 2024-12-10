from typing import Dict, List

from proton.runner.run import run
from pathlib import Path


class App:

    def __init__(self):
        # Current home dir
        self.current_dir = Path.home()

    def greet(self):
        return "Hello"

    def get_files(self) -> List[Dict]:
        return [
            {"name": f.name, "is_dir": f.is_dir(), "path": str(f)}
            for f in self.current_dir.iterdir()
        ]

    def set_dir(self, path: str):
        self.current_dir = Path(path)

    def go_back(self):
        self.current_dir = Path(self.current_dir).parent

    def get_file_content(self, path: str) -> str:
        return Path(path).read_text()


app = App()

if __name__ == "__main__":
    run(app)
