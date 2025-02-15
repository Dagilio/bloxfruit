import customtkinter as ctk
import time
import threading
from plyer import notification
from PIL import Image
import os

# ------------------------
#      GLOBAL VARIABLES
# ------------------------

timer_running = False  # Tracks if the AFK timer is running
side_data = {}         # Stores data for each side
square_images = {}     # Cache for fruit images
trade_validity_label = None  # Label for trade validity

# ------------------------
#   FRUIT ITEM VALUES
# ------------------------
ITEM_VALUES = {
    # Commons: Rocket to Spike
    "Rocket":   {"game_price": 5000,     "market_value": 5000},
    "Spin":     {"game_price": 7500,     "market_value": 7500},
    "Blade":    {"game_price": 30000,    "market_value": 50000},
    "Spring":   {"game_price": 60000,    "market_value": 60000},
    "Bomb":     {"game_price": 80000,    "market_value": 80000},
    "Smoke":    {"game_price": 100000,   "market_value": 100000},
    "Spike":    {"game_price": 180000,   "market_value": 180000},

    # Uncommons: Flame to Diamond
    "Flame":    {"game_price": 250000,   "market_value": 250000},
    "Falcon":   {"game_price": 300000,   "market_value": 300000},
    "Ice":      {"game_price": 350000,   "market_value": 550000},
    "Sand":     {"game_price": 420000,   "market_value": 420000},
    "Dark":     {"game_price": 500000,   "market_value": 400000},
    "Diamond":  {"game_price": 600000,   "market_value": 1500000},

    # Rares: Light to Magma
    "Light":    {"game_price": 650000,   "market_value": 800000},
    "Rubber":   {"game_price": 750000,   "market_value": 700000},
    "Barrier":  {"game_price": 800000,   "market_value": 800000},
    "Ghost":    {"game_price": 800000,   "market_value": 800000},
    "Magma":    {"game_price": 1150000,  "market_value": 1150000},

    # Legendary: Quake to Rumble
    "Quake":    {"game_price": 1000000,  "market_value": 1000000},
    "Buddha":   {"game_price": 1200000,  "market_value": 10000000},
    "Love":     {"game_price": 1300000,  "market_value": 1150000},
    "Spider":   {"game_price": 1500000,  "market_value": 1150000},
    "Sound":    {"game_price": 1700000,  "market_value": 2500000},
    "Phoenix":  {"game_price": 1800000,  "market_value": 2250000},
    "Portal":   {"game_price": 1900000,  "market_value": 10000000},
    "Rumble":   {"game_price": 2100000,  "market_value": 7000000},

    # Mythical: Pain to West Dragon
    "Pain":     {"game_price": 2300000,  "market_value": 2000000},
    "Blizzard": {"game_price": 2400000,  "market_value": 5000000},
    "Gravity":  {"game_price": 2500000,  "market_value": 2000000},
    "Mammoth":  {"game_price": 2700000,  "market_value": 8000000},
    "T-Rex":    {"game_price": 2700000,  "market_value": 20000000},
    "Dough":    {"game_price": 2800000,  "market_value": 30000000},
    "Shadow":   {"game_price": 2900000,  "market_value": 6000000},
    "Venom":    {"game_price": 3000000,  "market_value": 9000000},
    "Control":  {"game_price": 3200000,  "market_value": 20000000},
    "Gas":      {"game_price": 3200000,  "market_value": 80000000},
    "Spirit":   {"game_price": 3400000,  "market_value": 9000000},
    "Leopard":  {"game_price": 5000000,  "market_value": 50000000},
    "Yeti":     {"game_price": 5000000,  "market_value": 115000000},
    "Kitsune":  {"game_price": 8000000,  "market_value": 165000000},
    "East Dragon": {"game_price": 15000000, "market_value": 545000000},
    "West Dragon": {"game_price": 15000000, "market_value": 565000000},

    # Gamepasses: Permanent Rocket to Fruit Notifier
    "Permanent Rocket": {"game_price":0, "robux": 50,  "market_value": 5000000},
    "Permanent Spin": {"game_price":0, "robux": 75,  "market_value": 7500000},
    "Permanent Blade": {"game_price":0, "robux": 100, "market_value": 10000000},
    "Permanent Spring": {"game_price":0, "robux": 180, "market_value": 15000000},
    "Permanent Bomb": {"game_price":0, "robux": 220, "market_value": 20000000},
    "Permanent Smoke": {"game_price":0, "robux": 250, "market_value": 25000000},
    "Permanent Spike": {"game_price":0, "robux": 380, "market_value": 30000000},
    "Permanent Flame": {"game_price":0, "robux": 550, "market_value": 40000000},
    "Permanent Falcon": {"game_price":0, "robux": 650, "market_value": 65000000},
    "Permanent Ice": {"game_price":0, "robux": 750, "market_value": 150000000},
    "Permanent Sand": {"game_price":0, "robux": 850, "market_value": 100000000},
    "Permanent Dark": {"game_price":0, "robux": 950, "market_value": 160000000},
    "Permanent Diamond": {"game_price":0, "robux": 1000, "market_value": 130000000},
    "Permanent Light": {"game_price":0,"robux": 1100, "market_value": 190000000},
    "Permanent Rubber": {"game_price":0, "robux": 1200, "market_value": 205000000},
    "Permanent Barrier": {"game_price":0, "robux": 1250, "market_value": 190000000},
    "Permanent Ghost": {"game_price":0,"robux": 1275, "market_value": 195000000},
    "Permanent Magma": {"game_price":0,"robux": 1300, "market_value": 235000000},
    "Permanent Quake": {"game_price":0, "robux": 1500, "market_value": 270000000},
    "Permanent Buddha": {"game_price":0,"robux": 1650, "market_value": 380000000},
    "Permanent Love": {"game_price":0, "robux": 1700, "market_value": 305000000},
    "Permanent Spider": {"game_price":0, "robux": 1800, "market_value": 325000000},
    "Permanent Sound": {"game_price":0, "robux": 1900, "market_value": 340000000},
    "Permanent Phoenix": {"game_price":0, "robux": 2000, "market_value": 360000000},
    "Permanent Portal": {"game_price":0, "robux": 2000, "market_value": 400000000},
    "Permanent Rumble": {"game_price":0, "robux": 2100, "market_value": 375000000},
    "Permanent Pain": {"game_price":0,"robux": 2200, "market_value": 395000000},
    "Permanent Blizzard": {"game_price":0, "robux": 2250, "market_value": 405000000},
    "Permanent Gravity": {"game_price":0, "robux": 2300, "market_value": 415000000},
    "Permanent Mammoth": {"game_price":0, "robux": 2350, "market_value": 375000000},
    "Permanent T-Rex": {"game_price":0, "robux":2350, "market_value": 425000000},
    "Permanent Dough": {"game_price":0, "robux":2400, "market_value": 450000000},
    "Permanent Shadow": {"game_price":0, "robux":2425, "market_value": 435000000},
    "Permanent Venom": {"game_price":0, "robux":2450, "market_value": 440000000},
    "Permanent Control": {"game_price":0, "robux":2500, "market_value": 575000000},
    "Permanent Gas": {"game_price":0, "robux":2500, "market_value": 415000000},
    "Permanent Spirit": {"game_price":0, "robux":2550, "market_value": 460000000},
    "Permanent Leopard": {"game_price":0, "robux":3000, "market_value":525000000},
    "Permanent Yeti": {"game_price":0, "robux":3000, "market_value":510000000},
    "Permanent Kitsune": {"game_price":0, "robux":4000, "market_value":720000000},
    "Permanent East Dragon": {"game_price":0, "robux":2500, "market_value":1350000000},
    "Permanent West Dragon": {"game_price":0, "robux":2500, "market_value":1350000000},

    # Additional Gamepasses
    "Fast Boats": {"game_price":0, "robux": 350, "market_value": 45000000},
    "2x Boss Drop": {"game_price":0, "robux": 350, "market_value": 55000000},
    "2x Money": {"game_price":0, "robux": 450, "market_value": 75000000},
    "2x Mastery": {"game_price":0, "robux": 450, "market_value": 55000000},
    "Fruit Storage": {"game_price":0, "robux":400, "market_value":75000000},
    "Dark Blade": {"game_price":0, "robux":1200, "market_value":200000000},
    "Fruit Notifier": {"game_price":0, "robux":2700, "market_value":500000000},
}

# -------------------------
#   RARITY DEFINITIONS
# -------------------------
RARITY_COLORS = {
    "Common":    "#FFFFE4",   # Light Yellow
    "Uncommon":  "#7FFFD4",   # Aquamarine
    "Rare":      "#4169E1",   # Royal Blue
    "Legendary": "#8F00FF",   # Violet
    "Mythical":  "#FF000D",   # Red
    "Gamepass":  "#FFD700",   # Gold
    "Permanent": "#FF8C00",   # Dark Orange for Permanent Gamepasses
}

def get_rarity(item):
    """Determine the rarity of the item based on its name and properties."""
    if "robux" in ITEM_VALUES[item]:
        if "Permanent" in item:
            return "Permanent"
        return "Gamepass"
    elif item in ["Rocket", "Spin", "Blade", "Spring", "Bomb", "Smoke", "Spike"]:
        return "Common"
    elif item in ["Flame", "Falcon", "Ice", "Sand", "Dark", "Diamond"]:
        return "Uncommon"
    elif item in ["Light", "Rubber", "Barrier", "Ghost", "Magma"]:
        return "Rare"
    elif item in ["Quake", "Rumble", "Buddha", "Love", "Spider", "Sound", "Phoenix", "Portal"]:
        return "Legendary"
    elif item in ["Pain", "Blizzard", "Gravity", "Mammoth", "T-Rex", "Dough", "Shadow", "Venom", "Control", "Gas", "Spirit", "Leopard", "Yeti", "Kitsune", "East Dragon", "West Dragon"]:
        return "Mythical"
    else:
        return "Common"  # Default rarity

# -------------------------
#   IMAGE LOADING LOGIC
# -------------------------
def load_square_images():
    add_path = os.path.join("imgs", "add.png")
    try:
        aimg = Image.open(add_path).resize((32, 32))
        square_images["add"] = ctk.CTkImage(dark_image=aimg, size=(32, 32))
    except Exception as e:
        print(f"Error loading add.png: {e}")
        square_images["add"] = None

    for fruit in ITEM_VALUES:
        path = os.path.join("imgs", fruit.lower().replace(" ", "_") + ".png")
        try:
            fimg = Image.open(path).resize((64, 64))
            square_images[fruit] = ctk.CTkImage(dark_image=fimg, size=(64, 64))
        except Exception as e:
            print(f"Error loading {fruit.lower().replace(' ', '_')}.png: {e}")
            square_images[fruit] = square_images["add"]  # Fallback to add icon

# ------------------------
#   AFK TIMER FUNCTIONS
# ------------------------
def start_afk_timer():
    global timer_running
    t = 19 * 60  # 19 minutes
    timer_running = True
    while t > 0 and timer_running:
        m, s = divmod(t, 60)
        time_left.set(f"{m:02}:{s:02}")
        time.sleep(1)
        t -= 1
    if timer_running:
        notification.notify(title='AFK Reminder',
                            message='Please move in Blox Fruits!',
                            timeout=10)
        timer_running = False

def start_afk():
    global timer_running
    if not timer_running:
        threading.Thread(target=start_afk_timer, daemon=True).start()
    else:
        print("AFK timer is already running.")

# ------------------------
#   FRUIT CALCULATOR
# ------------------------
def show_fruit_calculator():
    clear_main_frame()
    ctk.CTkLabel(main_frame, text="Blox Fruits Trade Calculator",
                font=('Helvetica', 24), text_color="#ffffff").pack(pady=10)

    # Trade Validity Check Label
    global trade_validity_label
    trade_validity_label = ctk.CTkLabel(main_frame, text="Trade Validity: N/A",
                                       font=('Helvetica', 14), text_color="#ffffff")
    trade_validity_label.pack(pady=(0, 20))

    trade_frame = ctk.CTkFrame(main_frame, fg_color="#3c3c3c", corner_radius=10)
    trade_frame.pack(pady=10, padx=20, fill="both", expand=True)
    trade_frame.grid_rowconfigure(0, weight=1)
    trade_frame.grid_columnconfigure(0, weight=1)
    trade_frame.grid_columnconfigure(1, weight=1)
    create_side(trade_frame, "You")
    create_side(trade_frame, "Them")

def create_side(parent, side):
    sf = ctk.CTkFrame(parent, fg_color="#4a4a4a", corner_radius=8)
    sf.grid(row=0, column=0 if side == "You" else 1, padx=10, pady=10, sticky="nsew")
    ctk.CTkLabel(sf, text=side, font=('Helvetica', 18), text_color="#ffffff").pack(pady=10)
    
    items_frame = ctk.CTkFrame(sf, fg_color="#4a4a4a")
    items_frame.pack()
    for i in range(2):
        items_frame.grid_rowconfigure(i, weight=1)
        items_frame.grid_columnconfigure(i, weight=1)
    
    items = [None] * 4
    squares = []
    for idx in range(4):
        r, c = divmod(idx, 2)
        btn = ctk.CTkButton(items_frame, text="", image=square_images["add"],
                           fg_color="#6a4c9c", hover_color="#7f5bad",
                           width=120, height=80,
                           command=lambda i=idx: handle_square_click(side, i))
        btn.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        squares.append(btn)
    
    gl = ctk.CTkLabel(sf, text="Total Game Price: $0",
                      font=('Helvetica Rounded', 16, 'bold'), text_color="#FFFFE4")
    gl.pack(pady=(10, 5))
    ml = ctk.CTkLabel(sf, text="Total Market Value: $0",
                      font=('Helvetica Rounded', 16, 'bold'), text_color="#90EE90")
    ml.pack(pady=(0, 10))
    so = create_search_overlay(sf, side)
    so.place_forget()
    
    side_data[side] = {
        "items": items,
        "squares": squares,
        "total_game_label": gl,
        "total_market_label": ml,
        "search_overlay": so,
        "active_idx": None
    }

def create_search_overlay(parent, side):
    ov = ctk.CTkFrame(parent, fg_color="#3c3c3c")
    ov.place(x=0, y=0, relwidth=1, relheight=1)
    ov.place_forget()
    
    var = ctk.StringVar()
    se = ctk.CTkEntry(ov, textvariable=var, placeholder_text="Search fruit...", width=320)
    se.pack(pady=10)
    
    sf = ctk.CTkScrollableFrame(ov, fg_color="#3c3c3c")
    sf.pack(fill="both", expand=True, padx=10, pady=10)
    
    frs = {}
    for frt, p in ITEM_VALUES.items():
        ctk_img = square_images.get(frt, square_images["add"])
        ff = ctk.CTkFrame(sf, fg_color="#615675", corner_radius=6)
        ff.pack(fill="x", pady=5, padx=5)
        ff.grid_columnconfigure(0, weight=0)
        ff.grid_columnconfigure(1, weight=1)
        
        il = ctk.CTkLabel(ff, text="", image=ctk_img)
        il.grid(row=0, column=0, rowspan=4 if "robux" in p else 3, padx=5, pady=5, sticky="n")
        
        # Determine rarity and set color
        rarity = get_rarity(frt)
        name_color = RARITY_COLORS.get(rarity, "#ff8080")
        
        # Name Label
        nl = ctk.CTkLabel(ff, text=frt, font=("Helvetica", 14, "bold"), text_color=name_color)
        nl.grid(row=0, column=1, sticky="w")
        
        # Market Value Label
        mt = ctk.CTkLabel(ff, text="Market value:", font=("Helvetica", 12, "bold"), text_color="#ffffff")
        mt.grid(row=1, column=1, sticky="w")
        
        # Market Value Amount
        ml = ctk.CTkLabel(ff, text=f"${p['market_value']:,}", font=("Helvetica", 12), text_color="#90EE90")
        ml.grid(row=2, column=1, sticky="w")
        
        # If gamepass, add Robux label
        if "robux" in p:
            robux_amount = f"R{p['robux']:,}"
            robux_color = RARITY_COLORS["Permanent"] if "Permanent" in frt else RARITY_COLORS["Gamepass"]
            robux_label = ctk.CTkLabel(ff, text=f"Robux: {robux_amount}",
                                       font=("Helvetica", 12), text_color=robux_color)
            robux_label.grid(row=3, column=1, sticky="w")
        
        # Bind Click Event
        ff.bind("<Button-1>", lambda e, fr=frt: select_fruit(side, fr))
        for child in ff.winfo_children():
            child.bind("<Button-1>", lambda e, fr=frt: select_fruit(side, fr))
        
        frs[frt] = ff
    
    def update_fruit_display(filter_text=""):
        """Show/hide frames that don't match the search filter, maintaining original order."""
        f_lower = filter_text.lower()
        for fr in frs.values():
            fr.pack_forget()
        for fruit in ITEM_VALUES:
            if f_lower in fruit.lower():
                frs[fruit].pack(fill="x", pady=5, padx=5)
    
    def on_search(*_):
        update_fruit_display(var.get())
        # Force scroll to the top
        sf._parent_canvas.yview_moveto(0)
    
    var.trace_add("write", on_search)
    update_fruit_display()
    
    return ov

def handle_square_click(side, idx):
    d = side_data[side]
    current_item = d["items"][idx]
    if current_item:
        d["items"][idx] = None
        d["squares"][idx].configure(image=square_images["add"])
        recalc_total(side)
    else:
        if d["active_idx"] is not None:
            d["search_overlay"].place_forget()
        d["active_idx"] = idx
        d["search_overlay"].place(x=0, y=0, relwidth=1, relheight=1)

def select_fruit(side, fruit):
    d = side_data[side]
    idx = d["active_idx"]
    if idx is not None:
        d["items"][idx] = fruit
        d["squares"][idx].configure(image=square_images.get(fruit, square_images["add"]))
        recalc_total(side)
        d["search_overlay"].place_forget()
        d["active_idx"] = None

def recalc_total(side):
    d = side_data[side]
    total_game = sum(ITEM_VALUES[x]['game_price'] for x in d["items"] if x)
    total_market = sum(ITEM_VALUES[x]['market_value'] for x in d["items"] if x)
    d["total_game_label"].configure(text=f"Total Game Price: ${total_game:,.0f}")
    d["total_market_label"].configure(text=f"Total Market Value: ${total_market:,.0f}")
    update_trade_validity()

def update_trade_validity():
    """Update the trade validity label based on 'You' and 'Them' total game prices."""
    you_items = side_data["You"]["items"]
    them_items = side_data["Them"]["items"]
    your_total = sum(ITEM_VALUES[x]['game_price'] for x in you_items if x)
    their_total = sum(ITEM_VALUES[x]['game_price'] for x in them_items if x)

    # Check if either side has at least one gamepass
    you_has_gamepass = any("robux" in ITEM_VALUES[item] for item in you_items if item)
    them_has_gamepass = any("robux" in ITEM_VALUES[item] for item in them_items if item)

    if you_has_gamepass or them_has_gamepass:
        # Trade is valid regardless of the difference
        trade_validity_label.configure(text="Trade Validity: Can Accept",
                                       text_color="#90EE90")  # Light Green
    else:
        # Define the 40% difference bounds based on "You" total
        lower_bound = 0.6 * your_total
        upper_bound = 1.4 * your_total

        if lower_bound <= their_total <= upper_bound:
            trade_validity_label.configure(text="Trade Validity: Can Accept",
                                           text_color="#90EE90")  # Light Green
        else:
            trade_validity_label.configure(text="Trade Validity: Value difference too large",
                                           text_color="#FF6347")  # Light Red (Tomato)

def clear_main_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

# ------------------------
#       MAIN WINDOW
# ------------------------
def setup_main_window():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    load_square_images()
    
    root = ctk.CTk()
    root.title('IrohBot - BloxFruits')
    root.geometry('1000x700')
    root.configure(fg_color="#2d2d2d")
    
    global main_frame
    main_frame = ctk.CTkFrame(root, fg_color="#3c3c3c", corner_radius=10)
    main_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))
    
    ctk.CTkLabel(main_frame, text="Welcome to IrohBot!",
                font=('Helvetica', 24), text_color="#ffffff").pack(pady=20)
    
    button_frame = ctk.CTkFrame(root, fg_color="#2d2d2d", height=80)
    button_frame.pack(side="bottom", fill="x", padx=20, pady=20)
    
    button_frame.grid_rowconfigure(0, weight=0)
    button_frame.grid_columnconfigure(0, weight=0)
    button_frame.grid_columnconfigure(1, weight=0)
    
    global time_left
    time_left = ctk.StringVar(value="19:00")
    ctk.CTkLabel(button_frame, textvariable=time_left,
                font=('Helvetica', 20), text_color="#ffffff").grid(
        row=0, column=0, columnspan=2, pady=(0, 5), sticky="w")
    
    ctk.CTkButton(button_frame, text='Start AFK Mode', command=start_afk,
                fg_color="#6a4c9c", hover_color="#9b7abf", height=40).grid(
        row=1, column=0, padx=(0, 5), sticky="w")
    
    ctk.CTkButton(button_frame, text='Fruit Calculator', command=show_fruit_calculator,
                fg_color="#6a4c9c", hover_color="#9b7abf", height=40).grid(
        row=1, column=1, padx=(5, 0), sticky="w")
    
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()

def on_closing(root):
    global timer_running
    timer_running = False
    root.destroy()

# ------------------------
#       MAIN ENTRY
# ------------------------
if __name__ == "__main__":
    setup_main_window()
