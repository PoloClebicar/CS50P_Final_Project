#Importing all the Libraries
import argparse
import cv2
import math
import sys

#Ended up needing to place this vatiable here for testing purpose. Not sure how to simulate tests when using argparse. Need to check it later
max_height = 600
max_width = 600
resolution = 5
outline = 0
ascii_table = 2
color = 1

def main():
    global max_height
    global max_width 
    global resolution 
    global outline 
    global ascii_table 
    global color 

    """

    Setting Up the Argparser to take all the necessacy and extra arguments.

    """
    parser = argparse.ArgumentParser(
                        prog='CS50 Final Project -  ASCII Renderer',
                        description='This programs imports a img, converts that image to ASCII, and displays it on the terminal.',
                        epilog='Usage: project.py -i ./path_to_img')


    parser.add_argument("-r", "--resolution",   type=int,       default= 5,     help="int [1-10], Changes the resolution of the grid of ASCII, the smaller the value, the greater the amouunt of characters printed.(Default 7)")
    parser.add_argument("-o", "--outline",      type=int,       default= 0,     help="int [0-1], Toggle the Outline Effect ON and OFF(Default).")
    parser.add_argument("-a", "--ascii",        type=int,       default= 2,     help="int [1-3], Toggles between the 3 types of characters list - ASCII / Extended ASCII(Default) / UNICODE")
    parser.add_argument("-c", "--color",        type=int,       default=1,      help="int [0-1], Toggles from Black and White to Color Mode(Default)")
    parser.add_argument("-x", "--xHeight", type=int, default=600, help="int [200 - 2000], The maximum height of the output ASCII img")
    parser.add_argument("-y", "--yWidth", type=int, default=600, help="int[200 - 2000], The maximum width of the output ASCII img")
    parser.add_argument("-i", "--image",        required=True,  help="Required path to img.")
    args = parser.parse_args()

    #Managind output resolution
    if(200 <= args.xHeight <= 2000): max_height = args.xHeight
    else:sys.exit("ASCII Imgae resolution Out of Bounds")
    if(200 <= args.yWidth <= 2000): max_width = args.yWidth
    else:sys.exit("ASCII Imgae resolution Out of Bounds")

    #Managing Resolution
    if (1 <= args.resolution <= 10): resolution = args.resolution
    else: sys.exit("Resolution Out of Bounds")

    #Managing Outline
    if (0 <= args.outline <= 1): outline = args.outline
    else: sys.exit("Outline Argument Out of Bounds")

    #Managing ASCII
    if (1 <= args.ascii <= 3): ascii_table = args.ascii
    else: sys.exit("ASCII Argument Out of Bounds")

    #Managing Color
    if (0 <= args.color <= 1): color = args.color
    else: sys.exit("Color Argument Out of Bounds")

    #Getting User image size
    img_file = cv2.imread(args.image)
    #assert img_file != None, sys.exit("Image Not Found")
    
    #cv2.imshow("Test", img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #print(img_size(img))

    #Getting the Original Image Size
    original_size_x, original_size_y = img_size(img_file)
    #print(new_img_size(original_size_x, original_size_y))

    #Resizing the Image
    img_file = cv2.resize(img_file, new_img_size(original_size_x, original_size_y))

    new_x ,new_y = img_size(img_file)

    # Steps needed to edge detect later
    img_gray = cv2.cvtColor(img_file, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
    #This is the important one that we will use to detect outlines
    edges = cv2.Canny(image=img_blur, threshold1=60, threshold2=150) 

    #Getting the amount of loops
    loop_x , loop_y = get_loop_sizes(new_x, new_y)

    #Getting the size of the loops
    rgb_list, sobel_list, lum_list = get_lists(loop_x, loop_y, img_file, edges)
    lum_list = crush_lum_values(lum_list)

    #for rgb in rgb_list: print(rgb)
    #for sobel in sobel_list: print(sobel)
    #for lum in lum_list: print(lum)

    ascii_list = generate_ASCII_list(rgb_list, sobel_list, lum_list, loop_x, loop_y)

    for char in ascii_list:
        print(char, end='')

def img_size(img):
    return img.shape[1], img.shape[0]
    ...

def new_img_size(size_x, size_y):
    """
    Returns the new Image size, making the larger side of the image equal to the Max size, and scaling the other side by the same amount

    :param size_x: The height of the image
    :type size_x: int
    :param size_y: The width of the image
    :type size_y: int
    """
    global max_height
    global max_width
    
    #Check What size of the image is larger
    if size_x > size_y:
        #If bigger than the max size, we reduce the size to the max
        if size_x > max_height:
            factor = size_x/max_height
            return (int(size_x/factor)), (int(size_y/factor))
        else:
            #If smaller than the max, we expand the size
            factor = max_height/size_x
            return (int(size_x * factor), int(size_y * factor))
    else:
        #If bigger than the max size, we reduce the size to the max
        if size_y > max_width:
            factor = size_y/max_width
            return (int(size_x/factor)), (int(size_y/factor))
        else:
            #If smaller than the max, we expand the size
            factor = max_width/size_y
            return (int(size_x * factor), int(size_y * factor))

def get_loop_sizes(x, y):
    """
    Returns the size of the loops, needed to convert the image to ASCII on the correct resolution

    :param x: Height of the image 
    :type x: int
    :param y: Width of the image 
    :type y: int
    """
    global resolution
    return int(x/resolution), int(y/resolution) 

def get_lists(loop_x, loop_y, img, edges):
    """
    Returns the RGB Value list, Sobel Value List and the Luminance Value List.
    :param loop_x: The number of collumns in the ASCII image
    :type loop_X: int
    :param loop_y: The number of rows in the ASCII image
    :type loop_y: int
    :param img: The orginal image uploaded by the user after resizing
    :type img: Open CV Image
    :param edges: The orginal image after resizing and converting to edge detection
    :type img: Open CV Image
    """
    global resolution
    base_y = 0
    base_x = 0
    rgb_list = []
    sobel_list = []
    lum_list = []
    square_res = math.pow(resolution, 2)
    red = 0
    green = 0
    blue = 0
    sobel = 0
    map_range = 0

    for _ in range(loop_y):
        for __ in range(loop_x):
            for i in range(resolution):
                for j in range(resolution):
                    pixel = img[i + base_y][j + base_x]
                    red += pixel[2]/square_res
                    green += pixel[1]/square_res
                    blue += pixel[0]/square_res
                    sobel = edges[i + base_y][j + base_x]/square_res
            base_x += resolution
            rgb_list.append([int(red) ,int(green), int(blue)])
            lum_list.append(int((0.299*rgb_list[map_range][2] + 0.587*rgb_list[map_range][1] + 0.114*rgb_list[map_range][0])))
            map_range += 1
            sobel_list.append(int(sobel))
            red = 0
            green = 0
            blue = 0
            sobel = 0
        base_x = 0
        base_y += resolution
    base_y = 0

    return rgb_list, sobel_list, lum_list

def crush_lum_values(lum_list):
    """
    'Crushes' the values in the Lum List. Making the smallest one map to the first ASCII in the density map, and the darkest to the last
    :param lum_list: A list of luminace values od each ASCII in the image
    :type lum_list: List
    """
    min_value = min(lum_list)

    for i in range(len(lum_list)):
        lum_list[i] = lum_list[i] - min_value

    max_value = max(lum_list)

    for j in range(len(lum_list)):
        lum_list[j] = int((lum_list[j]/max_value) * 255)

    return lum_list

def generate_ASCII_list(rgb_list, sobel_list, lum_list, loop_x, loop_y):
    if ascii_table == 1:
        ascii_desnsity = ["#", "@", "W", "w", "x", "h", "a", "}", "`", " " ]
    elif ascii_table == 2:
        ascii_desnsity = ["#", "@", "€", "w", "x", "«", "?", "ì", "•", " " ]
    elif ascii_table == 3:
        ascii_desnsity = ["Ã", "Ð", "Ö",  "#", "W", "w", "u", "²", ".", "´" ]
    map_range = 0
    to_print = ""
    ascii_list = []
    for _ in range(loop_y):
        for __ in range(loop_x):
            if lum_list[map_range] in range(25):
                to_print = ascii_desnsity[9]
            elif lum_list[map_range] in range(50):
                to_print = ascii_desnsity[8]
            elif lum_list[map_range] in range(75):
                to_print = ascii_desnsity[7]
            elif lum_list[map_range] in range(100):
                to_print = ascii_desnsity[6]
            elif lum_list[map_range] in range(125):
                to_print = ascii_desnsity[5]
            elif lum_list[map_range] in range(150):
                to_print = ascii_desnsity[4]
            elif lum_list[map_range] in range(170):
                to_print = ascii_desnsity[3]
            elif lum_list[map_range] in range(195):
                to_print = ascii_desnsity[2]
            elif lum_list[map_range] in range(220):
                to_print = ascii_desnsity[1]
            elif lum_list[map_range] in range(255):
                to_print = ascii_desnsity[0]
            
            if outline: 
                if sobel_list[map_range] != 0: to_print = "|"
            
            for _ in range(2):
                if color:
                    ascii_list.append(f'\033[38;2;{rgb_list[map_range][0]};{rgb_list[map_range][1]};{rgb_list[map_range][2]}m{to_print}\33[0m')
                else:
                    ascii_list.append(f'{to_print}')
            map_range += 1
        ascii_list.append(f"\n")

    return ascii_list


if __name__ == "__main__":
    main()