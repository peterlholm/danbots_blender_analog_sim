"Generate structured image"
from pathlib import Path
from math import cos, pi
from PIL import Image
#from PIL.ExifTags import TAGS
from PIL.PngImagePlugin import PngInfo

XPAUTHOR = 40094
XPTITLE = 40092
IMAGEDESCRIPTION = 0x010e
PICTURE_SIZE = 400
FREQ = 17
PIC_PR_PERIOD = PICTURE_SIZE / FREQ
PIXEL_COLOR = (0, 255, 0)
DPI = 4000      # for film
DPIXY = (DPI, DPI)
INCH = 25.4     # mm

# DESIGN CONSTANTS

PIC_SIZE = 5.0    # mm
NO_PIXELS = int(PIC_SIZE / INCH * DPI)

DIAS_SIZE = 800
NO_GITTER = 10
PIX_PR_LINE = DIAS_SIZE/NO_GITTER
LINE_SIZE = 2

_DEBUG = False

def create_images(folder):
    img = Image.new('L', (DIAS_SIZE, DIAS_SIZE))
    imga = Image.new('LA', (DIAS_SIZE, DIAS_SIZE), (0,255))

    val = 255
    # create border
    for n in range(DIAS_SIZE):
        img.putpixel((n, 0), val)
        img.putpixel((n, 1), val)
        img.putpixel((n,DIAS_SIZE-1),val)
        img.putpixel((n,DIAS_SIZE-2),val)
        img.putpixel((0, n), val)
        img.putpixel((1, n), val)
        img.putpixel((DIAS_SIZE-1,n),val)
        img.putpixel((DIAS_SIZE-2,n),val)
        imga.putpixel((n, 0), val)
        imga.putpixel((n, 1), val)
        imga.putpixel((n,DIAS_SIZE-1),val)
        imga.putpixel((n,DIAS_SIZE-2),val)
        imga.putpixel((0,n), val)
        imga.putpixel((1,n), val)
        imga.putpixel((DIAS_SIZE-1,n),val)
        imga.putpixel((DIAS_SIZE-2,n),val)
    for y in range(NO_GITTER):
        print(y)
        #print(val, intens)
        yval = int(y * PIX_PR_LINE)
        for x in range(DIAS_SIZE):
            for t in range(3):
                img.putpixel((x, yval+t), val)
                imga.putpixel((x, yval+t), val)
    savefolder = Path(folder)
    img.save(savefolder / "gitter.png", dpi=DPIXY)
    imga.save(savefolder / "gitter_a.png", dpi=DPIXY)

def create_window(folder):
    "create a white window"
    img = Image.new('L', (DIAS_SIZE, DIAS_SIZE))
    imga = Image.new('LA', (DIAS_SIZE, DIAS_SIZE), (0,255))
    val = 255
    # create border
    for n in range(DIAS_SIZE):
        img.putpixel((n, 0), val)
        img.putpixel((n, 1), val)
        img.putpixel((n,DIAS_SIZE-1),val)
        img.putpixel((n,DIAS_SIZE-2),val)
        img.putpixel((0, n), val)
        img.putpixel((1, n), val)
        img.putpixel((DIAS_SIZE-1,n),val)
        img.putpixel((DIAS_SIZE-2,n),val)
        imga.putpixel((n, 0), val)
        imga.putpixel((n, 1), val)
        imga.putpixel((n,DIAS_SIZE-1),val)
        imga.putpixel((n,DIAS_SIZE-2),val)
        imga.putpixel((0,n), val)
        imga.putpixel((1,n), val)
        imga.putpixel((DIAS_SIZE-1,n),val)
        imga.putpixel((DIAS_SIZE-2,n),val)
    for y in range(NO_GITTER):
        #print(y)
        #print(val, intens)
        yval = int(y * PIX_PR_LINE)
        for x in range(DIAS_SIZE):
            for t in range(20):
                img.putpixel((x, yval+t), val)
                imga.putpixel((x, yval+t), val)
    savefolder = Path(folder)
    img.save(savefolder / "window.png", dpi=DPIXY)
    imga.save(savefolder / "window_a.png", dpi=DPIXY)


def create_dias(folder):
    "create the dias"
    grey = Image.new('L', (PICTURE_SIZE, PICTURE_SIZE))
    greya = Image.new('LA', (PICTURE_SIZE, PICTURE_SIZE))
    rgb = Image.new('RGB', (PICTURE_SIZE, PICTURE_SIZE))
    rgba = Image.new('RGBA', (PICTURE_SIZE, PICTURE_SIZE))
    print("Freq (pic/period", PIC_PR_PERIOD)
    print("MM pr periode", PIC_PR_PERIOD/DPI*INCH)
    for y in range(PICTURE_SIZE):
        val = y / PIC_PR_PERIOD * 2 * pi
        intens = cos(val)
        #print(val, intens)
        for x in range(PICTURE_SIZE):
            val = 128 + int(intens * 128)
            grey.putpixel((x, y), val)
            greya.putpixel((x, y), (0, val))
            color = (0, int((1-intens) * 128), 0)
            rgb.putpixel((x, y), color)
            rgba.putpixel((x, y), (0, 255, 0, val))
    savefolder = Path(folder)

    metadata = PngInfo()
    metadata.add_text(
        "Description", f"Freq (pic/period {PIC_PR_PERIOD} mm pr periode {PIC_PR_PERIOD/DPI*INCH}")
    metadata.add_text("Author", "Peter Holm")
    exif = rgb.getexif()
    exif[XPAUTHOR] = "Peter Holm"
    exif[XPTITLE] = f"Freq (pic/period {PIC_PR_PERIOD} mm pr periode {PIC_PR_PERIOD/DPI*INCH}"

    exif[IMAGEDESCRIPTION] = f"Freq (pic/period {PIC_PR_PERIOD} mm pr periode {PIC_PR_PERIOD/DPI*INCH}"

    rgb.save(savefolder / "rgb.png", dpi=DPIXY, exif=exif, pnginfo=metadata)
    rgba.save(savefolder / "rgba.png", dpi=DPIXY, pnginfo=metadata)
    grey.save(savefolder / "grey.png", dpi=DPIXY, pnginfo=metadata)
    greya.save(savefolder / "greyA.png", dpi=DPIXY, pnginfo=metadata)
    # img.save("int.png","I")
    rgb.save(savefolder / "rbg.jpg", dpi=DPIXY, exif=exif, pnginfo=metadata)
    return rgb


def picture_size(imgfile):
    "get the physical size of picture"
    img = Image.open(imgfile)
    # img.load()
    dpi = img.info.get('dpi', None)
    if dpi:
        size = (img.width/dpi[0]*INCH, img.height/dpi[1]*INCH)
    else:
        size = None
    if _DEBUG:
        exif = img.getexif()
        print("Exif", exif)
        print(img.format, img.size, img.mode)
        print("dpi", dpi)
    return size


if __name__ == '__main__':
    print("Picture size pixels", NO_PIXELS)
    #create_images("tmp")
    create_window('tmp')
    # sz = picture_size('tmp/rgb.png')
    # print("Size (mm)", sz)
