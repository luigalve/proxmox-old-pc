# Install Proxmox on an Old PC: the complete guide

Generated from the data inside index.html by tools/generate_full_guide.py.
Never edit this file by hand: change the app data and regenerate.

> Turn a forgotten desktop into a home virtualization server, one step at a time.

This is the whole walkthrough in one file: every step, action, cheat sheet, and fix. Where instructions differ by setup, both versions appear, labeled **Older PC** and **Newer PC**. The interactive version of this guide is the index.html app in this repo.

## The journey at a glance

1. Recon: know what you have
2. Make the bootable drive
3. Prep the firmware
4. First boot: the black screen gauntlet
5. Run the installer
6. First login, from another device
7. Free updates and sensible defaults

## Step 1: Recon: know what you have

Ten minutes of looking saves an evening of guessing. This step is pure information gathering, nothing gets changed yet, and the cheat sheet carries the deeper why for every item below.

**What you need:**

- A device, like an old PC, that will become the Proxmox server
- A USB drive, or external drive, that will be flashed and used to install Proxmox
- A device, like a laptop or the same PC, to download the installer and flash the drive. One PC and one drive is enough to install (that is how new PCs with installation media work), but Proxmox runs headless after install, so plan on a second device with a browser for First Login.

**Actions:**

1. Note the make and model of the PC that will become your Proxmox server. Check the stickers / service tag on the case.
2. Confirm your PC has sufficient RAM (8 GB or more is comfortable) and note the CPU model. On Windows press: Win + R, type dxdiag, press Enter.
3. Confirm the CPU supports virtualization. Enter BIOS setup and look for it directly. It hides under names like VT-x, VT-d, AMD-V, or SVM Mode. If you find it, enable it now and save yourself a return trip.
4. **Newer PC:** Confirm this machine really is UEFI: press Win + R, type msinfo32, press Enter, and read the 'BIOS Mode' line. UEFI should appear for modern devices, and GPT will be your partition answer later. Says Legacy instead? Tap the Older PC button above.
    **Older PC:** Confirm this machine really is BIOS: press Win + R, type msinfo32, press Enter, and read the 'BIOS Mode' line. Legacy should appear for older PCs, and MBR will be your partition answer later. Says UEFI instead? Tap the Newer PC button above.
5. **Newer PC:** Pick a USB or external drive you do not mind wiping completely and note its size.
    **Older PC:** Pick a USB or external drive you do not mind wiping completely and note its size. Aim for a USB that is 16 GB or smaller.

**Recon cheat sheet: the deeper why**

| Item | What to know | Real world |
|---|---|---|
| Identify the model | The exact model unlocks the manual, the spec page, and the right setup keys. Look for a sticker or service tag on the case. | Documenting the model or service tag is the first move on almost every support call, because it turns guessing into looking things up. |
| Check specs fast on Windows | Press Win + R, type dxdiag, press Enter. The System tab shows the model, CPU, and RAM on one screen. | dxdiag works on any Windows box, which is why it's helpful to reach for it before anything else. |
| CPU virtualization (Intel VT-x / AMD-V) | A hardware feature that lets one CPU safely act as several, which is exactly what a hypervisor like Proxmox needs to run virtual machines. | Every VM host depends on it, from an old desktop to enterprise clusters. Factories sometimes ship it disabled, but you can enable it in BIOS setup. |
| RAM and CPU cores | Each running VM reserves its own memory and cores, so the amount of RAM and the CPU model decide how many VMs you can run at once. 8 GB RAM and a CPU with 4+ cores comfortably runs Proxmox plus a couple of light VMs. More RAM and cores mean more and bigger VMs. | Memory is usually the first wall a VM host hits, which is why a RAM upgrade is the simplest thing to do to improve performance. |
| Confirm BIOS (Older PC) | In Windows, msinfo32 shows BIOS Mode: Legacy. At power-on, enter setup (F2 on Dells, Del on many desktops); a keyboard-only blue or gray screen is classic BIOS. | Firmware mode decides your partition scheme (BIOS pairs with MBR), and a mismatch is a top cause of 'my USB will not boot'. |
| Confirm UEFI (Newer PC) | In Windows: msinfo32 shows BIOS Mode: UEFI. At power-on: enter setup; a graphical screen with mouse support is UEFI. | Firmware mode decides your partition scheme (UEFI pairs with GPT), and a mismatch is a top cause of 'my USB will not boot'. |
| The USB drive | 8 to 16 GB is the sweet spot. Older USB 2.0 drives are slow but the safest bet on old machines. Everything on the drive gets erased during flashing. | Enterprises rarely flash by hand: the OS arrives over the network (PXE) or through a management dashboard before a device ever reaches a user. USB installs are the home lab and small shop path, so knowing both worlds is the point. |

**If something goes wrong:**

- **My 64 GB USB drive flashed perfectly and still would not boot the old Dell: black screen even though the flash reported success** (Older PC)
  The fix was not software at all. I switched to a much smaller, older drive and it booted on the first try. If your machine is old, start with a smaller drive.

- **The PC acts strange or refuses to start after a RAM or component upgrade** (All setups)
  Reseat everything you touched. RAM that is not fully clicked into its slot, or a cable nudged loose during the upgrade, causes black screens and random failures that look exactly like software problems. Push until it clicks, and check both ends of every cable.

**You're done when:** You can answer three questions: Does my CPU support virtualization? Is my PC BIOS or UEFI? Which drive am I willing to erase?

## Step 2: Make the bootable drive

One journey: from an empty USB drive to one that can start the Proxmox installer. Pick your tool below. I used both, and the buttons tell you what actually happened.

*Pick your tool: this step has 2 paths. Follow one.*

### Path: Rufus

1. Download the Proxmox VE ISO from proxmox.com: open Downloads and look for the newest 'Proxmox VE ISO Installer'. (The file ends in .iso and is roughly 1.5 GB)
2. Download Rufus from rufus.ie. Look for the latest Standard or Portable .exe; Portable runs with no install at all.
3. Verify the downloads: locate the file you downloaded, right click it, and select Copy as Path. Use the cheat sheet below to find the correct command for your system, then compare the output against the SHA256 checksum listed on the download page. Matching values mean a clean, untampered file.
4. Plug in your USB drive and open Rufus. Confirm the Device box shows your USB, matching the size you noted in Recon.
5. Under Boot selection, click SELECT and choose the Proxmox .iso from your Downloads folder.
6. **Newer PC:** Set Partition scheme to GPT and Target system to UEFI (non CSM), the pairing modern machines expect.
    **Older PC:** Set Partition scheme to MBR and Target system to BIOS (or UEFI-CSM), the pairing old machines expect.
7. Leave File system and the remaining options at their defaults.
8. Click START. When Rufus asks how to write the image, choose 'Write in DD Image mode'. Proxmox officially recommends DD.
9. Wait for the green READY bar, then eject the drive.

### Path: Ventoy

1. Download the Proxmox VE ISO from proxmox.com: open Downloads and look for the newest 'Proxmox VE ISO Installer'. The file ends in .iso and is roughly 1.5 GB.
2. Download Ventoy from ventoy.net: look for the ventoy-windows .zip release, extract it, and run Ventoy2Disk.exe.
3. Verify the downloads: locate the file you downloaded, right click it, and select Copy as Path. Use the cheat sheet below to find the correct command for your system, then compare the output against the SHA256 checksum listed on the download page. Matching values mean a clean, untampered file.
4. **Newer PC:** In Options, set the partition style to GPT.
    **Older PC:** In Options, set the partition style to MBR.
5. Select your USB drive and click Install. This erases the drive and turns it into a Ventoy drive.
6. Copy the Proxmox .iso file onto the new Ventoy partition. No burning step: Ventoy boots ISO files directly.
7. Eject the drive.

**Flash options, decoded**

| Option | What it actually is | What to do here |
|---|---|---|
| Device | The USB drive that gets erased and rebuilt as the boot drive, which will plug into the old PC. | Triple-check it matches your drive's size. Rufus will happily erase and write to any drive it can see. |
| Boot selection | The ISO you downloaded: the entire Proxmox installer packed into a single file. | Point it at the .iso in your Downloads folder. |
| MBR (Master Boot Record) | The classic partition map from the BIOS era: a small table at the very start of the drive that tells old firmware where to boot from. | Pick MBR for old BIOS machines, roughly pre-2012. |
| GPT (GUID Partition Table) | The modern replacement: a larger, smarter map that keeps backup copies of itself, and the format UEFI firmware expects. | Pick GPT for modern UEFI machines. |
| Target system | A label that tells the drive which firmware to introduce itself to: BIOS, UEFI, or both. | Rufus sets it automatically to match your MBR or GPT choice. |
| File system | How the drive's data area is organized (FAT32, NTFS, and so on). | Leave the default. A DD write replaces the whole layout anyway. |
| ISO mode | Writes the installer as ordinary files copied onto the drive. Flexible and readable afterward, but some installers cannot boot this way. | Not this time. |
| DD mode | Clones the ISO onto the drive byte for byte: an exact image of the disk the Proxmox team built. | This is the one. Proxmox is designed to boot from a DD image. |

**Verifying a download (SHA256)**

| Platform | Command |
|---|---|
| Windows PowerShell | Get-FileHash -Path "filePath" -Algorithm SHA256 |
| Windows CMD | certutil -hashfile "filePath" sha256 |
| Linux | sha256sum ~/fileLocation/fileName.fileType |
| macOS | shasum -a 256 ~/fileLocation/fileName.fileType |
| Cross-platform (OpenSSL) | openssl sha256 ~/fileLocation/fileName.fileType |

**If something goes wrong:**

- **The finished drive boots into a Proxmox error or a grub prompt** (All setups)
  This happens when the image was written in ISO mode instead of DD. Re-run the flash and pick 'Write in DD Image mode' at the prompt. If it happens twice, re-download the ISO and verify the checksum in case the file is corrupted.

- **The Ventoy drive is invisible to the boot menu or hangs on an old PC** (Ventoy, Older PC)
  This is where Ventoy lost me. My older Dell never got along with it. If your PC is old, do not fight this battle, switch to Rufus in MBR mode. That is the exact road I ended up taking.

- **Rufus does not list my USB drive** (Rufus)
  Try a different port first. If it is an unusual drive, open 'Show advanced drive properties' and enable 'List USB Hard Drives', but make sure you unplug any external hard drives you do not want accidentally wiped before you do. Once they appear in that list, one wrong click at START erases a real drive.

**You're done when:** Your tool reports success and your USB drive is ejected.

## Step 3: Prep the firmware

Three settings stand between you and a clean boot, and all of them live in the setup screen you never visit. The cheat sheet covers how to get in and where each one hides.

**Actions:**

1. Enter BIOS: Power-on your PC and tap the setup key repeatedly. On Dells F2 opens BIOS, and F12 opens the one-time boot menu.
2. Inside BIOS: Find the virtualization setting and turn it on. Look under menus named CPU, Advanced, or Security for variations of Intel Virtualization Technology, VT-x, VT-d, AMD-V, or SVM Mode.
3. **Newer PC:** Inside BIOS: Find Secure Boot and set it to Disabled (Boot or Security tab; some boards only unlock it after you set an admin password or switch the mode to Custom). Quick warning: Secure Boot protects against boot-level malware, and disabling it can make a BitLocker-encrypted Windows drive ask for its recovery key at the next startup. Get the key first: go to aka.ms/myrecoverykey, sign in with your Microsoft account, and write down the key listed for this PC (a photo works).
    **Older PC:** Older BIOS machines have no Secure Boot. Nothing to do here: tick this and move on.
4. Inside BIOS: To boot from the USB, change the Boot Order (also called Boot Sequence or Boot Priority) and move USB to the top of the list, above the internal disk.
5. Save and exit BIOS: press F10 on most machines, choose Yes to confirm, and the PC restarts with your changes.

**Firmware cheat sheet: why and how**

| Setting | How to do it | Why it matters |
|---|---|---|
| Enter BIOS setup from power-on | Immediately after powering on, tap the setup key repeatedly: F2 (Dell), Del (many desktops), F1, F10, or Esc. Missed it? Restart and tap earlier. | Firmware settings live underneath the operating system, so they can only be reached at power-on, before anything else loads. |
| Enter BIOS setup from Windows 10/11 (Newer PC) | Hold Shift and click Restart in the Start menu. On the blue screen pick Troubleshoot, then Advanced options, then UEFI Firmware Settings, then Restart. | No key-tap timing needed. The tile only exists on UEFI machines: legacy BIOS PCs show the same blue recovery menu, but without a firmware entry, so they must use the power-on key. |
| Enabling virtualization | Under CPU, Advanced, or Security. Look for Intel Virtualization Technology, VT-x, VT-d, AMD-V, or SVM Mode. Set it to Enabled. | Proxmox is a hypervisor, and hypervisors lean on this CPU feature to run VMs at full speed. Left off, VMs crawl or refuse to start. |
| Secure Boot (Newer PC) | Boot or Security tab, set it to Disabled. On some boards it only unlocks after you set an admin password or switch the mode to Custom. | A UEFI feature that only boots software signed by trusted vendors. Great on a work laptop, but it can block installers. Corporate machines usually turn it back on after imaging. |
| Boot order | Boot Order, Boot Sequence, or Boot Priority menu. Use the on-screen keys (often + and -, or F5 and F6) to move USB to the top. | The PC reads this list top to bottom at every power-on. USB above the internal disk means your installer wins the race. |
| The one-time boot menu | Note your brand's boot-menu key (Dell uses F12), restart, and tap it repeatedly until the menu opens. Pick the USB entry from the list. | A shortcut that boots one chosen device once, without changing the saved boot order in BIOS setup. |

**If something goes wrong:**

- **I cannot find the virtualization setting anywhere** (All setups)
  Look under CPU, Advanced, or Security tabs. Some boards only reveal it after a firmware update. Search your exact PC model plus 'enable virtualization' to get the precise menu path.

- **Secure Boot turned itself back on** (Newer PC)
  Some boards re-enable it when a firmware security check fails or after an update. Two fixes that work: update the BIOS firmware from the manufacturer's support page, or clear the CMOS (power off and unplug, then remove the coin battery for a minute or use the board's CMOS jumper). Recheck the setting afterward, and expect the date and time to need resetting after a CMOS clear.

**You're done when:** Virtualization is on, Secure Boot is out of the way, and the PC will look at USB first.

## Step 4: First boot: the black screen gauntlet

The step where old hardware fights back. The actions are the walkthrough; the cheat sheet explains why each move works, and the fixes below include the exact ones that saved this project.

**Actions:**

1. **Newer PC:** Plug the Proxmox USB into the PC.
    **Older PC:** Plug the Proxmox USB into a rear USB 2.0 port, not a front port and not a blue USB 3.0 one.
2. Power on and open the boot menu (F12 on Dells), or let your new boot order do the work.
3. **Newer PC:** Pick your USB drive from the list. UEFI machines may list it twice: try the entry that starts with UEFI first.
    **Older PC:** Pick your USB drive from the list.
4. At the Proxmox menu, choose 'Install Proxmox VE (Graphical)'.
5. Land on the installer's license screen. Take a breath. The hard part is over.

**First boot, explained**

| Item | What it is | Why it helps |
|---|---|---|
| Rear USB ports | The ports soldered directly to the motherboard, which makes them the most reliable ones for USB boot. | Old firmware predates USB 3.0 and may not see the drive. Rear 2.0 ports are compatible, sometimes only 1 specific port in the back works for booting USB. |
| Boot menu vs boot order | The boot menu (F12 on Dells) picks a device for this one boot only; boot order is the saved list used every time. | Either path works. The menu is faster and leaves no settings changed behind you. |
| The drive listed twice (Newer PC) | UEFI machines often show 'UEFI: YourDrive' and a plain 'YourDrive' entry. Same drive, two boot styles. | The UEFI entry matches the GPT drive you built, so that is the one to pick. |
| Graphical vs Terminal UI installer | Two faces of the same installer. One graphical, the other plain text. | Some video hardware freezes on the graphical mode, Terminal UI installs the identical system. |

**If something goes wrong:**

- **Black screen right after choosing Install** (Older PC)
  The fix that saved me: move the USB drive to a rear USB 2.0 port and try again. Old machines and USB 3.0 boot handoffs do not mix, and the port swap ended it in one try.

- **The graphical installer never appears, or the screen comes up garbled** (All setups)
  Reboot and pick the Terminal UI install option from the Proxmox menu instead. It is the same installer with a plainer face, and far pickier hardware still accepts it.

- **The USB drive does not load the boot menu at all** (All setups)
  Move the USB drive to a rear port (if it is back there already, try a different rear port), then recheck boot order and Secure Boot, and reflash the drive to rule out a bad write. As a last resort, reflash in ISO mode purely to test whether the machine can see the drive at all: DD is still the correct write mode for the real Proxmox install, so once the drive shows up, flash it in DD mode again before installing.

**You're done when:** The Proxmox installer's initial screen loaded!

## Step 5: Run the installer

Filling out boxes here. One of the boxes erases a disk! So make sure to read that one twice. Reference the cheat sheet below for deeper learning.

**Actions:**

1. Accept the license agreement.
2. Target Harddisk: choose the internal disk Proxmox will live on. Everything on that disk is erased.
3. Set your country, time zone, and keyboard layout.
4. Create the root password and enter a real email address. Make the password strong: you will type it a lot.
5. On the network page, set the hostname as an FQDN like pve.home.lan (the cheat sheet decodes those three parts), then confirm the IP address, gateway, and DNS the installer suggests. Write the IP down.
6. Click Install and let it run (this may take a while). When it's done it may ask to reboot (or reboot automatically). Reboot and immediately pull the USB drive out so the PC does not try to boot from it again.

**Installer choices, decoded**

| Item | What it is | Real world |
|---|---|---|
| License agreement (EULA) | The legal terms you accept to use the software: what you may do with it, and what the maker promises and does not. | Home users click through. Enterprises route these through legal and procurement before software is allowed in the building. |
| Target disk | The internal drive Proxmox installs onto. Everything on it is erased and replaced with the Proxmox server's own storage layout. | To avoid an irreversible mistake, like wiping the wrong disk, make sure to read this screen carefully and match the disk size before clicking anything. |
| FQDN (Fully Qualified Domain Name): pve.home.lan | lan is the top-level domain (TLD), home is the second-level domain (your network's domain), and pve is the hostname (this Proxmox PC's own name). Rename pve freely; keep a private ending. | Enterprises enforce naming conventions like site-role-number (nyc-hv-01) so a name alone says what and where a server is. Private networks use endings like .lan, .internal, or .home.arpa instead of public domains they do not own. |
| Static IP vs DHCP | DHCP hands out a dynamic IP, which can change over time. A static IP is fixed, which is better for servers because clients need to know exactly where to reach them. | Servers get static IP addresses (or DHCP reservations) in every serious network. This keeps the server reachable at one known address. |

**If something goes wrong:**

- **The installer cannot find my hard disk** (Older PC)
  Go back into firmware setup and switch the SATA mode to AHCI, then boot the installer again.

- **After the reboot, the PC boots back into the installer instead of Proxmox** (All setups)
  The boot process is still looking at the USB drive. Pull the drive when the installer asks for the reboot; if it already looped, remove it and restart. If you set USB first in the boot order earlier, you can now move the internal disk back to the top.

**You're done when:** The PC reboots into Proxmox on its own, no USB attached, and shows a login banner with an address ending in :8006.

## Step 6: First login, from another device

Proxmox has no desktop. You run it from a browser on your normal computer, and this is the moment it starts feeling like a real server.

**Actions:**

1. On your everyday computer, make sure you are on the same network as the server. Guest Wi-Fi does not count, and a VPN on this device can get in the way too: both are covered under issues.
2. Browse to https://YOUR-SERVER-IP:8006. The https matters, and so does the :8006.
3. Click through the browser's certificate warning (Advanced, then Proceed). It is expected: the server signs its own certificate and your browser has never met it before. The cheat sheet has the full story.
4. Log in as root with your password. Leave the realm set to PAM.
5. Meet the 'No valid subscription' popup and click OK. It is a reminder, not an error. The free tier is fully functional.

**First login, explained**

| Item | What it means | Real world |
|---|---|---|
| The certificate warning | Proxmox signs its own certificate, so your browser meets a stranger vouching for itself and objects on principle. On your own network, reaching your own server, proceeding is fine. | Enterprises run an internal certificate authority (the AD CS role in Windows shops) so every internal service gets a trusted certificate and employees never see this warning. |
| https and :8006 | The s means the connection is encrypted. :8006 is the numbered door, the port, that Proxmox answers on. Both are required parts of the address. | Every network service listens on a port, and knowing the number is half of reaching anything: 443 for the web, 22 for SSH, 8006 for Proxmox. |
| The PAM realm | PAM is Linux's built-in local login system, and your root account lives there, so the realm box stays on PAM tonight. | Proxmox can also plug into central logins later (LDAP or Active Directory), which is how companies avoid managing accounts one server at a time. |
| 'No valid subscription' | A reminder that this install has no paid support subscription attached. It is not an error, and nothing is locked. | The popup exists because Proxmox sells enterprise support contracts. The software itself stays fully functional without one. |

**If something goes wrong:**

- **The page will not load at all** (All setups)
  This one got me. My laptop was on the guest network, and guest isolation quietly blocks devices from seeing each other, so the server might as well not exist. Join the main network and the page appears. Also confirm you typed https and :8006, and ping the server's IP if you can.

- **Everything looks right, but this device runs a VPN** (All setups)
  A VPN tunnels your traffic out to another network, so as far as your LAN is concerned, your laptop is no longer sitting next to the server. Pause the VPN, or exclude local addresses if it supports split tunneling, reload the page, and reconnect the VPN afterward.

- **Connection refused, or the address seems wrong** (All setups)
  Read the IP straight off the server's own console banner. DHCP may have handed out something different from what you wrote down during the install.

**You're done when:** The Proxmox dashboard is on your screen.

## Step 7: Free updates and sensible defaults

Out of the box, Proxmox points at the paid enterprise update channel. Two clicks aim it at the free one, and the cheat sheet explains what those channels and ports actually are.

**Actions:**

1. In the web UI, select your node in the left tree, then open Updates, then Repositories.
2. Disable the enterprise repository entries.
3. Click Add, choose the No-Subscription repository, and confirm.
4. Go back to Updates, click Refresh, then Upgrade, and let it finish.
5. Two habits while it runs: never expose port 8006 to the internet, and store the server's IP and root password somewhere safe.

**Update channels and ports, decoded**

| Item | What it is | Why it matters here |
|---|---|---|
| Enterprise repository | The paid update channel: the same software after extra staging and testing, tied to a support subscription and its access key. | Without a subscription key it answers 401 Unauthorized, which is exactly why a fresh free install fails to update until you switch channels. |
| No-Subscription repository | The free public channel. Same Proxmox, with updates arriving a little sooner and less enterprise soak time. | The intended channel for home labs and small setups. Production shops pay for the enterprise channel mostly for the extra testing and the support contract. |
| 'Exposing a port' | Port forwarding: opening one numbered door on your router so the internet can reach a device inside. Necessary for things meant to be public, like a self-hosted website or a game server. | Admin panels are never meant to be public. Bots scan the whole internet for doors like 8006 around the clock, so admins reach their servers from outside through a VPN instead of opening the door. |

**If something goes wrong:**

- **Refresh or apt fails with a 401 Unauthorized error** (All setups)
  An enterprise repository is still enabled. Disable it under Repositories and refresh again. This is the single most common first-day error in Proxmox.

**You're done when:** Refresh runs without a 401 error and the upgrade completes. Your server is alive, current, and ready for its first VM.

## The finish line

Your server is running. The next project writes itself: your first VM.
