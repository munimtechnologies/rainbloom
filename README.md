# Rainbloom

A calm, endless puzzle about rain and flowers, in one HTML file. By MV2 of Munim, Inc., made with AI agents.
Apache-2.0.

Turn the channel tiles of a small garden so the rain from each cloud reaches every flower. Then the clouds
change colour. **Red rain and blue rain** fall on the same garden, each flower blooms only in its own colour,
and where the two rains meet the water turns **violet**. Most gardens are about keeping the rains apart, and
some are about bringing them together.

- **Endless gardens**, grown from a seed: the same number is always the same garden, and every one is
  solvable. Gardens get larger, then bring stones that never turn (garden 6), gaps that water cannot cross
  (garden 9), red and blue rain (garden 12) and violet flowers fed by both (garden 16).
- **Stars for few turns.** Par is the fewest clockwise turns that restore the garden; a hint caps a garden at
  two stars.
- **A daily garden**, the same for everyone on a date, with a streak that grows on consecutive days.
- **Five worlds** (Meadow, Orchard, Dunes, Snowfield, Lantern Night), ten gardens each, then round again.
- Saves progress in the browser. Lands straight in a garden. Works with a mouse, touch or keyboard, in
  landscape and portrait. Sound is synthesized and starts only after your first click; M or the Sound button
  turns it off.

## Controls

| | |
|---|---|
| Click / tap a tile | turn it clockwise |
| Right-click | turn it back |
| Arrow keys, then Space or Enter | move the cursor, turn (Shift+Space turns back) |
| H | hint (caps this garden at two stars) |
| R | restart the garden |
| M | sound on or off |

## How it works

`index.html` holds everything. The rules live in `<script id="logic">` with no browser code, so the tests run
them under Node. Each garden grows a random spanning forest, one depth-first tree per rain colour, on a grid
that may have gaps; clouds sit on each tree (the violet tree gets a red cloud and, at its far end, a blue one),
dead ends become flowers that want their tree's colour, and the tiles are then turned at random. Because
channels only run along tree links, the grown layout waters every tile and never lets two trees meet, so every
garden has a solution, and par counts the clockwise turns back to it.

Built from [html-jam-kit](https://github.com/munimtechnologies/html-jam-kit). The puzzle generator grew out
of [Rainworks](https://github.com/munimtechnologies/rainworks), MV2's hand-tracked WebXR puzzle.

## Test

```
python -m unittest -v test_rainbloom.py
```

Static checks always run. With Node.js installed the tests also run the rules' self-test (60 gardens and
8 daily gardens: one tree per colour, no channel off the board or into a gap, the grown layout solves in
exactly par turns, following the hints alone finishes in par, a flower in the wrong colour does not count),
and they run the whole page against a stub browser: a full play-through with mouse, keys, hints, the garden
picker, the daily garden and a portrait phone, plus the `#demo` and `#cover` pages. The canvas stub rejects
NaN and negative radii, so a drawing bug fails the test.

All 14 tests, including the Node ones, passed on Node 22 on 14 October 2026 (v0.1.0).

Open `index.html#selftest` for the same checks in a browser, `#cover` for the three store covers, and
`#demo` for a garden that plays itself (used for store videos; it never saves). `capture.py` runs all of that
in headless Chromium with Playwright and writes the covers, screenshots and two 20-second videos.

## Credits and licence

Made by MV2 of Munim, Inc. with AI agents (Anthropic Claude): the code, the drawing and the sounds are all
AI-made, with no third-party assets. Code under the Apache License 2.0.
