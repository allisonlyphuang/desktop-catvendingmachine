# desktop-catvendingmachine
A desktop pet style vending machine loaded with cats instead of snacks.

Crammed as a last-minute birthday gift for a friend, because I'm such a good person.

<img width="579" height="331" alt="catvending_demo" src="https://github.com/user-attachments/assets/5bb65166-dca8-48dc-b2de-04166c70658e" />


# Quick Start
Have python and want to run it now? Copy, paste, and run:

```
pip install Pillow
python catvending.py
```

Make sure the terminal is open inside the project folder where vendingMachine.png and cat_library live.

# Features
- Interactive dispense animation: left-clicking the machine triggers a vending-machine style shake before dispensing out a cat.
- Customization: pulls randomized images from the local cat_library folder: feel free to add more cats or replace with other images.
- Auto-dismiss timer: Stays pinned above your IDE, browser, or games so the desktop companion is always visible.
- Uses custom canvas backgruond stripping to look like a floating asset rather than an app window.

# How to Run it Locally
## Prerequisites
- Python 3.8 or higher
- Dependencies: Pillow for advanced image resizing and rendering
## Local setup
1. Clone this repo or download source files
2. Ensure directory structure matches the following:
```
├── catvending.py
├── vendingMachine.png
└── cat_library/
    ├── cat1.jpg
    └── cat2.png
```
3. Run the command:
```
python catvending.py
```

# Controls
- Left click machine to dispense a new cat
- Left click cat to dismiss the cat
- Right click machine to kill the application

# How it works
**State-locked debouncing**
- To protect the rendering loop from input spamming the machine, the handler uses a boolean flag (self.is_shaking) as a lock. When a dispense sequence runs, subsequent inputs are intercepted and dropped, preventing overlapping animations.

**Window lifecycles**
- Instead of hiding a pre-loaded window, the app instantiates a tk.Toplevel frame. This window's lifecycle is managed via the event loop using .after() callbacks. When dismissed, the app cancels pending timers and calls .destroy(), freeing memory to avoid resource leaks.

**Error and bug catching**
- The asset loader scans the directory and filters filenames against an extension list. If the folder is empty or missing, a try-except blcok catche sthe error and falls back to a default text UI so the app doesn't crash.
