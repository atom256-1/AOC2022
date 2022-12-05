import re

filename = "data.txt"

file = open(filename, "r")

content = file.read().split("\n\n")

stack = content[0]
operations = content[1].split("\n")

# Transposing and horizontally flipping the text block containing the stacks
piles_str = [''.join(i[::-1]) for i in zip(*content[0].split("\n"))]

# Checks that the lines that are kept do contain a pile (They start with a digit)
# If so, the digit is removed and the elements of the piles are turned in a list
piles = [list(piles_str[i][1:].strip()) for i in range(len(piles_str)) if piles_str[i][0].isdigit()]


# For the operations block, we only care about the numerical data as we know the
# structure already
moves = [[int(match) for match in re.findall("\d+", operations[i])] for i in range(len(operations))]

file.close()


x = 0

for i in range(len(moves)) :
	piles[moves[i][2] - 1].extend(piles[moves[i][1] - 1][-moves[i][0]:])
	del piles[moves[i][1] - 1][-moves[i][0]:]


print()
for i in range(len(piles)) :
	print(i + 1, ":", piles[i][-1])

print()
for i in range(len(piles)) :
	print(piles[i][-1], end = "")