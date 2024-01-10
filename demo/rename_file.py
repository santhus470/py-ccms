import os
path = 'C:\\Users\PC12\Desktop\\2toSinL3'
start=1
print('strat')
for root, d, f in os.walk(path):
    print(path)
    for file in f:
        print(file)
        os.rename(os.path.join(path, file), os.path.join(path, '1-1-2019'+f'-{start}.JPEG'))
        print(file)
        start+=1

print('Stop')