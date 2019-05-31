import argparse
import os
import sys
import numpy as np

from PIL import Image, ImageFilter

SIMILARITY_THRESHOLD = 40

all_files = []
nz_indices = []
pairs = []

def make_fingerprint(file):
	img = Image.open(file) \
	.resize((160,160)) \
	.convert('L').resize((16,16)) \
	.convert('1')
	img_np = np.array(img).flatten()
	nz_indices.append(img_np)

def intersection_diff(arr1, arr2):
    return np.count_nonzero(np.bitwise_xor(arr1, arr2))

def make_pairs():
	for i, val in enumerate(nz_indices):
		similar_ids = []
		for j, val2 in enumerate(nz_indices[(i+1):]):
			if (intersection_diff(val, val2) < SIMILARITY_THRESHOLD):
				similar_ids.append(j+i+1)
		pairs.append(similar_ids)

def print_similar():
	for i, pair_ids in enumerate(pairs):
		for idx in pair_ids:
			print(F"{all_files[i]} {all_files[idx]}")


parser = argparse.ArgumentParser(usage='solution.py [-h] --path PATH',
		description='First test task on images similarity.')
parser.add_argument('--path', dest='PATH',
                   help='folder with images')

args = parser.parse_args()
if args.PATH is None:
   	parser.error("the following arguments are required: --path")
else:
	folder = args.PATH
	
with os.scandir(folder) as files:
   for file in files:
       filename = file.name
       all_files.append(filename)
       abs_path = folder+ "\\" + filename
       make_fingerprint(abs_path)

make_pairs()
print_similar()