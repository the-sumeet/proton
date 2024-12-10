import importlib
import importlib.util
import webview
from importlib.machinery import SourceFileLoader
from proton.runner.run import get_evaluate_js


def get_window(app_path: str, app_name: str, vite_server_url: str):
    module = SourceFileLoader(f"{app_name}.app", f"{app_path}/app.py").load_module()
    app = getattr(module, "app")
    window = webview.create_window("App", vite_server_url, js_api=app)
    webview.start(debug=True)
