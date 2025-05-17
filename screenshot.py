import tkinter as tk
from PIL import ImageGrab, Image
import ctypes

# Enable DPI awareness for accurate screen coordinates on high-DPI displays
ctypes.windll.user32.SetProcessDPIAware()

start_x = start_y = end_x = end_y = 0
rect_id = None

def on_mouse_down(event):
    global start_x, start_y
    start_x, start_y = event.x_root, event.y_root
    # Start rectangle
    global rect_id
    rect_id = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red', width=2)

def on_mouse_drag(event):
    global rect_id
    # Update rectangle as user drags
    canvas.coords(rect_id, start_x, start_y, event.x_root, event.y_root)

def on_mouse_up(event):
    global end_x, end_y
    end_x, end_y = event.x_root, event.y_root
    root.quit()

import tkinter as tk
from PIL import ImageGrab

def capture_region():
    """
    Open a fullscreen transparent window to let the user drag-select a screen region.
    Returns a PIL Image of the selected region or None if cancelled.
    """
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.3)  # semi-transparent
    root.config(cursor="cross")
    root.lift()
    root.attributes("-topmost", True)

    start_x = start_y = cur_x = cur_y = 0
    rect = None
    coords = {}

    canvas = tk.Canvas(root, cursor="cross", bg="grey")
    canvas.pack(fill=tk.BOTH, expand=True)

    def on_button_press(event):
        nonlocal start_x, start_y, rect
        start_x, start_y = event.x, event.y
        if rect:
            canvas.delete(rect)
            rect = None

    def on_move_press(event):
        nonlocal rect, cur_x, cur_y
        cur_x, cur_y = event.x, event.y
        if rect:
            canvas.delete(rect)
        rect = canvas.create_rectangle(start_x, start_y, cur_x, cur_y, outline='red', width=2)

    def on_button_release(event):
        nonlocal coords
        coords['x1'] = min(start_x, event.x)
        coords['y1'] = min(start_y, event.y)
        coords['x2'] = max(start_x, event.x)
        coords['y2'] = max(start_y, event.y)
        root.quit()

    # Bind mouse events
    canvas.bind("<ButtonPress-1>", on_button_press)
    canvas.bind("<B1-Motion>", on_move_press)
    canvas.bind("<ButtonRelease-1>", on_button_release)

    # Run the selection loop
    root.mainloop()
    root.destroy()

    if 'x1' in coords:
        # Capture selected region from the screen
        img = ImageGrab.grab(bbox=(coords['x1'], coords['y1'], coords['x2'], coords['y2']))
        return img
    else:
        return None


if __name__ == "__main__":
    capture_region()
