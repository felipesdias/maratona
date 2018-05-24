import os
for dire in os.listdir("."):
    if not os.path.isfile(dire):
        for filename in os.listdir("./"+dire):
            os.rename("./"+dire+"/"+filename, "./"+dire+"/"+filename.replace(' ', '_'))