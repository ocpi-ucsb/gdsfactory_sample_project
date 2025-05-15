import gdsfactory as gf


@gf.cell
def mzi3(delta_length=100.0) -> gf.Component:
    c = gf.Component()

    # components
    mmi_in = gf.get_component("mmi1x2")
    mmi_out = gf.get_component("mmi2x2")
    bend = gf.get_component("bend_euler")
    half_delay_straight = gf.get_component("straight", length=delta_length / 2)

    # references
    mmi_in_ref = c << mmi_in
    mmi_out_ref = c << mmi_out
    straight_top1_ref = c << half_delay_straight
    straight_top2_ref = c << half_delay_straight
    bend_top1_ref = c << bend
    bend_top2_ref = (c << bend).dmirror()
    bend_top3_ref = (c << bend).dmirror()
    bend_top4_ref = c << bend
    bend_btm1_ref = (c << bend).dmirror()
    bend_btm2_ref = c << bend
    bend_btm3_ref = c << bend
    bend_btm4_ref = (c << bend).dmirror()

    # connections

    # connections
    bend_top1_ref.connect("o1", mmi_in_ref.ports["o2"])
    straight_top1_ref.connect(
        "o1", bend_top1_ref.ports["o2"]
    )  # was straight_top2 but should be 1
    bend_top2_ref.connect("o1", straight_top1_ref.ports["o2"])
    bend_top3_ref.connect("o1", bend_top2_ref.ports["o2"])
    straight_top2_ref.connect("o1", bend_top3_ref.ports["o2"])
    bend_top4_ref.connect("o1", straight_top2_ref.ports["o2"])

    bend_btm1_ref.connect("o1", mmi_in_ref.ports["o3"])
    bend_btm2_ref.connect("o1", bend_btm1_ref.ports["o2"])
    bend_btm3_ref.connect("o1", bend_btm2_ref.ports["o2"])
    bend_btm4_ref.connect("o1", bend_btm3_ref.ports["o2"])

    mmi_out_ref.connect("o1", bend_btm4_ref.ports["o2"])

    # ports
    c.add_port(
        "o1",
        port=mmi_in_ref.ports["o1"],
    )
    c.add_port("o2", port=mmi_out_ref.ports["o3"])
    c.add_port("o3", port=mmi_out_ref.ports["o4"])
    return c


@gf.cell
def mzi4(delta_length=10.0) -> gf.Component:
    c = gf.Component()

    # components
    mmi_in = gf.get_component("mmi1x2")
    mmi_out = gf.get_component("mmi2x2")
    bend = gf.get_component("bend_euler")
    half_delay_straight = gf.get_component("straight", length=delta_length / 2)

    # references
    mmi_in_ref = c << mmi_in
    mmi_out_ref = c << mmi_out
    straight_top1_ref = c << half_delay_straight
    straight_top2_ref = c << half_delay_straight
    bend_top1_ref = c << bend
    bend_top2_ref = (c << bend).dmirror()
    bend_top3_ref = (c << bend).dmirror()
    bend_top4_ref = c << bend
    bend_btm1_ref = (c << bend).dmirror()
    bend_btm2_ref = c << bend
    bend_btm3_ref = c << bend
    bend_btm4_ref = (c << bend).dmirror()

    # connections

    # connections
    bend_top1_ref.connect("o1", mmi_in_ref.ports["o2"])
    straight_top1_ref.connect(
        "o1", bend_top1_ref.ports["o2"]
    )  # was straight_top2 but should be 1
    bend_top2_ref.connect("o1", straight_top1_ref.ports["o2"])
    bend_top3_ref.connect("o1", bend_top2_ref.ports["o2"])
    straight_top2_ref.connect("o1", bend_top3_ref.ports["o2"])
    bend_top4_ref.connect("o1", straight_top2_ref.ports["o2"])

    bend_btm1_ref.connect("o1", mmi_in_ref.ports["o3"])
    bend_btm2_ref.connect("o1", bend_btm1_ref.ports["o2"])
    bend_btm3_ref.connect("o1", bend_btm2_ref.ports["o2"])
    bend_btm4_ref.connect("o1", bend_btm3_ref.ports["o2"])

    mmi_out_ref.connect("o1", bend_btm4_ref.ports["o2"])

    # ports
    c.add_port(
        "o1",
        port=mmi_in_ref.ports["o1"],
    )
    c.add_port("o2", port=mmi_out_ref.ports["o3"])
    c.add_port("o3", port=mmi_out_ref.ports["o4"])
    return c
