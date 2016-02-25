#!/usr/bin/env python
"""BFM - Generating bitmaps in fun ways"""
import Image
import ca2d
import math
import random

"""Creates a bitmap using the given functions"""
def functionalBitmap(length, width, filename, rF, gF, bF):
    img = Image.new('RGB', (length, width), "white")
    p = img.load()
    
    def clamp(n):
        return max(min(255, n), 0)
    
    for i in range(img.size[0]):
        for j in range (img.size[1]):
            p[i, j] = (clamp(rF(i, j)), clamp(gF(i, j)), clamp(bF(i, j)))
    img.save(filename + ".bmp")
    
"""Creates a bitmap using the Cellular Autonoma rules"""
def caBitmap(length, width, filename, rR, gR, bR, seed):
    img = Image.new('RGB', (width, length), "white")
    p = img.load()
        
    #First Row Condition
    if seed == 'm':
        middle = math.floor(width / 2)
        p[middle, 0] = (0, 0, 0)
    else: 
        random.seed(seed)    
        for i in range(0, width):
            p[i, 0] = (random.randint(0, 1) * 255, random.randint(0, 1) * 255, random.randint(0, 1) * 255)
    
    #Convert rules to arrays
    rules = [[0 for i in range(8)] for j in range(3)]
    def bitfield(n):
        bn = bin(n)[2:]
        if len(bn) < 8:     #Need to pad with 0's 
            dif = 8 - len(bn)
            for i in range(dif):
                bn = '0' + bn
        return [int(digit) for digit in bn]
    
    rules[0] = bitfield(rR)
    rules[1] = bitfield(gR)
    rules[2] = bitfield(bR)

    #return the color [ R, G, B ] given the 'r'ules and 'p'arents
    def applyRule(r, p):
        intp = 0
        color = ()
        for c in range(0, 3):
            intp = 0
            for parent in range(0, 3):
                if p[parent][c] == 255:
                    intp += 2 ** parent
            color += (0 if r[c][intp] == 1 else 255,)
        return color
    
    #return the parents colors [[p0r,g,b],[p1r,g,b],[p2r,g,b]]    
    def getParents(pix, i, r, w):
        par = [[0 for z in range(3)] for j in range(3)]
        #middle pixel is always in range
        par[1] = [pix[i, r-1][0], pix[i, r-1][1], pix[i, r-1][2]]
        #Two exceptional cases, i=0, i=width-1
        if i == 0:
            par[0] = [255, 255, 255]
            par[2] = [pix[i + 1, r-1][0], pix[i + 1, r-1][1], pix[i + 1, r-1][2]]        
        elif i == width-1:
            par[2] = [255, 255, 255]
            par[0] = [pix[i-1, r-1][0], pix[i-1, r-1][1], pix[i-1, r-1][2]] 
        else:
            par[0] = [pix[i-1, r-1][0], pix[i-1, r-1][1], pix[i-1, r-1][2]]
            par[2] = [pix[i + 1, r-1][0], pix[i + 1, r-1][1], pix[i + 1, r-1][2]]       
        return par
        
    for row in range(1, length):
        for i in range(0, width):
            parents = getParents(p, i, row, width)
            p[i, row] = applyRule(rules, parents)
    img.save(filename + ".bmp")

def ca2dBW(l, f, r, i=2, s="r"):
    if s == "r":
        s = random.randint(0, 125000)
    ca2dBitmap(l, f, r, r, r, i, s, "yes")
    
def ca2dColor(l, f, rR, rG, rB, i, s="r"):
    if s == "r":
        s = random.randint(0, 125000)
    ca2dBitmap(l, f, rR, rG, rB, i, s, "no")
    
"""Creates a 2D image by 'wrapping' an Elementary CA around a center point"""
#def ca2dBitmap( length, filename, rule, innersize=7, seed=2 ):
def ca2dBitmap(length, filename, rR, rG, rB, innersize=2, seed=2, monochrome="no"):    
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    #Make image
    
    #Make length always odd, so we have a center pixel
    if length % 2 == 0:
        l = length + 1    
    else:
        l = length
    img = Image.new('RGB', (l, l), "white")
    p = img.load()
    
    center_x = (l-1) / 2
    center_y = (l-1) / 2
    #If seed isnt given, default pattern (cross)
    if seed == "n":
        p[center_x, center_y] = BLACK
        p[center_x + 1, center_y] = BLACK
        p[center_x-1, center_y] = BLACK
        p[center_x, center_y-1] = BLACK
        p[center_x, center_y + 1] = BLACK
    else:
        #for a box of 'radius' innersize around the center, randomly set white/black
        for i in range(-innersize, innersize + 1):
            for j in range(-innersize, innersize + 1):
                if monochrome == "yes":
                    p[center_x + i, center_y + j] = WHITE if random.randint(0, 1) == 1 else BLACK
                else:
                    p[center_x + i, center_y + j] = randC()
    
    #calculate # of generations
    gencount = (l-1) / 2
    print "length: ", l, " Gencount: ", gencount, "Start Gen: ", innersize
    
    
    #Side structs
    sides = []
    sides.append(ca2d.Side(1, 1, 0, -1, center_x, center_y, rR, rG, rB, innersize)) #pointing right, going up   
    sides.append(ca2d.Side(1, -1, -1, 0, center_x, center_y, rR, rG, rB, innersize)) #pointing up, going left
    sides.append(ca2d.Side(-1, -1, 0, 1, center_x, center_y, rR, rG, rB, innersize)) #pointing left, going down
    sides.append(ca2d.Side(-1, 1, 1, 0, center_x, center_y, rR, rG, rB, innersize)) #pointing down, going right
    
    #Corner structs
    corners = []
    corners.append(ca2d.Corner(1, 1, center_x, center_y, rR, rG, rB, innersize))
    corners.append(ca2d.Corner(1, -1, center_x, center_y, rR, rG, rB, innersize))
    corners.append(ca2d.Corner(-1, -1, center_x, center_y, rR, rG, rB, innersize))
    corners.append(ca2d.Corner(-1, 1, center_x, center_y, rR, rG, rB, innersize))
    
    #Loop over generations (start at 2 to ignore middle cells)
    for g in range (innersize, gencount + 1):
        for s in sides:
            s.update(p)
        for c in corners:
            b = c.update(p)
            
    #save image out
    img.save(filename + ".bmp")
    
    
def randC():
    r = random.randint(0, 1) * 255
    g = random.randint(0, 1) * 255
    b = random.randint(0, 1) * 255
    return (r, g, b)          

"""Script Use Cases"""
if __name__ == "__main__":
    import sys
    usage = "-x: Runs Examples"
    usage += "\n-ca l w fn rule:  Creates b/w image using the CA rule given int(0,255).  Uses 1 live cell in the middle of first row to start."
    usage += "\n-ca l w fn redrule greenrule bluerule: As above but seperate rule for each color channel"
    usage += "\n-ca l w fn rule seed: b/w image using given CA rule, but first row is random based on seed"
    usage += "\n-ca l w fn redrule greenrule bluerule seed: seperate rules. with first row determined by seed"
    if len(sys.argv) == 1:
        print usage
    elif len(sys.argv) > 1:    
        if sys.argv[1] == "-x":
            extext  = " BMF.functionalBitmap generates a bitmap using functions to determine the value of a color channel"
            extext += "\n Calling functionalBitmap( 255, 255, 'test1', R, G, B ) would output a file 'test1.bmp' to the directory"
            extext += "\n with dimensions 100px X 100px.  The value of the RGB channels at a point x,y in the image will be "
            extext += "\n determined by the given functions (expecting two inputs) R(x,y), G(x,y), B(x,y)"
            extext += "\n These functions are clamped to the range [0,255].  For the following: l,w = 255,255\n"
            extext += "\n  filename  |    R(x,y)   |    G(x,y)    |    B(x,y)    "
            extext += "\n--------------------------------------------------------- "
            print extext
            
            extext  = "  gradientx |      x      |      x       |      x     "
            print extext
            def gradx(x, y):
                return x
            functionalBitmap(255, 255, 'gradientx', gradx, gradx, gradx)
            
            extext  = "  gradienty |      y      |      y       |      y     "
            print extext
            def grady(x, y):
                return y
            functionalBitmap(255, 255, 'gradienty', grady, grady, grady)
            
            extext  = "  vargrad   |      x      |      y       |    255-y     "
            print extext
            def invy(x, y):
                return 255-y
            functionalBitmap(255, 255, 'vargrad', gradx, grady, invy)
            
            extext  = "  trigfun   |  255*sin(x) |  255*cos(y)  |    255-y     "
            print extext
            def sx(x, y):
                return int(math.sin(x) * 255)
            def cy(x, y):
                return int(math.cos(y) * 255)
            functionalBitmap(255, 255, 'trigfun', sx, cy, invy)
            
            extext  = "\n BMF.caBitmap generates a bitmap using cellular autonama rules to determine the color channel values."
            extext += "\n The first row of pixels is either a live middle pixel, or random based on the command"
            extext += "\n Subsequent rows will be determined by applying the CA rule given to the previous row, in the color channel for the rule.  CA rules must be given as a integer [0, 256]"
            extext += "\n The 8-bit representation of the int corresponds to the 8 possible parent states. If 1, alive, if 0 dead."
            extext += "\n A concise explanation can be found here: http://mathworld.wolfram.com/ElementaryCellularAutomaton.html"
            extext += "\n\n Differet rules may be passed for all three color channels.\n"
            extext += "\n  filename  |           script call          |        function call"        
            extext += "\n------------------------------------------------------------------------------------------"
            extext += "\n   rule30   | -ca 255 255 'rule30' 30 30 30  | caBitmap(255,255,'rule30',30,30,30,'m') "
            extext += "\n   rule90   | -ca 255 255 'rule90' 90 90 90  | caBitmap(255,255,'rule90',90,90,90,'m') "
            extext += "\n   rules    | -ca 255 255 'rules'  30 138 60 | caBitmap(255,255,'rules',30,138,60,'m') "
            print extext
            caBitmap(255, 255, 'rule30', 30, 30, 30, 'm')
            caBitmap(255, 255, 'rule90', 90, 90, 90, 'm')
            caBitmap(255, 255, 'rules', 30, 138, 60, 'm')
            
            extext = "\n If a 7th value is added, the function will use that as the seed to randomly fill"
            extext += "\n the first row."
            extext += "\n  filename  |           script call              |     function  call"        
            extext += "\n------------------------------------------------------------------------------------------------"
            extext += "\n   random   | -ca 255 255 'random' 30 90 30 3148 | caBitmap(255,255,'random',30,90,30,3148) "
            print extext
            caBitmap(255, 255, 'random', 30, 90, 30, 3148)
        #Cellular Autonoma Usage
        elif sys.argv[1] == "-ca":
            a = sys.argv
            l = int(a[2])
            w = int(a[3])
            f = a[4]
            R = int(a[5])
            G = int(a[6])
            B = int(a[7])
            if len(sys.argv) == 8:
                #middle first row
                caBitmap(l, w, f, R, G, B, 'm')
                print f + ".bmp created. Using rules: ", R, G, B, " with lone live cell to start." 
            elif len(sys.argv) == 9:
                #random seed first row
                s = int(a[8])
                caBitmap(l, w, f, R, G, B, s)
                print f + ".bmp created using rules :", R, G, B, " random seed: ", s
            else:
                print usage
        elif sys.argv[1] == "-2d":
            print "calling 2d"
            if len(sys.argv) == 7:
                a = sys.argv
                l = int(a[2])
                f = a[3]
                r = int(a[4])
                i = int(a[5])
                s = int(a[6])
                if 2 * i > l + 1:
                    i = 2
                #2dcaBitmap( length, filename )
                ca2dBitmap(l, f, r, i, s)
            if len(sys.argv) == 6:
                a = sys.argv
                l = int(a[2])
                f = a[3]
                r = int(a[4])
                i = int(a[5])
                s = random.randint(0, 3600)
                if 2 * i > l + 1:
                    i = 2
                #2dcaBitmap( length, filename )
                ca2dBitmap(l, f, r, i, s)
            if len(sys.argv) == 5:
                a = sys.argv
                l = int(a[2])
                f = a[3]
                r = int(a[4])
                i = int(a[5])
                s = random.randint(0, 3600)
                if 2 * i > l + 1:
                    i = 2
                #2dcaBitmap( length, filename )
                ca2dBitmap(l, f, r, i, s)
        elif sys.argv[1] == "-2dc":
            print "calling 2dcolor"
            print len(sys.argv)
            if len(sys.argv) == 8:
                a = sys.argv
                l = int(a[2])
                f = a[3]
                rR = int(a[4])
                rG = int(a[5])
                rB = int(a[6])
                i = int(a[7])
                s = random.randint(0, 3600)
                if 2 * i > l + 1:
                    i = 2
                #2dcaBitmap( length, filename )
                ca2dBitmap(l, f, rR, rG, rB, i, s)

        else:
            print usage        
            
            