# BitmapFun
Creating bitmaps in Python with cellular autonoma.  Can easily generate black and white or colored bitmaps using cellular autonama rules to determine pixel color.  A brief overview of elementary cellular autonoma can be found here http://mathworld.wolfram.com/ElementaryCellularAutomaton.html

Normal representations of CA's have the first generation as the top row, and each row below it is the next generation.  In addition to this normal representation, there is a fucntion to generate the bitmap by 'wrapping' the generations around a central point.  Additional corner cases are accounted for by defining the 'parents' in a consistent way.

Both the normal and wrapped generators can be either black and white or colored.  To create colored bitmaps, each color channel is given its own rule, and the initial cells are each given a random 0 or 255 in each color channel. 

####Admissions Portfolio - Topics Studied
* Elementary Cellular Automaton
* Python Basics

##Usage 
* Download cabmp.py and ca2d.py 
* From their directory you can import in the python module
  
    ````
      >>>import cabmp
      >>>cabmp.ca2dcolor(101,'colorCA',30,30,30,5)
   ````
* Or you can use it as a script.  
   
   ````
      ./cabmp.py -2dc 101 'colorCA' 30 30 30 5
   ````
* Run `./cabmp.py -x` to see examples/usage

##Examples
* Black/White 101x101 with random 9x9 square in middle to start - Rule 30
      - `>>>cabmp.ca2dbw(101, 'bw30', 30, 4)`
      
   ![Black White Sample](https://raw.githubusercontent.com/wpower12/BitmapFun/master/cabmp/src/bw30.bmp)

* Color 101, random 9x9 square in middle to start, - R, G, B all Rule 30
      - `>>>cabmp.ca2dcolor(101, 'color30', 30, 30, 30, 4)`
      
   ![Color Sample](https://raw.githubusercontent.com/wpower12/BitmapFun/master/cabmp/src/color30.bmp)

* Color 101x101, random 9x9 square to start, R:30, G:135, B:230
      - `>>>cabmp.ca2dcolor(101, 'color30', 30, 135, 230, 4)`
      
   ![Multi Rule Sample](https://raw.githubusercontent.com/wpower12/BitmapFun/master/cabmp/src/multicolor.bmp)
