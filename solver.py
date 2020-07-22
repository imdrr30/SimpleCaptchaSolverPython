from PIL import Image


def checker(img1,img2):
    if img1.size[0]!=img2.size[0]:
        return False
    else:
        temp = img1.load()
        temp2 = img2.load()
        unmatched=0
        for i in range(img1.size[0]):
            for j in range(img1.size[1]):
                if temp[i,j][0]!=temp2[i,j][0]:
                    unmatched+=1
                    if unmatched>=10:
                        return False
        return True


def solver(
        img,
        mask="data.png"):

    img = Image.open(img)
    pix = img.load()

    letters = Image.open(mask)
    ledata = letters.load()

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if (pix[x, y][0] > 75) \
                    and (pix[x, y][1] > 75) \
                    and (pix[x, y][2] > 75):
                pix[x, y] = (255, 255, 255, 255)
            else:
                pix[x, y] = (0, 0, 0, 255)
    counter = 0
    old_x = -1
    letterlist = []
    for x in range(letters.size[0]):
        black = True
        for y in range(letters.size[1]):
            if ledata[x, y] !=(0,0,0,255):
                black = False
                break
        if black:
            if x-old_x>=5:
                box = (old_x , 0, x, 40)
                letter = letters.crop(box)
                letterlist.append(letter)
                counter += 1
            old_x = x

    counter = 0
    old_x = -1
    caplist = []
    for x in range(img.size[0]):
        black = True
        for y in range(img.size[1]):
            if pix[x, y] != (0, 0, 0):
                black = False
                break
        if black:
            if x - old_x >= 5:
                box = (old_x, 0, x, 40)
                letter = img.crop(box)
                caplist.append(letter)
                counter += 1
            old_x = x
    alphanum='0123456789abcdefghijklmnopqrstuvwxyz'
    captcha=[]
    for i in range(len(caplist)):
        for j in range(len(letterlist)):
            if checker(caplist[i],letterlist[j]):
                captcha.append(alphanum[j])
    solved=''.join(captcha)
    if len(solved)==6:
        return solved
    else:
        raise Exception("Captcha can't be solved.")

if __name__ == '__main__':
    for i in range(28):
        try:
            print(solver(f'ss/cp_{i}.jpg'))
        except:
            pass