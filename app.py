import os
import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog
import glob
import cv2

import faceclip as f_clip

# ===== 定数 =====

DEF_FONT = ("Yu Gothic", "12")

# ディレクトリダイアログを開く
def open_dirdialog():
    dir_path = filedialog.askdirectory()
    return dir_path

# ファイルダイアログを開く　
def open_filedialog():
    file_path = filedialog.askopenfilename()
    return file_path

def start_processing(i_path,o_dir,resize,rename,re_w,re_h,ext,frame,face_clip):
    if(os.path.isdir(i_path)):
        processing_img(i_path,o_dir,resize,rename,re_w,re_h,ext)
    else:
        processing_video(i_path,o_dir,re_w,re_h,ext,frame,frame)


def processing_img(i_dir,o_dir,resize,rename,re_w,re_h,ext,face_clip):
    if len(i_dir) != 0 and len(o_dir) != 0 and i_dir != o_dir:
        files = glob.glob(i_dir+ "/*")
        for i, f in enumerate(files):
            if f.endswith((".png",".jpg")):
                img=cv2.imread(f)
                if resize: img = cv2.resize(img, dsize=(int(re_w), int(re_h)))
                name = os.path.basename(f)
                if rename: name = str(i).zfill(5) + ext
                cv2.imwrite(os.path.join(o_dir,name),img)
        messagebox.showinfo("完了","処理が完了しました。")
    else:
        messagebox.showinfo("エラー","処理を中断しました。")

def processing_video(i_file,o_dir,re_w,re_h,ext,frame_rate,face_clip):
    cap = cv2.VideoCapture(i_file)
    start_num = len(glob.glob(o_dir+ "/*"))

    if not cap.isOpened():
        return

    num = start_num
    cnt = 0
    while True:
        ret, frame = cap.read()
        if ret:
            if cnt % int(frame_rate) == 0:
                if(face_clip):
                    frame = f_clip.face_clip(frame,resize_width=int(re_w),resize_height=int(re_h))
                    if  len(frame) != 0:
                        filename = str(num).zfill(5) + ext
                        cv2.imwrite(os.path.join(o_dir,filename),frame)
                        num += 1
            cnt += 1
        else:
            return


# ===== イベントハンドラー =====

def click_input_dir_open():
    path = open_dirdialog()
    input_dir_box.delete(0,tk.END)
    input_dir_box.insert(tk.END,path)

def click_input_file_open():
    path = open_filedialog()
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
    frame = box_frame.get()
    face_clip = bln_face_clip.get()

    start_processing(i_dir,o_dir,flg_resize,flg_rename,re_w,re_h,ext,frame,face_clip)



# ===== ウィンドウ =====

#ウィンドウを作成
root = tk.Tk() 
root.title(u"image-processing")
root.geometry("800x480")

#UI

# Input Dir
frame00 = tk.Frame(root)
frame00.grid(column=0,row=0, padx=5, pady=5,sticky=tk.W)

input_label =tk.Label(frame00,text="Input",font=DEF_FONT)
input_label.pack(side='left',padx=5)
input_dir_box = tk.Entry(frame00, width=60,font=DEF_FONT)
input_dir_box.pack(side='left',padx=5)
input_button_dir = tk.Button(frame00,text=u'Open Dir',command=click_input_dir_open,font=DEF_FONT)
input_button_dir.pack(side='left',padx=5)
input_button_file = tk.Button(frame00,text=u'Open File',command=click_input_file_open,font=DEF_FONT)
input_button_file.pack(side='left',padx=5)

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

# FaceClip
frame04 = tk.Frame(root)
frame04.grid(column=0,row=4, padx=5, pady=5,sticky=tk.W)
bln_face_clip = tk.BooleanVar()
bln_face_clip.set(True)
check_face_clip = tk.Checkbutton(frame04,variable=bln_face_clip, text='FaceClip', font=DEF_FONT)
check_face_clip.pack(side='left',padx=5)

# Frame
frame_frame = tk.Frame(root)
frame_frame.grid(column=0,row=5, padx=5, pady=5,sticky=tk.W)
label_frame =tk.Label(frame_frame,text="Frame",font=DEF_FONT)
label_frame.pack(side='left',padx=5)
box_frame= tk.Entry(frame_frame, width=5,font=DEF_FONT)
box_frame.pack(side='left',padx=5)
box_frame.insert(tk.END,30)

# Progress
frame_progress = tk.Frame(root)
frame_progress.grid(column=0,row=6, padx=5, pady=5,sticky=tk.W)
pb_var = tk.IntVar(0)
pb_var.set(0)
#pb_max = tk.IntVar(0)
pb_max = 200
progress_bar = ttk.Progressbar(frame_progress,maximum=pb_max,mode="determinate",variable=pb_var)
progress_bar.pack(side='left',padx=5)

# Start
frame_start = tk.Frame(root)
frame_start.grid(column=0,row=7, padx=5, pady=5,sticky=tk.W)

button_start = tk.Button(frame_start,text=u'Start',command=click_start,font=DEF_FONT)
button_start.pack(side='left',padx=5)

#ウィンドウを表示
root.mainloop()