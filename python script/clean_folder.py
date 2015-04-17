import os, glob

for file in glob.glob('./input_file/*'):
	os.remove(file)

for file in glob.glob('./output_file/*'):
	os.remove(file)
