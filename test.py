import os
path:str = r"\\AWASE1HCMICAP01\AppsData\GR Ver Report\May 2026"
paths :list[str] =os.listdir(path)
path_split = [int(k[2].split(".")[0]) for k in [path.split(" ") for path in paths] ]
print(list(set(path_split)))