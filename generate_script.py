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


getname = '''
define getname
	p *(script->getAtom($arg0).value)
end'''

fscript.write(getname)

print 'Generating jsvm.x done!'
