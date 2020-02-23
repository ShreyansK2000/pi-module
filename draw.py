import cv2

def boundingBoxes(frame, objects, translations):
    textheight = 0
    for i in range(0, len(objects)):
        coords = objects[i]['rectangle']
        x, y = coords['x'], coords['y']
        w, h = coords['w'], coords['h']
        cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 2)
        textheight = y - 10 if (y + h + 10) > 480 else y + h + 10            
        cv2.putText(frame, translations[i], (x, textheight), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,25,220), 2)

    filename = 'boxed.bmp'
    cv2.imwrite(filename, frame)
    
    return filename