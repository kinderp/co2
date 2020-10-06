# co2
back to the future...

# Early days

Let's suppose to be a developer in early days of computer history when operating systems didn't exist yet:
a common task like writing something on a device as disk(s) could be been a not easy task, it requested a deep knowledge
of device details (data/status registers of device controller) in order to comunicate with the physical device. 
Another problem was portability either between different machine or betweeb different devices of the same type.
Probably code were written in assembly and it wasn't portable to different architecture but because of code were
writtern for a specific device probably an hardware upgrade implied to re-write your procedure for the newer device as well.

Operating systems solved all the above problems (and even more than that) introducing the so called `I/O subsystem`.

The main functions of `I/O subsystem` are:

* Control I/O devices
* Issue comands to the devices
* Catch interrupts and handle errors

It also provide a **common interface between the devices and the rest of the system** that is:

* simple
* easy to use
* be the same for all the different devices (common or device independent)

so let's dive into the `I/O subsystem`.

# I/O subsystem

## I/O Hardware

### I/O devices

I/O subsystem deals with two different types of devices:

* **block devices**: stores information in fixed-size blocks (each one with its own address: **block addressable**). The essential property of block devices is that is possible to read or write each block independently of all the other ones. Disks are the most common block devices

* **character devices**: deliver or accept a stream of characters, without regard any block structure. It is **not addressable** and not have any seek operation. Printes, network cards, mice are the most common ones

Anyway the boundary between block and chars devices are not so well defined but it's a enough good **general abstraction** that can be used as a basis for making os I/O interface **device independent**

Filesystem, for example, deals only with **abstract block devices** and leave the device-dependent (talking with the **device controller**) part to "lower-level" software called **device driver**

### Device controllers

I/O units consist of a mechanical compoennt and an electronic component.
The electronic component is called the **device controller** or **adapter**, in a PC it takes the form of a printed circuit card that can be inserted in an expansion slot.
Ofc the mechanical component is the device itself.
**The operating systems deals with the controller**, not the device.
**Interface between the controller and the device is low-level** (serial bit of stream with preamble, tracks and checksum)
With the controller, the operating system initializes the controller with some parameters and then lets the controller take care of actually driving the device.


```
________________________________________________
_________Some_kind_of_BUS_______________________Towards Memory,CPU and other I/O devices
           | |
           | |
+------------------------+
|                        |
| Device controller      |  The  device  controller  transforms  the  serial  bits stream into a block
| (electronic component) |  of bytes ( stored in some internal buffer ) and permorfs errors correction.
|                        |  After checksum has been verified, the block of bytes can be to main memory.
+------------------------+
           | |         
           | | Low level interface, formatted (preamble + tracks) streams of bits
           | |
+------------------------+
|                        |
| Physical Device        |
| (mechanical component) |
|                        |
+------------------------+
```

## I/O Software

As already explained, the most important goal of I/O software is **device independence**. It means that should be possible to **write programs that can access any I/O devices without having to specify the device in advance**. For example, a program that reads a file as input should be able to read a file on an hard disk or and external ssd device **without having to modify the program for each different device**. **It is up to the operating system to take care of the problems caused by the fact that these devices are different and require different command sequences to read or write**.
Other tasks are error handling, buffering or make operations that are actually interrupt-driven look blocking to the end user programs (e.g. synchronous/blocking vs asynchronous/interrupt-driven transfers) but we're not interested in all of these.

I/O software is often organized in four layers:

```

+-----------------------------------------------+
|              User-level I/O software          | layer 4
+-----------------------------------------------+
| Device independent operating systems software | layer 3
+-----------------------------------------------+
|                  Device drivers               | layer 2
+-----------------------------------------------+
|                Interrupt handlers             | layer 1
+-----------------------------------------------+
|                   Hardware                    |
+-----------------------------------------------+

```

### Interrupt handlers

I/O operations can take some time. Once a user-level I/O software (a process in memory) has requested an
operation (read/write) it can just stands by that operation completes. It's the device driver (who really
knows how to talk to the physical device) that blocks itself (and so implicitly user-level software) until 
the I/O has completed. When I/O operation finally completes an hardware interrupts is raised by physical 
device and it is cathed by the corresponding interrupt handler that will handle the interrupt and then will
unblock the driver that started it. The effect of an interrupt wil lbe that a driver that was previously 
blocked will be able to run again

### Device drivers

I/O devives are really different from each others in terms of registers for read/write commands or for status
notification, the nature of commands vary radically from device to device as well.
Thus each I/O device attached to a computer needs some device-specific code for controlling it. This code called
the **device driver**, is generally written by the devices's manufacter. Operating systems needs this code in 
order to provide I/O operations.
Device drivers depending of the operating systems can be part of the kernel or it can be loaded as user-mode
process.
As mentioned before, operating systems usually classify driver as:

* **block devices**
* **character devices**

Opeting systems usually define a **standard interface that all block driver must support** and a second **standard interface
that all character driver must support**. These interfaces consist of a number of procedures that the rest of the operating
system can call to get the driver to do work for it.

```
+-----------------------------------------------+
|              User-level I/O software          | layer 4
+-----------------------------------------------+
| Device independent operating systems software | layer 3
|                                               |
|  +---------------------+--------------------+ |
|  | interface all block | interface all char | |
|  | driver must support | driver must support| |
|  +------| |------------+------------| |-----+ |
+---------| |-------------------------| |-------+
|                  Device drivers               | layer 2
+-----------------------------------------------+
|                Interrupt handlers             | layer 1
+-----------------------------------------------+
|                   Hardware                    |
+-----------------------------------------------+
```

In general terms, the job of a device driver is to accept abstract I/O requests from the device-independent software above it and see
to it that the request is really executed. Some tasks in this operation are:
* check that input parametes are valid and return an error if not
* translate abstract I/O request to the concrete forms (which operations send to device-controller and in what sequence)
* Once determinated which commands to issue to the device controller, start all them writing into the controller's device registers

After the commnd or commands have been issued one of the two situations will apply:
* the device driver must wait until the controller does some work for it, so it blocks itself until the interrupt comes in to unblock it
* the operations finish without delay, so the driver does not need to block
After the operations have been completed it must check for errors and if all is right the driver may have data to pass to the device-independent
software (e.g. a disk block just read)
Dealing with requests for reading and writing is the main function of a driver, but there may be other ones:
* the driver may need to initialize a device at system startup or the first time it is uded
* handle Plug 'n Play
* log events

## Device-Independent I/O software

The basic function of the device-independent software is to perform the I/O functions that are common to all devices and to provide a uniform
interface to the user-level software.
Below the typical operations done in the device-independent software

```
+--------------------------------------------+
| Uniform interfacing for device driver      |
+ -------------------------------------------+
| Buffering                                  |
+--------------------------------------------+
| Error reporting                            |
+--------------------------------------------+
| Allocating and releasing dedicated devices |
+--------------------------------------------+
| Providing a device-independent block size  |
+--------------------------------------------+
```

### Uniform interfacing for Device Drivers

A major issue in an operating system is how to make all I/O devices and drivers look more-or-less the same.
If disks, printers, monitors, keyboards, etc., are all interfaced in different ways, every time a new peripheral
device comes along the operating system must be modified for the new device.
It's not acceptable a design in which each device driver has a different interface to the operating system. A good
design is that one in which all drivers have the same interface towards the operating system.
With a standard interface is is much easier to plug in a new driver, providing it conforms to the driver interface.
It also means that driver writers know what is expected to of them (e.g. what funcitons they must provide and what
kernel functions theu may call).

Another IMPORTANT aspect of having a uniform interace is how I/O devices are named. **The device-independet software
takes care of mapping symbolic device names onto the proper driver**. For example, in UNIX a device name, such as `/dev/hda0`,
uniquely specifies the **i-node** for a **special file**, and this i-node contains:
* the **major device number** which is uded to locate the appropriate driver
* the **minor device number**, which is passed as a parameter to the driver in order to specify the unit to be read or written
All devices have major and minor numbers, and all drivers are accessed by using the major device number to select the driver.


## User-level I/O software

Although most of the I/O software is within the operating system, a small portion of it consists of **libraries** linked together
with user programs, and even whole programs running outside the kernel.
System call, including the **I/O system calls**, are normally made by library procedures.
When a C program contains the call: 

```c
count = write(fd, buffer, nbytes) // library procedure which will call corresponding system call
```

the library procedure `write` will be linked with the program and contained in the binary program present in memory at run time.
The collection of all these library procedures (`write`, `read` etc.) is clearly part of the I/O system.

Usually these procesures (`write`, `read`) do little more than put their parameters in the appropriate place for the system call, others
like `printf`, `scanf` make some formatting work before calling a system call 


Collection of all these procedures is the standard I/O library and all run as part of user programs.

Below a summary of the I/O layers

```
    Abstract layers                                                        ALL Concrete Layers (not only I/O)
+---------------------+                                           +------+-----------------+-----+-----------------+
|   User processes    | Make I/O call, format I/O                 | Init | User process #1 | ... | User Process #n |
+---------------------+                                           +------+--+--------+-----+-----+-------+---------+
|  Device-independent | Naming, Protection, blocking,             | Process | File   |       ...         | Network |
|      software       | buffering, allocation                     | manager | system |       ---         | manager |
+---------------------+                                           +---------+---+----+-----+-----+-----------------+
|   Device drivers    | Set up device registers, check status     | Disk driver |TTY driver| ... | Ethernet driver |
+---------------------+                                           +--------+----+-------+--+-----+----+------------+
| Interrupt handlers  | Wake up driver when I/O completed         | Kernel | Clock task | System task |     ...    |
+---------------------+                                           +--------+------------+-------------+------------+
|      Hardware       | Perform I/O operation                     |                     HARDWARE                   |
+---------------------+                                           +------------------------------------------------+
```

When a user program tries to read a block from a file, for example, the operating system is invoked (system call)
to carry out the call. The device-independent software looks for it in the buffer cache. If the needed block is not
there, it calls the device driver to issue the request to the hardware to go get it from disk. The process is then
blocked unitl the disk operation has been completed.
When the disk is finished, the hardware generates an interrupt. The interrupt handler is run to discover what has 
happened, that is, which device wants attention right now. It then extracts the status from the device and wakes up
the sleeping process (device-driver) to finish off the I/O request and let the user process continue.

## At User (sys-admin) perspective

Let's see how all this theory is translated pratically in sys-admin daily basis work.

Suppose you are a sys-admin and your today task consists of preparing a new disk for a dev machine

Note: we will see how to do that manually, block devices are created automatically by udev at run-time
      and probably most of sys-admins do not use anymore cli tools (`fdisk`) for formatting HDs. But we
      are interested in what happens under the hood and so will show manual process for that.
      
You will:

1. create a new block device file (a UNIX special file) using `mknod` command for the new disk.
           
           
            In order to use mknod you need to know the major and minor node numbers for the device to create. 
            The  devices.txt  file  in the kernel source documentation is the canonical source of this infos.
           
            mknod <device-name> <device-type> <major-number> <minor-number>
            
            (*) device-name - full name of device (e.g. /dev/random etc.)
            
            (*) device-type - device files can represent 2 types of device , a 
                              storage device (block) or a device use for other 
                              purpose (character).
                              Block devices are stuff like cd-roms, hard drives
                              etc . Character devices are things like /dev/zero 
                              /dev/null, or any other device not used to  store 
                              info. As you probably have guessed, for mknod "b" 
                              means block, and "c" means character
           
            (*) major-number - a number referring to what type the device is in
            (*) minor-number - the number of the device within the group
           
            We suppose it's a good old IDE drive (/dev/hdX)
           
            /dev/hda is the master IDE drive on the primary IDE controller. 
            /dev/hdb is the slave drive on the primary controller. 
            /dev/hdc and /dev/hdd are the master and slave devices on the 
            secondary controller respectively. 
           
            Each disk is divided into partitions. 
           
            Partitions 1-4 are primary partitions and partitions 5 and above are 
            logical partitions inside extended partitions. 
            Therefore the device file which references each partition is made up
            of several parts. 
            For example /dev/hdc9 references partition 9 (a logical partition in-
            side an extended partition type) on the master IDE drive on the 2-th 
            IDE controller. 
           
            The major and minor node numbers are somewhat complex. 
            For 1st IDE controller all partitions are block devices  on major 3 
            Master drive hda is at minor 0 and slave drive hdb is at  minor  64 
            For each partition inside the drive add the partition number to the
            minor node number for the drive. 
            For example /dev/hdb5 is major 3, minor 69 (64 + 5 = 69). 
            Drives on the secondary interface are handled the same way, but with
            major node 22.
           
           
   Suppose our new IDE disk is attached on the 2nd IDE controller as master drive.
   Our mknod command will be somethink like this:
   
   `mknod /dev/hdc 22 0`
   
   A new device file `hdc` will appear in `/dev`
   
2. create a new primary partition in that device using `fdisk`


           # fdisk  /dev/hdc

           The number of cylinders for this disk is set to 9729.
           There is nothing wrong with that, but this is larger than 1024,
           and could in certain setups cause problems with:
           1) software that runs at boot time (e.g., old versions of LILO)
           2) booting and partitioning software from other OSs
              (e.g., DOS FDISK, OS/2 FDISK)

           Command (m for help): n
           First cylinder (2662-5283, default 2662):
           Using default value 2662
           Last cylinder, +cylinders or +size{K,M,G} (2662-3264, default 3264):
           Using default value 3264
           
           .... Other stuff below, like:
           .... choose partition type
           .... save and exit
           

   at the end a new device file `hdc1` for the new partition will appear in `dev`
   
3. Format the new partition `mkfs.ext4 /dev/hdc1`
4. Mount the new partition in a mount point of your choice (e.g. /mnt/code) : `mount /dev/hdc1 /mnt/code`

After that, the new disk is ready to be used. A developer can for example do something like this:

* `cd /mnt/code`
* `touch hello_world.sh`
* `echo "echo hello world" > hello_world.sh`
* `chmod u+x ./hello_world.sh`
* `./hello_world.sh`

If you wanna see the `OS I/O subsystem` at work you can do this:

 ```
m hello_world.sh; strace touch hello_world.sh 2>&1 |grep \
> hello_world;strace 2>&1 echo echo hello world > hello_world.sh|grep hello

execve("/usr/bin/touch", ["touch", "hello_world.sh"], 0x7ffe6c1f5408 /* 107 vars */) = 0
openat(AT_FDCWD, "hello_world.sh", O_WRONLY|O_CREAT|O_NOCTTY|O_NONBLOCK, 0666) = 3
execve("/usr/bin/echo", ["echo", "echo", "hello", "world"], 0x7fff9a73b068 /* 107 vars */) = 0
write(1, "echo hello world\n", 17)      = 17
```

1. `touch` command is executed by `execve()` call
2. `hello_world.sh` is opened (`openat()` is like `open()` we're not interested in little differences)
3. `echo` command is executed by `execve()` call
4. `echo hello world` is written by `write()` call

```
+---------------------+                    - Layer 4 - User processes -
|                     | Echo runs in user space and in order to write something in the new block device
|                     | it uses aN  I/O  library function that will call the write() system call at the 
|        echo         | below level (level3: Device independent software). write() would have been used
|                     | even if hello world would have been written in a SSD disk thanks to the layer 3
|                     | that provides a COMMON / UNIFORM DEVICE INDEPENDENT interface to the developers
+---------------------+-                   - Layer 3 - Device Independent Software -
|                     | This level is responsible to translate abstract requests as write() in concrete     
|        write()      | ones identifying the correct device driver to whom forward the incoming request
|                     | Driver is selected using major and minor numbers defined when /dev/hdc file was
|                     | created with mknod
+---------------------+
|                     |
|  IDE Disk(s) driver | 
|                     |
+---------------------+
| Physical device     |
+---------------------+
```

## Everything is a file

We conclude this high level `I/O` overview with this big UNIX rule: [Everything is a file](https://en.wikipedia.org/wiki/Everything_is_a_file)

`I/O subsystem` **provides a DEVICE INDEPENDENT interface** with simply one BIG idea, **treating all devices 
in the system as files** (even if special:block/character/pipe) and **move down the interaction code with the device 
controller** to level 2 hiding its complexity and details to the user-space programmers.

It would be nice having the same simple and powerful way to manage resources in the cloud.

In order to achive the same power and simplicity in managing devices in a modern cloud infrastructure we should 
before examine which kind of servives and common deplyment models we have to deal with there.
Deployment models regards how infrastructure is architected, on top of these different types of infrastructures different services will be deployed. 

We'll work on AWS
 
# AWS

## Region & Availability Zones

**A region is a geographic location spread throughout the world** with the idea that a disaster or something in one area of the world will not affect a different area. 

By having regions all around the world, there are also **some performance benefits in getting the data and services closer to your users**. 

So what is the difference between a region and an availability zone? 

**An availability zone is an isolated set of resources within a region**. 

**Each region has at least two availability zones**. 

The idea is that a fire or power outage in one availability zone should not affect another availability zone. 

Each availability zone is also connected via a high-speed network connection. This allows you to architect and run as if you're in the same data center, but with the benefit that if something happens in one availability zone it usually does not affect all of the other availability zones in the region. 

Not all regions have all AWS services available. As a new service is introduced, usually it starts in a few regions, then it will expand to all regions. 

Be aware the price per hour differs slightly from one region to the other. Depending on the service, the cost difference can be significant, so you want to consider that as you're choosing which region to use to run your service.

## Instance Deployment Models

Let's go through some examples on best practices for instance deployment. 

We'll start out with the **single instance model**. This is where within the AWS Cloud you have a single AWS region and a single availability zone in which you place a single instance. This is the most basic setup, and obviously has a **single point of failure**, however, this does have its uses for development or proof of concept, where you're trying to keep costs down and keep things simple to get started on a project. This is not a recommended architecture for a production scenario due to the single point of failure, however, the reality is many applications are a monolithic application that runs on a single server. Many times you can get better reliability out of a server on the cloud than a physical server in your data center. 

```

Single Instance MODEL:

                                 (R) some kinf of resource/service
                                     - EC2 instance
+-------------------+                - DynamoDB
| AWS Cloud         |                - RDS
| +--------------+  |                - ELB
| | AWS Region   |  |                - S3 bucket
| | +---------+  |  |                 
| | | AZ      |  |  |
| | | +-----+ |  |  |
| | | | (R) | |  |  |
| | | +-----+ |  |  |
| | +---------+  |  |
| +--------------+  |
+-------------------+
```

The next step would be to deploy **multiple instances**. In this scenario, we have the AWS cloud and a single region still within the cloud, but instead of a single availability zone we have two. In those, you place one or more instances. For this example, let's just say **we put one instance in each availability zone** for a total of two instances. AWS provides **elastic load balancing** ( `ELB` ) options to direct traffic to your instances in each availability zone. With this setup, you are now redundant both in your instances and in your availability zones. AWS helps you out in that an elastic load balancer must have at least two instances in two different availability zones in order to send traffic to those instances. You can also perform live updates to your application by taking certain instances out of the load balancer, updating them, then introducing them back to live traffic. This is used for many production scenarios where **region failure is an acceptable risk**, meaning in your assessment the likelihood of a region failing is not great enough for you to take the next step and move to a more complex architecture. 

```

Multiple Instance MODEL:

+-------------------------------+
| AWS Cloud                     |
| +--------------------------+  |
| | AWS Region               |  |
| |                          |  |
| |      +----(ELB)----+     |  |
| |     \|/           \|/    |  |
| | +---------+  +---------+ |  |
| | | AZ #1   |  | AZ #2   | |  |
| | | +-----+ |  | +-----+ | |  |
| | | | (R) | |  | | (R) | | |  |
| | | +-----+ |  | +-----+ | |  |
| | +---------+  +---------+ |  |
| +--------------------------+  |
+-------------------------------+
```



If you do find that region failure is not an acceptable risk, then you would move to **multiple instances and multiple regions**. In this model, you would select two different AWS regions. Within each region you would still have at least two availability zones, and within each of those you would have at least one instance. Each region would have its own elastic load balancer, then **in order to wrap traffic between the regions, you would use Amazon Route 53**, which is their `DNS` service. This will allow you to set up various scenarios of two live regions, one warm standby region, or a backup region. Multi-region is the most complex architecture. It also has the highest cost. In this example, supposing we only needed the compute power of a single instance, this would cost four times as much as the single instance model and twice as much as the single region model. It does, however, give you the highest level of redundancy. Before going to a multiple region architecture, consider carefully all pieces of your system, including the instances, databases, S3 buckets, or other third-party services that your application depends on. You could have a multi-region architecture, yet still have a weak link that could take your system down.

```

Multiple Instances & Multiple Regions MODEL:

+--------------------------------------------------------------------------+
| AWS Cloud                                                                |
|                                                                          |
|            +--------------------(R53)------------------+                 |
|            |                                           |                 |
|           \|/                                         \|/                |
| +--------------------------+              +--------------------------+   |
| | AWS Region               |              | AWS Region               |   |
| |                          |              |                          |   |
| |      +----(ELB)----+     |              |      +----(ELB)----+     |   |
| |     \|/           \|/    |              |     \|/           \|/    |   |
| | +---------+  +---------+ |              | +---------+  +---------+ |   |
| | | AZ #1   |  | AZ #2   | |              | | AZ #1   |  | AZ #2   | |   |
| | | +-----+ |  | +-----+ | |              | | +-----+ |  | +-----+ | |   |
| | | | (R) | |  | | (R) | | |              | | | (R) | |  | | (R) | | |   |
| | | +-----+ |  | +-----+ | |              | | +-----+ |  | +-----+ | |   |
| | +---------+  +---------+ |              | +---------+  +---------+ |   |
| +--------------------------+              | +------------------------+   |
+--------------------------------------------------------------------------+

```

## VPC & Subnets

Let's to discuss now the different AWS networking services, including **Virtual Private Cloud** (`VPC`); **Elastic Load Balancing**, `ELB`; `Route 53`; `API Gateway` etc. We'll discuss what the service does and when you might use the service. We'll also take a look at some example use cases so you can see how you might implement these services in your projects. 

You can think of a **VPC** as a **logically isolated piece of the AWS cloud**. It's like your own private data center. The VPC is the foundation for all `EC2` instances, meaning if you're going to use an EC2 or a compute instance, all of the virtual machines offered by Amazon, you will be using a VPC. 

This is where you can define **subnets**, **define IP address ranges** for your instances, as well as **configure access control** to and from your instances.

**Let's take a look at the architecture of the VPCs** summaring some rules: 

1. Within the AWS cloud we have regions. 

2. VPCs belong to a region. 

3. Your VPC will span all availability zones in that region, and you can have multiple VPCs within the same region. 

4. Your VPC will contain one or more subnets. 

5. A subnet is tied to a single availability zone. 

5. your EC2 instances will be launched into a specific subnet. 


```

+-------------------------------------------------------------------------------------------------------------+
| AWS Cloud                                                                                                   |
|                                                                                                             |
| +--------------------------------------------------------------------------------------------------------+  |
| | AWS Region                                                                                             |  |
| |                                                                                                        |  |
| |                   +-------------------------------------+  +-------------------------------------+     |  |
| |                   | VPC #1                              |  |  VPC #2                             |     |  |
| |   +-------------------------------------------------------------------------------------------------+  |  |
| |   | AZ #1         |                                     |  |                                     |  |  |  |
| |   |               |  +-------------+    +-------------+ |  |  +-------------+    +-------------+ |  |  |  |
| |   |               |  | Subnet #1   |    | Subnet #2   | |  |  | Subnet #1   |    | Subnet #2   | |  |  |  |
| |   |               |  |             |    |             | |  |  |             |    |             | |  |  |  |
| |   |               |  |  (R)   (R)  |    | (R)    (R)  | |  |  |  (R)  (R)   |    |  (R)  (R)   | |  |  |  |
| |   |               |  |             |    |             | |  |  |             |    |             | |  |  |  |
| |   |               |  +-------------+    +-------------+ |  |  +-------------+    +-------------+ |  |  |  |
| |   |               |                                     |  |                                     |  |  |  |
| |   +-------------------------------------------------------------------------------------------------+  |  |
| |                   |                                     |  |                                     |     |  |
| |                   |                                     |  |                                     |     |  |
| |   +-------------------------------------------------------------------------------------------------+  |  |
| |   | AZ #2         |                                     |  |                                     |  |  |  |
| |   |               |  +-------------+    +-------------+ |  |  +-------------+    +-------------+ |  |  |  |
| |   |               |  | Subnet #1   |    | Subnet #2   | |  |  | Subnet #1   |    | Subnet #2   | |  |  |  |
| |   |               |  |             |    |             | |  |  |             |    |             | |  |  |  |
| |   |               |  |  (R)   (R)  |    | (R)    (R)  | |  |  |  (R)  (R)   |    |  (R)  (R)   | |  |  |  |
| |   |               |  |             |    |             | |  |  |             |    |             | |  |  |  |
| |   |               |  +-------------+    +-------------+ |  |  +-------------+    +-------------+ |  |  |  |
| |   |               |                                     |  |                                     |  |  |  |
| |   +-------------------------------------------------------------------------------------------------+  |  |
| |                   |                                     |  |                                     |     |  |
| |                   |                                     |  |                                     |     |  |
| |                   +-------------------------------------+  +-------------------------------------+     |  |
| |                                                                                                        |  |
| +--------------------------------------------------------------------------------------------------------+  |
|                                                                                                             |
+-------------------------------------------------------------------------------------------------------------+

```
When you create an AWS account, Amazon creates a default VPC for you in each region. This allows you to launch virtual machines for the EC2 service without really having to configure or think about anything. This can work really well for simple applications where you don't need to define multiple subnets or have control around the IP address ranges that are being used. Each region will have a default VPC with a subnet in each availability zone. This allows you to launch EC2 instances wherever you need them. As your application grows, you can modify the default VPC or you can create additional VPCs that are suited for your needs. 

Behind the scenes is a massive network infrastructure. Within each availability zone and between availability zones in the same region is a private AWS network. This is highly over-provisioned, highly scalable, and very high throughput. Availability zones are connected and designed for extremely low latency, as if you were in the same data center. At the edge of the private network, AWS utilizes several different public internet providers to ensure high availability, high throughput, and low latency of all network traffic. Amazon also has their own global network backbone which provides region-to-region connection. This ensures privacy, speed, and reliability. When you launch EC2 instances into your network, the speed of those instances will vary by instance type.

## Deployment tree

A deployment model cam be though as a tree like in the below figure:

```
                                            (app)
                                              |
                                              |
                +-----------------------------+------------------------------+
                |                                                            |
                |                                                            |
              (vpc1)                                                       (vpc2)
                |                                                            |
                |                                                            |
       +--------+---------+                                         +--------+---------+           
       |                  |                                         |                  |
       |                  |                                         |                  |
     (sub1)             (sub2)                                    (sub1)             (sub2)
       |                  |                                         |                  |
       |                  |                                         |                  |
+---+---+---+---+      +---+---+                             +---+---+---+---+      +---+---+
|   |   |   |   |      |   |   |                             |   |   |   |   |      |   |   |
(R) (R) (R) (R) (R)    (R) (R) (R)                           (R) (R) (R) (R)  R)    (R) (R)  R)
```

