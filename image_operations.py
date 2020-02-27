from PIL import Image
import os
import cv2

import time

should_stream = False
latest_frame = None

def start_stream():
    global should_stream
    global latest_frame
    
    should_stream = True
    
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    while should_stream:
        success, frame = camera.read()
        latest_frame = frame
        
        if latest_frame is not None:
            cv2.imshow("Live stream", latest_frame)
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # release video capture
    camera.release()
    cv2.destroyAllWindows()
    
def stop_stream():
    global should_stream
    should_stream = False

def get_frame():
    global latest_frame
    return latest_frame
    
def palettize(filename):
    limitedColours = Image.open(filename).quantize(colors=64)
    bmp_filename = 'Images/limited.bmp'
    limitedColours.save(bmp_filename)
    
    palette_filename = getPalette(bmp_filename)
        
    return bmp_filename, palette_filename

def getPalette(filename):
    palette_filename = 'Images/limited.txt'
    
    with open(filename, "rb") as f:
        f.read(54) # go to offset 54
        palette_bytes = f.read(256)
        paletteFile = open(palette_filename, 'w')
                
        byte_iter = iter(palette_bytes)
        for byte in byte_iter:
            b = byte
            g = next(byte_iter)
            r = next(byte_iter)
                
            paletteFile.write(rgb2hex(r,g,b) + '\n')
                
            # force iterator to next 0 byte
            try:
                next(byte_iter)
            except:
                break
                
    return palette_filename

def rgb2hex(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(r,g,b)

def boundingBoxes(frame, objects, translations):
    textheight = 0
    for i in range(0, len(objects)):
        coords = objects[i]['rectangle']
        x, y = coords['x'], coords['y']
        w, h = coords['w'], coords['h']
        cv2.rectangle(frame, (x,y), (x + w, y + h), (0,255,0), 2)
        textheight = y - 10 if (y + h + 10) > 480 else y + h + 10            
        cv2.putText(frame, translations[i], (x, textheight), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,25,220), 2)

    filename = 'Images/boxed.bmp'
    cv2.imwrite(filename, frame)
    
    return filename