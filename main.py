import threading #to run the gui and get_awi function at the same time
import time
import json
from win32 import win32gui
from datetime import datetime
from os.path import exists
from tkinter import *
from ctypes import windll

#whether the application is running
running_status = True
 
# exits the gui and saves the info to a json file
def exit():
    global running_status
    running_status = False
    global day_list
    name1, temporal_location1 = map(list, zip(*day_list))
    temporal_location2 = []
    for i in temporal_location1:
        temporal_location2.append(str(i))
    day_list1 = list(zip(name1, temporal_location2))
    with open(str(datetime.today().strftime('%Y-%m-%d'))+".json", "w")as f:
        json.dump(day_list1, f)
    root.quit()
    return running_status
 
#gets the active window info
def get_awi():
 
    global day_list
    day_list = []
 
    active_window_name = ""
 
    new_window_name = ""
 
    name_list = []
 
    if exists(str(datetime.today().strftime('%Y-%m-%d'))+".json"):
            json_file = open(str(datetime.today().strftime('%Y-%m-%d'))+".json")
            day_list_strings = json.load(json_file)
            json_file.close()
            name_strings, temporal_strings = map(list, zip(*day_list_strings))
            deltatime_list = []
            for i in temporal_strings:
                deltatime_list.append(datetime.strptime(i, "%H:%M:%S") - datetime.strptime("0:00:00", "%H:%M:%S"))
            day_list = [list(a) for a in (zip(name_strings, deltatime_list))]       
 
    while running_status == True:
 
        if len(day_list) > 0:
            name_list, temporal_location = map(list, zip(*day_list))
 
        new_window_name = win32gui.GetWindowText(win32gui.GetForegroundWindow())
 
        google_chrome_name = "- Google Chrome"
        discord_name = "- Discord"
 
        if google_chrome_name in new_window_name:
            new_window_name = "Google Chrome"
 
        if discord_name in new_window_name:
            new_window_name = "Discord"
           
        if active_window_name != new_window_name:
            active_window_name = new_window_name
            t = datetime.now()
            initial_time = t.strftime("%H:%M:%S")
            zerotd = t - t
            donkey = t - t
            if active_window_name in name_list:
                donkey = day_list[name_list.index(active_window_name)][1]
        if active_window_name not in name_list:
            initial_active_window_info = [active_window_name, zerotd]
            print(initial_active_window_info)
            day_list.append(initial_active_window_info)
        else:
            t = datetime.now()
            current_time = t.strftime("%H:%M:%S")
            time_running = (datetime.strptime(current_time, "%H:%M:%S") - datetime.strptime(initial_time, "%H:%M:%S"))
            if active_window_name in name_list:
                day_list[name_list.index(active_window_name)][1] = time_running + donkey
            else:
                day_list[name_list.index(active_window_name)][1] = time_running
 
        time.sleep(1)

#displays the gui

def gui():
 
    global root
 
    tk_title = "❤ Penguin Time Tracker"
 
    root=Tk()
    root.title(tk_title)
    root.overrideredirect(True) # turns off the title bar
    root.geometry('500x300+75+75') # set new geometry the + 75 + 75 is where it starts on the screen
    root.iconbitmap("glpenguin.ico") # to show your own icon
    root.minimized = False # only to know if root is minimized
    root.maximized = False # only to know if root is maximized
 
    root.config(bg="#25292e")
    title_bar = Frame(root, bg="#121212", relief='raised', bd=0,highlightthickness=0)
 
 
    def set_appwindow(mainWindow): # to display the window icon on the taskbar,
                                # even when using root.overrideredirect(True
        # Some WindowsOS styles, required for task bar integration
        GWL_EXSTYLE = -20
        WS_EX_APPWINDOW = 0x00040000
        WS_EX_TOOLWINDOW = 0x00000080
        # Magic
        hwnd = windll.user32.GetParent(mainWindow.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
   
        mainWindow.wm_withdraw()
        mainWindow.after(10, lambda: mainWindow.wm_deiconify())
       
 
    def minimize_me():
        root.attributes("-alpha",0) # so you can't see the window when is minimized
        root.minimized = True      
 
 
    def deminimize(event):
        root.focus()
        root.attributes("-alpha",1) # so you can see the window when is not minimized
        if root.minimized == True:
            root.minimized = False                              
           
 
    def maximize_me():
 
        if root.maximized == False: # if the window was not maximized
            root.normal_size = root.geometry()
            expand_button.config(text=" 🗗 ")
            root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
            root.maximized = not root.maximized
            # now it's maximized
           
        else: # if the window was maximized
            expand_button.config(text=" 🗖 ")
            root.geometry(root.normal_size)
            root.maximized = not root.maximized
            # now it is not maximized
 
    # put a close button on the title bar
    close_button = Button(title_bar, text='  ×  ', command=(exit),bg="#10121f",padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
    expand_button = Button(title_bar, text=' 🗖 ', command=maximize_me,bg="#10121f",padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
    minimize_button = Button(title_bar, text=' 🗕 ',command=minimize_me,bg="#10121f",padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
    title_bar_title = Label(title_bar, text=tk_title, bg="#10121f",bd=0,fg='white',font=("Calibri 13 bold"),highlightthickness=0)
 
    # a frame for the main area of the window, this is where the actual app will go
    window = Frame(root, bg="#121212",highlightthickness=0)
 
    # pack the widgets
    title_bar.pack(fill=X)
    close_button.pack(side=RIGHT,ipadx=7,ipady=1)
    expand_button.pack(side=RIGHT,ipadx=7,ipady=1)
    minimize_button.pack(side=RIGHT,ipadx=7,ipady=1)
    title_bar_title.pack(side=LEFT, padx=10)
    #xwin=None
    #ywin=None
    # bind title bar motion to the move window function
 
    def changex_on_hovering(event):
        global close_button
        close_button = Button(title_bar, text='  ×  ', command=root.destroy,bg="#10121f",padx=2,pady=2,font=("calibri", 13),bd=0,fg='white',highlightthickness=0)
        close_button['bg']='red'
       
       
    def returnx_to_normalstate(event):
        global close_button
        close_button['bg']="#10121f"
       
 
    def change_size_on_hovering(event):
        global expand_button
        expand_button = Button(title_bar, text=' 🗖 ', command=maximize_me,bg="#10121f",padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
        expand_button['bg']="#3e4042"
       
       
    def return_size_on_hovering(event):
        global expand_button
        expand_button['bg']="#10121f"
       
 
    def changem_size_on_hovering(event):
        global minimize_button
        minimize_button = Button(title_bar, text=' 🗕 ',command=minimize_me,bg="#10121f",padx=2,pady=2,bd=0,fg='white',font=("calibri", 13),highlightthickness=0)
        minimize_button['bg']="#3e4042"
       
       
    def returnm_size_on_hovering(event):
        global minimize_button
        minimize_button['bg']="#10121f"
       
 
    def get_pos(event): # this is executed when the title bar is clicked to move the window
 
        if root.maximized == False:
   
            xwin = root.winfo_x()
            ywin = root.winfo_y()
            startx = event.x_root
            starty = event.y_root
 
            ywin = ywin - starty
            xwin = xwin - startx
 
           
            def move_window(event): # runs when window is dragged
                root.config(cursor="fleur")
                root.geometry(f'+{event.x_root + xwin}+{event.y_root + ywin}')
 
 
            def release_window(event): # runs when window is released
                root.config(cursor="arrow")
               
               
            title_bar.bind('<B1-Motion>', move_window)
            title_bar.bind('<ButtonRelease-1>', release_window)
            title_bar_title.bind('<B1-Motion>', move_window)
            title_bar_title.bind('<ButtonRelease-1>', release_window)
        else:
            expand_button.config(text=" 🗖 ")
            root.maximized = not root.maximized
 
    title_bar.bind('<Button-1>', get_pos) # so you can drag the window from the title bar
    title_bar_title.bind('<Button-1>', get_pos) # so you can drag the window from the title
 
    # button effects in the title bar when hovering over buttons
    close_button.bind('<Enter>',changex_on_hovering)
    close_button.bind('<Leave>',returnx_to_normalstate)
    expand_button.bind('<Enter>', change_size_on_hovering)
    expand_button.bind('<Leave>', return_size_on_hovering)
    minimize_button.bind('<Enter>', changem_size_on_hovering)
    minimize_button.bind('<Leave>', returnm_size_on_hovering)
 
    # resize the window width
    resizex_widget = Frame(window,bg="#25292e",cursor='sb_h_double_arrow')
    resizex_widget.pack(side=RIGHT,ipadx=2,fill=Y)
 
 
    def resizex(event):
        xwin = root.winfo_x()
        difference = (event.x_root - xwin) - root.winfo_width()
       
        if root.winfo_width() > 150 : # 150 is the minimum width for the window
            try:
                root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
            except:
                pass
        else:
            if difference > 0: # so the window can't be too small (150x150)
                try:
                    root.geometry(f"{ root.winfo_width() + difference }x{ root.winfo_height() }")
                except:
                    pass
               
        resizex_widget.config(bg="#25292e")
 
    resizex_widget.bind("<B1-Motion>",resizex)
 
    # resize the window height
    resizey_widget = Frame(window,bg="#25292e",cursor='sb_v_double_arrow')
    resizey_widget.pack(side=BOTTOM,ipadx=2,fill=X)
 
    def resizey(event):
        ywin = root.winfo_y()
        difference = (event.y_root - ywin) - root.winfo_height()
 
        if root.winfo_height() > 150: # 150 is the minimum height for the window
            try:
                root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
            except:
                pass
        else:
            if difference > 0: # so the window can't be too small (150x150)
                try:
                    root.geometry(f"{ root.winfo_width()  }x{ root.winfo_height() + difference}")
                except:
                    pass
 
        resizex_widget.config(bg="#25292e")
 
    resizey_widget.bind("<B1-Motion>",resizey)
 
    # some settings
    root.bind("<FocusIn>",deminimize) # to view the window by clicking on the window icon on the taskbar
    root.after(10, lambda: set_appwindow(root)) # to see the icon on the task bar
 
    root.iconbitmap("glpenguin.ico")
 
    frame1 = Frame(window, bg="#121212", highlightthickness=0)
    frame2 = Frame(window, bg="#121212", highlightthickness=0)
    frame3 = Frame(window, bg="#121212", highlightthickness=0)
   
    my_listbox = Listbox(frame2, font=("Calibri", 15), bg="#121212",fg="#fff", highlightbackground="#1F1B24")
    my_listbox2 = Listbox(frame3, font=("Calibri", 15), bg="#121212",fg="#fff", highlightbackground="#1F1B24")
   
    window.pack(fill=BOTH)
    frame1.pack(fill=X)
    frame2.pack(fill=BOTH, side=LEFT, expand=True)
    my_listbox.pack(side=TOP,ipadx=7,ipady=1, fill=BOTH, expand=True)
    frame3.pack(fill=BOTH, side=LEFT, expand=True)
    my_listbox2.pack(side=TOP,ipadx=7,ipady=1, fill=BOTH, expand=True)
 
    def clock():
 
        global day_list
        if day_list != []:
            for i in day_list:
                if i[0] == "":
                    day_list.remove(i)
                if i[0] == "Search":
                    day_list.remove(i)
                if i[0] == "Task Switching":
                    day_list.remove(i)
            my_listbox.delete(0, END)
            my_listbox2.delete(0, END)
            n1, tl1 =map(list, zip(*day_list))
            for i in n1:
                i_string = str(i)
                if len(i) > 0:
                    i_capital = i_string[0].upper() + i_string[1:]
                    my_listbox.insert(END, i_capital)
            for i in tl1:
                my_listbox2.insert(END, i)
        root.after(100, clock)
 
    clock()
 
    root.mainloop()

#sets the functions to run as separate threads
t1 = threading.Thread(target=get_awi)
t2 = threading.Thread(target=gui)
 
#runs the threads    
t1.start()
t2.start()
