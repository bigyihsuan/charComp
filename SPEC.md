# charComp specification

## Coordinates

Coordinates are JSON objects with labels `x: float` and `y: float`. The values are a fraction of the height and width of the image's size.
`(0,0)` is defined as the top left corner of the image. `(1,1)` is defined as the bottom right of the image. `(0.5,0.5)` is the center of the image, at half the height and half the width.

# Glyphs

* `name: str`
* `glyph: str`
* `offsets: obj` (optional)

Glyphs have a `name` and a `glyph` at minimum.

They can have an optional `offsets: obj` that contains custom offsets, defined in XY coordinates, for the other glyphs in a template.

For example, let's have a template `up-down` with `2` slots, and a glyph with these offsets:
```
"offsets": {
    "up-down": [
        { "x": -0.05, "y": 0.05 },
        { "x": 0.3, "y": -0.1 }
    ]
}
```
This will move the other glyph left 0.05 and down 1 if this glyph is in the second slot, and the other glyph 0.3 right and 0.1 up if the glyph is in the first slot. (Note that uses a similar coordinate system, scaled from 0 to +/-1.)

# Templates

* `name: str`
* `glyph: str`
* `slots: list`

## Slots

Slots are defined by a pair of XY coordinates, defining the top left and bottom right corners.