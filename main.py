
# Gautam D
# 24 April 2020

from PIL import Image as Img
from PIL import ImageTk
from tkinter import *
from tkinter import messagebox as mbx
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter import scrolledtext as tkst
import tkoptiondialog as opd
from datetime import datetime
import os, json, uuid

instructions = """
Minecraft Pixel Art Maker
2.0

How To Use This App

-- In Brief --
Minecraft Pixel Art Maker uses the PIL library to process a given image by resizing, pixelating it and limiting
its colours to a given range that can be used in Minecraft maps. It then analyses the final image by identifying
a suitable minecraft block and coordinates for each pixel, and writing these in Minecraft functions ('.mcfunction' files)
using '/setblock' commands, that can be applied to any Minecraft world using behaviour packs and executed to build the
corresponding structure. When this area is mapped in the world, the blocks show up as pixels of the image on a map.
--------------

Step 1 : Selecting an Image
  Click on the 'Select' button to open the file dialog to choose the input image to process.
A number of input file formats are accepted (https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html)
but 'PNG' and 'JPG'/'JPEG' files work best.

Step 2 : Selecting a Colour Palette
  There are 3 options, which will decide the number of colours used. They are -
» Basic - This uses the 16 minecraft dye colours only, and builds a 2D array of blocks in minecraft.
The type of dyed block can be chosen through a pop-up dialogue on clocking the 'Basic' option, from amongst
'Concrete', 'Wool', 'Terracotta', 'Carpets' and 'Concrete powder'. The colours are 'white', 'orange', 'magenta',
'light_blue', 'yellow', 'lime', 'pink', 'gray', 'silver', 'cyan', 'purple', 'blue','brown', 'green', 'red' and 'black'
» Standard - This uses more blocks to get a range of 44 colours (the basic 16 + 28 more). No fluids and falling blocks are used.
The list of map colours at https://minecraft.gamepedia.com/Map_item_format is probably correct for Minecraft Java Edition,
but not for Windows 10 (Bedrock edition). Hence, the list used here is slightly different.
» Extended - This makes use of map shading to give a total of 3 x 44 = 132 colours by arranging the blocks in a 3D structure.
In a minecraft map, if a block is lower than the one directly north of it, it becomes one shade darker than normal and if it is
higher than the one directly north of it, one shade lighter. This is always true for a height difference of 2 or more blocks (for
only 1 block, Minecraft makes an alternating checkerboard pattern). A pop-up dialogue asks for the maximum height of the structure
when this option is chosen. The max height, by default, will never be allowed to exceed 128 levels due to Minecraft's world limit.

Step 3 : Entering a function name
  Enter a name for your work in the textbox in part 3. The name cannot contain spaces or special characters other than underscore,
since Minecraft will raise an error. The program checks that it is an identifier (https://en.wikipedia.org/wiki/Identifier_(computer_languages))
and prompts you if an invalid name is entered.

Step 4 : Choosing an art size
  You can select how many level 0 maps (the smallest zoom of maps in Minecraft) you want the final picture to cover in Minecraft.
There are 9 options ranging from 1x1 (1 map) to 3x4 (12 maps). It is normally easier to use smaller sizes as the number of commands
required for larger sizes is very big (196608 commands for the largest) and will increase the number of functions.
Minecraft has a recursive upper limit on 10,000 commands that can be executed from a single function call. Hence, the program
divides the image into chunks of size 64 x 128 (8192 commands each, covering exactly half of one level 0 map) and writes one function
for each chunk (resulting in 2-24 functions depending on the size chosen). These functions will need to be executed by the user individually.

Step 5 : View the processed image
  After selecting these 4 preferences, click on the 'Process Image' button on the right side of the app window to convert the image.
You will see a small thumbnail of the original and final images, and there will also be 3 buttons which display the original, resized
and (final) re-coloured images each in full-size, using the system's default photo viewer. The functions will be written using the last
fully converted image.

Step 6 : Choose a save location
  Click on the 'Select' button below the images to choose where to save the final '.mcfunction' files. Ensure that it is a valid address
and accessible on the computer.

Step 7 : Select a fill mode
  There are 2 options which can determine how Minecraft builds the structure. They are -
» Keep - Minecraft builds only those parts of the structure which do not coincide with an existing block in the world. Ensure beforehand
that the area you fill it in contains only air, or else parts of the structure overlapping with solid blocks will not be placed. This
is the default option.
» Destroy - Minecraft builds the entire structure, irrespective of what exists already. if there are overlapping solid blocks, they are
destroyed and drop any items as they would if normally broken. For a 3D structure, the entire volume of the cuboid from the bottom diagonal
corner to its opposite one is filled with air, not just replacing the single blocks in each vertical column that belong to the structure.

Step 8 : Configure final options
  Before writing the function files, there are 4 more settings provided. They are -
» Save processed image locally - If this is checked, the program will attempt to save the final converted image onto your computer
(the one displayed by the View Converted Image button), and a file dialog will open to select the save location and filename.
If you do not enter a file extension (e.g. - '.png'), it attempts to save it in the format of the originally selected image.
If the program detects an extension in the filename, it attempts to save the image in that format. This may cause an error for
certain image types, in which case it will display an error dialog and proceed to the next stage.
» Auto-generate a behaviour pack - To apply minecraft functions to a world, they need to be in a behavoiur pack (Read more here -
https://www.minecraft.net/en-us/addons,   and here - https://minecraft.gamepedia.com/Tutorials/Creating_behavior_packs)
If checked, minecraft creates a folder 'xxxxx_behavior_pack' where xxxxx is the name entered in part 3, and in it creates the 3
essential items - 'manifest.json', an icon image named 'pack_icon.png' and a 'functions' folder which will hold the function files.
The manifest.json file can be opened with any text editor and you can change the default pack name, description, id, version etc.
You can also replace the 'pack_icon.png' with another image named similarly. To use the behaviour pack, move it to Minecraft's
'behavior_pack' folder on your system, or, zip (compress) the folder, rename the '.zip' extension to '.mcpack' and double-click it to
launch Minecraft and import it.
» Link Function coordinates - The program uses relative coordinates ('tilde' ~ notation in Minecraft commands) to specify postitions
(See more here - https://minecraft.gamepedia.com/Commands#Tilde_and_caret_notation), so that the structure can be built in any location
in the world depending on the place the functions are executed from. The origin is the top-left corner (top left lower corner in 3D)
on the map (with the least X, Y, Z coordinates of all the values).
If this option is unchecked, all functions use the same origin and need to be run from the same place to make the picture continuous.
Else, each function's origin is at its top-left corner and the player will need to move to the other corner of one chunk before building
the next (the function itself attempts to teleport the player to the next location and places a command block there).
» Create sub-folder for functions - If selected, all the functions of an image will be placed in a sub-folder located in the
output directory or in the behavior pack's 'functions' folder, with the name given in step 3, and serially numbered 1, 2, ...
Else, each function will be created directly in the above location and named 'xxxxx_1.mcfunction', 'xxxxx_2.mcfunction', etc
where xxxxx is the name.

Finally, click on the 'Write Functions' button to create the functions and finish.
In addition to the functions to create the image, a 'clearblocks' function will be created, which can be used to replace all the blocks
generated by one function with air, making it easier to remove sections or the whole of the structure if required.
Apply a behaviour pack containing the files to Minecraft, and the picture is now in your world !

"""


class PixelFunction :

    BASICCOLOURS = [(255, 255, 255), (216, 127, 51), (178, 76, 216), (102, 153, 216),
     (229, 229, 51), (127, 204, 25), (242, 127, 165), (76, 76, 76),
     (153, 153, 153), (76, 127, 153), (127, 63, 178), (51, 76, 178),
     (102, 76, 51), (102, 127, 51), (153, 51, 51), (0,0,0)]
    COLOURNAMES = ['white', 'orange', 'magenta', 'light_blue',
                   'yellow', 'lime', 'pink', 'gray',
                   'silver', 'cyan', 'purple', 'blue',
                   'brown', 'green', 'red', 'black']

    javacolours = [(255, 255, 255),  (216, 127, 51),     (178, 76, 216),     (102, 153, 216),
                   (229, 229, 51),  (127, 204, 25),     (242, 127, 165),    (76, 76, 76),
                   (153, 153, 153), (76, 127, 153),     (127, 63, 178),     (51, 76, 178),
                   (102, 76, 51),   (102, 127, 51),     (153, 51, 51),      (0,0,0),
                   (127, 178, 56),  (247, 233, 163),    (199, 199, 199),    (160, 160, 255),
                   (167, 167, 167), (0, 124, 0),        (164, 168, 184),    (151, 109, 77),
                   (112, 112, 112), (143, 119, 72),     (255, 252, 245),    (250, 238, 77),
                   (92, 219, 213),  (74, 128, 255),     (0, 217, 58),       (129, 86, 49),
                   (112, 2, 0),     (209, 177, 161),    (159, 82, 36),      (149, 87, 108),
                   (112, 108, 138), (186, 133, 36),     (103, 117, 53),     (160, 77, 78),
                   (57, 41, 35),    (135, 107, 98),     (87, 92, 92),       (122, 73, 88),
                   (76, 62, 92),    (76, 50, 35),       (76, 82, 42),       (142, 60, 46),
                  (19,19,19)]
    javanames = ['concrete 0', 'concrete 1', 'concrete 2', 'concrete 3',
                'concrete 4', 'concrete 5', 'concrete 6', 'concrete 7',
                'concrete 8', 'concrete 9', 'concrete 10', 'concrete 11',
                'concrete 12', 'concrete 13', 'concrete 14', 'concrete 15',
                'slime 0',  'end_stone 0', 'web 0', 'blue_ice 0',
                'iron_block 0', 'leaves 0', 'clay 0', 'dirt 1',
                'stone 0', 'planks 0', 'quartz_block 0', 'gold_block 0',
                'diamond_block 0', 'lapis_block 0', 'emerald_block 0', 'podzol 0',
                'netherrack 0', 'stained_hardened_clay 0', 'stained_hardened_clay 1', 'stained_hardened_clay 2',
                'stained_hardened_clay 3', 'stained_hardened_clay 4', 'stained_hardened_clay 5', 'stained_hardened_clay 6',
                'stained_hardened_clay 7', 'stained_hardened_clay 8', 'stained_hardened_clay 9', 'stained_hardened_clay 10',
                'stained_hardened_clay 11','stained_hardened_clay 12','stained_hardened_clay 13','stained_hardened_clay 14',
                'stained_hardened_clay 15']
    
    ALLCOLOURS = [(196, 196, 196),  (166, 97, 39),      (136, 58, 166),     (78, 118, 166),
                   (176, 176, 39),  (97, 157, 19),      (186, 97, 127),     (58, 58, 58),
                   (118, 118, 118), (58, 97, 118),      (97, 48, 136),      (39, 58, 136),
                   (78, 58, 39),    (78, 97, 39),       (118, 39, 39),      (0,0,0),
                   (127, 178, 56),  (247, 233, 163),    (199, 199, 199),    (160, 160, 255),
                   (134, 134, 134), (123, 40, 40),      (134, 134, 147),    (151, 109, 77),
                   (90, 90, 90),    (115, 95, 58),      (220, 220, 220),    (250, 238, 77),
                   (92, 219, 213),  (74, 128, 255),     (0, 217, 58),       (115, 66, 40),
                   (90, 0, 0),      (86, 86, 86),       (0, 100, 0),        (205, 0, 0),
                   (61, 102, 123),  (82, 60, 40),       (82, 102, 41),      (90, 0, 0),
                   (142, 61, 173),  (205, 150, 75),     (50, 75, 20),       (42, 66, 42)]
    ALLNAMES = ['concrete 0', 'concrete 1', 'concrete 2', 'concrete 3',
                'concrete 4', 'concrete 5', 'concrete 6', 'concrete 7',
                'concrete 8', 'concrete 9', 'concrete 10', 'concrete 11',
                'concrete 12', 'concrete 13', 'concrete 14', 'concrete 15',
                'slime 0',  'end_stone 0', 'web 0', 'blue_ice 0',
                'iron_block 0', 'brick_block 0', 'clay 0', 'dirt 1',
                'stone 0', 'planks 0', 'quartz_block 0', 'gold_block 0',
                'diamond_block 0', 'lapis_block 0', 'emerald_block 0', 'redstone_lamp 0',
                'netherrack 0', 'sandstone 0', 'dried_kelp_block 0', 'redstone_block 0',
                'prismarine 0', 'soul_sand 0', 'end_portal_frame 0', 'netherbrick 0',
                'purpur_block 0', 'glowstone 0', 'leaves 12', 'leaves 13']

    DARKCLRS = [((rgb*180)//255 for rgb in c) for c in ALLCOLOURS]
    MEDCLRS = [((rgb*220)//255 for rgb in c) for c in ALLCOLOURS]
    EXTENDEDCOLOURS = ALLCOLOURS + MEDCLRS + DARKCLRS
    CSETLENGTH = len(ALLCOLOURS)

    BP, FP, EP = "BASIC", "FULL", "EXTENDED"
    materials = ('Concrete', 'Wool', 'Terracotta', 'Carpets', 'Concrete powder')
    mnames = {0:'concrete', 1:'wool', 2:'stained_hardened_clay', 3:'carpet', 4:'concrete_powder'}
    FKEEP, FDEST = "keep", "destroy"
    sizes = ((1,1),(2,1),(1,2),(2,2),(3,2),(2,3),(3,3),(4,3),(3,4))


    def __init__(self):
        """Make the 768-colour palettes and Launch the GUI window to begin creating pixel art"""

        # Create the palettes
        #mbx.showinfo('1', 'Analysing colors')
        self.BASICPALETTE, self.FULLPALETTE, self.EXTENDEDPALETTE = [], [], []
        for v in self.BASICCOLOURS :
            self.BASICPALETTE.extend(v)
        self.BASICPALETTE.extend( (768-len(self.BASICPALETTE))*[0] )
        for v in self.ALLCOLOURS :
            self.FULLPALETTE.extend(v)
        self.FULLPALETTE.extend( (768-len(self.FULLPALETTE))*[0] )
        for v in self.EXTENDEDCOLOURS :
            self.EXTENDEDPALETTE.extend(v)
        self.EXTENDEDPALETTE.extend( (768-len(self.EXTENDEDPALETTE))*[0] )
        

        # Variables
        self.PHOTO = None
        self.ORIGFILE = None
        self.ORIGEXT = None
        self.PALETTE = None
        self.FILLMODE = self.FKEEP
        self.OUTPUTDIR = None
        self.NAME = ""
        self.SIZE, self.NUM = (1,1), 2
        self.RESIZEDSMALL = None
        self.RESIZED, self.RESIZEDLARGE = None , None
        self.PROCESSED, self.PROCESSEDLARGE = None, None
        self.CHUNKS, self.FILES = [], []
        self.MANIFEST = {}
        
        
        # Create GUI
        self.dialogs = True
        self.main()
        self.root.mainloop()
        

    def main(self) :
        """Create the GUI"""
        
        self.root = Tk()
        self.root.title("Minecraft Pixel Art Maker")
        self.root.geometry('900x800')
        self.icon = "./resources/pixaicon.ico"
        self.root.iconbitmap(self.icon)

        #Files
        self.arrow1 = PhotoImage(file="./resources/furnaceloading1.png")
        self.arrow2 = PhotoImage(file="./resources/furnaceloading2.png")
        self.arrow3 = PhotoImage(file="./resources/furnaceloading3.png")
        self.arrow4 = PhotoImage(file="./resources/furnaceloading4.png")
        self.brokenimage = Img.open("./resources/brokenimage.gif")
        self.logo = Img.open("./resources/icon.png")
        self.logotk = ImageTk.PhotoImage(image=self.logo)
        self.exampleimage = PhotoImage(file="./resources/pixelartmaker.png")
        
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label='Create New', command=self._restart)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Process Image', command=self.processimg)
        self.filemenu.add_command(label='Write Functions', command=self.create, state=DISABLED)
        self.filemenu.add_separator()
        self.filemenu.add_checkbutton(label='Suppress Dialogs', command=self._toggledialogs)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Quit', command=self.root.destroy)
        self.menubar.add_cascade(label='File', menu=self.filemenu)
        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label='How To Use', command=self.howtouse)
        self.helpmenu.add_command(label='About', command=self.about)
        self.menubar.add_cascade(label='Help', menu=self.helpmenu)

        self.head = Label(self.root, text="Minecraft Pixel Art Maker", font=('Bahnschrift', 20, 'bold'))
        self.head.pack(padx=15, pady=15)
        self.h2 = Label(self.root, text="Bring any photograph into Minecraft by creating functions to build a structure\
 that can be captured as an image on a map",
                   font=('Bahnschrift', 12), fg='#dd5500')
        self.h2.pack(padx=15, pady=10)
        self.fmain = LabelFrame(self.root)
        self.fmain.pack(expand=YES, fill=BOTH, padx=10, pady=10)
        self.fleft = Frame(self.fmain)
        self.fleft.pack(side=LEFT, expand=YES, fill=BOTH)
        self.fright = Frame(self.fmain)
        self.fright.pack(side=RIGHT, expand=YES, fill=BOTH)
        
        self.l1 = Label(self.fleft, text="1. Original Image", font=('Bahnschrift', 12, 'bold'), anchor='w')
        self.l1.pack(side=TOP, padx=15, pady=15, ipadx=100, expand=YES, fill=X)
        self.f1 = Frame(self.fleft)
        self.f1.pack(side=TOP, ipadx=10, ipady=10, expand=YES, fill=X)
        self.l1a = Label(self.f1, text="Choose the image to process : ")
        self.l1a.grid(column=1, row=0, ipadx=10)
        self.l1b = Label(self.f1, text='[No Picture Selected]')
        self.l1b.grid(column=2, row=0)
        self.b1 = Button(self.f1, text="Select", height=1, width=8, bg='#ddddff', activebackground='#6622bb', command=self.openimage)
        self.b1.grid(column=0, row=0, padx=30, pady=5, ipadx=5)

        self.l2 = Label(self.fleft, text="2. Colour Palette", font=('Bahnschrift', 12, 'bold'), anchor='w')
        self.l2.pack(side=TOP, padx=15, pady=5, ipadx=100, expand=YES, fill=X)
        self.f2 = Frame(self.fleft)
        self.f2.pack(side=TOP, ipadx=10, ipady=10, expand=YES, fill=X)
        self.l2a = Label(self.f2, text="Choose a colour set : ")
        self.l2a.grid(column=0, row=0, ipadx=10)
        self.ptypevar = StringVar()
        self.r2a = Radiobutton(self.f2, text="Basic\nUse only the 16 colours of dyed wool/concrete/etc  \n(You can specify which material to use)",
                    disabledforeground='#444444', bg='#ddddff', activebackground='#6622bb', var=self.ptypevar, value=self.BP, command=self.setpalette)
        self.r2a.grid(column=1, row=0, padx=5, pady=5, ipadx=20)
        self.r2a.select()
        self.r2b = Radiobutton(self.f2, text="Standard\nUse all possible blocks for a range of upto 50 colours", disabledforeground='#444444',
                               bg='#ddddff', activebackground='#6622bb', var=self.ptypevar, value=self.FP, command = self.setpalette)
        self.r2b.grid(column=1, row=1, padx=5, pady=5, ipadx=20)
        self.r2c = Radiobutton(self.f2, text="Extended\nArrange all the blocks in 3D space instead of flat to \nget 2 more darker shades for each colour",
                    disabledforeground='#444444', bg='#ddddff', activebackground='#6622bb', var=self.ptypevar, value=self.EP, command = self.setpalette)
        self.r2c.grid(column=1, row=2, padx=5, pady=5, ipadx=20)
        #self.b2 = Button(self.f2, text="Change", height=1, width=8, bg='#ddddff', activebackground='#6622bb', command=self.resetpalette)

        self.l3 = Label(self.fleft, text="3. Name", font=('Bahnschrift', 12, 'bold'), anchor='w')
        self.l3.pack(side=TOP, padx=15, pady=5, ipadx=100, expand=YES, fill=X)
        self.f3 = Frame(self.fleft)
        self.f3.pack(side=TOP, ipadx=10, ipady=10, expand=YES, fill=X)
        self.l3a = Label(self.f3, text="Enter a name for the functions : \n(Use only alphanumeric characters and \
underscore (A-Z, a-z, 0-9, _)\n and do not specify any extension)", justify=LEFT)
        self.l3a.grid(column=0, row=0, ipadx=30)
        self.e3 = Entry(self.f3, width=48, bg='#ffffff')
        self.e3.grid(column=0, row=1, columnspan=2, ipadx=30)
        self.e3.bind('<FocusOut>', self._checkvalidname)

        self.l4 = Label(self.fleft, text="4. Size", font=('Bahnschrift', 12, 'bold'), anchor='w')
        self.l4.pack(side=TOP, padx=15, pady=5, ipadx=100, expand=YES, fill=X)
        self.f4 = Frame(self.fleft)
        self.f4.pack(side=TOP, ipadx=10, ipady=10, expand=YES, fill=X)
        self.l4a = Label(self.f4, text="Choose the number of 128x128 maps the final image must cover : \n(Horizontal × Vertical)")
        self.l4a.grid(column=0, row=0, columnspan=3, ipadx=30, pady=5)
        self.sizevar = StringVar()
        self.r4a = Radiobutton(self.f4, text='1x1', var=self.sizevar, value='1x1', command=self.setsize)
        self.r4a.grid(column=0, row=1, padx=2, pady=1)
        self.r4a.select()
        self.r4b = Radiobutton(self.f4, text='2x1', var=self.sizevar, value='2x1', command=self.setsize)
        self.r4b.grid(column=1, row=1, padx=2, pady=1)
        self.r4c = Radiobutton(self.f4, text='1x2', var=self.sizevar, value='1x2', command=self.setsize)
        self.r4c.grid(column=2, row=1, padx=2, pady=1)
        self.r4d = Radiobutton(self.f4, text='2x2', var=self.sizevar, value='2x2', command=self.setsize)
        self.r4d.grid(column=0, row=2, padx=2, pady=1)
        self.r4e = Radiobutton(self.f4, text='3x2', var=self.sizevar, value='3x2', command=self.setsize)
        self.r4e.grid(column=1, row=2, padx=2, pady=1)
        self.r4f = Radiobutton(self.f4, text='2x3', var=self.sizevar, value='2x3', command=self.setsize)
        self.r4f.grid(column=2, row=2, padx=2, pady=1)
        self.r4g = Radiobutton(self.f4, text='3x3', var=self.sizevar, value='3x3', command=self.setsize)
        self.r4g.grid(column=0, row=3, padx=2, pady=1)
        self.r4h = Radiobutton(self.f4, text='4x3', var=self.sizevar, value='4x3', command=self.setsize)
        self.r4h.grid(column=1, row=3, padx=2, pady=1)
        self.r4i = Radiobutton(self.f4, text='3x4', var=self.sizevar, value='3x4', command=self.setsize)
        self.r4i.grid(column=2, row=3, padx=2, pady=1)

        self.f5 = Frame(self.fright)
        self.f5.pack(expand=YES, fill=BOTH, ipadx=10, ipady=10)
        self.finbtn = Button(self.f5, text="Process Image", width=15, height=2, bg='#ddffbb', activebackground='#55cc11', font=('Calibri', 10, 'bold'),
                             command=self.processimg)
        self.finbtn.pack(anchor='center', padx=20, pady=50)

        self.f6 = Frame(self.fright)
        self.l6a = Label(self.f6)
        self.l6a.grid(column=0, row=0, padx=5, pady=5)
        self.l6b = Label(self.f6)
        self.l6b.grid(column=1, row=0, padx=5, pady=5)
        self.l6c = Label(self.f6)
        self.l6c.grid(column=2, row=0, padx=5, pady=5)
        self.f7 = Frame(self.fright)
        self.l7 = Label(self.f7, text="View the images in full size : ", font=('Calibri', 10, 'italic'))
        self.l7.grid(column=0, row=0, columnspan=3, padx=5, pady=5)
        self.b7a = Button(self.f7, text='Original\nImage', width=10, height=2, bg='#ddffff', activebackground='#77ffff', command=lambda:self._showimage(0))
        self.b7a.grid(column=0, row=1, padx=5, pady=5)
        self.b7b = Button(self.f7, text='Resized\nImage', width=10, height=2, bg='#ddffff', activebackground='#77ffff', command=lambda : self._showimage(1))
        self.b7b.grid(column=1, row=1, padx=5, pady=5)
        self.b7c = Button(self.f7, text='Converted\nImage', width=12, height=2, bg='#ddddff', activebackground='#6622bb', command=lambda : self._showimage(2))
        self.b7c.grid(column=2, row=1, padx=5, pady=5)

        self.l8 = Label(self.fright, text="5. Save Location", font=('Bahnschrift', 12, 'bold'), anchor='w')
        self.f8 = Frame(self.fright)
        self.l8a = Label(self.f8, text="Select where to write the functions : ")
        self.l8a.grid(column=1, row=0, ipadx=10)
        self.l8b = Label(self.f8, text='[No Folder Selected]')
        self.l8b.grid(column=1, row=1)
        self.b8 = Button(self.f8, text="Select", height=1, width=8, bg='#ddddff', activebackground='#6622bb', command=self.setoutdir)
        self.b8.grid(column=0, row=0, padx=30, pady=5, rowspan=2)

        self.l9 = Label(self.fright, text="6. Fill setting", font=('Bahnschrift', 12, 'bold'), anchor='w')
        self.f9 = Frame(self.fright)
        self.l9a = Label(self.f9, text="Select how to build the structure : ")
        self.l9a.grid(column=0, row=0, ipadx=10, rowspan=2)
        self.ftypevar = StringVar()
        self.r9a = Radiobutton(self.f9, text="Keep (Fill only air blocks)", bg='#ddddff', activebackground='#6622bb',
                         var=self.ftypevar, value=self.FKEEP, command=self.setfilltype)
        self.r9a.grid(column=1, row=0, padx=5, pady=5, ipadx=20)
        self.r9a.select()
        self.r9b = Radiobutton(self.f9, text="Destroy (Replace all blocks)", bg='#ddddff', activebackground='#6622bb',
                         var=self.ftypevar, value=self.FDEST, command = self.setfilltype)
        self.r9b.grid(column=1, row=1, padx=5, pady=5, ipadx=20)

        self.l10 = Label(self.fright, text="7. More Options", font=('Bahnschrift', 12, 'bold'), anchor='w')
        self.f10 = Frame(self.fright)
        self.saveimagevar = BooleanVar()
        self.genbpackvar = BooleanVar()
        self.linkposvar = BooleanVar()
        self.fnfoldervar = BooleanVar()
        self.c10a = Checkbutton(self.f10, text="Save processed image locally", justify=LEFT, var=self.saveimagevar)
        self.c10a.grid(column=0, row=0, padx=10, pady=5, sticky='w')
        self.c10b = Checkbutton(self.f10, text="Auto-generate a behavior pack", justify=LEFT, var=self.genbpackvar)
        self.c10b.grid(column=0, row=1, padx=10, pady=5, sticky='w')
        self.c10c = Checkbutton(self.f10, text="Link function coordinates", justify=LEFT, var=self.linkposvar)
        self.c10c.grid(column=0, row=2, padx=10, pady=5, sticky='w')
        self.c10c.invoke()
        self.c10d = Checkbutton(self.f10, text="Create sub-folder for functions", justify=LEFT, var=self.fnfoldervar)
        self.c10d.grid(column=0, row=3, padx=10, pady=5, sticky='w')
        self.c10d.invoke()

        self.f11 = Frame(self.fright)
        self.writebtn = Button(self.f11, text="Write Functions", width=15, height=1, bg='#ddffbb', activebackground='#55cc11', font=('Calibri', 10, 'bold'),
                               command=self.create)
        self.writebtn.pack(anchor='center', side=LEFT, padx=20, ipady=10)
        self.restartbtn = Button(self.f11, text="Create New Art", width=15, height=1, bg='#dddddd', activebackground='#aaaaaa', font=('Calibri', 10, 'bold'),
                               command=self._restart)


        
    def _hidewidgets2(self):
        self.f5.pack(expand=YES, fill=BOTH, ipadx=10, ipady=10)
        self.f6.pack_forget()
        self.f7.pack_forget()
        self.l8.pack_forget()
        self.f8.pack_forget()
        self.l9.pack_forget()
        self.f9.pack_forget()
        self.l10.pack_forget()
        self.f10.pack_forget()
        self.f11.pack_forget()

    def _disableall(self):
        self.b1.config(state=DISABLED)
        self.r2a.config(state=DISABLED)
        self.r2b.config(state=DISABLED)
        self.r2c.config(state=DISABLED)
        self.e3.config(state=DISABLED)
        self.r4a.config(state=DISABLED)
        self.r4b.config(state=DISABLED)
        self.r4c.config(state=DISABLED)
        self.r4d.config(state=DISABLED)
        self.r4e.config(state=DISABLED)
        self.r4f.config(state=DISABLED)
        self.r4g.config(state=DISABLED)
        self.r4h.config(state=DISABLED)
        self.r4i.config(state=DISABLED)
        self.b8.config(state=DISABLED)
        self.r9a.config(state=DISABLED)
        self.r9b.config(state=DISABLED)
        self.c10a.config(state=DISABLED)
        self.c10b.config(state=DISABLED)
        self.writebtn.pack_forget()

    def _toggledialogs(self):
        self.dialogs = not self.dialogs
        

    def openimage(self):
        """Identify the original image file for processing"""
        
        self._hidewidgets2()
        try :
            fileaddr = os.path.normpath(fd.askopenfilename(title='Select image',
                    filetypes=[('All Images',('*.png','*.jpg','*.jpeg','*.dng','*.bmp','*.gif','*.tiff','*.tif')),
                       ("PNG files",'*.png'),("JPEG files",('*.jpg','*.jpeg')),("DNG files",'*.dng'),
                       ("BMP files",'*.bmp'),("GIF files",'*.gif'),("TIFF files",('*.tiff','*.tif')),
                       ("all files",'*.*')]))
            if not os.path.isfile(fileaddr):
                mbx.showerror('Invalid File', "The given image address does not exist.")
                return
            fpath, file = os.path.split(fileaddr)
            fname, fext = os.path.splitext(file)
            self.ORIGFILE = fileaddr
            self.ORIGEXT = fext
            self.PHOTO = Img.open(fileaddr)
            if self.dialogs :
                mbx.showinfo('Input Image', "Selected {} as the image.".format(fileaddr))
            self.l1b.config(text = file, font=('Calibri', 10, 'bold'))
        except :
            retry = mbx.askyesno('Error','Failed to load file. Try again ?')
            if retry :
                self.openimage()
            else :
                return


    def setpalette(self):
        """Set the chosen palette and additional information depending on the choice"""
        self._hidewidgets2()
        p = self.ptypevar.get()
        self.r2a.config(state=DISABLED)
        self.r2b.config(state=DISABLED)
        self.r2c.config(state=DISABLED)
        if p == self.BP :
            bloc = opd.askradio(self.materials, 'Select Material', "Choose material to build image out of in minecraft : ", parent=self.root)
            if bloc is None :
                bloc = 0
            self.PALETTE = (self.BP, self.mnames[bloc])
        elif p == self.EP :
            try :
                maxheight = abs(int(sd.askinteger('Maximum Height', "Enter the maximum height of the 3D block structure :\n\n\
Enter 0 to place no limit on maximum height (Note that the max height will not exceed 128 in any case)\n\
Giving a value from 1-127 may force some pixels on the final map to deviate from their calculated shades slightly", parent=self.root)))
                if maxheight < 1 or maxheight > 128:
                    maxheight = 128
            except TypeError :
                maxheight = 128
            self.PALETTE = (self.EP, maxheight)
        else :
            self.PALETTE = (self.FP, None)
        if self.dialogs :
            mbx.showinfo('Palette', "Set the colour palette to {}".format(self.PALETTE[0]))
        #self.b2.grid(column=0, row=1, padx=30, pady=5, rowspan=2)
        self.r2a.config(state=NORMAL)
        self.r2b.config(state=NORMAL)
        self.r2c.config(state=NORMAL)


    def setsize(self):
        """Configures the map size variable and divides the area into 64x128 modules"""
        self._hidewidgets2()
        s = self.sizevar.get()
        self.NUM = 2*int(s[0])*int(s[2])
        if self.NUM >= 8 :
            if self.dialogs :
                mbx.showwarning('Warning', "The selected image size is very large and may cause lag in-game or missing chunks \
due to far corners not loading or loading very slowly. Consider disabling the 'Link function coordinates' option before finishing.")
        self.SIZE = (int(s[0]), int(s[2]))
        # Break the total area into vertical 64x128 rectangles, one function per chunk
        self.CHUNKS = [(64*x, 128*z) for z in range(self.SIZE[1]) for x in range(2*self.SIZE[0])]
        if self.dialogs :
            mbx.showinfo('Map size', "Set the picture size to {}.\nThis will cover an area of {}x{} blocks and generate {} functions.".format(
                self.SIZE, 128*self.SIZE[0], 128*self.SIZE[1], self.NUM))

    def setfilltype(self):
        """Set how to fill blocks in the function"""
        self.FILLMODE = self.ftypevar.get()
        if self.dialogs :
            mbx.showinfo('Fill mode selected', "The fill mode is set to '{}'".format(self.FILLMODE))

    def _checkvalidname(self, event):
        """Verifies that the entered name can be used as a function name"""
        name = self.e3.get()
        allowed = [c for c in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890_"]
        if len(name) == 0:
            mbx.showerror('No Name', "Please enter a name for the functions")
            self.e3.focus_set()
            return False
        if name is not None and all([char in allowed for char in name]) :
            self.NAME = name
            return True
        else :
            mbx.showerror('Invalid Name', "The given name is invalid !\n It must contain only alphanumeric characters and underscore (A-Z, a-z, 0-9, _)")
            self.e3.delete(0, END)
            self.e3.focus_set()
            return False



    def processimg(self):
        """Resize the given image and convert using the specified palette.
            Display all the options to view it in the window"""
        
        if self.PHOTO is None :
            mbx.showwarning('No Picture', "Please select an input image !")
            return
        if self.PALETTE is None :
            mbx.showwarning('No Palette', "Please select a colour palette !")
            return
        if self.SIZE not in self.sizes or self.CHUNKS == []:
            mbx.showwarning('Size Undefined', "Please select an image size !")
            return
        
        # Resize first, then quantize
        try :            
            self.RESIZED = self.PHOTO.resize((128*self.SIZE[0],128*self.SIZE[1]), Img.NEAREST)
            if self.SIZE[0]*self.SIZE[1] <= 6 :
                self.RESIZEDLARGE = self.RESIZED.resize((1024*self.SIZE[0],1024*self.SIZE[1]), Img.NEAREST)
            else :
                self.RESIZEDLARGE = self.RESIZED.resize((512*self.SIZE[0],512*self.SIZE[1]), Img.NEAREST)

            if self.PALETTE[0] == self.BP :
                palet = self.BASICPALETTE
            elif self.PALETTE[0] == self.FP :
                palet = self.FULLPALETTE
            elif self.PALETTE[0] == self.EP :
                palet = self.EXTENDEDPALETTE
            self.blankpaletteimg = Img.new('P', (1,1))
            self.blankpaletteimg.putpalette(palet)
            
            try :
                self.PROCESSED = self.RESIZED.quantize(palette = self.blankpaletteimg)
            except ValueError :
                prgb = self.RESIZED.convert('RGB')
                self.PROCESSED = prgb.quantize(palette = self.blankpaletteimg)

            if self.SIZE[0]*self.SIZE[1] <= 6 :
                self.PROCESSEDLARGE = self.PROCESSED.resize((1024*self.SIZE[0],1024*self.SIZE[1]), Img.NEAREST)
            else :
                self.PROCESSEDLARGE = self.PROCESSED.resize((512*self.SIZE[0],512*self.SIZE[1]), Img.NEAREST)
            try :
                w, h = self.PHOTO.size
                if w/h >= 1 :
                    self.dispimg1 = ImageTk.PhotoImage(image = self.PHOTO.resize((128, int(128*h/w)), Img.NEAREST))
                else :
                    self.dispimg1 = ImageTk.PhotoImage(image = self.PHOTO.resize((int(128*w/h), 128), Img.NEAREST))
                w, h = self.PROCESSED.size
                if w/h >= 1 :
                    self.dispimg2 = ImageTk.PhotoImage(image = self.PROCESSED.resize((128, int(128*h/w)), Img.NEAREST))
                else :
                    self.dispimg2 = ImageTk.PhotoImage(image = self.PROCESSED.resize((int(128*w/h), 128), Img.NEAREST))
            except :
                pass
        except :
            mbx.showerror('Error', "An unknown processing error occurred.")
            return

        self.f5.pack_forget()
        self.f6.pack()
        self.f6.after(200, self._animateimages, 1)

    def _animateimages(self, stage=1):
        """Animates a loading arrow before displaying the images in the tk window"""
        if stage == 1 :
            self.l6a.config(image = self.dispimg1)
            self.l6a.image = self.dispimg1
            self.l6b.config(image = self.arrow1)
            self.l6b.image = self.arrow1
            self.f6.after(200, self._animateimages, 2)
        elif stage == 2 :
            self.l6b.config(image = self.arrow2)
            self.l6b.image = self.arrow2
            self.f6.after(200, self._animateimages, 3)
        elif stage == 3 :
            self.l6b.config(image = self.arrow3)
            self.l6b.image = self.arrow3
            self.f6.after(200, self._animateimages, 4)
        elif stage == 4 :
            self.l6b.config(image = self.arrow4)
            self.l6b.image = self.arrow4
            self.f6.after(200, self._animateimages, 5)
        elif stage == 5 :
            self.l6c.config(image = self.dispimg2)         
            self.l6c.image = self.dispimg2
            self.l6a.grid()
            self.f7.pack()
            self.l8.pack(side=TOP, padx=15, pady=15, ipadx=100, expand=YES, fill=X)
            self.f8.pack(side=TOP, ipadx=10, ipady=10, expand=YES, fill=X)
            self.l9.pack(side=TOP, padx=15, pady=15, ipadx=100, expand=YES, fill=X)
            self.f9.pack(side=TOP, ipadx=10, ipady=10, expand=YES, fill=X)
            self.l10.pack(side=TOP, padx=15, pady=15, ipadx=100, expand=YES, fill=X)
            self.f10.pack(side=TOP, ipadx=10, ipady=10, expand=YES, fill=X)
            self.f11.pack(ipadx=10, ipady=20, expand=YES, fill=X)
            self.root.geometry('1000x900')
            self.filemenu.entryconfig('Write Functions', state=NORMAL)

    def _showimage(self, n):
        """Display one of the images in the default application"""
        try :
            if n == 0 :
                self.PHOTO.show()
            elif n == 1 :
                self.RESIZEDLARGE.show()
            elif n == 2 :
                self.PROCESSEDLARGE.show()
        except :
            mbx.showerror('Error', "There was an unknown error while displaying the image")


    def setoutdir(self):
        """Prompt user to choose a location to save functions in and create the file objects there"""
        
        try :
            saddr = fd.askdirectory(title='Save Function In', mustexist=True)
            saddr = os.path.normpath(saddr)
            if saddr == '':
                return
            self.OUTPUTDIR = saddr
        except :
            mbx.showerror('Error', "Failed to access the specified directory")
            return
        if self.dialogs :
            mbx.showinfo('Save', "Selected {} as the output folder".format(self.OUTPUTDIR))
        self.b8.config(text="Change")
        self.l8b.config(text = saddr, font=('Calibri', 10, 'bold'))



    def create(self):
        """Finish the process by analysing all the image data and writing the minecraft functions"""

        if not self._checkvalidname(None):
            return
        if self.OUTPUTDIR is None or not os.path.exists(self.OUTPUTDIR) :
            mbx.showerror('Invalid Directory', "The specified output folder does not exist !")
            return
        if self.FILLMODE != self.FKEEP and self.FILLMODE != self.FDEST :
            mbx.showerror('Unknown fill mode', "No command fill mode (keep or destroy) has been selected !")
            return        
        if self.CHUNKS == [] :
            mbx.showerror('Unknown size', "Please re-select the Image size option !")
            return
        if self.PROCESSED is None :
            mbx.showerror('Unprocessed photo', 'The image has not been processed yet ! Please finish processing first.')

        # --- Save image Locally ---
        savelocal = self.saveimagevar.get()
        if savelocal :
            try :
                out = fd.asksaveasfilename(title='Save Processed Image', initialdir=self.OUTPUTDIR, filetypes=(
                            ('All Images',('*.png','*.jpg','*.jpeg','*.dng','*.bmp','*.gif','*.tiff','*.tif')),
                            ("all files",'*.*')))
                if out :
                    try :
                        if os.path.splitext(out)[1] == '' :
                            # Extension not explicitly specified -> Use original image's
                            out1 = os.path.abspath(out + self.ORIGEXT)
                            self.PROCESSEDLARGE.save(out1)
                        else :
                            self.PROCESSEDLARGE.save(os.path.abspath(out))
                    except OSError :
                        self.PROCESSEDLARGE.convert('RGB').save(os.path.normpath(out))
                    if self.dialogs :
                        mbx.showinfo('Saved Image', "Successfully saved '{}' !".format(out))
            except :
                rty = mbx.askyesno('6', "Failed to save image file. This may be due to not specifying any extension ('.png,\
'.jpg, '.gif', etc) or using a different extension from the original image's. Continue to write functions anyway ?")
                if not rty :
                    return

        # --- Create behaviour pack ---
        makepack = self.genbpackvar.get()
        if makepack :
            try :
                self.MANIFEST = {
                    "format_version" : 2,
                    "header" : {
                        "name" : "{} Pixel Art".format(self.NAME),
                        "description" : datetime.now().strftime("Created with Minecraft Pixel Art Maker %d/%m/%Y %H:%M"),
                        "uuid" : str(uuid.uuid4()),
                        "version" : (1, 0, 0),
                        "min_engine_version" : (1, 14, 0)
                        },
                    "modules" : [
                        {
                            "description" : "Contains {} functions with setblock commands.\n Replace this pack's name, \
    description, uuids, version and minimum minecraft version with your own if preferred".format(len(self.CHUNKS)),
                            "type" : "data",
                            "uuid" : str(uuid.uuid4()),
                            "version" : (1, 0, 0)
                        }
                                ]
                    }
                os.chdir(self.OUTPUTDIR)
                folder = os.path.abspath(os.path.join('.', "{}_behaviour_pack".format(self.NAME)))
                try :
                    os.mkdir(folder)
                except FileExistsError :
                    mbx.showinfo('Existing folder', '{} already exists. Data will be added to this folder.'.format(folder))
                os.chdir(folder)
                with open('manifest.json', 'w') as m :
                    json.dump(self.MANIFEST, m, indent=4)
                try :
                    iconname = os.path.abspath(os.path.join('.', "pack_icon.png"))
                    self.PROCESSED.save(iconname)
                except :
                    try :
                        self.PROCESSED.convert('RGB').save(iconname)
                    except :
                        try :
                            self.logo.save(iconname)
                        except :
                            icon = open('pack_icon.png', 'wb')
                            icon.close()
                folder2 = os.path.abspath(os.path.join('.', "functions"))
                try :
                    os.mkdir(folder2)
                except FileExistsError :
                    mbx.showinfo('Existing folder', '{} already exists. Data will be added to this folder.'.format(folder2))
                os.chdir(folder2)
            except :
                rty = mbx.askyesno('6', "Failed create a behaviour pack. Continue to write functions anyway ?")
                if not rty :
                    return
        else :
            os.chdir(self.OUTPUTDIR)
    
        self.subfolder = self.fnfoldervar.get()
        if self.subfolder :
            try :
                os.mkdir(os.path.join('.', self.NAME))
            except FileExistsError :
                mbx.showinfo('Existing folder', '{} already exists. Data will be added to this folder.'.format(
                    os.path.abspath(os.path.join('.', self.NAME))))
            os.chdir(os.path.join('.', self.NAME))

        #self._disableall()
        # --- Analyse image ---
        self.pixelmap = self.PROCESSED.load()
        self.width, self.height = self.PROCESSED.size
        self.tp = not self.linkposvar.get()
        
        if self.PALETTE[0] == self.EP:
            # Generate array of block heights for 3D
            self.hmax = self.PALETTE[1]
            self.ymap = []
            for x in range(self.width) :
                try :
                    yrow = [1]
                    h_error = 0
                    for z in range(self.height) :
                        cid = self.pixelmap[x,z]
                        h = cid // self.CSETLENGTH
                        lasty = yrow[-1]
                        if h == 2 :
                            if h_error > 0 :
                                while h_error > 0:
                                    yrow[-h_error] -= 2*h_error
                                    h_error -= 1
                            # Dark colour -> make the block lower than the one north of it
                            # --> or make everything before it higher, if required and possible
                            if lasty-2 < 1 :
                                h_error -= 1
                                yrow.append(lasty)
                            else :
                                yrow.append(lasty-2)
                        elif h == 0 :
                            if h_error < 0 :
                                while h_error < 0:
                                    yrow[h_error] -= 2*h_error
                                    h_error += 1
                            # Bright colour -> make the block higher than the one north of it, if possible
                            if self.hmax is None or lasty+2 <= self.hmax :
                                yrow.append(lasty+2)
                            else :
                                yrow.append(lasty)
                                h_error += 1
                        else :
                            while h_error > 0:
                                yrow[-h_error] -= 2*h_error
                                h_error -= 1
                            while h_error < 0:
                                yrow[h_error] -= 2*h_error
                                h_error += 1
                            # Regular/medium colour -> same height as the block north of it
                            yrow.append(lasty)
                        # Also correct height errors due to maximum height limit if approaching the end or error > limit
                        if abs(h_error) >= self.hmax//2 or len(yrow) >= self.height-1 :
                            while h_error > 0:
                                yrow[-h_error] -= 2*h_error
                                h_error -= 1
                            while h_error < 0:
                                yrow[h_error] -= 2*h_error
                                h_error += 1
                    self.ymap.append(yrow)
                except :
                    mbx.showerror("An error occurred while creating the 3D height map.\nContinuing anyway")
                    continue

        # --- Begin Writing functions ---
        self.fn = 0
        for i in range(len(self.CHUNKS)) :
            try :
                zone = self.CHUNKS[i]
                x0, z0 = zone # Top left corner coordinates
                self.fn += 1
                if self.subfolder :
                    fun = open('{}.mcfunction'.format(self.fn), 'w')
                else :
                    fun = open('{}_{}.mcfunction'.format(self.NAME, self.fn), 'w')
                self.FILES.append(fun)
                note = "section {}/{} of commands of function group {} (x={}-{}, z={}-{})".format(
                        self.fn, self.NUM, self.NAME, x0, x0+63, z0, z0+127)
                fun.write("# {}\nsay Running {}\n".format(note, note))
                if self.FILLMODE == self.FKEEP :
                    fmode = self.FKEEP
                else :
                    # Fill area/volume to be built with air
                    if self.PALETTE[0] == self.EP :
                        if self.tp :
                            for i in range(0, 64, 2):
                                fun.write("fill ~{} ~1 ~ ~{} ~{} ~127 air 0 replace\n".format(i, i+1, self.hmax))
                        else :
                            for i in range(x0, x0+64, 2):
                                fun.write("fill ~{} ~1 ~ ~{} ~{} ~127 air 0 replace\n".format(i, i+1, self.hmax))
                    else :
                        if self.tp :
                            fun.write("fill ~ ~1 ~ ~63 ~1 ~127 air 0 destroy\n")
                        else :
                            fun.write("fill ~{} ~1 ~{} ~{} ~1 ~{} air 0 destroy\n".format(x0, z0, x0+63, z0+63))
                    fmode = ""
                
                if self.PALETTE[0] == 'BASIC' :
                    mat = self.PALETTE[1]
                    for x in range(x0, x0+64) :
                        for z in range(z0, z0+128) :
                            cid = self.pixelmap[x,z]
                            if not self.tp :
                                sx = '' if x == 0 else str(x)
                                sz = '' if z == 0 else str(z)
                            else :
                                sx = '' if x == x0 else str(x - x0)
                                sz = '' if z == z0 else str(z - z0)
                            command = "setblock ~{} ~1 ~{} {} {} {}".format(sx, sz, mat, cid, fmode)
                            fun.write(command)
                            fun.write('\n')

                elif self.PALETTE[0] == 'FULL' :
                    for x in range(x0, x0+64) :
                        for z in range(z0, z0+128) :
                            cid = self.pixelmap[x,z]
                            block = self.ALLNAMES[cid]
                            if not self.tp :
                                sx = '' if x == 0 else str(x)
                                sz = '' if z == 0 else str(z)
                            else :
                                sx = '' if x == x0 else str(x - x0)
                                sz = '' if z == z0 else str(z - z0)
                            command = "setblock ~{} ~1 ~{} {} {}".format(sx, sz, block, fmode)
                            fun.write(command)
                            fun.write('\n')

                elif self.PALETTE[0] == 'EXTENDED' :
                    for x in range(x0, x0+64) :
                        for z in range(z0, z0+128) :
                            cid = self.pixelmap[x,z] % self.CSETLENGTH
                            block = self.ALLNAMES[cid]
                            if not self.tp :
                                sx = '' if x == 0 else str(x)
                                sz = '' if z == 0 else str(z)
                            else :
                                sx = '' if x == x0 else str(x - x0)
                                sz = '' if z == z0 else str(z - z0)
                            sy = str(self.ymap[x][z])
                            command = "setblock ~{} ~{} ~{} {} {}".format(sx, sy, sz, block, fmode)
                            fun.write(command)
                            fun.write('\n')

                if self.tp :
                    try :
                        nextzone = self.CHUNKS[i+1]
                        dx, dz = nextzone[0] - x0, nextzone[1] - z0
                        dx = '' if dx == 0 else str(dx)
                        dz = '' if dz == 0 else str(dz)
                        fun.write("teleport @p ~{} ~ ~{}\n".format(dx, dz))
                        fun.write("setblock ~{} ~ ~{} command_block\n".format(dx, dz))
                    except IndexError :
                        pass
            except :
                mbx.showwarning('Error', "An error occurred while writing function {}. It may be incomplete - continuing anyway".format(self.fn))
                continue
            finally :
                fun.close()
        try :
            # Write a function to clear any 64x128 area of blocks
            with open('clearblocks.mcfunction', 'w') as cf :
                cf.write("# Clear all blocks in one 64x128 zone used by the pack maker\n")
                cf.write("say Clearing all blocks in this 64x128 zone...\n")
                if self.PALETTE[0] == 'EXTENDED' :
                    for i in range(0, 64, 2):
                        cf.write("fill ~{} ~1 ~ ~{} ~{} ~127 air 0 replace\n".format(i, i+1, self.hmax))
                else :
                    cf.write("fill ~ ~1 ~ ~63 ~1 ~127 air 0 replace\n")
        except :
            pass

        mbx.showinfo('Complete', "The program has finished !\n\n1. Add the generated functions to a behaviour pack (if not created already) \
and apply it to a minecraft world. \n2. Open the world, run '/reload', and stand in the top-left corner block of any level 0 map (smallest size). \
\n3. Execute all of them in order using the '/function' command and then map the entire covered area.\nYour picture is now in minecraft !")
        self.restartbtn.pack(anchor='center', side=RIGHT, padx=20, ipady=10)
    

    def _restart(self):
        """Create a new instance of the app"""
        self.root.destroy()
        self.__init__()

    def about(self):
        """Show details"""
        mbx.showinfo('About', "Minecraft Pixel Art Maker\nVersion 2.0\n\nBuilt by Gautam D\n23-27 Apr 2020\n\n\
Written in Python 3.7.2\nUsing the Pillow (PIL) library ver. 5.4.1")

    def howtouse(self):
        """Displays the instructions"""
        global instructions
        self.instr = Toplevel(self.root)
        self.instr.title('How to Use')
        self.instr.iconbitmap(self.icon)
        self.text = tkst.ScrolledText(self.instr, width=120, height=40, wrap='word', bg='#eeeeee', font=('Bahnschrift', 10),
                                      spacing2=3, padx=20, relief=FLAT)
        self.text.insert(INSERT, instructions)
        self.text.image_create('1.end', image=self.logotk, pady=20)
        self.text.tag_add('margin', '1.0', 'end')
        self.text.tag_config('margin', lmargin2=50, rmargin=5)
        self.text.tag_add('title1', '1.0', '3.end')
        self.text.tag_config('title1', font=('Bahnschrift', 18, 'bold'), justify=CENTER)
        self.text.tag_add('title2', '4.0', '5.end')
        self.text.tag_config('title2', font=('Bahnschrift', 15, 'bold'), justify=CENTER)
        self.text.tag_add('bloo', '7.0', '13.end')
        self.text.tag_config('bloo', foreground='#aa5522', justify=CENTER)
        self.text.tag_config('subbtitle', font=('Bahnschrift', 11, 'bold'))
        self.text.tag_add('subbtitle', '15.0', '15.end')        
        self.text.tag_add('subbtitle', '20.0', '20.end')
        self.text.tag_add('subbtitle', '35.0', '35.end')
        self.text.tag_add('subbtitle', '40.0', '40.end')
        self.text.tag_add('subbtitle', '48.0', '48.end')
        self.text.tag_add('subbtitle', '54.0', '54.end')
        self.text.tag_add('subbtitle', '58.0', '58.end')
        self.text.tag_add('subbtitle', '67.0', '67.end')
        self.text.tag_config('bullet', font=('Bahnschrift', 15, 'bold'), foreground='#00aa00')
        self.text.tag_add('bullet', '22.0', '22.1')
        self.text.tag_add('bullet', '26.0', '26.1')
        self.text.tag_add('bullet', '29.0', '29.1')
        self.text.tag_add('bullet', '60.0', '60.1')
        self.text.tag_add('bullet', '63.0', '63.1')
        self.text.tag_add('bullet', '69.0', '69.1')
        self.text.tag_add('bullet', '74.0', '74.1')
        self.text.tag_add('bullet', '82.0', '82.1')
        self.text.tag_add('bullet', '89.0', '89.1')
        self.text.tag_config('link', font=('Bahnschrift', 10, 'underline'), foreground='#0000ff')
        self.text.tag_add('link', '17.45', '17.145')
        self.text.tag_add('link', '27.27', '27.74')
        self.text.tag_add('link', '37.82', '37.153')
        self.text.tag_add('link', '75.0', '75.38')
        self.text.tag_add('link', '75.53', '75.118')
        self.text.tag_add('link', '83.17', '83.82')
        self.text.image_create(END, image=self.exampleimage)
        self.text.config(state=DISABLED)
        self.text.pack(fill=BOTH, expand=YES, padx=5, pady=5)


if __name__ == '__main__' :
    
    p = PixelFunction()

#_______________________________________________________________________________________________________________________
        
