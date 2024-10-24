from bs4 import BeautifulSoup
import requests
import sqlite3
import tkinter as tk
from tkinter import font ,ttk


db = sqlite3.connect("parser.db")
cursor = db.cursor()

def show_data():
    tree = ttk.Treeview(root,columns=("ID","Названия","Цена","Ссылка","Адресс"),show="headings")
    tree.heading("ID",text="ID")
    tree.heading("Названия",text="Названия")
    tree.heading("Цена",text="Цена")
    tree.heading("Ссылка",text="Ссылка")
    tree.heading("Адресс",text="Адресс")

    tree.column("ID",width=50)
    tree.column("Названия",width=200)
    tree.column("Цена",width=100)
    tree.column("Ссылка",width=200)
    tree.column("Адресс",width=200)

    scrollbar = ttk.Scrollbar(root,orient="vertical",command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right",fill="y")
    tree.pack(fill="both",expand=True,padx=10,pady=10)
    cursor.execute("SELECT * FROM parser")
    all_informations = cursor.fetchall()


    for row in tree.get_children():
        tree.delete(row)


    for row in all_informations:
        tree.insert("",tk.END,values=row)

def get_link():

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parser(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Названия TEXT,
                Цена TEXT,
                Ссылка TEXT,
                Адресс TEXT
        )
    """)
    initial_link = entry.get()
    search_link = second_entry.get()
    if search_link:
        r = requests.get(initial_link + f"q-{search_link}/")
        parsing = r.text
    else:
        r = requests.get(initial_link)
        parsing = r.text

    soup = BeautifulSoup(parsing,"html.parser")
    get_texts = soup.select("div.css-u2ayx9 > a,.css-1wxaaza,.css-1mwdrlh,.css-13afqrm")

    name = ""
    price = ""
    link = ""
    address = ""

    for i in get_texts:
        try:

            if i.get("class") == ["css-z3gu2d"]:
                link = "https://www.olx.uz" + i.get("href")

            elif i.get("class") == ["css-1wxaaza"]:
                name = i.text

            elif i.get("class") == ["css-1mwdrlh"]:
                address = i.text

            elif i.get("class") == ["css-13afqrm"]:
                price = i.text
            

            if name and price and link and address:
                cursor.execute("INSERT INTO parser (Названия,Цена,Ссылка,Адресс) VALUES(?,?,?,?)",(name,price,link,address))
                db.commit()

                name,price,link,address = "","","",""
        except Exception:
            second_entry.delete(0,tk.END)
            success_label.config(text="Произошла ошибка при парсинге")

    second_entry.delete(0,tk.END)
    success_label.config(text="Вы успешно сохранили данные в базу данных")

    db.close()



root = tk.Tk()
root.title("Parser Olx")
root.geometry("800x800")
root.config(bg="#2c3e50")  


header_font = font.Font(family="Helvetica", size=18, weight="bold")
label_font = font.Font(family="Arial", size=12)
entry_font = font.Font(family="Arial", size=10)


label = tk.Label(
    root, text="Olx", font=header_font, fg="#ecf0f1", bg="#2c3e50"
)
label.pack(pady=(10, 5))


entry = tk.Entry(root, font=entry_font, fg="#34495e", width=40, justify="center")
entry.pack(pady=5)
entry.insert(0, "https://www.olx.uz/oz/list/")
entry.config(state="readonly")


second_label = tk.Label(
    root, text="Поиск товаров", font=label_font, fg="#ecf0f1", bg="#2c3e50"
)
second_label.pack(pady=(15, 5))


second_entry = tk.Entry(root, font=entry_font, width=40, fg="#34495e", justify="center")
second_entry.pack(pady=5)


success_label = tk.Label(
    root, text="", fg="green", bg="#2c3e50", font=label_font
)
success_label.pack(pady=(10, 5))


button = tk.Button(
    root, text="Подтвердить", font=label_font, bg="#3498db", fg="white",
    activebackground="#2980b9", activeforeground="white", command=lambda: get_link()
)
button.pack(pady=(20, 10), ipadx=10, ipady=5)

show_button = tk.Button(
    root,text="Показать данные",font=label_font,bg="#3498db",fg="green",
    activebackground="#2980b9",activeforeground="white" ,command=show_data
    )
show_button.pack(pady=(20,10),ipadx=10,ipady=5)

root.mainloop()

