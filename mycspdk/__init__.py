import gdsfactory as gf
from gdsfactory.generic_tech import get_generic_pdk

import pathlib
from gdsfactory.config import module_path

home = pathlib.Path.home()
cwd = pathlib.Path.cwd()
module_path = pathlib.Path(__file__).parent.absolute()
LAYER_VIEWS = gf.technology.LayerViews(module_path / "layers.lyp")

PDK = get_generic_pdk()
PDK.layer_views = LAYER_VIEWS

__all__ = ["PDK"]
