from bmp24 import BMP24
from bmp8 import BMP8
import time

# read 24bit bmp file
print("reading 24bit bmp file")
time.sleep(1)
img1 = BMP24("./raw_image/img1_24.bmp")
img1.read_data()
img1.write_data(img1.bits, "./generated_image/origin_img1_24.bmp")
print("-" * 40)
# randomly change pixels to black
print("randomly change pixels to black")
time.sleep(1)
img1.change_data()
img1.write_data(img1.changed_bits, "./generated_image/img2_24.bmp")
print("-" * 40)
# add frame
print("add frame")
time.sleep(1)
img1.add_frame(8)
img1.write_data(img1.changed_bits, "./generated_image/img3_24.bmp")
print("-" * 40)

print("press enter to continue")
input()

# read 8bit bmp file
print("reading 8bit bmp file")
time.sleep(1)
img2 = BMP8("./raw_image/img1_8.bmp")
img2.read_data()

# change white to black in the color table
print("change white to black in the color table")
time.sleep(1)
img2.read_color_table()
img2.change_color(255, ('\x00'.encode(), '\x00'.encode(), '\x00'.encode()))
img2.write_color_table("./generated_image/img2_8.bmp")


print("Done")
