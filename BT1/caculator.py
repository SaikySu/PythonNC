import tkinter as tk
from tkinter import ttk

def Tru():
    a = float(entry_a.get())
    b = float(entry_b.get())
    
    hieu = a - b
    result.set(f"Hiệu là: {hieu}")
    
def Cong():
    a = float(entry_a.get())
    b = float(entry_b.get())
    tong = a + b
    result.set(f"Tổng là: {tong}")
    
def Nhan():
    a = float(entry_a.get())
    b = float(entry_b.get())
    tich = a * b
    result.set(f"Tích là: {tich}")
    
def Chia():
    a = float(entry_a.get())
    b = float(entry_b.get())
    if b != 0:
        thuong = a / b
        result.set(f"Thương là: {thuong}")
    else:
        result.set("Lỗi: Không thể chia cho 0")
        


# Tạo cửa sổ chính
win = tk.Tk()
win.title("Công cụ tính toán Promax")

# Lable Frame Input
buttons_frame = ttk.LabelFrame(win, text='Nhập', labelanchor='n')  
buttons_frame.grid(column=0, row=0)
ttk.Label(buttons_frame, text="Nhập số a: ").grid(column=0, row=0, sticky=tk.W)
entry_a = ttk.Entry(buttons_frame)
entry_a.grid(column=1, row=0)  

ttk.Label(buttons_frame, text="Nhập số b: ").grid(column=0, row=1, sticky=tk.W)
entry_b = ttk.Entry(buttons_frame)
entry_b.grid(column=1, row=1)  

# Lable Frame Caculate
buttons_frame_caculate = ttk.LabelFrame(win, text='Tính toán', labelanchor='n') 
buttons_frame_caculate.grid(column=1, row=0)

# Cộng
solve_button_cong = ttk.Button(buttons_frame_caculate, text="+", command=Cong)
solve_button_cong.grid(row=0, column=0)
# Trừ
solve_button_tru = ttk.Button(buttons_frame_caculate, text="-", command=Tru)
solve_button_tru.grid(row=1, column=0)
# Nhân
solve_button_nhan = ttk.Button(buttons_frame_caculate, text="*", command=Nhan)
solve_button_nhan.grid(row=0, column=1)
# Chia
solve_button_chia = ttk.Button(buttons_frame_caculate, text="/", command=Chia)
solve_button_chia.grid(row=1, column=1)

# Result Lable Frame
buttons_frame_Result = ttk.LabelFrame(win, text='Kết quả') 
buttons_frame_Result.grid(column=0, row=1)
ttk.Label(buttons_frame_Result, text="Kết quả là: ").grid(column=0, row=0, sticky=tk.W)

result = tk.StringVar()
label_result = ttk.Label(buttons_frame_Result, textvariable=result)
label_result.grid(column=1, row=0)

# Chạy vòng lặp chính
win.mainloop()
