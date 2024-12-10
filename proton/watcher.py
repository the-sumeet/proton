import ast
import logging
import os
from typing import Callable, List
from multiprocessing import Process
from typing import Optional
from watchdog.events import (DirCreatedEvent, DirDeletedEvent,
                             DirModifiedEvent, FileCreatedEvent,
                             FileDeletedEvent, FileModifiedEvent,
                             FileSystemEventHandler)
from watchdog.observers import Observer

from proton.schema.method import Method

webview_process: Optional[Process] = None
logger = logging.getLogger(__name__)


def get_on_change(get_process: Callable, codegen: Callable) -> Callable:
    def on_change():
        codegen()
        global webview_process
        if webview_process:
            webview_process.terminate()
        webview_process = get_process()
        webview_process.start()

    return on_change


def get_first_class_methods(file_path) -> tuple[Optional[str], list[Method]]:
    with open(file_path, "r") as file:
        try:
            tree = ast.parse(file.read())
        except SyntaxError:
            return None, []

    # Find the first class in the AST
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            # Get all methods in the class
            methods = []
            for method in node.body:
                if isinstance(method, ast.FunctionDef):
                    args = [arg.arg for arg in method.args.args]
                    args = args[1:]  # Remove self
                    methods.append(Method(name=method.name, args=args))

            return class_name, methods

    return None, []


class PyFilesWatcher(FileSystemEventHandler):

    def __init__(self, on_change: Callable, excludes: Optional[List[str]] = None):
        super().__init__()
        self.on_change = on_change
        self.excludes = excludes or []

    def should_exclude(self, path: str) -> bool:
        return any(path.startswith(exclude) for exclude in self.excludes)

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent):
        if self.should_exclude(event.src_path):
            return

        self.on_change()
        if event.is_directory:
            return
        logger.info(f"File modified: {event.src_path}")

    def on_created(self, event: DirCreatedEvent | FileCreatedEvent):
        if self.should_exclude(event.src_path):
            return

        self.on_change()
        if event.is_directory:
            return
        logger.info(f"File created: {event.src_path}")

    def on_deleted(self, event: DirDeletedEvent | FileDeletedEvent):
        if self.should_exclude(event.src_path):
            return

        self.on_change()
        if event.is_directory:
            return
        logger.info(f"File deleted: {event.src_path}")


def start_watcher(path: str, on_change: Callable):
    handler = PyFilesWatcher(on_change, excludes=[os.path.join(path, "frontend")])
    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()
