from tkinter import *
import pymysql
from tkinter import messagebox
from SearchBook import *
from CheckIn import *
from AddBorrower import *



empTable = "LIBRARIANS"
root = Tk()
root.title("Library")
root.minsize(width=400,height=400)
root.geometry("600x500")
count = 0
try:
    con = pymysql.connect(host='localhost',user='root',password='MyNewPass',unix_socket="/tmp/mysql.sock",database='LIBRARY')
    cur = con.cursor()
except:
    messagebox.showinfo("Unable to connect to DB","try again")
    

def empMenu():
    
    global headingFrame1,headingFrame2,headingLabel,SubmitBtn,Canvas1,labelFrame,backBtn
    headingFrame1.destroy()
    headingFrame2.destroy()
    headingLabel.destroy()
    Canvas1.destroy()
    SubmitBtn.destroy()
    
    
    Canvas1 = Canvas(root)

    Canvas1.config(bg="#f7f1e3",width = 500, height = 500)
    Canvas1.pack(expand=True,fill=BOTH)
    
    headingFrame1 = Frame(root,bg="#333945",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
        
    headingFrame2 = Frame(headingFrame1,bg="#EAF0F1")
    headingFrame2.place(relx=0.01,rely=0.05,relwidth=0.98,relheight=0.9)
        
    headingLabel = Label(headingFrame2, text="LIBRARY MENU", fg='black')
    headingLabel.place(relx=0.25,rely=0.15, relwidth=0.5, relheight=0.5)
    
    
    
    btn1 = Button(root,text="Add Borrower",bg='black', fg='#333945', command=addBorrower)
    btn1.place(relx=0.28,rely=0.3, relwidth=0.45,relheight=0.1)
    
    btn2 = Button(root,text="Search Book",bg='black', fg='#333945', command=searchBook)
    btn2.place(relx=0.28,rely=0.4, relwidth=0.45,relheight=0.1)
    
    btn3 = Button(root,text="Check-in Book",bg='black', fg='#333945', command = checkinBook)
    btn3.place(relx=0.28,rely=0.5, relwidth=0.45,relheight=0.1)
    
    btn4 = Button(root,text="Refresh Fines",bg='black', fg='#333945', command=refresh)
    btn4.place(relx=0.28,rely=0.6, relwidth=0.45,relheight=0.1)
    
    backBtn = Button(root,text="<  BACK",bg='#455A64', fg='#333945', command=Employee)
    backBtn.place(relx=0.5,rely=0.9, relwidth=0.18,relheight=0.08)
    


def gettingEmpDetails():
    
    EmpId = en1.get()
    password = en2.get()
    
    
    try:
        if (type(int(EmpId)) == int):
            pass
        else:
            messagebox.showinfo("Invalid Value","Employee ID should be an integer")
            return
    except:
        messagebox.showinfo("Invalid Value","Employee ID should be an integer")
        return
        
    
    sql = "INSERT INTO "+empTable+" VALUES("+EmpId+",'"+password+"')" 
    try:
        cur.execute(sql)
        con.commit()
    except:
        messagebox.showinfo("Error inserting","Cannot add data to Database")
    
    print(EmpId)
    
    print(password)
    
    en1.delete(0, END)
    en2.delete(0, END)
   

    
def gettingLoginDetails():
    
    login = en1.get()
    password = en2.get()
    
    try:
        cur.execute("SELECT Empid FROM LIBRARIANS WHERE Password='"+password+"'")
        result = cur.fetchone()[0]
        
        int_login = int(login)
        if(result == int_login):
            empMenu()
        else:
            messagebox.showerror("Failure","Can't log in, check your credentials")
    except:
        messagebox.showinfo("FAILED","Please check your credentials")
    
    print(login)
    print(password)
    en1.delete(0, END)
    en2.delete(0, END)
    
    
def EmpRegister():
    
    global labelFrame
    
    global count
    count += 1

    if(count>=2):
        labelFrame.destroy()
    
    global en1,en2
    
    labelFrame = Frame(root,bg='#044F67')
    labelFrame.place(relx=0.2,rely=0.44,relwidth=0.6,relheight=0.42)
    
    # Employee ID
    lb1 = Label(labelFrame,text="Emp ID : ", bg='#044F67', fg='white')
    lb1.place(relx=0.05,rely=0.05)
    
    en1 = Entry(labelFrame)
    en1.place(relx=0.3,rely=0.05, relwidth=0.62)
    
    #Employee Paswword
    lb2 = Label(labelFrame,text="Password : ", bg='#044F67', fg='white')
    lb2.place(relx=0.05,rely=0.2)
    
    en2 = Entry(labelFrame)
    en2.place(relx=0.3,rely=0.2, relwidth=0.62)
    
    #Submit Button
    SubmitBtn = Button(root,text="SUBMIT",bg='#264348', fg='#333945',command=gettingEmpDetails)
    SubmitBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)


def Login():
    
    global labelFrame
    
    global count
    count += 1

    if(count>=2):
        labelFrame.destroy()
    
    global en1,en2,SubmitBtn,btn1,btn2
    
    labelFrame = Frame(root,bg='#044F67')
    labelFrame.place(relx=0.2,rely=0.44,relwidth=0.6,relheight=0.3)
    
    #Login ID
    lb1 = Label(labelFrame,text="Login ID : ", bg='#044F67', fg='white')
    lb1.place(relx=0.05,rely=0.1)
    
    en1 = Entry(labelFrame)
    en1.place(relx=0.3,rely=0.1, relwidth=0.62)
    
    
    # Paswword
    lb2 = Label(labelFrame,text="Password : ", bg='#044F67', fg='white')
    lb2.place(relx=0.05,rely=0.3)
    
    en2 = Entry(labelFrame)
    en2.place(relx=0.3,rely=0.3, relwidth=0.62)
    
    
    #Submit Button
    SubmitBtn = Button(root,text="SUBMIT",bg='#264348', fg='#333945',command=gettingLoginDetails)
    SubmitBtn.place(relx=0.28,rely=0.9, relwidth=0.18,relheight=0.08)

def Employee():
    
    global headingFrame1,headingFrame2,headingLabel,btn1,btn2,btn3,Canvas1
    headingFrame1.destroy()
    headingFrame2.destroy()
    headingLabel.destroy()
    Canvas1.destroy()
    btn1.destroy()

    
    Canvas1 = Canvas(root)

    Canvas1.config(bg="#FFF9C4",width = 500, height = 500)
    Canvas1.pack(expand=True,fill=BOTH)

    
    headingFrame1 = Frame(root,bg="#333945",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
    
    headingFrame2 = Frame(headingFrame1,bg="#EAF0F1")
    headingFrame2.place(relx=0.01,rely=0.05,relwidth=0.98,relheight=0.9)
    
    headingLabel = Label(headingFrame2, text="Hello, Librarian", fg='black')
    headingLabel.place(relx=0.25,rely=0.15, relwidth=0.5, relheight=0.5)
    
    btn1 = Button(root,text="Register",bg='black', fg='#333945',command=EmpRegister)
    btn1.place(relx=0.28,rely=0.3, relwidth=0.2,relheight=0.1)
    
    btn2 = Button(root,text="Login",bg='black', fg='#333945', command=Login)
    btn2.place(relx=0.53,rely=0.3, relwidth=0.2,relheight=0.1)
    
    btn3 = Button(root,text="Quit",bg='#455A64', fg='#333945', command=root.quit)
    btn3.place(relx=0.53,rely=0.9, relwidth=0.18,relheight=0.08)





Canvas1 = Canvas(root)

Canvas1.config(bg="#FFF9C4",width = 500,height = 500)
Canvas1.pack(expand=True,fill=BOTH)

headingFrame1 = Frame(root,bg="#333945",bd=5)
headingFrame1.place(relx=0.2,rely=0.1,relwidth=0.6,relheight=0.16)

headingFrame2 = Frame(headingFrame1,bg="#EAF0F1")
headingFrame2.place(relx=0.01,rely=0.05,relwidth=0.98,relheight=0.9)

headingLabel = Label(headingFrame2, text="Welcome to the Library", fg='black')
headingLabel.place(relx=0.25,rely=0.1, relwidth=0.5, relheight=0.5)

btn1 = Button(root,text="Continue",bg='black', fg='#333945', command=Employee)
btn1.place(relx=0.38,rely=0.8, relwidth=0.2,relheight=0.1)

root.mainloop()
