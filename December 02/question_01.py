# This is inefficient, but it helps readability
translation = {
	"A" : "Rock",
	"B" : "Paper",
	"C" : "Scissors",
	"X" : "Rock",
	"Y" : "Paper",
	"Z" : "Scissors"
}

score = {
	"Rock" : 1,
	"Paper" : 2,
	"Scissors" : 3
}

filename = "data_01.txt"

file = open(filename, "r")
content = [line.split(" ") for line in file.read().split("\n")]
content = [(score[translation[a]], score[translation[b]]) for [a, b] in content]
file.close()

def result(A, B) :
	# You can easily show that ((A - 2) + A + B)mod3 * 3 will give the accurate point value
	return ((2*(A - 1) + B) % 3) * 3


points = 0

for i in range(len(content)) :
	# A is the opponent's hand
	A = content[i][0]
	# B is your hand
	B = content[i][1]
	
	points += result(A, B) + B


print()
print(points)