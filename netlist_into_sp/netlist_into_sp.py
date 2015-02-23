#encoding:utf-8
import os, sys, getopt, operator, re

#读取 netlist_sim 和 sp 文件 
opts, args = getopt.getopt(sys.argv[1:], "hi:o:")
input_file, output_file = '', ''

def usage():
	print('Usage: ' + sys.argv[0] + ' -i netlist_sim -o ***.sp')

for op, value in opts:
	if op == '-i':
		input_file = value
	if op == '-o':
		output_file = value
	elif op == '-h':
		usage()
		sys.exit()


#读取原 netlist_sim 文件 并将去除了 i66等 所在行的文件储存在 new_netlist_sim_file 中
netlist_sim_file = open(input_file, 'r')
new_netlist_sim_file = []

for line in netlist_sim_file.readlines()[1:]: #略过 netlist_sim 文件中第一行的空白行
	if re.findall(r"\bi\d{2}\w*\b", line):
		pass
	else:
		new_netlist_sim_file.append(line)

netlist_sim_file.close()


#用 new_netlist_sim_file 替换 sp 文件中的 netlist_sim 部分
sp_file = open(output_file, 'r')
temp_file = sp_file.readlines()

#找出 netlist_sim 文件中 ***netlist_sim*** 部分所在的两行的行数
#查出一个元素在 list 中的所有位置
def find_all_index(array, item):
	return [index for index, element in enumerate(array) if element == item]

for line in temp_file:
	if 'netlist_sim' in line:
		netlist_sim_line = line

start_line, end_line = find_all_index(temp_file, netlist_sim_line)

#替换两行 ***netlist_sim*** 中的部分
temp_file[start_line+3 : end_line-2] = new_netlist_sim_file

#将替换后的文件重新写入
write_file = open(output_file, 'w')
for line in temp_file:
	write_file.write(line)

write_file.close()
sp_file.close()
