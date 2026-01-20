class Color:
    def __init__(self,r,g,b):
        self.r=r
        self.g=g
        self.b=b

    def to_tuple(self):
        return (
            min(255, max(0, int(self.r))),
            min(255, max(0, int(self.g))),
            min(255, max(0, int(self.b)))
        )
    def __mul__(self, k):
        return Color(self.r*k, self.g*k, self.b*k)
    
    def __add__(self,color):
        return Color(self.r+color.r, self.g+color.g, self.b+color.b)