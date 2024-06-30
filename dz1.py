#!/usr/bin/env python
# coding: utf-8

# In[13]:


#подключаем нужные библиотеки:
import requests #подключила биб-ку для работы с post/get запросами к сайту 
import pandas as pd #подключили биб-ку для работы с фреймом данных
import numpy as np #подключили биб-ку для работы с массивом
from bs4 import BeautifulSoup #подключили биб-ку супа
from datetime import datetime #подключили биб-ку для получения системной даты и времени (запишется в название выходного файла)


# In[14]:


user_url = "https://otus.ru/"
try:
    user_url = input("Введите адрес сайта: ") #запрашиваем у польз-ля адрес сайта
except:
    user_url = "https://otus.ru/" #по умолчанию обращаемся к сайту Отуса


# In[17]:


def get_hyp_array(a_user_url):
    response = requests.get(a_user_url) #обратились к сайту
    #print(response) #поверили - работает ли сайт - если 200 - то ответ стабильный, 404 - нет доступа
    soup = BeautifulSoup(response.content, "html.parser") #взяли страничку с сайта и подключили к ней метод парсера- получили объект суп
    ar = np.array #завели массив
    for a in soup.find_all('a', href=True): #нашли все теги (итератор цикла a, тег поиска - a) с ссылками href
        if a['href'].startswith("http"): #выбрали из этих ссылок только ссылки на др сайты (были еще ссылки на странички этого же, "парсируемого" сайта)
            ar = np.append(ar, a['href']) #добавили в массив
    return ar

try:
    head_array = get_hyp_array(user_url)
except:
    user_url = "https://otus.ru/"
    print("Ссылки <a href> по введенному адресу не найдены. Поиск произведется на сайте {f}".format(f = user_url))
    head_array = get_hyp_array(user_url)

if len(head_array) > 0:
    print("Список найденных URL для сайта {f}: ".format(f = user_url))
    for i in range(len(head_array)):
        print(head_array[i]) #выводим первичный список ссылок, п.3 дз1

    #выводим список ссылок для каждой из первичного списка:

    print("Произведем парсинг каждого найденного сайта в первичной выборке на наличие ссылок.")

    #запрашиваем, куда выводить рез-ты:
    i = 0
    choice = 2
    while i <= 2:
        try:
            choice = int(input("Выводить результаты на экран (1) или в файл (2): "))
            if choice in (1,2):
                break
            else:
                if i < 2:
                    print("Для ввода доступны клавиши 1 или 2, повторите попытку.")
                else:
                    print("Выбор не сделан, по умолчанию результат выведется в файл")
                    choice = 2
                    break
            i += 1
        except:
            if i < 2:
                print("Для ввода доступны клавиши 1 или 2, повторите попытку.")
            else:
                print("Выбор не сделан, по умолчанию результат выведется в файл")
                choice = 2
                break
            i += 1

    #выводим рез-ты:
    if choice == 2: #в случае, если выбрали сохранение результатов в файл
        current_datetime = str(datetime.now()).replace(":","-").replace(".","-")
        filename = "hyperlinks_dz1" + "_" + current_datetime + ".csv" #имя выходного файла
    
    for i in range(len(head_array)):
        try:
            second_array = [] #обнуляем массив
            second_array = get_hyp_array(head_array[i])
            if choice == 1: #выводим список сайтов в консоль
                print("Список найденных URL для сайта {f}: ".format(f = head_array[i]))
                try:
                    if len(second_array) > 0:
                        for j in range(len(second_array)):
                            print(second_array[j])
                except:
                    print("   На сайте {f} отсутствуют ссылки на другие сайты! ".format(f = head_array[i]))
            elif choice == 2: #вывели список сайтов в файл
                try:
                    if len(second_array) > 0:
                        df1 = pd.DataFrame({"hyperlinks": "Список найденных URL для сайта {f}: ".format(f = head_array[i])}, index = [0])
                        df2 = pd.DataFrame({"hyperlinks": second_array}) #переписали из массива в датафрейм
                        df = pd.concat([df1, df2]) #соединили: в конец датафрейм1 добавили основной блок с ссылками для текущего сайта - датафрейм 2
                        df.to_csv(filename, mode = 'a', index = False) #загнали рез-ты в файл, через добавление в конец файла
                except:
                    df1 = pd.DataFrame({"hyperlinks": "Список найденных URL для сайта {f}: ".format(f = head_array[i])}, index = [0])     
                    df2 = pd.DataFrame({"hyperlinks": "   На сайте {f} отсутствуют ссылки на другие сайты! ".format(f = head_array[i])}, index = [0])
                    df = pd.concat([df1, df2]) #соединили: в конец датафрейм1 добавили основной блок с ссылками для текущего сайта - датафрейм 2
                    df.to_csv(filename, mode = 'a', index = False) #загнали рез-ты в файл, через добавление в конец файла
        except:
            continue
    print("Выгрузка данных завершена!")
else:
    print("На сайте {f} отсутствуют ссылки на другие сайты!".format(f = user_url))

