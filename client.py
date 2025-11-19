import customtkinter as ctk
import socket
import threading
import datetime
from PIL import Image,ImageFilter
import tkinter.messagebox as messagebox

# ---------------- GLOBAL VARIABLES ----------------
client = None
USERNAME = None
root = ctk.CTk()
root.withdraw()   

# ---------------- RECEIVE MESSAGES ----------------
def receive_messages(scrolls):
    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                break

            try:
                sender, text = data.split("::", 1)
            except:
                sender = "Friend"
                text = data

            now = datetime.datetime.now().strftime("%I:%M %p")

            bubble = ctk.CTkFrame(scrolls, fg_color="#3B3B3B", corner_radius=12)
            bubble.pack(anchor="w", pady=5, padx=10)

            ctk.CTkLabel(bubble, text=sender, text_color="white", font=("Arial", 10, "bold"))\
                .pack(anchor="nw", padx=(8,70), pady=(2, 0))

            ctk.CTkLabel(bubble, text=text, text_color="white", font=("Arial", 13), wraplength=230)\
                .pack(anchor="w", padx=(8,70))

            ctk.CTkLabel(bubble, text=now, text_color="#AAAAAA", font=("Arial", 9))\
                .place(relx=1.0, rely=1.0, x=-8, y=-3, anchor="se")
            bubble.lift()
            scrolls._parent_canvas.yview_moveto(1)
        except:
            break

# ---------------- SEND MESSAGE ----------------
def send_message(entry, scrolls):
    message = entry.get("0.0", "end").strip()
    if message == "":
        return

    client.send(f"{USERNAME}::{message}".encode())

    now = datetime.datetime.now().strftime("%I:%M %p")

    bubble = ctk.CTkFrame(scrolls, fg_color="#014F7C", corner_radius=12)
    bubble.pack(anchor="e", pady=5, padx=10)

    ctk.CTkLabel(bubble, text=message, text_color="white", font=("Arial", 14), wraplength=230)\
        .pack(anchor="w", padx=(8,70), pady=(5,5))

    ctk.CTkLabel(bubble, text=now, text_color="#AAAAAA", font=("Arial", 9))\
        .place(relx=1.0, rely=1.0, x=-8, y=-3, anchor="se")


    entry.delete("0.0", "end")
    scrolls._parent_canvas.yview_moveto(1)

# ---------------- OPEN CHAT WINDOW ----------------
def open_chat(username):
    global USERNAME, client
    USERNAME = username

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect(("13.49.238.62", 5000))
    except Exception as e:
        messagebox.showerror("Connection Error",
                             f"Cannot connect to the server.\nPlease make sure the server is running.\n\nError: {e}")
        return
    chat = ctk.CTkToplevel(root)
    chat.geometry("400x600")
    chat.title(f"ChatMe - {USERNAME}")

   

    # ---- TITLE----
    title_label = ctk.CTkLabel(chat, 
                               text=f"Welcome, {USERNAME}",
                               font=("Arial", 22, "bold")
                               )
    title_label.pack(pady=10)
    title_label.lift() 

    # ---- CHAT AREA ----
    scrolls = ctk.CTkScrollableFrame(chat, width=380, 
                                     height=450,
                                     fg_color="#1A1A1A",
                                     label_fg_color="transparent"
                                     )
    scrolls.pack(pady=(5, 0))
    scrolls.lift()

    frame = ctk.CTkFrame(chat)
    frame.pack(pady=5)
    frame.lift()

    entry = ctk.CTkTextbox(frame, width=300, height=50,
                           corner_radius=5, font=("Arial", 14),
                           border_color="#2B7AFA", border_width=1)
    entry.pack(side="left")

    send_button = ctk.CTkButton(
        frame,
        text="Send",
        width=70,
        height=50,
        corner_radius=5,
        font=("Arial", 14),
        command=lambda: send_message(entry, scrolls)
    )
    send_button.pack(side="right", padx=5)

    send_button.lift()
    entry.lift()

    # ---- START RECEIVE THREAD ----
    threading.Thread(target=receive_messages, args=(scrolls,), daemon=True).start()
# ---------------- LOGIN WINDOW ----------------
login = ctk.CTkToplevel(root)
login.geometry("400x600")
login.title("Login")
bg = ctk.CTkImage(Image.open("Chat-App/resources/background.png"), size=(400, 400))

background_label = ctk.CTkLabel(login, image=bg, text="")
background_label.place(x=0, y=0, relwidth=1, relheight=0.8)

ctk.CTkLabel(login, text="ChatMe", font=("Verdana", 32,"bold")).pack(pady=10)
username_entry = ctk.CTkEntry(login, width=300,height=40, font=("Arial", 14),corner_radius=10,placeholder_text="Enter your User name...",border_color="#0044C2",border_width=2)
ctk.CTkLabel(login, text="User Name : ", font=("Arial", 16)).pack(pady=(380,0),padx=(50,250))
username_entry.pack(pady=(10,0))

def login_action():
    name = username_entry.get().strip()
    if name != "":
        login.withdraw()
        open_chat(name)

ctk.CTkButton(login, text="Join Chat", width=300, height=40,corner_radius=10, command=login_action).pack(pady=15)

root.mainloop()


