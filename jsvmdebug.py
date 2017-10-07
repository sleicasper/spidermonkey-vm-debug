import gdb,re

class Pasciistr(gdb.Command):
	def __init__(self):
		super(self.__class__, self).__init__("pasciistr", gdb.COMMAND_USER)
		self.char_PN = re.compile(r'\'([\w\\]+)\'')
		self.decimal_PN = re.compile(r'^[0-9]+$')
	def invoke(self, args, from_tty):
		argv = gdb.string_to_argv(args)
		ptr = str( gdb.parse_and_eval(argv[0]) )

		if len( self.decimal_PN.findall(ptr) ) == 1:
			ptr = int(ptr)
		else:
			ptr = int(ptr, 16)
		if len( self.decimal_PN.findall(argv[1]) ) == 1:
			length = int(argv[1])
		else:
			length = int(argv[1], 16)
		if length <= 0:
			length = 100
		if length > 100:
			length = 100
		result = ''
		for i in range(length):
			resstr = gdb.execute("x/1c" + str(ptr), to_string = True)
			if len(self.char_PN.findall(resstr)) == 1:
				ch = self.char_PN.findall(resstr)[0]
				result += ch
			else:
				print("re find error")
				return
			ptr += 1
		print(result)


class Getjsname(gdb.Command):
	def __init__(self):
		super(self.__class__, self).__init__("getjsname", gdb.COMMAND_USER)
	def invoke(self, args, from_tty):
		argv = gdb.string_to_argv(args)
		if len(argv) != 1:
			print("argv error")
			return

		maxidx = int( str(gdb.parse_and_eval("(script.ptr).natoms_")) )
		idx = abs(int(argv[0]))
		if idx >= maxidx:
			print("idx too big")
			return
		length = gdb.execute("p (*(script->getAtom(%d).value)).d.u1.length"%idx, to_string=True)
		length = str(length)
		if len(re.compile(r'^\$[0-9]+ = ([0-9]+)$').findall(length)) == 1:
			length = re.compile(r'^\$[0-9]+ = ([0-9]+)$').findall(length)[0]
			gdb.execute("pasciistr &(*(script->getAtom(%d).value)).d.inlineStorageLatin1 %s"%(idx, length))
		else:
			print("re find error")
			return

Pasciistr()
Getjsname()
