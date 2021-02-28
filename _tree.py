from co2.system_calls import IOSystemCalls
IOSystemCalls.mkdir("/dev")
IOSystemCalls.mknod("/dev/hda", 1, 1)
IOSystemCalls.mknod("/dev/hdb", 2, 2)

IOSystemCalls.super_table["ram0"].render(0,s_dev="ram0")

IOSystemCalls.mkdir("/test")
IOSystemCalls.mkdir("/test/mnt")
IOSystemCalls.mkdir("/test/mnt2")

IOSystemCalls.mount("hda", "/test/mnt")
IOSystemCalls.mount("hdb", "/test/mnt2")

IOSystemCalls.super_table["ram0"].render(0,s_dev="ram0")

IOSystemCalls.mkdir("/test/mnt/uno")
IOSystemCalls.mkdir("/test/mnt/due")

IOSystemCalls.mkdir("/test/mnt2/quattro")
IOSystemCalls.mkdir("/test/mnt2/cinque")

IOSystemCalls.super_table["ram0"].render(0,s_dev="ram0")

IOSystemCalls.mkdir("/test/mnt/uno/1")
IOSystemCalls.mkdir("/test/mnt/uno/2")
IOSystemCalls.mkdir("/test/mnt/uno/3")

IOSystemCalls.mkdir("/test/mnt/due/4")
IOSystemCalls.mkdir("/test/mnt/due/5")
IOSystemCalls.mkdir("/test/mnt/due/6")

IOSystemCalls.super_table["ram0"].render(0,s_dev="ram0")

IOSystemCalls.mkdir("/test/mnt2/quattro/1")
IOSystemCalls.mkdir("/test/mnt2/quattro/2")

IOSystemCalls.mkdir("/test/mnt2/cinque/1")
IOSystemCalls.mkdir("/test/mnt2/cinque/2")

IOSystemCalls.super_table["ram0"].render(0,s_dev="ram0")

IOSystemCalls.open("/test/mnt/uno/1/file1")
IOSystemCalls.open("/test/mnt/uno/1/file2")

IOSystemCalls.open("/test/mnt/uno/2/file3")
IOSystemCalls.open("/test/mnt/uno/2/file4")

IOSystemCalls.open("/test/mnt/due/4/file5")
IOSystemCalls.open("/test/mnt/due/5/file6")
IOSystemCalls.open("/test/mnt/due/6/file7")

IOSystemCalls.super_table["ram0"].render(0,s_dev="ram0")
