img1 = open('./raw_image/img1_8.bmp', 'rb').read()
img2 = open('./new_8.bmp', 'rb').read()

with open("img1.txt", 'wb') as f:
    f.write(img1)
with open("img2.txt", 'wb') as f:
    f.write(img2)
