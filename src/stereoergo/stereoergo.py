import rv
import time


def set_stereo(stereotype, quiet=False):
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

    if not quiet:
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
    node = "#RVSourceStereo.stereo.rightOffset"
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

        self._is_running = False
        self._last_update = time.time()
        self.wiggle_fps = 5

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

        # "w" to enable wiggle, ; and ' to adjust speed
        rv.commands.bind("default", "stereo", "key-down--w", self.wiggle_toggle, "Toggle wiggle mode")
        rv.commands.bind("default", "stereo", "key-down--;", lambda evt: self.wiggle_nudge(offset=-1, evt=evt), "Wiggle increase FPS")
        rv.commands.bind("default", "stereo", "key-down--'", lambda evt: self.wiggle_nudge(offset=1, evt=evt), "Wiggle increase FPS")


    def wiggle_toggle(self, evt):
        self._is_running = not self._is_running

    def wiggle_nudge(self, evt, offset):
        self.wiggle_fps = self.wiggle_fps + offset
        self.wiggle_fps = max(1, self.wiggle_fps)
        self.wiggle_fps = min(60, self.wiggle_fps)

    def render(self, evt):
        """Timer-like thing for stereo-wiggle mode
        """

        if evt is not None:
            evt.reject()

        if not self._is_running:
            return

        # Check if enough time has elapsed
        now = time.time()
        since_last = (now - self._last_update)
        if since_last < (1.0/self.wiggle_fps):
            # Too soon, don't update yet
            return

        self._last_update = now
        def wiggle_step():
            if current_stereo_mode() == "right":
                set_stereo("left", quiet=True)
                eye_oneletter = "L"
            else:
                set_stereo("right", quiet=True)
                eye_oneletter = "R"

            # Maybe slightly annoying, but the message timeout/fade
            # ensures keeps the render method is continously called,
            # otherwise the wiggling will stop after a few seconds
            rv.extra_commands.displayFeedback(
                "Wiggle %s (%s fps, press 'w' to stop, ; and ' adjust speed)" % (eye_oneletter, self.wiggle_fps),
                1.0)

        wiggle_step()


def createMode():
    """Called by RV, returns an instance of the mode
    """

    return StereoErgo()
