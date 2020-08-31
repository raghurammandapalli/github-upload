from tkinter import *
from tkinter import messagebox
import pymysql



con = pymysql.connect(host="localhost",user="root",password='MyNewPass',database='LIBRARY',unix_socket="/tmp/mysql.sock")
cur = con.cursor()

def refresh():
    global today_date
    try:
        cur.execute("SELECT CURDATE()")
        con.commit()
        today_date = cur.fetchone()[0]
        print("today's date:")
        print(today_date)
        cur.execute("SELECT * FROM BOOK_LOANS WHERE Date_in IS NULL")
        con.commit()
        for i in cur:
            print("i[3]:")
            print(str(i[3]))
            cur.execute("SELECT DATEDIFF('"+str(today_date)+"','"+str(i[3])+"') AS days")
            con.commit()
            diff = cur.fetchone()
            print("difference:")
            print(diff[0])
            if diff[0] > 14:
                fine = diff[0]*0.25
                print("fine:")
                print(fine)      
                cur.execute("UPDATE FINES SET Fine_amt = "+str(fine)+" WHERE Loan_id = "+str(i[0]))
                con.commit()
            else:
                continue
                
        messagebox.showinfo("Success","Refresh Complete")        
    except:
        messagebox.showinfo("Error","Cannot Refresh")

def last():
    variable = en1.get()
    if variable.lower() == 'yes':
        cur.execute("UPDATE FINES SET Paid = True WHERE Loan_id = "+str(Loan_id))
        con.commit()
        cur.execute("UPDATE BOOK_LOANS SET Date_in = '"+str(today_date)+"' WHERE Loan_id = "+str(Loan_id))
        con.commit()
        messagebox.showinfo("Success","Book Checked in")
    else:
        messagebox.showinfo("Failed","Please collect fine first!")
   
        
def check():
    global labelFrame,checkBtn,en1
    checkBtn.destroy()
    labelFrame.destroy()
    if found == False:
        messagebox.showinfo("Not Found","No book to check out")
    else:
        refresh()
        cur.execute("SELECT * FROM FINES WHERE Loan_id = "+str(Loan_id))
        con.commit()
        i = cur.fetchone()
        if i[2]:
            cur.execute("UPDATE BOOK_LOANS SET Date_in = '"+str(today_date)+"' WHERE Loan_id = "+str(Loan_id))
            con.commit()
            messagebox.showinfo("Success","Book Checked in") 
        else:
            labelFrame = Frame(root,bg='black')
            labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.3)  
        
            lb1 = Label(labelFrame,text="Is "+str(i[1])+" Fine Paid: ", bg='black', fg='white')
            lb1.place(relx=0.05,rely=0.2)
        
            en1 = Entry(labelFrame)
            en1.place(relx=0.3,rely=0.2, relwidth=0.62)
            
            checkBtn = Button(root,text="Confirm",bg='#d1ccc0', fg='black',command=last)
            checkBtn.place(relx=0.28,rely=0.85, relwidth=0.18,relheight=0.08)
        
        
def bookCheckin():
    
    global quitBtn,labelFrame,found,checkBtn,Loan_id
    found = False
    sub = en1.get()
    
    issueBtn.destroy()
    quitBtn.destroy()
    labelFrame.destroy()
    lb1.destroy()
    en1.destroy()
    
    labelFrame = Frame(root,bg='black')
    labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.5)
    
    Label(labelFrame, text="%-20s%-20s%-20s%-20s%-20s"%('ISBN','Card_id','Date_out','Due_date','Date_in'),bg='black',fg='white').place(relx=0.07,rely=0.1)
    Label(labelFrame, text="----------------------------------------------------------------------------",bg='black',fg='white').place(relx=0.05,rely=0.2)
    try:# search based on card_no
        res1 = cur.execute("SELECT * FROM BOOK_LOANS WHERE Card_id = "+str(sub)+" AND Date_in IS NULL")
        con.commit()
        if res1 > 0:
            found = True
            i = cur.fetchone()
            Loan_id = i[0]
            date_in = "NULL"
            Label(labelFrame, text="%-20s%-20s%-20s%-20s%-20s"%(i[1],i[2],i[3],i[4],date_in),bg='black',fg='white').place(relx=0.07,rely=0.25)
            
        else: # search based on Isbn.
            res2 = cur.execute("SELECT * FROM BOOK_LOANS WHERE Isbn = "+str(sub)+" AND Date_in IS NULL")
            con.commit()
            if res2 > 0:
                found = True
                i = cur.fetchone()
                Loan_id = i[0]
                date_in = "NULL"
                Label(labelFrame, text="%-20s%-20s%-20s%-20s%-20s"%(i[1],i[2],i[3],i[4],date_in),bg='black',fg='white').place(relx=0.07,rely=0.25)
                
            else:
                messagebox.showinfo("Not Found","Cannot find the book")
                
    except:
        try: # search based on Borrower Name.
            res = cur.execute("SELECT * FROM BOOK_LOANS AS B,BORROWER AS W WHERE B.Card_id = W.Card_id AND W.Bname LIKE '%"+str(sub)+"%' AND Date_in IS NULL")
            con.commit()
            if res != 0:
                found = True
                i = cur.fetchone()
                Loan_id = i[0]
                date_in = "NULL"
                Label(labelFrame, text="%-20s%-20s%-20s%-20s%-20s"%(i[1],i[2],i[3],i[4],date_in),bg='black',fg='white').place(relx=0.07,rely=0.25)
            else:
                messagebox.showinfo("Not Found","Cannot find the book.")    
        except:
            messagebox.showinfo("Error","Enter correct format to search.")
    
    
    
    checkBtn = Button(root,text="Confirm",bg='#d1ccc0', fg='black',command=check)
    checkBtn.place(relx=0.28,rely=0.85, relwidth=0.18,relheight=0.08)
    
    quitBtn = Button(root,text="< Back",bg='#455A64', fg='black', command=checkinBook)
    quitBtn.place(relx=0.53,rely=0.85, relwidth=0.18,relheight=0.08)

    
def checkinBook(): 
    
    global en1,issueBtn,lb1,labelFrame,quitBtn,Canvas1,root
    root = Tk()
    root.title("Library")
    root.minsize(width=400,height=400)
    root.geometry("600x500")
    
    
    
    

    
    Canvas1 = Canvas(root)
    
    Canvas1.config(bg="#706fd3",width = 500, height = 500)
    Canvas1.pack(expand=True,fill=BOTH)
    
    labelFrame = Frame(root,bg='black')
    labelFrame.place(relx=0.1,rely=0.3,relwidth=0.8,relheight=0.3)
        
    headingFrame1 = Frame(root,bg="#333945",bd=5)
    headingFrame1.place(relx=0.25,rely=0.1,relwidth=0.5,relheight=0.13)
        
    headingFrame2 = Frame(headingFrame1,bg="#EAF0F1")
    headingFrame2.place(relx=0.01,rely=0.05,relwidth=0.98,relheight=0.9)
        
    headingLabel = Label(headingFrame2, text="Checkin BOOK", fg='black')
    headingLabel.place(relx=0.25,rely=0.15, relwidth=0.5, relheight=0.5)   
        
    lb1 = Label(labelFrame,text="Enter Here : ", bg='black', fg='white')
    lb1.place(relx=0.05,rely=0.2)
        
    en1 = Entry(labelFrame)
    en1.place(relx=0.3,rely=0.2, relwidth=0.62)
    
    
    
    
    #checkin Button
    issueBtn = Button(root,text="Checkin",bg='#d1ccc0', fg='black',command=bookCheckin)
    issueBtn.place(relx=0.28,rely=0.75, relwidth=0.18,relheight=0.08)
    
    quitBtn = Button(root,text="Quit",bg='#aaa69d', fg='black', command=root.quit)
    quitBtn.place(relx=0.53,rely=0.75, relwidth=0.18,relheight=0.08)
    
    root.mainloop()