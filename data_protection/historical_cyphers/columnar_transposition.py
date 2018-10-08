def encode(txt,key):
    size = len(key)  # how big are the columns 
    cols = list(map("".join,zip(*zip(*[iter(txt)]*size)))) # list partitioned into columns
    return "".join([cols[key.index(str(c))] for c in range(1,size+1)])

print(encode("HELLODARKNESSMYOLDFRIEND", "3754"))
