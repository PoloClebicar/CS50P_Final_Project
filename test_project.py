import project
import cv2

def test_new_img_size():
   assert project.new_img_size(1000, 1000) == (600, 600)
   assert project.new_img_size(1000, 500) == (600, 300)
   assert project.new_img_size(500, 1000) == (300, 600)
   assert project.new_img_size(2500, 1000) == (600, 239)

def test_loop_sizes():
   assert project.get_loop_sizes(600, 600) == (120, 120)
   assert project.get_loop_sizes(500, 250) == (100, 50)
   assert project.get_loop_sizes(1920, 1080) == (384, 216)
   assert project.get_loop_sizes(2000, 200) == (400, 40)
   assert project.get_loop_sizes(200, 2000) == (40, 400)

def test_get_lists():
    img = cv2.imread("01.png")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
    edges = cv2.Canny(image=img_blur, threshold1=60, threshold2=150) 

    assert project.get_lists(5, 5, img, edges) == ([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], 
                                                    [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], 
                                                    [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], 
                                                    [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], 
                                                    [254, 254, 254], [254, 254, 254], [254, 254, 254], [254, 254, 254], [254, 254, 254]], 
                                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 0, 0, 0, 0, 0], 
                                                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 253, 253, 253, 253, 253])

def test_crush_lum_values():
    list = [50, 50, 150, 160, 200]
    assert project.crush_lum_values(list) == [0,0,170,187,255]
    list = [0, 50, 50, 200, 255]
    assert project.crush_lum_values(list) == [0,50,50,200,255]
    list = [10, 10, 10, 10, 255]
    assert project.crush_lum_values(list) == [0,0,0,0,255]

def test_generate_ascii_list():
    rgb =[[[100],[0],[0]],
          [[100],[0],[0]],
          [[100],[0],[0]],
          [[100],[0],[0]]]    
    lum =[[[100],[0],[0]],
          [[100],[0],[0]],
          [[100],[0],[0]],
          [[100],[0],[0]]]
    out =[[[100],[0],[0]],
          [[100],[0],[0]],
          [[100],[0],[0]],
          [[100],[0],[0]]]
    assert project.generate_ASCII_list(rgb,lum,out,2,2) == ['\x1b[38;2;[100];[0];[0]m\x1b[0m', '\x1b[38;2;[100];[0];[0]m\x1b[0m', 
                                                            '\x1b[38;2;[100];[0];[0]m\x1b[0m', '\x1b[38;2;[100];[0];[0]m\x1b[0m', '\n', 
                                                            '\x1b[38;2;[100];[0];[0]m\x1b[0m', '\x1b[38;2;[100];[0];[0]m\x1b[0m', 
                                                            '\x1b[38;2;[100];[0];[0]m\x1b[0m', '\x1b[38;2;[100];[0];[0]m\x1b[0m', '\n']
