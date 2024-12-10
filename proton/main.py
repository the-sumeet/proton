import logging
import os
import subprocess
from multiprocessing import Process
from pathlib import Path

import typer

from proton.constants import MAIN_FILE_NAME
from proton.schema.fe_type import FeType
from proton.schema.init_config import InitConfig
from proton.utils.code_generator import get_js_code, get_js_bindings
from proton.utils.config import load_app_config
from proton.utils.templates import copy_template_dir
from proton.utils.webview import get_window
from proton.watcher import start_watcher, get_on_change

logging.basicConfig(level=logging.DEBUG)

app = typer.Typer(no_args_is_help=True)
logger = logging.getLogger(__name__)


@app.command()
def init(
        type: FeType = typer.Argument(help="Type of the front-end framework"),
        name: str = typer.Argument(help="Name of the project", case_sensitive=False),
):
    init_config = InitConfig(name=name, fe_type=type)

    logger.info(f"Creating project '{name}' of type '{type.name}'")
    if type == FeType.vanilla:
        copy_template_dir(Path(__file__).parent / "templates/$vanilla", init_config)
    elif type == FeType.svelte:
        copy_template_dir(Path(__file__).parent / "templates/$svelte", init_config)


@app.command()
def dev():
    current_dir = os.getcwd()
    app_name = current_dir.split("/")[-1]
    frontend_dir = os.path.join(current_dir,  f"{app_name}/frontend")
    app_dir = os.path.join(current_dir, app_name)
    config = load_app_config(current_dir)

    # Install FE dependencies.

    logger.info(f"Installing front-end dependencies in {frontend_dir}")
    process = subprocess.Popen(
        config.fe_install.split(" "),
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if process.returncode and process.returncode > 0:
        logger.error("Error installing dependencies")
        for line in process.stderr:
            logger.error(line.strip())
        return
    else:
        logger.info("Dependencies installed successfully")
        for line in process.stdout:
            logger.info(line.strip())

    # Start FE server, keep reading the stdout
    process = subprocess.Popen(
        config.fe_dev_watcher.split(" "),
        cwd=frontend_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    vite_server_url = ""
    if process.returncode and process.returncode > 0:
        logger.error("Error installing dependencies")
        for line in process.stderr:
            logger.error(line.strip())
        return
    else:
        logger.info("Dependencies installed successfully")
        for line in process.stdout:
            if "Local:" in line:

                index = line.index("Local:")
                if index == -1 or len(line) < 7:
                    continue
                vite_server_url = line[index + 6:].strip()
                logger.info(f"Vite Server URL: {vite_server_url}")
                break

    # Start watching python files
    def codegen():
        js_pywebview_api = get_js_code(app_dir, MAIN_FILE_NAME)
        os.makedirs(os.path.join(frontend_dir, "proton/main"), exist_ok=True)
        with open(os.path.join(frontend_dir, "proton/main/pyapi.js"), "w") as file:
            file.write(js_pywebview_api)

        js_bindings = get_js_bindings(app_dir, MAIN_FILE_NAME)
        os.makedirs(os.path.join(frontend_dir, "proton/main"), exist_ok=True)
        with open(os.path.join(frontend_dir, "proton/main/App.js"), "w") as file:
            file.write(js_bindings)

    def get_process():
        return Process(
            target=get_window,
            args=(
                app_dir,
                app_name,
                vite_server_url,
            )
        )
    get_on_change(get_process, codegen)()
    start_watcher(app_dir, get_on_change(get_process, codegen))
    logger.info("Watching for changes in Python files...")

    while True:
        pass



if __name__ == "__main__":
    app()
