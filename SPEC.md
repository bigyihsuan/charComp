# charComp specification

## Terminology in this Spec
* `glyph`: a single, indivisible input SVG.
* `template`: a character form that can take multiple glyphs in slots.
* `slot`: a rectangular box in a tamplate that contains a glyph.
* `character`: a finished, outputted SVG that contains glyphs placed in a template.

## SVGs

SVGs are expected to be square. If not, they will be rescaled to be square before processing.

## JSONs

* `name`: string. the name of the template.
* `glyph`: the unicode character representing this template.
* `slots`: a JSON object. Each field in this object must be a list of lists of floats. The field names are the names f the slots. The innermost list is a pair of coordinates; more details below.

## `slots` Coordinate System

Each number in the sublists of the fields in `slots` is a float between 0 and 1, inclusive.
The top left corner is `[0,0]` and the bottom corner `[1,1]`.
A pair of coordinates defines the top left and bottom right of the slot.

## Program Input/Output

```bash
python3 charComp.py svgDirectory inputString outputFile
```

Input is a directory `svgDirectory` to all SVGs with associated JSONs, and a string `inputString` containing Unicode "Ideographic Description Characters" and letters corresponding to glyphs.

Output is an SVG containing the character as specified by the input string, outputed to the file `outputFile`.