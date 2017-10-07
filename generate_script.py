import re,os


with open("./jsvmdebug.py") as fi:
	with open("../jsvmdebug.py", "w") as fo:
		fo.write(fi.read())
os.chdir("..")
BYTECODES = [('JSOP_AND', '0x45', '5'), ('JSOP_GOTO', '0x06', '5'), ('JSOP_IFEQ', '0x07', '5'), ('JSOP_IFNE', '0x08', '5'), ('JSOP_LABEL', '0x6a', '5'), ('JSOP_LOOPENTRY', '0xe3', '2'), ('JSOP_LOOPHEAD', '0x6d', '1'), ('JSOP_OR', '0x44', '5'), ('JSOP_CASE', '0x79', '5'), ('JSOP_CONDSWITCH', '0x78', '1'), ('JSOP_DEFAULT', '0x7a', '5'), ('JSOP_ENDITER', '0x4e', '1'), ('JSOP_ISGENCLOSING', '0xbb', '1'), ('JSOP_ISNOITER', '0x4d', '1'), ('JSOP_ITER', '0x4b', '2'), ('JSOP_MOREITER', '0x4c', '1'), ('JSOP_ENTERWITH', '0x03', '5'), ('JSOP_LEAVEWITH', '0x04', '1'), ('JSOP_EXCEPTION', '0x76', '1'), ('JSOP_FINALLY', '0x87', '1'), ('JSOP_GOSUB', '0x74', '5'), ('JSOP_RETSUB', '0x75', '1'), ('JSOP_THROW', '0x70', '1'), ('JSOP_THROWING', '0x97', '1'), ('JSOP_THROWMSG', '0x4a', '3'), ('JSOP_TRY', '0x86', '1'), ('JSOP_CALL', '0x3a', '3'), ('JSOP_CALLITER', '0x91', '3'), ('JSOP_CALL_IGNORES_RV', '0xe7', '3'), ('JSOP_CHECKISCALLABLE', '0xdb', '2'), ('JSOP_EVAL', '0x7b', '3'), ('JSOP_FUNAPPLY', '0x4f', '3'), ('JSOP_FUNCALL', '0x6c', '3'), ('JSOP_FUNWITHPROTO', '0x34', '5'), ('JSOP_GETRVAL', '0x02', '1'), ('JSOP_LAMBDA', '0x82', '5'), ('JSOP_LAMBDA_ARROW', '0x83', '5'), ('JSOP_NEW', '0x52', '3'), ('JSOP_OPTIMIZE_SPREADCALL', '0xb2', '1'), ('JSOP_RETRVAL', '0x99', '1'), ('JSOP_RETURN', '0x05', '1'), ('JSOP_RUNONCE', '0x47', '1'), ('JSOP_SETFUNNAME', '0xb6', '2'), ('JSOP_SETRVAL', '0x98', '1'), ('JSOP_SPREADCALL', '0x29', '1'), ('JSOP_SPREADEVAL', '0x2b', '1'), ('JSOP_SPREADNEW', '0x2a', '1'), ('JSOP_SPREADSUPERCALL', '0xa6', '1'), ('JSOP_STRICTEVAL', '0x7c', '3'), ('JSOP_STRICTSPREADEVAL', '0x32', '1'), ('JSOP_SUPERCALL', '0xa5', '3'), ('JSOP_TOASYNC', '0x95', '1'), ('JSOP_AWAIT', '0xd1', '4'), ('JSOP_CHECKISOBJ', '0x0e', '2'), ('JSOP_FINALYIELDRVAL', '0xcc', '1'), ('JSOP_GENERATOR', '0xd4', '1'), ('JSOP_INITIALYIELD', '0xca', '4'), ('JSOP_RESUME', '0xcd', '3'), ('JSOP_YIELD', '0xcb', '4'), ('JSOP_DEBUGGER', '0x73', '1'), ('JSOP_DEBUGLEAVELEXICALENV', '0xc9', '1'), ('JSOP_BINDNAME', '0x6e', '5'), ('JSOP_DEFCONST', '0x80', '5'), ('JSOP_DEFFUN', '0x7f', '1'), ('JSOP_DEFLET', '0xa2', '5'), ('JSOP_DEFVAR', '0x81', '5'), ('JSOP_DELNAME', '0x24', '5'), ('JSOP_GETIMPORT', '0xb0', '5'), ('JSOP_GETNAME', '0x3b', '5'), ('JSOP_SETNAME', '0x6f', '5'), ('JSOP_STRICTSETNAME', '0x31', '5'), ('JSOP_BINDGNAME', '0xd6', '5'), ('JSOP_BINDVAR', '0xd5', '1'), ('JSOP_GETGNAME', '0x9a', '5'), ('JSOP_INITGLEXICAL', '0xa1', '5'), ('JSOP_SETGNAME', '0x9b', '5'), ('JSOP_STRICTSETGNAME', '0x9c', '5'), ('JSOP_CHECKLEXICAL', '0x8a', '4'), ('JSOP_GETLOCAL', '0x56', '4'), ('JSOP_INITLEXICAL', '0x8b', '4'), ('JSOP_SETLOCAL', '0x57', '4'), ('JSOP_THROWSETCALLEE', '0xb3', '1'), ('JSOP_THROWSETCONST', '0xa9', '4'), ('JSOP_CHECKALIASEDLEXICAL', '0x8c', '5'), ('JSOP_GETALIASEDVAR', '0x88', '5'), ('JSOP_INITALIASEDLEXICAL', '0x8d', '5'), ('JSOP_SETALIASEDVAR', '0x89', '5'), ('JSOP_THROWSETALIASEDCONST', '0xaa', '5'), ('JSOP_GETINTRINSIC', '0x8f', '5'), ('JSOP_SETINTRINSIC', '0x90', '5'), ('JSOP_FRESHENLEXICALENV', '0xc5', '1'), ('JSOP_POPLEXICALENV', '0xc8', '1'), ('JSOP_PUSHLEXICALENV', '0xc7', '5'), ('JSOP_RECREATELEXICALENV', '0xc6', '1'), ('JSOP_CHECKRETURN', '0xbe', '1'), ('JSOP_CHECKTHIS', '0xbd', '1'), ('JSOP_CHECKTHISREINIT', '0xbf', '1'), ('JSOP_FUNCTIONTHIS', '0xb9', '1'), ('JSOP_GIMPLICITTHIS', '0x9d', '5'), ('JSOP_GLOBALTHIS', '0xba', '1'), ('JSOP_IMPLICITTHIS', '0xe2', '5'), ('JSOP_SUPERBASE', '0x67', '1'), ('JSOP_SUPERFUN', '0xa4', '1'), ('JSOP_ARGUMENTS', '0x09', '1'), ('JSOP_CALLEE', '0x84', '1'), ('JSOP_GETARG', '0x54', '3'), ('JSOP_NEWTARGET', '0x94', '1'), ('JSOP_REST', '0xe0', '1'), ('JSOP_SETARG', '0x55', '3'), ('JSOP_POPVARENV', '0xb5', '1'), ('JSOP_PUSHVARENV', '0xb4', '5'), ('JSOP_ADD', '0x1b', '1'), ('JSOP_NEG', '0x22', '1'), ('JSOP_POS', '0x23', '1'), ('JSOP_POW', '0x96', '1'), ('JSOP_BITNOT', '0x21', '1'), ('JSOP_URSH', '0x1a', '1'), ('JSOP_NOT', '0x20', '1'), ('JSOP_DELELEM', '0x26', '1'), ('JSOP_DELPROP', '0x25', '5'), ('JSOP_IN', '0x71', '1'), ('JSOP_INSTANCEOF', '0x72', '1'), ('JSOP_STRICTDELPROP', '0x2e', '5'), ('JSOP_TYPEOF', '0x27', '1'), ('JSOP_TYPEOFEXPR', '0xc4', '1'), ('JSOP_VOID', '0x28', '1'), ('JSOP_DUP', '0x0c', '1'), ('JSOP_DUP2', '0x0d', '1'), ('JSOP_DUPAT', '0x2c', '4'), ('JSOP_PICK', '0x85', '2'), ('JSOP_POP', '0x51', '1'), ('JSOP_POPN', '0x0b', '3'), ('JSOP_SWAP', '0x0a', '1'), ('JSOP_UNPICK', '0xb7', '2'), ('JSOP_DEBUGAFTERYIELD', '0xd0', '1'), ('JSOP_DOUBLE', '0x3c', '5'), ('JSOP_FALSE', '0x42', '1'), ('JSOP_TRUE', '0x43', '1'), ('JSOP_INT32', '0xd8', '5'), ('JSOP_INT8', '0xd7', '2'), ('JSOP_IS_CONSTRUCTING', '0x41', '1'), ('JSOP_NULL', '0x40', '1'), ('JSOP_ONE', '0x3f', '1'), ('JSOP_STRING', '0x3d', '5'), ('JSOP_SYMBOL', '0x2d', '2'), ('JSOP_UINT16', '0x58', '3'), ('JSOP_UINT24', '0xbc', '4'), ('JSOP_UNDEFINED', '0x01', '1'), ('JSOP_UNINITIALIZED', '0x8e', '1'), ('JSOP_ZERO', '0x3e', '1'), ('JSOP_CALLELEM', '0xc1', '1'), ('JSOP_CALLPROP', '0xb8', '5'), ('JSOP_CALLSITEOBJ', '0x65', '5'), ('JSOP_CHECKOBJCOERCIBLE', '0xa3', '1'), ('JSOP_CLASSHERITAGE', '0x33', '1'), ('JSOP_GETBOUNDNAME', '0xc3', '5'), ('JSOP_GETELEM', '0x37', '1'), ('JSOP_GETELEM_SUPER', '0x7d', '1'), ('JSOP_GETPROP', '0x35', '5'), ('JSOP_GETPROP_SUPER', '0x68', '5'), ('JSOP_INITELEM', '0x5e', '1'), ('JSOP_INITELEM_GETTER', '0x63', '1'), ('JSOP_INITELEM_SETTER', '0x64', '1'), ('JSOP_INITHIDDENELEM', '0xaf', '1'), ('JSOP_INITHIDDENELEM_GETTER', '0xad', '1'), ('JSOP_INITHIDDENELEM_SETTER', '0xae', '1'), ('JSOP_INITHIDDENPROP', '0x93', '5'), ('JSOP_INITHIDDENPROP_GETTER', '0xab', '5'), ('JSOP_INITHIDDENPROP_SETTER', '0xac', '5'), ('JSOP_INITHOMEOBJECT', '0x5c', '2'), ('JSOP_INITLOCKEDPROP', '0x92', '5'), ('JSOP_INITPROP', '0x5d', '5'), ('JSOP_INITPROP_GETTER', '0x61', '5'), ('JSOP_INITPROP_SETTER', '0x62', '5'), ('JSOP_MUTATEPROTO', '0xc2', '1'), ('JSOP_NEWINIT', '0x59', '5'), ('JSOP_NEWOBJECT', '0x5b', '5'), ('JSOP_OBJECT', '0x50', '5'), ('JSOP_OBJWITHPROTO', '0x53', '1'), ('JSOP_SETELEM', '0x38', '1'), ('JSOP_SETELEM_SUPER', '0x9e', '1'), ('JSOP_SETPROP', '0x36', '5'), ('JSOP_SETPROP_SUPER', '0x6b', '5'), ('JSOP_STRICTDELELEM', '0x2f', '1'), ('JSOP_STRICTSETELEM', '0x39', '1'), ('JSOP_STRICTSETELEM_SUPER', '0x9f', '1'), ('JSOP_STRICTSETPROP', '0x30', '5'), ('JSOP_STRICTSETPROP_SUPER', '0x69', '5'), ('JSOP_TOID', '0xe1', '1'), ('JSOP_ARRAYPUSH', '0xce', '1'), ('JSOP_HOLE', '0xda', '1'), ('JSOP_INITELEM_ARRAY', '0x60', '5'), ('JSOP_INITELEM_INC', '0x5f', '1'), ('JSOP_LENGTH', '0xd9', '5'), ('JSOP_NEWARRAY', '0x5a', '5'), ('JSOP_NEWARRAY_COPYONWRITE', '0x66', '5'), ('JSOP_SPREADCALLARRAY', '0x7e', '5'), ('JSOP_REGEXP', '0xa0', '5'), ('JSOP_CLASSCONSTRUCTOR', '0xa7', '5'), ('JSOP_DERIVEDCONSTRUCTOR', '0xa8', '5'), ('JSOP_DEBUGCHECKSELFHOSTED', '0xb1', '1'), ('JSOP_FORCEINTERPRETER', '0xcf', '1'), ('JSOP_JUMPTARGET', '0xe6', '1'), ('JSOP_LINENO', '0x77', '5'), ('JSOP_NOP', '0x00', '1'), ('JSOP_NOP_DESTRUCTURING', '0xe5', '1'), ('JSOP_TOSTRING', '0xe4', '1')]
fscript = open("jsvm.x", "w")
fscript.write("source jsvmdebug.py\n")
fscript.write("source js/jsvmdebug.py\n")
dirname = os.path.dirname(os.path.realpath(__file__))
pattern = re.compile(r'^CASE\([A-Z0-9_]+\)')
lineno = 1
fscript.write("define addvmbp\n")
with open("src/vm/Interpreter.cpp") as f:
	while True:
		line = f.readline()
		if len(line) == 0:
			break
		res = pattern.findall(line)
		if len(res) != 0:
			fscript.write("\tb " + dirname + "/src/vm/Interpreter.cpp:" + str(lineno) + '\n')
		lineno += 1
fscript.write("end\n")

dis = '''
define dis
	echo start disassembly\\n
	set $ptr = (uint8_t*)$arg0
	set $codelength = 0
	set $count = $arg1
	set $i = 0
	while $i != $count
		set $bytecode = *($ptr)
		set $bytecodearg = *((uint32_t*)($ptr+1))
		pbytecode
		set $ptr = $ptr + $codelength
		set $i = $i + 1
	end
end
'''
bytecodehead = '''
python
def shiftendian(aNum):
    result = 0
    while aNum:
            result = (result << 8) | (aNum&0xff)
            aNum = aNum >> 8
    return result
class Pbytecode(gdb.Command):
	def __init__(self):
		super(self.__class__, self).__init__("pbytecode", gdb.COMMAND_USER)
	def invoke(self, args, from_tty):
		argv = gdb.string_to_argv(args)
		bytecode = gdb.parse_and_eval("$bytecode")
		bytecode = int(bytecode)
		bytecodearg= gdb.parse_and_eval("$bytecodearg")
		bytecodearg = int(bytecodearg)
		if 0 == 1:
			pass
'''
bytecodetail = '''
		else:
			print("bytecode: %02x"%bytecode)
			print("wrong bytecode")
			exit(0)
Pbytecode()
end
'''

disvm = '''
define disvm
	dis activation.regs_.pc 12
end'''

fscript.write(bytecodehead)
for elem in BYTECODES:
	SF = '''
		elif bytecode == %s:
			codetmp = shiftendian(%s & %s)
			print("%%-25s %%-8x %%02x"%%("%s", codetmp, %s))
			gdb.execute('set $codelength = %s')'''
	if elem[2] == '1':
		mask = 0
	elif elem[2] == '2':
		mask = 0xff
	elif elem[2] == '3':
		mask = 0xffff
	elif elem[2] == '4':
		mask = 0xffffff
	elif elem[2] == '5':
		mask = 0xffffffff
	else:
		print 'error'
		exit(0)
	fscript.write(SF%(elem[1], "bytecodearg", mask, elem[0], elem[1], elem[2]))
fscript.write(bytecodetail)
fscript.write(dis)
fscript.write(disvm)

getname = '''
define getname
	p *(script->getAtom($arg0).value)
end'''

fscript.write(getname)

print 'Generating jsvm.x done!'
