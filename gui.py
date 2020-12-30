import PySimpleGUI as sg
import voice_recogniton

mainText = "AI Assistant"
youText = "You: "
aiText = "Mary: "

# ----- Full layout -----
layout = [
    [sg.Text(mainText, key='mainText')],
    [sg.Text(youText, size=(50,3), font=("Helvetica", 25), key='youText')],
    [sg.Text(aiText, size=(50,3), font=("Helvetica", 25), key='aiText')],
    [sg.Button("CLOSE",'center',size=(10,1))]
]

# Create the window
window = sg.Window("AI Assitant", layout, finalize=True, element_justification='c')
window.size = (500, 300)
window.BackgroundColor = ""

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "CLOSE" or event == sg.WIN_CLOSED:
        break

window.close()