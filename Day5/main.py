import time
import PySimpleGUI as sg

layout = [
    [sg.Button("OPEN"), sg.Button("NEW"), sg.Button("SAVE"), sg.Button("SAVE AS")],
    [sg.Multiline(key="text-space", size=(150, 50))],
    [sg.Button("CLOSE")]
]

# Create the window
window = sg.Window("File Editor", layout)

text = ""
current_file = ""
last_save = ""

# Create an event loop
while True:
    event, values = window.read(timeout=5)

    text = values["text-space"]
    if text != last_save:
        window.set_title("File Editor (Unsaved Changes)")
    else:
        window.set_title("File Editor")

    # End program if user closes window or
    # presses the OK button
    if event == "CLOSE" or event == sg.WIN_CLOSED:
        break
    elif event == "OPEN":
        if text != last_save:
            choice = sg.popup_ok_cancel("You have unsaved changes. Proceed and delete them?")
            if choice == "CANCEL":
                time.sleep(0.001)
                continue
        file_path = sg.popup_get_file('Select a file')
        if file_path:
            with open(file_path, "r") as f:
                text = f.read()
                current_file = file_path
                last_save = text
            window["text-space"].update(text)

    elif event == "NEW":
        if text != last_save:
            choice = sg.popup_ok_cancel("You have unsaved changes. Proceed and delete them?")
            if choice == "Cancel":
                time.sleep(0.001)
                continue
        text = ""
        current_file = ""
        last_save = ""
        window["text-space"].update(text)
    elif event == "SAVE" and current_file:
        with open(current_file, "w") as f:
            f.write(text)
            last_save = text
    elif event == "SAVE AS" or event == "SAVE":
        file_path = sg.popup_get_file('Select a file', save_as=True)
        if file_path:
            current_file = file_path
            with open(file_path, "w") as f:
                f.write(text)
                last_save = text

    time.sleep(0.001)

window.close()
