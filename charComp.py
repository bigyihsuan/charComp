import pprint
import sys
import os
import json
import svgutils.transform as svt

# with open('sample.json') as f:
#     print(json.load(f))


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

    idc = dict(zip("⿰⿱⿲⿳⿴⿵⿶⿷⿸⿹⿺⿻", [2, 2, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2]))
    tree = []
    for c in inputStr[::-1]:
        if c in idc:
            t = (c, [tree.pop() for i in range(idc[c])])
            tree.append(t)
        else:
            tree.append(c)
    return tree


def compose(svgDirectory: str, inputString: str, outputFile: str):
    return


# if __name__ == '__main__':
#     if len(sys.argv) != 4:
#         print(f"Not enough arguments: expected 3 args, got {len(sys.argv)-1} args")
#         exit(1)
inputDir = sys.argv[1]
outputDir = sys.argv[2]
inputStr = sys.argv[3]
for root, dirs, files in os.walk(inputDir):
    jsons = [json.load(open(inputDir + f)) for f in files if 'json' in f]

pp = pprint.PrettyPrinter()
# pp.pprint(glyphs)
pp.pprint(jsons)

pp.pprint(parseInputString(inputStr))

exit(0)

character = svt.SVGFigure()

template = list(filter(lambda j: j['glyph'] == '⿱', jsons))[0]
left = svt.fromfile(inputDir + inputStr[1] + '.svg')
right = svt.fromfile(inputDir + inputStr[2] + '.svg')

leftLeftTop = template['slots']['up']['tl']
leftRightBottom = template['slots']['up']['br']

rightLeftTop = template['slots']['down']['tl']
rightRightBottom = template['slots']['down']['br']

leftRoot = left.getroot()
rightRoot = right.getroot()

width = 320
height = 320
scale = 8 * width / height

# lx = width * leftLeftTop[0]
lx = 1 * scale
ly = height * leftLeftTop['y']

rx = width * rightLeftTop['x'] + lx
ry = height * rightLeftTop['y']

print(lx, ly, rx, ry)

leftxscale = (leftRightBottom['x'] - leftLeftTop['x']) * scale
leftyscale = (leftRightBottom['y'] - leftLeftTop['y']) * scale

rightxscale = (rightRightBottom['x'] - rightLeftTop['x']) * scale
rightyscale = (rightRightBottom['y'] - rightLeftTop['y']) * scale

# leftRoot.moveto(lx, ly, scale_x=leftxscale, scale_y=leftyscale)
leftRoot.moveto(lx, ly, scale_x=leftxscale, scale_y=leftyscale)
rightRoot.moveto(rx, ry, scale_x=rightxscale, scale_y=rightyscale)

character.append([leftRoot, rightRoot])
character.save(outputDir + inputStr + ".svg")
