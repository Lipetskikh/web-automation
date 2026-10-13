import pyautogui
from PIL import Image
import cv2
import pytesseract
import time
import csv
import pyperclip
import numpy as np
from Levenshtein import distance

print('Для выхода нажмите клавиши <Ctrl+C>')

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

try:
    def paste(text: str):
        buffer = pyperclip.paste()
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        #pyperclip.copy(buffer)

    def ocr_from_image(image_path):
        #print('opencv start')
        image = cv2.imread(image_path) # загрузка изображения
        image = cv2.resize(image, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC) # увеличение изображения
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #конвертация в оттенки серого
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1] # пороговая обработка (бинаризация)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)) # улучшение резкости
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 1)
        custom_config = r'--oem 3 --psm 11' # распознавание текста
        text = pytesseract.image_to_string(opening, config = custom_config, lang = 'rus') # rus+eng
        text = text.strip('\n')
        return text

    def is_goto_button_visible():
        try:
            button_region = pyautogui.screenshot(region = (1769, 234, 140, 50)) # обл с кнопой
            button_region.save('button_area.png')
            
            button_img = cv2.cvtColor(np.array(button_region), cv2.COLOR_RGB2BGR) # в np array для обработки
            template = cv2.imread('goto_room.PNG')
            # масштабируем шаблон, если нужно
            # template = cv2.resize(template, None, fx=0.9, fy=0.9)
        
            res = cv2.matchTemplate(button_img, template, cv2.TM_CCOEFF_NORMED) # поиск шаблона
            threshold = 0.8  # порог совпадения (можно регулировать)
            loc = np.where(res >= threshold)
            return len(loc[0]) > 0 # True, если найдены совпадения

        except Exception as e:
            print(f'Ошибка при поиске кнопки: {e}')
            return False

    def fuzzy_startswith(text, prefix, max_errors):
        text_part = text[:len(prefix)]
        return distance(text_part.lower(), prefix.lower()) <= max_errors
    
    resultFile = open('resultRoomsGoTo.csv', 'w', newline = '', encoding = 'utf-8') # переписать на ввод названия файла с клавы!!!
    resultWriter = csv.writer(resultFile, delimiter = ';')
    resultWriter.writerow(['Помещение', 'Есть ли переход', 'Распознанный текст'])
    #print('ok')

    with open('inputRooms.txt', encoding = 'utf-8') as inputFile: #magic outside Hogwards # encoding = 'utf-8'
        rooms = [room.strip('\n') for room in inputFile]

    max_errors = 1 # максимальное кол-во опечаток
    
    for i in range(len(rooms)):
        #print(type(rooms[i]))
        #print(rooms[i])
        #pyautogui.click(pyautogui.locateCenterOnScreen('logo.PNG'))
        #time.sleep(0.2)
        #pyautogui.click(1256, 203)
        #time.sleep(0.2)
        pyautogui.click(1886, 201) #in order to cancel previos finding #1886 1571
        time.sleep(0.2)
        #time.sleep(5)
        pyautogui.click(pyautogui.locateCenterOnScreen('find_room.PNG')) #to set cursor
        time.sleep(1)
        #pyautogui.write(str(rooms[i]))
        paste(rooms[i])
        time.sleep(2)
        pyautogui.press('enter')
        time.sleep(9)
        screen = pyautogui.screenshot(region = (1358, 219, 410, 82))
        screen.save('text_screen.png')
        recog_text = ocr_from_image('text_screen.png')
        #text = pytesseract.image_to_string(screen, lang = 'rus+eng')
        recog_text = recog_text.lstrip()
        rooms[i] = rooms[i].lstrip()

        # добавить скрин области с кнопой по аналогии скрина с текстом для распознавания
        #reg = pyautogui.screenshot(region = (1358, 139, 559, 163))
        #reg.save('info_region.png')
        
        print(recog_text)
        if (is_goto_button_visible() and fuzzy_startswith(recog_text, rooms[i], max_errors)):
            resultWriter.writerow([rooms[i], 'есть', recog_text])
            print(i, rooms[i], 'yes')
        else:
            resultWriter.writerow([rooms[i], 'нет', recog_text])
            print(i, rooms[i], 'no')
        time.sleep(0.25)

    inputFile.close()
    resultFile.close()
    print('\nГотово')
    
except KeyboardInterrupt:
    inputFile.close()
    resultFile.close()
    print('\nГотово')
