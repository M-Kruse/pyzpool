import subprocess
import json
import re
import pprint
import itertools

class Zpool(object):
    """docstring for Zpool"""
    def __init__(self):
        super(Zpool, self).__init__()
        ## Add some sanity check to make sure zpool binary exists
        #Init our json objects 
        self.pools_json = { "pools": {} }
        self.status_json = { "pools": {} }
        self.events_json = { "events": [] }
        self.history_json = { "history": [] }
        self.status_json = {"pools": {} }

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
        ##Add error handling
        output = stdout.decode('utf-8').strip()
        events = output.split("\n")
        del events[0]
        for e in events:
            values = e.split(" ")
            timestamp = "{0} {1} {2} {3}".format(values[0],values[1],values[2],values[3])
            event_class = values[4]
            self.events_json["events"].append({"timestamp": timestamp, "event_class":event_class})

    def __get_history(self):
        stdout, stderr = self.__run_cmd(['zpool', 'history'])
        ##Add error handling
        output = stdout.decode('utf-8').strip()
        history = output.split("\n")
        #First line is always the headers, pop it off
        del history[0]
        for h in history:
            values = h.split(" ")
            timestamp = values[0]
            del values[0] #pop off the first one, the timestamp, the rest of the strings are the history
            cmd = " ".join(map(str, values))
            self.history_json["history"].append({"timestamp": timestamp, "command":cmd})

    def __get_status(self):
        """
        Parse the output of zpool status. This is tricky due to the format of the output.
        The config data is the only multiline item not seperated by a semicolon.
        It looks hacky because it is kinda hacky.
        """
        stdout, stderr = self.__run_cmd(['zpool', 'status'])
        ##Add error handling
        output = stdout.decode('utf-8').strip()
        #The only multiline data item in this output is the config which shows the vdev data in a hierarchical format
        config = output[output.find("config:")+len("config:"):output.rfind("errors:")]
        #Parse out the other values, skipping the config we just extracted and remove the dangling 'config:' entry since that is stored separately 
        values = [item.strip() for item in output.split("\n") if item not in config and 'config:' not in item]
        #Pull out the pool name
        pool_name = output[output.find("pool:")+len("pool:"):output.rfind("state:")].strip()
        #Loop through all the values and start building onto the JSON object
        for value in values:
            if self.status_json["status"].get(pool_name):
                self.status_json["status"][pool_name].update({value.split(": ")[0]:value.split(": ")[1]})
            else:
                self.status_json["status"][pool_name] = {value.split(": ")[0]:value.split(": ")[1]}
        for line in config.split("\n"):
            #The only way i can figure to dynamically handle the vdev hierarchical is by the indent/whitespace count since that seems to be consistent
            #The vdevs have 3 and dev members of the vdevs have 5
            lead_spaces = sum( 1 for _ in itertools.takewhile(str.isspace,line))
            if lead_spaces == 3:
                vdev = line.strip().split(" ")[0]
                self.status_json["status"][pool_name]["config"] = {vdev: {}}
            if lead_spaces == 5:
                dev = line.split(" ")
                dev = [item for item in dev if item.strip()]
                #Check if vdev already exists in the json object, if so append otherwise create new list object that you can append any additional drives to
                if self.status_json["status"][pool_name]["config"][vdev].get("devs"):
                    self.status_json["status"][pool_name]["config"][vdev]["devs"].append({"name":dev[0],"state":dev[1], "errors":{"READ":dev[2],"WRITE":dev[3],"CKSUM":dev[4]}})
                else:
                    self.status_json["status"][pool_name]["config"][vdev]["devs"] = [{"name":dev[0],"state":dev[1], "errors":{"READ":dev[2],"WRITE":dev[3],"CKSUM":dev[4]}}]
    
    def __get_iostat(self, pool, rate):
        self.iostat_json = {"pools": {} }
        count = 1
        if rate < 0:
            rate = 1
        if pool:
            cmd = ['zpool', 'iostat', "-y", "-H", pool, str(rate), str(count)]
        else:
            cmd = ['zpool', 'iostat', "-y", "-H", str(rate), str(count)]
        stdout, stderr = self.__run_cmd(cmd)
        ##Add error handling
        output = stdout.decode('utf-8').strip()
        output = output.split("\t")
        #We are basically just caching the latest iostat output, over the last second of time, and caching it our class.
        #Workers can do whatever they want with it from there.
        self.iostat_json["pools"][output[0]] = {
            "capacity": {
                "alloc":output[1],
                "free":output[2]},
                "operations": {
                    "read":output[3],
                    "write":output[4]
                },
                    "bandwidth": {
                            "read":output[5],
                            "write":output[6]
                    }
            }

    def __handle_prop(self, method, zpool, property):
        assert property
        stdout, stderr = self.__run_cmd(['zpool', method, property, '-H'])
        ##Add error handling
        output = stdout.decode('utf-8').strip()
        values = output.split("\t")
        self.property_json["property"][property] = { "name":values[0], "property":values[1], "value":values[2], "source": values[3] }

    def list(self):
        self.__get_pools()
        return json.dumps(self.pools_json["pools"])

    def events(self):
        self.__get_events()
        return json.dumps(self.events_json)

    def history(self):
        self.__get_history()
        return json.dumps(self.history_json)

    def status(self):
        self.__get_status()
        return json.dumps(self.status_json)

    def iostat(self, pool_name=None, query_rate=1):
        self.__get_iostat(pool_name, query_rate)
        return self.iostat_json

    def property(self, pool_name, prop_name, method='get'):
        self.property_json = {"property": {} }
        if method not in ['get']:
            raise Exception("[ERROR] Can only parse 'set' or 'get' for property handler method")
        else:
            self.__handle_prop(method, pool_name, prop_name)
            return self.property_json

if __name__ == "__main__":
    z = Zpool()
    print(z.iostat("ZSTOR"))
