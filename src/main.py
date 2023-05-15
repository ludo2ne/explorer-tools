from folder import Folder

cloud = Folder("/home/ensai/cloud computing")

cloud.list_files_and_folders()

print("\n" + "="*100 + "\n")

f1 = Folder("data/folder1")
f1.compare("data/folder2")
