import pymel.core as pm
from maya import cmds


def get_time_ranges(anim_curve):
    """
    Build list of time ranges for the keys on this curve, plus the index of the key

    Args:
        anim_curve (pm.nt.AnimCurve):

    Returns: [
        (0, 30), 1,
        (30, 60), 2,
    ]

    """
    curve_keys = [int(anim_curve.getTime(i)) for i in range(anim_curve.numKeys())]
    if len(curve_keys) < 2:
        cmds.warning("At least 2 keys are needed for every control in the layer")
        return

    time_ranges = []
    for i, frame in enumerate(curve_keys):
        if i == 0:
            continue

        range_info = (
            (curve_keys[i - 1], frame), i  # key index of curve
        )
        time_ranges.append(range_info)

    return time_ranges


def adjustment_blend(layer_name="AnimLayer1", allow_ui=False):
    anim_layer = pm.PyNode(layer_name)

    affected_attrs = [
        a.attrName(longName=True, includeNode=True) for a in anim_layer.getAttributes()
        if a.type() != "bool"
    ]
    first_curve = anim_layer.getAnimCurves()[0]

    time_ranges = get_time_ranges(first_curve)
    if not time_ranges:
        return

    if len(time_ranges) >= 4 and allow_ui:
        confirm = cmds.confirmDialog(
            title='Adjustment Blend',
            message="{} key intervals found in {}.\nContinue? (might take a while)".format(
                len(time_ranges),
                anim_layer
            ),
            button=["Continue", "Cancel"],
            defaultButton="Cancel",
            cancelButton="Cancel",
            dismissString="Cancel",
            icon="warning",
        )
        if confirm == "Cancel":
            return

    curve_attr_map = get_curve_attr_map(anim_layer)

    # get start and end values for all the key intervals
    start_and_end_values = {}
    for time_range_info in time_ranges:
        key_index = time_range_info[1]
        start_and_end_values[key_index] = dict()
        for anim_curve in anim_layer.getAnimCurves():
            start_value, end_value = anim_curve.getValue(key_index - 1), anim_curve.getValue(key_index)
            start_and_end_values[key_index][anim_curve] = (start_value, end_value)

    for time_range_info in time_ranges:
        time_range = time_range_info[0]
        key_index = time_range_info[1]

        frames_to_modify = range(time_range[0] + 1, time_range[1])

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
            for frame in frames_to_modify:
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

        # create final attribute setting on curves
        for anim_curve in anim_layer.getAnimCurves():
            start_value, end_value = start_and_end_values.get(key_index).get(anim_curve)
            if start_value == end_value:
                continue

            affected_attr = curve_attr_map.get(anim_curve)

            if not percentage_values.get(affected_attr):
                continue

            pose_total_change = abs(end_value - start_value)

            frames = []
            values = []
            previous_value = start_value

            for frame in frames_to_modify:
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


def get_curve_attr_map(anim_layer):
    """
    Traverse hierarchy of anim curves to find the output attribute

    Returns: dict()

    """
    curve_attr_map = {}
    for anim_curve in anim_layer.getAnimCurves():

        anim_layer_node = anim_curve

        # please god don't have more than 50 animlayers in a hierarchy
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

    return curve_attr_map


def run_adjustment_blend(layer_name=None, allow_ui=False):
    """
    Run adjustment blend on selected anim layer

    Args:
        layer_name:

    Returns:

    """
    if layer_name is None:
        anim_layers = pm.ls(type="animLayer")
        anim_layers = [a for a in anim_layers if a.name() != "BaseAnimation"]
        if not anim_layers:
            cmds.warning("No AnimLayers found")
            return

        selected_anim_layers = [a for a in anim_layers if a.getSelected()]
        if selected_anim_layers:
            layer_name = selected_anim_layers[0]
        else:
            cmds.warning("No selected anim layers found, using first one: {}".format(anim_layers[0]))
            layer_name = anim_layers[0]

    with pm.UndoChunk():
        adjustment_blend(layer_name, allow_ui)


if __name__ == '__main__':
    import cProfile

    with pm.UndoChunk():
        cProfile.run("adjustment_blend()", sort="time")
