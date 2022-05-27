import sys
from tkinter import *
from os import path
from tkinter import messagebox
from tkinter.font import BOLD, Font
from PIL import ImageTk, Image
from random import randint
from Connection import contact, update

if getattr(sys, 'frozen', False):
    folder = path.dirname(sys.executable)
elif __file__:
    folder = path.dirname(__file__)

#c:\Dev\Py\tkinter\Agenda

iconspath = folder+'\\Icons\\'

class Addbook:
    
    def __init__(self, icons):
        self.icons = icons
        self.root = Tk()
        self.iconcntb = ImageTk.PhotoImage(Image.open(icons[0]).resize((35,35)))
        self.iconcntb_B = ImageTk.PhotoImage(Image.open(icons[0]).resize((45,45)))
        self.iconcntg = ImageTk.PhotoImage(Image.open(icons[1]).resize((35,35)))
        self.iconcntg_B = ImageTk.PhotoImage(Image.open(icons[1]).resize((45,45)))
        self.iconcnty = ImageTk.PhotoImage(Image.open(icons[2]).resize((35,35)))
        self.iconcnty_B = ImageTk.PhotoImage(Image.open(icons[2]).resize((45,45)))
        self.iconlupa = ImageTk.PhotoImage(Image.open(icons[3]).resize((20,20)))
        self.iconppl = ImageTk.PhotoImage(Image.open(icons[4]).resize((20,20)))
        self.iconadd = ImageTk.PhotoImage(Image.open(icons[5]).resize((40,40)))
        self.iconback = ImageTk.PhotoImage(Image.open(icons[6]).resize((30,30)))
        self.iconx = ImageTk.PhotoImage(Image.open(icons[7]).resize((30,30)))
        self.icon_ico = ImageTk.PhotoImage(Image.open(icons[9]).resize((100,100)))
        
        self.iconscnt = [self.iconcntb, self.iconcntg, self.iconcnty, self.iconcntb_B, self.iconcntg_B, self.iconcnty_B]
        self.iconsbg = ['#426970','#44854d','#9f8b3c']

        self.font_ttl = Font(font=('Garamond', 18, BOLD))
        self.font_subttl = Font(font=('Garamond', 14))
        self.font_lbl = Font(font=('Garamond', 12))

        '''Root config'''
        self.root.geometry('330x480')
        self.root.resizable(width=False, height=False)
        self.root.title('AddressBook')
        self.root.iconbitmap(icons[8])

        '''Contacts list'''
        self.cntlst = []
        
        self.display_intro()
        self.root.update()
        self.root.after(3000, self.display_main(intro=True))
        self.root.mainloop()
    
    def display_intro(self):
        self.frm_intro = Frame(self.root, width=330, height=480, bg='#19a993')
        self.frm_intro.pack(fill='both')
        self.frm_intro.grid_propagate(0)
        self.frm_intro.rowconfigure([0,1], minsize=240)
        self.frm_intro.columnconfigure(0, minsize=330)
        
        labelimg = Label(self.frm_intro, image=self.icon_ico, bg='#19a993')
        labelimg.grid(row=0,column=0, sticky='s')
        
        label_ttl = Label(self.frm_intro, text='AddressBook', font=self.font_ttl, fg='#e6b045', bg='#19a993')
        label_ttl.grid(row=1,column=0, sticky='n')
        
        label_firm = Label(self.frm_intro, text='Max Garcia - 2022', font=self.font_lbl, bg='#19a993', fg='white')
        label_firm.grid(row=1,column=0, sticky='s', pady=3)

    def display_main(self, add=False, det=False, srch=False, intro=False):
        '''Main Frame'''
        if add: self.frmadd.destroy()
        if det: self.frmdet.destroy()
        if intro: self.frm_intro.destroy()

        self.frmain = Frame(self.root)
        self.frmain.pack()
        
        #Title Frame
        frmttl = Frame(self.frmain, bg='#19a993')
        frmttl.pack(fill=X)
        lblttl = Label(frmttl, bg='#19a993', fg='#e6b045', text='Contacts', font=self.font_ttl)
        lblttl.pack(fill=X, ipady=4)
        cnvline = Canvas(frmttl, height=0, highlightbackground='#e6b045')
        cnvline.pack()

        #Search Frame
        frmsrch = Frame(frmttl, bg='#19a993')
        frmsrch.pack(fill=X, pady=5)
        btnlupa = Button(frmsrch, relief=FLAT, image=self.iconlupa, bd=0, height=39, bg='#EBEBEB', cursor='hand2')
        btnlupa.pack(side=LEFT, ipadx=14, padx=(8,0))
        entry = Entry(frmsrch, bd=0, bg='#EBEBEB', width=27, fg='#606060', font=self.font_lbl)
        entry.pack(side=LEFT, fill=Y)
        
        if not srch: entry.insert(0,'Buscar...')
        else: entry.insert(0, srch)
        
        labelppl = Label(frmsrch, bg='#19a993', image=self.iconppl)
        btnppl = Button(frmsrch, bg='#19a993', image=self.iconx, relief=FLAT, bd=0, 
                        activebackground='#19a993', cursor='hand2')

        entry.bind('<FocusIn>', lambda event: self.search_focus(event, btnlupa, btnppl, labelppl, srch))
        if not srch: labelppl.pack(side=RIGHT, fill=Y, padx=(0,14))
        else: btnppl.pack(side=RIGHT, fill=Y, padx=(0,11))
        btnppl.bind('<1>', lambda x: self.search_cancel(entry))

        #Contacts frame
        frmcnt = Frame(self.frmain, bg='white')
        frmcnt.pack(fill=X)
        cnvcnt = Canvas(frmcnt, height=373, width=312, highlightthickness=0, bg='white')
        cnvcnt.pack(fill=BOTH, side=LEFT)
        frmcnv = Frame(cnvcnt, bg='white')
        scrll = Scrollbar(frmcnt, command=cnvcnt.yview)
        scrll.pack(side=RIGHT, fill=BOTH)
        btnchng = Button(frmcnt, image=self.iconadd, relief='flat', bd=0, command=self.display_add, cursor='hand2', bg='white')
        btnchng.place(x=260, y=300)

        #Scroll Config
        cnvcnt.configure(yscrollcommand=scrll.set)
        cnvcnt.bind('<Configure>', lambda e: cnvcnt.configure(scrollregion=cnvcnt.bbox('all')))
        cnvcnt.bind('<Enter>', self.Enter_on_cnv)
        cnvcnt.bind('<Leave>', self.Leave_cnv)
        cnvcnt.create_window((0,0), window=frmcnv, anchor='nw', width=312)

        #Contact frames
        lblempty = Label(frmcnv, text='The contacts you add will be displayed here', fg='#606060', font=self.font_lbl, bd=0, bg='white')
        lblsrch = Label(frmcnv, text='No contact matches the search', fg='#606060', font=self.font_lbl, bd=0, bg='white')
        
        self.cntlst = update()
        frmcnts = []
        if len(self.cntlst)>0:
            lblempty.forget()
            for x in range(len(self.cntlst)):
                frmcnts.append([Frame(frmcnv, cursor='hand2', bd=2, bg='white')])
                frmcnts[x].append(Label(frmcnts[x][0], image=self.iconscnt[int(self.cntlst[x][4])], height=50, width=50, bg='white'))
                frmcnts[x].append(Label(frmcnts[x][0], text= self.cntlst[x][1], font=self.font_lbl, bg='white'))
                frmcnts[x][0].bind('<Enter>', lambda event,frmnum=x:self.Enter_on_frm(event,frmnum))
                frmcnts[x][0].bind('<Leave>', lambda event,frmnum=x:self.Leave_on_frm(event,frmnum))
                if not srch:
                    frmcnts[x][0].pack(fill=X, pady=8, padx=8)
                    frmcnts[x][1].pack(side=LEFT)
                    frmcnts[x][2].pack(side=LEFT)
                elif srch.lower() in self.cntlst[x][1].lower():
                    frmcnts[x][0].pack(fill=X, pady=8, padx=8)
                    frmcnts[x][1].pack(side=LEFT)
                    frmcnts[x][2].pack(side=LEFT)
            if len(frmcnv.pack_slaves())==0:
                lblsrch.pack(fill=BOTH, ipady=3)
        else:
            lblempty.pack(fill=BOTH, ipady=3)
        
    def display_add(self):
        '''Add Frame'''
        self.frmain.destroy()
        
        self.frmadd = Frame(self.root, bg='white')
        self.frmadd.pack(fill=BOTH)

        #Title Frame
        frmttl = Frame(self.frmadd)
        frmttl.pack(fill=X, side=TOP)
        lblttl = Label(frmttl, bg='#19a993', fg='#e6b045', text='Add Contact', font=self.font_ttl)
        lblttl.pack(fill=X, ipady=4)
        cnvline = Canvas(frmttl, height=0, highlightbackground='#e6b045')
        cnvline.pack()
        btnback = Button(frmttl, text='back', relief=FLAT, bd=0,
                              image=self.iconback, bg='#19a993', cursor='hand2', 
                              command= lambda x=1: self.display_main(add=True), activebackground='#19a993')
        btnback.place(x=10, y=5)
        
        #New contact details
        cnticon = randint(3,5)
        frmcnt = Frame(self.frmadd, relief=SOLID, bd=1, highlightthickness=1)
        frmcnt.pack(fill=BOTH, padx=33, pady=97)
        frmcnt.columnconfigure(1, minsize=181)
        lblicon = Label(frmcnt, image=self.iconscnt[cnticon], anchor='center', bg=self.iconsbg[cnticon-3])
        lblicon.grid(row=0, column=0, columnspan=4, sticky='nsew', pady=(0,8), ipady=4)
        
        lblcnt = Label(frmcnt, text='Name: ', font=self.font_subttl)
        lblcnt.grid(row=1, column=0, sticky='ew', padx=(15,0), pady=8)
        lblcnt = Label(frmcnt, text='Phone: ', font=self.font_subttl)
        lblcnt.grid(row=2, column=0, sticky='ew', padx=(15,0), pady=8)
        lblcnt = Label(frmcnt, text='Email: ', font=self.font_subttl)
        lblcnt.grid(row=3, column=0, sticky='ew', padx=(15,0), pady=8)
        
        entname = Entry(frmcnt, bd=1, bg='#EBEBEB', fg='#606060', font=self.font_lbl)
        entname.grid(row=1, column=1, sticky='ew', padx=(0,8))
        entphn = Entry(frmcnt, bd=1, bg='#EBEBEB', fg='#606060', font=self.font_lbl)
        entphn.grid(row=2, column=1, sticky='ew', padx=(0,8))
        enteml = Entry(frmcnt, bd=1, bg='#EBEBEB', fg='#606060', font=self.font_lbl)
        enteml.grid(row=3, column=1, sticky='ew', padx=(0,8))
        
        #bottom buttons
        btnsv = Button(self.frmadd, bg='#19a993', text='Save', relief=GROOVE, bd=1, fg='white',
                            font=self.font_subttl, cursor='hand2', highlightthickness=0, 
                            command=lambda x=1: self.add_cnt(entname.get(),entphn.get(),enteml.get(),cnticon-3))
        btnsv.pack(fill=X, ipady=5)

    def display_details(self, cnt, event=False, updt=False):
        ''''Details Frame'''
        if updt: self.frmupdt.destroy() 
        else: 
            self.frmain.destroy()
            event.widget.unbind_all('<1>')
        
        self.frmdet = Frame(self.root, bg='white')
        self.frmdet.pack(fill=BOTH)
        
        #Cnt image
        frmttl = Frame(self.frmdet)
        frmttl.pack(fill=X)
        frmttl.columnconfigure(0, minsize=330)

        lblimg = Label(frmttl, image=self.iconscnt[int(cnt[4])+3], bg=self.iconsbg[int(cnt[4])])
        lblimg.grid(row=0, column=0, rowspan=2, sticky='ew', ipady=50)
        lblname = Label(frmttl, text=cnt[1], bg=self.iconsbg[int(cnt[4])], font=self.font_subttl, fg='white')
        lblname.grid(row=1, column=0, sticky='sew', pady=(0,10))
        btnback = Button(frmttl, text='back', relief=FLAT, bd=0, image=self.iconback, bg=self.iconsbg[int(cnt[4])], 
                        cursor='hand2', command=lambda x=1: self.display_main(det=True),
                        activebackground=self.iconsbg[int(cnt[4])])
        btnback.place(x=10, y=7)
        
        #Cnt info
        frmcnt = Frame(self.frmdet, relief=SOLID, bd=1, highlightthickness=1)
        frmcnt.pack(fill=BOTH, padx=10, pady=(30,165))
        frmcnt.columnconfigure(1, minsize=181)
        
        lblcnt = Label(frmcnt, text='Phone: ', font=self.font_subttl)
        lblcnt.grid(row=0, column=0, sticky='ew', padx=(15,0), pady=8)
        lblcnt = Label(frmcnt, text='Email: ', font=self.font_subttl)
        lblcnt.grid(row=1, column=0, sticky='ew', padx=(15,0), pady=8)
        
        lblphn = Label(frmcnt, fg='#606060', font=self.font_subttl, text=cnt[2])
        lblphn.grid(row=0, column=1, sticky='w', padx=(0,8))
        lbleml = Label(frmcnt, fg='#606060', font=self.font_subttl, text=cnt[3])
        lbleml.grid(row=1, column=1, sticky='w', padx=(0,8))
        
        #bottom buttons
        frmbtn = Frame(self.frmdet, bg='#19a993')
        frmbtn.pack(fill=X, side='bottom')
        frmbtn.columnconfigure([0,1], minsize=165)
        btndel = Button(frmbtn, bg='#19a993', text='Delete', relief=GROOVE, bd=2, fg='white', highlightthickness=0,
                        font=self.font_subttl, cursor='hand2', command= lambda id=cnt[0]: self.del_cnt(id))
        btndel.grid(row=0, column=0, sticky='ew', ipady=6)
        btnupdt = Button(frmbtn, bg='#19a993', text='Update', relief=GROOVE, bd=2, fg='white',
                        font=self.font_subttl, cursor='hand2', command= lambda cnt=cnt: 
                        self.display_updt(cnt), highlightthickness=0)
        btnupdt.grid(row=0, column=1, sticky='ew', ipady=6)
    
    def display_updt(self, cnt):
        '''Update Frame'''
        self.frmdet.destroy()
        
        self.frmupdt = Frame(self.root, bg='white')
        self.frmupdt.pack(fill=BOTH)

        #Title Frame
        frmttl = Frame(self.frmupdt)
        frmttl.pack(fill=X, side=TOP)
        lblttl = Label(frmttl, bg='#19a993', fg='#e6b045', text='Update Contact', font=self.font_ttl)
        lblttl.pack(fill=X, ipady=4)
        cnvline = Canvas(frmttl, height=0, highlightbackground='#e6b045')
        cnvline.pack()
        btnback = Button(frmttl, text='back', relief=FLAT, bd=0,
                              image=self.iconback, bg='#19a993', cursor='hand2', command=lambda cnt=cnt:
                              self.display_details(cnt,updt=True), activebackground='#19a993')
        btnback.place(x=10, y=5)
        
        #New contact details
        frmcnt = Frame(self.frmupdt, relief=SOLID, bd=1, highlightthickness=1)
        frmcnt.pack(fill=BOTH, padx=33, pady=97)
        frmcnt.columnconfigure(1, minsize=181)
        lblicon = Label(frmcnt, image=self.iconscnt[(cnt[4])+3], anchor='center', bg=self.iconsbg[(cnt[4])-3])
        lblicon.grid(row=0, column=0, columnspan=4, sticky='nsew', pady=(0,8), ipady=4)
        
        lblcnt = Label(frmcnt, text='Name: ', font=self.font_subttl)
        lblcnt.grid(row=1, column=0, sticky='ew', padx=(15,0), pady=8)
        lblcnt = Label(frmcnt, text='Phone: ', font=self.font_subttl)
        lblcnt.grid(row=2, column=0, sticky='ew', padx=(15,0), pady=8)
        lblcnt = Label(frmcnt, text='Email: ', font=self.font_subttl)
        lblcnt.grid(row=3, column=0, sticky='ew', padx=(15,0), pady=8)
        
        entname = Entry(frmcnt, bd=1, bg='#EBEBEB', fg='#606060', font=self.font_lbl)
        entname.grid(row=1, column=1, sticky='ew', padx=(0,8))
        entname.insert(0,cnt[1])
        entphn = Entry(frmcnt, bd=1, bg='#EBEBEB', fg='#606060', font=self.font_lbl)
        entphn.grid(row=2, column=1, sticky='ew', padx=(0,8))
        entphn.insert(0,cnt[2])
        enteml = Entry(frmcnt, bd=1, bg='#EBEBEB', fg='#606060', font=self.font_lbl)
        enteml.grid(row=3, column=1, sticky='ew', padx=(0,8))
        enteml.insert(0,cnt[3])
        
        #bottom buttons
        btnsv = Button(self.frmupdt, bg='#19a993', text='Update', relief=GROOVE, bd=1, fg='white',
                        font=self.font_subttl, cursor='hand2', highlightthickness=0, 
                        command = lambda id=cnt[0], clr=cnt[4]: self.updt_cnt(id, entname.get(), entphn.get(), enteml.get(), clr))
        btnsv.pack(fill=X, ipady=5)

    def add_cnt(self, name, phone, email, clr):
        cnt = contact(name, phone, email, clr)
        if cnt.add():
            self.display_main(add=True)

    def updt_cnt(self, id, name, phone, email, clr):
        contacto = contact(name, phone, email, clr, id)
        if contacto.update():
            cnt = (id, name, phone, email, clr)
            self.display_details(cnt, updt=True)

    def del_cnt(self, cnt_id):
        if messagebox.askokcancel(title='Delete confirmation', message='Do you want to delete this contact'):
            cnt = contact(id=cnt_id)
            cnt.delete()
            self.cntlst = update()
            self.display_main(det=True)

    def search_focus(self, event, lupa, ppl, label, srch=False):
        entry = event.widget
        if not srch: entry.delete(0,END)
        
        lupa.bind('<1>', lambda x: self.search_result(entry))
        ppl.pack(side=RIGHT, fill=Y, padx=(0,11))
        label.destroy()
    
    def search_result(self, entry):
        srch = entry.get()
        self.frmain.destroy()
        self.display_main(srch=srch)
    
    def search_cancel(self, entry):
        entry.delete(0,END)
        entry.insert(0, 'Search...')
        self.frmain.destroy()
        self.display_main()

    def Enter_on_cnv(self, event):
        canvas = event.widget
        if len(self.cntlst)>5:
            canvas.bind_all('<MouseWheel>', lambda event: canvas.yview('scroll',int((event.delta/120)*-1),'units') 
                            if len(self.cntlst)>5 else None)

    def Leave_cnv(self, event):
        event.widget.unbind_all('<MouseWheel>')

    def Enter_on_frm(self, event, frmnum):
        event.widget.config(relief=GROOVE)
        cnt = self.cntlst[frmnum]
        event.widget.bind_all('<1>', lambda event: self.display_details(cnt, event=event))

    def Leave_on_frm(self, event, frmnum):
        event.widget.config(relief=FLAT)
        event.widget.unbind_all('<1>')

icons = (
         iconspath+'Cnt_blue.png',
         iconspath+'Cnt_Green.png',
         iconspath+'Cnt_Yellow.png',
         iconspath+'Lupa.png',
         iconspath+'People.png',
         iconspath+'Btn_add.png',
         iconspath+'Back.png',
         iconspath+'X.png',
         iconspath+'top_icon.ico',
         iconspath+'top_icon.png'
        )

Addbook(icons)





