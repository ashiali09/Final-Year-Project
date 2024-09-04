
def text_detection1():

    import cv2
    import pytesseract
    import pyttsx3
#from .engine import Engine
    engine =pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
# Tesseract ocr Executable file location
    pytesseract.pytesseract.tesseract_cmd =  "C:\\Users\\AMIR\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe"
    engine.say('text detection')
    engine.runAndWait()     
        
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    output_txt = []
       
    while True:
            _,img = cap.read()
            # DETECTING CHARACTERS
            hImg, wImg, none1 = img.shape
            boxes = pytesseract.image_to_boxes(img)
          
            data1 = pytesseract.image_to_data(img)
            
            for z, b in enumerate(data1.splitlines()):
                if z != 0: 
                  # Converts 'data1' string into a list stored in 'b'
                 b = b.split()
                 # Checking if array contains a word
                if len(b) == 12:
                   #output_txt.append(b[11])
                   
                   # Storing values in the right variables
                   x, y = int(b[6]), int(b[7])
                   w, h = int(b[8]), int(b[9])
                  
                   cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
                   # Display detected word under each bounding box
                   cv2.putText(img, b[11], (x - 15, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 1)
                   #cv2.imshow("Result", img)
                   output_txt= b[11]
                   engine.say(output_txt)
                   engine.runAndWait()
                   print (output_txt)
            #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
            #cv2.putText(img, str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20, 230, 20), 2)
            
            
            yield img
            
            #if cv2.waitKey(1) & 0xFF==ord('q'): 
             #   cap.release()  
            
         
#detect_from_webcam() 
            cv2.destroyAllWindows() 
       