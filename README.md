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
>>> z.status()
{'status': {'ZSTOR': {'pool': 'ZSTOR', 'state': 'ONLINE', 'scan': 'resilvered 51.3M in 0h0m with 0 errors on Tue May 21 00:12:13 2019', 'errors': 'No known data errors', 'config': {'mirror-0': {'devs': [{'name': 'scsi-35000cca2530a2c38', 'state': 'ONLINE', 'errors': {'READ': '0', 'WRITE': '0', 'CKSUM': '0'}}, {'name': 'scsi-35000cca2530a2598', 'state': 'ONLINE', 'errors': {'READ': '0', 'WRITE': '0', 'CKSUM': '0'}}]}}}}}
>>> from pprint import pprint
>>> pprint(z.status())
{'status': {'ZSTOR': {'config': {'mirror-0': {'devs': [{'errors': {'CKSUM': '0',
                                                                   'READ': '0',
                                                                   'WRITE': '0'},
                                                        'name': 'scsi-35000cca2530a2c38',
                                                        'state': 'ONLINE'},
                                                       {'errors': {'CKSUM': '0',
                                                                   'READ': '0',
                                                                   'WRITE': '0'},
                                                        'name': 'scsi-35000cca2530a2598',
                                                        'state': 'ONLINE'}]}},
                      'errors': 'No known data errors',
                      'pool': 'ZSTOR',
                      'scan': 'resilvered 51.3M in 0h0m with 0 errors on Tue '
                              'May 21 00:12:13 2019',
                      'state': 'ONLINE'}}}
>>>
>>> for dev in json.loads(z.status())['status']['ZSTOR']['config']['mirror-0']['devs']:
...  print(dev['name'])
... 
scsi-35000cca2530a2c38
scsi-35000cca2530a2598
>>> 
```
