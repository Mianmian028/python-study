def add(x,y):
	a=x+y
	return a 
print add(2,3)
print add('foo',"t")
print add(x=2,y=3)
print add(x="foo",y="t")

print"++++++++++++++++++++++"
def quad(x,a=2,b=1,c=0):
    return a*x**2+b*x+c
print quad(2.0)
print quad(2,1,1,1)
print quad(2,1)

print"++++++++++++++++++++++"
def lifang(x):
	a=x*x*x
	return a
print lifang(2)
