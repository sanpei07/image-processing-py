import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
import glob
import cv2

# ===== 定数 =====

DEF_FONT = ("Yu Gothic", "12")

# ディレクトリダイアログを開く
def open_dirdialog():
    dir_path = filedialog.askdirectory()
    return dir_path

def start_processing(i_dir,o_dir,resize,rename,re_w,re_h,ext):
    if len(i_dir) != 0 and len(o_dir) != 0 and i_dir != o_dir:
        files = glob.glob(i_dir+ "/*")
        for i, f in enumerate(files):
            if f.endswith((".png",".jpg")):
                img=cv2.imread(f)
                if resize: img = cv2.resize(img, dsize=(int(re_w), int(re_h)))
                name = os.path.basename(f)
                if rename: name = str(i).zfill(5) + ext
                cv2.imwrite(os.path.join(o_dir,name),img)
        messagebox.showinfo("完了","処理が完了しました")
    else:
        pass


# ===== イベントハンドラー =====

def click_input_open():
    path = open_dirdialog()
    input_dir_box.delete(0,tk.END)
    input_dir_box.insert(tk.END,path)
    

def click_output_open():
    path = open_dirdialog()
    output_dir_box.delete(0,tk.END)
    output_dir_box.insert(tk.END,path)

def click_start():
    i_dir = input_dir_box.get()
    o_dir = output_dir_box.get()
    re_w = box_resize_w.get()
    re_h = box_resize_w.get()
    ext = text_extension.get()
    flg_resize = bln_resize.get()
    flg_rename = bln_rename.get()

    start_processing(i_dir,o_dir,flg_resize,flg_rename,re_w,re_h,ext)



# ===== ウィンドウ =====

#ウィンドウを作成
root = tk.Tk() 
root.title(u"image-processing")
root.geometry("720x480")

#UI

# Input Dir
frame00 = tk.Frame(root)
frame00.grid(column=0,row=0, padx=5, pady=5,sticky=tk.W)

input_label =tk.Label(frame00,text="Input",font=DEF_FONT)
input_label.pack(side='left',padx=5)
input_dir_box = tk.Entry(frame00, width=60,font=DEF_FONT)
input_dir_box.pack(side='left',padx=5)
input_button = tk.Button(frame00,text=u'Open',command=click_input_open,font=DEF_FONT)
input_button.pack(side='left',padx=5)

# Output Dir
frame01 = tk.Frame(root)
frame01.grid(column=0,row=1, padx=5, pady=5,sticky=tk.W)

output_label =tk.Label(frame01,text="Output",font=DEF_FONT)
output_label.pack(side='left',padx=5)
output_dir_box = tk.Entry(frame01, width=60,font=DEF_FONT)
output_dir_box.pack(side='left',padx=5)
output_button = tk.Button(frame01,text=u'Open',command=click_output_open,font=DEF_FONT)
output_button.pack(side='left',padx=5)

# Resize
frame02 = tk.Frame(root)
frame02.grid(column=0,row=2, padx=5, pady=5,sticky=tk.W)

bln_resize = tk.BooleanVar()
bln_resize.set(True)

check_resize = tk.Checkbutton(frame02,variable=bln_resize, text='ReSize', font=DEF_FONT)
check_resize.pack(side='left',padx=5)
label_resize_w =tk.Label(frame02,text="Width",font=DEF_FONT)
label_resize_w.pack(side='left',padx=5)
box_resize_w = tk.Entry(frame02, width=5,font=DEF_FONT)
box_resize_w.pack(side='left',padx=5)
label_resize_h =tk.Label(frame02,text="Height",font=DEF_FONT)
label_resize_h.pack(side='left',padx=5)
box_resize_h = tk.Entry(frame02, width=5,font=DEF_FONT)
box_resize_h.pack(side='left',padx=5)

box_resize_w.insert(tk.END,256)
box_resize_h.insert(tk.END,256)

# Rename
frame03 = tk.Frame(root)
frame03.grid(column=0,row=3, padx=5, pady=5,sticky=tk.W)

bln_rename = tk.BooleanVar()
bln_rename.set(True)

check_rename = tk.Checkbutton(frame03,variable=bln_rename, text='ReName', font=DEF_FONT)
check_rename.pack(side='left',padx=5)

text_extension = tk.StringVar()
text_extension.set('.png')
list_extension= ('.png', '.jpg')
select_extension = ttk.Combobox(frame03,state="readonly",font=DEF_FONT,values=list_extension, textvariable=text_extension)
select_extension.pack(side='left',padx=5)

# Progress
frame04 = tk.Frame(root)
frame04.grid(column=0,row=4, padx=5, pady=5,sticky=tk.W)
pb_var = tk.IntVar(0)
pb_var.set(0)
#pb_max = tk.IntVar(0)
pb_max = 200
progress_bar = ttk.Progressbar(frame04,maximum=pb_max,mode="determinate",variable=pb_var)
progress_bar.pack(side='left',padx=5)

# Start
frame05 = tk.Frame(root)
frame05.grid(column=0,row=5, padx=5, pady=5,sticky=tk.W)

button_start = tk.Button(frame05,text=u'Start',command=click_start,font=DEF_FONT)
button_start.pack(side='left',padx=5)

#ウィンドウを表示
root.mainloop()