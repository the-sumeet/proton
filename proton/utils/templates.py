import os
import shutil
from pathlib import Path
from string import Template

from proton.schema.init_config import InitConfig
from proton.utils.strings import rreplace

tmpl_file_ends_with = (
    ("tmpl.py", "py"),
    ("tmpl.html", "html"),
    ("tmpl.json", "json"),
)


def copy_template_dir(template_dir: str | Path, init_config: InitConfig):
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(init_config.name, os.path.relpath(src_file, template_dir))

            is_template = False
            for tmpl_ext in tmpl_file_ends_with:
                if dest_file.endswith(tmpl_ext[0]):
                    is_template = True
                    dest_file = rreplace(dest_file, tmpl_ext[0], tmpl_ext[1], 1)
                    break

            os.makedirs(os.path.dirname(dest_file), exist_ok=True)

            if is_template:
                with open(src_file, "r") as f:
                    content = Template(f.read())
                with open(dest_file, "w") as f:
                    f.write(content.substitute(init_config.dict()))
            else:
                shutil.copyfile(src_file, dest_file)
