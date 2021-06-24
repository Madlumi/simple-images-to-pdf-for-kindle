import os
from pathlib import Path
from PIL import Image
import re
import shutil


#output parameters
qual=80
xo=600
yo=800

#folders
iFol=r'input file'
oF=r'output folder'
oName=r'output name'
tFol=r'temporay file folder'
pre='image'



def tryint(s):
    try:
        return int(s)
    except:
        return s

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)


def append_id(filename,i):
    a = filename[:-4]
    b=filename[-4:]

    return a+i+b

#todo split pages?
def CopyComp(file,out, dim):
    img = Image.open(file)
    
    #L = greysacle, RGB = rgb
    if not img.mode == 'L':
      img = img.convert('L')
    
    width, height = img.size
    if(width>height):
        #spliterino
        i1 = img.crop([0,0,width/2,height])
        i2 = img.crop([width/2,0,width,height])

        i1.thumbnail((dim[0],dim[1]),Image.ANTIALIAS)
        i1.save(append_id(out,"a"), quality=dim[2])

        i2.thumbnail((dim[0],dim[1]),Image.ANTIALIAS)
        i2.save(append_id(out,"b"), quality=dim[2])


        
    else:
        img.thumbnail((dim[0],dim[1]),Image.ANTIALIAS)
        img.save(out, quality=dim[2])

def pdfify(path, opath):
    il=[]
    ia=None
    for file in os.listdir(path):
        if(ia==None):
            ia=Image.open(path+'\\'+file)
        else:
            il.append(Image.open(path+'\\'+file))
    print(il)
    print(ia)
    #imagelist = [im2,im3,im4]
    ia.save(opath,save_all=True,  append_images=il)
    
def cleartmp(f):
    shutil.rmtree(f)
    if not os.path.exists(f):
        os.makedirs(f)



oFol= oF+'\\'+oName+".pdf"
if not os.path.exists(tFol):
    os.makedirs(tFol)
if not os.path.exists(oFol):
    os.makedirs(oFol)

iii = [x[0] for x in os.walk(iFol)]
sort_nicely(iii)

i = 0
pdfi=1




cleartmp(tFol)
print("----------------------")
print("<          start     >")
print(" ")
print("    compressing...   >")


for f in iii:
    #print(f)
    for file in os.listdir(f):
        if file.endswith(".png") or file.endswith(".jpg"):
            fn= (pre+"_"+(f'{i:05d}')+".jpg")
            print(os.path.join(f, file)+"  "+os.path.join(tFol, fn))
            CopyComp(os.path.join(f, file),os.path.join(tFol, fn), [xo,yo,qual])            
            i=i+1
            
            if(i>500):
                oFol= oF+'\\'+oName+"_"+str(pdfi)+".pdf"
                pdfify(tFol,oFol)
                cleartmp(tFol)
                i=0
                pdfi+=1


oFol= oF+'\\'+oName+"_"+str(pdfi)+".pdf"
print("----------------------")
print("<size conversion done>")
print(" ")
print("<       pdfing...    >")
pdfify(tFol,oFol)

print("----------------------")
print("<clearing tmp files  >")
print(" ")

cleartmp(tFol)
