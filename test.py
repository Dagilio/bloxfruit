import os
import time
import threading
import concurrent.futures
import customtkinter as ctk
import tkinter as tk
from plyer import notification
from PIL import Image

# Global variables
timer_running = False
side_data = {}
square_images = {}
trade_validity_label = None

root = None
page_container = None
pages = {}
time_left = None

ITEM_VALUES = {
    "Rocket": {"game_price": 5000, "market_value": 5000},
    "Spin": {"game_price": 7500, "market_value": 7500},
    "Blade": {"game_price": 30000, "market_value": 50000},
    "Spring": {"game_price": 60000, "market_value": 60000},
    "Bomb": {"game_price": 80000, "market_value": 80000},
    "Smoke": {"game_price": 100000, "market_value": 100000},
    "Spike": {"game_price": 180000, "market_value": 180000},
    "Flame": {"game_price": 250000, "market_value": 250000},
    "Falcon": {"game_price": 300000, "market_value": 300000},
    "Ice": {"game_price": 350000, "market_value": 550000},
    "Sand": {"game_price": 420000, "market_value": 420000},
    "Dark": {"game_price": 500000, "market_value": 400000},
    "Diamond": {"game_price": 600000, "market_value": 1500000},
    "Light": {"game_price": 650000, "market_value": 800000},
    "Rubber": {"game_price": 750000, "market_value": 700000},
    "Barrier": {"game_price": 800000, "market_value": 800000},
    "Ghost": {"game_price": 800000, "market_value": 800000},
    "Magma": {"game_price": 1150000, "market_value": 1150000},
    "Quake": {"game_price": 1000000, "market_value": 1000000},
    "Buddha": {"game_price": 1200000, "market_value": 10000000},
    "Love": {"game_price": 1300000, "market_value": 1150000},
    "Spider": {"game_price": 1500000, "market_value": 1150000},
    "Sound": {"game_price": 1700000, "market_value": 2500000},
    "Phoenix": {"game_price": 1800000, "market_value": 2250000},
    "Portal": {"game_price": 1900000, "market_value": 10000000},
    "Rumble": {"game_price": 2100000, "market_value": 7000000},
    "Pain": {"game_price": 2300000, "market_value": 2000000},
    "Blizzard": {"game_price": 2400000, "market_value": 5000000},
    "Gravity": {"game_price": 2500000, "market_value": 2000000},
    "Mammoth": {"game_price": 2700000, "market_value": 8000000},
    "T-Rex": {"game_price": 2700000, "market_value": 20000000},
    "Dough": {"game_price": 2800000, "market_value": 30000000},
    "Shadow": {"game_price": 2900000, "market_value": 6000000},
    "Venom": {"game_price": 3000000, "market_value": 9000000},
    "Control": {"game_price": 3200000, "market_value": 20000000},
    "Gas": {"game_price": 3200000, "market_value": 80000000},
    "Spirit": {"game_price": 3400000, "market_value": 9000000},
    "Leopard": {"game_price": 5000000, "market_value": 50000000},
    "Yeti": {"game_price": 5000000, "market_value": 115000000},
    "Kitsune": {"game_price": 8000000, "market_value": 165000000},
    "East Dragon": {"game_price": 15000000, "market_value": 545000000},
    "West Dragon": {"game_price": 15000000, "market_value": 565000000},
    "Permanent Rocket": {"game_price": 0, "robux": 50, "market_value": 5000000},
    "Permanent Spin": {"game_price": 0, "robux": 75, "market_value": 7500000},
    "Permanent Blade": {"game_price": 0, "robux": 100, "market_value": 10000000},
    "Permanent Spring": {"game_price": 0, "robux": 180, "market_value": 15000000},
    "Permanent Bomb": {"game_price": 0, "robux": 220, "market_value": 20000000},
    "Permanent Smoke": {"game_price": 0, "robux": 250, "market_value": 25000000},
    "Permanent Spike": {"game_price": 0, "robux": 380, "market_value": 30000000},
    "Permanent Flame": {"game_price": 0, "robux": 550, "market_value": 40000000},
    "Permanent Falcon": {"game_price": 0, "robux": 650, "market_value": 65000000},
    "Permanent Ice": {"game_price": 0, "robux": 750, "market_value": 150000000},
    "Permanent Sand": {"game_price": 0, "robux": 850, "market_value": 100000000},
    "Permanent Dark": {"game_price": 0, "robux": 950, "market_value": 160000000},
    "Permanent Diamond": {"game_price": 0, "robux": 1000, "market_value": 130000000},
    "Permanent Light": {"game_price": 0, "robux": 1100, "market_value": 190000000},
    "Permanent Rubber": {"game_price": 0, "robux": 1200, "market_value": 205000000},
    "Permanent Barrier": {"game_price": 0, "robux": 1250, "market_value": 190000000},
    "Permanent Ghost": {"game_price": 0, "robux": 1275, "market_value": 195000000},
    "Permanent Magma": {"game_price": 0, "robux": 1300, "market_value": 235000000},
    "Permanent Quake": {"game_price": 0, "robux": 1500, "market_value": 270000000},
    "Permanent Buddha": {"game_price": 0, "robux": 1650, "market_value": 380000000},
    "Permanent Love": {"game_price": 0, "robux": 1700, "market_value": 305000000},
    "Permanent Spider": {"game_price": 0, "robux": 1800, "market_value": 325000000},
    "Permanent Sound": {"game_price": 0, "robux": 1900, "market_value": 340000000},
    "Permanent Phoenix": {"game_price": 0, "robux": 2000, "market_value": 360000000},
    "Permanent Portal": {"game_price": 0, "robux": 2000, "market_value": 400000000},
    "Permanent Rumble": {"game_price": 0, "robux": 2100, "market_value": 375000000},
    "Permanent Pain": {"game_price": 0, "robux": 2200, "market_value": 395000000},
    "Permanent Blizzard": {"game_price": 0, "robux": 2250, "market_value": 405000000},
    "Permanent Gravity": {"game_price": 0, "robux": 2300, "market_value": 415000000},
    "Permanent Mammoth": {"game_price": 0, "robux": 2350, "market_value": 375000000},
    "Permanent T-Rex": {"game_price": 0, "robux": 2350, "market_value": 425000000},
    "Permanent Dough": {"game_price": 0, "robux": 2400, "market_value": 450000000},
    "Permanent Shadow": {"game_price": 0, "robux": 2425, "market_value": 435000000},
    "Permanent Venom": {"game_price": 0, "robux": 2450, "market_value": 440000000},
    "Permanent Control": {"game_price": 0, "robux": 2500, "market_value": 575000000},
    "Permanent Gas": {"game_price": 0, "robux": 2500, "market_value": 415000000},
    "Permanent Spirit": {"game_price": 0, "robux": 2550, "market_value": 460000000},
    "Permanent Leopard": {"game_price": 0, "robux": 3000, "market_value": 525000000},
    "Permanent Yeti": {"game_price": 0, "robux": 3000, "market_value": 510000000},
    "Permanent Kitsune": {"game_price": 0, "robux": 4000, "market_value": 720000000},
    "Permanent East Dragon": {"game_price": 0, "robux": 2500, "market_value": 1350000000},
    "Permanent West Dragon": {"game_price": 0, "robux": 2500, "market_value": 1350000000},
    "Fast Boats": {"game_price": 0, "robux": 350, "market_value": 45000000},
    "2x Boss Drop": {"game_price": 0, "robux": 350, "market_value": 55000000},
    "2x Money": {"game_price": 0, "robux": 450, "market_value": 75000000},
    "2x Mastery": {"game_price": 0, "robux": 450, "market_value": 55000000},
    "Fruit Storage": {"game_price": 0, "robux": 400, "market_value": 75000000},
    "Dark Blade": {"game_price": 0, "robux": 1200, "market_value": 200000000},
    "Fruit Notifier": {"game_price": 0, "robux": 2700, "market_value": 500000000},
}

RARITY_COLORS = {
    "Common": "#FFFFE4",
    "Uncommon": "#7FFFD4",
    "Rare": "#4169E1",
    "Legendary": "#8F00FF",
    "Mythical": "#FF000D",
    "Gamepass": "#FFD700",
    "Permanent": "#FF8C00",
}

def get_rarity(item):
    if "robux" in ITEM_VALUES[item]:
        return "Permanent" if "Permanent" in item else "Gamepass"
    elif item in ["Rocket", "Spin", "Blade", "Spring", "Bomb", "Smoke", "Spike"]:
        return "Common"
    elif item in ["Flame", "Falcon", "Ice", "Sand", "Dark", "Diamond"]:
        return "Uncommon"
    elif item in ["Light", "Rubber", "Barrier", "Ghost", "Magma"]:
        return "Rare"
    elif item in ["Quake", "Rumble", "Buddha", "Love", "Spider", "Sound", "Phoenix", "Portal"]:
        return "Legendary"
    elif item in ["Pain", "Blizzard", "Gravity", "Mammoth", "T-Rex", "Dough", "Shadow",
                  "Venom", "Control", "Gas", "Spirit", "Leopard", "Yeti", "Kitsune",
                  "East Dragon", "West Dragon"]:
        return "Mythical"
    return "Common"

def load_pil_image(task):
    fruit, path, size = task
    try:
        img = Image.open(path).resize(size)
        return fruit, img
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return fruit, None

def load_square_images():
    global square_images
    tasks = []
    add_path = os.path.join("imgs", "add.png")
    tasks.append(("add", add_path, (32, 32)))
    for fruit in ITEM_VALUES:
        path = os.path.join("imgs", fruit.lower().replace(" ", "_") + ".png")
        tasks.append((fruit, path, (64, 64)))
    pil_images = {}
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for fruit, pil_img in executor.map(load_pil_image, tasks):
            pil_images[fruit] = pil_img
    add_img = ctk.CTkImage(dark_image=pil_images["add"], size=(32, 32)) if pil_images.get("add") else None
    square_images["add"] = add_img
    for fruit in ITEM_VALUES:
        if pil_images.get(fruit):
            square_images[fruit] = ctk.CTkImage(dark_image=pil_images[fruit], size=(64, 64))
        else:
            square_images[fruit] = add_img

class VirtualFruitItem(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#615675", corner_radius=6, **kwargs)
        self.click_callback = None
        self.current_fruit = None
        self.img_label = ctk.CTkLabel(self, text="")
        self.img_label.grid(row=0, column=0, rowspan=4, padx=5, pady=5, sticky="n")
        self.name_label = ctk.CTkLabel(self, text="", font=("Helvetica", 14, "bold"))
        self.name_label.grid(row=0, column=1, sticky="w")
        self.market_label = ctk.CTkLabel(self, text="", font=("Helvetica", 12, "bold"))
        self.market_label.grid(row=1, column=1, sticky="w")
        self.value_label = ctk.CTkLabel(self, text="", font=("Helvetica", 12))
        self.value_label.grid(row=2, column=1, sticky="w")
        self.robux_label = None

    def update_data(self, fruit):
        self.current_fruit = fruit
        data = ITEM_VALUES[fruit]
        img = square_images.get(fruit, square_images["add"])
        self.img_label.configure(image=img, text="")
        self.name_label.configure(text=fruit, text_color=RARITY_COLORS.get(get_rarity(fruit), "#ff8080"))
        self.market_label.configure(text="Market value:")
        self.value_label.configure(text=f"${data['market_value']:,}", text_color="#90EE90")
        if "robux" in data:
            if self.robux_label is None:
                self.robux_label = ctk.CTkLabel(self, text="", font=("Helvetica", 12))
                self.robux_label.grid(row=3, column=1, sticky="w")
            robux_color = RARITY_COLORS["Permanent"] if "Permanent" in fruit else RARITY_COLORS["Gamepass"]
            self.robux_label.configure(text=f"Robux: R{data['robux']:,}", text_color=robux_color)
        else:
            if self.robux_label is not None:
                self.robux_label.destroy()
                self.robux_label = None
        if self.click_callback:
            self.bind("<Button-1>", lambda e, f=fruit: self.click_callback(f))
            for widget in self.winfo_children():
                widget.bind("<Button-1>", lambda e, f=fruit: self.click_callback(f))

class VirtualFruitList(ctk.CTkFrame):
    def __init__(self, master, data, click_callback=None, **kwargs):
        super().__init__(master, **kwargs)
        self.data = data
        self.click_callback = click_callback
        self.item_height = 90
        self.canvas = tk.Canvas(self, bg=self.cget("fg_color"), highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, side="left")
        self.vscroll = ctk.CTkScrollbar(self, orientation="vertical", command=self.on_scroll)
        self.vscroll.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.vscroll.set)
        self.inner_frame = ctk.CTkFrame(self.canvas, fg_color=self.cget("fg_color"))
        self.window = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.item_frames = []
        self.visible_count = 0
        self.refresh_visible_count()
        self.refresh()
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def refresh_visible_count(self):
        height = self.canvas.winfo_height()
        new_count = int(height / self.item_height) + 2
        if new_count != self.visible_count:
            for widget in self.item_frames:
                widget.destroy()
            self.item_frames = []
            self.visible_count = new_count
            for _ in range(self.visible_count):
                item = VirtualFruitItem(self.inner_frame)
                self.item_frames.append(item)

    def on_frame_configure(self, event):
        total_height = len(self.data) * self.item_height
        self.inner_frame.configure(height=total_height)
        self.canvas.configure(scrollregion=(0, 0, self.canvas.winfo_width(), total_height))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.window, width=event.width)
        self.refresh_visible_count()
        self.refresh()

    def set_data(self, data):
        self.data = data
        total_height = len(data) * self.item_height
        self.inner_frame.configure(height=total_height)
        self.canvas.configure(scrollregion=(0, 0, self.canvas.winfo_width(), total_height))
        self.refresh_visible_count()
        self.refresh()

    def refresh(self, event=None):
        y_offset = self.canvas.canvasy(0)
        first_index = int(y_offset / self.item_height)
        for i, widget in enumerate(self.item_frames):
            data_index = first_index + i
            if data_index < len(self.data):
                fruit = self.data[data_index]
                widget.click_callback = self.click_callback
                widget.update_data(fruit)
                widget.configure(height=self.item_height)
                widget.place(x=0, y=(first_index + i) * self.item_height, relwidth=1)
            else:
                widget.place_forget()

    def on_scroll(self, *args):
        self.canvas.yview(*args)
        self.refresh()

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")
        self.refresh()

def create_search_overlay(parent, side):
    ov = ctk.CTkFrame(parent, fg_color="#3c3c3c")
    ov.place(x=0, y=0, relwidth=1, relheight=1)
    ov.place_forget()
    var = ctk.StringVar()
    se = ctk.CTkEntry(ov, textvariable=var, placeholder_text="Search fruit...", width=320)
    se.pack(pady=10)
    all_fruits = list(ITEM_VALUES.keys())
    virtual_list = VirtualFruitList(
        ov,
        data=all_fruits,
        click_callback=lambda fruit: select_fruit(side, fruit),
        fg_color="#3c3c3c"
    )
    virtual_list.pack(fill="both", expand=True, padx=10, pady=10)

    def on_search(*_):
        filter_text = var.get().lower()
        filtered = [fruit for fruit in all_fruits if filter_text in fruit.lower()]
        virtual_list.set_data(filtered)

    var.trace_add("write", on_search)
    return ov

def reset_trade_state():
    for side in ["You", "Them"]:
        d = side_data.get(side)
        if d:
            d["items"] = [None] * 4
            for btn in d["squares"]:
                btn.configure(image=square_images["add"])
            d["total_game_label"].configure(text="Total Game Price: $0")
            d["total_market_label"].configure(text="Total Market Value: $0")
            d["search_overlay"].place_forget()
            d["active_idx"] = None
    if trade_validity_label:
        trade_validity_label.configure(text="Trade Validity: N/A", text_color="#ffffff")

def go_home():
    reset_trade_state()
    show_page("home")

def create_side(parent, side):
    sf = ctk.CTkFrame(parent, fg_color="#4a4a4a", corner_radius=8)
    col = 0 if side == "You" else 1
    sf.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
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
        btn = ctk.CTkButton(
            items_frame,
            text="",
            image=square_images["add"],
            fg_color="#6a4c9c",
            hover_color="#7f5bad",
            width=120,
            height=80,
            command=lambda i=idx, s=side: handle_square_click(s, i)
        )
        btn.grid(row=r, column=c, padx=10, pady=10, sticky="nsew")
        squares.append(btn)
    gl = ctk.CTkLabel(
        sf,
        text="Total Game Price: $0",
        font=('Helvetica Rounded', 16, 'bold'),
        text_color="#FFFFE4"
    )
    gl.pack(pady=(10, 5))
    ml = ctk.CTkLabel(
        sf,
        text="Total Market Value: $0",
        font=('Helvetica Rounded', 16, 'bold'),
        text_color="#90EE90"
    )
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

def handle_square_click(side, idx):
    d = side_data[side]
    if d["items"][idx]:
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
    you_items = side_data["You"]["items"]
    them_items = side_data["Them"]["items"]
    your_total = sum(ITEM_VALUES[x]['game_price'] for x in you_items if x)
    their_total = sum(ITEM_VALUES[x]['market_value'] for x in them_items if x)
    you_has_gamepass = any("robux" in ITEM_VALUES[item] for item in you_items if item)
    them_has_gamepass = any("robux" in ITEM_VALUES[item] for item in them_items if item)
    if you_has_gamepass or them_has_gamepass:
        trade_validity_label.configure(text="Trade Validity: Can Accept", text_color="#90EE90")
    else:
        lower_bound = 0.6 * your_total
        upper_bound = 1.4 * your_total
        if lower_bound <= their_total <= upper_bound:
            trade_validity_label.configure(text="Trade Validity: Can Accept", text_color="#90EE90")
        else:
            trade_validity_label.configure(text="Trade Validity: Value difference too large", text_color="#FF6347")

def init_trade_page(parent):
    global trade_validity_label
    trade_page = ctk.CTkFrame(parent, fg_color="#3c3c3c", corner_radius=10)
    ctk.CTkLabel(
        trade_page,
        text="Blox Fruits Trade Calculator",
        font=('Helvetica', 24),
        text_color="#ffffff"
    ).pack(pady=10)
    trade_validity_label = ctk.CTkLabel(
        trade_page,
        text="Trade Validity: N/A",
        font=('Helvetica', 14),
        text_color="#ffffff"
    )
    trade_validity_label.pack(pady=(0, 20))
    trade_frame = ctk.CTkFrame(trade_page, fg_color="#3c3c3c", corner_radius=10)
    trade_frame.pack(pady=10, padx=20, fill="both", expand=True)
    trade_frame.grid_rowconfigure(0, weight=1)
    trade_frame.grid_columnconfigure(0, weight=1)
    trade_frame.grid_columnconfigure(1, weight=1)
    create_side(trade_frame, "You")
    create_side(trade_frame, "Them")
    nav_frame = ctk.CTkFrame(trade_page, fg_color="#3c3c3c")
    nav_frame.pack(pady=10)
    ctk.CTkButton(
        nav_frame,
        text="Back",
        command=go_home,
        fg_color="#6a4c9c",
        hover_color="#9b7abf",
        height=40
    ).grid(row=0, column=0, padx=10)
    ctk.CTkButton(
        nav_frame,
        text="Clear",
        command=reset_trade_state,
        fg_color="#6a4c9c",
        hover_color="#9b7abf",
        height=40
    ).grid(row=0, column=1, padx=10)
    return trade_page

def show_page(page_name):
    for page in pages.values():
        page.pack_forget()
    pages[page_name].pack(fill="both", expand=True)

def start_afk_timer():
    global timer_running
    t = 19 * 60
    timer_running = True
    while t > 0 and timer_running:
        m, s = divmod(t, 60)
        time_left.set(f"{m:02}:{s:02}")
        time.sleep(1)
        t -= 1
    if timer_running:
        notification.notify(title='AFK Reminder', message='Please move in Blox Fruits!', timeout=10)
    timer_running = False

def start_afk():
    global timer_running
    if not timer_running:
        threading.Thread(target=start_afk_timer, daemon=True).start()
    else:
        print("AFK timer is already running.")

def setup_main_window():
    global root, page_container, time_left
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    load_square_images()
    root = ctk.CTk()
    root.title('IrohBot - BloxFruits')
    root.geometry('1000x700')
    root.configure(fg_color="#2d2d2d")
    button_frame = ctk.CTkFrame(root, fg_color="#2d2d2d", height=80)
    button_frame.pack(side="bottom", fill="x", padx=20, pady=20)
    button_frame.grid_columnconfigure(0, weight=0)
    button_frame.grid_columnconfigure(1, weight=0)
    time_left = ctk.StringVar(value="19:00")
    ctk.CTkLabel(
        button_frame,
        textvariable=time_left,
        font=('Helvetica', 20),
        text_color="#ffffff"
    ).grid(row=0, column=0, columnspan=2, pady=(0,5), sticky="w")
    ctk.CTkButton(
        button_frame,
        text='Start AFK Mode',
        command=start_afk,
        fg_color="#6a4c9c",
        hover_color="#9b7abf",
        height=40
    ).grid(row=1, column=0, padx=(0,5), sticky="w")
    ctk.CTkButton(
        button_frame,
        text='Fruit Calculator',
        command=lambda: show_page("trade"),
        fg_color="#6a4c9c",
        hover_color="#9b7abf",
        height=40
    ).grid(row=1, column=1, padx=(5,0), sticky="w")
    page_container = ctk.CTkFrame(root, fg_color="#3c3c3c", corner_radius=10)
    page_container.pack(fill="both", expand=True, padx=20, pady=(20,10))
    home_page = ctk.CTkFrame(page_container, fg_color="#3c3c3c", corner_radius=10)
    ctk.CTkLabel(
        home_page,
        text="Welcome to IrohBot!",
        font=('Helvetica', 24),
        text_color="#ffffff"
    ).pack(pady=20)
    pages["home"] = home_page
    pages["trade"] = init_trade_page(page_container)
    show_page("home")
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.mainloop()

def on_closing(root):
    global timer_running
    timer_running = False
    root.destroy()

if __name__ == "__main__":
    try:
        setup_main_window()
    except Exception as e:
        print("An error occurred:", e)
        input("Press Enter to exit...")
