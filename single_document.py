import os

pathmongodb = "C:\\Program Files\\MongoDB\\Server\\5.0\\bin"
database_name = "test"
collection_name = "test"
output = "a.json"

cmd = "cd " + pathmongodb
returned_value = os.system(cmd) 

#mongoexport
#mongoexport --db tên_database --collection tên_collection --out tên_file_xuất_ra.json
cmd = "mongoexport --db "+database_name+" --collection "+collection_name+" --out "+output
returned_value = os.system(cmd) 

#mongoimport
#mongoimport --db tên_database --collection tên_collection --file tên_file_import.json
cmd = "mongoimport --db "+database_name+" --collection "+collection_name+" --file "+output
returned_value = os.system(cmd) 
