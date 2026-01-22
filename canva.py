Cw = 480
Ch = 270

class Canva:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.pixels = [
            [(0, 0, 0) for _ in range(width)]
            for _ in range(height)
        ]

    def putPixel(self,x,y,color_tuple):
        Sx = Cw//2 + x
        Sy = Ch//2 -y
        if (0 <= Sx < self.width and 0 <= Sy < self.height):
            self.pixels[Sy][Sx] = color_tuple

    def savePPM(self, filename):
        with open(filename, "w") as f:
            # Header
            f.write("P3\n")                                 #Précision du type (ici ASCII)
            f.write(f"{self.width} {self.height}\n")        #Précision du format
            f.write("255\n")                                #précision valeur max

            # Pixels
            for y in range(self.height):            #parcours des lignes
                for x in range(self.width):         #parcours des colonnes
                    r, g, b = self.pixels[y][x]     #extraction du tuple
                    f.write(f"{r} {g} {b} ")        #écriture dans le fichier
                f.write("\n")                       #fin de la lignes --> ligne suivante