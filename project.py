import argparse
"""

Setting Up the Argparser to take all the necessacy and extra arguments.

"""
parser = argparse.ArgumentParser(
                    prog='CS50 Final Project -  ASCII Renderer',
                    description='This programs imports a img and convert that image to ASCII, and display it in the terminal.',
                    epilog='Usage: project.py -i ./path_to_image -r int -o bool -a int')


parser.add_argument("-r", "--resolution", type=int, help="int [1-15], Changes the resolution of the grid of ASCII, the smaller the value, the greater the amouunt of characters printed.(Default 7)")
parser.add_argument("-o", "--outline", type=bool, help="bool, Toggle the Outline Effect ON and OFF(Default).")
parser.add_argument("-a", "--ascii", type=int, help="int [1-3], Toggles between the 3 types of characters list - ASCII / Extended ASCII / UNICODE(Default)")
parser.add_argument("-n","--noise", type=bool, help="bool oggles the noise feature ON and OFF(Default). When ON, mix between diferent ASCII characters for same level of brightness.")
parser.add_argument("-c", "--color", type=bool, help="bool, Toggles from Black and White to Color Mode(Default)")
parser.add_argument("-i", "--image", required=True, help="Required path to img.")
arg = parser.parse_args()

print("hello")