#!/tps/bin/python
from optparse import OptionParser

parser=OptionParser()
parser.add_option('-d','--date',dest='log date',help="Enter the log date, ex: 20130718.log")
parser.add_option('-f','--file',dest='file name',help="Enter the file name you want to match the log, ex: test.csv")
parser.add_option('-o','--output',dest='output file',help="Define an output file.")
args_dict=parser.parse_args()[0].__dict__

def test_entry(dict):
	if None in dict.values():
		raise TypeError("Your entry is not correct, or you might missed something, please use -h for help and try again.")
	if 'log' not in dict['log date']:
		raise TypeError("Don't forget the suffix.")
	if '.' not in dict['file name']:
		raise TypeError("Don't forget the suffix.")

def compare(dict):
	log_obj=open('/var/opt/BESClient/__BESData/__Global/Logs/'+dict['log date'])
	log_file=log_obj.readlines()
	log_obj.close()

	test_obj=open(dict['file name'])
	test_file=test_obj.readlines()
	test_obj.close()

	output=open(dict['output file'],'w')
	print>>output,test_file[0].strip('\n')+',Black Hole'
	for csvline in test_file[1:]:
		csvtime=csvline.split(',')[0].split()[-1].split(':')
		csvtimehm=csvtime[:2]
		csvtimes=int(csvtime[2])
		newline = csvline
		count=''
		for logline in log_file:
			if 'At ' in logline:
				logtime=logline.split()[1].split(':')
				logtimehm=logtime[:2]
				logtimes=int(logtime[2])
				if csvtimehm==logtimehm and logtimes in (csvtimes+1,csvtimes,csvtimes+2):
					count = 0.5
					#newline=newline.strip('\n')+',0.5'
		if newline.strip('\n').split(',')[-1]=='':
			newline=newline.strip('\n').strip(',')+", ,"+str(count)
		else:
			newline=newline.strip('\n').strip(',')+','+str(count)
		out = newline.strip('\n').strip(',')
		#print out
		print>>output,out
	output.close()

if __name__=="__main__":
	test_entry(args_dict)
	compare(args_dict)
