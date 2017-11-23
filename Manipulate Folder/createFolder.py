import os, sys
# decide the parent path placement
# enter parent path name in argv[1]
p_dir_path = os.getcwd() + "/" + sys.argv[1]
# create parent-folder
os.makedirs(p_dir_path)
# create children-folder
for i in range(1, int(sys.argv[3]) + 1):
    # decide target path
    targetpath = p_dir_path + "/" + sys.argv[2]
    # create children-folder in order
    os.makedirs(targetpath + str(i))
