import os.path
import traceback

def load(self):
	names=[]
	for root, sub, files in os.walk("./plugins/"):
		for filename in files:
			if filename.startswith('_'): continue
			name, ext = os.path.splitext(filename)
			if ext[1:] in ('py', 'pyw'):
				pathname=os.path.join(root, filename)
				with open(pathname, 'r') as afile:
					c = afile.readline().strip()
					if c ==r'#1dbdc6da34094db4e661ed43aac83d91':
						names.append(name)
	for name in names:
		try:
			# reivnote:
			# __import__('plugins.foo') returns the plugins parent module,
			# so we use getattr to reach inside for the desired plugin
			self.plugins[name] = getattr(__import__('plugins.{}'.format(name)), name)
			current = self.plugins[name]
			current.__init__(self)
			try: 
				if getattr(current, "loop"):
					self.pluginloops.append(getattr(current, "loop"))
			except AttributeError: pass
			try:
				if getattr(current, "exit"):
					self.pluginexit.append(getattr(current, "exit"))
			except AttributeError: pass
			except NameError: pass
		except:
			traceback.print_exc()
		else:
			self.writeLog("---plugin '{}' initialized.".format(name), 1)