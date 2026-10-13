import pyautogui
from PIL import Image
import time
import csv
import pyperclip

print('Для выхода нажмите клавиши <Ctrl+C>')

try:
    def paste(text: str):
        buffer = pyperclip.paste()
        pyperclip.copy(text)
        pyautogui.hotkey('ctrl', 'v')
        #pyperclip.copy(buffer)
    
    resultFile = open('resultRoomsGoTo.csv', 'w', newline = '', encoding = 'utf-8')
    resultWriter = csv.writer(resultFile, delimiter = ';')
    resultWriter.writerow(['Помещение', 'Есть ли переход'])

    with open('inputRooms.txt', encoding = 'utf-8') as inputFile: #magic outside Hogwards # encoding = 'utf-8'
        rooms = [room.strip('\n') for room in inputFile]
        
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
        #text = pytesseract.image_to_string(screen, lang = 'rus+eng')
        print(text)
        if pyautogui.locateOnScreen('goto_room.PNG') != None:
            resultWriter.writerow([rooms[i], 'есть'])
            print(i, rooms[i], 'yes')
            #time.sleep(22)
            #pyautogui.click(pyautogui.locateCenterOnScreen('general_view.PNG'))
            #time.sleep(22)
        elif pyautogui.locateOnScreen('goto_room.PNG') == None:
            resultWriter.writerow([rooms[i], 'нет'])
            print(i, rooms[i], 'no')
        time.sleep(0.25)

    inputFile.close()
    resultFile.close()
    print('\nГотово')
    
except KeyboardInterrupt:
    inputFile.close()
    resultFile.close()
    print('\nГотово')
