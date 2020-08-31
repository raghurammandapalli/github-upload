from tkinter import *
from tkinter import messagebox
import pymysql



con = pymysql.connect(host="localhost",user="root",password='MyNewPass',database='LIBRARY',unix_socket="/tmp/mysql.sock")
cur = con.cursor()

    
def issue():
    
    global backBtn
    
    card_id = en1.get()
    
    issueBtn.destroy()
    quitBtn.destroy()
    labelFrame.destroy()
    lb1.destroy()
    en1.destroy()
    
    result = cur.execute("SELECT * FROM BOOK_LOANS WHERE Card_id = "+str(card_id)+" AND Date_in IS NULL")
    con.commit()
    if(result < 3):
        cur.execute("SELECT CURDATE()")
        con.commit()
        today_date = cur.fetchone()[0]
        print(type(today_date))
        print(today_date)
        print("due:")
        cur.execute("SELECT DATE_ADD('"+str(today_date)+"', INTERVAL 14 DAY)")
        con.commit()
        due_date = cur.fetchone()[0]
        print(due_date)
        print(str(today_date))
        
        try:
            cur.execute("INSERT INTO BOOK_LOANS(Isbn,Card_id,Date_out,Due_date) VALUES(%s,%s,%s,%s)",(str(Isbn),str(card_id),str(today_date),str(due_date)))
            con.commit()
            cur.execute("SELECT * FROM BOOK_LOANS WHERE Isbn = "+str(Isbn)+" AND Date_in IS NULL")
            con.commit()
            loan_id = cur.fetchone()[0]
            print("loan_id:")
            print(loan_id)
            cur.execute("INSERT INTO FINES(Loan_id) VALUES("+str(loan_id)+")")
            con.commit()
            messagebox.showinfo("Success","Issued Book")
        except:
            messagebox.showinfo("Error","Can't Issue Book")
    else:
        messagebox.showinfo("Error","Already 3 Books Issued")
    
    
    
    
    backBtn = Button(root,text="< Back",bg='#455A64', fg='black', command=issueBook)
    backBtn.place(relx=0.53,rely=0.85, relwidth=0.18,relheight=0.08)

    
def issueBook():
    
    if available == False:
        messagebox.showinfo("Error","The book is already issued!")
    else:
        global en1,issueBtn,lb1,labelFrame,quitBtn,Canvas1,headingFrame1,headingFrame2,headingLabel
    
        headingFrame1.destroy()
        headingFrame2.destroy()
        headingLabel.destroy()
        labelFrame.destroy()
        Canvas1.destroy()
        quitBtn.destroy()
        checkoutBtn.destroy()
    
    
    

    
        Canvas1 = Canvas(root)
    
        Canvas1.config(bg="#706fd3",width = 500, height = 500)
        Canvas1.pack(expand=True,fill=BOTH)
    
        labelFrame = Frame(root,bg='black')
        labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.3)
        
        headingFrame1 = Frame(root,bg="#333945",bd=5)
        headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
        
        headingFrame2 = Frame(headingFrame1,bg="#EAF0F1")
        headingFrame2.place(relx=0.01,rely=0.05,relwidth=0.98,relheight=0.9)
        
        headingLabel = Label(headingFrame2, text="ISSUE BOOK", fg='black')
        headingLabel.place(relx=0.25,rely=0.15, relwidth=0.5, relheight=0.5)   
        
        lb1 = Label(labelFrame,text="Card ID : ", bg='black', fg='white')
        lb1.place(relx=0.05,rely=0.2)
        
        en1 = Entry(labelFrame)
        en1.place(relx=0.3,rely=0.2, relwidth=0.62)
    
    
    
    
    #Issue Button
        issueBtn = Button(root,text="Issue",bg='#d1ccc0', fg='black',command=issue)
        issueBtn.place(relx=0.28,rely=0.75, relwidth=0.18,relheight=0.08)
    
        quitBtn = Button(root,text="Quit",bg='#aaa69d', fg='black', command=root.quit)
        quitBtn.place(relx=0.53,rely=0.75, relwidth=0.18,relheight=0.08)
    
def search():
    
    global SearchBtn,labelFrame,lb1,en1,quitBtn,root,Canvas1,checkoutBtn
    global Isbn,available
    sub = en1.get()
    
    SearchBtn.destroy()
    quitBtn.destroy()
    lb1.destroy()
    en1.destroy()
    
    
    labelFrame = Frame(root,bg='black')
    labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.5)
    
    y = 0.25
    
    Label(labelFrame, text="%-20s%-30s%-30s%-30s"%('ISBN','Name','Title','Available'),bg='black',fg='white').place(relx=0.07,rely=0.1)
    Label(labelFrame, text="----------------------------------------------------------------------------",bg='black',fg='white').place(relx=0.05,rely=0.2)
    
    searchSql = "SELECT * FROM BOOK_AUTHORS AS B,AUTHORS AS A,BOOK AS C WHERE B.Author_id = A.Author_id AND C.Isbn = B.Isbn AND C.Isbn = "+sub
    try: #search by isbn
        available = False
        cur.execute(searchSql)
        con.commit()
        Isbn = cur.fetchone()[1]
        Name = []
        cur.execute(searchSql)
        con.commit()
        Title = cur.fetchone()[5]
        cur.execute(searchSql)
        con.commit()
        for i in cur:
            if(i[5] == Title):
                Name.append(i[3])
        result = cur.execute("SELECT * FROM BOOK_LOANS WHERE Isbn = "+str(Isbn)+" AND Date_in IS NULL")
        con.commit()
        if(result == 0):
            available = True
        Label(labelFrame, text="%-20s%-20s%-30s%-30s"%(Isbn,Name,Title,available),bg='black',fg='white').place(relx=0.07,rely=y)
        
    except:
        try:
            #search by title
            available = False
            query = "SELECT * FROM BOOK_AUTHORS AS B,AUTHORS AS A,BOOK AS C WHERE B.Author_id = A.Author_id AND C.Isbn = B.Isbn AND C.Title LIKE '%"+sub+"%'"
            res = cur.execute(query)
            con.commit()
            if res != 0:
                Isbn = cur.fetchone()[1]
                Name = []
                cur.execute(query)
                con.commit()
                Title = cur.fetchone()[5]
                cur.execute(query)
                con.commit()
                for i in cur:
                    if(i[5] == Title):
                        Name.append(i[3])
                result = cur.execute("SELECT * FROM BOOK_LOANS WHERE Isbn = "+str(Isbn)+" AND Date_in IS NULL")
                con.commit()
                if(result == 0):
                    available = True
            
                Label(labelFrame, text="%-20s%-20s%-30s%-30s"%(Isbn,Name,Title,available),bg='black',fg='white').place(relx=0.07,rely=y)
            
            else:
                #search by Name
                available = False
                query = "SELECT * FROM BOOK_AUTHORS AS B,AUTHORS AS A,BOOK AS C WHERE B.Author_id = A.Author_id AND C.Isbn = B.Isbn AND A.Name LIKE '%"+sub+"%'"
                cur.execute(query)
                con.commit()
                Isbn = cur.fetchone()[1]
                Name = []
                cur.execute(query)
                con.commit()
                Title = cur.fetchone()[5]
                cur.execute(query)
                con.commit()
                for i in cur:
                    if(i[5] == Title):
                        Name.append(i[3])
                result = cur.execute("SELECT * FROM BOOK_LOANS WHERE Isbn = "+str(Isbn)+" AND Date_in IS NULL")
                con.commit()
                if(result == 0):
                    available = True
                    
                Label(labelFrame, text="%-20s%-20s%-30s%-30s"%(Isbn,Name,Title,available),bg='black',fg='white').place(relx=0.07,rely=y)
                
                
        except:
            messagebox.showinfo("Search Error","The value entered is wrong, Try again")
    
    print(sub)
    checkoutBtn = Button(root,text="Check-out",bg='black', fg='#333945', command = issueBook)
    checkoutBtn.place(relx=0.30,rely=0.85, relwidth=0.18,relheight=0.08)
   
    quitBtn = Button(root,text="< Back",bg='#455A64', fg='#333945', command=searchBook)
    quitBtn.place(relx=0.53,rely=0.85, relwidth=0.18,relheight=0.08)

    
def searchBook(): 
    
    global en1,SearchBtn,lb1,labelFrame,quitBtn,Canvas1,root,headingFrame1,headingFrame2,headingLabel
    
    root = Tk()
    root.title("Library")
    root.minsize(width=400,height=400)
    root.geometry("600x500")
    
    
    
    
    
    
    Canvas1 = Canvas(root)
    
    Canvas1.config(bg="white",width = 500, height = 500)
    Canvas1.pack(expand=True,fill=BOTH)
    
    labelFrame = Frame(root,bg='black')
    labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.3)
        
    headingFrame1 = Frame(root,bg="#333945",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
        
    headingFrame2 = Frame(headingFrame1,bg="#EAF0F1")
    headingFrame2.place(relx=0.01,rely=0.05,relwidth=0.98,relheight=0.9)
        
    headingLabel = Label(headingFrame2, text="SEARCH BOOK", fg='black')
    headingLabel.place(relx=0.25,rely=0.15, relwidth=0.5, relheight=0.5)   
        
    lb1 = Label(labelFrame,text="Enter Here : ", bg='black', fg='white')
    lb1.place(relx=0.05,rely=0.5)
        
    en1 = Entry(labelFrame)
    en1.place(relx=0.3,rely=0.5, relwidth=0.62)
    
    #Search Button
    SearchBtn = Button(root,text="Search",bg='#264348', fg='#333945',command=search)
    SearchBtn.place(relx=0.28,rely=0.75, relwidth=0.18,relheight=0.08)
    
    quitBtn = Button(root,text="Quit",bg='#455A64', fg='#333945', command=root.quit)
    quitBtn.place(relx=0.53,rely=0.75, relwidth=0.18,relheight=0.08)
    
    root.mainloop()