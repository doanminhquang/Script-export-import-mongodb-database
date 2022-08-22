from os import system

def GoToMongoDB(path):
    cmd = "cd %s" % (path)
    system(cmd) 

def MongoExport(database_name, collection_name, path):
    cmd = "mongoexport --db %s --collection %s --out %s" % (database_name, collection_name, path)
    system(cmd)     

def MongoImport(database_name, collection_name, path):
    cmd = "mongoimport --db %s --collection %s --file %s" % (database_name, collection_name, path)
    system(cmd) 
       
def MongoDump(database_name, path):    
    cmd = "mongodump -d %s -o %s"  % (database_name, path)
    system(cmd) 
    
def MongoRestore(database_name, path):
    cmd = "mongorestore -d %s %s"  % (database_name, path)
    system(cmd) 
