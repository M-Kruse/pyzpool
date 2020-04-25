This is a python wrapper for the ZFS admin tool "zpool", to support parsing commands in JSON format.

This is being developed against ZFS On Linux version of zpool. It may not work with other versions and may break if some conventions are changed.

# Usage

## Import

```
>>> from pyzpool import Zpool
>>> z = Zpool()
```

## Command equivalents

`zpool list`

```
>>> import json
>>> json.loads(z.list())['ZSTOR']
{'size': '10.9T', 'alloc': '4.58T', 'free': '6.29T', 'frag': '6%', 'cap': '42%', 'dedup': '1.00x', 'health': 'ONLINE'}
>>> json.loads(z.list())['ZSTOR']['size']
'10.9T'
```

`zpool events`
```
>>> json.loads(z.events())
{'events': [{'timestamp': 'Apr 23 2020 13:49:04.506000729', 'event_class': 'sysevent.fs.zfs.history_event'}, {'timestamp': 'Apr 23 2020 13:49:04.793000752', 'event_class': 'sysevent.fs.zfs.config_sync'}, {'timestamp': 'Apr 23 2020 13:49:04.793000752', 'event_class': 'sysevent.fs.zfs.pool_import'}, {'timestamp': 'Apr 23 2020 13:49:04.795000753', 'event_class': 'sysevent.fs.zfs.history_event'}, {'timestamp': 'Apr 23 2020 13:49:05.091000777', 'event_class': 'sysevent.fs.zfs.config_sync'}]}
>>> json.loads(z.events())['events'][0]
{'timestamp': 'Apr 23 2020 13:49:04.506000729', 'event_class': 'sysevent.fs.zfs.history_event'}
>>> json.loads(z.events())['events'][1]
{'timestamp': 'Apr 23 2020 13:49:04.793000752', 'event_class': 'sysevent.fs.zfs.config_sync'}
```

`zpool status`
```
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

`zpool iostat ${pool_name} 1 -H -y `
```
>>> from pprint import pprint
>>> pprint(z.iostat("ZSTOR"))
{'pools': {u'ZSTOR': {'bandwidth': {'read': u'0', 'write': u'0'},
                      'capacity': {'alloc': u'4.59T', 'free': u'6.29T'},
                      'operations': {'read': u'0', 'write': u'0'}}}}
>>> 
```

`zpool get ${property} ${pool}`
```
>>> z.property("ZSTOR", "alloc")
{'property': {'alloc': {'source': u'-', 'property': u'allocated', 'name': u'ZSTOR', 'value': u'4.59T'}}}
>>> z.property("ZSTOR", "size")
{'property': {'size': {'source': u'-', 'property': u'size', 'name': u'ZSTOR', 'value': u'10.9T'}}}
>>> 

```
