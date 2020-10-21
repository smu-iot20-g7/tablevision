import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.widgets as widgets

WIDTH = 0
HEIGHT = 0

FIRST = [0, 0]
SECOND = [0, 0]
THIRD = [0, 0]
FOURTH = [0, 0]

tables = {}

def runCropper():
    prompter = True

    while prompter:
        table_id = input("Enter table ID: ")

        if table_id in tables:
            print("Table exists already!")
            continue

        imageCropper()

        tables[table_id] = [FIRST, SECOND, THIRD, FOURTH]

        want_to_continue = input("Do you want to continue? [Y|N]: ").capitalize()

        if want_to_continue != "Y":
            prompter = False
            print(tables)
            print("Goodbye!")

def onselect(eclick, erelease):
    if eclick.ydata>erelease.ydata:
        eclick.ydata,erelease.ydata=erelease.ydata,eclick.ydata
    if eclick.xdata>erelease.xdata:
        eclick.xdata,erelease.xdata=erelease.xdata,eclick.xdata

    FIRST[0] = eclick.xdata 
    FIRST[1] = eclick.ydata 
    SECOND[0], SECOND[1] = erelease.xdata , eclick.ydata 
    THIRD[0], THIRD[1] = eclick.xdata , erelease.ydata 
    FOURTH[0], FOURTH[1] = erelease.xdata , erelease.ydata
    plt.close()

def imageCropper():
    print("EH DRAW LEFT TO RIGHT AH DONT STUPID")

    global fig, ax, filename, im, arr, plt_image, rs, WIDTH, HEIGHT

    fig = plt.figure()
    ax = fig.add_subplot(111)
    filename="test.jpg"
    im = Image.open(filename)
    arr = np.asarray(im)
    WIDTH, HEIGHT = im.size
    plt_image=plt.imshow(arr)
    rs=widgets.RectangleSelector(
        ax, onselect, drawtype='box',
        rectprops = dict(facecolor='red', edgecolor = 'black', alpha=0.5, fill=True))
    plt.show()

runCropper()