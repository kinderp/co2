from co2.system_calls import ProcessSystemCalls
from co2.system_calls import IOSystemCalls
from co2.core.fs.fs import OFlags

import ipdb
ipdb.set_trace()

ProcessSystemCalls.boot()
assert IOSystemCalls.open('/file', OFlags.O_RDONLY) < 0 # file does not exist, error
assert IOSystemCalls.open('/file', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.open('/file', OFlags.O_RDONLY) > 0

# /dev is created in boot()
#assert IOSystemCalls.mkdir('/dev') > 0
assert IOSystemCalls.mkdir('/etc') > 0
assert IOSystemCalls.open('/etc/resolv.conf', OFlags.O_CREAT | OFlags.O_WRONLY) > 0

assert IOSystemCalls.mkdir('/usr') > 0
assert IOSystemCalls.mkdir('/usr/local') > 0

# /bin is created in boot()
#assert IOSystemCalls.mkdir('/bin') > 0

assert IOSystemCalls.mkdir('/home') > 0
assert IOSystemCalls.mkdir('/home/user1') > 0
assert IOSystemCalls.open('/home/user1/.profile', OFlags.O_CREAT | OFlags.O_WRONLY) > 0

assert IOSystemCalls.mkdir('/home/user2') > 0
assert IOSystemCalls.open('/home/user2/.profile', OFlags.O_CREAT | OFlags.O_WRONLY) > 0

assert IOSystemCalls.mkdir('/home/user3') > 0
assert IOSystemCalls.open('/home/user3/.profile', OFlags.O_CREAT | OFlags.O_WRONLY) > 0

assert IOSystemCalls.mknod('/dev/hda', 1, 1) > 0
assert IOSystemCalls.mknod('/dev/hdb', 1, 2) > 0
assert IOSystemCalls.mknod('/dev/hdc', 1, 3) > 0
assert IOSystemCalls.mknod('/dev/hdd', 1, 4) > 0

assert IOSystemCalls.mkdir('/mnt') > 0
assert IOSystemCalls.mkdir('/mnt/hda') > 0
assert IOSystemCalls.mkdir('/mnt/hdb') > 0
assert IOSystemCalls.mkdir('/mnt/hdc') > 0
assert IOSystemCalls.mkdir('/mnt/hdd') > 0

assert IOSystemCalls.mount('hda', '/mnt/hda') > 0
assert IOSystemCalls.mount('hdb', '/mnt/hdb') > 0
assert IOSystemCalls.mount('hdc', '/mnt/hdc') > 0
assert IOSystemCalls.mount('hdd', '/mnt/hdd') > 0

assert IOSystemCalls.mkdir('/mnt/hda/test') > 0
assert IOSystemCalls.open('/mnt/hda/test/1', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.open('/mnt/hda/test/2', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.mkdir('/mnt/hda/test2') > 0
assert IOSystemCalls.open('/mnt/hda/test2/1', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
import pdb
pdb.set_trace()
assert IOSystemCalls.open('/mnt/hda/test2/2', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.open('/mnt/hda/test2/3', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.open('/mnt/hda/test2/4', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.rmdir('/mnt/hda/test2') > 0

assert IOSystemCalls.umount('hda', '/mnt/hda') > 0

assert IOSystemCalls.mkdir('/mnt/hdb/test') > 0
assert IOSystemCalls.open('/mnt/hdb/test/1', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.open('/mnt/hdb/test/2', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.mkdir('/mnt/hdb/test2') > 0
assert IOSystemCalls.open('/mnt/hdb/test2/1', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.open('/mnt/hdb/test2/2', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.open('/mnt/hdb/test2/3', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.open('/mnt/hdb/test2/4', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.rmdir('/mnt/hdb/test2') > 0

assert IOSystemCalls.umount('hdb', '/mnt/hdb') > 0

assert IOSystemCalls.mkdir('/mnt/hdc/test') > 0
assert IOSystemCalls.open('/mnt/hdc/test/1', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.open('/mnt/hdc/test/2', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.mkdir('/mnt/hdc/test2') > 0
assert IOSystemCalls.open('/mnt/hdc/test2/1', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.open('/mnt/hdc/test2/2', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.open('/mnt/hdc/test2/3', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.open('/mnt/hdc/test2/4', OFlags.O_CREAT | OFlags.O_WRONLY) > 0
assert IOSystemCalls.rmdir('/mnt/hdc/test2')> 0

assert IOSystemCalls.umount('hdc', '/mnt/hdc') > 0
