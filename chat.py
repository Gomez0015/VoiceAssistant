from datetime import datetime
import random 
import time
import json
import torch
import os
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from voice_recogniton import startListening, reset
import textToSpeech
import lcd
import requests

#Get Weather API Key
api_key = "5c5d689b501f93d37bf2fe54a0192306"

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

lcd.firstmsg();

with open('intents.json', 'r') as f:
    intents = json.load(f)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]


model =  NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

lookingforcity = False
bot_name = "O.T.I.S"
print("-- Chat Start -- 'quit or shutdown' to exit")
while True:
    sentence = startListening()
    print(sentence)
    if lookingforcity == True:
        if sentence != "nothing detected":
            city = sentence.lower()
            url = "https://api.openweathermap.org/data/2.5/weather?" + "q=" + city + "&appid=" + api_key

            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                main = data['main']
                kelvin_temp = main['temp']
                K = float(kelvin_temp)
                current_temp = int(K-273.15)

                response = 'current temperature is ' + str(current_temp) + ' C'
                lcd.msg(response)
                print(f'{bot_name}: {response}elsius')
                textToSpeech.text2Speech(response + "elsius")
                lookingforcity = False
                continue
            else:
                # showing the error message
                print("Error in the HTTP request")
                lookingforcity = False
                continue
    if sentence == 'quit':
        textToSpeech.text2Speech("Shutting down")
        lcd.msg('Shutting Down...')
        print(f'{bot_name}: Shutting Down...')
        reset()
        break

    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)

    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                response = random.choice(intent["responses"])
                if response == "The current time is: ":
                    response = response + datetime.now().strftime("%H:%M:%S")
                elif response == "The current weather is: ":
                    response = "Which City are you in?"
                    lookingforcity = True

                lcd.msg(response)
                print(f'{bot_name}: {response}')
                textToSpeech.text2Speech(response)
                
    else:           
        print(f'{bot_name}: I do not understand...')
        textToSpeech.text2Speech("I do not understand")
    