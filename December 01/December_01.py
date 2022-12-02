import numpy

filename = "data_01.txt"

file = open(filename, "r")
content = file.read().split("\n")
file.close()

j = 0
elf = [0]

for i in range(len(content)) :
	if(content[i] == "") :
		elf += [0]
		j += 1
	else :
		elf[j] += int(content[i])

print()
k = numpy.argmax(elf)
m = max(elf)
total = m
print(k + 1, ":", m)
elf[k] = 0

k = numpy.argmax(elf)
m = max(elf)
total += m
print(k + 1, ":", m)
elf[k] = 0

k = numpy.argmax(elf)
m = max(elf)
total += m
print(k + 1, ":", m)

print()
print("Total = " + str(total))