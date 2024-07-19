
# ASCII Renderer
## Video Demo: __TO DO___
### Description: 
A program that converts images to ASCII Art and displays them in terminal in color.

## How does the program work? 

We open an image file using the `open cv` library. After that, we can access the rgb value of each individual pixel in the image and get its size in pixels.

`resolution` defines the number of pixels, height and width of a square, that will be converted into a single character in the final product. 

A resolution of 5px (default) means each square of 5px x 5px. In other words, each square of 25 pixels in the image will become an individual character in the final image. 

We convert the image to a more manageable size(default = 600px max width or height), and divide that by the `resolution`. With that we get our `loop_x` and `loop_y`, which essentially means amount of Columns and Rows in the image. 

After that, we check the avarege rgb value for that squre of pixels, defines by the resolution, and store that, toghether with the luminance values, wich are calculated based on the rgb values. 

Once we have the luminance and rgb values of each resolution square, we simplu loop through all of them placing the correct ASCII based on the luminance and color them using ANSI codes.

## Installation

```
git clone https://github.com/PoloClebicar/CS50P_Final_Project.git
``` 

Move into the downloaded directory. 

`python3 project.py -i ./path_to_img`

## What arguments do we pass in this program?

`-i ./path_to_img`

This is the only argument required by the program. It's the path to a valid image type(.jpeg, .jpg, .png)

`-r --resolution int` 

Allows for changes in the resolution of the final image. The smaller the value, the greater the number of characters in the final output.

`-o --outline int`

Toggles the outline feature on and off. The outline feature uses an edge detection method called sobel filter, to detect harsh changes in contrast in the image, allowing the program to detect edges. Unfortunately, this only makes a noticeable difference in certain images and is kept turned off by default.

`-a --ascii int`

Allows the choice between 3 different sets of characters to draw the final image.1 - Only original ASCII characters2 - Extended ASCII characters are included3- UNICODE characters are included

`-c --color`

Toggles between the color mode (default) and non-color (your default terminal color) characters

