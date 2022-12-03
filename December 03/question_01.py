filename = "data.txt"

file = open(filename, "r")
content = [[string[:len(string)//2], string[len(string)//2:]] for string in file.read().split("\n")]
file.close()


priorities = 0

for i in range(len(content)) :
	item = list(set(content[i][0]) & set(content[i][1]))[0]
	
	if(item.islower()) :
		value = ord(item) - 96
	else :
		value = ord(item) - 64 + 26
	
	priorities += value


print()
print(priorities)