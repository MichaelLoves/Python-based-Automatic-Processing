#encoding:utf-8
import os, sys, getopt, operator, csv, re
from copy import deepcopy



def run_simulation(start_height, end_height, interval, input_file, sim_time):
	read_file = open(input_file, 'r')
	temp_file = read_file.readlines()
	for line in temp_file:
		if '.TRAN' in line:
			TRAN_option = line.split(' ')
			line_number = temp_file.index(line)

			new_option = ['.TRAN', '1p', 'simtime', 'sweep', 'currentheight']
			new_option.append(start_height)
			new_option.append(end_height)
			new_option.append(interval)
			
			#把列表再次转换为 STRING 类型进行储存
			temp_file[line_number] = ' '.join(new_option) + '\n'

	#以写模式打开 input_file, 但先把文件内容进行清空
	output_file = open(input_file, 'w')
	for line in temp_file:
		output_file.write(line)
	output_file.close()

	os.system('hspice64 -hpp -mt 4  -i ' + input_file + ' -o ./waveform/result' + str(sim_time) +'.lis')
	read_file.close()

	#读取.lis文件统计错误率
	file = open('./waveform/result' + str(sim_time) + '.lis', 'r')
	
	#sim_times 进行模拟的总次数  error_times 出现错误的总次数
	#出现错误的标准：利用Hspice自带的.MEASURE命令对于特定端子进行检测
	#端子的输出值为maxval后面的数字， 若此值低于0.1V， 则认为是出现了错误
	sim_times, error_times = 0, 0
	for line in file.readlines():
		if 'maxval' in line:
			sim_times += 1
			signal_voltage = line[9:15]
			if signal_voltage < 0.1:
				error_times += 1
	error_rate = error_times / sim_times
	

	#输出模拟数据
	if sim_time == 1:
		#如果是第一次进行模拟， 创建txt文件， 并在第一行表明数据名称
		output = open('./waveform/error_calculation.txt', 'w+')
		output.write('start_height  end_height  interval  error_rate  max_vol\n')
	else:
		output = open('./waveform/error_calculation.txt', 'a+')
	output.write(start_height + '               ')
	output.write(end_height + '            ')
	output.write(interval + '          ')
	output.write(str(error_rate) + '              ')
	output.write(str(signal_voltage))
	output.write('\n')
	output.close()




#从命令行中获取 CSV 文件
opts, args = getopt.getopt(sys.argv[1:], "hi:c:")
input_file, input_csv_file = '', ''

def usage():
	print('Usage: ' + sys.argv[0] + ' -i input_file -c input_csv_file')

for op, value in opts:
	if op == '-i':
		input_file = value
	if op == '-c':
		input_csv_file = value
	elif op == '-h':
		usage()
		sys.exit()


temp_file = csv.reader(open(input_csv_file, 'rU'))

input_data = []
for line in temp_file:
	if re.findall(r"\bstart\w*\b", ' '.join(line)):
		pass
	else:
		single_data = line[0].split(';')
		input_data.append(single_data)

#记录模拟的次数， 用于标记输出文件
sim_time = 0
for data in input_data:
	sim_time += 1
	run_simulation(data[0], data[1], data[2], input_file, sim_time)


