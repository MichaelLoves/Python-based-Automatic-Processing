#encoding:utf-8
import os, sys, getopt, operator, csv, re, glob
import math, time
from copy import deepcopy

#电源电压
VDD = 1.8

#查找一个元素的所有位置
def find_index(arr, search):
	return [index for index,item in enumerate(arr) if item == search]

def find_index_2(arr, search):
	return [index for index, item in enumerate(arr) if search in item]

def extract_data(line):
	data_name, data = '', ''
	data_name = line.split('=')[0]
	raw_data = line.split('  ')[1]
	if 'e' in raw_data:
		data = float(raw_data.split('e')[0])/10**float(raw_data.split('e')[1].strip('-'))
	elif raw_data:
		data = raw_data
	else:
		data = ''
	return(data_name, data)

def is_Normal(single_result):
	#判断是否为正常波形。在 injection timing 的前一个 rise 开始之后的一个， 两个， 三个周期之内最大的电压都达到VDD则视为正常波形
	max_vol_1 = float(single_result['max_vol_1'])
	max_vol_2 = float(single_result['max_vol_2'])
	max_vol_3 = float(single_result['max_vol_3'])

	if max_vol_1 + max_vol_2 + max_vol_3 >= VDD*3:
		return(True)

def is_Transient_pulse(single_result):
	#判断是否发生 transient pulse 现象. 在 normal 的基础上, 若 fall_timing_before_pulse 迟于
	#rise_timing_before_pulse, 则视为 transient pulse 出现
	if single_result['fall_timing_before_pulse'] > single_result['rise_timing_before_pulse']:
		return(True)
	else:
		return(False)

def is_DeadlocK(single_result):
	#判断是否发生 deadlock 现象, 在注入 error pulse 之后, 没有出现第三个波的情况视为 deadlock
	if not single_result['rise_timing_3']:
		return(True)
	else:
		return(False)

def hspice_simulation(start_timing, end_timing, current_height, injection_node, output_node, input_file):

	injection_timing = float(start_timing)
	stop_timing = float(end_timing)
	#在 injection timing 的开始时间和结束时间之间进行间隔为 0.1ns 的循环
	while injection_timing <= stop_timing:
		injection_timing = round(injection_timing, 2)
		read_file = open(input_file, 'r')
		temp_file = read_file.readlines()

		#在原 sp 文件中查找定义 currentdelay 的命令行, 默认为 .param currentduration 下面的 n 行之内, n 取决于注入 node 的个数
		for line_number, line in enumerate(temp_file):
			if '.param currentduration' in line:
				for line_index, line_2 in enumerate(temp_file[line_number+2 : line_number+7]):
					#初始化原 sp 文件中的命令行, 去掉之前行开头可能有的'*'符号
					line_2.strip('*')
					if '.param currentdelay' + injection_node[1:] in line_2:
						#comment out 注入 node 所在行的命令
						temp_file[line_number+line_index+2] = '*' + line_2

		#通过替换 .param currentdelay = **n 这行命令中的 ** 来定义不同的 injection timing
		for line_number, line in enumerate(temp_file):
			if '.TRAN 1p simtime' in line and '*' not in line:
				temp_file[line_number+1] = re.sub('\s\d+\w\s', str(injection_timing) + 'n', temp_file[line_number+1])

		#替换 .MEASURE command 中的有关 injection node 的参数部分
		for line_number, line in enumerate(temp_file):
			if '.MEASURE' in line and 'currentdelay' in line:
				temp_file[line_number] = re.sub('\d{2}', injection_node[1:], line)


		#输出入力文件时, 以 injection node 和 injection timing 作为文件名保存
		write_file = open('./input_file/' + injection_node + '_' + str(injection_timing) + '.sp', 'w+')
		for item in temp_file:
			write_file.write(item)

		write_file.close()
		read_file.close()

		#injection timing 每次 shift 的间隔为 0.1ns
		injection_timing = round(injection_timing + 0.1, 2)

	#调用 input_file 文件夹中的每个 sp 文件进行一次 hspice 模拟, 输出文件的文件名与输入文件保持一致并保持在 output_file 文件夹中
	#for input_file in sorted(glob.glob('./input_file/*.sp')):
		#进行 Hspice Simulation
	#	os.system('hspice64 -hpp -mt 4 -i ' + input_file + ' -o output_file/' + input_file[-12:-3] + '.lis')


def analyze_waveform(lis_file):
	file = lis_file.readlines()
	result_list = []

	#先找到'transient analysis'所在行的行数, 用来确定每次模拟的结果在文件中所在的位置
	#以 'transient analysis'所在行作为截取上限
	for line in file:
		if re.findall(r'transient analysis', line):
			top_line_num = find_index(file, line)[0]

	#以 '100.0%time'所在行作为截取下限
	bottom_line_num = find_index_2(file, r'100.0% time =')[0]

	#根据截取上限和下限, 截取中间部分的参数数据, 并清楚空白行
	single_result = file[top_line_num + 2 : bottom_line_num]
	while ' \n' in single_result:
		single_result.remove(' \n')

	#将模拟结果保存在 single_result_dict 中, 不同的参数对应后面不同的数值
	single_result_dict = {}
	for item in single_result:
		data_name, data = extract_data(item)
		single_result_dict[data_name] = data

	#输出 single_result 内容
	#print('*'*40 + 'result_list' + '*'*40)
	#print(single_result_dict)

	#统计是否出现 deadlock
	if is_Normal(single_result_dict):
		if is_Transient_pulse(single_result_dict):
			return('transient pulse')
		else:
			return('normal')
	elif is_DeadlocK(single_result_dict):
		return('deadlock')
	else:
		return('unknown')


#用于测量程式运行时间
#程序开始时间
start_time = time.time()

#从命令行中获取 CSV 文件
#可以是储存了不同 current height 的, 也可以是储存了不同 injection timing 的 CSV 文件
#simulation_mode = 1 : fixed current height, shift injection timing
#simulation_mode = 2 : fixed injection timing, shift current height
opts, args = getopt.getopt(sys.argv[1:], "hi:c:m:")
input_file, simulation_mode, input_csv_file = '', '', ''

def usage():
	#比如 python Hspice Simulation.py -i 3NAND_2_NP_errorall.sp -m 1 -c timing.csv
	print('Usage: ' + sys.argv[0] + ' -i input_file.sp -m simulation_mode -c input_csv_file')

for op, value in opts:
	if op == '-i':
		input_file = value
	if op == '-c':
		input_csv_file = value
	if op == '-m':
		simulation_mode = value
	elif op == '-h':
		usage()
		sys.exit()


#读取 CSV 文件
CSV_file = csv.reader(open(input_csv_file, 'rU'))

#保存 CSV 文件中的输入数据
input_data = []
for line in CSV_file:
	if re.findall(r"\bstart\w*\b", ' '.join(line)):
		pass
	else:
		single_data = line[0].split(';')
		input_data.append(single_data)

print('input_data')
print(input_data)

#进行模拟之前, 清空 input_file 和 output_file 文件夹中的所有文件
for file in glob.glob('./input_file/*'):
	os.remove(file)
for file in glob.glob('./output_file/*'):
	os.remove(file)

#'''
########## 进行 hspice simulation ##########
for data in input_data:
	print('hspice_simulation')
	hspice_simulation(data[0], data[1], data[2], data[3], data[4], input_file)

#读取 output_file 文件夹中每个 .lis 文件并对其中的参数进行抽取和统计, 以便判断是否出现错误波形
#统计结果保存在 result.txt 文件之中
result_file = open('result.txt', 'w')
result_list = []

for file in sorted(glob.glob('./output_file/*.lis')):
	print('filename', file)
	lis_file = open(file, 'r')
	result = analyze_waveform(lis_file)
	result_list.extend([file + ' '*3 + result + '\n'])
	lis_file.close()
result_file.writelines(result_list)
result_file.close()
#'''


########## 对于 result.txt 文件中的结果进行统计 #########
result_file = open('result.txt', 'r+')
result = result_file.readlines()

number_of_simulation = len(result)
number_of_deadlock = 0
number_of_normal = 0
number_of_transient_pulse = 0

for line in result:
	single_result = line.split('   ', 1)
	print('single_result', single_result)	
	if single_result[1].strip('\n') == 'normal':
		number_of_normal += 1
	elif single_result[1].strip('\n') == 'deadlock':
		number_of_deadlock += 1
	elif single_result[1].strip('\n') == 'transient pulse':
		number_of_transient_pulse += 1		

result_file.write('\n\nData Analysis \n')
result_file.write('number_of_simulation : %s \n' %number_of_simulation)
result_file.write('number_of_normal : %s \n' %number_of_normal)
result_file.write('number_of_deadlock : %s \n' %number_of_deadlock)
result_file.write('number_of_transient_pulse : %s \n' %number_of_transient_pulse)


#程序结束时间
finish_time = time.time()
result_file.write('time used(s) : %s' %(finish_time - start_time))


result_file.close()

