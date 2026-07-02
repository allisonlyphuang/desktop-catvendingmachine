import tkinter as tk
from PIL import Image, ImageTk
import random
import os
import sys

def get_asset_path(relative_path):
    if getattr(sys, 'frozen', False):
        # look in the folder where the compiled .exe lives
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

class DesktopVendingPet:
    def __init__(self, root): # anything that defines the vending machine and what it looks like/does/intial states
        self.is_shaking = False

        self.cat_window = None
        
        #self.rooot stores main window object so we can modify it
        self.root = root 

        # 1. strip window borders and title bar
        self.root.overrideredirect(True)

        # keep above all other software
        self.root.attributes("-topmost", True)

        # detect user's monitor resolution
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        # find coordinates for bottom right corner
        self.base_x = screen_w - 120 - 30
        self.base_y = screen_h - 180 - 60 

        # apply size and position to the window
        self.root.geometry(f"120x180+{self.base_x}+{self.base_y}")

        # define chroma key
        self.transparent_color = "#abcdef"
        self.root.attributes("-transparentcolor", self.transparent_color)

        # create a canvas widget to hold graphics
        self.canvas = tk.Canvas( # a widget used for drawing shapes + handling pixels
            self.root,
            width=120,
            height=180,
            bg=self.transparent_color,
            highlightthickness=0 # remove default canvas border 
        )

        # load and display vending machine
        try:
            vending_img = Image.open(get_asset_path("vendingMachine.png"))
            vending_img = vending_img.resize((120, 180), Image.Resampling.LANCZOS)

            # keep a reference so garbage collection doesn't delete it
            self.vending_photo = ImageTk.PhotoImage(vending_img)

            # draw image starting at top left of canvas 0,0
            self.canvas.create_image(0, 0, anchor="nw", image=self.vending_photo)
        except Exception:
            self.canvas.create_rectangle(10, 10, 110, 170, fill="#ff4d4f", outline="")

        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.trigger_dispense)

        # self.root.bind(event, action) connects a user interaction to a specific code instruction 
        # <Button-3> = right click 
        self.root.bind("<Button-3>", lambda event: sys.exit())


    def trigger_dispense(self, event):
        self.dismiss_cat()
        # if already shaking, stop 
        if self.is_shaking:
            return 

        # lock machine so click spamming does nothign
        self.is_shaking = True

        # define offsets
        # 3. Define rapid programmatic pixel offset configurations
        shake_offsets = [(-8, 2), (8, -2), (-5, 4), (5, -3), (-2, 2), (2, -1), (0, 0)]
        delay_step_ms = 45
        
        for index, (offset_x, offset_y) in enumerate(shake_offsets):
            next_x = self.base_x + offset_x
            next_y = self.base_y + offset_y
            
            # use formula to schedule each frame in the future
            self.root.after(
                index * delay_step_ms, 
                lambda x=next_x, y=next_y: self.root.geometry(f"120x180+{x}+{y}")
            )

        self.root.after(315, self.spawn_cat_picture)

    def spawn_cat_picture(self):
        self.is_shaking = False
        cat_x = self.base_x - 190
        cat_y = self.base_y + 30
        
        self.cat_window = tk.Toplevel(self.root)
        self.cat_window.overrideredirect(True)
        self.cat_window.attributes("-topmost", True)
        self.cat_window.geometry(f"200x150+{cat_x}+{cat_y}")
        
        library_dir = get_asset_path("cat_library")
        try:
            if os.path.exists(library_dir) and len(os.listdir(library_dir)) != 0:
                # pick random cat
                valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
                
                filenames = [f for f in os.listdir(library_dir) if f.lower().endswith(valid_extensions)]

                random_filename = random.choice(os.listdir(library_dir))
                full_path = os.path.join(library_dir, random_filename)
                
                if len(filenames) != 0:
                    random_filename = random.choice(filenames)
                    full_path = os.path.join(library_dir, random_filename)
                    
                    img = Image.open(full_path)
                    img = img.resize((200, 150), Image.Resampling.LANCZOS)
                    
                    self.cat_photo = ImageTk.PhotoImage(img)
                    cat_label = tk.Label(self.cat_window, image=self.cat_photo, bd=0)
                else:
                    raise FileNotFoundError
            else:
                raise FileNotFoundError
                
        except Exception:
            # Fallback UI if the folder is missing or an image is corrupted
            cat_label = tk.Label(
                self.cat_window, text="\ndispensed ⭐", font=("Arial", 14, "bold"),
                bg="#fff0f6", fg="#c41d7f", width=200, height=150, relief="solid", bd=2
            )
            
        cat_label.pack()

        cat_label.bind("<Button-1>", lambda event: self.dismiss_cat())
        self.timer_id = self.root.after(5000, self.dismiss_cat)
    
    def dismiss_cat(self):
        # cancel the timer
        if hasattr(self, 'timer_id') and self.timer_id is not None:
            try:
                self.root.after_cancel(self.timer_id)
            except Exception:
                pass # ignore if the timer already completed naturally
            self.timer_id = None

        # check the window
        if self.cat_window is not None:
            try:
                self.cat_window.destroy()
            except Exception:
                pass
            self.cat_window = None 

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopVendingPet(root)
    root.mainloop()



