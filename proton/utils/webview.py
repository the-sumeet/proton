import importlib

import webview

from proton.runner.run import get_evaluate_js


def get_window(app_name: str, vite_server_url: str, js_code: str):
    module = importlib.import_module(f'{app_name}.app')
    app = getattr(module, "app")
    window = webview.create_window("App", vite_server_url, js_api=app, )
    print(js_code)
    webview.start(get_evaluate_js(js_code=js_code), window, debug=True)
