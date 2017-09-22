import re
import os



os.system("wget -O /tmp/Bytecode https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey/Internals/Bytecode")
pattern = re.compile(r'''
 <dt id="([A-Z0-9_]+)">.*</dt>
 <dd>
 <table class="standard-table">
  <tbody>
   <tr>
    <th>Value</th>
    <td><code>\d* \((0x[a-f0-9]+)\)</code></td>
   </tr>
   <tr>
    <th>Operands</th>
    <td><code>.*</code></td>
   </tr>
   <tr>
    <th>Length</th>
    <td><code>(\d+)</code></td>
   </tr>
   <tr>
''')

	
with open("/tmp/Bytecode") as f:
	data = f.read()
	print pattern.findall(data)
	print len(pattern.findall(data))
