import pprint
import sys
import os
import os.path
import json
import svgutils.transform as svt

# with open('sample.json') as f:
#     print(json.load(f))
idcArity = dict(zip("⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻", [2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2]))


def parseInputString(inputStr: str) -> list:
    """Parses an input string into tree of components.

    Args:
        inputStr (str): The input string, containing Unicode Ideographic Description Characters and other characters in between.

    Returns:
        tree: list: The tree of components, containing tuple[str, list].
            The str is a single Unicode Ideographic Description Character.
            The list contains tuple[str, list].
            This is recursive.
    """
    tree = []
    for c in inputStr[::-1]:
        if c in idcArity:
            t = (c, [tree.pop() for i in range(idcArity[c])])
            tree.append(t)
        else:
            tree.append(c)
    return tree[::-1]


def getJson(glyph: str) -> dict:
    """Gets the JSON dictionary of a glyph.

    Args:
        glyph (str): the glyph to find

    Returns:
        dict: the first JSON dictionary found of the glyph
    """
    global jsons
    return list(filter(lambda j: j['glyph'] == glyph, jsons))[0]


def getSvg(glyph: str) -> svt.SVGFigure:
    """Gets the SVG of a glyph.

    Args:
        glyph (str): the glyph to find

    Returns:
        svt.SVGFigure: the glyph's SVG
    """
    global inputDir
    return svt.fromfile(os.path.join(inputDir, glyph + '.svg'))


def composeGlyphs(sideLength: float, scale: float, idc: str, *glyphs) -> svt.SVGFigure:
    """Composes a Unicode Ideographic Description Character with glyphs.

    Args:
        sideLength (float): The side length (in pixels).
        scale (float): Multiply the side length by this value.
        idc (str): The Unicode Ideographic Description Character.
        *glyphs (tuple[str]): the glyphs to compose together according to `idc`.

    Returns:
        svt.SVGFigure: The SVG of the composed character.
    """

    if idcArity[idc] < len(glyphs):
        print(
            f"[NOTICE] more glyphs ({len(glyphs)}) than idc {idc} can take ({idcArity[idc]}), working with first {idcArity[idc]} glyphs")
        glyphs = glyphs[:idcArity[idc]]

    template = getJson(idc)
    glyphJsons = dict((g, getJson(g)) for g in glyphs)
    glyphSvgs = dict((g, getSvg(g)) for g in glyphs)
    glyphRoots = dict((g, glyphSvgs[g].getroot()) for g in glyphs)

    # pprint.pp(glyphJsons)
    # pprint.pp(glyphSvgs)
    # pprint.pp(glyphRoots)
    # pprint.pp(template)

    character = svt.SVGFigure()

    slots = template['slots']
    for t in zip(slots, glyphs):
        slot = t[0]
        glyph = t[1]
        glyphRoot = glyphRoots[glyph]
        # get the top left and bottom right corners of the slot
        tl = slots[slot][0]
        br = slots[slot][1]
        # calculate the tl corner of the slot
        slotx = 1 + sideLength * tl['x']
        sloty = 1 + sideLength * tl['y']

        # calculate the scaling for the glyph
        xScale = scale * (br['x'] - tl['x'])
        yScale = scale * (br['y'] - tl['y'])

        # apply the transformation of the current slot to the current glyph
        glyphRoot.moveto(slotx, sloty, scale_x=xScale, scale_y=yScale)

        # print(slot + " = " + glyph)
        # pprint.pp(template['slots'][slot])

    # apply additional offsets as defined in the glyphs
    for g in glyphJsons:
        if 'offsets' not in glyphJsons[g]:
            continue
        if template['name'] not in glyphJsons[g]['offsets']:
            continue
        # pprint.pp(glyphJsons[g])
        for i in range(len(glyphRoots)):
            if i != list(glyphJsons.keys()).index(g):
                # if `i` is not the current glyph,
                # apply the offset to `i` as defined in `g` by moving it
                offsetx = glyphJsons[g]['offsets'][template['name']][i]['x'] * sideLength * scale
                offsety = glyphJsons[g]['offsets'][template['name']][i]['y'] * sideLength * scale
                glyphRoots[list(glyphJsons.keys())[i]].moveto(slotx + offsetx, sloty + offsety)

    # place onto the character
    character.append(list(glyphRoots.values()))
    global outputDir
    # character.save(os.path.join(outputDir, idc + ''.join(glyphs) + ".svg"))
    return character


def composeMixed(sideLength: float, scale: float, idc: str, *glyphs) -> svt.SVGFigure:
    """Composes SVGs of characters or glyphs, or a mix of glyph strings and SVGs together based on an input Unicode Ideographic Description Character.

    Args:
        sideLength (float): The side length (in pixels).
        scale (float): Multiply the side length by this value.
        idc (str): The Unicode Ideographic Description Character.
        *glyphs:

    Returns:
        svt.SVGFigure: the completed character
    """
    if idcArity[idc] < len(glyphs):
        print(
            f"[NOTICE] more glyphs ({len(glyphs)}) than idc {idc} can take ({idcArity[idc]}), working with first {idcArity[idc]} glyphs")
        glyphs = glyphs[:idcArity[idc]]

    template = getJson(idc)
    character = svt.SVGFigure()
    glyphSvgs = list(glyphs)
    # get SVGs of all non-SVG glyphs
    glyphSvgs = [getSvg(g) if type(g) is str else g for g in glyphSvgs]
    glyphRoots = [g.getroot() for g in glyphs]

    slots = template['slots']
    for t in zip(slots, glyphs, glyphRoots):
        slot = t[0]
        glyph = t[1]
        glyphRoot = t[2]
        # get the top left and bottom right corners of the slot
        tl = slots[slot][0]
        br = slots[slot][1]
        # calculate the tl corner of the slot
        slotx = 1 + sideLength * tl['x']
        sloty = 1 + sideLength * tl['y']

        # calculate the scaling for the glyph
        xScale = scale * (br['x'] - tl['x'])
        yScale = scale * (br['y'] - tl['y'])

        # apply the transformation of the current slot to the current glyph
        glyphRoot.moveto(slotx, sloty, scale_x=xScale, scale_y=yScale)

        # print(slot + " = " + glyph)
        # pprint.pp(template['slots'][slot])

    # place onto the character
    character.append(glyphRoots)
    # global outputDir
    # import random
    # character.save(os.path.join(outputDir, str(int(random.random() * 100)) + ".svg"))
    return character


def compose(sideLength: float, scale: float, inputTree: list) -> svt.SVGFigure:
    """Recursively composes a character based on a given input tree.

    Args:
        sideLength (float): The side length (in pixels).
        scale (float): Multiply the side length by this value.
        inputTree (list): The input tree, as generated by `parseInputString()`.

    Returns:
        svt.SVGFigure: The final outputted character.
    """
    for tup in inputTree:
        # print('for:', tup)
        # base case: inputTree has only glyphs in its list
        possibleTuples = list(filter(lambda e: type(e) is tuple, tup[1]))
        print(len(possibleTuples))
        if len(possibleTuples) == 0:
            print('base')
            return composeGlyphs(sideLength, scale, tup[0], *tup[1])

        # recursive case: inputTree has tuples
        tup = list(tup)
        for i in range(len(tup[1])):
            if type(tup[1][i]) is tuple:
                # print('before:', tup[1][i])
                tup[1][i] = compose(sideLength, scale, [tup[1][i]])
                # print('after:', tup[1][i])
        return composeMixed(sideLength, scale, tup[0], *tup[1])


# if __name__ == '__main__':
#     if len(sys.argv) != 4:
#         print(f"Not enough arguments: expected 3 args, got {len(sys.argv)-1} args")
#         exit(1)
inputDir = sys.argv[1]
outputDir = sys.argv[2]
inputStr = sys.argv[3]
for root, dirs, files in os.walk(inputDir):
    jsons = []
    for f in files:
        if 'json' in f:
            fileName = os.path.join(inputDir, f)
            jsons.append(json.load(open(fileName)))

pp = pprint.PrettyPrinter()
# pp.pprint(glyphs)
# pp.pprint(jsons)
# pp.pprint(getJson('k'))
# pp.pprint(parseInputString(inputStr))

inputTree = parseInputString(inputStr)
# for t in inputTree:
#     pp.pprint(t)

compose(320, 8, inputTree).save(os.path.join(outputDir, inputStr + ".svg"))

exit(0)
