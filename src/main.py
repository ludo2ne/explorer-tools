from folder import Folder

cloud = Folder("/home/ludovic/pro")

cloud.list_files_and_folders()

print("\n" + "="*100 + "\n")

f1 = Folder("data/folder1")
f1.compare("data/folder2")

print("\n" + "="*100 + "\n")

cloud.display_large_old_files(nb_years = 0, size_mo = 0.2)