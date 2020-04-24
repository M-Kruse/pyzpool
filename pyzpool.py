import subprocess

class Zpool(object):
	"""docstring for Zpool"""
	def __init__(self):
		super(Zpool, self).__init__()
		self.pools_json = { "pools": {} }
		self.events_json = { "events": [] }
		
	def __run_cmd(self, cmd_list):
		process = subprocess.Popen(cmd_list,
	        	             stdout=subprocess.PIPE, 
	                	     stderr=subprocess.PIPE)
		stdout, stderr = process.communicate()
		return stdout, stderr
		
	def __get_pools(self):
		stdout, stderr = self.__run_cmd(['zpool', 'list'])
		output = stdout.decode('utf-8').strip()
		pools = output.split("\n")
		del pools[0]
		for line in pools:
			line = line.split(" ")
			line = [i for i in line if i]
			self.pools_json["pools"][line[0]] = {
				"size": line[1],
				"alloc": line[2],
				"free":line[3],
				"frag":line[5],
				"cap":line[6],
				"dedup":line[7],
				"health":line[8]
			}
	
	def __get_events(self):
		stdout, stderr = self.__run_cmd(['zpool', 'events'])
		output = stdout.decode('utf-8').strip()
		events = output.split("\n")
		del events[0]
		for e in events:
			values = e.split(" ")
			timestamp = "{0} {1} {2} {3}".format(values[0],values[1],values[2],values[3])
			event_class = values[4]
			self.events_json["events"].append({"timestamp": timestamp, "event_class":event_class})

	def list(self):
		self.__get_pools()
		return self.pools_json["pools"]

	def events(self):
		self.__get_events()
		return self.events_json