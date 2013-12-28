More ergonomics stereo-review shortcuts for [Tweak Software's
RV](http://www.tweaksoftware.com/)

It is written using the RV Python bindings, so requires RV 3.12.13

# What does it do?

Prevents RSI.

Err, more helpfully.. In stereo hotkeys mode (Alt+s to enable):

- Shift+left/right adjusts convergence
- Shift+up toggles scanline-interleave mode
- Shift+down toggles anaglyph mode (and greyscale)
- Up-arrow cycles between eyes (same with down arrow)
- Page-up and Page-down step through frames then eyes (frame1-left, frame1-right, frame2-left, frame2-right etc)

# Installing

Either [download the rvpkg][rvpkg], or run "make" to generate it from source.

Then in RV's preference, under the "Packages" tab, click "Add
Packages", and load the rvpkg file.

In the package listing, check "Installed" and "Load" for "Stereo
Ergonomics mode", and restart RV.

# Change log

* `v1.0` ([download](https://github.com/downloads/dbr/stereoergo-rv/stereoergo-1.0.rvpkg))
 * Initial release
* `v2.0` ([download](https://github.com/downloads/dbr/stereoergo-rv/stereoergo-2.0.rvpkg))
 * Stereo Wiggle" mode, automatically flicks between eyes at a set
   rate, very useful for spotting stereo-depth errors in long
   sequences
 * Offset nudging (shift+left/right) alter the "right offset" instead
   of "relative offset", same as the default "alt+s o" shortcut.


 [rvpkg]: https://github.com/downloads/dbr/stereoergo-rv/stereoergo-2.0.rvpkg
