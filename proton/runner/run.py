import time
from typing import Any

import webview


def get_evaluate_js(js_code: str = ""):
    #     js_code = ""
    #     for name, obj in inspect.getmembers(app):
    #         if inspect.isfunction(obj) or inspect.ismethod(obj):
    #             # Get the signature of the method
    #             signature = inspect.signature(obj)
    #             # Get the parameters (arguments) of the method
    #             params = [param for param in signature.parameters.values()]
    #
    #             js_code += f"""
    #             async function {name}() {{
    #     return await window.pywebview.api.greet();
    # }}
    # """

    def evaluate_js(window):
        #     js_code = """
        # async function greet() {
        #     return await window.pywebview.api.greet();
        # }
        # """
        window.evaluate_js(js_code)

    return evaluate_js


def run(window, app: Any):
    window.events.restored += get_evaluate_js(app)
    webview.start(get_evaluate_js(app), window, debug=True)
