
Instructions:

1) Download python 3.6 and some kind of text editor, best is to run in spyder. If you want both, download anaconda for windows and it takes care of all packages, interpreter and text editor and comes with spyder.

2) Extract the zip file.

3) Open config.yml in textpad or notepad.(I highly recommend Atom, it can read pretty much any file format. https://atom.io/ ) and set parameters: window_size: size of block along a single axis, overlap: overlapping if desired, slide_along parameter decides, in what direction the window will slide. Defaulted to EAST, can be changed to other directions.

4) Open feature_extraction and set working directory (line 30), put directory name where you extracted the zip file.

5) execute the python file, you will see data in each block getting printed.