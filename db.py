import os
import os.path
import zipfile
from datetime import datetime
from pymongo import MongoClient

global_root = 'data/'
global_export = global_root + 'export/'
global_import = global_root + 'import/'
    
def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       os.path.join(path, '..')))

def input_int(str, min, max):
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

def mongoexport(database_name, collection_name, path):
    cmd = "mongoexport --db " + database_name + " --collection " + collection_name + " --out "+ path
    os.system(cmd)     

def mongoimport(database_name, collection_name, path):
    cmd = "mongoimport --db " + database_name + " --collection " + collection_name + " --file "+ path
    os.system(cmd) 

def run_single(choice_mode,database_name,collection_name):
    try:
        print("***** Choice: "+collection_name)
        if(choice_mode == switcher_mode[0]):
            path_output = global_export+database_name+'/'+collection_name+'.json'
            mongoexport(database_name,collection_name,path_output)
        else:
            path_input = global_import+collection_name+'.json'
            mongoimport(database_name,collection_name,path_input)  
    except IOError:
        print("File not accessible")

def run_all(choice_mode,database_name,collections):            
    for n in range(len(collections)):
        collection_name = collections[n]
        run_single(choice_mode,database_name,collection_name)      
    if(choice_mode == switcher_mode[0]):
        timestr = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        with zipfile.ZipFile(global_export+database_name+'_'+timestr+'.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipdir(global_export+database_name+'/', zipf) 

if __name__ == "__main__":

    pathmongodb = "C:\\Program Files\\MongoDB\\Server\\5.0\\bin"

    switcher_dbmode={0:'Local', 1:'Alat'}

    for j in range(len(switcher_dbmode)):
        print(str(j)+" : "+switcher_dbmode[j])
        
    min = 0
    max = len(switcher_dbmode)-1
    n_db = input_int("----- Enter selection ("+str(min)+"-"+str(max)+"): ",min,max)
    
    global client
    
    if n_db == 0:
        client = MongoClient(host="localhost", port=27017)
    else:
        client = MongoClient("")

    choice_dbmode = switcher_dbmode.get(n_db,"Invalid choice")
    print("***** Choice: "+choice_dbmode+" mode")  

    switcher_mode={0:'Export', 1:'Import', 2:'Import And Create'}

    for j in range(len(switcher_mode)):
        print(str(j)+" : "+switcher_mode[j])

    min = 0
    max = len(switcher_mode)-1
    n = input_int("----- Enter selection (" + str(min) + "-" + str(max) + "): ", min,max)

    choice_mode = switcher_mode.get(n,"Invalid choice")
    print("***** Choice: " + choice_mode + " mode")  
    
    if choice_mode != switcher_mode[0]:
        tmp_collections = []
        for filename in os.listdir(global_import):
            if filename.endswith(".json"):
                tmp_collections.append(os.path.splitext(filename)[0])        
        if len(tmp_collections) == 0 :
            print("File import not found")
            raise SystemExit
    
    cmd = "cd " + pathmongodb
    returned_value = os.system(cmd) 

    dbs = client.list_database_names()
    for j in range(len(dbs)):
        print(str(j) + " : " + dbs[j])

    if choice_mode != switcher_mode[2]:
        min = 0
        max = len(dbs) - 1
        m = input_int("----- Enter index of db name (" + str(min) + "-" + str(max) + "): ", min, max)
    else:
        min = -1
        max = len(dbs) - 1
        m = input_int("----- Enter index of db name (" + str(min) + " = create new) || (" + str(min + 1) + "-" + str(max)+"): ", min, max)

    if m != -1 :
        database_name = dbs[m]
    else:
        database_name = input("----- Enter db name: ")
    
    print("***** Choice: " + database_name)

    if choice_mode != switcher_mode[2]:
        collections = client[database_name].list_collection_names()
        min = -1
        max = len(collections) - 1
    else:
        collections = tmp_collections
        min = -1
        max = len(collections) - 1

    for j in range(len(collections)):
        print(str(j) + " : " + collections[j])
    p = input_int("----- Enter index of collection name (" + str(min) + " = all) || (" + str(min + 1) + "-" + str(max) + "): ", min, max)

    if(p == -1):
        run_all(choice_mode, database_name, collections)
    else:
        collection_name = collections[p]
        run_single(choice_mode, database_name, collection_name)     
