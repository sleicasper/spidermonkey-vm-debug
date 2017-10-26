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

def shiftendian(aNum):
    result = 0
    while aNum:
            result = (result << 8) | (aNum&0xff)
            aNum = aNum >> 8
    return result
class Pbytecode(gdb.Command):
	def __init__(self):
		super(self.__class__, self).__init__("pbytecode", gdb.COMMAND_USER)
		self.hex_PN = re.compile(r'(0x[0-9a-fA-F]+)')
		self._BYTECODES = {
			0x45:{'name':'JSOP_AND', 'codelen':'5', 'isstring':'0'},
			0x06:{'name':'JSOP_GOTO', 'codelen':'5', 'isstring':'0'},
			0x07:{'name':'JSOP_IFEQ', 'codelen':'5', 'isstring':'0'},
			0x08:{'name':'JSOP_IFNE', 'codelen':'5', 'isstring':'0'},
			0x6a:{'name':'JSOP_LABEL', 'codelen':'5', 'isstring':'0'},
			0xe3:{'name':'JSOP_LOOPENTRY', 'codelen':'2', 'isstring':'0'},
			0x6d:{'name':'JSOP_LOOPHEAD', 'codelen':'1', 'isstring':'0'},
			0x44:{'name':'JSOP_OR', 'codelen':'5', 'isstring':'1'},
			0x79:{'name':'JSOP_CASE', 'codelen':'5', 'isstring':'1'},
			0x78:{'name':'JSOP_CONDSWITCH', 'codelen':'1', 'isstring':'1'},
			0x7a:{'name':'JSOP_DEFAULT', 'codelen':'5', 'isstring':'1'},
			0x4e:{'name':'JSOP_ENDITER', 'codelen':'1', 'isstring':'1'},
			0xbb:{'name':'JSOP_ISGENCLOSING', 'codelen':'1', 'isstring':'1'},
			0x4d:{'name':'JSOP_ISNOITER', 'codelen':'1', 'isstring':'1'},
			0x4b:{'name':'JSOP_ITER', 'codelen':'2', 'isstring':'1'},
			0x4c:{'name':'JSOP_MOREITER', 'codelen':'1', 'isstring':'1'},
			0x03:{'name':'JSOP_ENTERWITH', 'codelen':'5', 'isstring':'1'},
			0x04:{'name':'JSOP_LEAVEWITH', 'codelen':'1', 'isstring':'1'},
			0x76:{'name':'JSOP_EXCEPTION', 'codelen':'1', 'isstring':'1'},
			0x87:{'name':'JSOP_FINALLY', 'codelen':'1', 'isstring':'1'},
			0x74:{'name':'JSOP_GOSUB', 'codelen':'5', 'isstring':'1'},
			0x75:{'name':'JSOP_RETSUB', 'codelen':'1', 'isstring':'1'},
			0x70:{'name':'JSOP_THROW', 'codelen':'1', 'isstring':'1'},
			0x97:{'name':'JSOP_THROWING', 'codelen':'1', 'isstring':'1'},
			0x4a:{'name':'JSOP_THROWMSG', 'codelen':'3', 'isstring':'1'},
			0x86:{'name':'JSOP_TRY', 'codelen':'1', 'isstring':'1'},
			0x3a:{'name':'JSOP_CALL', 'codelen':'3', 'isstring':'0'},
			0x91:{'name':'JSOP_CALLITER', 'codelen':'3', 'isstring':'0'},
			0xe7:{'name':'JSOP_CALL_IGNORES_RV', 'codelen':'3', 'isstring':'0'},
			0xdb:{'name':'JSOP_CHECKISCALLABLE', 'codelen':'2', 'isstring':'1'},
			0x7b:{'name':'JSOP_EVAL', 'codelen':'3', 'isstring':'0'},
			0x4f:{'name':'JSOP_FUNAPPLY', 'codelen':'3', 'isstring':'1'},
			0x6c:{'name':'JSOP_FUNCALL', 'codelen':'3', 'isstring':'1'},
			0x34:{'name':'JSOP_FUNWITHPROTO', 'codelen':'5', 'isstring':'1'},
			0x02:{'name':'JSOP_GETRVAL', 'codelen':'1', 'isstring':'1'},
			0x82:{'name':'JSOP_LAMBDA', 'codelen':'5', 'isstring':'1'},
			0x83:{'name':'JSOP_LAMBDA_ARROW', 'codelen':'5', 'isstring':'1'},
			0x52:{'name':'JSOP_NEW', 'codelen':'3', 'isstring':'1'},
			0xb2:{'name':'JSOP_OPTIMIZE_SPREADCALL', 'codelen':'1', 'isstring':'1'},
			0x99:{'name':'JSOP_RETRVAL', 'codelen':'1', 'isstring':'1'},
			0x05:{'name':'JSOP_RETURN', 'codelen':'1', 'isstring':'1'},
			0x47:{'name':'JSOP_RUNONCE', 'codelen':'1', 'isstring':'1'},
			0xb6:{'name':'JSOP_SETFUNNAME', 'codelen':'2', 'isstring':'1'},
			0x98:{'name':'JSOP_SETRVAL', 'codelen':'1', 'isstring':'1'},
			0x29:{'name':'JSOP_SPREADCALL', 'codelen':'1', 'isstring':'1'},
			0x2b:{'name':'JSOP_SPREADEVAL', 'codelen':'1', 'isstring':'1'},
			0x2a:{'name':'JSOP_SPREADNEW', 'codelen':'1', 'isstring':'1'},
			0xa6:{'name':'JSOP_SPREADSUPERCALL', 'codelen':'1', 'isstring':'1'},
			0x7c:{'name':'JSOP_STRICTEVAL', 'codelen':'3', 'isstring':'1'},
			0x32:{'name':'JSOP_STRICTSPREADEVAL', 'codelen':'1', 'isstring':'1'},
			0xa5:{'name':'JSOP_SUPERCALL', 'codelen':'3', 'isstring':'1'},
			0x95:{'name':'JSOP_TOASYNC', 'codelen':'1', 'isstring':'1'},
			0xd1:{'name':'JSOP_AWAIT', 'codelen':'4', 'isstring':'1'},
			0x0e:{'name':'JSOP_CHECKISOBJ', 'codelen':'2', 'isstring':'1'},
			0xcc:{'name':'JSOP_FINALYIELDRVAL', 'codelen':'1', 'isstring':'1'},
			0xd4:{'name':'JSOP_GENERATOR', 'codelen':'1', 'isstring':'1'},
			0xca:{'name':'JSOP_INITIALYIELD', 'codelen':'4', 'isstring':'1'},
			0xcd:{'name':'JSOP_RESUME', 'codelen':'3', 'isstring':'1'},
			0xcb:{'name':'JSOP_YIELD', 'codelen':'4', 'isstring':'1'},
			0x73:{'name':'JSOP_DEBUGGER', 'codelen':'1', 'isstring':'1'},
			0xc9:{'name':'JSOP_DEBUGLEAVELEXICALENV', 'codelen':'1', 'isstring':'1'},
			0x6e:{'name':'JSOP_BINDNAME', 'codelen':'5', 'isstring':'1'},
			0x80:{'name':'JSOP_DEFCONST', 'codelen':'5', 'isstring':'1'},
			0x7f:{'name':'JSOP_DEFFUN', 'codelen':'1', 'isstring':'1'},
			0xa2:{'name':'JSOP_DEFLET', 'codelen':'5', 'isstring':'1'},
			0x81:{'name':'JSOP_DEFVAR', 'codelen':'5', 'isstring':'1'},
			0x24:{'name':'JSOP_DELNAME', 'codelen':'5', 'isstring':'1'},
			0xb0:{'name':'JSOP_GETIMPORT', 'codelen':'5', 'isstring':'1'},
			0x3b:{'name':'JSOP_GETNAME', 'codelen':'5', 'isstring':'1'},
			0x6f:{'name':'JSOP_SETNAME', 'codelen':'5', 'isstring':'1'},
			0x31:{'name':'JSOP_STRICTSETNAME', 'codelen':'5', 'isstring':'1'},
			0xd6:{'name':'JSOP_BINDGNAME', 'codelen':'5', 'isstring':'1'},
			0xd5:{'name':'JSOP_BINDVAR', 'codelen':'1', 'isstring':'1'},
			0x9a:{'name':'JSOP_GETGNAME', 'codelen':'5', 'isstring':'1'},
			0xa1:{'name':'JSOP_INITGLEXICAL', 'codelen':'5', 'isstring':'1'},
			0x9b:{'name':'JSOP_SETGNAME', 'codelen':'5', 'isstring':'1'},
			0x9c:{'name':'JSOP_STRICTSETGNAME', 'codelen':'5', 'isstring':'1'},
			0x8a:{'name':'JSOP_CHECKLEXICAL', 'codelen':'4', 'isstring':'1'},
			0x56:{'name':'JSOP_GETLOCAL', 'codelen':'4', 'isstring':'1'},
			0x8b:{'name':'JSOP_INITLEXICAL', 'codelen':'4', 'isstring':'1'},
			0x57:{'name':'JSOP_SETLOCAL', 'codelen':'4', 'isstring':'1'},
			0xb3:{'name':'JSOP_THROWSETCALLEE', 'codelen':'1', 'isstring':'1'},
			0xa9:{'name':'JSOP_THROWSETCONST', 'codelen':'4', 'isstring':'1'},
			0x8c:{'name':'JSOP_CHECKALIASEDLEXICAL', 'codelen':'5', 'isstring':'1'},
			0x88:{'name':'JSOP_GETALIASEDVAR', 'codelen':'5', 'isstring':'1'},
			0x8d:{'name':'JSOP_INITALIASEDLEXICAL', 'codelen':'5', 'isstring':'1'},
			0x89:{'name':'JSOP_SETALIASEDVAR', 'codelen':'5', 'isstring':'1'},
			0xaa:{'name':'JSOP_THROWSETALIASEDCONST', 'codelen':'5', 'isstring':'1'},
			0x8f:{'name':'JSOP_GETINTRINSIC', 'codelen':'5', 'isstring':'1'},
			0x90:{'name':'JSOP_SETINTRINSIC', 'codelen':'5', 'isstring':'0'},
			0xc5:{'name':'JSOP_FRESHENLEXICALENV', 'codelen':'1', 'isstring':'1'},
			0xc8:{'name':'JSOP_POPLEXICALENV', 'codelen':'1', 'isstring':'1'},
			0xc7:{'name':'JSOP_PUSHLEXICALENV', 'codelen':'5', 'isstring':'1'},
			0xc6:{'name':'JSOP_RECREATELEXICALENV', 'codelen':'1', 'isstring':'1'},
			0xbe:{'name':'JSOP_CHECKRETURN', 'codelen':'1', 'isstring':'1'},
			0xbd:{'name':'JSOP_CHECKTHIS', 'codelen':'1', 'isstring':'1'},
			0xbf:{'name':'JSOP_CHECKTHISREINIT', 'codelen':'1', 'isstring':'1'},
			0xb9:{'name':'JSOP_FUNCTIONTHIS', 'codelen':'1', 'isstring':'1'},
			0x9d:{'name':'JSOP_GIMPLICITTHIS', 'codelen':'5', 'isstring':'1'},
			0xba:{'name':'JSOP_GLOBALTHIS', 'codelen':'1', 'isstring':'1'},
			0xe2:{'name':'JSOP_IMPLICITTHIS', 'codelen':'5', 'isstring':'1'},
			0x67:{'name':'JSOP_SUPERBASE', 'codelen':'1', 'isstring':'1'},
			0xa4:{'name':'JSOP_SUPERFUN', 'codelen':'1', 'isstring':'1'},
			0x09:{'name':'JSOP_ARGUMENTS', 'codelen':'1', 'isstring':'1'},
			0x84:{'name':'JSOP_CALLEE', 'codelen':'1', 'isstring':'1'},
			0x54:{'name':'JSOP_GETARG', 'codelen':'3', 'isstring':'1'},
			0x94:{'name':'JSOP_NEWTARGET', 'codelen':'1', 'isstring':'1'},
			0xe0:{'name':'JSOP_REST', 'codelen':'1', 'isstring':'1'},
			0x55:{'name':'JSOP_SETARG', 'codelen':'3', 'isstring':'1'},
			0xb5:{'name':'JSOP_POPVARENV', 'codelen':'1', 'isstring':'1'},
			0xb4:{'name':'JSOP_PUSHVARENV', 'codelen':'5', 'isstring':'1'},
			0x1b:{'name':'JSOP_ADD', 'codelen':'1', 'isstring':'1'},
			0x22:{'name':'JSOP_NEG', 'codelen':'1', 'isstring':'1'},
			0x23:{'name':'JSOP_POS', 'codelen':'1', 'isstring':'1'},
			0x96:{'name':'JSOP_POW', 'codelen':'1', 'isstring':'1'},
			0x21:{'name':'JSOP_BITNOT', 'codelen':'1', 'isstring':'1'},
			0x1a:{'name':'JSOP_URSH', 'codelen':'1', 'isstring':'1'},
			0x20:{'name':'JSOP_NOT', 'codelen':'1', 'isstring':'1'},
			0x26:{'name':'JSOP_DELELEM', 'codelen':'1', 'isstring':'1'},
			0x25:{'name':'JSOP_DELPROP', 'codelen':'5', 'isstring':'1'},
			0x71:{'name':'JSOP_IN', 'codelen':'1', 'isstring':'1'},
			0x72:{'name':'JSOP_INSTANCEOF', 'codelen':'1', 'isstring':'1'},
			0x2e:{'name':'JSOP_STRICTDELPROP', 'codelen':'5', 'isstring':'1'},
			0x27:{'name':'JSOP_TYPEOF', 'codelen':'1', 'isstring':'1'},
			0xc4:{'name':'JSOP_TYPEOFEXPR', 'codelen':'1', 'isstring':'1'},
			0x28:{'name':'JSOP_VOID', 'codelen':'1', 'isstring':'1'},
			0x0c:{'name':'JSOP_DUP', 'codelen':'1', 'isstring':'1'},
			0x0d:{'name':'JSOP_DUP2', 'codelen':'1', 'isstring':'1'},
			0x2c:{'name':'JSOP_DUPAT', 'codelen':'4', 'isstring':'1'},
			0x85:{'name':'JSOP_PICK', 'codelen':'2', 'isstring':'1'},
			0x51:{'name':'JSOP_POP', 'codelen':'1', 'isstring':'1'},
			0x0b:{'name':'JSOP_POPN', 'codelen':'3', 'isstring':'1'},
			0x0a:{'name':'JSOP_SWAP', 'codelen':'1', 'isstring':'1'},
			0xb7:{'name':'JSOP_UNPICK', 'codelen':'2', 'isstring':'1'},
			0xd0:{'name':'JSOP_DEBUGAFTERYIELD', 'codelen':'1', 'isstring':'1'},
			0x3c:{'name':'JSOP_DOUBLE', 'codelen':'5', 'isstring':'1'},
			0x42:{'name':'JSOP_FALSE', 'codelen':'1', 'isstring':'1'},
			0x43:{'name':'JSOP_TRUE', 'codelen':'1', 'isstring':'1'},
			0xd8:{'name':'JSOP_INT32', 'codelen':'5', 'isstring':'1'},
			0xd7:{'name':'JSOP_INT8', 'codelen':'2', 'isstring':'1'},
			0x41:{'name':'JSOP_IS_CONSTRUCTING', 'codelen':'1', 'isstring':'1'},
			0x40:{'name':'JSOP_NULL', 'codelen':'1', 'isstring':'1'},
			0x3f:{'name':'JSOP_ONE', 'codelen':'1', 'isstring':'1'},
			0x3d:{'name':'JSOP_STRING', 'codelen':'5', 'isstring':'1'},
			0x2d:{'name':'JSOP_SYMBOL', 'codelen':'2', 'isstring':'1'},
			0x58:{'name':'JSOP_UINT16', 'codelen':'3', 'isstring':'1'},
			0xbc:{'name':'JSOP_UINT24', 'codelen':'4', 'isstring':'1'},
			0x01:{'name':'JSOP_UNDEFINED', 'codelen':'1', 'isstring':'1'},
			0x8e:{'name':'JSOP_UNINITIALIZED', 'codelen':'1', 'isstring':'1'},
			0x3e:{'name':'JSOP_ZERO', 'codelen':'1', 'isstring':'1'},
			0xc1:{'name':'JSOP_CALLELEM', 'codelen':'1', 'isstring':'1'},
			0xb8:{'name':'JSOP_CALLPROP', 'codelen':'5', 'isstring':'1'},
			0x65:{'name':'JSOP_CALLSITEOBJ', 'codelen':'5', 'isstring':'1'},
			0xa3:{'name':'JSOP_CHECKOBJCOERCIBLE', 'codelen':'1', 'isstring':'1'},
			0x33:{'name':'JSOP_CLASSHERITAGE', 'codelen':'1', 'isstring':'1'},
			0xc3:{'name':'JSOP_GETBOUNDNAME', 'codelen':'5', 'isstring':'1'},
			0x37:{'name':'JSOP_GETELEM', 'codelen':'1', 'isstring':'1'},
			0x7d:{'name':'JSOP_GETELEM_SUPER', 'codelen':'1', 'isstring':'1'},
			0x35:{'name':'JSOP_GETPROP', 'codelen':'5', 'isstring':'1'},
			0x68:{'name':'JSOP_GETPROP_SUPER', 'codelen':'5', 'isstring':'1'},
			0x5e:{'name':'JSOP_INITELEM', 'codelen':'1', 'isstring':'1'},
			0x63:{'name':'JSOP_INITELEM_GETTER', 'codelen':'1', 'isstring':'1'},
			0x64:{'name':'JSOP_INITELEM_SETTER', 'codelen':'1', 'isstring':'1'},
			0xaf:{'name':'JSOP_INITHIDDENELEM', 'codelen':'1', 'isstring':'1'},
			0xad:{'name':'JSOP_INITHIDDENELEM_GETTER', 'codelen':'1', 'isstring':'1'},
			0xae:{'name':'JSOP_INITHIDDENELEM_SETTER', 'codelen':'1', 'isstring':'1'},
			0x93:{'name':'JSOP_INITHIDDENPROP', 'codelen':'5', 'isstring':'1'},
			0xab:{'name':'JSOP_INITHIDDENPROP_GETTER', 'codelen':'5', 'isstring':'1'},
			0xac:{'name':'JSOP_INITHIDDENPROP_SETTER', 'codelen':'5', 'isstring':'1'},
			0x5c:{'name':'JSOP_INITHOMEOBJECT', 'codelen':'2', 'isstring':'1'},
			0x92:{'name':'JSOP_INITLOCKEDPROP', 'codelen':'5', 'isstring':'1'},
			0x5d:{'name':'JSOP_INITPROP', 'codelen':'5', 'isstring':'1'},
			0x61:{'name':'JSOP_INITPROP_GETTER', 'codelen':'5', 'isstring':'1'},
			0x62:{'name':'JSOP_INITPROP_SETTER', 'codelen':'5', 'isstring':'1'},
			0xc2:{'name':'JSOP_MUTATEPROTO', 'codelen':'1', 'isstring':'1'},
			0x59:{'name':'JSOP_NEWINIT', 'codelen':'5', 'isstring':'1'},
			0x5b:{'name':'JSOP_NEWOBJECT', 'codelen':'5', 'isstring':'1'},
			0x50:{'name':'JSOP_OBJECT', 'codelen':'5', 'isstring':'1'},
			0x53:{'name':'JSOP_OBJWITHPROTO', 'codelen':'1', 'isstring':'1'},
			0x38:{'name':'JSOP_SETELEM', 'codelen':'1', 'isstring':'1'},
			0x9e:{'name':'JSOP_SETELEM_SUPER', 'codelen':'1', 'isstring':'1'},
			0x36:{'name':'JSOP_SETPROP', 'codelen':'5', 'isstring':'1'},
			0x6b:{'name':'JSOP_SETPROP_SUPER', 'codelen':'5', 'isstring':'1'},
			0x2f:{'name':'JSOP_STRICTDELELEM', 'codelen':'1', 'isstring':'1'},
			0x39:{'name':'JSOP_STRICTSETELEM', 'codelen':'1', 'isstring':'1'},
			0x9f:{'name':'JSOP_STRICTSETELEM_SUPER', 'codelen':'1', 'isstring':'1'},
			0x30:{'name':'JSOP_STRICTSETPROP', 'codelen':'5', 'isstring':'1'},
			0x69:{'name':'JSOP_STRICTSETPROP_SUPER', 'codelen':'5', 'isstring':'1'},
			0xe1:{'name':'JSOP_TOID', 'codelen':'1', 'isstring':'1'},
			0xce:{'name':'JSOP_ARRAYPUSH', 'codelen':'1', 'isstring':'1'},
			0xda:{'name':'JSOP_HOLE', 'codelen':'1', 'isstring':'1'},
			0x60:{'name':'JSOP_INITELEM_ARRAY', 'codelen':'5', 'isstring':'1'},
			0x5f:{'name':'JSOP_INITELEM_INC', 'codelen':'1', 'isstring':'1'},
			0xd9:{'name':'JSOP_LENGTH', 'codelen':'5', 'isstring':'1'},
			0x5a:{'name':'JSOP_NEWARRAY', 'codelen':'5', 'isstring':'1'},
			0x66:{'name':'JSOP_NEWARRAY_COPYONWRITE', 'codelen':'5', 'isstring':'1'},
			0x7e:{'name':'JSOP_SPREADCALLARRAY', 'codelen':'5', 'isstring':'1'},
			0xa0:{'name':'JSOP_REGEXP', 'codelen':'5', 'isstring':'1'},
			0xa7:{'name':'JSOP_CLASSCONSTRUCTOR', 'codelen':'5', 'isstring':'1'},
			0xa8:{'name':'JSOP_DERIVEDCONSTRUCTOR', 'codelen':'5', 'isstring':'1'},
			0xb1:{'name':'JSOP_DEBUGCHECKSELFHOSTED', 'codelen':'1', 'isstring':'1'},
			0xcf:{'name':'JSOP_FORCEINTERPRETER', 'codelen':'1', 'isstring':'1'},
			0xe6:{'name':'JSOP_JUMPTARGET', 'codelen':'1', 'isstring':'1'},
			0x77:{'name':'JSOP_LINENO', 'codelen':'5', 'isstring':'1'},
			0x00:{'name':'JSOP_NOP', 'codelen':'1', 'isstring':'1'},
			0xe5:{'name':'JSOP_NOP_DESTRUCTURING', 'codelen':'1', 'isstring':'1'},
			0xe4:{'name':'JSOP_TOSTRING', 'codelen':'1', 'isstring':'1'}}
	def invoke(self, args, from_tty):
		argv = gdb.string_to_argv(args)
		bytecode = gdb.parse_and_eval("$bytecode")
		bytecode = int(bytecode)
		if bytecode in self._BYTECODES:
			codeinfo = self._BYTECODES[bytecode]
			bytecodeptr = gdb.parse_and_eval("$bytecodeptr")
			bytecodeptr = self.hex_PN.findall(str(bytecodeptr))[0]
			bytecodearg= gdb.parse_and_eval("$bytecodearg")
			bytecodearg = shiftendian(int(bytecodearg))
			codelen = codeinfo['codelen']

			if codelen == '1':
				mask = 0
			elif codelen == '2':
				mask = 0xff
			elif codelen == '3':
				mask = 0xffff
			elif  codelen == '4':
				mask = 0xffffff
			elif  codelen == '5':
				mask = 0xffffffff
			else:
				print('error')
				exit(0)
			bytecodearg = bytecodearg & mask
			if codeinfo['isstring'] == '1':
				othermsg = str(gdb.execute("getjsname %d"%bytecodearg, to_string = True)).strip()
			else:
				othermsg = ''
			print("%-16s %-25s 0x%-8x %02x %010s%-25s"%(bytecodeptr, codeinfo['name'], bytecodearg, bytecode, "", othermsg))
			gdb.execute('set $codelength = %s'%(codelen))
		else:
			print("bytecode: %02x"%bytecode)
			print("wrong bytecode")
			exit(0)
		return
Pasciistr()
Getjsname()
Pbytecode()
