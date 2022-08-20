from os import path, walk, listdir,makedirs
 
def ZipDir(dir, ziph, comment):
    for folderName, subfolders, filenames in walk(dir):
       for filename in filenames:
           filePath = path.join(folderName, filename)
           ziph.write(filePath, path.basename(filePath))
    
    ziph.comment = str.encode(comment)

def CreateReadmeTxt(dir, comment):
    with open(dir + '/readme.txt', 'w') as f:
        f.write(comment)
        
def CreateDirectoryNotExist(dir):
    isExist = path.exists(dir)
    if not isExist:
      makedirs(dir)
      
def LenFolder(dir):
    return len([name for name in listdir(dir) if path.isfile(path.join(dir, name))])

def InputInt(str, min, max):
    while True:
        try:
            n = int(input(str))
            if (n <  min or n > max):
                continue
        except:
            print("Input Invalid")
            continue
        else:
            return n