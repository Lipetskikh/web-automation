import pyautogui
#from PIL import Image

print('Для выхода нажмите клавиши <Ctrl+C>')
try:
    while True:
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
        #im = pyautogui.screenshot('screen.png')
        #im.save(r'home\admin\screen.png')
        #im2 = Image.open('screen.png')
        #pixelColor = im2.getpixel((1888, 255))
        #positionStr += ' RGB: (' + str(pixelColor[0]).rjust(3)
        #positionStr += ', ' + str(pixelColor[1]).rjust(3)
        #positionStr += ', ' + str(pixelColor[2]).rjust(3) + ')'
        print(positionStr, end = '\n')
        for i in range(len(positionStr)):
            pyautogui.press('backspace')
         #print('\b' * len(positionStr), end = '', flush = True)
        # \b - знак +-
except KeyboardInterrupt:
    print('\nГотово')
