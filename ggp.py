class Python:
	def __init__(self,port):
		self.path = "python\pythonw.exe"
		self.script = "ggp\manage.py"
		self.args1 = "runserver"
		self.args2 = port

	def Run(self):
		import subprocess as p
		self.proc = p.Popen([self.path,self.script,self.args1,self.args2])

	def Stop(self):
		self.proc.kill()
		import subprocess as p
		# p.call(["clean.exe"])
		# p.call(["taskkill","/IM","pythonw.exe","/F"],stdout=p.PIPE)
		p.call(["taskkill","/IM","pythonw.exe","/F"])

class Browser:
	def __init__(self,url):
		# self.path = "viewer\GoogleChromePortable\GoogleChromePortable.exe"
		self.path = "viewer\FirefoxPortable\FirefoxPortable.exe"
		self.script = url
		# self.args1 = "--disable-extensions"
		# self.args2 = "--start-maximized"

	def Run(self,wait):
		import subprocess as p
		# self.proc = p.Popen([self.path,self.script,self.args1,self.args2])
		self.proc = p.Popen([self.path,self.script])
		if wait: self.Wait()

	def Stop(self):
		self.proc.kill()

	def Wait(self):
		self.proc.wait()

class Shiny:
	def __init__(self,cwd):
		self.path = cwd + r"\dist\R-Portable\App\R-Portable\bin\i386\Rscript.exe"
		self.script = r"dist\script\R\run.R"
		self.args1 = "--vanilla"
		self.args2 = cwd
		self.args3 = "--no-Rconsole"

	def Run(self):
		import subprocess as p
		self.proc = p.Popen([self.path,self.args1,self.args3,self.script],cwd=self.args2)

	def Stop(self):
		self.proc.kill()

ggp_url = "http://localhost"
ggp_port = "9915"

py = Python(ggp_port)
py.Run()

# sh = Shiny(".\lumens")
# sh.Run()

# Wait for the Django to run by checking the url using http request.
counter = 1
counter_max = 10
while True:
	try:
		import urllib
		opener = urllib.FancyURLopener({})
		f = opener.open(ggp_url + ":" + ggp_port)
		break
	except:
		if counter > counter_max: break
		# print counter
		counter+=1


if counter <= 10:
	bw = Browser(ggp_url + ":" + ggp_port)
	bw.Run(wait=True)

	bw.Stop()

py.Stop()
# sh.Stop()

#NOTES: google chrome close, doesn't end the process