import os.path, time

times= time.ctime(os.path.getmtime(r"C:\Users\solid\Downloads\save_pro_key_2 - Copy - Copy\data.txt"))
if(times=="Sun Sep 27 16:16:58 2020"):
    print("ok")

# print("created: %s" % time.ctime(os.path.getctime(file)))