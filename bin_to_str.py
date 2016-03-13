import os
import random
import base64


def detect(filename):
	FILE_IS = "text"
	fileSize = os.stat(filename).st_size
	points = [random.randint(0, fileSize) for _ in range(10)]
	incoming = open(filename, mode="rt", encoding="ASCII")
	with incoming:
		for aPoint in points:
			incoming.seek(aPoint)
			try:
				x = incoming.read(1)
			except UnicodeDecodeError:
				FILE_IS = "binary"
				break
	return FILE_IS

def doer():
	ch = lambda binary: base64.b64encode(binary)
	filename = input("file:\t")
	mime = detect(filename)
	if mime == "binary":
		fpSrc = open(filename, mode="rb")			# implement lazy read here
		fpDest= open(filename+".base64", mode="wt", encoding="ASCII")
		with fpSrc, fpDest:
			x = fpSrc.read()
			fpDest.write(ch(x).decode())
	else:
		print("its ok, after all its pure text")
	return

if __name__ == '__main__':
	random.seed(os.urandom(100))
	doer()
