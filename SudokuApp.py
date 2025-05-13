import numpy as np
import random

class Sudoku:
    def __init__(self):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        
    def is_valid(self, row, col, num):
        if num in self.board[row]:
            return False
    
        if num in [self.board[i][col] for i in range(9)]:
            return False

        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False
        return True
        
    def check_full_solution(self, solution):
        # Tüm satırları kontrol et
        for row in range(9):
            row_values = set()
            for col in range(9):
                val = solution[row][col]
                if val == 0 or val in row_values:
                    return False
                row_values.add(val)
                
        # Tüm sütunları kontrol et
        for col in range(9):
            col_values = set()
            for row in range(9):
                val = solution[row][col]
                if val == 0 or val in col_values:
                    return False
                col_values.add(val)
                
        # Tüm 3x3 kutuları kontrol et
        for box_row in range(0, 9, 3):
            for box_col in range(0, 9, 3):
                box_values = set()
                for row in range(box_row, box_row + 3):
                    for col in range(box_col, box_col + 3):
                        val = solution[row][col]
                        if val == 0 or val in box_values:
                            return False
                        box_values.add(val)
                        
        return True

    def fill_board(self):
        empty = self.find_empty()
        if not empty:
            return True
        
        row, col = empty
        nums = list(range(1, 10))
        random.shuffle(nums)
        
        for num in nums:
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.fill_board():
                    return True
                self.board[row][col] = 0
        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def clean_boxes_kolay(self, count=20):
        cleared = 0
        while cleared < count:
            row = random.randint(0,8)
            col = random.randint(0, 8) 
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cleared += 1

    def clean_boxes_orta(self, count=30):
        cleared = 0
        while cleared < count:
            row = random.randint(0,8)
            col = random.randint(0, 8) 
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cleared += 1

    def clean_boxes_zor(self, count=40):
        cleared = 0
        while cleared < count:
            row = random.randint(0,8)
            col = random.randint(0, 8) 
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cleared += 1

    def clean_boxes_expert(self, count=50):
        cleared = 0
        while cleared < count:
            row = random.randint(0,8)
            col = random.randint(0, 8) 
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                cleared += 1

    def secim(self):
        secim = input("Seçiminizi giriniz: Kolay/Orta/Zor/Ekspert: ")
        if secim == "kolay":
            print("kolay seviye seçildi")
            self.clean_boxes_kolay()
        elif secim == "orta":
            print("orta seviye seçildi")
            self.clean_boxes_orta()
        elif secim == "zor":
            print("zor seviye seçildi")
            self.clean_boxes_zor()
        elif secim == "ekspert":
            print("expert seviye seçildi")
            self.clean_boxes_expert()
        else:
            print("Geçersiz secim yaptınız. Varsayılan olarak orta seviye seçildi.")
            self.clean_boxes_orta()

    def print_board(self):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("-" * 21)
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("|", end=" ")
                val = self.board[i][j]
                print("." if val == 0 else val, end=" ")
            print()  

    def play(self):
        while self.find_empty():
            self.print_board()
            print("boş bir hücreyi doldurmak için satır, sütun ve sayı girin")

            try:
                row = int(input("Satır (1-9): ")) - 1
                col = int(input("Sütun (1-9): ")) - 1
                num = int(input("Sayı (1-9): "))

            except ValueError:
                print("Geçersiz giriş lütfen tekrar deneyiniz.")
                continue

            if self.board[row][col] != 0:
                print("bu hücre zaten dolu")
                continue

            if self.is_valid(row, col, num):
                self.board[row][col] = num

            else:
                print("kurallara uygun değil lütfen tekrardan dene. ")

    def start_game(self):
        self.fill_board()
        self.secim()
        self.play()
        print("Tebrikler sudoku tamamlandı.. ")

        
if __name__ == "__main__":
    game = Sudoku()
    game.start_game()













































