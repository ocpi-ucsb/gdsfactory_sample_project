from gdsfactory.component import Component


from typing import Literal


from gdsfactory.component import Component


import gdsfactory as gf
from cspdk.si220.cband import cells

wg_layer = (1, 0)
wg_width = 0.9  # um
grating_layer = (130, 0)  # partial etch layer
wg_R_min = 100  # waveguide bend radius
xs = gf.cross_section.cross_section(
    width=wg_width, radius=2 * wg_R_min, radius_min=wg_R_min, layer=wg_layer
)


@gf.cell
def cooling_laser() -> gf.Component:
    c = gf.Component()
    ring_radius = 750
    gap = 0.9
    racetrack_len = 380  # um
    bend_spec: Component = gf.components.bend_euler(
        radius=ring_radius, angle=90, p=1, cross_section=xs, npoints=20000
    )
    cooling_ring = c << gf.components.ring_double(
        gap=gap,
        radius=ring_radius,
        length_x=racetrack_len,
        length_y=0,
        bend=bend_spec,
        straight="straight",
        coupler_ring="coupler_ring",
        cross_section=xs,
    )
    cooling_ring.drotate(90)
    return c


@gf.cell
def demo_2() -> gf.Component:
    c = gf.grid([cells.straight, cells.bend_s])
    return c


@gf.cell
def LEFT3GRT() -> gf.Component:
    path = ".gds"
    c = gf.import_gds(path)
    c.add_port(
        name="o1",
        center=(0, 0),
        orientation=180,
        layer=grating_layer,
    )
    return c


@gf.cell
def splitter_1x3(gap=0.9, coupler_length=750, in_out_wg_spacing=50) -> gf.Component:
    """1x3 directional coupler splitter"""
    c = gf.Component()
    straight_3 = c << gf.components.straight_array(
        n=3, spacing=gap, length=coupler_length, cross_section=xs
    )
    sbend_len_x = 1000
    sbend = gf.components.bend_s(
        size=(sbend_len_x, in_out_wg_spacing), npoints=10000, cross_section=xs
    )
    sb_input_top = c.add_ref(sbend).mirror_x()
    sb_input_bot = c.add_ref(sbend).mirror_x().mirror_y()
    sb_output_top = c.add_ref(sbend)
    sb_output_bot = c.add_ref(sbend).mirror_y()

    # straight waveguide
    straight_center_wg = gf.components.straight(length=sbend_len_x, cross_section=xs)
    straight_center_wg_input = c.add_ref(straight_center_wg)
    straight_center_wg_output = c.add_ref(straight_center_wg)

    # connect ports
    sb_input_top.connect("o1", straight_3.ports["o3"])
    sb_input_bot.connect("o1", straight_3.ports["o1"])
    sb_output_top.connect("o1", straight_3.ports["o4"])
    sb_output_bot.connect("o1", straight_3.ports["o6"])
    straight_center_wg_input.connect("o1", straight_3.ports["o2"])
    straight_center_wg_output.connect("o1", straight_3.ports["o5"])

    # add ports
    port_names = [
        "input_top",
        "input_center",
        "input_bottom",
        "output_top",
        "output_center",
        "output_bottom",
    ]
    ports = [
        sb_input_top.ports["o2"],
        straight_center_wg_input.ports["o2"],
        sb_input_bot.ports["o2"],
        sb_output_top.ports["o2"],
        straight_center_wg_output.ports["o2"],
        sb_output_bot.ports["o2"],
    ]
    for ind, port_name in enumerate(port_names):
        c.add_port(
            name=port_name,
            port=ports[ind],
            orientation=ports[ind].orientation,
            cross_section=xs,
        )

    c.add_label(
        text=f"3x3 coupler. gap {gap:.1f} um, length {coupler_length/1e3:.1f} mm",
        position=(0, 0),
        layer=wg_layer,
    )

    return c


@gf.cell
def splitter_coupler(gap=1.0, length=1000) -> gf.Component:
    c = gf.Component()
    c << gf.components.coupler(
        gap=gap, length=length, dy=101 + xs.width, dx=1000, cross_section=xs
    )
    return c


@gf.cell(check_instances=False)
def taper_angled(
    input_taper_width=4.0, angle=12, output_taper_width=0.9, check_instances=False
) -> gf.Component:
    angled_taper = gf.Component()
    input_straight_length = 100
    taper_cross_sec = gf.cross_section.cross_section(
        width=input_taper_width, layer=wg_layer
    )
    P_straight = gf.path.straight(length=input_straight_length).rotate(-angle)
    inp_straight = angled_taper << gf.path.extrude(
        p=P_straight, cross_section=taper_cross_sec
    )  # , shear_angle=angle)

    taper1 = angled_taper << gf.components.taper(
        length=500, width1=input_taper_width, width2=wg_width, layer=wg_layer
    )
    taper1.connect("o1", inp_straight.ports["o2"])

    bend = angled_taper << gf.components.bend_euler(
        radius=500, angle=angle, npoints=10000, cross_section=xs
    )
    bend.connect("o1", taper1.ports["o2"])

    strt = angled_taper << gf.components.straight(length=600, cross_section=xs)
    strt.connect("o1", bend.ports["o2"])

    # Create the straight section
    final_taper = angled_taper << gf.components.taper(
        length=1000, width1=wg_width, width2=output_taper_width, layer=wg_layer
    )
    final_taper.connect("o1", other=strt.ports["o2"])

    final_straight = angled_taper << gf.components.taper(
        length=500, width1=output_taper_width, width2=output_taper_width, layer=wg_layer
    )
    final_straight.connect("o1", other=final_taper.ports["o2"])

    text = angled_taper << gf.components.text(
        text=f"angle= {angle:.1f} deg, w = {input_taper_width:.2f} um", size=50
    )
    text.xmin = inp_straight.xmin + 500
    text.y = inp_straight.ymin + 50

    text = angled_taper << gf.components.text(
        text=f"w = {output_taper_width:.1f} um", size=50
    )
    text.xmax = final_straight.xmax - 200
    text.y = final_straight.ymax + 100
    return angled_taper
