filename = "data.txt"

file = open(filename, "r")
lines = file.read().split("\n")
content = [[lines[3*i], lines[3*i + 1], lines[3*i + 2]] for i in range(len(lines)//3)]
file.close()


priorities = 0

for i in range(len(content)) :
	item = list(set(content[i][0]) & set(content[i][1]) & set(content[i][2]))[0]
	
	if(item.islower()) :
		value = ord(item) - 96
	else :
		value = ord(item) - 64 + 26
	
	priorities += value


print()
print(priorities)