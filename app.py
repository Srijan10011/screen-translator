import tkinter as tk
from tkinter import ttk, messagebox
from langdetect import detect, LangDetectException
from screenshot import capture_region
from ocr import extract_text
from translate import translate_text


class ScreenTranslatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screen Translator")
        self.geometry("650x500")
        self.configure(padx=15, pady=15)

        # Language options
        self.languages = {
            "English": "en",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Chinese (Simplified)": "zh-cn",
            "Japanese": "ja",
            "Korean": "ko"
        }

        self.create_widgets()

    def create_widgets(self):
        # --- Top Section: Select Region Button ---
        top_frame = ttk.Frame(self)
        top_frame.pack(fill="x", pady=(0, 10))

        self.select_btn = ttk.Button(top_frame, text="Select Region & Translate", command=self.on_select_region)
        self.select_btn.pack()

        # --- OCR Text Section ---
        ocr_frame = ttk.LabelFrame(self, text="Extracted OCR Text (editable)")
        ocr_frame.pack(fill="both", expand=False, pady=(0, 10))

        self.ocr_text_box = tk.Text(ocr_frame, height=6, wrap="word")
        self.ocr_text_box.pack(fill="both", expand=True, padx=10, pady=5)

        # Detected Language Label
        self.detected_lang_label = ttk.Label(self, text="Detected language: Unknown", foreground="gray")
        self.detected_lang_label.pack(anchor="w", pady=(0, 10))

        # --- Language Selection & Translate ---
        lang_frame = ttk.Frame(self)
        lang_frame.pack(fill="x", pady=(0, 10))

        ttk.Label(lang_frame, text="Translate to:").pack(side="left")
        self.lang_var = tk.StringVar(value="English")
        self.lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var,
                                       values=list(self.languages.keys()), state="readonly", width=20)
        self.lang_combo.pack(side="left", padx=10)

        # Spacer
        ttk.Label(lang_frame, text="").pack(side="left", expand=True)

        # Copy Button Placeholder
        self.copy_btn = ttk.Button(lang_frame, text="Copy Translated Text", command=self.copy_translated_text)
        self.copy_btn.pack(side="right")

        # --- Translated Text Section ---
        translated_frame = ttk.LabelFrame(self, text="Translated Text")
        translated_frame.pack(fill="both", expand=True)

        self.translated_text_box = tk.Text(translated_frame, height=6, wrap="word")
        self.translated_text_box.pack(fill="both", expand=True, padx=10, pady=5)

    def on_select_region(self):
        self.ocr_text_box.delete("1.0", tk.END)
        self.translated_text_box.delete("1.0", tk.END)
        self.detected_lang_label.config(text="Detected language: Unknown")

        try:
            img = capture_region()
            if img is None:
                messagebox.showinfo("Cancelled", "Region selection cancelled.")
                return

            extracted_text = extract_text(img)
            if not extracted_text.strip():
                messagebox.showinfo("No Text Found", "No text could be extracted from the selected region.")
                return

            self.ocr_text_box.insert(tk.END, extracted_text)

            try:
                detected_code = detect(extracted_text)
                detected_name = next((name for name, code in self.languages.items()
                                      if code.startswith(detected_code)), detected_code)
            except LangDetectException:
                detected_name = "Unknown"

            self.detected_lang_label.config(text=f"Detected language: {detected_name}")

            target_lang = self.languages[self.lang_var.get()]
            translated = translate_text(extracted_text, target_lang)
            self.translated_text_box.insert(tk.END, translated)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{e}")

    def copy_translated_text(self):
        translated = self.translated_text_box.get("1.0", tk.END).strip()
        if translated:
            self.clipboard_clear()
            self.clipboard_append(translated)
            messagebox.showinfo("Copied", "Translated text copied to clipboard!")
        else:
            messagebox.showwarning("No Text", "There is no translated text to copy.")


if __name__ == "__main__":
    app = ScreenTranslatorApp()
    app.mainloop()
