import tkinter
from tkinter import ttk
import sqlite3
import numpy
import pygame
import random
from tkinter import messagebox
pygame.mixer.init()

class DataBase:

    def __init__(self):
        self.Open()
        self.Cursor.execute("""CREATE TABLE IF NOT EXISTS karbar(
                               UserName char PRIMARY KEY, 
                               Password char,
                               FirstName char,
                               LastName char,
                               Games int,
                               Wins int
                               );""")
        self.Connect.commit()
        self.Cursor.execute("select * from karbar;")
        if len(self.Cursor.fetchall())==0:
            self.Cursor.execute("""INSERT INTO karbar
                                   (UserName, Password, FirstName, LastName, Games, Wins)
                                   VALUES 
                                   ("admin", "123456", "None", "None", 0, 0)""")
            self.Connect.commit()
        self.Close()

    def Check(self, x, y):
        self.Open()
        if y==1:
            self.Cursor.execute("select UserName from karbar;")
            list=self.Cursor.fetchall()
            self.Close()
            for i in list:
                if x==i[0]:
                    return True
            return False
        elif y==2:
            self.Cursor.execute("select Password from karbar;")
            list=self.Cursor.fetchall()
            self.Close()
            for i in list:
                if x==i[0]:
                    return True
            return False
    def Insert(self, UserName, Password, FirstName, LastName):
        self.Open()
        self.Cursor.execute("""INSERT INTO karbar
                               (UserName, Password, FirstName, LastName, Games, Wins)
                               VALUES 
                               (?, ?, ?, ?, 0, 0)""", (UserName, Password, FirstName, LastName))
        self.Connect.commit()
        self.Close()

    def Change(self, UserName, x, y):
        self.Open()
        query=""

        if y==1:
            query="""Update karbar set Password = ? where UserName = ?"""
        elif y==2:
            query="""Update karbar set FirstName = ? where UserName = ?"""
        elif y==3:
            query="""Update karbar set LastName = ? where UserName = ?"""
        elif y==4:
            query="""Update karbar set Games = ? where UserName = ?"""
        elif y==5:
            query="""Update karbar set Wins = ? where UserName = ?"""

        self.Cursor.execute(query, (x, UserName))
        self.Connect.commit()
        self.Close()

    def Show(self, UserName):
        self.Open()
        self.Cursor.execute("select * from karbar where UserName = ?;", (UserName,))
        answer=self.Cursor.fetchall()
        self.Close()
        return answer[0]

    def Show_Users(self):
        self.Open()
        self.Cursor.execute("select UserName from karbar;")
        List=self.Cursor.fetchall()
        return List
        self.Close()


    def Close(self):
        self.Cursor.close()
        self.Connect.close()

    def Open(self):
        self.Connect=sqlite3.connect('karbar.db')
        self.Cursor=self.Connect.cursor()

class EnterPage:
    def __init__(self):
        self.Page=tkinter.Tk()
        self.Page.geometry('400x400')
        self.User=tkinter.Entry(self.Page, width=20, bg='yellow', font=('arial'))
        self.LabelUser=tkinter.Label(text='User Name :', font=('arial'))
        self.Password=tkinter.Entry(self.Page, width=20, bg='yellow', font=('arial'))
        self.LabelPassword=tkinter.Label(text='Password   :', font=('arial'))
        self.SignIn=tkinter.Button(self.Page, text='Sign Up', command=self.sign_up)
        self.Login=tkinter.Button(self.Page, text='Login', command=self.enter)
        self.Info = tkinter.Label(self.Page, text='Enter your user name and password \n if you want create account,signup',font=('arial'))
        self.First=False
        self.UserName=""

    def show(self):
        self.User.place(x=120, y=100)
        self.LabelUser.place(x=0, y=100)
        self.Password.place(x=120, y=150)
        self.LabelPassword.place(x=0, y=150)
        self.SignIn.place(x=100, y=200)
        self.Login.place(x=244, y=200)
        self.Info.place(x=58, y=300)
        self.Page.mainloop()

    def enter(self):
        if dataBase.Check(self.User.get(), 1) and dataBase.Check(self.Password.get(), 2):
            if self.User.get()=='admin' and self.Password.get()=='123456':
                self.First=True
            self.UserName=self.User.get()
            self.Page.destroy()
            checkAdmin=CheckAdmin()
            checkAdmin.check()

        else:
            if self.User.get() or self.Password.get():
                self.Info.config(text='The password or user name is incorrect\ntry again or signup', fg='red')

            else:
                self.Info.config(text='please enter your user name and password', fg='red')

    def sign_up(self):
        self.NewWin=tkinter.Toplevel()
        self.NewWin.geometry('400x300')
        self.UserEntry=tkinter.Entry(self.NewWin, width=20, font=('arial'), bg='yellow')
        self.UserLabel=tkinter.Label(self.NewWin, text='User Name :', font=('arial'))
        self.PasswordEntry=tkinter.Entry(self.NewWin, width=20, font=('arial'), bg='yellow')
        self.PasswordLabel=tkinter.Label(self.NewWin, text='Password   :', font=('arial'))
        self.FirstNameEntry=tkinter.Entry(self.NewWin, width=20, font=('arial'), bg='yellow')
        self.FirstNameLabel=tkinter.Label(self.NewWin, text='First Name :', font=('arial'))
        self.LastNameEntry=tkinter.Entry(self.NewWin, width=20, font=('arial'), bg='yellow')
        self.LastNameLabel=tkinter.Label(self.NewWin, text='Last Name :', font=('arial'))
        Button=tkinter.Button(self.NewWin, command=self.insert, text='Sign Up')
        self.UserEntry.place(x=120, y=40)
        self.UserLabel.place(x=0, y=40)
        self.PasswordEntry.place(x=120, y=80)
        self.PasswordLabel.place(x=0, y=80)
        self.FirstNameEntry.place(x=120, y=120)
        self.FirstNameLabel.place(x=0, y=120)
        self.LastNameEntry.place(x=120, y=160)
        self.LastNameLabel.place(x=0, y=160)
        Button.place(x=170, y=200)

    def insert(self):
        LabelError = tkinter.Label(self.NewWin, font=('arial'), fg='red')
        LabelError.place(x=100, y=0)
        if self.UserEntry.get() and self.PasswordEntry.get() and self.FirstNameEntry.get() and self.LastNameEntry.get():
            if dataBase.Check(self.UserEntry.get(), 1):
                LabelError.config(text='This User Name alredy exists!')
            else:
                dataBase.Insert(self.UserEntry.get(), self.PasswordEntry.get(), self.FirstNameEntry.get(), self.LastNameEntry.get())
                self.User.insert(0, self.UserEntry.get())
                self.Password.insert(0, self.PasswordEntry.get())
                self.NewWin.destroy()
                LabelDone=tkinter.Label(self.Page, text='Account created', fg='green', font=('arial'))
                LabelDone.place(x=100, y=0)
        else:
            LabelError.config(text='Please fill all asks')

class CheckAdmin:
    def check(self):
        if enterPage.First:
            self.Page=tkinter.Tk()
            self.Page.geometry('300x200')
            self.Label=tkinter.Label(self.Page, text='Please enter new password', font=('arial'))
            self.Label.place(x=50, y=0)
            self.Entry=tkinter.Entry(self.Page, font=('arial'), bg='yellow')
            self.Entry.place(x=50, y=100)
            self.Button=tkinter.Button(self.Page, text='Change', font=('arial'), command=self.change)
            self.Button.place(x=110, y=150)
        else:
            mainPage = MainPage()
            mainPage.show()

    def change(self):
        if self.Entry.get():
            if self.Entry.get()=='123456':
                self.Label.config(text='Please enter another password', fg='red')
            else:
                dataBase.Change('admin', self.Entry.get(), 1)
                self.Page.destroy()
                mainPage = MainPage()
                mainPage.show()
        else:
            self.Label.config(text='Please enter somthing', fg='red')

class MainPage:
    def __init__(self):
        self.Page=tkinter.Tk()
        self.Page.geometry('500x600')

    def show(self):
        list=dataBase.Show(enterPage.UserName)
        label=tkinter.Label(self.Page, text=f"User name :{list[0]}\nFirst name :{list[2]}\nLast name :{list[3]}\nGames :{list[4]}\nWins :{list[5]}", font=('arial'))
        label.pack()
        button_change=tkinter.Button(self.Page, text='change', width=10, height=5, command=self.change)
        button_change.pack()
        label2=tkinter.Label(self.Page, text='please enter size of table:', font=('arial'))
        label2.pack()
        self.size=tkinter.Entry(self.Page, width=2, font=('arial'))
        self.size.pack()
        label3=tkinter.Label(self.Page, text='choose your enemy!', font=('arial'))
        label3.pack()
        Users=dataBase.Show_Users()
        Enemy=[]
        for i in range(len(Users)):
            if Users[i][0] != enterPage.UserName:
                Enemy.append(Users[i][0])
        self.enemy=ttk.Combobox(self.Page, values=Enemy, font=('arial'))
        self.enemy.set(Enemy[0])
        self.enemy.pack()
        button_play=tkinter.Button(self.Page, text='Play', width=10, height=5, command=self.play)
        button_play.pack()
        self.Page.mainloop()

    def play(self):
        if self.size.get():
            self.player1=enterPage.UserName
            self.player2=self.enemy.get()
            self.colors=['red', 'blue']
            self.points=[0, 0]
            self.who=random.randint(0, 1)
            self.n = int(self.size.get())
            self.table=numpy.zeros((self.n, self.n))
            self.Page.destroy()
            self.Page=tkinter.Tk()
            self.W=self.Page.winfo_screenwidth()
            self.H=self.Page.winfo_screenheight()
            self.Page.geometry(f'{self.W}x{self.H}')
            self.background=tkinter.Label(self.Page, bg=self.colors[self.who], width=self.W, height=self.H)
            self.background.pack()
            self.labelPoints1=tkinter.Label(self.Page, text=f"{self.player1} = {self.points[0]}", fg=self.colors[0], font=('arial'))
            self.labelPoints1.place(x=self.W//2-30, y=0)
            self.labelPoints2=tkinter.Label(self.Page, text=f"{self.player2} = {self.points[1]}", fg=self.colors[1], font=('arial'))
            self.labelPoints2.place(x=self.W//2-30, y=30)
            self.btn=[]
            for i in range(self.n):
                but = []
                for j in range(self.n):
                    but.append(tkinter.Button(self.Page,width=5, height=2, bg='white', font=('arial'), command=lambda i=i, j=j : self.click(i, j)))
                    but[j].place(x=i * 62 + ((self.W-60*self.n)//2), y=j * 62+60)
                self.btn.append(but)

    def click(self, i, j):
        if self.table[j][i] == 0:
            S=tkinter.Button(self.Page, width=2, height=2, font=('arial'), text='S')
            O=tkinter.Button(self.Page, width=2, height=2, font=('arial'), text='O')
            S.config(command=lambda i=i, j=j, S=S, O=O: self.choose(i, j, 1, S, O))
            O.config(command=lambda i=i, j=j, S=S, O=O: self.choose(i, j, 2, S, O))
            S.place(x = i * 62 + ((self.W-60*self.n)/2), y=j * 62 + 60)
            O.place(x = i * 62 + ((self.W-60*self.n)/2) + 32, y=j * 62 + 60)

    def choose(self, i, j, k, S, O):
        S.destroy()
        O.destroy()
        if k==1:
            self.table[j][i]=1
            self.btn[i][j].config(text='S')
        else:
            self.table[j][i]=2
            self.btn[i][j].config(text='O')
        self.btn[i][j].config(fg=self.colors[self.who])
        if not self.check(i, j):
            self.who=abs(self.who-1)
        if self.check2():
            self.finish()
        self.background.config(bg=self.colors[self.who])
        self.labelPoints1.config(text=f"{self.player1} = {self.points[0]}")
        self.labelPoints2.config(text=f"{self.player2} = {self.points[1]}")

    def check(self, i, j):
        pygame.mixer.music.load('tada.wav')
        if self.table[j][i] == 1:
            if i >= 2 and self.table[j][i - 1] == 2 and self.table[j][i - 2] == 1:
                pygame.mixer.music.play()
                self.btn[i][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i - 1][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i - 2][j].config(bg=self.colors[self.who], fg='black')
                return True
            elif i <= self.n - 3 and self.table[j][i + 1] == 2 and self.table[j][i + 2] == 1:
                pygame.mixer.music.play()
                self.points[self.who] += 1
                self.btn[i][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i + 1][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i + 2][j].config(bg=self.colors[self.who], fg='black')
                return True
            elif j >= 2 and self.table[j - 1][i] == 2 and self.table[j - 2][i] == 1:
                pygame.mixer.music.play()
                self.points[self.who] += 1
                self.btn[i][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i][j - 1].config(bg=self.colors[self.who], fg='black')
                self.btn[i][j - 2].config(bg=self.colors[self.who], fg='black')
                return True
            elif j <= self.n - 3 and self.table[j + 1][i] == 2 and self.table[j + 2][i] == 1:
                pygame.mixer.music.play()
                self.points[self.who] += 1
                self.btn[i][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i][j + 1].config(bg=self.colors[self.who], fg='black')
                self.btn[i][j + 2].config(bg=self.colors[self.who], fg='black')
                return True
            elif i >= 2 and j >= 2 and self.table[j - 1][i - 1] == 2 and self.table[j - 2][i - 2] == 1:
                pygame.mixer.music.play()
                self.points[self.who] += 1
                self.btn[i][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i - 1][j - 1].config(bg=self.colors[self.who], fg='black')
                self.btn[i - 2][j - 2].config(bg=self.colors[self.who], fg='black')
                return True
            elif i <= self.n - 3 and j <= self.n - 3 and self.table[j + 1][i + 1] == 2 and self.table[j + 2][i + 2] == 1:
                pygame.mixer.music.play()
                self.points[self.who] += 1
                self.btn[i][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i + 1][j + 1].config(bg=self.colors[self.who], fg='black')
                self.btn[i + 2][j + 2].config(bg=self.colors[self.who], fg='black')
                return True
            elif i <= self.n - 3 and j >= 2 and self.table[j - 1][i + 1] == 2 and self.table[j - 2][i + 2] == 1:
                pygame.mixer.music.play()
                self.points[self.who] += 1
                self.btn[i][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i + 1][j - 1].config(bg=self.colors[self.who], fg='black')
                self.btn[i + 2][j - 2].config(bg=self.colors[self.who], fg='black')
                return True
            elif i >= 2 and j <= self.n - 3 and self.table[j + 1][i - 1] == 2 and self.table[j + 2][i - 2] == 1:
                pygame.mixer.music.play()
                self.points[self.who] += 1
                self.btn[i][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i - 1][j + 1].config(bg=self.colors[self.who], fg='black')
                self.btn[i - 2][j + 2].config(bg=self.colors[self.who], fg='black')
                return True
            else:
                return False

        elif self.table[j][i] == 2:
            if j >= 1 and j <= self.n - 2 and self.table[j - 1][i] == 1 and self.table[j + 1][i] == 1:
                pygame.mixer.music.play()
                self.points[self.who] += 1
                self.btn[i][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i][j - 1].config(bg=self.colors[self.who], fg='black')
                self.btn[i][j + 1].config(bg=self.colors[self.who], fg='black')
                return True
            elif i >= 1 and i <= self.n - 2 and self.table[j][i - 1] == 1 and self.table[j][i + 1] == 1:
                pygame.mixer.music.play()
                self.points[self.who] += 1
                self.btn[i][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i - 1][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i + 1][j].config(bg=self.colors[self.who], fg='black')
                return True
            elif i >= 1 and j >= 1 and i <= self.n - 2 and j <= self.n - 2 and self.table[j - 1][i - 1] == 1 and self.table[j + 1][i + 1] == 1:
                pygame.mixer.music.play()
                self.points[self.who] += 1
                self.btn[i][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i - 1][j - 1].config(bg=self.colors[self.who], fg='black')
                self.btn[i + 1][j + 1].config(bg=self.colors[self.who], fg='black')
                return True
            elif i >= 1 and j >= 1 and i <= self.n - 2 and j <= self.n - 2 and self.table[j - 1][i + 1] == 1 and self.table[j + 1][i - 1] == 1:
                pygame.mixer.music.play()
                self.points[self.who] += 1
                self.btn[i][j].config(bg=self.colors[self.who], fg='black')
                self.btn[i - 1][j + 1].config(bg=self.colors[self.who], fg='black')
                self.btn[i + 1][j - 1].config(bg=self.colors[self.who], fg='black')
                return True
            else:
                return False
    def check2(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.table[i][j]==0:
                    return False
        return True

    def finish(self):
        winner=""
        if self.points[0] > self.points[1]:
            winner=self.player1
        elif self.points[0] == self.points[1]:
            winner='nobody'
        else:
            winner=self.player2
        messagebox.showinfo(message=f"{winner} win the game")

        self.Page.destroy()
        enterPage.__init__()
        enterPage.show()

    def change(self):
        self.newWin = tkinter.Toplevel()
        self.newWin.geometry('500x300')
        if enterPage.UserName == 'admin':
            List=dataBase.Show_Users()
            for i in range(len(List)):
                List[i]=List[i][0]
            self.selectUser=ttk.Combobox(self.newWin, values=List, font=('arial'))
            self.selectUser.set(List[0])
            self.selectUser.place(x=150, y=0)
            selectLabel=tkinter.Label(self.newWin, text='User names:', font=('arial'))
            selectLabel.place(x=0, y=0)
        self.newPassword=tkinter.Entry(self.newWin, font=('arial'))
        self.newPassword.place(x=150, y=40)
        passwordLabel=tkinter.Label(self.newWin, text='New password:', font=('arial'))
        passwordLabel.place(x=0, y=40)
        self.newFirstName=tkinter.Entry(self.newWin, font=('arial'))
        self.newFirstName.place(x=150, y=80)
        newFirstNameLabel=tkinter.Label(self.newWin, text='New first name:', font=('arial'))
        newFirstNameLabel.place(x=0, y=80)
        self.newLastName=tkinter.Entry(self.newWin, font=('arial'))
        self.newLastName.place(x=150, y=120)
        newLastNameLabel=tkinter.Label(self.newWin, text='New last name:', font=('arial'))
        newLastNameLabel.place(x=0, y=120)
        button=tkinter.Button(self.newWin, text='ok', command=self.change_ok, font=('arial'))
        button.place(x=150, y=160)

    def change_ok(self):
        if enterPage.UserName=='admin':
            self.UserName=self.selectUser.get()
        else:
            self.UserName=enterPage.UserName
        if self.newPassword.get():
            dataBase.Change(self.UserName, self.newPassword.get(), 1)
        if self.newFirstName.get():
            dataBase.Change(self.UserName, self.newFirstName.get(), 2)
        if self.newLastName.get():
            dataBase.Change(self.UserName, self.newLastName.get(), 3)
        self.newWin.destroy()


dataBase=DataBase()
enterPage=EnterPage()
enterPage.show()