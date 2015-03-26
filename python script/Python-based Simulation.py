 #encoding:utf-8
import os, sys, getopt, operator, csv, re
import math
from copy import deepcopy

#查找一个元素的所有位置
def find_all_index(arr, search):
	return [index for index,item in enumerate(arr) if item == search]

def find_all_index_2(arr, search):
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


def shift_timing(start_timing, end_timing, current_height, injection_node, output_node, input_file, sim_time):
	read_file = open(input_file, 'r')
	temp_file = read_file.readlines()

	#通过 injection_node 参数在 sp 文件中找到与其对应的 currentdelay** 参数, 用于替换 .TRAN option
	for line in temp_file:
		if injection_node in line:
			node_delay_time = line.split(' ')[6]
	
	for line_number, line in enumerate(temp_file):
		#修改 TRAN 命令
		if '.TRAN' in line:
			TRAN_option = line.split(' ')

			#定义新的 TRAN_option
			new_TRAN_option = ['.TRAN', '1p', 'simtime', 'sweep', node_delay_time]
			new_TRAN_option.append(start_timing + 'n')
			new_TRAN_option.append(end_timing + 'n')
			#shift timing 默认的间隔为0.1ns
			new_TRAN_option.append('0.1n')

			#把列表再次转换为 STRING 类型进行储存
			temp_file[line_number] = ' '.join(new_TRAN_option) + '\n'

		#修改 currentheight 的数值
		elif '.param currentheight' in line:
			current_height_option = line.split(' ', 4)
			new_current_height_option = current_height_option[:3]
			new_current_height_option.append(current_height + 'e-6' + '  ')
			new_current_height_option.append(current_height_option[-1].strip(' '))
			temp_file[line_number] = ' '.join(new_current_height_option)			
			
		#将所有 node 的 currentdelay 都修改为 simtime
		elif '.param currentdelay' in line:
			currentdelay_option = line.split(' ')
			new_currentdelay_option = currentdelay_option[:3]
			new_currentdelay_option.append('simtime')
			new_currentdelay_option.extend(['  ' + currentdelay_option[-1]])
			temp_file[line_number] = ' '.join(new_currentdelay_option)
	
		elif '.param mvdd' in line:
			VDD = float(line.split(' ')[-1].strip('\n'))

	#以写模式打开 input_file, 但先把文件内容进行清空
	output_file = open(input_file, 'w')
	for line in temp_file:
		output_file.write(line)
	output_file.close()

	#'''
	#进行 Hspice Simulation
	os.system('hspice64 -hpp -mt 4  -i ' + input_file + ' -o ../waveform/shift_timing_result-' + start_timing + '-' + end_timing + '.lis')
	read_file.close()

	#读取.lis文件统计错误率
	file = open('../waveform/shift_timing_result-' + start_timing + '-' + end_timing + '.lis', 'r')
	lis_file = file.readlines()

	#sim_times : 进行模拟的总次数    error_times : 出现错误的总次数
	#出现错误的标准：利用Hspice自带的.MEASURE命令对于特定端子进行检测
	#端子的输出值为maxval后面的数字， 若此值低于0.1V(此值的设定可以进行进一步考虑)， 则认为是出现了错误
	sim_times, error_times = 0, 0
	for line in lis_file:
		if (output_node + '_minvol') in line:
			sim_times += 1
			signal_min_voltage = line.split(' ')[2]
			
			if 'e' in signal_min_voltage:
				e_index = signal_min_voltage.index('e')
				e_number = float(signal_min_voltage[-1])
				min_voltage = float(signal_min_voltage[:e_index])/10**e_number
			else:
				min_voltage = float(signal_min_voltage)

			if min_voltage < VDD/2: 
				error_times += 1
	error_rate = error_times / sim_times


	#输出有关模拟的统计数据
	if sim_time == 1:
		#如果是第一次进行模拟， 创建txt文件， 并在第一行表明数据名称
		output_csv_file = open('shift_timing_error_calculation.csv', 'wb')
		csv_writer = csv.writer(output_csv_file)
		csv_writer.writerow(['start timing', 'end timing', 'current height', 'injection node', 'output node', 'error rate', 'min vol'])
		csv_writer.writerow([start_timing, end_timing, current_height, injection_node, output_node, error_rate, signal_min_voltage])
		

	else:
		#如果是第二次之后的模拟, 进行追加填写
		output_csv_file = open('shift_timing_error_calculation.csv', 'a+')
		csv_writer = csv.writer(output_csv_file)
		csv_writer.writerow([start_timing, end_timing, current_height, injection_node, output_node, error_rate, signal_min_voltage])
	
	output_csv_file.close()
	#'''


def shift_current_height(start_height, end_height, interval, injection_node, injection_timing, output_node, input_file, sim_time):
	read_file = open(input_file, 'r')
	temp_file = read_file.readlines()
	for line_number, line in enumerate(temp_file):
		#修改 .TRAN 所在行的命令
		if '.TRAN' in line:
			TRAN_option = line.split(' ')

			new_TRAN_option = ['.TRAN', '1p', 'simtime', 'sweep', 'currentheight']
			new_TRAN_option.append(start_height + 'e-6')
			new_TRAN_option.append(end_height + 'e-6')
			new_TRAN_option.append(interval + 'e-6')
			
			#把列表再次转换为 STRING 类型进行储存
			temp_file[line_number] = ' '.join(new_TRAN_option) + '\n'

		#修改 injection_node 的 currentdelay 参数
		elif ('.param ' + 'currentdelay' + injection_node.strip('i')) in line:
			currentdelay_option = line.split(' ')

			#替换其中 currentdelay** 后的数字部分
			new_currentdelay_option = currentdelay_option[:3]
			new_currentdelay_option.append(injection_timing)
			new_currentdelay_option.extend(['  ' + currentdelay_option[-1]])

			#把列表再次转换为 STRING 类型进行储存
			temp_file[line_number] = ' '.join(new_currentdelay_option)

		elif '.param mvdd' in line:
			VDD = float(line.split(' ')[-1].strip('\n'))

	#以写模式打开 input_file, 但先把文件内容进行清空, 之后把替换 TRAN OPTION 的文件再次写入
	output_file = open(input_file, 'w')
	for line in temp_file:
		output_file.write(line)
	output_file.close()

	#'''
	#进行 Hspice Simulation
	os.system('hspice64 -hpp -mt 4  -i ' + input_file + ' -o ../waveform/shift_current_height_result-'+ start_height + '-' + end_height +'.lis')
	read_file.close()

	#读取.lis文件统计错误率
	file = open('../waveform/shift_current_height_result-' + start_height + '-' + end_height +'.lis', 'r')
	lis_file = file.readlines()

	
	#sim_times : 进行模拟的总次数    error_times : 出现错误的总次数
	#出现错误的标准：利用Hspice自带的.MEASURE命令对于特定端子进行检测
	#端子的输出值为minval后面的数字， 若此值低于0.1V(此值的设定可以进行进一步考虑)， 则认为是出现了错误
	sim_times, error_times = 0, 0
	for line in lis_file:
		if (output_node + '_minvol') in line:
			sim_times += 1
			signal_min_voltage = line.split(' ')[2]
			
			if 'e' in signal_min_voltage:
				e_index = signal_min_voltage.index('e')
				e_number = float(signal_min_voltage[-1])
				min_voltage = float(signal_min_voltage[:e_index])/10**e_number
			else:
				min_voltage = float(signal_min_voltage)

			if min_voltage < VDD/2: 
				error_times += 1
	error_rate = error_times / sim_times

	
	#输出有关模拟的统计数据
	if sim_time == 1:
		#如果是第一次进行模拟， 创建CSV文件， 并在第一行标明数据名称
		output_csv_file = open('shift_current_height_error_calculation.csv', 'wb')
		csv_writer = csv.writer(output_csv_file)
		csv_writer.writerow(['start height', 'end height', 'interval', 'injection node', 'output node', 'injection timing', 'error rate', 'min vol'])
		csv_writer.writerow([start_height, end_height, interval, injection_node, output_node, injection_timing, error_rate, signal_min_voltage])

	else:
		#如果是第二次之后的模拟, 进行追加填写
		output_csv_file = open('shift_current_height_error_calculation.csv', 'a+')
		csv_writer = csv.writer(output_csv_file)
		csv_writer.writerow([start_height, end_height, interval, injection_node, output_node, injection_timing, error_rate, signal_min_voltage])

	output_csv_file.close()
	#'''

#处理 .lis 文件以判断波形中是否出现错误
def analyze_waveform(lis_file):
	with open(lis_file) as temp_file:
		file = temp_file.readlines()
		result_list = []

		#先找到'transient analysis'所在行的行数, 用来确定每次模拟的结果在文件中所在的位置
		#以 'transient analysis'所在行作为截取上限
		for line in file:
			if re.findall(r'transient analysis', line):
				line_index_list_1 = find_all_index(file, line)

		#以 '100.0%time'所在行作为截取下限
		line_index_list_2 = find_all_index_2(file, r'100.0% time =')

		#print('line_index_list_1', line_index_list_1)
		#print('line_index_list_2', line_index_list_2)

		#根据截取上限和下限, 截取中间部分的参数数据, 并清楚空白行
		temp_file = []
		for line_number in line_index_list_1:
			temp_file.append(file[line_number+2:line_number+14])

		for i in range(len(line_index_list_1)):
			single_result = file[line_index_list_1[i]+2:line_index_list_2[i]]

			#清楚中间空白行
			while ' \n' in single_result:
				single_result.remove(' \n')

		#每一次的模拟结果保存在 single_result_dict 中, 不同的参数对应后面不同的数值
		#最后将所有的 single_result_dict 填加到 result_list 列表之中
		for single_result in temp_file:
			single_result_dict = {}
			for item in single_result:
				data_name, data = extract_data(item)
				single_result_dict[data_name] = data
			result_list.append(single_result_dict)
		print('result_list')
		for part in result_list:
			print(part)
			print()				



#从命令行中获取 CSV 文件
#可以是储存了不同 current height 的, 也可以是储存了不同 injection timing 的 CSV 文件
#simulation_mode = 1 : fixed current height, shift injection timing
#simulation_mode = 2 : fixed injection timing, shift current height
opts, args = getopt.getopt(sys.argv[1:], "hi:c:m:")
input_file, simulation_mode, input_csv_file = '', '', ''

def usage():
	#比如 python Python-based Simulation.py -i 3NAND_2_NP_errorall.sp -m 1 -c timing.csv
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

'''
#记录模拟的次数， 用于标记输出文件
sim_time = 0
for data in input_data:
	sim_time += 1
	if simulation_mode == '1':
		shift_timing(data[0], data[1], data[2], data[3], data[4], input_file, sim_time)
	elif simulation_mode == '2':
		shift_current_height(data[0], data[1], data[2], data[3], data[4], data[5], input_file, sim_time)
	else:
		usage()
		sys.exit()

if simulation_mode == '1':
	print('Shift timing simulation done! ---> shift_timing_error_calculation.csv')
elif simulation_mode == '2':
	print('Shift current height simulation done! ---> shift_current_height_error_calculation.csv')
'''

analyze_waveform('../waveform/test.lis')