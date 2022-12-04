filename = "data.txt"

file = open(filename, "r")

lines = file.read().split("\n")
pairs = [line.split(",") for line in lines]
content = [[tuple(pair1.split("-")), tuple(pair2.split("-"))] for [pair1, pair2] in pairs]
content =  [[(int(tup1[0]), int(tup1[1])), (int(tup2[0]), int(tup2[1]))] for [tup1, tup2] in content]

file.close()

a = 0
o = 0

for i in range(len(content)) :
	pairs = content[i]
	set0 = set(range(pairs[0][0], pairs[0][1] + 1))
	set1 = set(range(pairs[1][0], pairs[1][1] + 1))
	
	if(set0.issubset(set1) or set1.issubset(set0)) :
		a += 1
	
	if(len(set0 & set1) != 0) :
		o += 1


print()
print("# of fully contained assigment pairs :", a)
print("# of assigment pairs that overlap    :", o)