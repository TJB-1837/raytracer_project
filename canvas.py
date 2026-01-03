class Canva:

    def putPixel(x,y,color):
        return (1920/2 + x, 1080/2 -y)
        

class Color:

    def __init__(self,r,g,b):
     (255,255,255)

    def add(color1,color2) : 
        if(color1.r+color2.r> 255 or color1.g+color2.g>255 or color1.b+color2.b>255):
            print("out of range colors")
            return
        else : 
            return Color(color1.r+color2.r, color1.g+color2.g, color1.b+color2.b)
