import os
from pathlib import Path
from PIL import Image
import re
import shutil




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

#copy and compress to new dimensions
def CopyComp(file,out, dim):
    #load an image
    img = Image.open(file)

    #Converts into greyscale
    #L = greysacle, RGB = rgb
    if not img.mode == 'L':
      img = img.convert('L')
    
    #save image
    width, height = img.size
    if(width>height):
        #split wide images into two

        i1 = img.crop([0,0,width/2,height])
        i2 = img.crop([width/2,0,width,height])

        i1.thumbnail((dim[0],dim[1]),Image.ANTIALIAS)
        i1.save(append_id(out,"a"), quality=dim[2])

        i2.thumbnail((dim[0],dim[1]),Image.ANTIALIAS)
        i2.save(append_id(out,"b"), quality=dim[2])


        
    else:
        img.thumbnail((dim[0],dim[1]),Image.ANTIALIAS)
        img.save(out, quality=dim[2])


#convert to pdf
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
#convert to zip
def zipify(path, opath):
    shutil.make_archive(opath, 'zip', path)
    os.rename(opath+".zip", opath)



#clear tmp files
def cleartmp(f):
    shutil.rmtree(f)
    if not os.path.exists(f):
        os.makedirs(f)

###todo do the ___main___ whatever thingies


def PngtoPdf(iFolder,oFolder,name,qual,xo,yo,outFormat):

    ###todo validate input




    #temp files
    tFolder=oFolder+"/tmp"
    pre='image'

    #make sure tmp and output folders exist
    if not os.path.exists(tFolder):
        os.makedirs(tFolder)
    if not os.path.exists(oFolder):
        os.makedirs(oFolder)

    #list of folders 
    folderList = [x[0] for x in os.walk(iFolder)]
    sort_nicely(folderList)

    i = 0
    pdfi=1



    #make sure the tmpfolder is empty
    cleartmp(tFolder)

    
    print("----------------")
    print("<    start     >")
    print("----------------")


    #loop through folders
    for f in folderList:
        #print(f)
        i=0;
        #loop though the files in current folder
        for file in os.listdir(f):
            #check if filetype is an image
            if file.endswith(".png") or file.endswith(".jpg"):
                #filename
                fn= (pre+"_"+(f'{i:05d}')+".jpg")

                #make filename use subfolder
                
                #print(os.path.join(f, file)+"  "+os.path.join(tFolder, fn))

                CopyComp(os.path.join(f, file),os.path.join(tFolder, fn), [xo,yo,qual])            
                i=i+1
                
        fn = os.path.basename(os.path.normpath(f))        
        oF=oFolder+"/"+fn+"."+outFormat
        if(i>0):
            print(oF)
            if(outFormat=="pdf"):
                pdfify(tFolder,oF)
                cleartmp(tFolder)
                
            if(outFormat=="cbz"):
                zipify(tFolder,oF)
                cleartmp(tFolder)
    print("----------------")
    print("<    done      >")
    print("----------------")



if __name__ == "__main__":
    #output parameters
    qual=85
    xo=600
    yo=800
    #format cbz, pdf
    outFormat="cbz"
     #folders
    #input
    iFol=r'C:\User\manga\input'
    #output name
    oName=r'test'
    #output folder
    oF=r'C:\User\manga\output'

    PngtoPdf(iFol,oF,oName,qual,xo,yo, outFormat);








    

