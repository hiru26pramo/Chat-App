
import customtkinter as ctk
import socket
import threading

# ---------------- SOCKET SETUP ----------------
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5000))   # same server IP + PORT


# ---------------- RECEIVE MESSAGES ----------------
def receive_messages():
    while True:
        try:
            data = client.recv(1024).decode()
            msg_label = ctk.CTkLabel(scrolls, text="Friend: " + data, anchor="w")
            msg_label.pack(anchor="w", padx=10, pady=2)
        except:
            break


threading.Thread(target=receive_messages, daemon=True).start()


# ---------------- GUI SETUP ----------------
ctk.set_appearance_mode("dark")

root = ctk.CTk()
root.title("ChatMe")
root.geometry("400x600")

Label = ctk.CTkLabel(root, text="ChatMe", font=ctk.CTkFont(size=24, weight="bold"))
Label.pack(pady=10)

scrolls = ctk.CTkScrollableFrame(root, width=380, height=450)
scrolls.pack(pady=(10, 0))

frame = ctk.CTkFrame(root)
frame.pack()

entry = ctk.CTkEntry(
    frame,
    width=300,
    height=50,
    placeholder_text="Type a Message",
    border_width=1,
    border_color="blue",
    corner_radius=0,
    font=("Arial", 14)
)
entry.pack(side="left")


# ---------------- SEND MESSAGE ----------------
def send_message():
    message = entry.get().strip()
    if message == "":
        return

    client.send(message.encode())

    my_msg = ctk.CTkLabel(scrolls, text="You: " + message, anchor="w")
    my_msg.pack(anchor="e", padx=10, pady=2)

    entry.delete(0, 'end')


send_button = ctk.CTkButton(
    frame,
    text="Send",
    width=80,
    height=50,
    corner_radius=0,
    font=("Arial", 14),
    command=send_message
)
send_button.pack(side="right")


root.mainloop()

