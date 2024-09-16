from flask import Flask, request
from parser import getNewsText, getNewsDict 
import json

app = Flask(__name__)



def selectNews(userRequest : list, newsTitles : list) -> str:
    for newsTitle in newsTitles:
        if set(userRequest) & set(newsTitle.split()):
            return newsTitle
    return ""


def getNewsNumber(userRequest : list, newsTitles : list) -> int:
    pageNumberNames = [
            ['1','один','первая','первое','первую'],
            ['2','два','вторая','второе','вторую'],
            ['3','три','третья','третье','третью'],
            ['4','четыре','четвертая','четвертое','четвертую'],
            ['5','пять','пятая','пятое','пятую'],
            ['6','шесть','шестая','шестое','шестую'],
            ['7','семь','седьмая','седьмое','седьмую'],
            ['8','восемь','восьмая','восьмое','восьмую'],
            ['9','девять','девятая','девятое','девятую'],
            ['10','десять','десятая','десятое','десятую']
    ]

    for i in range(10):
        if set(userRequest) & set(pageNumberNames[i]):
            return i
    return -1


@app.route("/", methods=["POST"])
def index():
    newsList = list(getNewsDict().keys())[:10]
    unswertext = ""
    userRequestTokens = request.json["request"]["nlu"]["tokens"]
    userCommand = request.json["request"]["command"]
    newSession = request.json["session"]["new"]
    if newSession:
        unswertext = "Новости на сегодня:\n"
        for news in newsList:
            unswertext += f"{news}\n"
    else:
        print(userRequestTokens)
        print(userCommand)
        if "список новостей" in userCommand:
            unswertext = "Новости на сегодня:\n"
            for news in newsList:
                unswertext += f"{news}\n"
        elif selectNews(userRequestTokens, newsList) != "":
            print(selectNews(userRequestTokens, newsList))
            unswertext = getNewsText(getNewsDict()[selectNews(userRequestTokens, newsList)])
        elif "номер" in userCommand or "расскажи" in userCommand:
            if getNewsNumber(userRequestTokens, newsList) != -1:
                print(getNewsNumber(userRequestTokens, newsList))
                unswertext = getNewsText(getNewsDict()[newsList[getNewsNumber(userRequestTokens, newsList)]])
            else:
                unswertext = "Чтото пошло не так, назовите правильно номер новости"
        else:
            unswertext = "Чтото пошло не так, назовите правильно команду"


    response = {
        "version":request.json["version"],
        "session":request.json["session"],
        "response": {
            "end_session": False,
            "text": unswertext
        }
    }
    return json.dumps(response)
        
