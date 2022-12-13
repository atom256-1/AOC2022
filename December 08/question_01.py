import numpy

filename = "data.txt"

file = open(filename, "r")

content = numpy.array([[int(val) for val in list(string)] for string in file.read().split("\n")])
visible = numpy.zeros(content.shape, dtype = bool)
visible[[0, -1], :] = True
visible[:, [0, -1]] = True

file.close()


# Row by row
for i in [-1, 1] :
	for j in range(visible.shape[0]) :
		highest = 0
		maxVal = max(content[j, :])
		for k in list(range(visible.shape[1]))[::i] :
			val = content[j, k]
			if(val > highest) :
				visible[j, k] = True
				highest = val
			if(val == maxVal) :
				break

# Column by column
for i in [-1, 1] :
	for j in range(visible.shape[1]) :
		highest = 0
		maxVal = max(content[:, j])
		for k in list(range(visible.shape[0]))[::i] :
			val = content[k, j]
			if(val > highest) :
				visible[k, j] = True
				highest = val
			if(val == maxVal) :
				break


print(numpy.count_nonzero(visible))
print()

score = numpy.zeros(content.shape, dtype = int)

for i in range(visible.shape[0]) :
	for j in range(visible.shape[1]) :
		if(visible[i, j]) :
			height = content[i, j]
			visible_count = [0, 0, 0, 0]
			
			print(i, j)
			
			for k in range(i + 1, visible.shape[0]) :
				visible_count[0] += 1
				if(content[k, j] >= height) :
					break
			print(list(range(i + 1, visible.shape[0])), visible_count[0])
			
			for k in list(range(i))[::-1] :
				visible_count[1] += 1
				if(content[k, j] >= height) :
					break
			print(list(range(i))[::-1], visible_count[1])
			
			for k in range(j + 1, visible.shape[1]) :
				visible_count[2] += 1
				if(content[i, k] >= height) :
					break
			print(list(range(j + 1, visible.shape[1])), visible_count[2])
			
			for k in list(range(j))[::-1] :
				visible_count[3] += 1
				if(content[i, k] >= height) :
					break
			print(list(range(j))[::-1], visible_count[3])
			print()
			
			score[i, j] = numpy.product(visible_count)


print(numpy.max(score))


















