
strs = "12,434,545,452,".split(',')
print(strs)
try:
    Arr = list(map(lambda x: int(x), strs))
except ValueError:
    print('参数有问题')

print(Arr)