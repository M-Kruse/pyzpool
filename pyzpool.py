import subprocess
import json
import re
import pprint
import itertools

class Zpool(object):
    """docstring for Zpool"""
    def __init__(self):
        super(Zpool, self).__init__()
        self.pools_json = { "pools": {} }
        self.status_json = { "pools": {} }
        self.events_json = { "events": [] }
        self.history_json = { "history": [] }
        self.status_json = {"status": {} }

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
        #The only multiline data item in this output is the config which shows the vdev data in a heirachal format
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
            lead_spaces = sum( 1 for _ in itertools.takewhile(str.isspace,line))
            if lead_spaces == 3:
                vdev = line.strip().split(" ")[0]
                self.status_json["status"][pool_name]["config"] = {vdev: {}}
            if lead_spaces == 5:
                dev = line.split(" ")
                dev = [item for item in dev if item.strip()]
                if self.status_json["status"][pool_name]["config"][vdev].get("devs"):
                    self.status_json["status"][pool_name]["config"][vdev]["devs"].append({"name":dev[0],"state":dev[1], "errors":{"READ":dev[2],"WRITE":dev[3],"CKSUM":dev[4]}})
                else:
                    self.status_json["status"][pool_name]["config"][vdev]["devs"] = [{"name":dev[0],"state":dev[1], "errors":{"READ":dev[2],"WRITE":dev[3],"CKSUM":dev[4]}}]
        

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
        return self.status_json

if __name__ == "__main__":
    z = Zpool()
    z.status()
    pprint.pprint(z.status_json)

# Status structure
# {
#     "pools": {
#         "ZSTOR": {
#             "state": "online",
#             "scan": "PLACEHOLDER DATE",
#             "errors": "0",
#             "config": {
#                 "mirror-0": {
#                     "devs": [{
#                         "name": "scsi-35000cca2530a2c38",
#                         "state": "ONLINE",
#                         "errors": {
#                             "READ": "0",
#                             "WRITE": "0",
#                             "CKSUM": "0"
#                         }
#                     }]
#                 }
#             }
#         }
#     }
# }