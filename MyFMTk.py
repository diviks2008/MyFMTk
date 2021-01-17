#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# for Debian, Ubuntu:
#       sudo apt install python3-tk python3-magic python3-pil python3-pil.imagetk
#
# for OpenSuse:
#       sudo zypper install python3-tk python3-python-magic python3-Pillow python3-Pillow-tk
#       In console for clearing out the X resources:
#       xrdb -load /dev/null
#       xrdb -query
#
#       Or install python3-magic:
#       sudo zypper remove python3-magic
#       sudo zypper install python3-python-magic

import os
import time
from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
import subprocess
from PIL import Image, ImageTk
# import imghdr
import magic
import sys
import shutil
import pwd
import grp

w = 685
h = 470
w_tab_image = 20
w_tab_rights = 59
w_tab_owner = 59
w_tab_group = 59
w_tab_ext = 79
w_tab_size = 79
w_tab_mtime = 150
w_tab_atime = 150
w_tab_name = w-(w_tab_image+w_tab_ext+w_tab_size+w_tab_mtime+w_tab_atime)-33
date_time = '%Y.%m.%d %H:%M:%S'
key_sort_by = 'name'
key_sort_invers = 0
key_hide_files_hidden = 1
str_folder_up = '. . .'
start_switch = '#'
myemail = '646976696b733230303840676d61696c2e636f6d'
preview_max_lines = 300

background_dirs = '#cccccc'
background_txt = '#ccffff'
background_with = '#ffffff'
background_media = '#ccccff'
background_image = '#ffccff'

# file_config = '.myfm_pft_config.txt'
# if os.path.exists('/home/divik/1_MyPO'):
#     file_config = os.path.join('/home/divik/1_MyPO', file_config)


def CenteredWindow(root):
    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    x = int((sw - w) / 2)
    y = int((sh - h) / 2)
    return w, h, x, y


class App:

    def __init__(self, master):
        self.collapsed_icon = PhotoImage(data='R0lGODlhDwANAKIAAAAAAMDAwICAgP//////ADAwMAAAAAAA'
                                         'ACH5BAEAAAEALAAAAAAPAA0AAAMyGCHM+lAMMoeAT9Jtm5NDKI4Wo'
                                         'FXcJphhipanq7Kvu8b1dLc5tcuom2foAQQAyKRSmQAAOw==')
        self.master = master
        self.master.iconphoto(False, self.collapsed_icon)
        self.folder_rab = os.getcwd()
        self.key_hide_files_hidden = key_hide_files_hidden
        self.key_sort_by = key_sort_by
        self.key_sort_invers = key_sort_invers
        self.line_select = 0

        frame01 = Frame(master)
        frame01.pack(side=LEFT, fill=Y, expand=1)
        self.text = Text(master)
        self.text.pack(side=LEFT, fill=BOTH, expand=1)

        frame1 = LabelFrame(frame01, height=17)  # , bg='Yellow')#, text='path to file')
        frame1.pack(padx=5, pady=5, side=TOP, fill=X)
        frame2 = LabelFrame(frame01)  # , bg='Blue')
        frame2.pack(padx=5, side=TOP, fill=BOTH, expand=1)  # , anchor=NW)
        frame3 = Frame(frame01, height=17)  # , bg='Green')
        frame3.pack(padx=5, pady=5, side=TOP, fill=X)

        # self.get_default_setup()
        self.frame1 = frame1
        self.frame2 = frame2

        l_frame1 = Label(frame1, text='Folder:')
        l_frame1.pack(padx=5, side=LEFT)

        self.e_frame1 = Entry(frame1)
        self.e_frame1.pack(padx=5, side=LEFT, fill=X, expand=1)
        self.e_frame1.insert(END, self.folder_rab)

        self.b_frame1 = Button(frame1, text='UP', command=self.folder_up)
        self.b_frame1.pack(padx=5, side=LEFT)

        # self.lb_frame2 = Listbox(frame2)
        # self.lb_frame2.pack(side=LEFT, fill=BOTH, expand=1)

        self.l_frame3 = Label(frame3)
        self.l_frame3.pack(padx=5, side=LEFT, fill=X, expand=1, anchor=W)
        self.l_frame4 = Label(frame3)
        self.l_frame4.pack(padx=5, side=LEFT, fill=X, expand=1, anchor=W)

        self.tree = ttk.Treeview(frame2, selectmode=BROWSE)
        # self.tree = ttk.Treeview(frame2)
        self.style = ttk.Style()
        self.style.map('Treeview', foreground=self.fixed_map('foreground'),
                       background=self.fixed_map('background'), tagname=self.fixed_map('tagname'))

        self.vsb_y = ttk.Scrollbar(frame2, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.vsb_y.set)
        vsb_x = ttk.Scrollbar(frame2, orient=HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscrollcommand=vsb_x.set)

        vsb_x.pack(side=BOTTOM, fill=X)
        self.vsb_y.pack(side=RIGHT, fill=Y)
        self.tree.pack(side=LEFT, fill=BOTH, expand=1)

        self.tree['columns'] = ('Name', 'rights', 'owner', 'group', 'ext', 'size', 'mtime')#, 'atime')
        self.tree.column('#0', width=w_tab_image, minwidth=w_tab_image)
        self.tree.column('Name', width=w_tab_name, minwidth=w_tab_name)  # , stretch=NO)
        self.tree.column('rights', width=w_tab_rights, minwidth=w_tab_rights)
        self.tree.column('owner', width=w_tab_owner, minwidth=w_tab_owner)
        self.tree.column('group', width=w_tab_group, minwidth=w_tab_group)
        self.tree.column('ext', width=w_tab_ext, minwidth=w_tab_ext)
        self.tree.column('size', width=w_tab_size, minwidth=w_tab_size)
        self.tree.column('mtime', width=w_tab_mtime, minwidth=w_tab_mtime)
        # self.tree.column('atime', width=w_tab_atime, minwidth=w_tab_atime)
        # self.tree.heading('#0', text='', anchor='center', command=self.sort_column_by_image)
        self.tree.heading('Name', text='Name', anchor='center', command=self.sort_column_by_name)
        self.tree.heading('rights', text='rights', anchor='center', command=self.sort_column_by_rights)
        self.tree.heading('owner', text='owner', anchor='center', command=self.sort_column_by_owner)
        self.tree.heading('group', text='group', anchor='center', command=self.sort_column_by_group)
        self.tree.heading('ext', text='ext', anchor='center', command=self.sort_column_by_ext)
        self.tree.heading('size', text='size', anchor='center', command=self.sort_column_by_size)
        self.tree.heading('mtime', text='Date modified', anchor='center', command=self.sort_column_by_mtime)
        # self.tree.heading('atime', text='Date access', anchor='center', command=self.sort_column_by_atime)

        self.insert_in_tree()

    def fixed_map(self, option):
        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
        return [elm for elm in self.style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]

    def insert_in_tree(self):
        item = self.get_item_selection()
        dic_dirs, dic_files = self.get_dic_in_folder()
        self.dic_dirs = dic_dirs
        self.dic_files = dic_files
        dirs_list = list(dic_dirs.keys())
        files_list = list(dic_files.keys())
        dirs_list = self.sort_list_files(dirs_list)
        files_list = self.sort_list_files(files_list)

        label = Label(image=self.collapsed_icon)
        label.image = self.collapsed_icon

        if self.key_sort_invers:
            dirs_list.reverse()
            files_list.reverse()

        self.clear_e_frame1()
        self.tree.insert('', 'end', values=[str_folder_up])

        for dir_path in dirs_list:
            if os.path.basename(dir_path).startswith('.') and self.key_hide_files_hidden:
                continue
            tab_mtime, tab_atime = self.get_mtime_file(dir_path)
            dir_rights = oct(os.stat(dir_path).st_mode)[-3:]
            dir_owner = pwd.getpwuid(os.stat(dir_path).st_uid).pw_name
            dir_group = grp.getgrgid(os.stat(dir_path).st_gid).gr_name
            if dic_dirs[dir_path][1] == 'denied':
                tab_values = ['    ' + dic_dirs[dir_path][0], '', '', '', '', dic_dirs[dir_path][1], tab_mtime]
            else:
                tab_values = ['    ' + dic_dirs[dir_path][0], dir_rights, dir_owner, dir_group, '{}/{}'.format(dic_dirs[dir_path][2], dic_dirs[dir_path][3]), dic_dirs[dir_path][1], tab_mtime]
            self.tree.insert('', 'end', image=label.image, values=tab_values, tags=('dirs',))
            # self.tree.tag_configure(tagname='dirs', background=background_dirs)
        for file_path in files_list:
            if os.path.basename(file_path).startswith('.') and self.key_hide_files_hidden:
                continue
            # file_size = self.converter_number_to_gb(os.path.getsize(file_path))
            # tab_size = '{:9}{:3}'.format(file_size.split(' ')[0], file_size.split(' ')[1])
            tab_size = self.converter_number_to_gb(os.path.getsize(file_path))
            tab_mtime, tab_atime = self.get_mtime_file(file_path)
            file_rights = oct(os.stat(file_path).st_mode)[-3:]
            file_owner = pwd.getpwuid(os.stat(file_path).st_uid).pw_name
            file_group = grp.getgrgid(os.stat(file_path).st_gid).gr_name
            tab_values = [dic_files[file_path][0], file_rights, file_owner, file_group, os.path.splitext(dic_files[file_path][0])[1], tab_size, tab_mtime]
            m = magic.Magic(mime=True)
            try:
                if m.from_file(file_path).startswith('text'):
                    self.tree.insert('', 'end', values=tab_values, tags=('txt',))
                    self.tree.tag_configure(tagname='txt', background=background_txt)
                elif m.from_file(file_path).startswith('video') or m.from_file(file_path).startswith('audio'):
                    self.tree.insert('', 'end', values=tab_values, tags=('media',))
                    self.tree.tag_configure(tagname='media', background=background_media)
                elif m.from_file(file_path).startswith('image'):
                    self.tree.insert('', 'end', values=tab_values, tags=('image',))
                    self.tree.tag_configure(tagname='image', background=background_image)
                else:
                    self.tree.insert('', 'end', values=tab_values, tags=('w',))
                    self.tree.tag_configure(tagname='w', background=background_with)
            except:
                self.tree.insert('', 'end', values=tab_values, tags=('w',))
                self.tree.tag_configure(tagname='w', background=background_with)

        self.set_selection_line_by_item(item)

    def get_dic_in_folder(self):
        dic_dirs = {}
        dic_files = {}
        for f in os.listdir(self.folder_rab):
            f_path = os.path.join(self.folder_rab, f)
            if os.path.isdir(f_path):
                try:
                    full_list = os.listdir(f_path)
                    d_list = [os.path.join(f_path, d) for d in full_list if os.path.isdir(os.path.join(f_path, d))]
                    f_list = [os.path.join(f_path, f) for f in full_list if os.path.isfile(os.path.join(f_path, f)) or os.path.islink(os.path.join(f_path, f))]
                    dic_dirs[f_path] = [f, len(full_list), len(d_list), len(f_list)]
                except:
                    dic_dirs[f_path] = [f, 'denied']
            else:
                try:
                    dic_files[f_path] = [f, os.path.getsize(f_path)]
                except:
                    dic_files[f_path] = [f, 'denied']
        return dic_dirs, dic_files

    def open_folder(self, event=''):
        folder_old = self.e_frame1.get()
        folder_new = filedialog.askdirectory(initialdir=self.folder_rab)
        if folder_new:
            if os.path.exists(folder_new):
                self.folder_rab = folder_new
            else:
                self.folder_rab = folder_old
            self.e_frame1.delete(0, END)
            self.e_frame1.insert(0, self.folder_rab)
            self.update()
            self.set_selection_line_by_item()

    def folder_up(self):
        folder_old = self.e_frame1.get()
        item = os.path.basename(self.folder_rab)
        if os.path.exists(folder_old):
            folder_new = os.path.dirname(folder_old)
            if os.path.exists(folder_new):
                self.folder_rab = folder_new
        else:
            self.folder_rab = os.getcwd()
        self.e_frame1.delete(0, END)
        self.e_frame1.insert(END, self.folder_rab)
        self.update()
        self.set_selection_line_by_item(item)

    def get_item_selection(self):
        self.text.delete(0.0, END)
        try:
            item = self.tree.item(self.tree.selection(), 'values')[0].strip()
            return item
        except:
            return ''

    def get_item_selection_up(self):
        self.text.delete(0.0, END)
        lines = self.tree.get_children()
        line_index_up = lines.index(self.tree.selection()[0]) - 1
        if line_index_up < 0:
            line_index_up = 0
        line_up = lines[line_index_up]
        item_up = self.tree.item(line_up, 'values')[0].strip()
        return item_up

    def get_filepath_selection(self):
        item = self.get_item_selection()
        if item == str_folder_up:
            file_path = self.folder_rab
        else:
            file_path = os.path.join(self.folder_rab, item)
        return file_path

    def set_selection_line_by_item(self, item=''):
        if not item:
            item = '. . .'
        lines = self.tree.get_children()
        line = self.tree.get_children()[0]
        for line in lines:
            if item == self.tree.item(line, 'values')[0].strip():
                break
        self.tree.selection_set(line)

    def print_islink(self, file_path):
        if os.path.islink(file_path):
            self.l_frame3.configure(text='link: {}'.format(file_path), anchor='w')
            self.l_frame4.configure(text='real path: {}'.format(os.readlink(file_path)), anchor='w')

    def line_clicked_double(self, event):
        folder_old = self.e_frame1.get()
        try:
            f_select = self.tree.item(self.tree.selection(), 'values')[0].strip()
        except:
            return
        if f_select == str_folder_up:
            self.folder_up()
            self.l_frame3.configure(text=os.path.basename(self.folder_rab), anchor=W)
            self.l_frame4.configure(text='')
            return
        file_path = os.path.join(self.folder_rab, f_select)

        if os.path.islink(file_path):
            self.print_islink(file_path)
            return
        try:
            if self.dic_dirs[file_path][1] == 'denied':
                self.l_frame3.configure(text=os.path.basename(file_path) + ': denied', anchor=W)
                self.l_frame4.configure(text='')
                return
        except:
            pass
        if os.path.isdir(file_path):
            self.folder_rab = file_path
            # self.save_setup()
            self.insert_in_tree()
            self.l_frame3.configure(text=os.path.basename(file_path), anchor=W)
            self.l_frame4.configure(text='')
            self.set_selection_line_by_item()
            return
        elif os.path.isfile(file_path):
            if sys.platform == 'win32':
                os.startfile(file_path)
                return
            try:
                subprocess.run(['xdg-open', file_path])
                return
            except:
                return
        else:
            # link
            return

    def preview(self, event):
        self.menu_close()
        file_path = self.get_filepath_selection()
        if not file_path or os.path.islink(file_path):
            self.print_islink(file_path)
            return

        self.l_frame3.configure(text=os.path.basename(file_path), anchor=W)
        try:
            if self.dic_dirs[file_path][1] == 'denied' or self.dic_files[file_path][1] == 'denied':
                self.l_frame4.configure(text='denied')
            else:
                self.l_frame4.configure(text='')
        except:
            self.l_frame4.configure(text='')

        m = magic.Magic(mime=True)
        try:
            if m.from_file(file_path).startswith('text'):
                try:
                    f = open(file_path, 'r')
                    for i in range(preview_max_lines):
                        text = f.readline()
                        if text:
                            self.text.insert(END, text)
                        else:
                            break
                    f.close()
                    if i >= preview_max_lines - 1:
                        self.text.insert(END,
                            '\n{0}\nThis is not all content.\nTo read a file, double click on the file name\n{0}\n'.format(
                                '.' * 71))
                    return
                except:
                    return
            elif m.from_file(file_path).startswith('image'):
                img = Image.open(file_path)
                img_data = 'size:{} format:{} mode:{}'.format(img.size, img.format, img.mode)
                self.l_frame4.configure(text=img_data)

                (x_image, y_image) = img.size
                x_win = self.text.winfo_x() - 80
                y_win = int(x_win * y_image / x_image)
                siz_win = (x_win, y_win)

                img_size = img.resize(siz_win, Image.ANTIALIAS)
                img_size = ImageTk.PhotoImage(img_size)
                self.img = Label(self.text, image=img_size)
                self.img.image = img_size
                self.img.place(x=5, y=5)
            self.text.update()
        except:
            return

    def get_mtime_file(self, file_path):
        f_mtime = os.path.getmtime(file_path)
        f_atime = os.path.getatime(file_path)
        tab_mtime = time.strftime(date_time, time.localtime(f_mtime))
        tab_atime = time.strftime(date_time, time.localtime(f_atime))
        return tab_mtime, tab_atime

    def menu_folder(self, event):
        try:
            self.menu_close()
        except:
            pass
        self.menu = Menu(self.frame1, tearoff=0)
        self.menu.add_command(label='Open folder', command=self.open_folder)
        self.menu.add_command(label='Update', command=self.insert_in_tree)
        self.menu.add_command(label='Quit', command=self.quit)
        self.menu.post(event.x_root, event.y_root)

    def menu_contecst(self, event):
        try:
            self.menu_close()
        except:
            pass
        self.menu = Menu(self.frame2, tearoff=0)
        self.menu.add_command(label='Cancel', command=self.menu_close)
        self.menu.add_command(label='Update', command=self.update)
        self.menu.add_command(label='----------------------------------')
        self.menu.add_command(label='Show/Hide hidden files', command=self.hide_files_hidden)
        self.menu.add_command(label='Create file', command=self.create_file)
        self.menu.add_command(label='Copy file', command=self.copy_file)
        self.menu.add_command(label='Move file', command=self.move_file)
        self.menu.add_command(label='Delete file', command=self.delete_file)
        self.menu.add_command(label='----------------------------------')
        self.menu.add_command(label='Create dir', command=self.create_dir)
        self.menu.add_command(label='Delete dir', command=self.delete_dir)
        self.menu.add_command(label='----------------------------------')
        self.menu.add_command(label='Chmod', command=self.chmod_file)
        self.menu.add_command(label='Rename', command=self.rename_file)
        self.menu.add_command(label='----------------------------------')
        self.menu.add_command(label='Quit', command=self.quit)
        self.menu.post(event.x_root, event.y_root)
        # self.menu.configure(font=self.myFont)

    def menu_close(self, event=''):
        try:
            self.menu.destroy()
        except:
            pass
        try:
            self.help.destroy()
        except:
            pass
        try:
            self.img.destroy()
        except:
            pass
        self.master.clipboard_clear()

    def create_file(self):
        new_name = str(
            subprocess.run(['/usr/bin/zenity', '--entry', '--title', 'Create file', '--text', 'Please enter new name'],
                           stdout=subprocess.PIPE).stdout.decode()).strip()

        if not new_name:
            return
        file_path = os.path.join(self.folder_rab, new_name)
        if os.path.exists(file_path):
            if not messagebox.askokcancel('Create file', '{}\n\nFile with this name exists!\nContinue?'.format(file_path)):
                return
        with open(file_path, 'w') as f:
            f.flush()
        os.chmod(file_path, mode=0o700)
        self.update()
        self.set_selection_line_by_item(new_name)

    def copy_file(self):
        file_path_old = self.get_filepath_selection()
        item = self.get_item_selection()
        if item == str_folder_up:
            return
        if os.path.isfile(file_path_old) and os.access(file_path_old, os.R_OK):
            dir_path = filedialog.askdirectory(initialdir=self.folder_rab)
            if dir_path:
                file_path_new = os.path.join(dir_path, os.path.basename(file_path_old))
                if os.path.exists(file_path_new):
                    if not messagebox.askokcancel('Copy file',
                                                  '{}\n\nFile with this name exists!\nContinue?'.format(file_path_new)):
                        return
                try:
                    shutil.copy2(file_path_old, file_path_new)
                except:
                    messagebox.showerror('Copy file',
                                        '{}\n{}\nError copying file\nInvalid new path or folder not accessible'.format(
                                            file_path_old, file_path_new))

    def move_file(self):
        file_path_old = self.get_filepath_selection()
        item = self.get_item_selection()
        if item == str_folder_up:
            return
        if os.path.isfile(file_path_old) and os.access(file_path_old, os.R_OK):
            dir_path = filedialog.askdirectory(initialdir=self.folder_rab)
            if dir_path:
                file_path_new = os.path.join(dir_path, os.path.basename(file_path_old))
                if os.path.exists(file_path_new):
                    if not messagebox.askokcancel('Move file',
                                                  '{}\n\nFile with this name exists!\nContinue?'.format(file_path_new)):
                        return
                try:
                    shutil.move(file_path_old, file_path_new)
                except:
                    messagebox.showerror('Copy file',
                                         '{}\n{}\nError copying file\nInvalid new path or folder not accessible'.format(
                                             file_path_old, file_path_new))

    def delete_file(self):
        file_path = self.get_filepath_selection()
        item_up = self.get_item_selection_up()
        item = self.get_item_selection()
        if item == str_folder_up:
            return
        if not os.access(file_path, os.R_OK):
            messagebox.showerror(title='Deletion Error! ', message='Access is denied!')
            return
        if os.path.isfile(file_path):
            if messagebox.askyesno(title='Delete File! ', message='{}\n\nWill be deleted. Confirm?'.format(file_path)):
                os.remove(file_path)
                self.update()
                self.set_selection_line_by_item(item_up)

    def create_dir(self):
        item = self.get_item_selection()
        new_name = str(
            subprocess.run(['/usr/bin/zenity', '--entry', '--title', 'Create file', '--text', 'Please enter new name'],
                           stdout=subprocess.PIPE).stdout.decode()).strip()

        if not new_name:
            return
        dir_path = os.path.join(self.folder_rab, new_name)
        if os.path.exists(dir_path):
            messagebox.showerror('Create folder',
                                          '{}\n\nFile with this name exists!'.format(dir_path))
            return
        elif not os.path.exists(dir_path):
            os.mkdir(dir_path)
            os.chmod(dir_path, mode=0o700)
            self.update()
            self.set_selection_line_by_item(new_name)
        else:
            self.update()
            self.set_selection_line_by_item(item)

    def delete_dir(self):
        file_path = self.get_filepath_selection()
        item_up = self.get_item_selection_up()
        item = self.get_item_selection()
        if item == str_folder_up:
            return
        if not os.access(file_path, os.R_OK):
            messagebox.showerror(title='Deletion Error! ', message='Access is denied!')
            return
        if os.path.isdir(file_path):
            if len(os.listdir(file_path)):
                messagebox.showerror(title='Deletion Error! ', message='Deleting only empty folders is allowed!')
                return
            else:
                if messagebox.askyesno(title='Delete Folder! ',
                                       message='{}\n\nWill be deleted. Confirm?'.format(file_path)):
                    os.rmdir(file_path)
                    self.update()
                    self.set_selection_line_by_item(item_up)

    def chmod_file(self):
        file_path = self.get_filepath_selection()
        item = self.get_item_selection()
        if item == str_folder_up:
            return
        chmod_enter = str(
            subprocess.run(['/usr/bin/zenity', '--entry', '--title', 'Chmode', '--text', '{}\nEnter chmod(format:777):'.format(file_path)],
                           stdout=subprocess.PIPE).stdout.decode()).strip()
        if chmod_enter:
            if self.is_chmod(chmod_enter):
                try:
                    os.chmod(file_path, mode=int(chmod_enter, base=8))
                except:
                    messagebox.showerror('Chmod error',
                                        '{}\nFailed to change file properties!\nThe file does not exist or access is denied!'.format(
                                            file_path))
            else:
                messagebox.showerror('Chmod error',
                                    '{}\nInvalid format or not a number!\nInput format, three-digit number:nnn'.format(
                                        file_path))

    def rename_file(self):
        file_path_old = self.get_filepath_selection()
        item = self.get_item_selection()
        if item == str_folder_up:
            return
        new_name = str(
            subprocess.run(['/usr/bin/zenity', '--entry', '--title', 'Rename file', '--text', 'Old name:\n{}\n\nEnter new name:'.format(os.path.basename(file_path_old))],
                           stdout=subprocess.PIPE).stdout.decode()).strip()

        if new_name:
            file_path_new = os.path.join(self.folder_rab, new_name)
            if os.path.exists(file_path_new):
                messagebox.showerror('Rename file', '{}\n\nFile with this name exists!'.format(file_path_new))
                return
            else:
                os.rename(file_path_old, file_path_new)
                self.update()
                self.set_selection_line_by_item(os.path.basename(file_path_new))

    def MyCopyToOneFolderNoDuble(self):
        pass

    def quit(self):
        self.menu_close()
        self.tree.destroy()
        sys.exit(0)

    def update(self):
        self.insert_in_tree()

    def update_and_set_key_sort_invers(self):
        self.set_key_sort_invers()
        self.update()

    def converter_number_to_gb(self, size):
        KB = 1024.0
        MB = KB * KB
        GB = MB * KB
        if size >= GB:
            return '{:,.1f} Gb'.format(size / GB)
        if size >= MB:
            return '{:,.1f} Mb'.format(size / MB)
        if size >= KB:
            return '{:,.1f} Kb'.format(size / KB)
        return '{} B'.format(size)

    def clear_e_frame1(self):
        if self.folder_rab.endswith('/') and len(self.folder_rab) != 1:
            folder_rab = self.folder_rab[:-1]
        self.e_frame1.delete(0, END)
        self.e_frame1.insert(0, self.folder_rab)
        for i in self.tree.get_children():
            self.tree.delete(i)

    def hide_files_hidden(self, event=''):
        if self.key_hide_files_hidden:
            self.key_hide_files_hidden = 0
        else:
            self.key_hide_files_hidden = 1
        f_select = ' #'
        self.insert_in_tree()

    def set_key_sort_invers(self):
        if self.key_sort_invers:
            # self.dirs_list.reverse()
            # self.files_list.reverse()
            self.key_sort_invers = 0
        else:
            self.key_sort_invers = 1

    def sort_column_by_image(self):
        pass

    def sort_column_by_name(self):
        self.key_sort_by = 'name'
        self.update_and_set_key_sort_invers()

    def sort_column_by_rights(self):
        self.key_sort_by = 'rights'
        self.update_and_set_key_sort_invers()

    def sort_column_by_owner(self):
        self.key_sort_by = 'owner'
        self.update_and_set_key_sort_invers()

    def sort_column_by_group(self):
        self.key_sort_by = 'group'
        self.update_and_set_key_sort_invers()

    def sort_column_by_ext(self):
        self.key_sort_by = 'ext'
        self.update_and_set_key_sort_invers()

    def sort_column_by_size(self):
        self.key_sort_by = 'size'
        self.update_and_set_key_sort_invers()

    def sort_column_by_mtime(self):
        self.key_sort_by = 'mtime'
        self.update_and_set_key_sort_invers()

    def sort_column_by_atime(self):
        self.key_sort_by = 'atime'
        self.update_and_set_key_sort_invers()

    def sort_by_name(self, f_path):
        return os.path.basename(f_path).lower()

    def sort_by_rights(self, f_path):
        return oct(os.stat(f_path).st_mode)[-3:]

    def sort_by_owner(self, f_path):
        return pwd.getpwuid(os.stat(f_path).st_uid).pw_name

    def sort_by_group(self, f_path):
        return grp.getgrgid(os.stat(f_path).st_gid).gr_name

    def sort_by_ext(self, f_path):
        if os.path.isdir(f_path):
            if self.dic_dirs[f_path][1] == 'denied':
                return 0
            return self.dic_dirs[f_path][2]
        return os.path.splitext(f_path)[1].lower()

    def sort_by_size(self, f_path):
        if os.path.isdir(f_path):
            if type(self.dic_dirs[f_path][1]) == str:
                return -1
            return self.dic_dirs[f_path][1]
        if type(self.dic_files[f_path][1]) == str:
            return -1
        return os.path.getsize(f_path)

    def sort_by_mtime(self, f_path):
        return os.path.getmtime(f_path)

    def sort_by_atime(self, f_path):
        return os.path.getatime(f_path)

    def sort_list_files(self, list_files):
        if self.key_sort_by == 'name':
            list_files.sort(key=self.sort_by_name)
        elif self.key_sort_by == 'rights':
            list_files.sort(key=self.sort_by_rights)
        elif self.key_sort_by == 'owner':
            list_files.sort(key=self.sort_by_owner)
        elif self.key_sort_by == 'group':
            list_files.sort(key=self.sort_by_group)
        elif self.key_sort_by == 'ext':
            list_files.sort(key=self.sort_by_ext)
        elif self.key_sort_by == 'size':
            list_files.sort(key=self.sort_by_size)
        elif self.key_sort_by == 'mtime':
            list_files.sort(key=self.sort_by_mtime)
        elif self.key_sort_by == 'atime':
            list_files.sort(key=self.sort_by_atime)
        return list_files

    def is_chmod(self, chmod_enter):
        try:
            int(chmod_enter)
        except:
            return 0
        if len(str(chmod_enter)) != 3:
            return 0
        for i in range(len(str(chmod_enter))):
            if int(str(chmod_enter)[i]) > 7:
                return 0
        return 1

    def help(self, event):
        try:
            self.menu.destroy()
        except:
            pass

        help_txt = '''
Description:
    MyFMTk is a minimal file manager.
    Designed for quick navigation through the list of text, photo and video files.
    After starting the program, double-click on the window header, expand MyFMTk to full screen.

Software requirements:
    The application requires `python3` to run.
    Run the following command to install the required dependencies:
    for Debian, Ubuntu:
    `sudo apt install python3-tk python3-magic python3-pil python3-pil.imagetk`

    for OpenSuse:
    `sudo zypper install python3-tk python3-python-magic python3-Pillow python3-Pillow-tk`
    To clear X resources, type in the console:
    `xrdb -load / dev / null`
    `xrdb -query`
    If python3-magic is installed:
    `sudo zypper remove python3-magic`
    `sudo zypper install python3-python-magic`

Features of the file list:
    names of text, photo and media files are highlighted with a colored background,
    all other files have a white background.
    The name of the selected file is duplicated in the bottom line of the FM window.
    If it is a link, then the full path of the link and the full real path are indicated.

Basic mouse button controls:
    1. Double click on the name of the "File Manager" window:
        FM will expand to full screen and a window will open on the right,
        to view the contents of text files
    2. Double click on the folder address bar:
        a menu for selecting a new folder for work will open
    3. Double click on the name "..."
        go to parent folder
    4. Double click on the folder name:
        go to this folder
    5. Double click on the file name, the file will be launched by the default application
       Following the link is prohibited, so there is no action
    6. Single click on the name of the text file or image (only in full screen mode):
        view file content
        (you can move through the list of files using the up and down arrow keys)
    7. Click the Right mouse button on the address bar - call the folder open menu
    8. Right-click on the file list field - open the file management menu

Sorting files:
    1. Single click on the column name:
        files are sorted according to the name of this column
    2. Click again on the name of the same column:
        reverse sort according to the name of this column

Sorting features:
    1. Column 'Ext':
        folders are sorted by the number of subfolders
    2. Column 'Size':
        folders are sorted by the number of items in the folder

Keyboard Key Control:
    1. cursor arrows "up" and "down" - move through the list of files
    2. "Escape" - close the menu and the "Help" window
    3. "Ctrl + H" show / hide hidden files
        '''

        # sw = self.master.winfo_screenwidth()
        # sh = self.master.winfo_screenheight()
        sw = 770
        sh = 400
        # x = int((sw - w) / 2)
        # y = int((sh - h) / 2)
        self.help = Toplevel()
        self.help.geometry('{}x{}+{}+{}'.format(sw, sh, 0, 0))
        self.help.title('Help for MyFM win2')
        text_window = Text(self.help)  # , width=width_w, height=height_w)
        text_window.pack(side=LEFT, fill=BOTH, expand=True)
        # button = Button(help, text=self.lang_dic['text_button'], command=help.destroy)
        # button.pack(side=BOTTOM)
        text_window.insert(END, help_txt)

        scrollbar1 = Scrollbar(self.help)
        scrollbar1.pack(side=RIGHT, fill=Y)
        text_window.config(yscrollcommand=scrollbar1.set)
        scrollbar1.config(command=text_window.yview)
        self.help.bind('<Escape>', self.menu_close)

    # def save_setup(self):
    #     data_dic = self.get_dic_from_file()
    #     data_dic['folder_rab'] = self.folder_rab
    #     with open(file_config, 'w') as f:
    #         for key in data_dic.keys():
    #             f.write('{} = {}'.format(key, data_dic[key]))
    #
    # def get_default_setup(self):
    #     if not os.path.exists(file_config):
    #         self.set_default_setup()
    #     data_dic = self.get_dic_from_file()
    #     self.folder_rab = data_dic['folder_rab']
    #
    # def set_default_setup(self):
    #     with open(file_config, 'w') as f:
    #         folder_rab = os.getcwd()
    #         f.write('folder_rab = {}'.format(folder_rab))
    #
    # def get_list_from_file(self):
    #     data_list = []
    #     if os.path.exists(file_config):
    #         with open(file_config, 'r') as f:
    #             f_lines = f.readlines()
    #         for f_line in f_lines:
    #             if f_line.strip().startswith(start_switch):
    #                 continue
    #             elif f_line.strip():
    #                 data_list.append(f_line.strip())
    #     else:
    #         self.set_default_setup()
    #         return self.get_list_from_file()
    #     return data_list
    #
    # def get_dic_from_file(self):
    #     data_dic = {}
    #     if os.path.exists(file_config):
    #         with open(file_config, 'r') as f:
    #             lines = f.readlines()
    #         for line in lines:
    #             if line.strip().startswith(start_switch):
    #                 continue
    #             elif line.strip():
    #                 data_dic[line.strip().split('=')[0].strip()] = line.strip().split('=')[1].strip()
    #     else:
    #         return {}
    #     return data_dic
    #
    # def get_dirs_and_files_in_folder(self, folder):
    #     full_f = [os.path.join(folder, f) for f in os.listdir(folder)]
    #     dirs = [d for d in full_f if os.path.isdir(d)]
    #     files = [f for f in full_f if os.path.isfile(f)]
    #     return dirs, files


def MyFM_PFT_v2():
    root = Tk()
    root.title('MyFM_PFT_win2')
    root.geometry('{}x{}+{}+{}'.format(*CenteredWindow(root)))
    # collapsed_icon = PhotoImage(data='R0lGODlhDwANAKIAAAAAAMDAwICAgP//////ADAwMAAAAAAA'
    #                                  'ACH5BAEAAAEALAAAAAAPAA0AAAMyGCHM+lAMMoeAT9Jtm5NDKI4Wo'
    #                                  'FXcJphhipanq7Kvu8b1dLc5tcuom2foAQQAyKRSmQAAOw==')
    # root.iconphoto(False, collapsed_icon)
    app = App(root)
    app.e_frame1.bind('<Double-ButtonRelease-1>', app.open_folder)
    root.bind('<Control-h>', app.hide_files_hidden)
    app.tree.bind('<Double-ButtonRelease-1>', app.line_clicked_double)
    # app.tree.bind('<space>', app.line_clicked_double)
    app.tree.bind('<ButtonRelease-1>', app.preview)
    app.tree.bind('<Button-3>', app.menu_contecst)
    app.e_frame1.bind('<Button-3>', app.menu_folder)
    root.bind('<Escape>', app.menu_close)
    root.bind('<Up>', app.preview)
    root.bind('<Down>', app.preview)
    root.bind('<F1>', app.help)

    root.mainloop()


if __name__ == '__main__':
    MyFM_PFT_v2()
