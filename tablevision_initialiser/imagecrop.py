import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.widgets as widgets
import json

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
        print()
        table_id = input("Enter table number: ")

        if table_id in tables:
            print("Table exists already!")
            continue

        imageCropper()

        print("===============================")
        print("Table " + table_id + " plotted!")
        print("===============================")
        print()

        tables[table_id] = [FIRST, SECOND, THIRD, FOURTH]

        want_to_continue = input("Do you want to continue? [Y|N]: ").capitalize()

        if want_to_continue != "Y":
            prompter = False
            print()
            print("Copy the following line into a Terminal window:")
            print("=========================================")
            print()
            print("python3 initialise.py '", end="")
            print(json.dumps(tables), end="")
            print("'")
            print()
            print("=========================================")
            print()
            print("Goodbye!")

def onselect(eclick, erelease):
    if eclick.ydata>erelease.ydata:
        eclick.ydata,erelease.ydata=erelease.ydata,eclick.ydata
    if eclick.xdata>erelease.xdata:
        eclick.xdata,erelease.xdata=erelease.xdata,eclick.xdata

    FIRST[0] = eclick.xdata / WIDTH
    FIRST[1] = eclick.ydata / HEIGHT
    SECOND[0], SECOND[1] = erelease.xdata / WIDTH , eclick.ydata / HEIGHT
    THIRD[0], THIRD[1] = eclick.xdata / WIDTH , erelease.ydata / HEIGHT
    FOURTH[0], FOURTH[1] = erelease.xdata / WIDTH , erelease.ydata / HEIGHT
    plt.close()

def imageCropper():
    print("Please annotate the boundary boxes, starting from the top-left to the bottom-right. Thank you :)")
    print()

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