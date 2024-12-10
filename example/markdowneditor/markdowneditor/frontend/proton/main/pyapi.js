window['py'] = {}; window['py']['main'] = {}; window['py']['main']['app'] = {};
            window['py']['main']['app']['__init__'] = async function __init__() {
                return await window.pywebview.api.__init__();
            }
            
            window['py']['main']['app']['greet'] = async function greet() {
                return await window.pywebview.api.greet();
            }
            
            window['py']['main']['app']['get_files'] = async function get_files() {
                return await window.pywebview.api.get_files();
            }
            
            window['py']['main']['app']['set_dir'] = async function set_dir(path) {
                return await window.pywebview.api.set_dir(path);
            }
            
            window['py']['main']['app']['go_back'] = async function go_back() {
                return await window.pywebview.api.go_back();
            }
            
            window['py']['main']['app']['get_file_content'] = async function get_file_content(path) {
                return await window.pywebview.api.get_file_content(path);
            }
            