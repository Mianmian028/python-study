i = 0
row = 5

while i < row:
 	i = i +1 


 	star_str = "---"
 	num_print = i 
 	j=0
 	while j < i:
 		star_str = star_str+"*" + " "
 		j=j+1

 	print star_str


print "=========="
i=0
row=5
while i < row:
	

	star_str=""
	j=0
	while j < 2 * row + 1 :
		if j < row - i :
			star_str = star_str + " "
		elif j >= 2 * row + 1 - (row - i) :
			star_str = star_str + " "
		else:
			star_str=star_str+"*"
		j=j+1

	i =i +1
	print star_str 


print "=========="
i=0
row=5
while i < row:
	print (row - i) * " " + (2*i + 1) * "*" 
	i =i +1



