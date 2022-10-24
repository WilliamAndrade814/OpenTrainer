from time import sleep
import PySimpleGUI as sg
import exercicios as ex


theme = sg.theme('reddit')

layout = [
    [sg.Image(filename='imagens/logo.png')],
    [sg.Text('Seja bem vindo ao Open Trainer.')],
    [sg.Text('Qual exercício gostaria de praticar?')],
    [sg.Button('Polichinelo', key='polichinelo'), sg.Button('Agachamento', key='agachamento'),
    sg.Button('Rosca Direta', key='rosca'), sg.Button('Elevação Lateral', key='elevacao')]
    ]
    
window = sg.Window('Open Trainer', layout=layout, element_justification='c')

while True:
    event, values = window.Read()
    if event == sg.WINDOW_CLOSED:
        break
    
    elif event == 'polichinelo':
        ex.polichinelos()
        
    elif event == 'agachamento':
         ex.agachamento()
                
    elif event == 'rosca':
         ex.rosca_direta()

    elif event == 'elevacao':
        ex.elevação_lateral()

