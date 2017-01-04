import fileinput

usercode = ""
for line in fileinput.input():
	usercode += "\t\t\t" + line

bootstrapper = ""
with open("bootstrap.py", "r") as f:
	for line in f:
		bootstrapper += line

bootstrapper = bootstrapper.replace("REPLACETHISTEXTWITHCODE", usercode)

with open("tmp.py", "w") as f:
	f.write(bootstrapper)

try:
	import tmp
except Exception as e:
	print "<span class='error'>" + str(e) + "</span>"
	