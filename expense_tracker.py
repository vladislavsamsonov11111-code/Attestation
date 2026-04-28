import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker - Трекер расходов")
        self.root.geometry("1100x650")
        
        self.data_file = "expenses.json"
        self.expenses = []
        self.load_data()
        
        self.setup_ui()
        self.refresh_table()
        self.update_summary()
        
    def load_data(self):
        """Загрузка данных из JSON файла"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.expenses = json.load(f)
            except:
                self.expenses = []
        else:
            self.expenses = []
    
    def save_data(self):
        """Сохранение данных в JSON файл"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=4)
    
    def setup_ui(self):
        """Настройка интерфейса"""
        # Основной контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # === Панель ввода данных ===
        input_frame = ttk.LabelFrame(main_frame, text="Добавление расхода", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Сумма
        ttk.Label(input_frame, text="Сумма (₽):").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.amount_entry = ttk.Entry(input_frame, width=15)
        self.amount_entry.grid(row=0, column=1, padx=(0, 20))
        
        # Категория
        ttk.Label(input_frame, text="Категория:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.category_var = tk.StringVar()
        categories = ["Еда", "Транспорт", "Развлечения", "Жильё", "Здоровье", "Одежда", "Другое"]
        self.category_combo = ttk.Combobox(input_frame, textvariable=self.category_var, values=categories, width=15)
        self.category_combo.grid(row=0, column=3, padx=(0, 20))
        self.category_combo.set("Еда")
        
        # Дата (обычное поле ввода)
        ttk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        self.date_entry = ttk.Entry(input_frame, width=12)
        self.date_entry.grid(row=0, column=5, padx=(0, 20))
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))
        
        # Кнопка добавления
        ttk.Button(input_frame, text="➕ Добавить расход", command=self.add_expense).grid(row=0, column=6)
        
        # === Панель фильтров ===
        filter_frame = ttk.LabelFrame(main_frame, text="Фильтрация", padding="10")
        filter_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Фильтр по категории
        ttk.Label(filter_frame, text="Категория:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.filter_category_var = tk.StringVar()
        self.filter_category_combo = ttk.Combobox(filter_frame, textvariable=self.filter_category_var, 
                                                   values=["Все"] + categories, width=15)
        self.filter_category_combo.grid(row=0, column=1, padx=(0, 20))
        self.filter_category_combo.set("Все")
        
        # Фильтр по дате "от"
        ttk.Label(filter_frame, text="Дата от (ДД.ММ.ГГГГ):").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.date_from = ttk.Entry(filter_frame, width=12)
        self.date_from.grid(row=0, column=3, padx=(0, 20))
        
        # Фильтр по дате "до"
        ttk.Label(filter_frame, text="Дата до (ДД.ММ.ГГГГ):").grid(row=0, column=4, sticky=tk.W, padx=(0, 10))
        self.date_to = ttk.Entry(filter_frame, width=12)
        self.date_to.grid(row=0, column=5, padx=(0, 20))
        
        # Кнопка фильтрации
        ttk.Button(filter_frame, text="🔍 Применить фильтр", command=self.apply_filter).grid(row=0, column=6, padx=(0, 10))
        ttk.Button(filter_frame, text="🔄 Сбросить", command=self.reset_filter).grid(row=0, column=7)
        
        # === Таблица с расходами ===
        table_frame = ttk.LabelFrame(main_frame, text="Список расходов", padding="10")
        table_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Создание таблицы с прокруткой
        columns = ("ID", "Дата", "Категория", "Сумма (₽)")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Настройка колонок
        self.tree.heading("ID", text="ID")
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Сумма (₽)", text="Сумма (₽)")
        
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Дата", width=120, anchor="center")
        self.tree.column("Категория", width=150, anchor="center")
        self.tree.column("Сумма (₽)", width=120, anchor="e")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Контекстное меню для удаления
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="🗑️ Удалить запись", command=self.delete_selected)
        self.tree.bind("<Button-3>", self.show_context_menu)
        
        # === Панель статистики ===
        stats_frame = ttk.LabelFrame(main_frame, text="Статистика", padding="10")
        stats_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Label(stats_frame, text="Общая сумма расходов:", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=(0, 20))
        self.total_label = ttk.Label(stats_frame, text="0 ₽", font=("Arial", 16, "bold"), foreground="red")
        self.total_label.grid(row=0, column=1, padx=(0, 40))
        
        ttk.Label(stats_frame, text="Количество записей:", font=("Arial", 11)).grid(row=0, column=2, padx=(0, 20))
        self.count_label = ttk.Label(stats_frame, text="0", font=("Arial", 14))
        self.count_label.grid(row=0, column=3)
        
        # Кнопки управления
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=2, pady=(15, 0))
        ttk.Button(control_frame, text="📊 Подсчёт за период", command=self.show_period_summary).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(control_frame, text="🗑️ Удалить все", command=self.delete_all).pack(side=tk.LEFT)
        
        # Настройка весов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)
        table_frame.rowconfigure(0, weight=1)
        
    def validate_amount(self, amount_str):
        """Проверка корректности суммы"""
        try:
            amount = float(amount_str)
            if amount <= 0:
                return False, "Сумма должна быть положительным числом!"
            return True, amount
        except ValueError:
            return False, "Введите корректное число!"
    
    def validate_date(self, date_str):
        """Проверка корректности даты (формат ДД.ММ.ГГГГ)"""
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            return True, date_str
        except ValueError:
            return False, "Неверный формат даты! Используйте ДД.ММ.ГГГГ (например, 15.04.2026)"
    
    def add_expense(self):
        """Добавление нового расхода"""
        amount_str = self.amount_entry.get().strip()
        category = self.category_var.get()
        date = self.date_entry.get().strip()
        
        # Валидация суммы
        is_valid, amount_or_error = self.validate_amount(amount_str)
        if not is_valid:
            messagebox.showerror("Ошибка", amount_or_error)
            return
        
        # Валидация даты
        is_valid, date_or_error = self.validate_date(date)
        if not is_valid:
            messagebox.showerror("Ошибка", date_or_error)
            return
        
        # Создание записи
        expense = {
            "id": len(self.expenses) + 1,
            "amount": round(amount_or_error, 2),
            "category": category,
            "date": date_or_error
        }
        
        self.expenses.append(expense)
        self.save_data()
        self.refresh_table()
        self.update_summary()
        
        # Очистка поля суммы
        self.amount_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", "Расход успешно добавлен!")
    
    def refresh_table(self, expenses_list=None):
        """Обновление таблицы"""
        # Очищаем таблицу
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Если список не передан, используем все расходы
        if expenses_list is None:
            expenses_list = self.expenses
        
        # Заполняем таблицу
        for expense in expenses_list:
            self.tree.insert("", tk.END, values=(
                expense["id"],
                expense["date"],
                expense["category"],
                f"{expense['amount']:.2f} ₽"
            ))
    
    def apply_filter(self):
        """Применение фильтров"""
        filtered = self.expenses.copy()
        
        # Фильтр по категории
        category_filter = self.filter_category_var.get()
        if category_filter != "Все":
            filtered = [e for e in filtered if e["category"] == category_filter]
        
        # Фильтр по дате
        date_from_str = self.date_from.get().strip()
        date_to_str = self.date_to.get().strip()
        
        if date_from_str and date_to_str:
            try:
                from_date = datetime.strptime(date_from_str, "%d.%m.%Y")
                to_date = datetime.strptime(date_to_str, "%d.%m.%Y")
                
                filtered = [
                    e for e in filtered
                    if from_date <= datetime.strptime(e["date"], "%d.%m.%Y") <= to_date
                ]
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты в фильтре! Используйте ДД.ММ.ГГГГ")
                return
        
        self.refresh_table(filtered)
        self.update_summary(filtered)
        
        if filtered:
            total = sum(e["amount"] for e in filtered)
            messagebox.showinfo("Результат фильтрации", 
                               f"Найдено записей: {len(filtered)}\nОбщая сумма: {total:.2f} ₽")
    
    def reset_filter(self):
        """Сброс фильтров"""
        self.filter_category_combo.set("Все")
        self.date_from.delete(0, tk.END)
        self.date_to.delete(0, tk.END)
        self.refresh_table()
        self.update_summary()
    
    def update_summary(self, expenses_list=None):
        """Обновление статистики"""
        if expenses_list is None:
            expenses_list = self.expenses
        
        total = sum(e["amount"] for e in expenses_list)
        count = len(expenses_list)
        
        self.total_label.config(text=f"{total:.2f} ₽")
        self.count_label.config(text=str(count))
    
    def show_period_summary(self):
        """Подсчёт суммы за выбранный период"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Подсчёт за период")
        dialog.geometry("400x280")
        dialog.resizable(False, False)
        
        # Центрирование окна
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Выберите период для подсчёта", font=("Arial", 12, "bold")).pack(pady=15)
        
        frame = ttk.Frame(dialog, padding="10")
        frame.pack()
        
        ttk.Label(frame, text="Дата от (ДД.ММ.ГГГГ):").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        date_from = ttk.Entry(frame, width=15)
        date_from.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame, text="Дата до (ДД.ММ.ГГГГ):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        date_to = ttk.Entry(frame, width=15)
        date_to.grid(row=1, column=1, padx=5, pady=5)
        
        result_label = ttk.Label(dialog, text="", font=("Arial", 11))
        result_label.pack(pady=15)
        
        def calculate():
            from_str = date_from.get().strip()
            to_str = date_to.get().strip()
            
            if not from_str or not to_str:
                messagebox.showerror("Ошибка", "Заполните оба поля даты!")
                return
            
            try:
                from_date = datetime.strptime(from_str, "%d.%m.%Y")
                to_date = datetime.strptime(to_str, "%d.%m.%Y")
                
                filtered = [
                    e for e in self.expenses
                    if from_date <= datetime.strptime(e["date"], "%d.%m.%Y") <= to_date
                ]
                
                total = sum(e["amount"] for e in filtered)
                
                result_text = f"Общая сумма: {total:.2f} ₽\n"
                result_text += f"Количество записей: {len(filtered)}\n"
                
                if filtered:
                    result_text += f"\nСредний чек: {total/len(filtered):.2f} ₽"
                
                result_label.config(text=result_text)
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ДД.ММ.ГГГГ")
        
        ttk.Button(dialog, text="📊 Подсчитать", command=calculate).pack(pady=10)
        
        # Пример заполнения текущей датой
        today = datetime.now().strftime("%d.%m.%Y")
        date_from.insert(0, today)
        date_to.insert(0, today)
    
    def delete_selected(self):
        """Удаление выбранной записи"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления!")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить выбранную запись?"):
            # Получаем ID записи
            item = self.tree.item(selected[0])
            expense_id = item["values"][0]
            
            # Удаляем из списка
            self.expenses = [e for e in self.expenses if e["id"] != expense_id]
            
            # Перенумеровка ID
            for i, expense in enumerate(self.expenses, 1):
                expense["id"] = i
            
            self.save_data()
            self.refresh_table()
            self.update_summary()
            messagebox.showinfo("Успех", "Запись удалена!")
    
    def delete_all(self):
        """Удаление всех записей"""
        if not self.expenses:
            messagebox.showinfo("Информация", "Нет записей для удаления!")
            return
        
        if messagebox.askyesno("Подтверждение", "Удалить ВСЕ записи? Это действие необратимо!"):
            self.expenses = []
            self.save_data()
            self.refresh_table()
            self.update_summary()
            messagebox.showinfo("Успех", "Все записи удалены!")
    
    def show_context_menu(self, event):
        """Показ контекстного меню"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
