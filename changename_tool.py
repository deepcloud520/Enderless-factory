import os
lst=os.listdir(os.getcwd())
while True:
    d=input('1:')
    s=input('2:')
    for file in lst:
        try:
            f=open(file,'r')
            res=f.read()
            f.close()
            f=open(file,'w')
            f.write(res.replace(d,s))
            f.close()
        except:
            print('error!')