# This file is executed on every boot (including wake-boot from deepsleep)
#import webrepl_setup
import webrepl
webrepl.start()

import esp # esp related
import esp32 # esp32 specific related

import machine # machine settings
import gc # garbage collector 
# gc.collect() # clear memory
# gc.mem_free() # print free memory
# esp32 memory: 108608
# >>> import micropython
# >>> micropython.mem_info()
# stack: 720 out of 15360
# GC: total: 111168, used: 20800, free: 90368
#  No. of 1-blocks: 592, 2-blocks: 43, max blk sz: 45, max free sz: 3611

esp.osdebug(None) #set debug to none
gc.collect() # collect all the garbage and clear the memory
machine.freq(240000000) # set the CPU frequency to 240 MHz

