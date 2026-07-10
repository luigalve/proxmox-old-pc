# Install Proxmox on an Old PC: troubleshooting and lessons

Generated from the data inside index.html by tools/generate_docs.py.
Never edit this file by hand: change the app data and regenerate.

> Turn a forgotten desktop into a home virtualization server, one step at a time.

## Issues that can hit any setup

### The PC acts strange or refuses to start after a RAM or component upgrade

*Seen at step 1: Recon: know what you have*

Reseat everything you touched. RAM that is not fully clicked into its slot, or a cable nudged loose during the upgrade, causes black screens and random failures that look exactly like software problems. Push until it clicks, and check both ends of every cable.

### The finished drive boots into a Proxmox error or a grub prompt

*Seen at step 2: Make the bootable drive*

This happens when the image was written in ISO mode instead of DD. Re-run the flash and pick 'Write in DD Image mode' at the prompt. If it happens twice, re-download the ISO and verify the checksum in case the file is corrupted.

### I cannot find the virtualization setting anywhere

*Seen at step 3: Prep the firmware*

Look under CPU, Advanced, or Security tabs. Some boards only reveal it after a firmware update. Search your exact PC model plus 'enable virtualization' to get the precise menu path.

### The graphical installer never appears, or the screen comes up garbled

*Seen at step 4: First boot: the black screen gauntlet*

Reboot and pick the Terminal UI install option from the Proxmox menu instead. It is the same installer with a plainer face, and far pickier hardware still accepts it.

### The USB drive does not load the boot menu at all

*Seen at step 4: First boot: the black screen gauntlet*

Move the USB drive to a rear port (if it is back there already, try a different rear port), then recheck boot order and Secure Boot, and reflash the drive to rule out a bad write. As a last resort, reflash in ISO mode purely to test whether the machine can see the drive at all: DD is still the correct write mode for the real Proxmox install, so once the drive shows up, flash it in DD mode again before installing.

### After the reboot, the PC boots back into the installer instead of Proxmox

*Seen at step 5: Run the installer*

The boot process is still looking at the USB drive. Pull the drive when the installer asks for the reboot; if it already looped, remove it and restart. If you set USB first in the boot order earlier, you can now move the internal disk back to the top.

### The page will not load at all

*Seen at step 6: First login, from another device*

This one got me. My laptop was on the guest network, and guest isolation quietly blocks devices from seeing each other, so the server might as well not exist. Join the main network and the page appears. Also confirm you typed https and :8006, and ping the server's IP if you can.

### Everything looks right, but this device runs a VPN

*Seen at step 6: First login, from another device*

A VPN tunnels your traffic out to another network, so as far as your LAN is concerned, your laptop is no longer sitting next to the server. Pause the VPN, or exclude local addresses if it supports split tunneling, reload the page, and reconnect the VPN afterward.

### Connection refused, or the address seems wrong

*Seen at step 6: First login, from another device*

Read the IP straight off the server's own console banner. DHCP may have handed out something different from what you wrote down during the install.

### Refresh or apt fails with a 401 Unauthorized error

*Seen at step 7: Free updates and sensible defaults*

An enterprise repository is still enabled. Disable it under Repositories and refresh again. This is the single most common first-day error in Proxmox.

## Setup-specific issues, step by step

### Step 1: Recon: know what you have

**My 64 GB USB drive flashed perfectly and still would not boot the old Dell: black screen even though the flash reported success** (Older PC)

The fix was not software at all. I switched to a much smaller, older drive and it booted on the first try. If your machine is old, start with a smaller drive.

### Step 2: Make the bootable drive

**The Ventoy drive is invisible to the boot menu or hangs on an old PC** (Ventoy, Older PC)

This is where Ventoy lost me. My older Dell never got along with it. If your PC is old, do not fight this battle, switch to Rufus in MBR mode. That is the exact road I ended up taking.

**Rufus does not list my USB drive** (Rufus)

Try a different port first. If it is an unusual drive, open 'Show advanced drive properties' and enable 'List USB Hard Drives', but make sure you unplug any external hard drives you do not want accidentally wiped before you do. Once they appear in that list, one wrong click at START erases a real drive.

### Step 3: Prep the firmware

**Secure Boot turned itself back on** (Newer PC)

Some boards re-enable it when a firmware security check fails or after an update. Two fixes that work: update the BIOS firmware from the manufacturer's support page, or clear the CMOS (power off and unplug, then remove the coin battery for a minute or use the board's CMOS jumper). Recheck the setting afterward, and expect the date and time to need resetting after a CMOS clear.

### Step 4: First boot: the black screen gauntlet

**Black screen right after choosing Install** (Older PC)

The fix that saved me: move the USB drive to a rear USB 2.0 port and try again. Old machines and USB 3.0 boot handoffs do not mix, and the port swap ended it in one try.

### Step 5: Run the installer

**The installer cannot find my hard disk** (Older PC)

Go back into firmware setup and switch the SATA mode to AHCI, then boot the installer again.

## The full journey, step by step

### Step 1: Recon: know what you have

Ten minutes of looking saves an evening of guessing. This step is pure information gathering, nothing gets changed yet, and the cheat sheet carries the deeper why for every item below.

You're done when: You can answer three questions: Does my CPU support virtualization? Is my PC BIOS or UEFI? Which drive am I willing to erase?

### Step 2: Make the bootable drive

One journey: from an empty USB drive to one that can start the Proxmox installer. Pick your tool below. I used both, and the buttons tell you what actually happened.

You're done when: Your tool reports success and your USB drive is ejected.

### Step 3: Prep the firmware

Three settings stand between you and a clean boot, and all of them live in the setup screen you never visit. The cheat sheet covers how to get in and where each one hides.

You're done when: Virtualization is on, Secure Boot is out of the way, and the PC will look at USB first.

### Step 4: First boot: the black screen gauntlet

The step where old hardware fights back. The actions are the walkthrough; the cheat sheet explains why each move works, and the fixes below include the exact ones that saved this project.

You're done when: The Proxmox installer's initial screen loaded!

### Step 5: Run the installer

Filling out boxes here. One of the boxes erases a disk! So make sure to read that one twice. Reference the cheat sheet below for deeper learning.

You're done when: The PC reboots into Proxmox on its own, no USB attached, and shows a login banner with an address ending in :8006.

### Step 6: First login, from another device

Proxmox has no desktop. You run it from a browser on your normal computer, and this is the moment it starts feeling like a real server.

You're done when: The Proxmox dashboard is on your screen.

### Step 7: Free updates and sensible defaults

Out of the box, Proxmox points at the paid enterprise update channel. Two clicks aim it at the free one, and the cheat sheet explains what those channels and ports actually are.

You're done when: Refresh runs without a 401 error and the upgrade completes. Your server is alive, current, and ready for its first VM.
