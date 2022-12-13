import os
from collections import UserDict

class FileSystemDict(UserDict) :
	def __setitem__(self, key, value) :
		if(key[-1] == "/") :
			keys = key[:-1].split("/")
			keys = [val + "/" for val in keys]
		else :
			keys = key.split("/")
			keys = [keys[i] + "/" for i in range(len(keys) - 1)] + [keys[-1]]
		
		dictRef = self.data
		for i in range(len(keys) - 1) :
			if(keys[i] in dictRef) :
				dictRef = dictRef[keys[i]]
			else :
				dictRef[keys[i]] = {}
		
		dictRef[keys[-1]] = value
	
	
	def __getitem__(self, key) :
		keys = key.split("/")
		if(keys[-1] == "") :
			keys = keys[:-1]
		keys = [val + "/" for val in keys]
		
		dictRef = self.data
		for i in range(len(keys)) :
			if(keys[i] in dictRef) :
				dictRef = dictRef[keys[i]]
			else :
				raise KeyError(key)
		
		return dictRef
	
	
	def __del__(self, key = None) :
		if(key == None) :
			del self.data
		else :
			keys = key.split("/")
			if(keys[-1] == "") :
				keys = keys[:-1]
			keys = [val + "/" for val in keys]
			
			dictRef = self.data
			for i in range(len(keys) - 1) :
				if(keys[i] in dictRef) :
					dictRef = dictRef[keys[i]]
				else :
					raise KeyError(key)
			
			if(keys[-1] in dictRef) :
				del dictRef[keys[-1]]
			else :
				raise KeyError
	
	
	def __delitem__(self, key) :
		keys = key.split("/")
		if(keys[-1] == "") :
			keys = keys[:-1]
		keys = [val + "/" for val in keys]
		
		dictRef = self.data
		for i in range(len(keys) - 1) :
			if(keys[i] in dictRef) :
				dictRef = dictRef[keys[i]]
			else :
				raise KeyError(key)
		
		if(keys[-1] in dictRef) :
			del dictRef[keys[-1]]
		else :
			raise KeyError
		
		return self.data


def Node(name, unitType, path, size, parent) :
	return {
		"data" : {
			"name" : name,
			"type" : unitType,
			"size" : size,
			"path" : path,
			"parent" : parent
		}
	}


class FileSystem() :
	def __init__(self) :
		self.nodes = FileSystemDict()
		self.workingDirectory = "/"
		self.parentDirectory = ""
		self.addNode("/ (Root)", "dir", self.workingDirectory)
	
	
	def pwd(self, doPrint = True) :
		if(doPrint) :
			print(self.workingDirectory)
		return self.workingDirectory
	
	
	def cd(self, path) :
		if(path == "..") :
			if(self.parentDirectory == "") :
				print("Warning, parent does not exist")
			self.workingDirectory = self.parentDirectory
			self.parentDirectory = self.nodes[self.workingDirectory]["data"]["parent"]
		else :
			if(os.path.isabs(path)) :
				self.workingDirectory = path
			else :
				self.workingDirectory += path
				if(path[-1] != "/") :
					self.workingDirectory += "/"
			
			self.parentDirectory = self.nodes[self.workingDirectory]["data"]["parent"]
	
	
	def addNode(self, name, unitType, path, size = 0) :
		if(os.path.isabs(path)) :
			targetDirectory = path
			parentDirectory = os.path.dirname(targetDirectory[:-1])
			if(parentDirectory != "/") :
				parentDirectory += "/"
		else :
			targetDirectory = self.workingDirectory + path
			if(path[-1] != "/") :
				targetDirectory += "/"
			parentDirectory = os.path.dirname(targetDirectory[:-1])
			if(parentDirectory != "/") :
				parentDirectory += "/"
		
		if(unitType == "dir" and name[-1] != "/" and name != "/ (Root)") :
			newNode = Node(name + "/", unitType, targetDirectory, size, parentDirectory)
		else :
			newNode = Node(name, unitType, targetDirectory, size, parentDirectory)
		self.nodes[targetDirectory] = newNode
	
	
	def getChildren(self, path) :
		children = list(self.nodes[path].keys())
		children.remove("data")
		return children
	
	
	def computeDirSizes(self, path = "/") :
		children = self.getChildren(path)
		if(self.nodes[path]["data"]["type"] == "file") :
			size = self.nodes[path]["data"]["size"]
		else :
			size = 0
		
		if(children != None and len(children) > 0) :
			for i in range(len(children)) :
				size += self.computeDirSizes(self.nodes[path][children[i]]["data"]["path"])
		
		self.nodes[path]["data"]["size"] = size
		return size
	
	
	def printFS(self, path = "/", offset = "", withSlash = False, dirSizes = False) :
		currentNode = self.nodes[path]["data"]
		
		if(withSlash or currentNode["name"][-1] != "/") :
			l = len(currentNode["name"])
		else :
			l = -1
		
		if(currentNode["type"] == "dir") :
			if(dirSizes and currentNode["size"] != 0) :
				print(offset + "- " + currentNode["name"][:l] + " (dir, size=" + str(currentNode["size"]) + ")")
			else :
				print(offset + "- " + currentNode["name"][:l] + " (dir)")
		elif(currentNode["type"] == "file") :
			print(offset + "- " + currentNode["name"] + " (file, size=" + str(currentNode["size"]) + ")")
		else :
			print(offset + "- " + currentNode["name"] + " (invalid, " + currentNode["type"] + ")")
		
		children = self.getChildren(path)
		if(children != None and len(children) > 0) :
			for i in range(len(children)) :
				self.printFS(self.nodes[path][children[i]]["data"]["path"], offset + "  ", withSlash, dirSizes)
	
	
	def printDir(self, path = "/", offset = "", level = 1, withFiles = False, withSlash = False, dirSizes = False) :
		currentNode = self.nodes[path]["data"]
		
		if(withSlash or currentNode["name"][-1] != "/") :
			l = len(currentNode["name"])
		else :
			l = -1
		
		if(currentNode["type"] == "dir") :
			if(dirSizes and currentNode["size"] != 0) :
				print(offset + "- " + currentNode["name"][:l] + " (dir, size=" + str(currentNode["size"]) + ")")
			else :
				print(offset + "- " + currentNode["name"][:l] + " (dir)")
		elif(currentNode["type"] == "file" and withFiles) :
			print(offset + "- " + currentNode["name"] + " (file, size=" + str(currentNode["size"]) + ")")
		else :
			print(offset + "- " + currentNode["name"] + " (invalid, " + currentNode["type"] + ")")
		
		if(level > 0) :
			children = self.getChildren(path)
			if(children != None and len(children) > 0) :
				for i in range(len(children)) :
					self.printDir(self.nodes[path][children[i]]["data"]["path"], offset + "  ", level - 1, withFiles, withSlash, dirSizes)


def getFileSizesSmallerThanX(FS, X, path = "/") :
	children = FS.getChildren(path)
	
	sizes = []
	files = []
	if(FS.nodes[path]["data"]["type"] == "dir") :
		size_tmp = FS.nodes[path]["data"]["size"]
		if(size_tmp < X) :
			sizes += [size_tmp]
			files += [path]
	
	if(children != None and len(children) > 0) :
		for i in range(len(children)) :
			sizes_tmp, files_tmp = getFileSizesSmallerThanX(FS, X, path = FS.nodes[path][children[i]]["data"]["path"])
			for j in range(len(sizes_tmp)) :
				sizes += [sizes_tmp[j]]
				files += [files_tmp[j]]
	
	return sizes, files


def getFileSizesBiggerThanX(FS, X, path = "/") :
	children = FS.getChildren(path)
	
	sizes = []
	files = []
	if(FS.nodes[path]["data"]["type"] == "dir") :
		size_tmp = FS.nodes[path]["data"]["size"]
		if(size_tmp >= X) :
			sizes += [size_tmp]
			files += [path]
	
	if(children != None and len(children) > 0) :
		for i in range(len(children)) :
			sizes_tmp, files_tmp = getFileSizesBiggerThanX(FS, X, path = FS.nodes[path][children[i]]["data"]["path"])
			for j in range(len(sizes_tmp)) :
				sizes += [sizes_tmp[j]]
				files += [files_tmp[j]]
	
	return sizes, files


if(__name__ == "__main__") :
	filename = "data.txt"
	
	file = open(filename, "r")
	content = file.read().split("\n")
	file.close()
	
	FS = FileSystem()
	
	readContent = False
	
	for i in range(len(content)) :
		line = content[i].split(" ")
		
		if(line[0] == "$") :
			readContent = False
			if(line[1] == "cd") :
				FS.cd(line[2])
			elif(line[1] == "ls") :
				readContent = True
			else :
				print("Warning, unrecognized operation")
		elif(readContent) :
			if(line[0] == "dir") :
				FS.addNode(line[1], "dir", line[1])
			else :
				FS.addNode(line[1], "file", line[1], size = int(line[0]))
		else :
			print("Warning, unrecognized operation")
	
	usedSpace = FS.computeDirSizes()
	FS.printDir(level = 2, dirSizes = True)
	
	print()
	fileSizes, files = getFileSizesSmallerThanX(FS, 100000)
	print(sum(fileSizes))
	print()
	
	
	diskSpace = 70000000
	spaceReqs = 30000000
	
	freeSpace = diskSpace - usedSpace
	
	print("Free space =", freeSpace)
	
	space2Free = spaceReqs - freeSpace
	
	print("Space to free = ", space2Free)
	
	fileSizes, files = getFileSizesBiggerThanX(FS, space2Free)
	minSize = min(fileSizes)
	file = files[fileSizes.index(minSize)]
	
	print("Min : ", minSize, files[fileSizes.index(minSize)])
	print(FS.nodes[file]["data"])
	
	del FS.nodes[file]
	
	print()
	FS.computeDirSizes()
	FS.printDir(level = 2, dirSizes = True)










