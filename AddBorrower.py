from tkinter import *
from tkinter import messagebox
import pymysql



con = pymysql.connect(host="localhost",user="root",password='MyNewPass',database='LIBRARY',unix_socket="/tmp/mysql.sock")
cur = con.cursor()


    
def insertBorrower():
    ssn = en1.get()
    bname = en2.get()
    address = en3.get()
    phone = en4.get()
    try:
        cur.execute("INSERT INTO BORROWER(Ssn,Bname,Address,Phone) VALUES('"+str(ssn)+"','"+bname+"','"+address+"','"+phone+"')")
        con.commit()
        messagebox.showinfo("Success","Borrower added to Database")
    except:
        messagebox.showinfo("Failure","Please check values and try again.")
    
    en1.delete(0, END)
    en2.delete(0, END)
    en3.delete(0, END)
    en4.delete(0, END)
def addBorrower(): 
    global Canvas1,labelFrame,lb1,en1,lb2,en2,lb3,en3,lb4,en4
    root = Tk()
    root.title("Library")
    root.minsize(width=400,height=400)
    root.geometry("600x500")
    
    
    Canvas1 = Canvas(root)
    
    Canvas1.config(bg="#FFF9C4",width = 500, height = 500)
    Canvas1.pack(expand=True,fill=BOTH)
        
    labelFrame = Frame(root,bg='#044F67')
    labelFrame.place(relx=0.2,rely=0.44,relwidth=0.6,relheight=0.42)
    
    # SSN
    lb1 = Label(labelFrame,text="Ssn : ", bg='#044F67', fg='white')
    lb1.place(relx=0.05,rely=0.05)
    
    en1 = Entry(labelFrame)
    en1.place(relx=0.3,rely=0.05, relwidth=0.62)
    
    #Borrower Name
    lb2 = Label(labelFrame,text="BName : ", bg='#044F67', fg='white')
    lb2.place(relx=0.05,rely=0.2)
    
    en2 = Entry(labelFrame)
    en2.place(relx=0.3,rely=0.2, relwidth=0.62)
    
    #Address
    lb3 = Label(labelFrame,text="Address : ", bg='#044F67', fg='white')
    lb3.place(relx=0.05,rely=0.35)
    
    en3 = Entry(labelFrame)
    en3.place(relx=0.3,rely=0.35, relwidth=0.62)
    
    #Phone
    lb4 = Label(labelFrame,text="Phone : ", bg='#044F67', fg='white')
    lb4.place(relx=0.05,rely=0.5)
    
    en4 = Entry(labelFrame)
    en4.place(relx=0.3,rely=0.5, relwidth=0.62)
    
    
    #Submit Button
    SubmitBtn = Button(root,text="SUBMIT",bg='#264348', fg='#333945',command=insertBorrower)
    SubmitBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)
    quitBtn = Button(root,text="Quit",bg='#264348', fg='#333945',command=root.quit)
    quitBtn.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)
    
    root.mainloop()