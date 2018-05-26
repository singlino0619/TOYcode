import os, sys
# decide the parent path placement
# enter parent path name in argv[1]
# usage: python createFolder "Parentfolder" "Childernfoldername" "the number of folders"
p_dir_path = os.getcwd() + "/" + sys.argv[1]
# create parent-folder
os.makedirs(p_dir_path, exist_ok=True)
# create children-folder
# the number of folders is determined by argv[3]
for i in range(1, int(sys.argv[3]) + 1):
    # decide target path
    # the children-folder name is created by the name of argv[2]
    targetpath = p_dir_path + "/" + sys.argv[2]
    # create children-folder in order
    os.makedirs(targetpath + str(i))
