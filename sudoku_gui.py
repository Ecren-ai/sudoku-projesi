import tkinter as tk
from tkinter import *
from tkinter import messagebox
from SudokuApp import Sudoku  
import pickle
import os

class SudokuGiris:
    def __init__(self, root):
        self.root = root
        self.sudoku_app = Sudoku()
        self.root.resizable(False,False)
        self.root.title("Sudoku Giriş")
        self.root.geometry("800x700")
        self.root.configure(bg="#FFE4E1")  # Daha soft bir pembe tonu

        # Ana başlık
        title_frame = tk.Frame(root, bg="#FFE4E1")
        title_frame.pack(pady=40)
        
        self.label = tk.Label(title_frame, 
                            text="♠ Sudoku Oyununa ♠ \n  Hoş Geldiniz! ",
                            bg="#FFE4E1", 
                            fg="#800080",  # Mor renk
                            font=("Trebuchet MS", 32, "bold"))
        self.label.pack()

        # Zorluk seviyesi frame
        difficulty_frame = tk.Frame(root, bg="#FFE4E1")
        difficulty_frame.pack(pady=30)

        self.zorluk_label = tk.Label(difficulty_frame, 
                                   text="✧ Zorluk Seviyesi ✧",
                                   bg="#FFE4E1", 
                                   fg="#800080",
                                   font=("Verdana", 18))
        self.zorluk_label.pack(pady=10)
        
        self.zorluk_seviyesi = tk.StringVar()
        self.zorluk_seviyesi.set("Kolay")

        # Özelleştirilmiş OptionMenu
        self.zorluk_menu = tk.OptionMenu(difficulty_frame, 
                                       self.zorluk_seviyesi, 
                                       "Kolay", "Orta", "Zor", "Expert")
        self.zorluk_menu.config(width=20, 
                              font=("Verdana", 12),
                              bg="#FFB6C1",  # Açık pembe
                              activebackground="#FF69B4")  # Koyu pembe
        self.zorluk_menu.pack(pady=15)

        # Butonlar frame
        button_frame = tk.Frame(root, bg="#FFE4E1")
        button_frame.pack(pady=30)

        # Buton stilleri
        button_style = {
            'font': ("Arial", 16, "bold"),
            'width': 20,
            'height': 2,
            'bd': 0,
            'borderwidth': 0,
            'relief': "ridge",
            'cursor': "hand2"
        }

        self.basla_buton = tk.Button(button_frame, 
                                    text="✦ Yeni Oyun ✦",
                                    bg="#DDA0DD",  # Mor-pembe
                                    activebackground="#BA55D3",
                                    fg="white",
                                    command=self.oyunu_baslat,
                                    **button_style)
        self.basla_buton.pack(pady=10)

        self.devam_et_buton = tk.Button(button_frame, 
                                       text="✧ Devam Et ✧",
                                       bg="#DDA0DD",
                                       activebackground="#BA55D3",
                                       fg="white",
                                       command=self.devam_et,
                                       **button_style)
        self.devam_et_buton.pack(pady=10)

        self.kapat_buton = tk.Button(button_frame, 
                                    text="✕ Çıkış ✕",
                                    bg="#DDA0DD",
                                    activebackground="#BA55D3",
                                    fg="white",
                                    command=root.quit,
                                    **button_style)
        self.kapat_buton.pack(pady=10)

        # Hover efektleri
        for button in [self.basla_buton, self.devam_et_buton, self.kapat_buton]:
            button.bind("<Enter>", lambda e, b=button: b.config(bg="#BA55D3"))
            button.bind("<Leave>", lambda e, b=button: b.config(bg="#DDA0DD"))    

    def oyunu_baslat(self):
        zorluk = self.zorluk_seviyesi.get()
        self.root.destroy()
        baslat_oyun(zorluk, self.sudoku_app)

    def devam_et(self):
        if os.path.exists("sudoku_save.pkl"):
            try:
                with open("sudoku_save.pkl", "rb") as f:
                    save_data = pickle.load(f)
                    
                self.root.destroy()
                baslat_oyun_kaydedilmis(save_data)
            except Exception as e:
                messagebox.showerror("Hata", f"Kaydedilmiş oyun yüklenirken bir hata oluştu: {str(e)}")
        else:
            messagebox.showinfo("Bilgi", "Kaydedilmiş oyun bulunamadı.")


# Sudoku oyununun ana penceresini açan fonksiyon
def baslat_oyun(zorluk, sudoku_app):
    oyun_pencere = tk.Tk()
    oyun_pencere.title(f"Sudoku - {zorluk} Seviye")
    oyun_pencere.geometry("800x800")
    oyun_pencere.configure(bg="#FFE4E1")
    oyun_pencere.resizable(False, False)

    # Ana frame
    main_frame = tk.Frame(oyun_pencere, bg="#FFE4E1", pady=20)
    main_frame.pack(expand=True)
    
    # Başlık
    title_label = tk.Label(main_frame, 
                          text=f"♠ {zorluk} Seviye ♠",
                          bg="#FFE4E1",
                          fg="#800080",
                          font=("Trebuchet MS", 24, "bold"))
    title_label.pack(pady=20)

    # Sudoku tahtası frame
    board_frame = tk.Frame(main_frame, 
                          bg="#DDA0DD",
                          bd=2, 
                          relief="solid")
    board_frame.pack(padx=20, pady=20)

    def validate_input(P):
        return P == "" or (P.isdigit() and 1 <= int(P) <= 9)

    def check_cell_value(entry, i, j):
        value = entry.get()
        if value.isdigit():
            num = int(value)
            if zorluk == "Kolay":  # Sadece kolay modda renk kontrolü
                temp_val = sudoku_app.board[i][j]
                sudoku_app.board[i][j] = 0
                if not sudoku_app.is_valid(i, j, num):
                    entry.config(fg="red")
                else:
                    entry.config(fg="#800080")
                sudoku_app.board[i][j] = temp_val

    # Sudoku çözümünü kontrol et
    def kontrol_et():
        # Mevcut çözümü al
        current_solution = [[0 for _ in range(9)] for _ in range(9)]
        bos_hucre_var = False
        
        # Tüm hücreleri kontrol et ve current_solution'a doldur
        for i in range(9):
            for j in range(9):
                value = entries[i][j].get()
                
                # Önce tüm hücrelerin arka plan rengini sıfırla
                if entries[i][j]["state"] != "readonly":
                    entries[i][j].config(bg="white")
                
                # Boş hücre kontrolü
                if value == "":
                    bos_hucre_var = True
                    entries[i][j].config(bg="#FFFF99")  # Boş hücreleri sarı ile işaretle
                    continue
                    
                current_solution[i][j] = int(value)
        
        if bos_hucre_var:
            messagebox.showwarning("Uyarı", "Tüm kutucukları doldurunuz!")
            return
            
        # Satır, sütun ve kutu kontrolü
        hatali_hucreler = []
        
        # Satırları kontrol et
        for row in range(9):
            seen_values = {}
            for col in range(9):
                val = current_solution[row][col]
                if val in seen_values:
                    # Bu satırda tekrar eden bir değer var
                    hatali_hucreler.append((row, col))
                    hatali_hucreler.append((row, seen_values[val]))
                else:
                    seen_values[val] = col
                    
        # Sütunları kontrol et
        for col in range(9):
            seen_values = {}
            for row in range(9):
                val = current_solution[row][col]
                if val in seen_values:
                    # Bu sütunda tekrar eden bir değer var
                    hatali_hucreler.append((row, col))
                    hatali_hucreler.append((seen_values[val], col))
                else:
                    seen_values[val] = row
                    
        # 3x3 kutuları kontrol et
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                seen_values = {}
                for row in range(box_row, box_row + 3):
                    for col in range(box_col, box_col + 3):
                        val = current_solution[row][col]
                        if val in seen_values:
                            # Bu kutuda tekrar eden bir değer var
                            r_prev, c_prev = seen_values[val]
                            hatali_hucreler.append((row, col))
                            hatali_hucreler.append((r_prev, c_prev))
                        else:
                            seen_values[val] = (row, col)
        
        # Hatalı hücreleri işaretle
        for row, col in hatali_hucreler:
            if entries[row][col]["state"] != "readonly":
                entries[row][col].config(bg="#FF9999")  # Hatalı hücreleri kırmızı ile işaretle
                
        if hatali_hucreler:
            messagebox.showwarning("Uyarı", "Bazı kutucuklarda hata var!")
        else:
            messagebox.showinfo("Tebrikler", "Sudoku doğru bir şekilde tamamlandı!")
            oyun_pencere.destroy()
            giris_pencere = tk.Tk()
            app = SudokuGiris(giris_pencere)
            giris_pencere.mainloop()

    def oyunu_kaydet(entries, zorluk, sudoku_app):
        current_solution = [[0 for _ in range(9)] for _ in range(9)]
        original_cells = [[False for _ in range(9)] for _ in range(9)]
        
        for i in range(9):
            for j in range(9):
                value = entries[i][j].get()
                if value == "":
                    current_solution[i][j] = 0
                else:
                    current_solution[i][j] = int(value)
                
                # Readonly olan hücreleri işaretle
                if entries[i][j]["state"] == "readonly":
                    original_cells[i][j] = True
        
        save_data = {
            "board": current_solution,
            "zorluk": zorluk,
            "original_cells": original_cells  # Orijinal (değiştirilemez) hücreleri kaydet
        }
        with open("sudoku_save.pkl", "wb") as f:
            pickle.dump(save_data, f)
        messagebox.showinfo("Bilgi", "Oyun başarıyla kaydedildi!")
        oyun_pencere.destroy()
        giris_pencere = tk.Tk()
        app = SudokuGiris(giris_pencere)
        giris_pencere.mainloop()

    entries = []
    vcmd = (oyun_pencere.register(validate_input), '%P')
    
    # Sudoku board'ı doldur
    sudoku_app.fill_board()
    
    if zorluk == "Kolay":
        sudoku_app.clean_boxes_kolay()
    elif zorluk == "Orta":
        sudoku_app.clean_boxes_orta()
    elif zorluk == "Zor":
        sudoku_app.clean_boxes_zor()
    elif zorluk == "Expert":
        sudoku_app.clean_boxes_expert()

    # GUI tahtasını oluştur
    # Önce tüm hücreleri oluştur
    for i in range(9):
        row_entries = []
        for j in range(9):
            cell_frame = tk.Frame(board_frame,
                                bg="#800080" if (i//3 + j//3) % 2 == 0 else "#DDA0DD",
                                padx=1, pady=1)
            cell_frame.grid(row=i, column=j, padx=1, pady=1)
            
            entry = tk.Entry(cell_frame,
                           width=3,
                           font=("Arial", 18, "bold"),
                           justify="center",
                           validate="key",
                           validatecommand=vcmd)
            
            entry.pack(padx=3, pady=3)
            val = sudoku_app.board[i][j]
            
            if val != 0:
                entry.insert(0, str(val))
                entry.config(state="readonly",
                           readonlybackground="#FFB6C1",
                           fg="#800080")
            else:
                entry.config(bg="white", fg="#800080")
                entry.bind("<KeyRelease>", lambda e, entry=entry, i=i, j=j: check_cell_value(entry, i, j))
            
            row_entries.append(entry)
        entries.append(row_entries)

    # Kontrol Et butonu ekle
    kontrol_frame = tk.Frame(main_frame, bg="#FFE4E1")
    kontrol_frame.pack(pady=20)
    
    # Ara ver butonu ekleme
    ara_ver_buton = tk.Button(kontrol_frame,
                            text="⏸ Ara Ver ⏸",
                            bg="#DDA0DD",
                            activebackground="#BA55D3",
                            fg="white",
                            font=("Arial", 16, "bold"),
                            width=20,
                            height=1,
                            bd=0,
                            relief="ridge",
                            cursor="hand2",
                            command=lambda: oyunu_kaydet(entries, zorluk, sudoku_app))
    ara_ver_buton.pack(pady=10)
    
    kontrol_buton = tk.Button(kontrol_frame,
                            text="✓ Kontrol Et ✓",
                            bg="#DDA0DD",
                            activebackground="#BA55D3",
                            fg="white",
                            font=("Arial", 16, "bold"),
                            width=20,
                            height=1,
                            bd=0,
                            relief="ridge",
                            cursor="hand2",
                            command=kontrol_et)
    kontrol_buton.pack()
    
    # Hover efekti
    kontrol_buton.bind("<Enter>", lambda e: kontrol_buton.config(bg="#BA55D3"))
    kontrol_buton.bind("<Leave>", lambda e: kontrol_buton.config(bg="#DDA0DD"))

    oyun_pencere.mainloop()

def baslat_oyun_kaydedilmis(save_data):
    oyun_pencere = tk.Tk()
    zorluk = save_data["zorluk"]
    oyun_pencere.title(f"Sudoku - {zorluk} Seviye (Devam edilen)")
    oyun_pencere.geometry("800x800")
    oyun_pencere.configure(bg="#FFE4E1")
    oyun_pencere.resizable(False, False)

    # Ana frame
    main_frame = tk.Frame(oyun_pencere, bg="#FFE4E1", pady=20)
    main_frame.pack(expand=True)
    
    # Başlık
    title_label = tk.Label(main_frame, 
                          text=f"♠ {zorluk} Seviye (Devam edilen) ♠",
                          bg="#FFE4E1",
                          fg="#800080",
                          font=("Trebuchet MS", 24, "bold"))
    title_label.pack(pady=20)

    # Sudoku tahtası frame
    board_frame = tk.Frame(main_frame, 
                          bg="#DDA0DD",
                          bd=2, 
                          relief="solid")
    board_frame.pack(padx=20, pady=20)

    def validate_input(P):
        return P == "" or (P.isdigit() and 1 <= int(P) <= 9)

    def check_cell_value(entry, i, j):
        value = entry.get()
        if value.isdigit():
            num = int(value)
        
    # Sudoku çözümünü kontrol et
    def kontrol_et():
        # Mevcut çözümü al
        current_solution = [[0 for _ in range(9)] for _ in range(9)]
        bos_hucre_var = False
        
        # Tüm hücreleri kontrol et ve current_solution'a doldur
        for i in range(9):
            for j in range(9):
                value = entries[i][j].get()
                
                # Önce tüm hücrelerin arka plan rengini sıfırla
                if entries[i][j]["state"] != "readonly":
                    entries[i][j].config(bg="white")
                
                # Boş hücre kontrolü
                if value == "":
                    bos_hucre_var = True
                    entries[i][j].config(bg="#FFFF99")  # Boş hücreleri sarı ile işaretle
                    continue
                    
                current_solution[i][j] = int(value)
        
        if bos_hucre_var:
            messagebox.showwarning("Uyarı", "Tüm kutucukları doldurunuz!")
            return
            
        # Satır, sütun ve kutu kontrolü
        hatali_hucreler = []
        
        # Satırları kontrol et
        for row in range(9):
            seen_values = {}
            for col in range(9):
                val = current_solution[row][col]
                if val in seen_values:
                    # Bu satırda tekrar eden bir değer var
                    hatali_hucreler.append((row, col))
                    hatali_hucreler.append((row, seen_values[val]))
                else:
                    seen_values[val] = col
                    
        # Sütunları kontrol et
        for col in range(9):
            seen_values = {}
            for row in range(9):
                val = current_solution[row][col]
                if val in seen_values:
                    # Bu sütunda tekrar eden bir değer var
                    hatali_hucreler.append((row, col))
                    hatali_hucreler.append((seen_values[val], col))
                else:
                    seen_values[val] = row
                    
        # 3x3 kutuları kontrol et
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                seen_values = {}
                for row in range(box_row, box_row + 3):
                    for col in range(box_col, box_col + 3):
                        val = current_solution[row][col]
                        if val in seen_values:
                            # Bu kutuda tekrar eden bir değer var
                            r_prev, c_prev = seen_values[val]
                            hatali_hucreler.append((row, col))
                            hatali_hucreler.append((r_prev, c_prev))
                        else:
                            seen_values[val] = (row, col)
        
        # Hatalı hücreleri işaretle
        for row, col in hatali_hucreler:
            if entries[row][col]["state"] != "readonly":
                entries[row][col].config(bg="#FF9999")  # Hatalı hücreleri kırmızı ile işaretle
                
        if hatali_hucreler:
            messagebox.showwarning("Uyarı", "Bazı kutucuklarda hata var!")
        else:
            messagebox.showinfo("Tebrikler", "Sudoku doğru bir şekilde tamamlandı!")
            oyun_pencere.destroy()
            giris_pencere = tk.Tk()
            app = SudokuGiris(giris_pencere)
            giris_pencere.mainloop()

    def oyunu_kaydet(entries, zorluk, sudoku_app):
        current_solution = [[0 for _ in range(9)] for _ in range(9)]
        original_cells = [[False for _ in range(9)] for _ in range(9)]
        
        for i in range(9):
            for j in range(9):
                value = entries[i][j].get()
                if value == "":
                    current_solution[i][j] = 0
                else:
                    current_solution[i][j] = int(value)
                
                # Readonly olan hücreleri işaretle
                if entries[i][j]["state"] == "readonly":
                    original_cells[i][j] = True
        
        save_data = {
            "board": current_solution,
            "zorluk": zorluk,
            "original_cells": original_cells  # Orijinal (değiştirilemez) hücreleri kaydet
        }
        with open("sudoku_save.pkl", "wb") as f:
            pickle.dump(save_data, f)
        messagebox.showinfo("Bilgi", "Oyun başarıyla kaydedildi!")
        oyun_pencere.destroy()
        giris_pencere = tk.Tk()
        app = SudokuGiris(giris_pencere)
        giris_pencere.mainloop()

    entries = []
    vcmd = (oyun_pencere.register(validate_input), '%P')

    # GUI tahtasını oluştur
    # Önce tüm hücreleri oluştur
    for i in range(9):
        row_entries = []
        for j in range(9):
            cell_frame = tk.Frame(board_frame,
                                bg="#800080" if (i//3 + j//3) % 2 == 0 else "#DDA0DD",
                                padx=1, pady=1)
            cell_frame.grid(row=i, column=j, padx=1, pady=1)
            
            entry = tk.Entry(cell_frame,
                           width=3,
                           font=("Arial", 18, "bold"),
                           justify="center",
                           validate="key",
                           validatecommand=vcmd)
            
            entry.pack(padx=3, pady=3)
            val = save_data["board"][i][j]
            
            if val != 0:
                entry.insert(0, str(val))
                
                # Eğer orijinal hücreyse (kaydedilmiş oyunda readonly olarak işaretlenmişse) readonly yap
                if "original_cells" in save_data and save_data["original_cells"][i][j]:
                    entry.config(state="readonly",
                               readonlybackground="#FFB6C1",
                               fg="#800080")
                else:
                    entry.config(bg="white", fg="#800080")
            else:
                entry.config(bg="white", fg="#800080")
            
            row_entries.append(entry)
        entries.append(row_entries)

    # Kontrol Et butonu ekle
    kontrol_frame = tk.Frame(main_frame, bg="#FFE4E1")
    kontrol_frame.pack(pady=20)
    
    # Ara ver butonu ekleme
    ara_ver_buton = tk.Button(kontrol_frame,
                            text="⏸ Ara Ver ⏸",
                            bg="#DDA0DD",
                            activebackground="#BA55D3",
                            fg="white",
                            font=("Arial", 16, "bold"),
                            width=20,
                            height=1,
                            bd=0,
                            relief="ridge",
                            cursor="hand2",
                            command=lambda: oyunu_kaydet(entries, zorluk, None))
    ara_ver_buton.pack(pady=10)
    
    kontrol_buton = tk.Button(kontrol_frame,
                            text="✓ Kontrol Et ✓",
                            bg="#DDA0DD",
                            activebackground="#BA55D3",
                            fg="white",
                            font=("Arial", 16, "bold"),
                            width=20,
                            height=1,
                            bd=0,
                            relief="ridge",
                            cursor="hand2",
                            command=kontrol_et)
    kontrol_buton.pack()
    
    # Hover efekti
    kontrol_buton.bind("<Enter>", lambda e: kontrol_buton.config(bg="#BA55D3"))
    kontrol_buton.bind("<Leave>", lambda e: kontrol_buton.config(bg="#DDA0DD"))
    ara_ver_buton.bind("<Enter>", lambda e: ara_ver_buton.config(bg="#BA55D3"))
    ara_ver_buton.bind("<Leave>", lambda e: ara_ver_buton.config(bg="#DDA0DD"))

    oyun_pencere.mainloop()

def check_input(entry, zorluk):
    try:
        value = int(entry.get())
        if value < 1 or value > 9:
            raise ValueError
    except ValueError:
        if entry.get() != "":
            entry.config(bg="purple")
            messagebox.showerror("Hata", "Lütfen 1-9 arasında bir sayı girin.")
            entry.delete(0, tk.END)
    finally:
        entry.config(bg="white")

# Ana giriş ekranını başlat
if __name__ == "__main__":
    giris_pencere = tk.Tk()
    app = SudokuGiris(giris_pencere)
    giris_pencere.mainloop()
