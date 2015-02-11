#encoding:utf-8
import csv
import os, sys, getopt, operator


#获取命令行， 并赋值到input_file和output_file
opts, args = getopt.getopt(sys.argv[1:], "hi:")
input_file = ''

def usage():
	print('Usage: ' + sys.argv[0] + ' -i input_file')

for op, value in opts:
	if op == '-i':
		input_file = value
	elif op == '-h':
		usage()
		sys.exit()



file = csv.reader(open(input_file, 'rU'), delimiter = ' ')
for row in file:
	print(row)
	line = row[0].split(';')
	#print('line', line)
	start_height = line[0]
	end_height = line[1]
	interval = line[2]
	#print('start_height', start_height)
	#print('end_height', end_height)
	#print('interval', interval)

with open(input_file) as csvfile:
	file = csvfile.readlines()
	temp_file = file[0].split('\r')
	for line in temp_file[1:]:
		print(line)