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
+---------------------+
|   User processes    | Make I/O call, format I/O
+---------------------+
|  Device-independent | Naming, Protection, blocking, buffering, allocation
|      software       |
+---------------------+
|   Device drivers    | Set up device registers, check status
+---------------------+
| Interrupt handlers  | Wake up driver when I/O completed
+---------------------+
|      Hardware       | Perform I/O operation
+---------------------+
```
