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

I/O subsystem deals with two different types of devices:

* **block devices**: stores information in fixed-size blocks (each one with its own address: **block addressable**). The essential property of block devices is that is possible to read or write each block independently of all the other ones. Disks are the most common block devices

* **character devices**: deliver or accept a stream of characters, without regard any block structure. It is **not addressable** and not have any seek operation. Printes, network cards, mice are the most common ones

Anyway the boundary between block and chars devices are not so well defined but it's a enough good **general abstraction** that can be used as a basis for making os I/O interface **device independent**

Filesystem, for example, deals only with **abstract block devices** and leave the device-dependent (talking with the **device controller**) part to "lower-level" software called **device driver**

## 
