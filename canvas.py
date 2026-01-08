import PIL

class Canvas:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.pixels = [
            [(0,0,0) for _ in range(width)]
            for _ in range(height)
        ]


    def putPixel(self,x,y,color):
        px = x + self.width//2
        py = self.height//2 - y - 1

        if 0 <= px < self.width and 0 <= py < self.height:
            self.pixels[py][px] = (
                max(0, min(255, int(color[0]))),
                max(0, min(255, int(color[1]))),
                max(0, min(255, int(color[2])))
            )


    def save(self,filename="render.ppm"):
        with open(filename,"wb") as f:
            header = f"P6\n{self.width} {self.height}\n255\n"
            f.write(header.encode())

            for row in self.pixels:
                for (r, g, b) in row:
                    f.write(bytes([r, g, b]))
