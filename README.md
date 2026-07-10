# Proxmox-old-pc
Interactive walkthrough app: Install Proxmox on an old PC, one step at a time. Runs offline, docs generated from the app's own data (single source of truth).


<!-- Repo README for Proxmox-old-pc.
     The GIF line stays commented out until you record it (ScreenToGif,
     about ten seconds of ticking through a step), then uncomment. -->

<!-- ![Demo](demo.gif) -->

# Install Proxmox on an Old PC: One Step at a Time

**[Try it live]([GitHub Pages link])** &middot; [Take the full guide as one file](docs/full-walkthrough.md)

An interactive walkthrough that takes a beginner from a forgotten desktop to a running Proxmox server. Tick the actions, complete the step, watch the map turn green. Hands-on mode gates each step behind its checklist; Just Browsing lets you read the whole journey in two minutes. One HTML file, runs offline with a double-click, no installs.

Everything in it comes from my own install on a Dell Inspiron 620: every fix in the troubleshooting panels is a problem I actually hit, next to what actually solved it.

## What broke and how I fixed it

- My 64 GB USB drive flashed perfectly and still would not boot the old Dell. Old firmware chokes on large drives; a smaller drive ended it.
- The USB drive would not boot from a front port. Old machines and USB 3.0 boot handoffs do not mix; moving it to a rear USB 2.0 port fixed it in one try.
- Secure Boot turned itself back on after I disabled it. Some boards re-enable it when a firmware check fails; a BIOS update or CMOS clear settles it.

The full list, with fixes, lives in the app's Issues panels and in [docs/troubleshooting-and-lessons.md](docs/troubleshooting-and-lessons.md).

## How this repo works

- **index.html** is the entire app, engine and content in one file. The project data sits between two markers inside it and is the single source of truth.
- **docs/** is generated, never hand-edited: [full-walkthrough.md](docs/full-walkthrough.md) is the complete guide in one printable file, [troubleshooting-and-lessons.md](docs/troubleshooting-and-lessons.md) is the fixes summary.
- **tools/** holds the Python scripts that build the docs from the app's data. After any data change: `python3 tools/generate_docs.py` and `python3 tools/generate_full_guide.py` (on Windows, `python` and backslashes).

Want to build one of these for your own project? The companion app teaches it from zero: **[Build Your Own Walkthrough App]([course Pages link])**.
