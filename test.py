import os, json, hashlib

def calcHash(filePath):
	hashVal = hashlib.sha1()
	block_size = 4 * 1024
	with open(filePath, mode="rb") as fh:
		while True:
			x = fh.read(block_size)
			if len(x)==0:	break
			hashVal.update(x)
	return hashVal.hexdigest()

def safeLoad(fileToUpdate, diffFile):
	df = open(diffFile, mode="rt", encoding="ASCII")
	security = [df.readline().strip()
	for _ in range(2)]
	print(security)
	if not calcHash(fileToUpdate) in security:
		raise PermissionError
	diff = json.load(df)
	df.close()
	return diff

def diff_files(OLD, NEW):
	diff = dict()																# data struct to store charcaterwise diffs
	times = max(map(lambda x: os.stat(x).st_size, [OLD, NEW]))					# ensure loop runs enough to cover the larges file
	old = open(OLD, mode="rt", encoding="ASCII")								# uint_8 not rune
	new = open(NEW, mode="rt", encoding="ASCII")
	with old, new:
		for _ in range(times):
			o = old.read(1)														# ??? reads 1 char and not 1 byte
			n = new.read(1)
			# characters match and neither is NULL; no problems, move on
			if o == n and o+n != "":				continue
			else:
				# case:	new file has ended
				if n is "":
					diff[_]	 = [o, None]											# !! ctor, i.e. {posn: [delete, insert]}.. note that _ here is index so enum() isn't needed
					# speed hack
					diff[_][0]+= old.read()
					break
				# case:	old file has ended
				elif o is "":
					diff[_] = [None, n]
					# speed hack
					diff[_][1]+= new.read()
					break
				else:
					diff[_] = [o, n]
	return diff																	# data structure ====>   [delete, insert] @ that position

def merge(old, diffFile, new):
	diff = safeLoad(old, diffFile)
	posn, ans = -1, str()
	toUpdate = open(old, mode="rt")
	with toUpdate:
		while True:
			x = toUpdate.read(1)
			posn+=1
			try:
				operation = diff[  posn  ]
				insert_ed = operation[1]
				x = insert_ed
				if insert_ed == None:
					x = ""
			except KeyError:
				if not x:	break
			ans+= x
	updatedF = open(new, mode="wt")
	with updatedF:
		updatedF.write(ans)
	return

def makeDiffFile(diffObj, From, to):
	src = calcHash(From)
	dest = calcHash(to)
	diffFileName = src[:5]+"__"+src[-3:]+"-"+dest[:5]+"__"+dest[-3:]+".diff"
	with open(diffFileName, mode="wt") as fh:
		fh.write(src+"\n")
		fh.write(dest+"\n")
		json.dump(diffObj, fh)
	return diffFileName

def interact():
	ch = input("What ould you like to do?\n\t1. [d]iff\n\t2. [m]erge\nchoice >>> ")
	if ch == "1":
		old = input("Enter path to old version:\t")
		new = input("Enter path to new version:\t")
		diffObj = diff_files(old, new)
		print(diffObj)
		df = makeDiffFile(diffObj, old, new)
		print("diff stored in %s" % df)
	else:
		f = input("Enter path to base file:\t")
		d = input("Enter path to diff file:\t")
		n = input("Enter path to  new file:\t")
		merge(f, d, n)
	return
