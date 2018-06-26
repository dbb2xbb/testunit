import re
ORG_STR_LIST = []
FILE_PATH='./srcfile.txt'
PARSE_DICT = {}
def write2file(fd,firstline,parse_dict):
	print("tell:",fd.tell())
	print(real_line)
	fd.write(real_line)
#	fd.write('\n')
	fd.close()

def store_orgstr():
	global PARSE_DICT
	global ORG_STR_LIST

	intents = []
	fd = open(FILE_PATH,'r+')
	line = fd.readline()
	while(line[0] == '*'):
		print('line:',line)
		PARSE_DICT[line[1:].split('=')[0]] = '[D:'+line[1:].split('=')[1][:-1]+']'
		line = fd.readline()
	#print(PARSE_DICT)	
	while(line and line[0] == '#'):
		intents.append(line)	
		line = fd.readline()
	print('INTENTS:',intents)	
	
	ORG_STR_LIST.append(PARSE_DICT)
	ORG_STR_LIST.extend(intents)

def parse_slot(slts):
	w_line=''
	r = re.compile(r'【.+?】')
	slotdic = r.findall(slts[1:])
	for slot in slotdic:
		w_line +=(''.join(PARSE_DICT[slot]))
	real_line =w_line+'\n'+' '
	return real_line

def rewrite2file():
	fd = open('./tmpfile.txt','w+')
	line = fd.readline()
	for i,slot in enumerate(ORG_STR_LIST[1:]):
		r_slot = parse_slot(slot)	
		ORG_STR_LIST.insert(2*(i+1),r_slot)	
	
	#print('FINALE_WAITINGFORWRITE:',ORG_STR_LIST)
	fd.writelines(ORG_STR_LIST[1:])
	fd.close()

def getFile(path):
	parse_dict = {}
	store_orgstr()
	rewrite2file()

#	write2file(fd,line,parse_dict)
	

def main():
	getFile(FILE_PATH)

if __name__ == '__main__':
	main()
