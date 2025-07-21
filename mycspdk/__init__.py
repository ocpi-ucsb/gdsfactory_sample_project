__version__ = "0.0.0"

import pathlib

from cspdk.si220.cband import PDK

home = pathlib.Path.home()
cwd = pathlib.Path.cwd()
module_path = pathlib.Path(__file__).parent.absolute()
repo_path = module_path.parent


__all__ = ["PDK"]
