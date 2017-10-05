from tkinter import *
import CheckUserPassword

AuthSuccess = 0


def EnterButton():
    CheckUserPassword.connect()
    ans = CheckUserPassword.checkUser(user_text.get())
    if ans == []:
        print('Wrong Username')
        AuthSuccess = 0
    else:
        if password_text.get() != ans[0][2]:
            print('Wrong Password')
            AuthSuccess = 0

        else:
            print('Password Correct')
            AuthSuccess = 1
            window.quit()


window = Tk()
user_text = StringVar()
password_text = StringVar()


def makeGUI():
    #put exception handler in case the object is destroyed so that it is re-made.
    window.wm_title("Authentication required")

    l1 = Label(window, text="User Name")
    l1.grid(row=1, column=1)

    l2 = Label(window, text="Password")
    l2.grid(row=2, column=1)


    e1 = Entry(window, textvariable=user_text)
    e1.grid(row=1, column=2, columnspan=2)


    e2 = Entry(window, textvariable=password_text, show='*')
    e2.grid(row=2, column=2, columnspan=2)

    b1 = Button(window, text="Enter", width=12, command=EnterButton)
    b1.grid(row=3, column=2)

    b2 = Button(window, text="Exit", width=12, command=window.quit)
    b2.grid(row=3, column=3)

    window.mainloop()

# def GUImainloop():




