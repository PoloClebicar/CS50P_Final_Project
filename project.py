#Importing all the Libraries
import argparse
import cv2
import math


"""

Setting Up the Argparser to take all the necessacy and extra arguments.

"""
parser = argparse.ArgumentParser(
                    prog='CS50 Final Project -  ASCII Renderer',
                    description='This programs imports a img and convert that image to ASCII, and display it in the terminal.',
                    epilog='Usage: project.py -i ./path_to_image -r int -o bool -a int')


parser.add_argument("-r", "--resolution",   type=int,       help="int [1-15], Changes the resolution of the grid of ASCII, the smaller the value, the greater the amouunt of characters printed.(Default 7)")
parser.add_argument("-o", "--outline",      type=bool,      help="bool, Toggle the Outline Effect ON and OFF(Default).")
parser.add_argument("-a", "--ascii",        type=int,       help="int [1-3], Toggles between the 3 types of characters list - ASCII / Extended ASCII / UNICODE(Default)")
parser.add_argument("-n","--noise",         type=bool,      help="bool Toggles the noise feature ON and OFF(Default). When ON, mix between diferent ASCII characters for same level of brightness.")
parser.add_argument("-c", "--color",        type=bool,      help="bool, Toggles from Black and White to Color Mode(Default)")
parser.add_argument("-i", "--image",        required=True,  help="Required path to img.")
args = parser.parse_args()

#Defining Necessaty Variables
max_height = 600
max_width = 600

resolution = 5

def main():
    #Getting User image size
    img_file = cv2.imread(args.image)
    
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
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) 
    #This is the important one that we will use to detect outlines
    edges = cv2.Canny(image=img_blur, threshold1=50, threshold2=120) 

    #Getting the amount of loops
    loop_x , loop_y = get_loop_sizes(new_x, new_y)

    #Getting the size of the loops
    rgb_list, sobel_list = get_rgb_values(loop_x, loop_y, img_file, edges)

    for rgb in rgb_list:
        print(rgb)

    for sobel in sobel_list:
        print(sobel)

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

def get_rgb_values(loop_x, loop_y, img, edges):
    global resolution
    base_y = 0
    base_x = 0
    rgb_list = []
    sobel_list = []
    square_res = math.pow(resolution, 2)
    red = 0
    green = 0
    blue = 0
    sobel = 0

    for _ in range(loop_y):
        for __ in range(loop_x):
            for i in range(resolution):
                for j in range(resolution):
                    pixel = img[i + base_y][j + base_x]
                    red += pixel[2]/square_res
                    green += pixel[2]/square_res
                    blue += pixel[2]/square_res
                    sobel = edges[i + base_y][j + base_x]/square_res
            base_x += resolution
            rgb_list.append([int(red * 0.299), int(green * 0.587), int(blue * 0.114)])
            sobel_list.append(int(sobel))
            red = 0
            green = 0
            blue = 0
            sobel = 0
        base_x = 0
        base_y += resolution
    base_y = 0

    return rgb_list, sobel_list

main()