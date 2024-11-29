import cv2 as cv
import numpy as np
from datetime import datetime
import math
import pygame



pygame.mixer.init()
 

pygame.mixer.music.load('alarm_sound.mp3')

alarm_triggered = False

cv.namedWindow('Clock')
cv.createTrackbar('hours', 'Clock', 12, 23 , lambda x: None)
cv.createTrackbar('minutes', 'Clock', 30 , 59 , lambda x: None)




blank = np.zeros((500, 500, 3), dtype="uint8")

while True:
   
    blank[:] = (255, 200, 200)
    
    
   
    cv.circle(blank, (250, 250), 215, (255, 255, 255), thickness=-1)

    
    current_time = datetime.now()
    second = current_time.second
    minute = current_time.minute
    hour = current_time.hour

   
    
    millisecond = current_time.microsecond // 1000
    second_angle = (second + millisecond / 1000.0) * 6  
    sec_coor = (int(250 + (190 * math.sin(second_angle * math.pi / 180))),
            int(250 - (190 * math.cos(second_angle * math.pi / 180))))

    
    minute_coor = (int(250 + (165 * math.sin(6 * minute * math.pi / 180))),
                   int(250 - (165 * math.cos(6 * minute * math.pi / 180))))
    

    hour_coor = (int(250 + (100 * math.sin(((hour * 60 + minute) * 0.5) * math.pi / 180))),
                   int(250 - (100 * math.cos(((hour * 60 + minute) * 0.5) * math.pi / 180))))


    
    cv.line(blank, (250, 250), sec_coor, (0, 0, 255), thickness=2)
    cv.line(blank, (250, 250), minute_coor, (0, 0, 0), thickness=3)
    cv.line(blank, (250, 250), hour_coor, (0, 0, 0), thickness=4)


    font = cv.FONT_HERSHEY_SIMPLEX
    for i in range(1, 13):
        angle = i * 30
        x = int(250 + 190 * math.sin(angle * math.pi / 180))
        y = int(250 - 190 * math.cos(angle * math.pi / 180))
        cv.putText(blank, str(i), (x-10, y+10), font, 1, (0, 0, 0), 2)
      

    for i in range(60):
       angle = i * 6
       x1 = int(250 + 200 * math.sin(angle * math.pi / 180))
       y1 = int(250 - 200 * math.cos(angle * math.pi / 180))
       x2 = int(250 + 210 * math.sin(angle * math.pi / 180))
       y2 = int(250 - 210 * math.cos(angle * math.pi / 180))
       thickness = 1 if i % 5 != 0 else 2
       cv.line(blank, (x1, y1), (x2, y2), (0, 0, 0), thickness)     


    time_text = current_time.strftime('%H:%M:%S')
    cv.putText(blank, time_text, (192, 290), font, 1, (0, 0, 0), 2)   


    date_text = current_time.strftime('%Y-%m-%d')
    cv.putText(blank, date_text, (192, 320), font, 0.5, (0, 0, 0), 2)


    alarm_hour = cv.getTrackbarPos('hours', 'Clock')
    alarm_minute = cv.getTrackbarPos('minutes', 'Clock')
    


    
    if hour == alarm_hour and minute == alarm_minute and not alarm_triggered:
        cv.putText(blank, "ALARM!", (150, 200), font, 2, (0, 0, 255), 3)
        pygame.mixer.music.play() 
        alarm_triggered = True  


         
    alarm_text = f"Alarm set for: {alarm_hour:02}:{alarm_minute:02}"
    cv.putText(blank, alarm_text, (120, 25), font, 0.8, (0, 0, 0), 2)
 


    cv.imshow("Clock", blank)
    
    
    if cv.waitKey(1) & 0xFF == ord('q'):  
        break

pygame.mixer.music.stop()  
cv.destroyAllWindows()