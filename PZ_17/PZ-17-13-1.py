#Ссылка из 11 варианта https://smashinghub.com/wp-content/uploads/2011/08/html5-forums-14.jpg
import tkinter as tk
from tkinter import ttk, messagebox

class RegistrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Registration Form")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        self.root.configure(bg="grey")  # Серый фон

        # Стиль
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 10), background="grey")
        self.style.configure("TButton", font=("Arial", 10, "bold"))
        self.style.configure("TFrame", background="grey")

        # Основной контейнер
        self.main_frame = ttk.Frame(self.root, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Заголовок
        header = ttk.Label(
            self.main_frame,
            text="Contact Us",
            font=("Arial", 18, "bold"),
            foreground="#2c3e50"
        )
        header.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Создание полей формы с метками сверху
        fields = [
            ("First Name", "text"),
            ("Last Name", "text"),
            ("Email", "text"),
            ("Website", "text"),
            ("Password", "password"),
            ("Confirm Password", "password")
        ]

        self.entries = {}
        for i, (field, field_type) in enumerate(fields, start=1):
            # Метка над полем
            label = ttk.Label(
                self.main_frame,
                text=field,
                font=("Arial", 9, "bold"),
                foreground="#34495e"
            )
            label.grid(row=i, column=0, sticky=tk.W, pady=(30, 0))

            # Поле ввода
            show_char = "*" if field_type == "password" else None
            entry = ttk.Entry(
                self.main_frame,
                width=40,
                font=("Arial", 10),
                show=show_char
            )
            entry.grid(row=i + 1, column=0, sticky=tk.EW, pady=(0, 10))

            # Сохраняем ссылку на поле
            self.entries[field] = entry

        # Checkbox
        self.terms_var = tk.IntVar()
        terms_frame = ttk.Frame(self.main_frame)
        terms_frame.grid(row=len(fields) * 2 + 1, column=0, sticky=tk.W, pady=(10, 0))

        # Кнопка регистрации
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.grid(row=len(fields) * 2 + 2, column=0, pady=20)

        ttk.Button(
            btn_frame,
            text="Sign Up",
            command=self.register,
            style="TButton",
            width=20
        ).pack(pady=10)

    def register(self):
        # Получаем данные из полей
        first_name = self.entries["First Name"].get().strip()
        last_name = self.entries["Last Name"].get().strip()
        email = self.entries["Email"].get().strip()
        website = self.entries["Website"].get().strip()
        password = self.entries["Password"].get().strip()
        confirm_password = self.entries["Confirm Password"].get().strip()

        # Валидация
        errors = []
        if not first_name:
            errors.append("First Name is required")
            self.highlight_error(self.entries["First Name"])

        if not last_name:
            errors.append("Last Name is required")
            self.highlight_error(self.entries["Last Name"])

        if not email:
            errors.append("Email is required")
            self.highlight_error(self.entries["Email"])
        elif "@" not in email or "." not in email:
            errors.append("Please enter a valid email address")
            self.highlight_error(self.entries["Email"])

        if not password:
            errors.append("Password is required")
            self.highlight_error(self.entries["Password"])
        elif len(password) < 6:
            errors.append("Password must be at least 6 characters")
            self.highlight_error(self.entries["Password"])

        if password != confirm_password:
            errors.append("Passwords do not match")
            self.highlight_error(self.entries["Confirm Password"])

        if errors:
            messagebox.showerror("Registration Error", "\n".join(errors))
            return

        # Если все проверки пройдены
        messagebox.showinfo("Success", "Registration successful!\n\n"
                                       f"Name: {first_name} {last_name}\n"
                                       f"Email: {email}\n"
                                       f"Website: {website or 'Not provided'}")
        self.clear_form()

    def highlight_error(self, entry):
        """Подсвечивает поле с ошибкой"""
        entry.configure(foreground='red')
        entry.after(3000, lambda: entry.configure(foreground='black'))

    def clear_form(self):
        """Очищает все поля формы"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.terms_var.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrationApp(root)
    root.mainloop()