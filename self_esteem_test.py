import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import random
import datetime

# ---------------- COLORS ----------------
COLOR_BG = "#E6F2F0"
COLOR_SURFACE = "#FAFCFB"
COLOR_TEXT = "#2E3A3A"
COLOR_ACCENT = "#4FB0AE"
COLOR_DELETE = "#E57373"

# ---------------- DATABASE ----------------
conn = sqlite3.connect("data.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    score INTEGER,
    level TEXT,
    invite_code TEXT UNIQUE,
    invited_by TEXT,
    date TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    text TEXT,
    date TEXT
)
""")
conn.commit()

def add_columns_if_not_exist():
    col_names = [row[1] for row in cur.execute("PRAGMA table_info(users)")]
    needed_cols = ['q1','q2','q3','q4','q5','q6','q7','q8','q9','q10','advice']
    for col in needed_cols:
        if col not in col_names:
            cur.execute(f"ALTER TABLE users ADD COLUMN {col} {'TEXT' if col=='advice' else 'INTEGER'} DEFAULT 0")
    conn.commit()

add_columns_if_not_exist()

# ---------------- QUESTIONS ----------------
questions = [
"وقتی با مشکلات زندگی روبه‌رو می‌شوم معمولاً:",
"وقتی اشتباهی از من سر می‌زند معمولاً:",
"وقتی تنها هستم معمولاً:",
"وقتی می‌خواهم چیزی برای خودم بخرم:",
"اگر کسی از من انتقاد یا مرا مسخره کند:",
"از شغلی که در حال حاضر به آن مشغول هستم:",
"در مورد هدف‌های زندگی:",
"در مورد خرج کردن برای خودم:",
"وقتی کسی از من درخواستی دارد که نمی‌خواهم انجام بدهم:",
"در مقایسه خودم با دیگران:"
]

options = [
["آرامش خودم را حفظ می‌کنم و منطقی فکر می‌کنم","دنبال راه حل می‌گردم","کمی نگران می‌شوم","استرس زیادی می‌گیرم","کاملاً بهم می‌ریزم"],
["اشتباه را می‌پذیرم و جبران می‌کنم","از آن درس می‌گیرم","کمی ناراحت می‌شوم","مدت زیادی خودم را سرزنش می‌کنم","احساس گناه شدید دارم"],
["از تنهایی برای رشد استفاده می‌کنم","با کارهای مورد علاقه سرگرم می‌شوم","گاهی احساس تنهایی دارم","اغلب احساس تنهایی دارم","تنهایی برایم آزاردهنده است"],
["چیزی را می‌خرم که دوست دارم","کیفیت را در نظر می‌گیرم","معمولی انتخاب می‌کنم","اغلب ارزان می‌خرم","همیشه ارزان‌ترین"],
["آرام می‌مانم","منطقی بررسی می‌کنم","کمی ناراحت می‌شوم","خیلی ناراحت می‌شوم","مدت‌ها درگیر می‌شوم"],
["کاملاً از شغلم راضی هستم","تا حد زیادی راضی هستم","تا حدی راضی هستم","چندان راضی نیستم","اصلاً راضی نیستم"],
["هدف‌های مشخص دارم","تقریباً می‌دانم چه می‌خواهم","در حال پیدا کردن مسیرم هستم","هدف مشخصی ندارم","کاملاً سردرگم هستم"],
["برای خودم هزینه می‌کنم","گاهی هزینه می‌کنم","با احتیاط خرج می‌کنم","کم خرج می‌کنم","تقریباً هیچ"],
["محترمانه نه می‌گویم","اغلب می‌توانم نه بگویم","گاهی سخت است","معمولاً نمی‌توانم","تقریباً همیشه قبول می‌کنم"],
["خیلی کم مقایسه می‌کنم","گاهی مقایسه می‌کنم","گاهی ناراحت می‌شوم","زیاد مقایسه می‌کنم","همیشه خودم را کمتر می‌بینم"]
]

index = 0
answers = []
user_name = ""
invite_code = ""
invited_by = ""
version = "نسخه نرم افزار: 1.1.1"

def generate_code(): 
    return str(random.randint(10000,99999))

# ---------------- TEST FLOW ----------------
def start_test():
    global user_name, invited_by, index, answers

    result_frame.pack_forget()

    user_name = name_entry.get().strip()
    invited_by = invite_entry.get().strip()
    if not user_name:
        messagebox.showerror("خطا", "نام را وارد کنید")
        return

    index = 0
    answers = []
    start_frame.pack_forget()
    show_question()

def show_question():
    global index
    for w in question_frame.winfo_children(): w.destroy()

    if index >= len(questions):
        finish()
        return

    tk.Label(
        question_frame,
        text=questions[index],
        bg=COLOR_BG,
        fg=COLOR_TEXT,
        font=("Tahoma", 15, "bold"),
        wraplength=750,
        justify="center"
    ).pack(pady=30)

    for i, opt in enumerate(options[index]):
        tk.Button(
            question_frame,
            text=opt,
            width=50,
            bg=COLOR_ACCENT,
            fg="white",
            font=("Tahoma", 13),
            command=lambda v=i: next_question(v)
        ).pack(pady=10)

    question_frame.pack(pady=10)

def next_question(val):
    answers.append(val+1)
    global index
    index += 1
    show_question()

# ---------------- RESULT CARD ----------------
def finish():
    global invite_code
    score = sum(answers)

    if score <= 20:
        level = "عزت نفس بالا"
        card_color = "#C8E6C9"
        text_color = "#1B5E20"
    elif score <= 35:
        level = "عزت نفس متوسط"
        card_color = "#FFF9C4"
        text_color = "#F57F17"
    else:
        level = "عزت نفس پایین"
        card_color = "#FFCDD2"
        text_color = "#B71C1C"

    invite_code = generate_code()
    date = str(datetime.date.today())

    cur.execute("""
        INSERT INTO users(name,score,level,invite_code,invited_by,date,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10,advice)
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (user_name, score, level, invite_code, invited_by, date, *answers, ""))
    conn.commit()

    question_frame.pack_forget()
    for w in result_frame.winfo_children(): w.destroy()

    card = tk.Frame(result_frame, bg=card_color, bd=10, relief="ridge")
    card.pack(pady=50, ipadx=20, ipady=20)

    tk.Label(card,text="🎉 نتیجه تست عزت نفس شما 🎉",bg=card_color,fg=text_color,font=("B Nazanin", 24, "bold")).pack(pady=10)
    tk.Label(card,text=f"نام: {user_name}",bg=card_color,fg=text_color,font=("IRANSans", 16)).pack(pady=5)
    tk.Label(card,text=f"امتیاز: {score}",bg=card_color,fg=text_color,font=("IRANSans", 18, "bold")).pack(pady=5)
    tk.Label(card,text=f"سطح: {level}",bg=card_color,fg=text_color,font=("IRANSans", 20, "bold")).pack(pady=15)

    tk.Button(result_frame,text="🔄 شروع مجدد",command=start_test,bg="#4FB0AE",fg="white",
              font=("Tahoma", 13, "bold"),width=20,height=2).pack(pady=20)

    result_frame.pack(expand=True)

# ---------------- ABOUT PAGE (NEW TEXT) ----------------
def about():
    text = (
        "مهدی شیخی نیکو هستم و عاشق خدمتگزاری به خلق خدا و از بچگی این رویا را داشتم "
        "که به مخلوقات خدا خدمتی کنم و آثاری ارزشمند یا یک اثر بزرگ ارزشمند بجای بگذارم "
        "که بندگان خدا، زندگی آسوده و راحتی داشته باشند. "
        "از شما عزیزان تقاضامندم که در این مسیر ما را یاری کنید تا افراد بیشتری "
        "به آرامش و سعادت و زندگی خوب دست یابند."
    )

    win = tk.Toplevel(root)
    win.title("درباره ما")
    win.geometry("900x450")
    win.configure(bg=COLOR_BG)

    tk.Label(
        win,
        text=text,
        bg=COLOR_BG,
        fg=COLOR_TEXT,
        font=("Tahoma", 15),
        wraplength=850,
        justify="center"
    ).pack(pady=40)

# ---------------- RESULTS FRIENDS ----------------
def results_friends():
    win = tk.Toplevel(root)
    win.title("تجربیات دوستان")
    win.geometry("450x550")
    win.configure(bg=COLOR_BG)

    tk.Label(win,text="نام شما",bg=COLOR_BG,font=("Tahoma",14,"bold")).pack()
    name_e = tk.Entry(win,font=("Tahoma",13),bg=COLOR_SURFACE)
    name_e.pack(pady=4)

    tk.Label(win,text="تجربه شما",bg=COLOR_BG,font=("Tahoma",14,"bold")).pack()
    text_e = tk.Text(win,height=4,font=("Tahoma",13),bg=COLOR_SURFACE)
    text_e.pack(pady=4,padx=10,fill="x")

    box = tk.Text(win,height=12,font=("Tahoma",13),bg=COLOR_SURFACE)
    box.pack(pady=10,padx=10,fill="both")

    def refresh():
        box.delete("1.0","end")
        cur.execute("SELECT name,text,date FROM results ORDER BY id DESC")
        for r in cur.fetchall():
            box.insert("end",f"{r[0]} ({r[2]}):\n{r[1]}\n{'-'*30}\n")

    def save():
        if name_e.get():
            cur.execute("INSERT INTO results(name,text,date) VALUES(?,?,?)",
                        (name_e.get(), text_e.get("1.0","end"), str(datetime.date.today())))
            conn.commit()
            refresh()

    tk.Button(win,text="ثبت تجربه",command=save,bg=COLOR_ACCENT,fg="white",
              font=("Tahoma",14,"bold")).pack(pady=5)

    refresh()

# ---------------- ADMIN: DELETE FRIEND RESULTS ----------------
def open_results_manager():
    win = tk.Toplevel(root)
    win.title("مدیریت تجربه‌ها")
    win.geometry("650x600")
    win.configure(bg=COLOR_BG)

    list_box = tk.Listbox(win, font=("Tahoma", 12), height=22)
    list_box.pack(fill="both", expand=True, padx=10, pady=10)

    def load_results():
        list_box.delete(0, "end")
        cur.execute("SELECT id, name, text, date FROM results ORDER BY id DESC")
        for r in cur.fetchall():
            list_box.insert("end", f"ID {r[0]} - {r[1]} ({r[3]}): {r[2][:40]}...")

    load_results()

    def delete_selected():
        try:
            sel = list_box.get(list_box.curselection())
        except:
            messagebox.showerror("خطا", "لطفاً یک آیتم انتخاب کنید.")
            return

        item_id = sel.split(" ")[1]

        if messagebox.askyesno("حذف تجربه", "آیا مطمئن هستید؟"):
            cur.execute("DELETE FROM results WHERE id=?", (item_id,))
            conn.commit()
            load_results()

    tk.Button(
        win,
        text="حذف تجربه انتخاب‌شده",
        bg=COLOR_DELETE,
        fg="white",
        font=("Tahoma",12,"bold"),
        command=delete_selected
    ).pack(pady=10)

# ---------------- ADMIN LOGIN ----------------
def admin_login():
    pw = simpledialog.askstring("ورود مدیر", "رمز عبور:", show="*")
    if pw == "1212":
        open_admin()
    else:
        messagebox.showerror("خطا","رمز اشتباه است")

def open_admin():
    win = tk.Toplevel(root)
    win.title("پنل مدیریت")
    win.geometry("650x650")
    win.configure(bg=COLOR_BG)

    box = tk.Text(win, font=("Tahoma",11), bg=COLOR_SURFACE)
    box.pack(fill="both", expand=True, padx=10, pady=10)

    cur.execute("SELECT name,score,level,invite_code,invited_by,date FROM users ORDER BY id DESC")
    for r in cur.fetchall():
        box.insert("end",
                   f"نام: {r[0]}\n"
                   f"امتیاز: {r[1]}\n"
                   f"سطح: {r[2]}\n"
                   f"کد: {r[3]}\n"
                   f"دعوت شده: {r[4]}\n"
                   f"تاریخ: {r[5]}\n"
                   f"{'-'*40}\n")

    tk.Button(
        win,
        text="مدیریت تجربه‌های دوستان",
        bg=COLOR_ACCENT,
        fg="white",
        font=("Tahoma", 12, "bold"),
        command=open_results_manager
    ).pack(pady=10)

# ---------------- MAIN UI ----------------
root = tk.Tk()
root.title("تست عزت نفس")
root.geometry("800x700")
root.configure(bg=COLOR_BG)

start_frame = tk.Frame(root, bg=COLOR_BG)
question_frame = tk.Frame(root, bg=COLOR_BG)
result_frame = tk.Frame(root, bg=COLOR_BG)

tk.Label(start_frame,text="نام و نام خانوادگی",bg=COLOR_BG,fg=COLOR_TEXT,font=("Tahoma",11)).pack(pady=5)
name_entry = tk.Entry(start_frame,font=("Tahoma",12),justify="center",bg=COLOR_SURFACE)
name_entry.pack(pady=5)

tk.Label(start_frame,text="کد دعوت (اگر دارید)",bg=COLOR_BG,fg=COLOR_TEXT).pack(pady=5)
invite_entry = tk.Entry(start_frame,font=("Tahoma",12),justify="center",bg=COLOR_SURFACE)
invite_entry.pack(pady=5)

tk.Button(start_frame,text="شروع تست عزت نفس",command=start_test,
          bg=COLOR_ACCENT,fg="white",font=("Tahoma",12,"bold"),
          width=25,height=2).pack(pady=20)

tk.Button(start_frame,text="تجربیات دیگران",command=results_friends,
          bg=COLOR_BG,fg=COLOR_TEXT,width=20).pack(pady=5)

tk.Button(start_frame,text="درباره ما",command=about,
          bg=COLOR_BG,fg=COLOR_TEXT,width=20).pack(pady=5)

tk.Button(start_frame,text="ورود مدیر",command=admin_login,
          bg=COLOR_BG,fg="#555",width=20).pack(pady=20)

tk.Label(start_frame,text=version,bg=COLOR_BG,fg="#777",font=("Tahoma",9)).pack(side="bottom")

start_frame.pack(expand=True)
root.mainloop()
