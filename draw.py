import cv2

def boundingBoxes(frame, objects):
    object_num = 0
    for item in objects:
        coords = objects[object_num]['rectangle']
        x = coords['x']
        y = coords['y']
        cv2.rectangle(frame, (x,y), (x+coords['w'], y+coords['h']), (0,255,0), 2)
        object_num += 1

    filename = 'boxed.bmp'
    cv2.imwrite(filename, frame)
    
    return filename