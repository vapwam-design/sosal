import tkinter as tk
from tkinter import ttk, messagebox
import json
import datetime

# Глобальный список записей
records = []

# Загрузка данных из файла при запуске
def load_from_file():
    global records
    try:
        with open("weather_data.json", "r", encoding="utf-8") as f:
            records = json.load(f)
    except FileNotFoundError:
        records = []

# Сохранение данных в файл
def save_to_file():
    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Сохранено", "Данные успешно сохранены в weather_data.json")

# Очистка поля ввода
def clear_entries():
    entry_date.delete(0, tk.END)
    entry_temp.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    var_rain.set(False)

# Добавление записи
def add_record():
    date_str = entry_date.get().strip()
    temp_str = entry_temp.get().strip()
    desc = entry_desc.get().strip()
    rain = var_rain.get()

    # Проверка даты
    try:
        datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Некорректный формат даты. Используйте ГГГГ-ММ-ДД.")
        return

    # Проверка температуры
    try:
        temp = float(temp_str)
    except ValueError:
        messagebox.showerror("Ошибка", "Температура должна быть числом.")
        return

    # Проверка описания
    if not desc:
        messagebox.showerror("Ошибка", "Заполните описание погоды.")
        return

    record = {
        "date": date_str,
        "temperature": temp,
        "description": desc,
        "rain": rain
    }
    records.append(record)
    messagebox.showinfo("Успех", "Запись добавлена.")
    clear_entries()

    # Обновление таблицы
    update_treeview()

# Обновление таблицы для отображения всех записей
def update_treeview(filtered_records=None):
    for item in tree.get_children():
        tree.delete(item)
    to_show = filtered_records if filtered_records is not None else records
    for rec in to_show:
        tree.insert("", "end", values=(
            rec["date"],
            rec["temperature"],
            rec["description"],
            "Да" if rec["rain"] else "Нет"
        ))

# Фильтрация записей
def apply_filter():
    date_filter = filter_date_entry.get().strip()
    temp_filter = filter_temp_entry.get().strip()

    filtered = records
    if date_filter:
        filtered = [r for r in filtered if r['date'] == date_filter]
    if temp_filter:
        try:
            temp_threshold = float(temp_filter)
            filtered = [r for r in filtered if r['temperature'] > temp_threshold]
        except ValueError:
            messagebox.showerror("Ошибка", "Некорректный фильтр по температуре.")
            return
    update_treeview(filtered)

# Основной код
load_from_file()

root = tk.Tk()
root.title("Weather Diary")
root.geometry("700x600")

# Ввод данных
frame_input = tk.Frame(root)
frame_input.pack(padx=10, pady=10)

tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="e")
entry_date = tk.Entry(frame_input)
entry_date.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Температура (°C):").grid(row=1, column=0, sticky="e")
entry_temp = tk.Entry(frame_input)
entry_temp.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Описание погоды:").grid(row=2, column=0, sticky="e")
entry_desc = tk.Entry(frame_input, width=50)
entry_desc.grid(row=2, column=1, padx=5, pady=5)

var_rain = tk.BooleanVar()
check_rain = tk.Checkbutton(frame_input, text="Осадки", variable=var_rain)
check_rain.grid(row=3, column=1, sticky="w", pady=5)

# Кнопка добавления
btn_add = tk.Button(root, text="Добавить запись", command=add_record)
btn_add.pack(pady=5)

# Таблица для отображения записей
columns = ("date", "temperature", "description", "rain")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("date", text="Дата")
tree.heading("temperature", text="Температура")
tree.heading("description", text="Описание")
tree.heading("rain", text="Осадки")
tree.pack(padx=10, pady=10, fill="both", expand=True)

update_treeview()

# Фильтры
filter_frame = tk.LabelFrame(root, text="Фильтры")
filter_frame.pack(padx=10, pady=10, fill="x")

tk.Label(filter_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=5, pady=5)
filter_date_entry = tk.Entry(filter_frame)
filter_date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(filter_frame, text="Температура > :").grid(row=0, column=2, padx=5, pady=5)
filter_temp_entry = tk.Entry(filter_frame)
filter_temp_entry.grid(row=0, column=3, padx=5, pady=5)

btn_filter = tk.Button(filter_frame, text="Фильтровать", command=apply_filter)
btn_filter.grid(row=0, column=4, padx=10, pady=5)

# Кнопки сохранить/загрузить
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=10)

btn_save = tk.Button(buttons_frame, text="Сохранить в файл", command=save_to_file)
btn_save.grid(row=0, column=0, padx=10)

btn_load = tk.Button(buttons_frame, text="Загрузить из файла", command=lambda: [load_from_file(), update_treeview()])
btn_load.grid(row=0, column=1, padx=10)

# Запуск главного цикла
root.mainloop()