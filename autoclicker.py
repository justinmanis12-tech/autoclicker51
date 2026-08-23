import tkinter as tk
import threading
import time
from pynput import mouse, keyboard

running = False
delay = 0.1
button = mouse.Button.left
click_count = 0
controller = mouse.Controller()

def click_loop():
    global running, click_count
    while running:
        controller.click(button)
        click_count += 1
        label_count.config(text=f"Кликов: {click_count}")
        time.sleep(delay)

def toggle_clicker():
    global running
    running = not running
    if running:
        btn_toggle.config(text="⏹ Остановить", bg="red")
        threading.Thread(target=click_loop, daemon=True).start()
    else:
        btn_toggle.config(text="▶ Запустить", bg="green")

def set_delay(val):
    global delay
    delay = round(float(val), 2)
    label_delay.config(text=f"Задержка: {delay} сек")

def toggle_button():
    global button
    if button == mouse.Button.left:
        button = mouse.Button.right
        btn_button.config(text="Правая")
    else:
        button = mouse.Button.left
        btn_button.config(text="Левая")

def reset_counter():
    global click_count
    click_count = 0
    label_count.config(text="Кликов: 0")


root = tk.Tk()
root.title("Автокликер")
root.geometry("300x350")
root.resizable(False, False)

tk.Label(root, text="🎯 АВТОКЛИКЕР", font=("Arial", 20, "bold")).pack(pady=10)

label_count = tk.Label(root, text="Кликов: 0", font=("Arial", 14))
label_count.pack(pady=5)

label_delay = tk.Label(root, text=f"Задержка: {delay} сек", font=("Arial", 12))
label_delay.pack(pady=5)

slider = tk.Scale(root, from_=0.01, to=5.0, resolution=0.01, orient=tk.HORIZONTAL,
                  length=250, label="Задержка (сек)", command=set_delay)
slider.set(delay)
slider.pack(pady=10)

btn_toggle = tk.Button(root, text="▶ Запустить", font=("Arial", 14),
                       bg="green", fg="white", width=15, command=toggle_clicker)
btn_toggle.pack(pady=5)

btn_button = tk.Button(root, text="Левая", font=("Arial", 12),
                       width=10, command=toggle_button)
btn_button.pack(pady=5)

btn_reset = tk.Button(root, text="🔄 Сбросить счётчик", font=("Arial", 12),
                      command=reset_counter, width=15)
btn_reset.pack(pady=5)

tk.Label(root, text="F6 — вкл/выкл | ESC — выход", font=("Arial", 10), fg="gray").pack(pady=5)


def on_press(key):
    try:
        if key == keyboard.Key.f6:
            toggle_clicker()
        elif key == keyboard.Key.esc:
            global running
            running = False
            root.destroy()
    except:
        pass

keyboard.Listener(on_press=on_press, daemon=True).start()


root.mainloop()