a=[[[1, 4]], [[2, 3]], [[3, 2]], [[4, 1]]]
b=[]

def tinh(y1,y2):
  for i in range(len(a)):
      if a[i][0][0]<y1 or a[i][0][0]>y2:
          b.append(i)

def xoa(list):
    count=0
    for i in b:
        list.pop(i-count)
        count+=1

def sapxep(list):
    list.sort()

tinh(0,5)

xoa(a)

sapxep(a)
print(a)
a.[0][1].sort()
