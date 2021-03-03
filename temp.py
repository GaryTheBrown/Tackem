import pathlib
folder = "/home/Tackem/.Tackem/videoripping/1"
print(folder)
for path in pathlib.Path(folder).rglob('*'):
    print(path)
