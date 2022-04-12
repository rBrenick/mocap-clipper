import pymel.core as pm
from maya import cmds


def adjustment_blend(layer_name="AnimLayer1"):
    anim_layer = pm.PyNode(layer_name)

    affected_attrs = [
        a.attrName(longName=True, includeNode=True) for a in anim_layer.getAttributes()
        if a.type() != "bool"
    ]
    first_curve = anim_layer.getAnimCurves()[0]
    time_range = int(first_curve.getTime(0)), int(first_curve.getTime(1))

    # calculate some values
    anim_layer.setMute(True)

    percentage_values = {}
    for a in affected_attrs:

        # get base animation values
        base_anim_values = {}
        for frame in range(time_range[0], time_range[1]):
            base_anim_values[frame] = cmds.getAttr(a, time=frame)

        # get per-frame value changes
        change_values = {time_range[0]: 0.0}
        for frame in range(time_range[0] + 1, time_range[1]):
            frame_value = base_anim_values[frame]
            previous_value = base_anim_values[frame - 1]

            frame_change_value = abs(frame_value - previous_value)
            change_values[frame] = frame_change_value

        # get total value change for this attr in the time range
        total_base_change = sum(change_values.values())

        # value never changes, skip this attr
        if total_base_change == 0:
            continue

        # calculate value changes as percentages
        a_percentage_values = {}
        for frame, change_value in change_values.items():
            a_percentage_values[frame] = (100.0 / total_base_change) * change_value
        percentage_values[a] = a_percentage_values

    # re-enable animlayer
    anim_layer.setMute(False)

    # traverse hierarchy of animcurves to find the output attribute
    curve_attr_map = {}
    for anim_curve in anim_layer.getAnimCurves():

        anim_layer_node = anim_curve

        # please god don't have more than 50 animlayers
        for i in range(50):
            if anim_layer_node.type() == "animBlendNodeAdditiveRotation":
                connections = anim_layer_node.outputX.connections(plugs=True)
            else:
                connections = anim_layer_node.output.connections(plugs=True)

            crv_output = connections[0]

            # we found the final output
            if crv_output.node().type() == "transform":
                curve_attr_map[anim_curve] = crv_output.attrName(longName=True, includeNode=True)
                break

            anim_layer_node = crv_output.node()

    # create final attribute setting on curves
    for anim_curve in anim_layer.getAnimCurves():
        start_value, end_value = anim_curve.getValue(0), anim_curve.getValue(1)
        if start_value == end_value:
            continue

        affected_attr = curve_attr_map.get(anim_curve)

        if not percentage_values.get(affected_attr):
            continue

        pose_total_change = abs(end_value - start_value)

        frames = []
        values = []
        previous_value = start_value
        for frame in range(*time_range):
            frames.append(frame)
            percentage_value = percentage_values[affected_attr][frame]

            value_delta = (pose_total_change / 100.0) * percentage_value

            if end_value > start_value:
                new_key_value = previous_value + value_delta
            else:
                new_key_value = previous_value - value_delta

            values.append(new_key_value)
            previous_value = new_key_value

        anim_curve.addKeys(frames, values)


if __name__ == '__main__':
    import cProfile

    with pm.UndoChunk():
        cProfile.run("adjustment_blend()", sort="time")
