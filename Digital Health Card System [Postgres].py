from tkinter import *
from tkinter import messagebox, ttk
from tkinter import filedialog
from turtle import left, right, width
from typing import final
import matplotlib.pyplot as pl
from PIL import Image, ImageTk
# import mysql.connector as sqlcon
import psycopg2
from psycopg2 import sql
import re
from tkcalendar import Calendar
import qrcode
import tkinter as tk
import smtplib
import io
import sys
import socket


main = Tk()
main.title("Digital Health Card System")
card = Toplevel()
card.title("Digital Health Card System")
card.iconbitmap(r"healthcare_icon.ico")
card.config(bg='powder blue')

def digital_to_binary(image_name):
        # Convert digital data to binary format
    with open(image_name, 'rb') as file:
        binaryData = file.read()
    return binaryData

main.state("zoomed")
main.iconbitmap(r"healthcare_icon.ico")
loginscreen =Toplevel()
loginscreen.title("Digital Health Card System")
loginscreen.iconbitmap(r"healthcare_icon.ico")
#---------------------------------------------------Database Connection---------------------------------------------------------

def connect_with_database():
    global dbcon
    global cursor
    try:
        dbcon = psycopg2.connect(
            host = "localhost",
            user = 'postgres',
            password = 'root',
            port = 5432,
            dbname = "digital"
        )
        dbcon.autocommit = True
        cursor = dbcon.cursor()
    except:
        dbcon = psycopg2.connect(
            host = "localhost",
            user = 'postgres',
            password = 'root',
            port = 5432
        )
        dbcon.autocommit = True
        cursor = dbcon.cursor()

connect_with_database()

def create_database_and_table():
    try:
        operation = sql.SQL("CREATE DATABASE digital").format(sql.Identifier("postgres"))
        cursor.execute(operation)
    except:
        pass

    # operation = sql.SQL("USE digital")
    # cursor.execute(operation)
    dbcon = psycopg2.connect(
        host = "localhost",
        user = 'postgres',
        password = 'root',
        port = 5432,
        dbname = "digital"
    )
    dbcon.autocommit = True
    cursor = dbcon.cursor()

    operation = """CREATE TABLE IF NOT EXISTS patient_details(
					pid            BIGSERIAL       PRIMARY KEY,
                    images          BYTEA           NOT NULL,
					name           VARCHAR(50)     NOT NULL,
					dob            VARCHAR(20)     NOT NULL,
					gender         VARCHAR(20)     NOT NULL,
					contact        BIGINT          NOT NULL,
					address        VARCHAR(99)     NOT NULL,
					blood_group    VARCHAR(20)     NOT NULL,
                    aadhar          VARCHAR(12)    NOT NULL,
                    email           VARCHAR(30)    NOT NULL,
                    diagnosis       VARCHAR(50),
                    report          VARCHAR(50),
                    doctor          VARCHAR(50))"""
    cursor.execute(sql.SQL(operation))
    dbcon.commit()
    
    
    operation = """CREATE TABLE IF NOT EXISTS doctor_details(
					username            VARCHAR(50)     NOT NULL    PRIMARY KEY,
					password            VARCHAR(50)     NOT NULL,
					contact             BIGINT          NOT NULL,
                    email               VARCHAR(30)    NOT NULL)"""
    cursor.execute(operation)


create_database_and_table()


#def insert_bydefault_data():
#    img_upload = "image.jpeg" 
#    Picture = digital_to_binary(img_upload)
#    
#    operation = """INSERT INTO patient_details VALUES
#					(01,Picture ,"karamveer", "2002-07-10", "M", 9589689898, "Mumbai", "B+","222233334444","rajputkaramveer2@gmail.com","null","null",""),
#                   (02,Picture ,"saara", "2002-03-20", "F", 9589689898, "Mumbai", "O-","222233334444","saarakaram@55@gmail.com","null","null","")"""
#    cursor.execute(operation)
    # dbcon.commit()


# Inserted By Default Data

#try:
#    insert_bydefault_data()    
#except:
#        pass

#--------------------------------------------------------------------------------------------------------------------------------
def clean_right_frame():
    global right_frame
    right_frame.grid_forget()
    right_frame = LabelFrame(main,bd=2,width=1000,bg="ghostwhite",height=620)
    right_frame.place(x=360,y=80)
    right_frame.grid_propagate(0)
    
def clean_p_update_frame():
    global p_update_frame
    p_update_frame.grid_forget()
    p_update_frame = LabelFrame(main,bd=2,width=1000,bg="ghostwhite",height=485)
    p_update_frame.place(x=360,y=210)
    p_update_frame.grid_propagate(0)

#------------------------------------------------Show Temp Upload Image------------------------------------------------
    
choose_img=Image.open(r"user_login_temp_img.png")
resize_choose_img = choose_img.resize((200, 168))
choose_ph=ImageTk.PhotoImage(resize_choose_img)


#----------------------------------------------------Register Patient Details-------------------------------------------------------
top = Tk()
top.withdraw()

def new_register():
    global gender_entry
    global blood_group_entry
    global dob_date
    clean_right_frame()
    #global dob_date
    def insert():
        global dob_date
        images = (image_entry_str.get())
        name = str(e1.get())
        dob = str(dob_entry_str.get())
        gender = str(gender_entry.get())
        contact = str(e4.get())
        address = str(e5.get())
        aadhar = str(e7.get())
        email = str(e8.get())
        
        
        data = [images,name,dob, gender, contact, address,aadhar,email]   
        num = ['0','1','2','3','4','5','6','7','8','9'] 
        for i in data:
            if (i== images):
                if (len(i)==0):
                    messagebox.showerror("Database","Please Upload the image.")
                    return
            if (i == name):
                if (len(i) == 0):
                    messagebox.showerror("Database", "Please enter Name.")
                    return
                for n in num:
                    if (n in name):
                        messagebox.showerror("Database", "Name should not contain any number.")
                        return
            elif (i == dob):
                if ( len(i)==0):
                    messagebox.showerror("Database", "Please enter correct Year of Birth.")
                    return
            elif (i == gender):
                if (len(i) == 0):
                    messagebox.showerror("Database", "Please select your gender.")
                    return
            elif (i == contact):
                if (len(i) != 10):
                    messagebox.showerror("Database", "Please enter valid 10 digits of Contact Number.")
                    return
                try:
                    con = int(contact)
                except:
                    messagebox.showerror("Database", "Number should not contain any character.")
                    return
                if (i[0]=='7' or i[0]=='8' or i[0]=='9'):
                    pass
                else:
                    messagebox.showerror("Database", "A number should start with 7 or 8 or 9")
                    return
            elif (i == address):
                if (len(i) == 0):
                    messagebox.showerror("Database", "Please enter valid Address.")
                    return
            try :
                blood_group = blood_group_entry.get(blood_group_entry.curselection()[0])
            except:
                messagebox.showerror("Database", "Please select valid Blood Group")
                return
            if ( i == aadhar):
                if (len(i) != 12 or i[0]=='1' or i[0] =='0'):
                    messagebox.showerror("Database","Please enter valid aadhar card Number.")
                    return
            if ( i == email):
                if (len(i) == 0):
                    messagebox.showerror("Database","Please enter Email Address.")
                    return
            
            if(i == email):
                pat = r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
                if not re.match(pat,i):
                    messagebox.showerror("Database","Please enter valid email address.")
                    return
                
        send_email = str(e8.get())
        gmail_user = 'digitalhealthcardsystem@gmail.com'
        gmail_password = ''
        sent_from = gmail_user
        to = [send_email]
        body = 'you have been successfully registered.'
        email_text = """
        From: %s
        To: %s
        Subject: Digital Health Card System
        
        
        
        
        
        %s                         
        """ % (sent_from,",".join(to) ,body)
        
        p_mail = True
        try:
            socket.create_connection(("google.com", 80), timeout=3)

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=60)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()

            p_mail = True
            print('Email sent!')
        except:
            print('Something went wrong...')
            p_mail = False
            # messagebox.showerror("Digital Health Card System","Email was does not send...")
        
        img_upload = image_entry_str.get()    
        Picture = digital_to_binary(img_upload)
        
        try:        
            operation = """INSERT INTO patient_details(images,name, dob, gender, contact, address, blood_group, aadhar, email,diagnosis,report,doctor) VALUES
					(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            values = (Picture,name, dob, gender, contact, address, blood_group,aadhar,email,"null","null","null")
            cursor.execute(operation,values)
            dbcon.commit()
        except:
            messagebox.showerror("Digital Health Card System","Image File Data Is To Long Please Select Another Image File.")
            return
        
        # get patient id
        operation = """SELECT *FROM patient_details"""
        cursor.execute(operation)
        data = cursor.fetchall()
        pid = str(data[-1][0])

        if p_mail == True:
            messagebox.showinfo("Digital Health Card System", "Your PID is: {}".format(pid)+" and The credentials have been sent to your registered email address.")
        else:
            messagebox.showwarning("Digital Health Card System", "Your PID is: {}".format(pid)+". However, the credentials could not be sent to your registered email address.")
        
        def clear_data():
        # clear the entry boxes
            choose_img_label.config(image=choose_ph)
            e1.delete(0, END)
            gender_entry_male.deselect()
            gender_entry_female.deselect()
            gender_entry_other.deselect()
            e4.delete(0, END)
            e5.delete(0,END)
            e6.delete(0,END)
            e7.delete(0,END)
            e8.delete(0,END)
            age_entry.config(text="Select Date")

            try:
                blood_group_entry.get(blood_group_entry.selection_clear(0,END))
            except:
                pass
        clear_data()

    choose_img_label = Label(right_frame,image=choose_ph)
    choose_img_label.place(x=690,y=68)
    def choose_img():
        global choose_ph2
        file = filedialog.askopenfilename(filetypes=[("jpeg file","*.jpeg"),("jpg file","*.jpg"),("png file","*.png")])
        file1 = str(file)
        final_file = file1.replace("/","\\\\")
        choose_img=Image.open(final_file)
        resize_choose_img2 = choose_img.resize((200, 168))
        choose_ph2=ImageTk.PhotoImage(resize_choose_img2)
        choose_img_label.configure(image=choose_ph2)
        image_entry_str.set(final_file)
    
        
    image_entry_str = StringVar()
    image_entry = Entry(right_frame,font=('arial',16,'bold'),textvariable=image_entry_str, bd=6, insertwidth=4, bg='powder blue')
    imgbtn = Button(right_frame,font=('aria',16,'bold'),text="Browse Image",fg='blue',command=choose_img,width=20).place(x=650,y=250)
    Label(right_frame,font=('aria',22,'bold'),bg="ghostwhite",text="REGISTRATION",fg='blue',bd=10,anchor='w').place(x=300,y=20)
    la1=Label(right_frame,font=('aria',16,'bold'),bg="ghostwhite",text="Patient Name :",fg='blue',bd=10,anchor='w').place(x=20,y=90)
    la2=Label(right_frame,font=('aria',16,'bold'),bg="ghostwhite",text="Date Of Birth :",fg='blue',bd=10,anchor='w').place(x=20,y=160)
    la3=Label(right_frame,font=('aria',16,'bold'),bg="ghostwhite",text="Gender :",fg='blue',bd=10,anchor='w').place(x=20,y=220)
    la4=Label(right_frame,font=('aria',16,'bold'),bg="ghostwhite",text="Contact No. :",fg='blue',bd=10,anchor='w').place(x=20,y=270)
    la5=Label(right_frame,font=('aria',16,'bold'),bg="ghostwhite",text="Address :",fg='blue',bd=10,anchor='w').place(x=20,y=330)
    la6=Label(right_frame,font=('aria',16,'bold'),bg="ghostwhite",text="Blood group :",fg='blue',bd=10,anchor='w').place(x=590,y=330)
    la7=Label(right_frame,font=('aria',16,'bold'),bg="ghostwhite",text="Aadhar No. :",fg='blue',bd=10,anchor='w').place(x=20,y=390)
    la8=Label(right_frame,font=('aria',16,'bold'),bg="ghostwhite",text="Email :",fg='blue',bd=10,anchor='w').place(x=20,y=450)
    
    e1=Entry(right_frame,font=('arial',16,'bold'), bd=6, insertwidth=4, bg='powder blue',width=28)
    e1.place(x=230,y=90)#pname
    #e2=Entry(right_frame,font=('arial',16,'bold'), bd=6, insertwidth=4, bg='powder blue').place(x=230,y=70)#yob
    def showdate():
        def top_on_closing():
            top.destroy()
        top.protocol("WM_DELETE_WINDOW", top_on_closing)
            
        def create_cal():
            top = Tk()
            style = ttk.Style(top)
            style.theme_use("alt")
            style.configure("style.TButton", font = "evogria 20 bold", background = "#FF847C", width = 20)
            style.map("TButton", background = [("active", "#2A363C")], foreground = [("active", "#FF847C")])
            global cal
            cal = Calendar(top,font = "Arial 14", selectmode = "day", cursor = "hand2")
            cal.pack(fill = "both", expand = True)

            def cal_done():
                top.withdraw()
                global dob_date
                dob_date = str(cal.selection_get())
                age_entry.config(text=dob_date)
                dob_entry_str.set(dob_date)
            ttk.Button(top, text = "ok", style = "style.TButton", command = cal_done).pack()

        create_cal()
    
    dob_entry_str = StringVar()
    dob_entry = Entry(right_frame,font=('arial',16,'bold'),textvariable=dob_entry_str, bd=6, insertwidth=4, bg='powder blue')
    
    age_entry = Button(right_frame,text="Select Date",font = "consolas 16 bold",width=18,command=showdate)
    age_entry.place(x=280,y=160)
    
    gender_entry = StringVar()
    gender_entry_male = Radiobutton(right_frame,text="Male",value="Male",variable = gender_entry,font = "consolas 16 bold")
    #gender_entry_male.deselect()
    gender_entry_female = Radiobutton(right_frame,text="Female" ,value="Female",variable = gender_entry,font = "consolas 16 bold")
    #gender_entry_female.deselect()
    gender_entry_other = Radiobutton(right_frame,text="Other" ,value="Other",variable = gender_entry,font = "consolas 16 bold")
    #gender_entry_other.deselect()
    gender_entry_male.place(x=230,y=220)
    gender_entry_female.place(x=340,y=220)
    gender_entry_other.place(x=470,y=220)
    
    e4=Entry(right_frame,font=('arial',16,'bold'), bd=6, insertwidth=4, bg='powder blue',width=28)
    e4.place(x=230,y=270)#contect no
    e5=Entry(right_frame,font=('arial',16,'bold'), bd=6, insertwidth=4, bg='powder blue',width=28)
    e5.place(x=230,y=330)#address
    e6=Entry(right_frame,font=('arial',16,'bold'), bd=6, insertwidth=4, bg='powder blue')#blood group
    blood_group_entry = Listbox(right_frame, font = "consolas 20",width=15,height=3)
    scrollbar = Scrollbar(right_frame,width=30,orient=VERTICAL)
    blood_group_entry.insert(END,"O+")
    blood_group_entry.insert(END,"O-")
    blood_group_entry.insert(END,"A+")
    blood_group_entry.insert(END,"A-")
    blood_group_entry.insert(END,"B+")
    blood_group_entry.insert(END,"B-")
    blood_group_entry.insert(END,"AB+")
    blood_group_entry.insert(END, "AB-")
    scrollbar.place(x=945,y=330)
    blood_group_entry.config(yscrollcommand = scrollbar.set)
    scrollbar.config(command = blood_group_entry.yview)
    blood_group_entry.place(x=750,y=330)
    
    e7=Entry(right_frame,font=('arial',16,'bold'), bd=6, insertwidth=4, bg='powder blue',width=28)
    e7.place(x=230,y=390)#aadhar
    e8=Entry(right_frame,font=('arial',16,'bold'), bd=6, insertwidth=4, bg='powder blue',width=30)
    e8.place(x=220,y=450)#email
    
    def clear_data():
        # clear the entry boxes
        choose_img_label.config(image=choose_ph)
        e1.delete(0, END)
        gender_entry_male.deselect()
        gender_entry_female.deselect()
        gender_entry_other.deselect()
        e4.delete(0, END)
        e5.delete(0,END)
        e6.delete(0,END)
        e7.delete(0,END)
        e8.delete(0,END)
        age_entry.config(text="Select Date")
        try:
            blood_group_entry.get(blood_group_entry.selection_clear(0,END))
        except:
            pass
    
    clear_b=Button(right_frame,command=clear_data,padx=8, pady=8,bd=4, fg="black" , font=('arial', 14, 'bold'),text='Clear', bg='powder blue',width=15)
    clear_b.place(x=50,y=520)
    b=Button(right_frame,command=insert,padx=8, pady=8,bd=4, fg="black" , font=('arial', 14, 'bold'),text='Register', bg='powder blue',width=15)
    b.place(x=730,y=520)
    b.update()

#----------------------------------------------------------Update Details-----------------------------------------------
def p_details_update():
    def update_patient_data():    
        global p_update_frame   
        p_update_frame = Frame(main,bd=2,width=1000,bg="ghostwhite",height=485)
        p_update_frame.place(x=360,y=210)
        try:
            patient_id = int(pid.get())
            operation = "SELECT *FROM patient_details where pid ='%d'"%(patient_id)
            cursor.execute(operation)
            results = cursor.fetchall()
            for rec in results:
                p_id = rec[0]
                p_images = rec[1]
                p_name = rec[2]
                p_yob = rec[3]
                p_gender = rec[4]
                p_contect = rec[5]
                p_address = rec[6]
                p_blood_group = rec[7]
                p_aadhar = rec[8]
                p_email = rec[9]
                p_diagnosis = rec[10]
                p_report = rec[11]
                p_doctor = rec[12]

            patientname = StringVar()
            patientyob = StringVar()
            patientgender = StringVar()
            patientcontact = StringVar()
            patientaddress = StringVar()
            patientbloodgroup = StringVar()
            patientaadhar = StringVar()
            patientemail = StringVar()
            
            global upload_ph
            upload_img2 = Image.open(io.BytesIO(p_images))
            resize_update_img = upload_img2.resize((200, 168))
            upload_ph=ImageTk.PhotoImage(resize_update_img)
            upload_img_label = Label(p_update_frame,image=upload_ph)
            upload_img_label.place(x=660,y=28)
            def upload_img():
                global upload_ph
                upload_file = filedialog.askopenfilename(filetypes=[("jpeg file","*.jpeg"),("jpg file","*.jpg"),("png file","*.png")])
                upload_file1 = str(upload_file)
                upload_final_file = upload_file1.replace("/","\\\\")
                upload_img=Image.open(upload_final_file)
                resize_upload_img = upload_img.resize((200, 168))
                upload_ph=ImageTk.PhotoImage(resize_upload_img)
                upload_img_label.configure(image=upload_ph)
                image_upload_entry_str.set(upload_final_file)
    
        
            image_upload_entry_str = StringVar()
            image_upload_entry = Entry(p_update_frame,font=('arial',16,'bold'),textvariable=image_upload_entry_str, bd=6, insertwidth=4, bg='powder blue')
            imguploadbtn = Button(p_update_frame,font=('aria',16,'bold'),text="Browse Image",fg='blue',command=upload_img,width=20).place(x=620,y=200)
    
            
            
            b = Label(p_update_frame,text="Patient Name        :",bg="ghostwhite",font=('arial',14,'bold'))
            b.place(x=20,y=20)
            e2 = Entry(p_update_frame,textvariable=patientname,font=('arial',14,'bold'),width=30)
            e2.place(x=250,y=20)
            patientname.set(str(p_name))
            b1 = Label(p_update_frame,text="Patient Year Of Birth :",bg="ghostwhite",font=('arial',14,'bold'))
            b1.place(x=20,y=70)
            e3 = Entry(p_update_frame,textvariable=patientyob,font=('arial',14,'bold'),width=30)
            e3.place(x=250,y=70)
            patientyob.set(str(p_yob))
            c = Label(p_update_frame,text="Patient Gender      :",bg="ghostwhite",font=('arial',14,'bold'))
            c.place(x=20,y=120)
            e4 = Entry(p_update_frame,textvariable=patientgender,font=('arial',14,'bold'),width=30)
            e4.place(x=250,y=120)
            patientgender.set(str(p_gender))
            d = Label(p_update_frame,text="Patient Contact     :",bg="ghostwhite",font=('arial',14,'bold'))
            d.place(x=20,y=170)
            e5 = Entry(p_update_frame,textvariable=patientcontact,font=('arial',14,'bold'),width=30)
            e5.place(x=250,y=170)
            patientcontact.set(str(p_contect))
            e = Label(p_update_frame,text="Patient Address     :",bg="ghostwhite",font=('arial',14,'bold'))
            e.place(x=20,y=220)
            e6 = Entry(p_update_frame,textvariable=patientaddress,font=('arial',14,'bold'),width=30)
            e6.place(x=250,y=220)
            patientaddress.set(str(p_address))
            f = Label(p_update_frame,text="Patient Blood Group :",bg="ghostwhite",font=('arial',14,'bold'))
            f.place(x=20,y=270)
            e7 = Entry(p_update_frame,textvariable=patientbloodgroup,font=('arial',14,'bold'),width=30)
            e7.place(x=250,y=270)
            patientbloodgroup.set(str(p_blood_group))
            g = Label(p_update_frame,text="Patient Aadhar      :",bg="ghostwhite",font=('arial',14,'bold'))
            g.place(x=20,y=320)
            e8 = Entry(p_update_frame,textvariable=patientaadhar,font=('arial',14,'bold'),width=30)
            e8.place(x=250,y=320)
            patientaadhar.set(str(p_aadhar))
            h = Label(p_update_frame,text="Patient Email       :",bg="ghostwhite",font=('arial',14,'bold'))
            h.place(x=20,y=370)
            e9 = Entry(p_update_frame,textvariable=patientemail,font=('arial',14,'bold'),width=30)
            e9.place(x=250,y=370)
            patientemail.set(str(p_email))
 
 #-----------------------------------------------------Updating Data-------------------------------------------------------------           
            def update_data():
                patient_id = int(p_id)
                pname = str(patientname.get())
                pyob = str(patientyob.get())
                pgender = str(patientgender.get())
                pcontect = str(patientcontact.get())
                paddress = str(patientaddress.get())
                pbloodgroup = str(patientbloodgroup.get())
                paadhar = str(patientaadhar.get())
                pemail = str(patientemail.get())
                
                try:
                    img_upload = image_upload_entry_str.get()    
                    Picture = digital_to_binary(img_upload)
                except:
                    Picture = p_images
                    #messagebox.showinfo("digital health card system","Image was not updated.")
                
                try:
                    operation = "UPDATE patient_details SET images=%s,name=%s,dob=%s,gender=%s,contact=%s,address=%s,blood_group=%s,aadhar=%s,email=%s where pid =%s"
                    data = (Picture,pname,pyob,pgender,pcontect,paddress,pbloodgroup,paadhar,pemail,patient_id)
                    cursor.execute(operation,data)
                    dbcon.commit()
                    messagebox.showinfo("digital health card system","Successfully Update record.")
                except:
                    messagebox.showerror("digital health card system","Images File To Long Please Select Another Image.")

        
            def more_data():
                clean_p_update_frame()
                pa = Label(p_update_frame,text="Patient ID          :"+str(p_id),bg="ghostwhite",font=('arial',14,'bold'))
                pa.place(x=20,y=20)
                pb = Label(p_update_frame,text="Patient Name        :"+str(p_name),bg="ghostwhite",font=('arial',14,'bold'))
                pb.place(x=20,y=70)
                
                pe4_details = StringVar()
                pe5_details = StringVar()
                pc = Label(p_update_frame,text="Patient Diagnosis :",bg="ghostwhite",font=('arial',14,'bold'))
                pc.place(x=20,y=120)
                
                pe4 = Text(p_update_frame,font=('arial',14,'bold'),width=50,height=3)
                pe4.place(x=250,y=120)
                pe4.insert("end",p_diagnosis)
                #pe4_details.set(p_diagnosis)
                
                #patientgender.set(str(p_gender))
                pd = Label(p_update_frame,text="Patient Report     :",bg="ghostwhite",font=('arial',14,'bold'))
                pd.place(x=20,y=220)
                
                pe5 = Text(p_update_frame,font=('arial',14,'bold'),width=50,height=3)
                pe5.place(x=250,y=220)
                pe5.insert("end",p_report)
                #pe5_details.set(p_report)
                
                p_doc = Label(p_update_frame,text="Doctor Name     :",bg="ghostwhite",font=('arial',14,'bold'))
                p_doc.place(x=20,y=320)
                
                #pe6 = Text(p_update_frame,font=('arial',14,'bold'),width=50,height=1)
                #pe6.place(x=250,y=320)
                #pe6.insert("end",p_doctor)
                
                pe6 = Entry(p_update_frame,font=('arial',14,'bold'))
                pe6.place(x=250,y=320)
                

                
                def update_more_data():
                    finaldiagnosisdetails = str(pe4.get("1.0","end"))
                    finalreportdetails = str(pe5.get("1.0","end"))
                    doctor_name = str(pe6.get())
                    
                    operation = "UPDATE patient_details SET diagnosis=%s,report=%s where pid =%s"
                    data = (finaldiagnosisdetails,finalreportdetails,patient_id)
                    cursor.execute(operation,data)
                    dbcon.commit()
                    
                    try:
                        if pe6.get() == "":
                            messagebox.showerror("digital health card system","Please enter the doctor name.")
                            return
                        op = "UPDATE patient_details SET doctor=%s where pid =%s"
                        d = (doctor_name,patient_id)
                        cursor.execute(op,d)
                        dbcon.commit()
                    except:
                        messagebox.showerror("digital health card system","Please enter doctor name.")
                        return
                    
                    send_email = str(p_email)
                    gmail_user = 'digitalhealthcardsystem@gmail.com'
                    gmail_password = ''
                    sent_from = gmail_user
                    to = [send_email]
                    body = 'your data has been successfully updated by '+doctor_name
                    email_text = """
                    From: %s
                    To: %s
                    Subject: Digital Health Card System
        
        
        
        

                    %s                         
                    """ % (sent_from,",".join(to) ,body)

                    u_pat_mail = True
                    try:
                        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                        server.ehlo()
                        server.login(gmail_user, gmail_password)
                        server.sendmail(sent_from, to, email_text)
                        server.close()
                        u_pat_mail = True
                        print('Email sent!')
                    except:
                        print('Something went wrong...')
                        # messagebox.showerror("Digital Health Card System","Email was does not send...")
                        u_pat_mail = False
                    
                    if u_pat_mail == True:
                        messagebox.showinfo("digital health card system","Successfully More Data Update record and The credentials have been sent to your registered email address.")
                    else:
                        messagebox.showwarning("digital health card system","Successfully More Data Update record. However, the credentials could not be sent to your registered email address.")

                pbtn = Button(p_update_frame,text="Update",font=('arial',14,'bold'),command=update_more_data)
                pbtn.place(x=480,y=420)
                pbtn2 = Button(p_update_frame,text="Back",font=('arial',14,'bold'),command=update_patient_data)
                pbtn2.place(x=260,y=420)
            
        
            btn = Button(p_update_frame,text="Update",font=('arial',14,'bold'),command=update_data)
            btn.place(x=480,y=420)
            
            btn2 = Button(p_update_frame,text="Add More",font=('arial',14,'bold'),command=more_data)
            btn2.place(x=260,y=420)
            
        except:
            messagebox.showerror("digital health card system","Something went wrong!")
   
#--------------------------------------------Clean Right Frame Function---------------------------------------------------------------------
    
    clean_right_frame()
    titlelable = Label(right_frame,text="Update Patient Details",bg="ghostwhite",font=('arial',24,'bold'))
    titlelable.place(x=400,y=5)
    lbl = Label(right_frame,text="Enter Pid :",bg="ghostwhite",font=('arial',18,'bold'))
    lbl.place(x=5,y=70)
    pid = Entry(right_frame,font=('arial',18,'bold'),bg="ghostwhite",width=47)
    pid.place(x=150,y=70)
    searchbtn = Button(right_frame,text="Search",bg="ghostwhite",font=('arial',18,'bold'),width=10,command=update_patient_data)
    searchbtn.place(x=800,y=65)


#-----------------------------------------------------Show Details-------------------------------------------------------
def view():
    def showdata():
        p_details_frame = Frame(main,bd=2,width=1000,bg="ghostwhite",height=485)
        p_details_frame.place(x=360,y=210)
        try:
            patient_id = int(pid.get())
            operation = "SELECT *FROM patient_details where pid ='%d'"%(patient_id)
            cursor.execute(operation)
            results = cursor.fetchall()
            for rec in results:
                p_image = rec[1]
                p_id = rec[0]
                p_name = rec[2]
                p_yob = rec[3]
                p_gender = rec[4]
                p_contect = rec[5]
                p_address = rec[6]
                p_blood_group = rec[7]
                p_aadhar = rec[8]
                p_email = rec[9]
                p_diagnosis = rec[10]
                p_report = rec[11]
                p_doctor = rec[12]
            
            show_img = Image.open(io.BytesIO(p_image))
            global show_ph   
            resize_show_img = show_img.resize((200, 170))
            show_ph=ImageTk.PhotoImage(resize_show_img)
            #choose_img_label.configure(image=choose_ph2)
            
            show_img_label = Label(p_details_frame,image=show_ph)
            show_img_label.place(x=685,y=20)
            a = Label(p_details_frame,text="Patient ID          :"+str(p_id),bg="ghostwhite",font=('arial',14,'bold'))
            a.place(x=20,y=20)
            b = Label(p_details_frame,text="Patient Name        :"+str(p_name),bg="ghostwhite",font=('arial',14,'bold'))
            b.place(x=20,y=70)
            b1 = Label(p_details_frame,text="Patient Year Of Birth :"+str(p_yob),bg="ghostwhite",font=('arial',14,'bold'),width=55,anchor="sw")
            b1.place(x=20,y=120)
            c = Label(p_details_frame,text="Patient Gender      :"+str(p_gender),bg="ghostwhite",font=('arial',14,'bold'))
            c.place(x=20,y=170)
            d = Label(p_details_frame,text="Patient Contact     :"+str(p_contect),bg="ghostwhite",font=('arial',14,'bold'),width=55,anchor="sw")
            d.place(x=20,y=220)
            e = Label(p_details_frame,text="Patient Address     :"+str(p_address),bg="ghostwhite",font=('arial',14,'bold'))
            e.place(x=20,y=270)
            f = Label(p_details_frame,text="Patient Blood Group :"+str(p_blood_group),bg="ghostwhite",font=('arial',14,'bold'))
            f.place(x=20,y=320)
            g = Label(p_details_frame,text="Patient Aadhar      :"+str(p_aadhar),bg="ghostwhite",font=('arial',14,'bold'))
            g.place(x=20,y=370)
            h = Label(p_details_frame,text="Patient Email       :"+str(p_email),bg="ghostwhite",font=('arial',14,'bold'))
            h.place(x=20,y=420)

            def more():
                a = Label(p_details_frame,text="Patient ID          :"+str(p_id),bg="ghostwhite",font=('arial',14,'bold'))
                a.place(x=20,y=20)
                b = Label(p_details_frame,text="Patient Name        :"+str(p_name),bg="ghostwhite",font=('arial',14,'bold'))
                b.place(x=20,y=70)
                b1.config(text="Patient Diagnosis        :"+str(p_diagnosis),bg="ghostwhite",font=('arial',14,'bold'))
                c.config(text="")
                d.config(text="Patient Report        :"+str(p_report),bg="ghostwhite",font=('arial',14,'bold'))
                e.config(text="")
                f.config(text="Last Record Updated by        :"+str(p_doctor))
                g.config(text="")
                h.config(text="")
                morebtn.destroy()
                btn = Button(p_details_frame,text="Back",font=('arial',14,'bold'),fg="red",bg="yellow",command=showdata)
                btn.place(x=850,y=420)
            
            morebtn = Button(p_details_frame,text="View More",font=('arial',14,'bold'),fg="red",bg="yellow",command=more)
            morebtn.place(x=850,y=420)
        except:
            messagebox.showerror("Digital health card system","Please enter valid pid number")
    
    clean_right_frame()
    titlelable = Label(right_frame,text="View Patient Details",bg="ghostwhite",font=('arial',24,'bold'))
    titlelable.place(x=400,y=5)
    lbl = Label(right_frame,text="Enter Pid :",bg="ghostwhite",font=('arial',18,'bold'))
    lbl.place(x=5,y=70)
    pid = Entry(right_frame,font=('arial',18,'bold'),width=47)
    pid.place(x=150,y=70)
    searchbtn = Button(right_frame,text="Search",font=('arial',18,'bold'),width=10,command=showdata)
    searchbtn.place(x=800,y=65)

#----------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------Login Screen------------------------------------------------------------------        
def check():
    operation = "SELECT *FROM doctor_details where username ='%s'"%(getusername.get())
    cursor.execute(sql.SQL(operation))
    results = cursor.fetchall()

    for rec in results:
        global doctor_password
        d_username = rec[0]
        doctor_password = rec[1]
            
    # if(getusername.get()=='1' and getpassword.get()=='1'):
    #    messagebox.showinfo("Digital health card system","welcome to digital health card system")
    #    loginscreen.withdraw()
    #    main.deiconify()
    #    main.state("zoomed")
    #    getusername.set("")
    #    getpassword.set("")
        
    if e.get()=="" and e1.get()=="":
        messagebox.showerror("Digital health card system","All field are empty")
        main.withdraw()
        loginscreen.deiconify()
        getusername.set("")
        getpassword.set("")
        return
    elif e.get()=="":
        messagebox.showerror("Digital health card system","Plaese Enter The Username")
        main.withdraw()
        loginscreen.deiconify()
        getusername.set("")
        getpassword.set("")
        return
    elif e1.get()=="":
        messagebox.showerror("Digital health card system","Please Enter The Password")
        loginscreen.deiconify()
        getusername.set("")
        getpassword.set("")
        return
    
    try:    
        if getpassword.get() == doctor_password and getusername.get() == d_username:
            try:
                messagebox.showinfo("Digital health card system","welcome to digital health card system")
                loginscreen.withdraw()
                main.deiconify()
                main.state("zoomed")
                getusername.set("")
                getpassword.set("")
                return
            except:
                messagebox.showwarning("Digital health card system","Username and Password was wrong")
            
        else:
            messagebox.showwarning("Digital health card system","Username and Password was wrong")
            main.withdraw()
            loginscreen.deiconify()
            getusername.set("")
            getpassword.set("")
            return
    except:
        messagebox.showwarning("Digital health card system","Username and Password was wrong")
        main.withdraw()
        loginscreen.deiconify()
        getusername.set("")
        getpassword.set("")
        return


#-------------------------------------------------------About us Screen-------------------------------------------------------
def about_window():
    clean_right_frame()
    right_frame.config(bg = "#FFE2E2")
    main_label = Label(right_frame,text="About US",font = "consolas 19 bold", bg = "#FFE2E2")
    main_label.place(x=380,y=5)
    about_lable1 = Label(right_frame,text="A Health ID allows you to store all your digital health records",font = "consolas 19 bold", bg = "#FFE2E2")
    about_lable1.place(x=5,y=80)
    about_lable2 = Label(right_frame,text="at one place and share these records with hospitals/doctors",font = "consolas 19 bold",bg = "#FFE2E2")
    about_lable2.place(x=5,y=120)
    about_lable3 = Label(right_frame,text="you visit, with your consent, with suitable applications. ",font = "consolas 19 bold",bg = "#FFE2E2")
    about_lable3.place(x=5,y=160)
    about_lable4 = Label(right_frame,text="9th Floor Tower-I,Connaught Place, ",font = "consolas 19 bold",bg = "#FFE2E2")
    about_lable4.place(x=5,y=280)
    about_lable5 = Label(right_frame,text="Jeevan Bharati Building,",font = "consolas 19 bold",bg = "#FFE2E2")
    about_lable5.place(x=5,y=320)
    about_lable6 = Label(right_frame,text="Mum- 400071 .",font = "consolas 19 bold",bg = "#FFE2E2")
    about_lable6.place(x=5,y=360)
    about_lable7 =Label(right_frame,text="contact us on:-",font = "consolas 19 bold",bg = "#FFE2E2")
    about_lable7.place(x=510,y=400)
    about_lable8 =Label(right_frame,text="1800-11-4477 / 14477",font = "consolas 19 bold",bg = "#FFE2E2")
    about_lable8.place(x=510,y=440)
    about_lable9 =Label(right_frame,text="digitalhealthcard@gmail.com",font = "consolas 19 bold",bg = "#FFE2E2")
    about_lable9.place(x=510,y=480)

#---------------------------------------------------Home Button------------------------------------------------------------
def log_out():
    main.withdraw()
    loginscreen.deiconify()

def home():
    top_frame = Frame(main,bd=3)
    top_frame.place(x=0,y=0)

    title = Label(top_frame, text = "Digital Health Card System", font = "evogria 45",bg = "#FFE2E2", width = 42, anchor = CENTER)
    title.pack()
    left_frame = Frame(main,bd=2,width=350,bg="ghostwhite",height=620,relief=RAISED)
    left_frame.place(x=0,y=80)
    right_frame = Frame(main,bd=2,width=1000,bg="ghostwhite",height=620,relief=RAISED)
    right_frame.place(x=360,y=80)

    global ph
    img=Image.open(r"home photo.jpeg")
    resizeimg = img.resize((1000, 620))
    ph=ImageTk.PhotoImage(resizeimg)
    homeimg = Label(right_frame,image=ph)
    homeimg.grid(row=0,column=0)

    homebtn=Button(left_frame,padx=16,pady=16, bd=4, fg='black', font=('arial',16,'bold'), text="Home",bg="powder blue",command=home,width=18)
    homebtn.place(x=10,y=20)

    b1=Button(left_frame,padx=16,pady=16, bd=4, fg='black', font=('arial',16,'bold'), text="Registration",bg="powder blue",command=new_register,width=18)
    b1.place(x=10,y=120)
        
    b3=Button(left_frame,padx=16,pady=16,bd=4, fg='black', font=('arial',16,'bold'),     text='Update Patient Details', bg='powder blue',width=18,command=p_details_update)
    b3.place(x=10,y=320)

    b4=Button(left_frame,padx=16,pady=16,bd=4, fg='black', font=('arial',16,'bold'),     text='Contact US', bg='powder blue',width=18,command=about_window)
    b4.place(x=10,y=420)

    b6=Button(left_frame,padx=16,pady=16, bd=4, fg='black', font=('arial',16,'bold'), text="View Patient Details",bg="powder blue",command=view,width=18)
    b6.place(x=10,y=220)
    
    logout = Button(left_frame,padx=8,pady=8, bd=2, fg='black', font=('arial',12,'bold'), text="Log-Out",bg="powder blue",command=log_out,width=7)
    logout.place(x=10,y=550) 

#----------------------------------------------------Main Screen---------------------------------------------------------------
top_frame = Frame(main,bd=3)
top_frame.place(x=0,y=0)

title = Label(top_frame, text = "Digital Health Card System", font = "evogria 45",bg = "#FFE2E2", width = 42, anchor = CENTER)
title.pack()
left_frame = Frame(main,bd=2,width=350,bg="ghostwhite",height=620,relief=RAISED)
left_frame.place(x=0,y=80)
right_frame = Frame(main,bd=2,width=1000,bg="ghostwhite",height=620,relief=RAISED)
right_frame.place(x=360,y=80)

img=Image.open(r"home photo.jpeg")
resizeimg = img.resize((1000, 620))
ph=ImageTk.PhotoImage(resizeimg)
homeimg = Label(right_frame,image=ph)
homeimg.grid(row=0,column=0)

homebtn=Button(left_frame,padx=16,pady=16, bd=4, fg='black', font=('arial',16,'bold'), text="Home",bg="powder blue",command=home,width=18)
homebtn.place(x=10,y=20)

b1=Button(left_frame,padx=16,pady=16, bd=4, fg='black', font=('arial',16,'bold'), text="Registration",bg="powder blue",command=new_register,width=18)
b1.place(x=10,y=120)
        
b3=Button(left_frame,padx=16,pady=16,bd=4, fg='black', font=('arial',16,'bold'),     text='Update Patient Details', bg='powder blue',width=18,command=p_details_update)
b3.place(x=10,y=320)

b4=Button(left_frame,padx=16,pady=16,bd=4, fg='black', font=('arial',16,'bold'),     text='Contact US', bg='powder blue',width=18,command=about_window)
b4.place(x=10,y=420)

b6=Button(left_frame,padx=16,pady=16, bd=4, fg='black', font=('arial',16,'bold'), text="View Patient Details",bg="powder blue",command=view,width=18)
b6.place(x=10,y=220) 

logout = Button(left_frame,padx=8,pady=8, bd=2, fg='black', font=('arial',12,'bold'), text="Log-Out",bg="powder blue",command=log_out,width=7)
logout.place(x=10,y=550)   
#---------------------------------------------------Digital Health Care Card--------------------------------------------
img2=r"digitalhealthcardsystemqrcode.png"
img2_final = Image.open(img2) 
resizeimg2 = img2_final.resize((200, 168))
ph2=ImageTk.PhotoImage(resizeimg2)

def viewcard():
    def cardback():
        card.withdraw()
        loginscreen.deiconify()
    def viewhealthcard():
        try:
            global pid2
            global cpatient_id
            cpatient_id = int(pid2.get())
            operation = "SELECT *FROM patient_details where pid ='%d'"%(cpatient_id)
            cursor.execute(operation)
            results = cursor.fetchall()
            global cp_id
            for rec in results:
                cp_id = rec[0]
                p_images = rec[1]
                p_name = rec[2]
                p_yob = rec[3]
                p_contect = rec[5]
                p_email = rec[9]
            
                ex = Label(card_frame,text=" ",font=('arial',14,'bold'),bg="ghostwhite",width=40,anchor='sw')
                ex.grid(row=1,column=1)
                a = Label(card_frame,text="Patient ID          :"+str(cp_id),bg="ghostwhite",font=('arial',14,'bold'),width=40,anchor='sw')
                a.grid(row=2,column=1)
                b = Label(card_frame,text="Patient Name        :"+str(p_name),bg="ghostwhite",font=('arial',14,'bold'),width=40,anchor='sw')
                b.grid(row=3,column=1)
                b1 = Label(card_frame,text="Patient Year Of Birth :"+str(p_yob),bg="ghostwhite",font=('arial',14,'bold'),width=40,anchor='sw')
                b1.grid(row=4,column=1)
                d = Label(card_frame,text="Patient Contact     :"+str(p_contect),bg="ghostwhite",font=('arial',14,'bold'),width=40,anchor='sw')
                d.grid(row=5,column=1)
                h = Label(card_frame,text="Patient Email       :"+str(p_email),bg="ghostwhite",font=('arial',14,'bold'),width=40,anchor='sw')
                h.grid(row=6,column=1)
                ex_final = Label(card_frame,text=" ",font=('arial',14,'bold'),bg="ghostwhite",width=40,anchor='sw')
                ex_final.grid(row=7,column=1)
            
                global card_ph
                card_img = Image.open(io.BytesIO(p_images))
                resize_card_img = card_img.resize((200, 168))
                card_ph=ImageTk.PhotoImage(resize_card_img)
            
                homeimg1 = Label(card_frame,image=card_ph)
                homeimg1.place(x=30,y=70)
                homeimg2 = Label(card_frame,image='')
                homeimg2.place(x=710,y=70)
        
            homeimg2.configure(image=ph2)
        except:
            messagebox.showerror("digital health card system","please enter valid pid number.")
        
    card.deiconify()
    card.state("zoomed")
    loginscreen.withdraw()
    main.withdraw()
    Label(card,bd=4, fg="black" , font=('arial', 24, 'bold'),text='View Digital Health Card', bg='powder blue').place(x=520,y=30)
        
    global pid2
    pid2 = StringVar()
    clbl = Label(card_frame,text="Enter Pid :",font=('arial',18,'bold'),width=15)
    clbl.grid(row=0,column=0)
    cpid = Entry(card_frame,font=('arial',18,'bold'),width=40,textvariable=pid2)
    cpid.grid(row=0,column=1)
    csearchbtn = Button(card_frame,text="Search",font=('arial',18,'bold'),width=15,command=viewhealthcard)
    csearchbtn.grid(row=0,column=2)
    
    backbtn = Button(card,bd=4, fg="black" , font=('arial', 16, 'bold'),text='Back', bg='ghostwhite', command=cardback,width=10)
    backbtn.place(x=1200,y=640)

#----------------------------------------------------Closing function----------------------------------------------------------------------------
d_reg = Toplevel()
d_reg.title("Digital Health Card System")
d_reg.iconbitmap(r"healthcare_icon.ico")
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()
    else:
        pass
loginscreen.protocol("WM_DELETE_WINDOW", on_closing)
main.protocol("WM_DELETE_WINDOW", on_closing)
card.protocol("WM_DELETE_WINDOW", on_closing)
d_reg.protocol("WM_DELETE_WINDOW", on_closing)

def d_reg_clear():
        de1.set("")
        de2.set("")
        de3.set("")
        de4.set("")
        de5.set("")
        
    
de1 = StringVar()
de2 = StringVar()
de3 = StringVar()
de4 = StringVar()
de5 = StringVar()
d_reg_lbl = Label(d_reg,text="DOCTOR REGISTRATION",font=("times new roman",15,"bold"),bg="ghostwhite",fg="red").place(x=550,y=10)
    
d_reg_name = Label(d_reg,text="USERNAME :",font=("times new roman",15,"bold"),bg="ghostwhite",fg="red").place(x=400,y=100)
pe1 = Entry(d_reg,textvariable=de1,font=("times new roman",15,"bold"),bd=6, insertwidth=4, bg='ghostwhite',width=30).place(x=600,y=100)
    
d_reg_pass1 = Label(d_reg,text="PASSWORD :",font=("times new roman",15,"bold"),bg="ghostwhite",fg="red").place(x=400,y=140)
pe2 = Entry(d_reg,textvariable=de2,font=("times new roman",15,"bold"),bd=6, insertwidth=4, bg='ghostwhite',width=30).place(x=600,y=140)
    
d_reg_pass2 = Label(d_reg,text="Confirmed Password :",font=("times new roman",15,"bold"),bg="ghostwhite",fg="red").place(x=400,y=180)
pe3 = Entry(d_reg,textvariable=de3,font=("times new roman",15,"bold"),bd=6, insertwidth=4, bg='ghostwhite',width=30).place(x=600,y=180)
    
d_reg_num = Label(d_reg,text="Phone Number :",font=("times new roman",15,"bold"),bg="ghostwhite",fg="red").place(x=400,y=220)
pe4 = Entry(d_reg,textvariable=de4,font=("times new roman",15,"bold"),bd=6, insertwidth=4, bg='ghostwhite',width=30).place(x=600,y=220)
    
d_reg_email = Label(d_reg,text="Email :",font=("times new roman",15,"bold"),bg="ghostwhite",fg="red").place(x=400,y=260)
pe5 = Entry(d_reg,textvariable=de5,font=("times new roman",15,"bold"),bd=6, insertwidth=4, bg='ghostwhite',width=30).place(x=600,y=260)

def d_reg_pass():
    loginscreen.withdraw()
    d_reg_login.deiconify()


def d_reg_entry():
    a = str(de1.get())
    b = str(de2.get())
    b_1 = str(de3.get())
    c = str(de4.get())
    d = str(de5.get())
    
    data = [a,b,b_1,c,d]   
    num = ['0','1','2','3','4','5','6','7','8','9'] 
    for i in data:
        if (i == a):
            if (len(i) == 0):
                messagebox.showerror("Digital Health Card System", "Please enter Userame.")
                return
            for n in num:
                if (n in a):
                    messagebox.showerror("Digital Health Card System", "Name should not contain any number.")
                    return
        elif (i == b):
            if ( len(i)==0):
                messagebox.showerror("Digital Health Card System", "Please enter password.")
                return
        elif (b != b_1):
            messagebox.showerror("Digital Health Card System","please enter new password same as well as confirmed password.")
            return
        elif (i == c):
            if (len(i) != 10):
                messagebox.showerror("Digital Health Card System", "Please enter valid 10 digits of Contact Number.")
                return
            try:
                con = int(c)
            except:
                messagebox.showerror("Digital Health Card System", "Number should not contain any character.")
                return
            if (i[0]=='7' or i[0]=='8' or i[0]=='9'):
                pass
            else:
                messagebox.showerror("Digital Health Card System", "A number should start with 7 or 8 or 9")
                return
        if ( i == d):
            if (len(i) == 0):
                messagebox.showerror("Digital Health Card System","Please enter Email Address.")
                return
            
        if(i == d):
            pat = r"^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
            if not re.match(pat,i):
                messagebox.showerror("Digital Health Card System","Please enter valid email address.")
                return
    
    
    try:        
        operation = """INSERT INTO doctor_details(username,password, contact, email) VALUES
					(%s,%s,%s,%s)"""
        values = (a, b, c, d)
        cursor.execute(operation,values)
        dbcon.commit()
        
        try:
            socket.create_connection(("google.com", 80), timeout=3)

            send_email = str(de5.get())
            gmail_user = 'digitalhealthcardsystem@gmail.com'
            gmail_password = ''
            sent_from = gmail_user
            to = [send_email]
            body = 'your doctor id registration has been successfully registered.'
            email_text = """
            From: %s
            To: %s
            Subject: Digital Health Card System
            
            
            
            
            
            %s                         
            """ % (sent_from,",".join(to) ,body)
            
            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=60)
                server.ehlo()
                server.login(gmail_user, gmail_password)
                server.sendmail(sent_from, to, email_text)
                server.close()

                print('Email sent!')
                messagebox.showinfo("Digital Health Card System","Doctor registration has been successfully registered and The credentials have been sent to your registered email address.")
            except:
                print('Something went wrong...')
                messagebox.showwarning("Digital Health Card System","Doctor registration has been successfully completed. However, the credentials could not be sent to your registered email address.")
        except Exception as e:
            messagebox.showwarning("Digital Health Card System","Doctor registration has been successfully completed. However, the credentials could not be sent to your registered email address.")
        
        d_reg_clear()
        d_reg.withdraw()
        loginscreen.deiconify()
        
    except Exception as e:
        messagebox.showerror("Digital Health Card System","This username was already exist.")
        return


d_sub = Button(d_reg,bd=2, fg="black" , font=('arial', 10, 'bold'),text='Submit', bg='powder blue', command=d_reg_entry,width=10)
d_sub.place(x=660,y=310)

def d_reg_back():
    d_reg.withdraw()
    loginscreen.deiconify()    
    
d_back = Button(d_reg,bd=2, fg="black" , font=('arial', 14, 'bold'),text='Back', bg='powder blue', command=d_reg_back,width=10)
d_back.place(x=1160,y=610)    
    
d_clear = Button(d_reg,bd=2, fg="black" , font=('arial', 10, 'bold'),text='Clear', bg='powder blue', command=d_reg_clear,width=10)
d_clear.place(x=770,y=310)
    
d_reg.state("zoomed")
d_reg.withdraw()
def d_reg_def():
    loginscreen.withdraw() 
           
def d_check():    
    if d_getusername.get()=="" and d_getpassword.get()=="":
        messagebox.showerror("Digital health card system","Please Enter Username and Password")
        main.withdraw()
        return
    elif d_getpassword.get()=="":
        messagebox.showinfo("Digital health card system","Plaese Enter The Password")
        main.withdraw()
        d_reg_login.deiconify()
        return
    elif d_getusername.get()=="":
        messagebox.showinfo("Digital health card system","Please Enter The Username")
        main.withdraw()
        d_reg_login.deiconify()
        return
    elif(d_getusername.get()=='admin' and d_getpassword.get()=='admin'):
        d_reg.state("zoomed")
        d_reg_login.withdraw()
        d_reg.deiconify()
        d_getusername.set("")
        d_getpassword.set("")
    else:
        messagebox.showerror("Digital health card system","Username and Password was wrong.")
        main.withdraw()
        d_reg_login.deiconify()
        d_getusername.set("")
        d_getpassword.set("")
        return
    
d_reg_login = Toplevel()
d_reg_login.title("Digital Health Card System")
d_reg_login.iconbitmap(r"healthcare_icon.ico")
loginlabel = Label(d_reg_login,text="Admin Login",font=('arial',16,'bold'),fg='blue',bd =10, anchor ='w')
loginlabel.place(x=170,y=5)

d_l=Label(d_reg_login, font=('arial',16,'bold'),text='username', fg='blue',bd =10, anchor ='w').place(x=10,y=50)
d_l1=Label(d_reg_login, font=('arial',16,'bold'),text='password', fg='blue',bd =10, anchor ='w').place(x=10,y=110)
d_getusername=StringVar()
d_getpassword=StringVar()
d_e=Entry(d_reg_login,font=('arial',16,'bold'), bd=6, insertwidth=4, bg='powder blue',textvariable=d_getusername)
d_e.place(x=135,y=50)
d_e1=Entry(d_reg_login,font=('arial',16,'bold'), bd=6, insertwidth=4, bg='powder blue',textvariable=d_getpassword)
d_e1.place(x=135,y=110)
d_b= Button(d_reg_login,bd=4, fg="black" , font=('arial', 16, 'bold'),text='submit', bg='powder blue', command=d_check,width=6).place(x=20,y=180)

def d_login_back():
        d_reg_login.withdraw()
        loginscreen.deiconify()

d_b1= Button(d_reg_login,bd=4, fg="black" , font=('arial', 16, 'bold'),text='back', bg='powder blue', command=d_login_back,width=6).place(x=145,y=180)
d_reg_login.geometry("400x250+500+200")


loginlabel = Label(loginscreen,text="Login",font=('arial',16,'bold'),fg='blue',bd =10, anchor ='w')
loginlabel.place(x=170,y=5)

d_reg_btn = Button(loginscreen,bd=2, fg="black" , font=('arial', 10, 'bold'),text='Admin', bg='powder blue', command=d_reg_pass,width=10)
d_reg_btn.place(x=305,y=5)

l=Label(loginscreen, font=('arial',16,'bold'),text='username', fg='blue',bd =10, anchor ='w').place(x=10,y=50)
l1=Label(loginscreen, font=('arial',16,'bold'),text='password', fg='blue',bd =10, anchor ='w').place(x=10,y=110)
getusername=StringVar()
getpassword=StringVar()
e=Entry(loginscreen,font=('arial',16,'bold'), bd=6, insertwidth=4, bg='powder blue',textvariable=getusername)
e.place(x=135,y=50)
e1=Entry(loginscreen,font=('arial',16,'bold'), bd=6, insertwidth=4, bg='powder blue',textvariable=getpassword)
e1.place(x=135,y=110)
b= Button(loginscreen,bd=4, fg="black" , font=('arial', 16, 'bold'),text='Login', bg='powder blue', command=check,width=6).place(x=20,y=180)
b1= Button(loginscreen,bd=4, fg="black" , font=('arial', 16, 'bold'),text='View Digital Health Card', bg='powder blue', command=viewcard,width=19).place(x=125,y=180)
loginscreen.geometry("400x250+500+200")
d_reg_login.withdraw()
loginscreen.deiconify()
main.withdraw()
card.withdraw()

card_frame = Frame(card,bd=3,bg="ghostwhite")
card_frame.place(x=170,y=150)

card.mainloop()
main.mainloop()
