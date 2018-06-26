import re
class AutoWriteIntent(object):
	def __init__(self):
		self.ORG_STR_LIST = []
		self.FILE_PATH='./srcfile.txt'
		self.PARSE_DICT = {}
	
	def store_orgstr(self):
		intents = []
		fd = open(self.FILE_PATH,'r+')
		line = fd.readline()
		while(line[0] == '*'):
			print('line:',line)
			self.PARSE_DICT[line[1:].split('=')[0]] = '[D:'+line[1:].split('=')[1][:-1]+']'
			line = fd.readline()
		
		while(re.match(r'\s+',line)):
			line = fd.readline()
		
		while(line and line[0] == '#'):
			intents.append(line)	
			line = fd.readline()
		
		self.ORG_STR_LIST.append(self.PARSE_DICT)
		self.ORG_STR_LIST.extend(intents)
	
	def parse_slot(self,slts):
		w_line=''
		err_flag=0
		r = re.compile(r'【.+?】')
		slotdic = r.findall(slts[1:])
		for slot in slotdic:
			try:
				w_line +=(''.join(self.PARSE_DICT[slot]))
			except KeyError as e:
				print(e)
				print('词槽{}不存在，此词槽解析失败'.format(slot))
				err_flag = 1

		real_line =w_line+'\n'+' ' if err_flag == 0 else None
		return real_line
	
	def rewrite2file(self):
		fd = open('./tmpfile.txt','w+')
		line = fd.readline()
		for i,slot in enumerate(self.ORG_STR_LIST[1:]):
			r_slot = self.parse_slot(slot)	
			if r_slot != None:
				self.ORG_STR_LIST.insert(2*(i+1),r_slot)	
			else:
				print('词槽解析错误，导致此意图添加失败.')

		fd.writelines(self.ORG_STR_LIST[1:])
		fd.close()
	
	def getFile(self):
		self.store_orgstr()
		self.rewrite2file()


	

def main():
	aw=AutoWriteIntent()
	aw.getFile()

if __name__ == '__main__':
	main()
