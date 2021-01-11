import _md5
import hashlib
print('hello world')
#print(_md5.md5(123))
x=hashlib.md5(str(123).encode('utf-8')).hexdigest()
#hashlib.md5(str(var_frais[0]).encode('utf-8')).hexdigest()
print(x)