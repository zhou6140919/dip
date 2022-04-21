import random
from PIL import Image
from struct import unpack, pack

class BMP24:
    def __init__(self, file_path):
        self.file_path = file_path
        self.f = open(file_path, 'rb')

    def read_header(self):
        self.f.seek(0)
        self.header = self.f.read(54)

    def parse_header(self):
        if not hasattr(self, 'header'):
            self.read_header()
            self.bfType = self.header[0:2]
            self.bfSize = self.header[2:6]
            self.bfReserved1 = self.header[6:8]
            self.bfReserved2 = self.header[8:10]
            self.bfOffBits = self.header[10:14]
            self.biSize = self.header[14:18]
            self.biWidth = self.header[18:22]
            self.biHeight = self.header[22:26]
            self.biPlanes = self.header[26:28]
            self.biBitCount = self.header[28:30]
            self.biCompression = self.header[30:34]
            self.biSizeImage = self.header[34:38]
            self.biXPelsPerMeter = self.header[38:42]
            self.biYPelsPerMeter = self.header[42:46]
            self.biClrUsed = self.header[46:50]
            self.biClrImportant = self.header[50:54]
            self.height = unpack('<i', self.biHeight)[0]
            self.width = unpack('<i', self.biWidth)[0]
            print("image pixel size:", self.height, self.width)
    
        if unpack("<H", self.biBitCount)[0] != 24:
            raise Exception('Not a 24-bit BMP file')
    def read_data(self):
        self.parse_header()
        self.f.seek(unpack('<i', self.bfOffBits)[0])
        self.bits = []
        for row in range(self.height):
            bits_row = []
            count = 0
            for pixel in range(self.width):
                bits_row.append(self.f.read(3))
                while count % 4 != 0:
                    self.f.read(1)
                    count += 1
            self.bits.append(bits_row)
        print('BMP data read')

    def write_data(self, bits, file_name):
        with open(file_name, 'wb') as w:
            w.write(self.header)
            for row in bits:
                for pixel in row:
                    w.write(pixel)
        print('BMP data written in', file_name)
        Image.open(file_name).show()

    def change_data(self):
        self.read_data()
        self.changed_bits = []
        for row in range(len(self.bits)):
            changed_row = []
            for pixel in range(len(self.bits[row])):
                if 390 <= row < 400 and 390 <= pixel < 400:
                    tmp_pixel = "\x00\x00\x00".encode()
                else:
                    tmp_pixel = self.bits[row][pixel]
                changed_row.append(tmp_pixel)
            self.changed_bits.append(changed_row)
        print('BMP data changed')

    def add_frame(self, frame_width):
        self.read_data()
        self.change_header(self.width + frame_width, self.height + frame_width)
        self.sorted_bits = []
        self.changed_bits = []
        for i in range(frame_width//2):
            self.changed_bits.append(["\x00\x00\x00".encode()] * (self.width + frame_width))
        for row in self.bits:
            changed_row = []
            changed_row.extend(["\x00\x00\x00".encode()] * (frame_width//2))
            for pixel in row:
                changed_row.append(pixel)
            changed_row.extend(["\x00\x00\x00".encode()] * (frame_width//2))
            self.changed_bits.append(changed_row)
        for i in range(frame_width//2):
            self.changed_bits.append(["\x00\x00\x00".encode()] * (self.width + frame_width))
        print('BMP added frame')

    def change_header(self, width, height):
        self.parse_header()
        self.biWidth = pack("<i", width)
        self.biHeight = pack("<i", height)
        self.biSizeImage = pack("<i", width * height * 3)
        self.bfSize = pack("<i", 54 + width * height * 3)
        self.header = self.bfType + self.bfSize + self.bfReserved1 + self.bfReserved2 + self.bfOffBits + self.biSize + self.biWidth + self.biHeight + self.biPlanes + self.biBitCount + self.biCompression + self.biSizeImage + self.biXPelsPerMeter + self.biYPelsPerMeter + self.biClrUsed + self.biClrImportant
        print('BMP header changed')

    def confirm_color(self):
        self.read_data()
        self.area = []
        for r in range(len(self.bits)):
            row_bits = []
            for c in range(len(self.bits[r])):
                if 390 <= r < 400 and 390 <= c < 400:
                    row_bits.append(self.bits[r][c])
            if row_bits:
                self.area.append(row_bits)
        # print(self.area)

        all_colors = []
        for row in self.area:
            all_colors_row = []
            for bit in row:
                colors = (bit[2], bit[1], bit[0])
                all_colors_row.append(colors)
            all_colors.append(all_colors_row)
        print(all_colors)



if __name__ == '__main__':
    img1 = BMP24('./raw_image/img1_24.bmp')
    # img1.change_data()
    # img1.write_data(img1.changed_bits, './generated_image/img2_24.bmp')
    # img1.read_data()
    # print(img1.bits)
    # img1.confirm_color()
    img1.add_frame(8)
    img1.write_data(img1.changed_bits, './generated_image/img3_24.bmp')
