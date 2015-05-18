#encoding:utf-8
import os, sys, getopt, operator, csv, re, glob
import math, time
from copy import deepcopy

#电源电压
VDD = float(1.8)

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
		#把原本的 string 类型转换为 float 类型, 好方便于之后的数值比较
		data = float(raw_data)
	else:
		#若在 .lis 文件中的结果为 failed (null)
		data = ''
	return(data_name, data)


def is_Normal(single_result):
	#判断是否为正常波形
	#在n_and_3_timing3之后三个周期内的pulse_width与之前的测量结果n_and_3_pulse_width大致相同 且最大电压约为VDD
	#且cd_3, cd_4的波形也为正常

	#确定 cd_3 的 pulse_width
	if single_result['cd_3_pulse_width_after_pulse_1'] > 0:
		cd_3_pulse_width_after_pulse = single_result['cd_3_pulse_width_after_pulse_1']
	else:
		cd_3_pulse_width_after_pulse = single_result['cd_3_pulse_width_after_pulse_2']

	#确定 cd_4 的 pulse_width
	if single_result['cd_4_pulse_width_after_pulse_1'] > 0:
		cd_4_pulse_width_after_pulse = single_result['cd_4_pulse_width_after_pulse_1']
	else:
		cd_4_pulse_width_after_pulse = single_result['cd_4_pulse_width_after_pulse_2']

	#确定在injection timing之后三个周内各自的n_and_3_pulse_width_after_pulse
	if single_result['n_and_3_pulse_width_after_pulse_in_period1_1'] > 0:
		n_and_3_pulse_width_after_pulse_in_period1 = single_result['n_and_3_pulse_width_after_pulse_in_period1_1']
	else:
		n_and_3_pulse_width_after_pulse_in_period1 = single_result['n_and_3_pulse_width_after_pulse_in_period1_2']

	if single_result['n_and_3_pulse_width_after_pulse_in_period2_1'] > 0:
		n_and_3_pulse_width_after_pulse_in_period2 = single_result['n_and_3_pulse_width_after_pulse_in_period2_1']
	else:
		n_and_3_pulse_width_after_pulse_in_period2 = single_result['n_and_3_pulse_width_after_pulse_in_period2_2']
		
	if single_result['n_and_3_pulse_width_after_pulse_in_period3_1'] > 0:
		n_and_3_pulse_width_after_pulse_in_period3 = single_result['n_and_3_pulse_width_after_pulse_in_period3_1']
	else:
		n_and_3_pulse_width_after_pulse_in_period3 = single_result['n_and_3_pulse_width_after_pulse_in_period3_2']


	'''
	print('is normal')
	print('1', single_result['n_and_3_rise_timing_1'] < single_result['error_pulse_injection_timing'] + single_result['n_and_3_period'] ) 
	print('2', single_result['n_and_3_pulse_width']*0.9 < n_and_3_pulse_width_after_pulse_in_period1 and \
	n_and_3_pulse_width_after_pulse_in_period1 < single_result['n_and_3_pulse_width']*1.1 )
	print('3', single_result['n_and_3_pulse_width']*0.9 < n_and_3_pulse_width_after_pulse_in_period2 and \
	n_and_3_pulse_width_after_pulse_in_period2 < single_result['n_and_3_pulse_width']*1.1 ) 
	print('4', single_result['n_and_3_pulse_width']*0.9 < n_and_3_pulse_width_after_pulse_in_period3 and \
	n_and_3_pulse_width_after_pulse_in_period3 < single_result['n_and_3_pulse_width']*1.1 )
	print('5', VDD*0.9 < single_result['n_and_3_max_vol_after_pulse_in_period1'] and \
	single_result['n_and_3_max_vol_after_pulse_in_period1'] < VDD*1.1 ) 
	print('6', VDD*0.9 < single_result['n_and_3_max_vol_after_pulse_in_period2'] and \
	single_result['n_and_3_max_vol_after_pulse_in_period2'] < VDD*1.1 )
	print('7', VDD*0.9 < single_result['n_and_3_max_vol_after_pulse_in_period3'] and \
	single_result['n_and_3_max_vol_after_pulse_in_period3'] < VDD*1.1 )
	print('8', single_result['cd_3_pulse_width']*0.7 < cd_3_pulse_width_after_pulse and \
	cd_3_pulse_width_after_pulse < single_result['cd_3_pulse_width']*1.3 )
	print('9', single_result['cd_3_rise_timing_after_pulse_1'] < single_result['error_pulse_injection_timing'] + single_result['cd_3_period'] )
	print('10', single_result['cd_4_pulse_width']*0.7 < cd_4_pulse_width_after_pulse and \
	cd_4_pulse_width_after_pulse < single_result['cd_4_pulse_width']*1.3 )
	print('11', single_result['cd_4_rise_timing_after_pulse_1'] < single_result['error_pulse_injection_timing'] + single_result['cd_4_period'] )
	print('12', single_result['n_nand_3_max_vol_after_pulse'] < VDD*0.5 or \
	single_result['n_nand_4_max_vol_after_pulse'] < VDD*0.5)
	#'''	

	#关于 n_and_3, cd_3, cd_4, n_nand_3, n_nand_4 的判断
	if ( single_result['n_and_3_rise_timing_1'] < single_result['error_pulse_injection_timing'] + single_result['n_and_3_period'] ) and \
	( single_result['n_and_3_pulse_width']*0.7 < n_and_3_pulse_width_after_pulse_in_period1 and \
	n_and_3_pulse_width_after_pulse_in_period1 < single_result['n_and_3_pulse_width']*1.3 ) and \
	( single_result['n_and_3_pulse_width']*0.7 < n_and_3_pulse_width_after_pulse_in_period2 and \
	n_and_3_pulse_width_after_pulse_in_period2 < single_result['n_and_3_pulse_width']*1.3 ) and \
	( single_result['n_and_3_pulse_width']*0.7 < n_and_3_pulse_width_after_pulse_in_period3 and \
	n_and_3_pulse_width_after_pulse_in_period3 < single_result['n_and_3_pulse_width']*1.3 ) and \
	( VDD*0.9 < single_result['n_and_3_max_vol_after_pulse_in_period1'] and \
	single_result['n_and_3_max_vol_after_pulse_in_period1'] < VDD*1.1 ) and \
	(VDD*0.9 < single_result['n_and_3_max_vol_after_pulse_in_period2'] and \
	single_result['n_and_3_max_vol_after_pulse_in_period2'] < VDD*1.1 ) and \
	(VDD*0.9 < single_result['n_and_3_max_vol_after_pulse_in_period3'] and \
	single_result['n_and_3_max_vol_after_pulse_in_period3'] < VDD*1.1 ) and \
	(single_result['cd_3_pulse_width']*0.7 < cd_3_pulse_width_after_pulse and \
	cd_3_pulse_width_after_pulse < single_result['cd_3_pulse_width']*1.3 ) and \
	(single_result['cd_3_rise_timing_after_pulse_1'] < single_result['error_pulse_injection_timing'] + single_result['cd_3_period'] ) and \
	(single_result['cd_4_pulse_width']*0.7 < cd_4_pulse_width_after_pulse and \
	cd_4_pulse_width_after_pulse < single_result['cd_4_pulse_width']*1.3 ) and \
	(single_result['cd_4_rise_timing_after_pulse_1'] < single_result['error_pulse_injection_timing'] + single_result['cd_4_period'] ):
		return(True)
	'''
	# and \
	(single_result['n_nand_3_max_vol_after_pulse'] < VDD*0.5 or \
	single_result['n_nand_4_max_vol_after_pulse'] < VDD*0.5):
		#return(True)
	'''

def is_DeadlocK(single_result):
	#判断是否发生 deadlock 现象, 在注入 error pulse 之后, 没有出现第三个波的情况视为 deadlock
	if not single_result['n_and_3_rise_timing_3']:
		return(True)
	else:
		return(False)

def is_11_error(single_result):
	#在 normal operation 的情况下, n_nand_3 和 n_nand_4的输出为1
	#设置阈值为vdd*0.5的根据在Evernote笔记中有所记录
	
	#'''
	print('is 11 error')
	print('1', single_result['n_and_3_max_vol_after_pulse_in_period1'] > VDD*0.5 )
	print('2', single_result['n_nand_3_max_vol_after_pulse'] > VDD*0.5 )
	print('3', single_result['n_nand_4_max_vol_after_pulse'] > VDD*0.5)
	#'''

	if single_result['n_and_3_max_vol_after_pulse_in_period1'] > VDD*0.5 and \
	single_result['n_nand_3_max_vol_after_pulse'] > VDD*0.5 and \
	single_result['n_nand_4_max_vol_after_pulse'] > VDD*0.5:
		return(True)

def is_wrong_output(single_result):
	#在cd信号正常的情况下(cd_3和cd_4波形正常)，应该有输出的n_and_3 和 n_and_4 为0, 且n_nand_3 和 n_nand_4 的输出为1, 则视为发生了出力的反转
	#cd信号正常:在injection timing+period之内rise, 且pulse width正常
	#波形特征 : n_and_3和 n_and_4的第一次 rise_timing 不在 injection timing+period 范围之内
 	#而 n_nand_3和 n_nand_4在 injection timing+period 范围内有波峰 

	#确定 CD_3 的 pulse_width
	if single_result['cd_3_pulse_width_after_pulse_in_period1_1'] > 0:
		cd_3_pulse_width_after_pulse_in_period1 = single_result['cd_3_pulse_width_after_pulse_in_period1_1']
	else:
		cd_3_pulse_width_after_pulse_in_period1 = single_result['cd_3_pulse_width_after_pulse_in_period1_2']

	#确定 CD_4 的 pulse_width
	if single_result['cd_4_pulse_width_after_pulse_1'] > 0:
		cd_4_pulse_width_after_pulse = single_result['cd_4_pulse_width_after_pulse_1']
	else:
		cd_4_pulse_width_after_pulse = single_result['cd_4_pulse_width_after_pulse_2']

	#'''
	print('1', single_result['cd_3_rise_timing_after_pulse_1'] < single_result['error_pulse_injection_timing'] + single_result['cd_3_period'] )
	print('2', cd_3_pulse_width_after_pulse > single_result['cd_3_pulse_width'] * 0.7 and cd_3_pulse_width_after_pulse < single_result['cd_3_pulse_width'] * 1.3 ) 
	print('3', single_result['cd_4_rise_timing_after_pulse_1'] < single_result['error_pulse_injection_timing'] + single_result['cd_4_period'] ) 
	print('4', cd_4_pulse_width_after_pulse > single_result['cd_4_pulse_width'] * 0.7 and cd_4_pulse_width_after_pulse < single_result['cd_4_pulse_width'] * 1.3 )
	print('5', not ( ( single_result['n_and_3_rise_to_vdd_timing_after_pulse'] < single_result['error_pulse_injection_timing'] + single_result['n_and_3_period'] and \
	single_result['n_and_3_pulse_width']*0.7 < n_and_3_pulse_width_after_pulse_in_period1 and \
	n_and_3_pulse_width_after_pulse_in_period1 < single_result['n_and_3_pulse_width']*1.3 ) and \
	single_result['n_nand_3_max_vol_after_pulse'] < VDD*0.5 ) )
	print()
	#'''

	#关于cd_3, cd_4, n_and_3 的判断
	if ( (single_result['cd_3_rise_timing_after_pulse_1'] < single_result['error_pulse_injection_timing'] + single_result['cd_3_period'] ) and \
	(cd_3_pulse_width_after_pulse > single_result['cd_3_pulse_width'] * 0.7 and cd_3_pulse_width_after_pulse < single_result['cd_3_pulse_width'] * 1.3 ) and \
	(single_result['cd_4_rise_timing_after_pulse_1'] < single_result['error_pulse_injection_timing'] + single_result['cd_4_period'] ) and \
	(cd_4_pulse_width_after_pulse > single_result['cd_4_pulse_width'] * 0.7 and cd_4_pulse_width_after_pulse < single_result['cd_4_pulse_width'] * 1.3 ) and \
	not ( single_result['n_and_3_rise_to_vdd_timing_after_pulse'] < single_result['error_pulse_injection_timing'] + single_result['n_and_3_period'] and \
	single_result['n_and_3_pulse_width']*0.7 < n_and_3_pulse_width_after_pulse_in_period1 and \
	n_and_3_pulse_width_after_pulse_in_period1 < single_result['n_and_3_pulse_width']*1.3 ) and \
	single_result['n_nand_3_max_vol_after_pulse'] < VDD*0.5 ):
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

		#在原 sp 文件中查找定义 injection timing 的命令行
		injection_timing_line_index = find_index_2(temp_file, 'injection timing delay')
		for line_index, line in enumerate(temp_file[injection_timing_line_index[0]+1 : injection_timing_line_index[1]]):
			#初始化原 sp 文件中的命令行, 去掉之前行开头可能有的'*'符号
			line.strip('*')
			if '.param injection_timing_' + injection_node in line:
				#comment out 注入 node 所在行的命令
				temp_file[injection_timing_line_index[0] + line_index + 1] = '*' + line
				#并把本行命令保存下来, 在下面的部分使用
				injection_timing_option = line.split(' ')

		#通过替换 .param currentdelay = **n 这行命令中的 ** 来定义不同的 injection timing
		for line_number, line in enumerate(temp_file):
			if '.TRAN 1p simtime' in line and '*' not in line:
				injection_timing_option[3] = str(injection_timing) + 'n'
				temp_file[line_number+1] = ' '.join(injection_timing_option)

		#替换 .MEASURE command 中的有关 injection node 的参数部分
		for line_number, line in enumerate(temp_file):
			if '.MEASURE' in line and 'injection_timing' in line:
				measure_command = line.split(' ')
				for part_num, part in enumerate(measure_command):
					if 'injection_timing_' in part:
						old_part = part.split('injection_timing_')
						temp = injection_node + old_part[-1][2:]
						new_part = old_part[0] + 'injection_timing_' + temp
						measure_command[part_num] = new_part
				temp_file[line_number] = ' '.join(measure_command)


		#输出入力文件时, 以 injection node 和 injection timing 作为文件名保存
		write_file = open('./input_file/' + injection_node + '_' + str(injection_timing) + '.sp', 'w+')
		for item in temp_file:
			write_file.write(item)

		write_file.close()
		read_file.close()

		#injection timing 每次 shift 的间隔为 0.1ns
		injection_timing = round(injection_timing + 0.1, 2)

	#调用 input_file 文件夹中的每个 sp 文件进行一次 hspice 模拟, 输出文件的文件名与输入文件保持一致并保持在 output_file 文件夹中
	for input_file in sorted(glob.glob('./input_file/' + injection_node + '*.sp')):
		#进行 Hspice Simulation
		os.system('hspice64 -hpp -mt 4 -i ' + input_file + ' -o output_file/' + input_file[-12:-3] + '.lis')
		

def analyze_waveform(lis_file):
	#print('analyze waveform : lis file', lis_file)
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
		if is_11_error(single_result_dict):
			return('11 error')
		else:
			return('normal')
	elif is_DeadlocK(single_result_dict):
		return('deadlock')
	elif is_wrong_output(single_result_dict):
		return('wrong output')
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

'''
#进行模拟之前, 清空 input_file 和 output_file 文件夹中的所有文件
for file in glob.glob('./input_file/*'):
	os.remove(file)
for file in glob.glob('./output_file/*'):
	os.remove(file)
#'''

'''
########## 进行 hspice simulation ##########
for data in input_data:
	hspice_simulation(data[0], data[1], data[2], data[3], data[4], input_file)
#'''

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

result_file.write('\n\nData Analysis\n')


for data in input_data:
	injection_node = data[3]

	#从所有的 result 中抽出关于 injection node 有关系的信息
	injection_node_result = []
	for line in result:
		if injection_node in line:
			injection_node_result.append(line)

	#对于抽出的信息组成的列表进行统计
	number_of_simulation = len(injection_node_result)
	number_of_deadlock = 0
	number_of_normal = 0
	number_of_11_error = 0
	number_of_wrong_output = 0
	number_of_unknown = 0

	for part in injection_node_result:
		single_result = part.split('   ', 1)	
		if single_result[1].strip('\n') == 'normal':
			number_of_normal += 1
		elif single_result[1].strip('\n') == 'deadlock':
			number_of_deadlock += 1
		elif single_result[1].strip('\n') == '11 error':
			number_of_11_error += 1
		elif single_result[1].strip('\n') == 'wrong output':
			number_of_wrong_output += 1
		else:
			number_of_unknown += 1	

	result_file.write('injection node : ' + injection_node + '  ' + 'injection timing : ' + data[0] + '--' + data[1] +'ns' + '\n')
	result_file.write('number of simulation : %s \n' %number_of_simulation)
	result_file.write('number of normal : %s \n' %number_of_normal)
	result_file.write('number of deadlock : %s \n' %number_of_deadlock)
	result_file.write('number of 11 error : %s \n' %number_of_11_error)
	result_file.write('number of wrong output: %s \n' %number_of_wrong_output)
	result_file.write('number of unknown : %s \n\n' %number_of_unknown)


#程序结束时间
finish_time = time.time()
result_file.write('time used(s) : %s' %(finish_time - start_time))


result_file.close()
