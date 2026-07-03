# desktop-catvendingmachine
A desktop pet style vending machine loaded with cats instead of snacks.

Crammed as a last-minute birthday gift for a friend, because I'm such a good person. So, keep this on your desktop for a quick dopamine hit during your long coding sessions (because we're all working so hard on Stardance) or as a gift for your cat-appreciating friend.

<img width="579" height="331" alt="catvending_demo" src="https://github.com/user-attachments/assets/5bb65166-dca8-48dc-b2de-04166c70658e" />


# ⭐ Quick Start
Have python? Copy, paste, and run:

```
pip install Pillow
python catvending.py
```

Make sure the terminal is open inside the project folder where vendingMachine.png and cat_library live.

# 🔎 Features
- **Semi-realistic dispense animation:** left-clicking the machine triggers a vending-machine style shake before dispensing out a cat.
- **Customization:** pulls randomized images from the local cat_library folder: feel free to add more cats or replace with other images.
- **Auto-dismiss timer:** Stays pinned above your IDE, browser, or games so the desktop companion is always visible.
- Uses custom canvas background stripping to look like a floating vending machine instead of an app window.

# 💻 How to Run it Locally
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

# 🎮 Controls
- Left click machine to dispense a new cat
- Left click cat to dismiss the cat
- Right click machine to kill the application

# ⚙️ How it works
**State-locked debouncing**
- To protect the rendering loop from input spamming the machine, the code uses a boolean flag (self.is_shaking) to check whether or not an animation is ongoing. When a dispense sequence runs, any interrupting inputs are intercepted and dropped, preventing overlapping animations and spam.

**Window lifecycles**
- Instead of hiding a pre-loaded window, the app instantiates a tk.Toplevel frame. This window's lifecycle is managed via the event loop using .after(). When the vending machine is dismissed, the app cancels pending timers and calls .destroy(), freeing memory.

**Error and bug catching**
- The asset loader scans the directory and filters filenames against an extension list. If the folder is empty or missing, a try-except block catches the error and falls back to a pre-set image and text so the app doesn't crash, and the user can be informed of the error.
