import tkinter as tk
from tkinter import ttk, messagebox


class EnglishRussianDictionary:
    def __init__(self, root):
        self.result_text = None
        self.root = root
        self.root.title("Русско-английский словарь")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        # Словарь с 10 словами
        self.dictionary = {
            "привет": "hello",
            "мир": "world",
            "дом": "house",
            "кот": "cat",
            "собака": "dog",
            "книга": "book",
            "солнце": "sun",
            "вода": "water",
            "яблоко": "apple",
            "машина": "car"
        }

        # Стиль
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TButton", font=("Arial", 12))

        # Основной интерфейс
        self.create_widgets()

    def create_widgets(self):
        # Фрейм для ввода
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(fill=tk.X)

        ttk.Label(input_frame, text="Введите русское слово:").pack(side=tk.LEFT)

        self.word_entry = ttk.Entry(input_frame, width=20, font=("Arial", 12))
        self.word_entry.pack(side=tk.LEFT, padx=10)
        self.word_entry.bind("<Return>", self.translate_word)

        # Кнопка перевода
        translate_btn = ttk.Button(
            input_frame,
            text="Перевести",
            command=self.translate_word
        )
        translate_btn.pack(side=tk.LEFT)

        # Фрейм для результата
        result_frame = ttk.Frame(self.root, padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(result_frame, text="Результат перевода:").pack(anchor=tk.W)

        self.result_text = tk.Text(
            result_frame,
            height=5,
            width=50,
            font=("Arial", 12),
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.result_text.pack(pady=5)

        # Фрейм для кнопок
        button_frame = ttk.Frame(self.root, padding=10)
        button_frame.pack(fill=tk.X)

        # Кнопка показа всех слов
        show_all_btn = ttk.Button(
            button_frame,
            text="Показать все слова",
            command=self.show_all_words
        )
        show_all_btn.pack(side=tk.LEFT, padx=5)

        # Кнопка очистки
        clear_btn = ttk.Button(
            button_frame,
            text="Очистить",
            command=self.clear_results
        )
        clear_btn.pack(side=tk.LEFT)

    def translate_word(self, event=None):
        word = self.word_entry.get().strip().lower()

        if not word:
            messagebox.showwarning("Ошибка", "Введите слово для перевода")
            return

        if word in self.dictionary:
            translation = self.dictionary[word]
            self.display_result(f"{word} → {translation}")
        else:
            self.display_result(f"Слово '{word}' не найдено в словаре")

    def show_all_words(self):
        all_words = "Все слова в словаре:\n\n"
        for rus, eng in sorted(self.dictionary.items()):
            all_words += f"{rus:10} → {eng}\n"

        self.display_result(all_words)

    def display_result(self, text):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.result_text.config(state=tk.DISABLED)

    def clear_results(self):
        self.word_entry.delete(0, tk.END)
        self.display_result("")


if __name__ == "__main__":
    root = tk.Tk()
    app = EnglishRussianDictionary(root)
    root.mainloop()