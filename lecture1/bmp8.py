from struct import unpack
from PIL import Image


class BMP8:
    def __init__(self, file_path):
        self.file_path = file_path
        self.f = open(file_path, 'rb')
        self.header = self.read_header()
        self.parse_header()
        self.read_data()

    def read_header(self):
        self.f.seek(0)
        return self.f.read(54)

    def parse_header(self):
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
        print("Header parsed")
        self.height = unpack('<i', self.biHeight)[0]
        self.width = unpack('<i', self.biWidth)[0]
        print("image pixel size:", self.height, self.width)


        if unpack('<H', self.biBitCount)[0] != 8:
            raise Exception('Only 8 bit BMPs are supported')

    def read_data(self):
        self.f.seek(54+1024)
        self.bits = []
        for r in range(self.height):
            self.bits.append([])
            for p in range(self.width):
                self.bits[r].append(self.f.read(1))
        print("Data read")
    def read_color_table(self):
        self.f.seek(54)
        self.color_table = {}
        self.int_color_table = {}
        for n in range(256):
            b = self.f.read(1)
            g = self.f.read(1)
            r = self.f.read(1)
            a = self.f.read(1)
            self.color_table[n] = (b, g, r)
            self.int_color_table[n] = (unpack('<B', b)[0], unpack('<B', g)[0], unpack('<B', r)[0])
        print("Color table read")
    def write_color_table(self, file_name):
        with open(file_name, 'wb') as w:
            w.write(self.header)
            for n in range(256):
                w.write(self.color_table[n][0])
                w.write(self.color_table[n][1])
                w.write(self.color_table[n][2])
                w.write('\x00'.encode())
            for r in self.bits:
                for p in r:
                    w.write(p)
        Image.open(file_name).show()
    def change_color(self, color_index, new_color):
        self.color_table[color_index] = new_color
        print(f"{color_index}th Color changed")


if __name__ == '__main__':
    img1 = BMP8("./raw_image/img1_8.bmp")
    img1.read_color_table()
    # change white background to black
    img1.change_color(255, ('\x00'.encode(), '\x00'.encode(), '\x00'.encode()))
    img1.write_color_table("./tmp_8.bmp")

