import rv


def set_stereo(stereotype):
    """Sets current stereo mode

    stereotype is string, valid options include:

    off
    anaglyph
    mirror
    pair
    hsqueezed
    vsqueezed
    checker
    scanline
    left
    right

    Based on setStereo in RV's rvui.mu
    """
    rv.commands.setStringProperty("#RVDisplayStereo.stereo.type", [stereotype], False)
    #rv.commands.setHardwareStereoMode(stereotype == "hardware" and stereoSupported())

    rv.extra_commands.displayFeedback("Stereo Mode: %s" % stereotype, 2.0)

    rv.commands.redraw()


def current_stereo_mode():
    """Returns active stereo mode, with same value as used in set_stereo
    """

    return rv.commands.getStringProperty("#RVDisplayStereo.stereo.type",
                                         0, # start
                                         1, # num
                                         )[0] # first item in list


def stereo_step(event, forward = False, backward = False):
    """Steps through both eyes, then changes to next frame
    """

    cur_view = current_stereo_mode()

    if forward:
        if cur_view == "left":
            set_stereo("right")
        elif cur_view == "right":
            set_stereo("left")
            rv.extra_commands.stepForward1()
        else:
            set_stereo("left")

    elif backward:
        if cur_view == "right":
            set_stereo("left")
        elif cur_view == "left":
            set_stereo("right")
            rv.extra_commands.stepBackward1()
        else:
            set_stereo("right")


def cycle_eye(event):
    """Toggles between eyes (switching to right eye from other stereo
    modes)
    """

    if current_stereo_mode() == "right":
        set_stereo("left")
    else:
        set_stereo("right")


def nudge_conv(event, left = False, right = False):
    """Adjusts the relative stereo offset by a small amount
    """

    node = "#RVDisplayStereo.stereo.relativeOffset"
    cur = rv.commands.getFloatProperty(node, 0, 1)[0]
    if left:
        cur += 0.0005
    else:
        cur -= 0.0005

    rv.commands.setFloatProperty(node, [cur], False)


def toggle_anaglyph_desat(event):
    """Sets anaglyph mode with saturation set to zero. Calling a
    second time disables stereo mode and restores saturation to 1
    """

    if current_stereo_mode() != "anaglyph":
        rv.commands.setFloatProperty("#RVColor.color.saturation", [0.0], False)
        set_stereo("anaglyph")
    else:
        # Could maybe store previous saturation value, and restore that instead?
        rv.commands.setFloatProperty("#RVColor.color.saturation", [1.0], False)
        set_stereo("none")


class StereoErgo(rv.rvtypes.MinorMode):
    def __init__(self):
        rv.rvtypes.MinorMode.__init__(self)
        self.init("stereoergo", [], None)

        # All shortcuts only apply in stereo-hotkey-mode (alt+s to toggle)

        # PgUp/PgDown to step through frame1 left, frame1 right, frame2 left, frame2 right etc
        rv.commands.bind("default", "stereo", "key-down--page-up",    lambda evt: stereo_step(backward=True, event = evt), "Step forward")
        rv.commands.bind("default", "stereo", "key-down--page-down",    lambda evt: stereo_step(forward=True, event = evt), "Step backwards")


        # Up (or down) to toggle between eyes
        rv.commands.bind("default", "stereo", "key-down--up", cycle_eye, "Cycle curent eye")
        rv.commands.bind("default", "stereo", "key-down--down", cycle_eye, "Cycle curent eye")

        # Shift+up to set scanline-interleave mode, shift+down to set anaglyph
        rv.commands.bind("default", "stereo", "key-down--shift--up", lambda evt: set_stereo("scanline"), "Scanline interlace")
        rv.commands.bind("default", "stereo", "key-down--shift--down", toggle_anaglyph_desat, "Anaglyph")


        # Shift+left/right to adjust convergence
        rv.commands.bind("default", "stereo", "key-down--shift--left", lambda evt: nudge_conv(event = evt, left=True), "Nudge convergence left")
        rv.commands.bind("default", "stereo", "key-down--shift--right", lambda evt: nudge_conv(event = evt, right=True), "Nudge convergence right")


def createMode():
    """Called by RV, returns an instance of the mode
    """

    return StereoErgo()
