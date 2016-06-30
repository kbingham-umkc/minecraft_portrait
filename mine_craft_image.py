########################################################################
##
## CS 101
## Program # : Color Reducer
## Name      : Instructor
## Email     : klb337@umkc.edu
##
## PROBLEM : Read a PPM Image and reduce colors to the closest of 16 minecraft colors
##
## ALGORITHM : 
## 
## ERROR HANDLING:
##      Invalid Files are caught and asked for a new filename.
##
## OTHER COMMENTS:
##      Any special comments
##
########################################################################

from mcpi.minecraft import Minecraft
from PIL import Image
mc = Minecraft.create()


MENU = """\n\n   Color Reduction

1. Convert Image
Q. Quit

==> """
MENU_CHOICES = ["1", "Q"]

COLOR_CHOICES = [(  0,   0,   0), (255,   0,   0), (  0, 255,   0),
                 (  0,   0, 255), (255, 255, 255)]

COLOR_CHOICES = [(  221,   221,   221), (219, 125, 62), ( 179, 80, 188),
                 (  107, 138, 201), (177, 166, 39), (65, 174, 56),
                 (208, 132, 153), (64, 64, 64), (154, 161, 161), (46, 110, 137),
                 (126, 61, 181), (46, 56, 141), (79, 50, 31), (53, 70, 27),
                 (150, 52, 48), (25, 22, 22)]


def get_choice(prompt : str, valid_choices : list) -> str:
    """ Prompts the user with the string prompt and returns only valid input choice
    :param prompt:str          - Output that is displayed to the user.  Usually a menu or prompt 
    :param valid_choices: list - List of strings of valid input choices.  If users choice is not
                                 in this list then the user will be prompted again.  Should be in
                                 upper case
    :return:str                - Returns the users choice.  It will only be one of the strings in the list of
                                 valid_choices
    """

    while True:
        choice = input(prompt).upper()

        if choice in valid_choices:
            return choice

        print("You must enter a valid choice.  ({})".format(",".join(valid_choices)))


def get_file(prompt : str, file_mode : str = "r"):
    """ Returns the filehandle to a file the user specified.  
    :param prompt:str          - Output that is displayed to the user.  
    :param file_mode:str       - Valid file mode for the file to be opened in.  r, w, a, rb, wb, ab, etc.
    :return:str                - Returns a valid file handle
    """
    while True:
        try:
            return Image.open(input(prompt))
        except FileNotFoundError:
            print("The file you specified does not exist.  Please enter a valid filename")
        except IOError:
            print("There was an IO Error opening your file.  Please enter a valid filename")

def valid_ppm(ppms : list) -> bool:
    """ Returns whether the file is a valid ppm 
    :param ppms:list           - List of strings.  Each string is a line from the ppm file.
    :return:tuple (bool, str, int, int, int)
                               - Returns True if this is a valid PPM file, False otherwise
                                 If it returns True, then the rest of the tuple is
                                    Header ( P3 ), Width, Height, ColorDepth
    """
    file_type = ppms[0]
    if file_type != "P3":
        print("The files first line should be P3")
        return False, "", 0, 0, 0

    resolution = ppms[1]
    try:
        width, height = resolution.split()
        width = int(width)
        height = int(height)
    except ValueError:
        print("The files resolution must be an integer.")
        return False, "", 0, 0, 0
    
    try:
        color_depth = int(ppms[2])
        if color_depth != 255:
            print("The color depth must be 255")
            return False, "", 0, 0, 0
        
    except ValueError:
        print("The color depth must be 255")
        return False, "", 0, 0, 0

    return True, file_type, width, height, color_depth  #All previous tests passed.  It's a valid ppm


def get_pixels(ppm_list : list) -> list:
    """ Returns a list of lists of red, green and blue pixels from the ppm file.  
    :param ppm_list:list       - Output that is displayed to the user.  
    :return:list               - List of colors of the file, so it is a list of lists.  [ [255, 0, 0], [0, 0, 0], ... ]
                                 The ppm file may not have a separate line for each color value. It can actually be separated by spaces.
    """

    ppms = []

    current_pixel = []
    for line in ppm_list[3:]:
        responses = line.split(" ")
        for value in responses:
            current_pixel.append(int(value))
            if len(current_pixel) == 3:
                ppms.append(current_pixel)
                current_pixel = []
    if len(current_pixel) == 3:
        ppms.append(current_pixel)
    return ppms

def get_distance(point1 : iter, point2 : iter) -> float:
    """ Returns distance from one point to another.  Each point is an iterable of dimensions.  
    :param point1:iter         - Collection of scalar values for the point.  This can be in any range of dimensions as long as
                                 both points have the same length.
    :param point2:iter         - Collection of scalar values for the point. 
    :return:float              - Returns a valid file handle
    """

    sum_value = 0
    for dimension in range(len(point1)):
        sum_value += (point1[dimension] - point2[dimension]) ** 2
    return sum_value ** 0.5


def get_closest_color(pixel : iter, color_choices : list = COLOR_CHOICES) -> list:
    """ Returns the single closest color to the pixels color from the list of colors provided.
    :param pixel:iter          - Collection of scalar values for the color ( red, green, blue ).
    :param color_choices:iter  - Collection of colors that we can choose. Each choice is a sublist of red, gree, blue
    :return:list               - Returns an iterable of the red, green, blue value is closest.
    """

    min_distance = 500
    closest_color = None
    for color in color_choices:
        new_distance = get_distance(pixel, color)
        if new_distance < min_distance:
            closest_color = color
            min_distance = new_distance
    return closest_color


def write_ppm(ppm_type : str, width : int, height : int, depth : int, pixels : list):
    """ Prompts for file to write to, and then writes out the new ppm to that file.
    :param ppm_type:str        - The header of the file, P3
    :param width:int           - Width of the ppm file
    :param height:int          - Width of the ppm file
    :param depth:int           - Width of the ppm file
    :param pixels:list         - Width of the ppm file
    :return:None 
    """

    out_ppm = get_file("What is the name of the file you want to save to? ==> ", "w")
    print("{}".format(ppm_type), file=out_ppm)
    print("{} {}".format(width, height), file=out_ppm)
    print("{}".format(depth), file=out_ppm)

    for red, green, blue in pixels:
        print("{}\n{}\n{}".format(red, green, blue), file=out_ppm)
    out_ppm.close()


def process_ppm(img) -> bool:
    """ Processes a ppm file.
    :param ppm_list:list       - Collection of lines out of the ppm file.
    :return:bool               - True if the file was valid and processed, False if not.
    """

    ground_y = mc.getHeight(0, 0)

    y = img.size[1] + ground_y     # Draw the top of the picture in the top of the sky.
    x = -img.size[0] // 2

    mc.setBlocks(x, ground_y, x, abs(x), y + 20, abs(x), 0)

    for row in range(img.size[1]):
        for col in range(img.size[0]):

            pixel = img.getpixel((col, row))
            color = tuple(get_closest_color(pixel))
            value = COLOR_CHOICES.index(color)
            mc.setBlock(x + col, y - row, 0, 35, value)

    print("\nYour file has been saved.")
    return True
        

# Run until the user chooses to quit
running = True
while running:

    # Get menu choice and perform actions.
    menu_choice = get_choice(MENU, MENU_CHOICES)
    if menu_choice == "1":

        valid = False
        while not valid:
            img_file = get_file("Enter a valid filename to convert. ==> ")

            valid = process_ppm(img_file)
        
    elif menu_choice == "Q":
        running = False
