from collections import deque

filename = "data.txt"

file = open(filename, "r")

content = list(file.read())

file.close()

def findMarker(inputList, length) :
	marker = deque(inputList[:length])

	for i in range(length, len(inputList)) :
		if(len(set(marker)) == len(marker)) :
			print(i)
			break
		
		marker.popleft()
		marker.append(inputList[i])
	
	return i

findMarker(content, 4)
findMarker(content, 14)