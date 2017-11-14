import re,os


with open("./jsvmdebug.py") as fi:
	with open("../jsvmdebug.py", "w") as fo:
		fo.write(fi.read())
os.chdir("..")
fscript = open("jsvm.x", "w")
fscript.write("set print pretty on\n")
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
	python print("%03s %-16s %-25s %-10s %02s %04s%-25s"%('', 'address', 'bytecodename', 'argv', 'bytecode', '', 'othermsg'))
	set $bytecode = *($ptr)
	while $i != $count and $bytecode != 153
		set $bytecodeptr = $ptr
		set $bytecode = *($ptr)
		set $bytecodearg = *((uint32_t*)($ptr+1))
		pbytecode
		set $ptr = $ptr + $codelength
		set $i = $i + 1
	end
end
'''

fscript.write(dis)

getname = '''
define getname
	p *(script->getAtom($arg0).value)
end'''

fscript.write(getname)

print 'Generating jsvm.x done!'
