import os
import json
import urllib 
import zipfile
from datetime import datetime
from pymongo import MongoClient
from module.MongoDBTerminal import GoToMongoDB, MongoExport, MongoImport, MongoDump, MongoRestore
from module.Utils import ZipDir, CreateReadmeTxt, CreateDirectoryNotExist, LenFolder, InputInt

global_root = 'data/'
global_export = global_root + 'export/'
global_import = global_root + 'import/'

def run_single(choice_mode, database_name, collection_name):
    try:
        print("***** Choice: %s" % (collection_name))
        if(choice_mode == switcher_mode[0]):
            path_output = '%s%s/%s.json' % (global_export, database_name, collection_name)     
            MongoExport(database_name , collection_name , path_output)
        else:
            path_input = '%s%s.json' % (global_import, collection_name) 
            MongoImport(database_name, collection_name, path_input)  
    except IOError:
        print("File not accessible")

def run_all(choice_mode, database_name, collections):        
    switcher_ext = {0:'JSON ONLY', 1:'JSON AND BSON'}

    for j in range(len(switcher_ext)):
        print("%s : %s" %(str(j), switcher_ext[j]))
            
    min = 0
    max = len(switcher_ext) - 1
    n_ext = InputInt("----- Enter selection (%s - %s): " %(str(min), str(max)), min, max)    
    
    choice_ext = switcher_ext.get(n_ext,"Invalid choice")
    print("***** Choice: %s Extension" %(choice_ext))  
    
    if(choice_ext == switcher_ext[0]):
        for n in range(len(collections)):
            collection_name = collections[n]
            run_single(choice_mode, database_name, collection_name) 
    else:
        if(choice_mode == switcher_mode[0]):
            MongoDump(database_name, global_export)
        else:
            path_input = '%s%s' % (global_import, database_name)
            MongoRestore(database_name, path_input)

    if(choice_mode == switcher_mode[0]):    
        timestr = datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")
        path_folder = '%s%s' % (global_export, database_name)
        
        count_file_in_folder = LenFolder(path_folder)
        
        if count_file_in_folder != 0:        
            CreateReadmeTxt(path_folder, comment_str)       
            
            with zipfile.ZipFile('%s_%s.zip' % (path_folder, timestr), 'w', zipfile.ZIP_DEFLATED) as zipf:
                ZipDir('%s/' %(path_folder), zipf, comment_str) 
        else:
            print("Export failed")
            os.rmdir(path_folder)

if __name__ == "__main__":

    with open("config.json") as json_data_file:
        data = json.load(json_data_file) 

        pathmongodb = data["pathmongodb"]
        username = urllib.parse.quote(data["username"])
        password = urllib.parse.quote(data["password"])
        dbname = data["dbname"]
        conn = data["conn"]
        hostlocal = data["host"]
        portlocal = int(data["port"])
        comment_str = data["comment"]

        switcher_dbmode = {0:'Local', 1:'Alat'}

        for j in range(len(switcher_dbmode)):
            print("%s : %s" %(str(j), switcher_dbmode[j]))
            
        min = 0
        max = len(switcher_dbmode) - 1
        n_db = InputInt("----- Enter selection (%s - %s): " %(str(min), str(max)), min, max)
        
        global client
        
        if n_db == 0:
            client = MongoClient(host = hostlocal, port = portlocal)
        else:
            client = MongoClient(conn % (username, password, dbname))

        choice_dbmode = switcher_dbmode.get(n_db,"Invalid choice")
        print("***** Choice: %s mode" %(choice_dbmode))  
        
        GoToMongoDB(pathmongodb)
        
        switcher_mode = {0:'Export', 1:'Import', 2:'Import And Create'}

        for j in range(len(switcher_mode)):
            print("%s : %s" %(str(j), switcher_mode[j]))

        min = 0
        max = len(switcher_mode) - 1
        n = InputInt("----- Enter selection (%s - %s): " %(str(min), str(max)), min, max)

        choice_mode = switcher_mode.get(n,"Invalid choice")
        print("***** Choice: %s mode" %(choice_mode))
        
        if choice_mode != switcher_mode[0]:
            tmp_collections = []
            for filename in os.listdir(global_import):            
                if filename.endswith(".json"):
                   tmp_collections.append(os.path.splitext(filename)[0])     

            subfolders = [ f.path for f in os.scandir(global_import) if f.is_dir() ]
                      
            if len(tmp_collections) == 0 and len(subfolders) == 0:
                print("File/Folder import not found")
                raise SystemExit  
        
        dbs = client.list_database_names()
        for j in range(len(dbs)):
            print(str(j) + " : " + dbs[j])

        if choice_mode != switcher_mode[2]:
            min = 0
            max = len(dbs) - 1
            m = InputInt("----- Enter index of db name (%s - %s): " %(str(min), str(max)), min, max)
        else:
            min = -1
            max = len(dbs) - 1
            m = InputInt("----- Enter index of db name (%s = create new) || (%s - %s): " %(str(min), str(min + 1), str(max)), min, max)

        if m != -1 :
            database_name = dbs[m]
        else:
            database_name = input("----- Enter db name: ")
        
        print("***** Choice: %s" % (database_name))

        if choice_mode != switcher_mode[2]:
            collections = client[database_name].list_collection_names()
            min = -1
            max = len(collections) - 1
        else:
            collections = tmp_collections
            min = -1
            max = len(collections) - 1
            
        if max == -1:
            print("Collections not found!")
            raise SystemExit

        for j in range(len(collections)):
            print(str(j) + " : " + collections[j])
        p = InputInt("----- Enter index of collection name (%s = all) || (%s - %s): " %(str(min), str(min + 1), str(max)), min, max)

        path_dir = '%s%s' % (global_export, database_name)

        CreateDirectoryNotExist(path_dir)

        if(p == -1):
            run_all(choice_mode, database_name, collections)
        else:
            collection_name = collections[p]
            run_single(choice_mode, database_name, collection_name)   
            
            if(choice_mode == switcher_mode[0]):     
                count_file_in_folder = LenFolder(path_dir)
                
                if count_file_in_folder != 0:              
                    CreateReadmeTxt(path_dir, comment_str)
