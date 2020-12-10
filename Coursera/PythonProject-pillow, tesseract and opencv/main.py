import PIL
from PIL import Image
from PIL import ImageEnhance
from IPython.display import display
from PIL import ImageFont, ImageDraw


# change the ratio of RGB of image
def convert_RGB(image, color, ratio):
    width, height = image.size
    newImage = Image.new("RGB", (width, height), "white")
    pixels = newImage.load()
    for i in range(image.width):
        for j in range(image.height):
            pixel = image.getpixel((i, j))
            red = pixel[0]
            green = pixel[1]
            blue = pixel[2]
            if color == 0:
                pixels[i, j] = (int(red * ratio), green, blue)
            elif color == 1:
                pixels[i, j] = (int(red), int(green * ratio), blue)
            else:
                pixels[i, j] = (int(red), green, int(blue * ratio))
    return newImage


# add text behind the image for processing
def bindingText(targetImage, message, h):
    # create black background
    extendImage = PIL.Image.new(targetImage.mode, (targetImage.width, targetImage.height + h))

    # paste image to background
    extendImage.paste(targetImage, (0, 0))

    # add text
    draw = ImageDraw.Draw(extendImage)
    font = ImageFont.truetype("readonly/fanwood-webfont.ttf", 50)
    # draw.text((0, targetImage.height + 5), message, font=font)
    draw.text((0, targetImage.height), message, font=font)

    return extendImage


# ---------------------------
# main function of this task
# ---------------------------

# start to process the image

image = Image.open("readonly/msi_recruitment.gif")
image = image.convert('RGB')
display()
# build a list of 9 images which have different color ratio + text
pic_candidates = []
for i in range(3):
    for r in (0.1, 0.5, 0.9):
        text = 'channel {} intensity {}'.format(i, r)
        # height 50 is result calculated by the pixels,
        # original image size is 800 x 450
        # desire is 1200 x 750
        # resize factor = 1/2
        # so 50 = 750 x 2 / 3 - 450
        candidate = bindingText(image, text, 50)
        # conver RGB ratio
        pic_candidates.append(convert_RGB(candidate, i, r))

# create a contact sheet from 9 pic_candidates we generated before
first_image = pic_candidates[0]
contact_sheet = PIL.Image.new(first_image.mode, (first_image.width * 3, first_image.height * 3))
x = 0
y = 0
draw = ImageDraw.Draw(contact_sheet)
font = ImageFont.truetype("readonly/fanwood-webfont.ttf", 50)

for img in pic_candidates:
    # Lets paste the current image into the contact sheet
    contact_sheet.paste(img, (x, y))
    # Now we update our X position. If it is going to be the width of the image, then we set it to 0
    # and update Y as well to point to the next "line" of the contact sheet.
    if x + first_image.width == contact_sheet.width:
        x = 0
        y = y + first_image.height
    else:
        x = x + first_image.width

# resize and display the contact sheet
contact_sheet = contact_sheet.resize((int(contact_sheet.width / 2), int(contact_sheet.height / 2)))

# show the result
contact_sheet.show()
