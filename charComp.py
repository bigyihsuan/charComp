import sys
import os
import json
import svgutils

# with open('sample.json') as f:
#     print(json.load(f))


def compose(svgDirectory: str, inputString: str, outputFile: str):
    return


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"Not enough arguments: expected 3 args, got {len(sys.argv)-1} args")
        exit(1)
