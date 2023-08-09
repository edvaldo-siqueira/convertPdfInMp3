import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import fitz
from gtts import gTTS
import threading

class PdfToAudioConverter(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Conversor de PDF para Áudio")
        self.geometry("600x600")
        self.configure(bg="white")

        self.pdf_file_path = ""
        self.output_file_path = ""

        self.label = tk.Label(self, text="Selecione um arquivo PDF:", bg="white", fg="black")
        self.label.pack(pady=10)

        self.select_button = tk.Button(self, text="Selecionar PDF", command=self.select_pdf, bg="lightblue", fg="black", padx=10, pady=5, relief=tk.RIDGE, borderwidth=2, cursor="hand2")
        self.select_button.pack()

        self.progress_bar = ttk.Progressbar(self, mode='determinate', length=600)
        self.progress_bar.pack(fill='x', padx=20, pady=(10, 0))

        self.percentage_label = tk.Label(self, text="0%", bg="white", fg="black")
        self.percentage_label.pack()

        self.convert_button = tk.Button(self, text="Converter para Áudio", command=self.convert_to_audio, bg="lightgreen", fg="black", padx=10, pady=5, relief=tk.RIDGE, borderwidth=2, cursor="hand2")
        self.convert_button.pack(pady=10)

    def select_pdf(self):
        self.pdf_file_path = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if self.pdf_file_path:
            self.label.config(text="PDF selecionado: " + self.pdf_file_path)

    def update_progress(self, current, total):
        percentage = int((current / total) * 100)
        self.progress_bar['value'] = percentage
        self.percentage_label.config(text=f"{percentage}%")
        if percentage == 100:
            self.label.config(text="Conversão concluída!\nArquivo de saída: " + self.output_file_path)

    def convert_to_audio(self):
        if not self.pdf_file_path:
            self.label.config(text="Por favor, selecione um arquivo PDF.")
            return

        self.output_file_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("Arquivos MP3", "*.mp3")])
        if self.output_file_path:
            self.convert_button.config(state="disabled")

            def conversion_thread():
                pdf_document = fitz.open(self.pdf_file_path)
                text = ""
                total_pages = pdf_document.page_count
                current_page = 0
                for page_num in range(total_pages):
                    page = pdf_document[page_num]
                    text += page.get_text("text")

                    current_page += 1
                    self.update_progress(current_page, total_pages)

                audio_text = gTTS(text, lang="pt-br", slow=False)  # Definindo slow como False
                audio_text.save(self.output_file_path)
                pdf_document.close()

                self.label.config(text="Conversão concluída!\nArquivo de saída: " + self.output_file_path)
                self.convert_button.config(state="normal")

            self.progress_bar['value'] = 0
            self.percentage_label.config(text="0%")
            threading.Thread(target=conversion_thread).start()

if __name__ == "__main__":
    app = PdfToAudioConverter()
    app.mainloop()
