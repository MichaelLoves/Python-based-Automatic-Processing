#encoding:utf-8
import os, sys, getopt, operator

#获取命令行， 并赋值到input_file和output_file
opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["start=", "end=", "in="])
input_file, output_file = '', ''
start_height, end_height, interval = '', '', ''

def usage():
	print('Usage: ' + sys.argv[0] + ' -i input_file -o output_file --start=start_height --end=end_height --in=interval')

if len(sys.argv) < 8:
	usage()
	sys.exit()

for op, value in opts:
	if op == '-i':
		input_file = value
	elif op == '-o':
		output_file = value
	elif op == '--start':
		start_height = value + 'e-6'
	elif op == '--end':
		end_height = value + 'e-6'
	elif op == '--in':
		interval = value + 'e-6'
	elif op == '-h':
		usage()
		sys.exit()



##找出文件中以.TRAN开头的一行，并指定其中的参数
##currentheight的开始高度，结束高度，变化间隔

#读入 input_file
with open(input_file, 'r') as read_file:

	#temp_file 作为一个缓存, 储存 input_file 的所有行
	temp_file = read_file.readlines()

	#修改 temp_file 中以 .TRAN 开头的行中的参数
	for line in temp_file:
		if '.TRAN' in line:
			TRAN_option = line.split(' ') #['.TRAN', '1p', 'simtime', 'sweep', 'currentheight', '-300e-6', '-400e-6', '-10e-6\n']
			#确定此行所在位置, 用于最末尾的替换操作
			line_number = temp_file.index(line)
			new_option = TRAN_option[:5]
			new_option.append(start_height)
			new_option.append(end_height)
			new_option.append(interval)
			#把列表再次转换为 STRING 类型进行储存
			temp_file[line_number] = ' '.join(new_option) + '\n'

	#以写模式打开 input_file, 但先把文件内容进行清空
	with open(input_file, 'w') as output_file:
		for line in temp_file:
			output_file.write(line)


#执行模拟
#os.system('hspice64 -hpp -mt 4 -i ' + input_file + ' -o ./waveform/' + output_file)

