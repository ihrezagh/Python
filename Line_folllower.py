from djitellopy import tello 
import cv2 as cv
import numpy as np



drone=tello.Tello()
drone.connect()
print(drone.get_battery())


drone.streamon()
drone.takeoff()


#cap = cv.VideoCapture(0)
hsv_values = [0,0,0,179,255,170]
sensors = 3
threshold = 0.2
width , height = 480 , 360 
senstivity = 3 #if number is high , less senitive

weights = [-25, -15 ,0 ,15 ,25]
forward_speed = 15 
curve = 0

def thresholding(img) :
    hsv = cv.cvtColor(img , cv.COLOR_BGR2HSV)
    lower = np.array([hsv_values[0] , hsv_values[1] , hsv_values[2]])
    upper = np.array([hsv_values[3] ,hsv_values[4] , hsv_values[5]])
    mask = cv.inRange(hsv , lower , upper)
    return mask


def get_contours(image_threshold , img) :
    contours , hieracrhy = cv.findContours(image_threshold , cv.RETR_EXTERNAL , cv.CHAIN_APPROX_NONE)
    if len(contours) != 0 :

        biggest = max(contours , key = cv.contourArea)
        x , y , w , h = cv.boundingRect(biggest)
        cx = x + w // 2
        cy = y + h // 2
        cv.drawContours(img , biggest , -1 , (255 , 0 , 255) , 7)
        cv.circle(img , (cx , cy) , 10 , (0 , 255 , 0) , cv.FILLED)

    return cx

def get_sensor_output(top_threshold , sensors) :
    imgs = np.hsplit(top_threshold , sensors)
    total_pixels = ( img.shape[1] // sensors ) * img.shape[0]
    sensor_value = []
    for x , im in enumerate(imgs) :
        pixel_count=cv.countNonZero(im)
        if pixel_count>threshold*total_pixels:
            sensor_value.append(1)
        cv.imshow(str(x) , im)
    print(sensor_value)
    return sensor_value
def send_commands(sensor_value,cx):
    global curve
    ##TRANSLATION

    lr = (cx - width//2)//senstivity
    lr - int(np.clip(lr , -10 , 10))
    if lr < 2 and lr > -2 :
        lr = 0
    ##Rotation
    if sensor_value == [1 , 0 , 0]:curve = weights[0]
    elif sensor_value == [1 , 1 , 0]:curve = weights[1]
    elif sensor_value == [0 , 1 , 0]:curve = weights[2]
    elif sensor_value == [0 , 1 , 1]:curve = weights[3]
    elif sensor_value == [0 , 0 , 1]:curve = weights[4]
    
    
    elif sensor_value == [0 , 0 , 0]:curve = weights[2]
    elif sensor_value == [1 , 1 , 1]:curve = weights[2]
    elif sensor_value == [1 , 0 , 1]:curve = weights[2]

    drone.send_rc_control(lr,30,0,curve)

try:
    while True :
        #_,img = cap.read()
        img=drone.get_frame_read().frame
        img = cv.resize(img , (width , height))
        img = cv.flip(img , 0)
        image_threshold = thresholding(img)
        h, w, channels = img.shape
        half2 = h//2
        top = img[:half2, :]
        top_threshold = image_threshold[:half2, :]
        cx = get_contours(top_threshold , top) #For Translation 
        sensor_value = get_sensor_output(top_threshold , sensors)
        send_commands(sensor_value,cx)
        #bottom = img[half2:, :]
        cv.imshow("Output" , top)
        cv.imshow("Path" , top_threshold)
        if cv.waitKey(1) & 0xFF == ord("q") :
            break
except KeyboardInterrupt:
    drone.land()
    exit(1)

finally:
    cv.destroyAllWindows()
    drone.land()

    print("alnded")



