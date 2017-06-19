from PIL import Image
import  numpy

def quantizeImg(int, imgArr):
    for i in range(imgHeight):
        imgArr[i][:] = [x / int for x in imgArr[i]]
    return imgArr

def dequantizeImg(int,imgArr):
    for i in range(imgHeight):
        imgArr[i][:] = [x * int for x in imgArr[i]]
    return imgArr

def encode(imgArr):
    encoded = ' '+str(imgArr[0,0][0])+';'+str(imgArr[0,0][1])+';'+str(imgArr[0,0][2])+''
    i = 0
    j = 1
    while i < imgHeight:
        if i == 0 :
            previous = imgArr[i,j-1]
        else:
            previous = imgArr[i-1,j]

        while(j < imgWidth):
            now = imgArr[i,j]
            if not (previous == now).all():
                encoded += '-'+str(i) + ';' + str(j) + '|' + str(now[0]) + ';' + str(now[1]) + ';' + str(now[2])
            previous = now
            j += 1
        j = 0
        i += 1
    encoded+='-'+str(imgHeight-1)+';'+str(imgWidth-1) #add the last pixel
    return encoded

def decode(encoded):
    rowended = False
    # create an empty array to store the image
    decoded = numpy.zeros((imgHeight,imgWidth,3),dtype=numpy.uint8)
    encodedArr = encoded.split('|')
    now = 0 #the current row index
    colleft = 0 #the previous collumn
    for item in encodedArr:
        item = item.split('-')
        range = item[1].split(';') #get the range of the  RGB value
        col = int(range[0])#get the collumn that the next value starts
        end = int(range[1]) #get the row index of the next value
        rgb = item[0].split(';') #get the rgb value

        #is value on the next collumn?
        if now <= imgWidth and  col > colleft:
            col = colleft
            end = imgWidth
            rowended = True

        while now < end:
            decoded[col][now] = numpy.array(rgb)
            #if is to change collumn and continue on that collumn
            if rowended and range[1] != 0 and now == imgWidth-1   :
                now=0
                end = int(range[1])
                col = int(range[0])
                rowended = False
            else:
                now+=1
            colleft = col

    return decoded

im = Image.open("6.16/media/puppy.png")
imgHeight = im.height
imgWidth = im.width
imgArr = numpy.array(im)
qImgArr = quantizeImg(10,imgArr)
encoded = encode(qImgArr)
newImg = decode(encoded)
newImg = dequantizeImg(10,newImg)
img = Image.fromarray(newImg,'RGB')
with open("6.16/results/encoded.txt", "w") as text_file:
    print(encoded, file=text_file)
img.save('6.16/results/test.jpg')
img.show()

