from co2.system_calls import IOSystemCalls
from co2.core.fs.fs import OFlags

import ipdb
ipdb.set_trace()

assert IOSystemCalls.open('/file', OFlags.O_CREAT | OFlags.O_WRONLY)

assert IOSystemCalls.mkdir('/dev')
assert IOSystemCalls.mkdir('/etc')
assert IOSystemCalls.open('/etc/resolv.conf', OFlags.O_CREAT | OFlags.O_WRONLY)

assert IOSystemCalls.mkdir('/usr')
assert IOSystemCalls.mkdir('/usr/local')

assert IOSystemCalls.mkdir('/bin')

assert IOSystemCalls.mkdir('/home')
assert IOSystemCalls.mkdir('/home/user1')
assert IOSystemCalls.open('/home/user1/.profile', OFlags.O_CREAT | OFlags.O_WRONLY)

assert IOSystemCalls.mkdir('/home/user2')
assert IOSystemCalls.open('/home/user2/.profile', OFlags.O_CREAT | OFlags.O_WRONLY)

assert IOSystemCalls.mkdir('/home/user3')
assert IOSystemCalls.open('/home/user3/.profile', OFlags.O_CREAT | OFlags.O_WRONLY)

assert IOSystemCalls.mknod('/dev/hda', 1, 1)
assert IOSystemCalls.mknod('/dev/hdb', 1, 2)
assert IOSystemCalls.mknod('/dev/hdc', 1, 3)
assert IOSystemCalls.mknod('/dev/hdd', 1, 4)

assert IOSystemCalls.mkdir('/mnt')
assert IOSystemCalls.mkdir('/mnt/hda')
assert IOSystemCalls.mkdir('/mnt/hdb')
assert IOSystemCalls.mkdir('/mnt/hdc')
assert IOSystemCalls.mkdir('/mnt/hdd')

assert IOSystemCalls.mount('hda', '/mnt/hda')
assert IOSystemCalls.mount('hdb', '/mnt/hdb')
assert IOSystemCalls.mount('hdc', '/mnt/hdc')
assert IOSystemCalls.mount('hdd', '/mnt/hdd')

assert IOSystemCalls.mkdir('/mnt/hda/test')
assert IOSystemCalls.open('/mnt/hda/test/1', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.open('/mnt/hda/test/2', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.mkdir('/mnt/hda/test2')
assert IOSystemCalls.open('/mnt/hda/test2/1', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.open('/mnt/hda/test2/2', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.open('/mnt/hda/test2/3', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.open('/mnt/hda/test2/4', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.rmdir('/mnt/hda/test2')

assert IOSystemCalls.umount('hda', '/mnt/hda')

assert IOSystemCalls.mkdir('/mnt/hdb/test')
assert IOSystemCalls.open('/mnt/hdb/test/1', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.open('/mnt/hdb/test/2', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.mkdir('/mnt/hdb/test2')
assert IOSystemCalls.open('/mnt/hdb/test2/1', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.open('/mnt/hdb/test2/2', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.open('/mnt/hdb/test2/3', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.open('/mnt/hdb/test2/4', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.rmdir('/mnt/hdb/test2')

assert IOSystemCalls.umount('hdb', '/mnt/hdb')

assert IOSystemCalls.mkdir('/mnt/hdc/test')
assert IOSystemCalls.open('/mnt/hdc/test/1', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.open('/mnt/hdc/test/2', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.mkdir('/mnt/hdc/test2')
assert IOSystemCalls.open('/mnt/hdc/test2/1', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.open('/mnt/hdc/test2/2', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.open('/mnt/hdc/test2/3', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.open('/mnt/hdc/test2/4', OFlags.O_CREAT | OFlags.O_WRONLY)
assert IOSystemCalls.rmdir('/mnt/hdc/test2')

assert IOSystemCalls.umount('hdc', '/mnt/hdc')
