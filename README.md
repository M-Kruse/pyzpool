#pyzpool

```
>>> from pyzpool import Zpool
>>> z = Zpool()
>>> z.list()
'{"ZSTOR": {"size": "10.9T", "alloc": "4.58T", "free": "6.29T", "frag": "6%", "cap": "42%", "dedup": "1.00x", "health": "ONLINE"}}'
>>> import json
>>> json.loads(z.list())
{'ZSTOR': {'size': '10.9T', 'alloc': '4.58T', 'free': '6.29T', 'frag': '6%', 'cap': '42%', 'dedup': '1.00x', 'health': 'ONLINE'}}
>>> json.loads(z.list())['ZSTOR']
{'size': '10.9T', 'alloc': '4.58T', 'free': '6.29T', 'frag': '6%', 'cap': '42%', 'dedup': '1.00x', 'health': 'ONLINE'}
>>> json.loads(z.list())['ZSTOR']['size']
'10.9T'
>>> json.loads(z.events())
{'events': [{'timestamp': 'Apr 23 2020 13:49:04.506000729', 'event_class': 'sysevent.fs.zfs.history_event'}, {'timestamp': 'Apr 23 2020 13:49:04.793000752', 'event_class': 'sysevent.fs.zfs.config_sync'}, {'timestamp': 'Apr 23 2020 13:49:04.793000752', 'event_class': 'sysevent.fs.zfs.pool_import'}, {'timestamp': 'Apr 23 2020 13:49:04.795000753', 'event_class': 'sysevent.fs.zfs.history_event'}, {'timestamp': 'Apr 23 2020 13:49:05.091000777', 'event_class': 'sysevent.fs.zfs.config_sync'}]}
>>> json.loads(z.events())['events'][0]
{'timestamp': 'Apr 23 2020 13:49:04.506000729', 'event_class': 'sysevent.fs.zfs.history_event'}
>>> json.loads(z.events())['events'][1]
{'timestamp': 'Apr 23 2020 13:49:04.793000752', 'event_class': 'sysevent.fs.zfs.config_sync'}
>>> 

```
