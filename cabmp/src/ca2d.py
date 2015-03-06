__author__ = "wpower"
__date__ = "$Feb 28, 2015 4:23:19 PM$"

"""Side - Used to simplify generation calculations for each side"""
class Side:
    """Side Constructor"""
    def __init__(self, f_x, f_y, inc_x, inc_y, centerx, centery, rR, rG,rB, start):
        #fx,fy are a kind of unit vector from the center to the first
        #cell in each generation for that side
        #incx,incy are a kind of unit vector from the first cell to 
        #the last in a generation
        self.n = start
        self.fx = f_x
        self.fy = f_y
        self.incx = inc_x
        self.incy = inc_y
        self.cenx = centerx
        self.ceny = centery      
        #self.rule = bitfield(r)
        self.rules = [bitfield(rR),bitfield(rG),bitfield(rB)]
        
    """Locate first cell in a generation"""
    def first(self, gen):
        #f vector points to the first cell - which is the corner (overlap)
        #so we go 'one in' in the direction of the inc vector
        #only one inc is ever non zero      
        first_x = self.cenx + gen * self.fx + self.incx
        first_y = self.ceny + gen * self.fy + self.incy
        return [first_x, first_y]
    
    """Seperating the different update situations"""
    def update(self, img):
        self.update_outer(img)
        self.update_inner(img)
        self.n = self.n + 1
    
    """Simple case - Parents all come from previous generation in same side"""
    def update_inner(self, img):
        #here we can assume 'parents' are cells in previous generations
        #basically the same as normal, but accouting for the inc vector
        f = self.first(self.n)
        prev = self.first(self.n-1)
        #print "N: ", self.n, "F ", f
        for i in range(1, self.n*2+1-3):
            #parents at
            p2 = [prev[0] + self.incx * i, prev[1] + self.incy * i]
            p1 = [prev[0] + self.incx * (i - 1), prev[1] + self.incy * (i - 1)]
            p0 = [prev[0] + self.incx * (i - 2), prev[1] + self.incy * (i - 2)]
            #current cell being updated
            img[f[0] + self.incx * i, f[1] + self.incy * i] = applycolors(p0, p1, p2, img, self.rules)
            #print "   ", i, "| 0:", p0, " 1:", p1, " 2:", p2
    
    """Parents come from previous corner and other sides previous generation"""
    def update_outer(self, img):
        f = self.first(self.n)                      #First of current  row
        p = self.first(self.n-1)                    #First of previous row 
        n1 = 2*(self.n-1)+1                         #Cells in current  row
        n0 = 2*(self.n-2)+1                         #Cells in previous row     
        fn = [f[0]+(n1-1)*self.incx, f[1]+(n1-1)*self.incy] #last cell in current  row
        pn = [p[0]+(n0-1)*self.incx, p[1]+(n0-1)*self.incy] #last cell in previous row
        
        #x' = x \cos \theta - y \sin \theta\,,
        #y' = x \sin \theta + y \cos \theta\,.
        ct = 0
        st = 1
        dx = self.incx*ct - self.incy*st
        dy = self.incx*st + self.incy*ct
          
        #0th side
        p0 = p
        p1 = [f[0]-dx, f[1]-dy]
        p2 = [f[0]-dx*2, f[1]-dy*2]
        side0 = (p0,p1,p2)
        #img[f[0], f[1]] = applyrule(p0, p1, p2, img, self.rule)
        img[f[0], f[1]] = applycolors(p0, p1, p2, img, self.rules)
        
        #nth side
        p2 = pn
        p1 = [fn[0]-dx, fn[1]-dy]
        p0 = [fn[0]-dx*2, fn[1]-dy*2]
        siden = (p0,p1,p2)
        img[fn[0], fn[1]] = applycolors(p0, p1, p2, img, self.rules)
        #print f, side0, fn, siden
        
"""Corner, very similar, but update reads parents from two seperate sides"""        
class Corner:
    def __init__(self, ix, iy, c_x, c_y, rR, rG,rB, start):
    #def __init__(self, ix, iy, c_x, c_y, rule, start):
        self.x = ix
        self.y = iy
        self.cenx = c_x
        self.ceny = c_y
        self.n = start      
        #self.rule = bitfield(rule) 
        self.rules = [bitfield(rR),bitfield(rG),bitfield(rB)]
        
    def loc(self, gen):
        x = gen*self.x+self.cenx
        y = gen*self.y+self.ceny
        return [x,y]
    
    def update(self, img):     
        f = self.loc(self.n)
        p = self.loc(self.n-1)
        p0 = [f[0]-self.x , f[1] ]
        p1 = [p[0], p[1]]
        p2 = [f[0], f[1]-self.y ]
        #img[ f[0], f[1] ] = applyrule(p0,p1,p2, img, self.rule)
        img[ f[0], f[1] ] = applycolors(p0,p1,p2, img, self.rules)
        self.n = self.n + 1
     
def bitfield(n):
    bn = bin(n)[2:]
    if len(bn) < 8:     #Need to pad with 0's 
        dif = 8 - len(bn)
        for i in range(dif):
            bn = '0' + bn
    return [int(digit) for digit in bn]

"""Returns BLACK/WHITE depending on the parents and rules"""
def applyrule( p0, p1, p2, img, r):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    #get ints of paretns
    v0 = 0 if img[p0[0], p0[1]] == BLACK else 1
    v1 = 0 if img[p1[0], p1[1]] == BLACK else 1
    v2 = 0 if img[p2[0], p2[1]] == BLACK else 1     
    intval = v0 + v1 * 2 + v2 * 4 
    return BLACK if r[intval] == 1 else WHITE

    #to make this do 3 channels seperatly just apply the rule to the channel
    
def applycolors(p0, p1, p2, img, rules):  
    return ( ar(p0, p1, p2, img, rules[0], 0), ar(p0, p1, p2, img, rules[1], 1), ar(p0, p1, p2, img, rules[2], 2) )
    
def ar(p0, p1, p2, img, r, c):
    ON, OFF = 255, 0
    #get ints of paretns
    v0 = 0 if img[p0[0], p0[1]][c] == OFF else 1
    v1 = 0 if img[p1[0], p1[1]][c] == OFF else 1
    v2 = 0 if img[p2[0], p2[1]][c] == OFF else 1     
    intval = v0 + v1 * 2 + v2 * 4 
    return ON if r[intval] == 1 else OFF
