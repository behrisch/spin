#!/bin/sh

sleep 5

#Enable SATA link power management for host0
echo 'min_power' > '/sys/class/scsi_host/host0/link_power_management_policy'
#Enable SATA link power management for host1
#Switched to max_performance because min_power is causing excessive screen flicker
#echo 'min_power' > '/sys/class/scsi_host/host1/link_power_management_policy'
echo 'max_performance' > '/sys/class/scsi_host/host1/link_power_management_policy'
#Enable Audio codec power management
echo '1' > '/sys/module/snd_hda_intel/parameters/power_save'
#Autosuspend for USB device Synaptics HIDUSB TouchPad V07 [SYNAPTICS]
#Disabled, has very long wakeup
#echo 'auto' > '/sys/bus/usb/devices/1-2/power/control'
#Autosuspend for USB device Touchscreen [ELAN]
echo 'auto' > '/sys/bus/usb/devices/1-9/power/control'
#Runtime PM for PCI Device Intel Corporation Sky Lake Host Bridge/DRAM Registers
echo 'auto' > '/sys/bus/pci/devices/0000:00:00.0/power/control'
#Runtime PM for PCI Device Realtek Semiconductor Co., Ltd. Device 522a
echo 'auto' > '/sys/bus/pci/devices/0000:02:00.0/power/control'
#Runtime PM for PCI Device Intel Corporation Wireless 7265
echo 'auto' > '/sys/bus/pci/devices/0000:01:00.0/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d23
echo 'auto' > '/sys/bus/pci/devices/0000:00:1f.4/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d70
echo 'auto' > '/sys/bus/pci/devices/0000:00:1f.3/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d21
echo 'auto' > '/sys/bus/pci/devices/0000:00:1f.2/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d46
echo 'auto' > '/sys/bus/pci/devices/0000:00:1f.0/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d2f
echo 'auto' > '/sys/bus/pci/devices/0000:00:14.0/power/control'
#Runtime PM for PCI Device Intel Corporation Device 1903
echo 'auto' > '/sys/bus/pci/devices/0000:00:04.0/power/control'
#Runtime PM for PCI Device Intel Corporation Sky Lake Imaging Unit
echo 'auto' > '/sys/bus/pci/devices/0000:00:05.0/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d03
echo 'auto' > '/sys/bus/pci/devices/0000:00:17.0/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d18
#Disabled, causes very long wakeup for touchpad
#echo 'auto' > '/sys/bus/pci/devices/0000:00:1d.0/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d19
echo 'auto' > '/sys/bus/pci/devices/0000:00:1d.1/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d3a
echo 'auto' > '/sys/bus/pci/devices/0000:00:16.0/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d62
echo 'auto' > '/sys/bus/pci/devices/0000:00:15.2/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d63
echo 'auto' > '/sys/bus/pci/devices/0000:00:15.3/power/control'
#Runtime PM for PCI Device Intel Corporation Sky Lake Integrated Graphics
echo 'auto' > '/sys/bus/pci/devices/0000:00:02.0/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d60
echo 'auto' > '/sys/bus/pci/devices/0000:00:15.0/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d31
echo 'auto' > '/sys/bus/pci/devices/0000:00:14.2/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d32
echo 'auto' > '/sys/bus/pci/devices/0000:00:14.3/power/control'
#Runtime PM for PCI Device Intel Corporation Device 9d35
echo 'auto' > '/sys/bus/pci/devices/0000:00:13.0/power/control'

