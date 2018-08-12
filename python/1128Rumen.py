s = "hello world"
print s.split() 

print "================="
a = [1,2,3,4,5]
b = [6,7,8,9,10]
print a+b

print "================="

a = [1,2,3,4,2+3]
print a 
print "================="
a={ "dog":2 , "cat":4}
print len(a)
print "================="

from numpy import array
a = array([1, 2, 3, 4])
a =a+2
print a 
print "================="
print "================="

i = 0
total = 0
while i < 1000000:
    total += i
    i += 1
print total

print "================="
 
a = 0
s = 0
while a < 10:
   s += a
   a += 1
print s

print "================="
raw=5
n=0
m=raw
while n<(raw*2):
    w=m
    while w>0:
        print " ",
        w-=1
    m-=1
    k=0
    while k<=n:
        print('*'),
        k+=1
    print ""
    n+=2


print "================="

i=1
while i<=9:
    j=1
    while j<=i:
            print("* "),
            j+=1
    print("\n")
    i+=1

print "================="
i=5
while i >=0:
    j=1 
    while j<=i:
		print "* ",
		j+=1
    print ("\n")
    i-=1

print "================="
raw=5
n=0
m=raw
while n<(2*raw):
	w=m
	while w>=0:
		print 3* " ",
		w-=1
	m-=1
	k=0
	while k<=n:
		print"*",
		k+=1
	print ""
	n+=4
print "================="
raw=5
n=0
m=raw
while n<(5*raw):
	w=m
	while w>=0:
		print 3*"A",
		w-=1
	k=0
	while k<=n:
		print "*",
		k+=1
	j=m
	while j>=0:
		print 3*"$",
		j-=1
	m-=1
	print""
	n+=4