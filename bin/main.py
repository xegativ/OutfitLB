# Cleaning code from main
# removing use of global variables

import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk

# removal of prefix
from ouser import *
"""
class ClosetPopUp(tk.Frame):
    def __init__(self, parent):
        self.top = tk.Toplevel(parent)
        self.l = tk.Label(self.top, text="Closet Name")
"""

class OutfitFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.test = tk.Label(self, text="HELLO")
        self.test.grid(row=0,column=0)

class PreviewFrame(tk.Frame):
    def __init__(self, parent, all_clothing, clothing_lb, *args, **kwargs):
        # not using super because tkinter uses old way
        tk.Frame.__init__(self, parent, width=5, *args, **kwargs)
        self.parent = parent

        self.all_clothing = all_clothing
        self.clothing_lb = clothing_lb

        self.filepath_current = "image.jpg"
        self.image_current = Image.open(self.filepath_current).resize((50, 50))        
        self.image_current = ImageTk.PhotoImage(self.image_current)

        # default no image
        self.prev_image = tk.Label(self, image=self.image_current)

        # <> CLOTHING PANEL PREVIEW
        self.prev_label_var = tk.StringVar()
        self.prev_label = tk.Label(self, textvariable=self.prev_label_var, font=("Helvetica", 10),justify= tk.LEFT) 
        
        # <> PRINTING PREVIEW DATA
        self.getPreview()

        # <> WIDGET DISPLAY
        self.widgetDisplay()

    def getPreview(self):
        
        # gets selected item in listbox
        self.prev_select = self.clothing_lb.curselection()
        # gets value of selected
        # gets index of selected
        print(f"Index: {self.prev_select[0]}")
        print(self.all_clothing[self.prev_select[0]].print_info())
        # check if no listbox item selected
        if not self.prev_select:
            print("[!] None selected.")
            self.prev_label_var.set("None selected.")
            self.prev_label = tk.Label(self.parent, textvariable=self.prev_label_var, font=("Helvetica", 10),justify= tk.LEFT) 
            self.prev_image = tk.Label(self.parent, text="No image.")
        else:
            print("[!] Selected")
            #strvar.set(clothing_lb.get(c_selection))
            self.prev_label_var.set(self.all_clothing[self.prev_select[0]].get_info())
            self.prev_label['textvariable']=self.prev_label_var
            # getting and displaying current clothing image
            self.filepath_current = self.all_clothing[self.prev_select[0]].get_image()
            if not self.filepath_current or self.filepath_current.isspace():
                self.filepath_current = "image.jpg"
                print("[!] No image for current")

            self.image_current = Image.open(self.filepath_current).resize((100, 100))
            self.image_current = ImageTk.PhotoImage(self.image_current)
            self.prev_image.configure(image=self.image_current)
            # prevent garbage collection
            self.prev_image.image = self.image_current

    def widgetDisplay(self):
        # clothing preview (right of all clothing list)
        self.prev_label.grid(row=1,column=4,sticky="W")
        self.prev_image.grid(row=0,column=4,sticky="W")

class ClosetFrame(tk.Frame):
    def __init__(self, parent, user, *args, **kwargs):
        # not using super because tkinter uses old way
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.user = user

        # <> NAV BAR
        self.navbar_frame = tk.Frame(self)

        # <> LEFT LIST AND RIGHT PREVIEW
        self.lb_frame = tk.Frame(self)
        self.lb_preview = tk.Frame(self)
        self.addframe = tk.Frame(self)

        self.navBar()        

        # Scrollbar and Listbox
        self.sb = tk.Scrollbar(self.lb_frame, orient=tk.VERTICAL) 
        # display current list box of closet
        self.clothing_lb = tk.Listbox(self.lb_frame, yscrollcommand = self.sb.set, height = 10, width = 25,activestyle = 'dotbox',font = ("Helvetica",10),fg = "white")
        self.sb['command'] = self.clothing_lb.yview
        
        # <> PREVIEW BUTTON
        self.prev_b = tk.Button(self.lb_preview, text='Preview', command=self.callPreview)
        
        # + EXAMPLE DATA
        self.all_clothing = self.user.get_closet('0').get_all()
        self.example_data()

        # <> ADD SECTION
         # Left type + image frame
        # Right info frame
        self.type_frame = tk.Frame(self)
        self.info_frame = tk.Frame(self)

        # init no image filepath
        self.filepath_add=""

        self.addType()
        self.addInfo()

        # <> WIDGET DISPLAY
        self.widgetDisplay()

    def navBar(self):
        # <> CLOSET DISPLAY
        # Dropdown menu
        self.dropdown_var = tk.StringVar()
        self.dropdown = ttk.Combobox(self.navbar_frame, textvariable=self.dropdown_var, values=self.user.get_all_closet_comb())
        self.dropdown.current(0)
        self.dropdown.bind("<<ComboboxSelected>>", self.dropdown_callback)

        # Add closet
        self.add_closet_b = tk.Button(self.navbar_frame, text="New closet", command=lambda: self.addCloset_expand())

        # Delete closet
        self.delete_closet_b = tk.Button(self.navbar_frame, text="Delete", command=lambda: self.deleteCloset())

    def addCloset_expand(self):
        self.add_closet_b.destroy()

        add_c_name = tk.StringVar()
        add_c_name.set("Closet-Name")
        add_c_id = tk.IntVar()
        add_c_id.set("ID")
        self.add_closet_name = tk.Entry(self.navbar_frame, textvariable=add_c_name, width=20)
        self.add_closet_id = tk.Entry(self.navbar_frame, textvariable=add_c_id, width=10)
        self.add_closet_b2 = tk.Button(self.navbar_frame, text="Add", command=lambda: self.addCloset())

        self.add_closet_name.grid(row=0,column=1,sticky="NW")
        self.add_closet_id.grid(row=0,column=2,sticky="NW")
        self.add_closet_b2.grid(row=0,column=3,sticky="NW")
        
    
    def addCloset(self):
        print(f"[+] Added new closet: {self.add_closet_name.get()}, {self.add_closet_id.get()}")
        self.user.new_closet(self.add_closet_name.get(),self.add_closet_id.get())

        # DELETE AND REVERT TO INITIAL NAVBAR
        self.add_closet_name.destroy()
        self.add_closet_id.destroy()
        self.add_closet_b2.destroy()

        # Add closet
        self.add_closet_b = tk.Button(self.navbar_frame, text="New closet", command=lambda: self.addCloset_expand())
        self.add_closet_b.grid(row=0,column=1,sticky="NW")

        # Update dropdown menu
        self.dropdown['values'] = self.user.get_all_closet_comb()

        print(f"[=] All closet name: {self.user.get_all_closet_name()}")
        print(f"[=] All closet id: {self.user.get_all_closet_id()}")
        #print(f"First closet: {self.user.get_closet('0')}")

    def deleteCloset(self):
        self.mb_confirm = tk.messagebox.askyesno(title="Delete confirmation", message=f"Are you sure you want to delete closet: {self.dropdown.get()}")
        
        if self.mb_confirm:
            print(f"[X] Deleted closet: {self.dropdown.get().split()[1]}")
            self.user.delete_closet(self.dropdown.get().split()[1])
            # Update dropdown menu
            self.dropdown['values'] = self.user.get_all_closet_comb()
            # CLEAR
            self.clothing_lb.delete(0,tk.END)
            self.dropdown.set('')


    #DEBUG
    def dropdown_callback(self,*args):
        # UPDATE
        print("[>] Closet selected: ", self.dropdown.get())

        # CLEAR
        self.clothing_lb.delete(0,tk.END)
        self.all_clothing = []

        # Get closet by splitting dropdown value and taking the id part since first element of 
        # dropdown.get() since "name + id"
        self.all_clothing = self.user.get_closet(self.dropdown.get().split()[1]).get_all()
        
        for i, clothing in enumerate(self.all_clothing):
            self.clothing_lb.insert(i, clothing.get_name())

            print(f"[+] {clothing.get_name()}")
            print(f"\t[=] CLEAN:{clothing.is_clean()}")
            
            if clothing.is_clean():
                self.clothing_lb.itemconfig(i,{'bg':'Green'})
            else:
                self.clothing_lb.itemconfig(i,{'bg':'Red'})

    def save_to_user(self):
        self.user.save_closet(self.all_clothing,self.dropdown.get().split()[1])
                
    def callPreview(self):
        """
        Creates a preview frame and changes the contents of such preview frame.
        Then places the preview frame using grid. 
        """
        self.previewframe = PreviewFrame(self.lb_preview, self.all_clothing, self.clothing_lb) # maybe self.lb_preview?
        self.previewframe.grid(row=0,column=2,sticky="W")

    def addInfo(self):
        # Name frame
        self.add_n_l = tk.Label(self.info_frame, text="Name",justify= tk.LEFT)
        self.add_n_en = tk.Entry(self.info_frame, width=20)

        # Description frame
        self.add_d_l = tk.Label(self.info_frame, text="Description",justify= tk.LEFT)
        self.add_d_txt = tk.Text(self.info_frame, width=15,height=2)

        # Clean? checklist w/ Description frame
        self.clean_var =  tk.IntVar()
        self.add_clean_b = tk.Checkbutton(self.info_frame, text = "Clean?", variable=self.clean_var)

        # Button submit
        self.add_sm_b = tk.Button(
            self.info_frame,
            text="ADD", 
            padx=10, 
            pady=5,
            command=lambda: self.addClothing()
            )

    def addType(self):
        self.type_var = tk.IntVar(self.parent, 0) # default value is top
        self.add_rb_t = tk.Radiobutton(self.type_frame, text="Top", variable=self.type_var, value=0)
        self.add_rb_b = tk.Radiobutton(self.type_frame, text="Bottom", variable=self.type_var, value=1)
        self.add_rb_s = tk.Radiobutton(self.type_frame, text="Shoes", variable=self.type_var, value=2)

        self.add_image_b = tk.Button(self.type_frame, text="Image", command=lambda: self.imageUpload())

        # SAVE 
        self.closet_save_b = tk.Button(self.type_frame, text='Save closet', command=lambda: self.save_to_user())
            
    def imageUpload(self):
        # clear current filepath
        self.filepath_add = ""
        # uploading file (image)
        self.filepath_add = filedialog.askopenfilename(filetypes = (("jpeg files", "*.jpg"),("png files", "*.png"),("all files","*.*")))
        
        # DEBUG
        print(f">> Updated filepath to: {self.filepath_add}")

    # Add clothing to clothing list function
    def addClothing(self):
        # check if valid closet
        try:
            if self.user.get_closet(self.dropdown.get().split()[1]):
                print("[!] Closet exists")
            # get name and description 
            self.add_n_var = self.add_n_en.get()
            self.add_d_var = self.add_d_txt.get("1.0",tk.END).replace('\n',' ')
            #new_c_name = str(input())

            # If empty string, use no name
            if not self.add_n_var or self.add_n_var.isspace():
                self.add_n_var = "No name"

            # debug print
            print(f"[+ type:{self.type_var.get()}] {self.add_n_var}")

            # Adding to clothing list -> type check
            match self.type_var.get():
                case 0:
                    self.all_clothing.append(Top(self.add_n_var, self.add_d_var, "Custom", clean=self.clean_var.get(), filepath=self.filepath_add))
                case 1:
                    self.all_clothing.append(Bottom(self.add_n_var, self.add_d_var, "Custom", clean=self.clean_var.get(), filepath=self.filepath_add))
                case 2:
                    self.all_clothing.append(Shoes(self.add_n_var, self.add_d_var, "Custom", clean=self.clean_var.get(), filepath=self.filepath_add))
            
            # RESET filepath
            self.filepath_add=""
            
            # Check if clean
            if self.clean_var.get():#[].is_clean():
                self.clothing_lb.insert(tk.END, self.add_n_var)
                self.clothing_lb.itemconfig(tk.END,{'bg':'Green'})
            else:
                self.clothing_lb.insert(tk.END, self.add_n_var)
                self.clothing_lb.itemconfig(tk.END,{'bg':'Red'})
        except:
            tk.messagebox.showwarning(title="Closet error", message="Closet does not exist!")
            print("[!] Closet does not exist")
        
    # WIDGET DISPLAYING
    # GRID FORMAT
    def widgetDisplay(self):
        """
        MAIN FRAME 
        """
        self.navbar_frame.grid(row=0,column=0,columnspan=6,sticky="NW")
        self.lb_frame.grid(row=1,column=0,columnspan=3)
        self.type_frame.grid(row=2, column=0)
        self.info_frame.grid(row=2, column=1)
        #addClothing_en.grid(row=1,column=1,rowspan=1,sticky="N")
        # name 
        self.addframe.grid(row=1,column=0,rowspan=3,sticky="NW")
        self.lb_preview.grid(row=1,column=3)

        """
        LISTBOX FRAME
        """
        # ALL CLOTHING FRAME
        self.dropdown.grid(row=0,column=0,sticky="NW")
        self.add_closet_b.grid(row=0,column=1,sticky="NW")
        self.delete_closet_b.grid(row=0,column=4,sticky="NW")

        # lb_frame
        self.clothing_lb.grid(row=0,column=0,columnspan=3)
        self.sb.grid(row=0,column=2, sticky='NSE')

        # lb_preview
        self.prev_b.grid(row=0,column=1,sticky="W")

        """
        INFO ADD FRAME 
        """
        self.add_n_l.grid(row=0,column=0,sticky="W")
        self.add_n_en.grid(row=1,column=0,sticky="N")

        # description
        self.add_d_l.grid(row=2,column=0,sticky="W")
        self.add_d_txt.grid(row=3,column=0,rowspan=1,sticky="N")
        self.add_clean_b.grid(row=4,column=0,rowspan=1,sticky="N")

         # button submit
        self.add_sm_b.grid(row=5,column=0, sticky="S")
        
        """
        TYPE FRAME 
        """
        self.add_rb_t.grid(row=0,column=0,sticky="W")
        self.add_rb_b.grid(row=1,column=0,sticky="W")
        self.add_rb_s.grid(row=2,column=0,sticky="W")
        # add image (under clothing type)
        self.add_image_b.grid(row=3,column=0,rowspan=1,sticky="N")
        
        self.closet_save_b.grid(row=6,column=0)


    def example_data(self):
        shirt_1 = Top("Blue Shirt", "Blue shirt I bought at Wendy's")
        shirt_2 = Top("Black Shirt", "Black shirt I bought at McDonald's")
        shirt_3 = Top("Red Shirt", "Red shirt I bought at Arby's", clean=False)

        self.all_clothing.append(shirt_1)
        self.all_clothing.append(shirt_2)
        self.all_clothing.append(shirt_3)

        print("ADDING CLOTHING...")

        for i, clothing in enumerate(self.all_clothing):
            self.clothing_lb.insert(i, clothing.get_name())
            print(f"[+] {clothing.get_name()}")

            if clothing.is_clean():
                self.clothing_lb.itemconfig(i,{'bg':'Green'})
            else:
                self.clothing_lb.itemconfig(i,{'bg':'Red'})

        print("FINISHED ADDING CLOTHING")

class MainApplication(tk.Frame):
    def __init__(self, parent, user, *args, **kwargs):
        # not using super because tkinter uses old way
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.user = user
        self.cframe = ClosetFrame(self, self.user)
        self.oframe = OutfitFrame(self)


        parent.geometry('650x500')
        parent.title("Outfit Manager")

        # frame storing and management
        self.all_frames = {}
        self.all_frames['CFRAME'] = self.cframe
        self.all_frames['OFRAME'] = self.oframe 

        # widget placement
        self.grid(padx=5, pady=5)
        self.cframe.grid(row=0,column=0,sticky="news")
        self.oframe.grid(row=0,column=0,sticky="news")
        self.parent.rowconfigure(0, weight=1)
        self.parent.columnconfigure(0, weight=1)

        # SHOW FRAME
        self.showFrame('CFRAME')

    def showFrame(self, page_name):
        current_frame = self.all_frames[page_name]
        current_frame.tkraise()

    
def main(): 
    agl13 = User("GH", "Andrew", "agl13")
    agl13.new_closet("AC",'0')
    agl13.new_closet("Buster-Wolf",'1')

    root = tk.Tk()
    MainApplication(root, agl13)
    root.mainloop()


if __name__ == '__main__':
    main()