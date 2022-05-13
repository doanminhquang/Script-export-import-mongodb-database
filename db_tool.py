import os
import os.path
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
        if(choice_mode == switcher_mode[0]):
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

    switcher_mode={0:'Export', 1:'Import', 2:'Import And Create'}

    for j in range(len(switcher_mode)):
        print("\t"+str(j)+" : "+switcher_mode[j])

    min = 0
    max = len(switcher_mode)-1
    n = input_int("Enter selection ("+str(min)+"-"+str(max)+"): ",min,max)

    choice_mode = switcher_mode.get(n,"Invalid choice")
    print("Choice: "+choice_mode+" mode")  

    cmd = "cd " + pathmongodb
    returned_value = os.system(cmd) 

    dbs = client.list_database_names()
    for j in range(len(dbs)):
        print("\t"+str(j)+" : "+dbs[j])

    if choice_mode != switcher_mode[2]:
        min = 0
        max = len(dbs)-1
        m = input_int("Index of db name ("+str(min)+"-"+str(max)+"): ",min,max)
    else:
        min = -1
        max = len(dbs)-1
        m = input_int("Index of db name ("+str(min)+" = create new) || ("+str(min+1)+"-"+str(max)+"): ",min,max)

    if m != -1 :
        database_name = dbs[m]
    else:
        database_name = input("Enter db name: ")
    
    print("Choice: "+database_name)
    
    if choice_mode != switcher_mode[2]:
        collections = client[database_name].list_collection_names()
        for j in range(len(collections)):
            print("\t"+str(j)+" : "+collections[j])
        min = -1
        max = len(collections)-1
        p = input_int("Index of collection name ("+str(min)+" = all) || ("+str(min+1)+"-"+str(max)+"): ",min,max)
    else:
        collections = []
        for filename in os.listdir("data/import/"):
            if filename.endswith(".json"):
                collections.append(os.path.splitext(filename)[0])
        min = -1
        max = len(collections)-1
        p = input_int("Index of collection name ("+str(min)+" = all) || ("+str(min+1)+"-"+str(max)+"): ",min,max)

    if(p==-1):
        run_all(choice_mode,database_name,collections)
    else:
        collection_name = collections[p]
        run_single(choice_mode,database_name,collection_name)     
