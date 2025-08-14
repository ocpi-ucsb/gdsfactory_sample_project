from typing import Literal


@gf.cell
def wg_xs(wg_width=0.9, **kwargs) -> gf.Component:
    wg_layer = (1, 0)
    wg_width = 0.9  # um
    wg_R_min = 100  # waveguide bend radius
    xs = gf.cross_section.cross_section(
        width=wg_width, radius=2 * wg_R_min, radius_min=wg_R_min, layer=wg_layer
    )
    return c
