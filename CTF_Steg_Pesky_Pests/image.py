from PIL import Image
import random
#test = Image.open("test.png")
#print(test.getpixel((0,0)))
#print(test.getpixel((1900,0)))
#print(test.getpixel((1900,600)))
racolivia = Image.open("ORIGINALraccoon.png")
#for r in range(303):
#    for c in range(500):
 #       pxl = (c,r)
#        tmp = racolivia.getpixel(pxl)
 #       if tmp[0] == 50:
  #          racolivia.putpixel(pxl, (0,0,0,243))

#----------------------------------------------------
#for r in range(20):
#    for c in range(20): #was 200 for both v <
#        pxl = (20+c,90+r)
#        racolivia.putpixel(pxl, (255,255,0,255))
#---------------------------------------------------
def makesquare(col,row):
    pixel = (col,row)
    
    for i in range(2):
        for j in range(2):
            upleft = racolivia.getpixel((col+i,row+j))
            upleft = list(upleft)
            poo = random.randint(0,1)
            if poo == 1:
                upleft[3] = 248
                print("248")
            if poo == 0:
                upleft[3] = 253
                print("253")
            upleft = tuple(upleft)
            racolivia.putpixel((col+i,row+j),upleft)            
    #lolo = racolivia.getpixel(pixel)
    #print("pixel", lolo, "should be alpha 253, along with these 3")
    #print(racolivia.getpixel((col+1,row)))
    #print(racolivia.getpixel((col+1,row+1)))
    #print(racolivia.getpixel((col,row+1)))

def wholeyards():
    row1 = input('please insert first row: ')
    row2 = input("row2: ")
    row3 = input("row3: ")
    c = input("column: ")
    r = input("row: ")
    c = int(c)
    r = int(r)
    stringrow1 = row1
    row1 = int(row1)
    iterate = 0
    print(stringrow1[0])
    print(type(stringrow1[0]))
    c1 = c
    for p in stringrow1:  #range(len(stringrow1)*2):
        if p == "1":
            makesquare((c1+(iterate*2)),r)
            iterate = iterate + 1
        elif p == "0":
            iterate = iterate + 1
        else:
            print("you messed ur string up buddy")
            break
        if iterate % 2 == 0:
            c1 = c1+1
    iterate = 0
    c1 = c
    for s in row2:
        if s == "1":
            makesquare((c1+(iterate*2)),r+2)
            iterate = iterate + 1
        elif s == "0":
            iterate = iterate + 1
        else:
            print("you messed ur string up buddy")
            break
        if iterate % 2 == 0:
            c1 = c1+1
    iterate = 0
    c1 = c
    for g in row3:
        if g == "1":
            makesquare((c1+(iterate*2)),r+4)
            iterate = iterate + 1
        elif g == "0":
            iterate = iterate + 1
        else:
            print("you messed ur string up buddy")
            break
        if iterate % 2 == 0:
            c1 = c1+1

def solver(): 
    for c in range(253):
        for r in range(248):
            cp = racolivia.getpixel((c,r))
            cp = list(cp)
            if (cp[3] == 253):
                cp = tuple(cp)
                racolivia.putpixel((c,r),(cp))
            elif (cp[3] ==248):
                cp = tuple(cp)
                racolivia.putpixel((c,r),(cp))
            else:
                cp = tuple(cp)
                racolivia.putpixel((c,r),(255,255,255,255))

            
        

def randomizamundo():
    for c in range(252):
        for r in range(247):
            skipper = random.randint(0,20)
            if skipper == 2:
                color = random.randint(0,4)
                if color == 0:
                    makerandomsquare(c,r,color)
                    #cp = racolivia.getpixel((c,r))
                    #cp = list(cp)
                    #cp[0]=cp[0]+1
                    #cp[0] =0
                    #cp[1]=255
                    #cp[2]=0
                    #cp = tuple(cp)
                    #racolivia.putpixel((c,r),cp)
                if color == 1:
                    #cp = racolivia.getpixel((c,r))
                    #cp = list(cp)
                    #cp[1]=cp[1]-1
                    #cp[0]=0
                    #cp[1]=255
                    #cp[2]=0
                    #cp = tuple(cp)
                    #racolivia.putpixel((c,r),cp)
                    makerandomsquare(c,r,color)
                if color == 2:
                    #cp = racolivia.getpixel((c,r))
                    #cp = list(cp)
                    #cp[2]=cp[2]+1
                    #cp[0]=0
                    #cp[1]=255
                    #cp[2]=0
                    #cp = tuple(cp)
                    #racolivia.putpixel((c,r),cp)
                    makerandomsquare(c,r,color)
                if color == 3:
                    #alpha = random.randint(0,15)
                    #cp = racolivia.getpixel((c,r))
                    #cp = list(cp)
                    #cp[0]=0
                    #cp[1]=150
                    #cp[2]=200 
                    #cp[3]= 240+alpha
                    #cp = tuple(cp)
                    #racolivia.putpixel((c,r),cp)
                    makerandomsquare(c,r,color)


def makerandomsquare(col,row,color):
    pixel = (col,row)
    
    for i in range(2):
        for j in range(2):
            upmeft = racolivia.getpixel((col+i,row+j))
            upmeft = list(upmeft)
            if color == 0:
                num = random.randint(1,3)
                if num < 3:
                    upmeft[0]= upmeft[0]+num
                elif num == 3:
                    upmeft[0]=upmeft[0]-1
                elif num ==4:
                    upmeft[0]=upmeft[0]-2
                upmeft = tuple(upmeft)
                racolivia.putpixel((col+i,row+j),upmeft)

            if color == 1:
                num = random.randint(1,4)
                if num < 3:
                    upmeft[1]= upmeft[1]+num
                elif num == 3:
                    upmeft[1]=upmeft[1]-1
                elif num ==4:
                    upmeft[1]=upmeft[1]-2
                upmeft = tuple(upmeft)
                racolivia.putpixel((col+i,row+j),upmeft)

            if color == 2:
                num = random.randint(1,4)
                if num < 3:
                    upmeft[2]= upmeft[2]+num
                elif num == 3:
                    upmeft[2]=upmeft[2]-1
                elif num ==4:
                    upmeft[2]=upmeft[2]-2
                upmeft = tuple(upmeft)
                racolivia.putpixel((col+i,row+j),upmeft)
            if color == 3:
                alpha = random.randint(0,15)
                upmeft[3]=240+alpha
                upmeft = tuple(upmeft)
                racolivia.putpixel((col+i,row+j),upmeft)


    #upleft = racolivia.getpixel()
    #upleft = list(upleft)
    #upleft[3] = 253
    #upleft = tuple(upleft)
    #racolivia.putpixel(pixel, upleft)
    #racolivia.putpixel((col+1,row), upleft)
    #racolivia.putpixel((col+1,row+1), upleft)
    #racolivia.putpixel((col,row+1), (0,0,255,255))

#makesquare(60,40)
randomizamundo()
wholeyards()
racolivia.save("racoonUDCTF.png")
solver()
racolivia.save("racoonUDCTFsolution.png")

