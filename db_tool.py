import os
from pymongo import MongoClient

def input_int(str,min,max):
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

def mongoexport(database_name,collection_name,path):
    cmd = "mongoexport --db "+database_name+" --collection "+collection_name+" --out "+path
    os.system(cmd)     

def mongoimport(database_name,collection_name,path):
    cmd = "mongoimport --db "+database_name+" --collection "+collection_name+" --file "+path
    os.system(cmd) 

def run_single(choice_mode,database_name,collection_name):
    try:
        print("Choice: "+collection_name)
        if(choice_mode == 'Export'):
            path_output = 'data/export/'+collection_name+'.json'
            mongoexport(database_name,collection_name,path_output)
        else:
            path_input = 'data/import/'+collection_name+'.json'
            mongoimport(database_name,collection_name,path_input)  
    except IOError:
        print("File not accessible")

def run_all(choice_mode,database_name,collections):            
    for n in range(len(collections)):
        collection_name = collections[n]
        run_single(choice_mode,database_name,collection_name)         

if __name__ == "__main__":

    pathmongodb = "C:\\Program Files\\MongoDB\\Server\\5.0\\bin"

    client = MongoClient(host="localhost", port=27017)

    switcher_mode={0:'Export', 1:'Import'}

    n = input_int("Export or Import (0 or 1): ",0,1)

    choice_mode = switcher_mode.get(n,"Invalid choice")

    cmd = "cd " + pathmongodb
    returned_value = os.system(cmd) 

    dbs = client.list_database_names()
    print("Len "+str(len(dbs))+": "+str(dbs))

    m = input_int("Index of db name: ",0,len(dbs)-1)
    database_name = dbs[m]
    print("Choice: "+database_name)
    collections = client[database_name].list_collection_names()
    print("Len "+str(len(collections))+": "+str(collections))

    p = input_int("Index of collection name (-1 = all): ",-1,len(collections)-1)

    if(p==-1):
        run_all(choice_mode,database_name,collections)
    else:
        collection_name = collections[p]
        run_single(choice_mode,database_name,collection_name)     
