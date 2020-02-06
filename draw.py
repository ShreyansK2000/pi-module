import cv2

def boundingBoxes(frame, objects):
    object_num = 0
    for item in objects:
        coords = objects[object_num]['rectangle']
        x = coords['x']
        y = coords['y']
        w = coords['h']
        h = coords['w']
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
        object_num += 1

    cv2.imwrite("boxed.jpeg", frame)