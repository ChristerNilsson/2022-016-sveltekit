# Behövs rutin som rensar bort filer i Home och small utgående från bilder.json vid behov.
# MD5 behövs inte på webben, används bara för att hålla reda på listan med bredder och höjder.
# MD5 är bättre än löpnummer. T ex om man bytt namn på en bild, kan man hitta bilden mha MD5.
# Användaren initierar alla ändringar via Originalkatalogen. Pythonprogrammet ändrar EJ i Originalkatalogen.
# Dessa uppdaterar bilder.json, som kan minska eller öka i storlek.
# Bilder hamnar alltid i Home och small. Dessa kataloger växer hela tiden. Parametrar sparas i MD5.json
# Update = YES innebär att Home, small, bilder.json, MD5.json kan uppdateras.

import time
import json
from os import scandir, mkdir,rename
from os.path import exists, getsize
from PIL import Image
import hashlib
import shutil
import re

QUALITY = 95
WIDTH = 475

# ROOT = "C:\\github\\2022-014-Bildbanken2\\"
# Original = ROOT + "Original"       # cirka 2.000.000 bytes per bild (Readonly)
# Home     = ROOT + "public\\Home"   # cirka 2.000.000 bytes per bild
# small    = ROOT + "public\\small"  # cirka 	  25.000 bytes per bild
# JSON     = ROOT + "public\\json\\" # cirka       120 bytes per bild (bilder.json)
# MD5      = ROOT + 'MD5.json'       # cirka        65 bytes per bild

ROOT = "C:\\github\\2022-016-sveltekit\\"
Original = ROOT + "Original"       # cirka 2.000.000 bytes per bild (Readonly)
Home     = ROOT + "static\\Home"   # cirka 2.000.000 bytes per bild
small    = ROOT + "static\\small"  # cirka 	  25.000 bytes per bild
JSON     = ROOT + "static\\json\\" # cirka       120 bytes per bild (bilder.json)
MD5      = ROOT + 'MD5.json'       # cirka        65 bytes per bild

def is_jpg(key): return key.endswith('.jpg') or key.endswith('.JPG')
def is_tif(key): return key.endswith('.tif') or key.endswith('.TIF')

def dumpjson(data,f):
	s = json.dumps(data, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
	s = s.replace("],","],\n") # Varje key (katalog,fil) på egen rad.
	s = s.replace(":{",":\n{")
	s = s.replace('},"','},\n"')
	f.write(s)

def loadJSON(path):
	if not exists(path): return {}
	with open(path, 'r', encoding="utf8") as f:
		return json.loads(f.read())

def ensurePath(root,path):
	arr = path.split("\\")
	for i in range(len(arr)):
		p = root + "\\" + "\\".join(arr[0:i])
		if not exists(p): mkdir(p)

def patch(tree,path,data):
	arr = path.split("\\")
	ptr = tree
	for key in arr[1:len(arr)]:
		if key not in ptr: ptr[key] = {}
		if key != arr[-1]: ptr = ptr[key]
	if data:
		ptr[key] = data
	else:
		del ptr[key]

def makeSmall(Original,Home,small,name):

	with open(Original+name,"rb") as f:
		data = f.read()
		md5hash = hashlib.md5(data).hexdigest()

	filename = "\\" + md5hash + ".jpg"
	if md5hash in md5Register and exists(Home + filename) and exists(small + filename):
		lst = md5Register[md5hash] + [md5hash]
		patch(cache, name, lst)
		return lst

	bigImg = Image.open(Original+name)
	bigSize = getsize(Original+name)

	if bigImg.width <= 2048:
		shutil.copyfile(Original + name, Home + "\\" + md5hash + '.jpg')
	else:
		bigImg = bigImg.resize((2048, round(2048 * bigImg.height / bigImg.width)))
		bigImg.save(Home + "\\" + md5hash + '.jpg',quality=QUALITY)

	smallImg = bigImg.resize((WIDTH, round(WIDTH*bigImg.height/bigImg.width)))
	smallImg.save(small + "\\" + md5hash + '.jpg',quality=QUALITY)
	lst = [smallImg.width, smallImg.height, bigSize, bigImg.width, bigImg.height]
	md5Register[md5hash] = lst
	patch(cache, name, lst + [md5hash])
	return lst

def expand(a,d):
	antal = {'images':0, 'folders':0}
	i = 0
	for key in a.keys():
		if key not in d:
			if is_jpg(key):
				start = time.perf_counter()
				d[key] = makeSmall(Original, Home, small, key)
				print(f'{i:6.0f} {1000 * (time.perf_counter() - start):6.0f}', key)
				i += 1
			else:
				antal['folders'] += 1

	print()
	antal['images'] = i
	return antal

def shrink(d,a):
	antal = {'images':0, 'folders':0, 'keys':0}
	keys = list(d.keys())
	keys = reversed(keys)
	for key in keys:
		if key not in a: # Original
			patch(cache, key, None)
			if is_jpg(key):
				antal['images'] += 1
			else:
				antal['folders'] += 1
	return antal

def fixMisspellings(root, path, namn,doit=False):

	namn1 = re.sub(".jpg", "", namn)
	namn1 = re.sub(".JPG", "", namn1)
	namn0 = namn1
	namn1 = re.sub("___", "__", namn1)
	namn1 = re.sub("__", "_", namn1)
	namn1 = re.sub("_ ","_",namn1)
	namn1 = re.sub(" _","_",namn1)
	namn1 = re.sub("  "," ",namn1)
	namn1 = re.sub("_Von_","_von_",namn1)

	if namn0 == namn1: return namn

	path1 = root + path + "\\"
	counter = ""
	if exists(path1 + namn1 + '.jpg'):
		counter = 1
		while exists(path1 + namn1 + "-" + str(counter) + '.jpg'):
			counter += 1
	print("")
	print(path1 + namn)
	if counter == "":
		print(path1 + namn1 + '.jpg')
		if doit: rename(path1 + namn, path1 + namn1 + '.jpg')
	else:
		print(path1 + namn1 + "-" + str(counter) + '.jpg')
		if doit: rename(path1 + namn, path1 + namn1 + "-" + str(counter) + '.jpg')
	return namn1 + '.jpg'

def flat(root, res={}, path=""):
	ensurePath(root, path)
	for name in [f for f in scandir(root + "\\" + path)]:
		namn = name.name

		# if not name.is_dir():
		# 	namn = fixMisspellings(root,path,namn,False)

		path1 = path + "\\" + namn
		if name.is_dir():
			res[path1] = ""
			flat(root, res, path1)
		elif is_jpg(namn):
			res[path1] = ""
		else:
			print("*** Ignored file:", "public\\Home" + path1)
	return res

def flatten(node, res={}, path=''):
	for key in node:
		path1 = path + "\\" + key
		if is_jpg(key):
			res[path1] = node[key]
		else:
			res[path1] = ""
		if not type(node[key]) is list:
			flatten(node[key],res, path1)
	return res

def compare(a,b,message):
	res = {}
	cimages = 0
	cfolders = 0
	for path in a:
		if path not in b:
			if is_jpg(path):
				if cimages == 0: res[path] = 0
				cimages += 1
			else:
				res[path] = 0
				cfolders += 1
	if cfolders > 0 or cimages > 0:
		print(message, cimages, 'images +', cfolders, 'folders')
	return res

def compare2(x,y):
	res = {}
	res['missing'] = compare(x, y, 'Missing:')
	res['surplus'] = compare(y, x, 'Surplus:')
	return res

def countFolders(arr):
	antal = 0
	for key in arr:
		if not is_jpg(key): antal += 1
	return antal

hash = {}
letters = list("+!§()0123456789_,.-¤")
# stoppord = ''.split(' ')

def flatWords(node):
	for key in node:
		words = key
		for letter in letters:
			words = words.replace(letter," ")
		for word in words.split(' '):
			wordLower = word.lower()
			if len(word) > 1 and wordLower == word:
				hash[word] = hash[word]+1 if word in hash else 1
		if type(node[key]) is dict: flatWords(node[key])

def convert(hash):
	arr = []
	for key in hash.keys():
		arr.append([hash[key],key])
	arr = sorted(arr)
	return arr

######################

# for i in range(100):
# 	time.sleep(0.1)
# 	print ("\rComplete: ", i, "%", end="")
# print ("\rComplete: 100%")

start = time.time()

md5Register = loadJSON(MD5) # givet md5key får man listan med sex element
cache = loadJSON(JSON + 'bilder.json')

a = flat(Original, {}) # Readonly!           Skickas INTE till GCS
b = flat(Home)   # Används bara för räkning. Skickas dock till GCS
c = flat(small)  # Används bara för räkning. Skickas dock till GCS
d = flatten(cache, {}) #                     Skickas till GCS

print()
ca = countFolders(a)
cb = countFolders(b)
cc = countFolders(c)
cd = countFolders(d)

print('Original:', len(a) - ca, 'images +', ca, 'folders')
print('Cache:   ', len(d) - cd, 'images +', cd, 'folders', )
print()
print('Home:    ', len(b),      'images')
print('Small:   ', len(c),      'images')

print()
resCache = compare2(a,d)

print()
for key in resCache['missing'].keys(): print('Missing:', key)
print()
for key in resCache['surplus'].keys(): print('Surplus:', key)

print('Readonly:', round(time.time()-start,3),'seconds')
print()
update = input('Update? (NO/Yes) ').upper()
update = update.startswith('Y')

if update:

	start = time.time()
	print()
	antal = expand(a,d)
	print()
	if antal['images'] > 0: print('Added:', antal['images'], 'images')

	antal = shrink(d,a)
	if antal['images'] > 0: print('Deleted:', antal['images'], 'images')

	if antal['keys'] > 0: print('Deleted:', antal['keys'], 'keys')

	with open(JSON + 'bilder.json', 'w', encoding="utf8") as f: dumpjson(cache,f)
	with open(MD5, 'w', encoding="utf8") as f: dumpjson(md5Register,f)
	print()
	print(round(time.time() - start,3),'seconds')
