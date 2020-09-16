import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

p1=GPIO.PWM(6, 50)
p2=GPIO.PWM(19, 50)
p3=GPIO.PWM(26, 50)
p4=GPIO.PWM(13, 50)

p1.start(7.5)
p2.start(7.5)
p3.start(7.7)
p4.start(7.1)
#6 right foot  3.5 stand inside, 7.5 //   10.1  stand outside max
#26 right leg  5.0 right turn // 7.7 stright // 11.5 max

#19 left foot 5.6 stand outside // 7.5  // 11.5 max inside max
#13 left leg 5.0 inside turn // 7.1 // 11.5 outside turn

try:
    motion2 = 0;
    while (motion2 < 2):
        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.3)
        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)

        time.sleep(0.5)

        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.23)
        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.23)
        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.23)
        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.23)
        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.23)

        #########

        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.23)
        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)

        time.sleep(0.5)

        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.23)
        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.23)
        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.23)
        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.23)
        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.23)

        motion2 = motion2 + 1




    motion1 = 0
    while(motion1 < 1):
        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.01)
        p1.ChangeDutyCycle(6)
        p2.ChangeDutyCycle(6)

        time.sleep(0.23)

        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.01)
        p1.ChangeDutyCycle(8.5)
        p2.ChangeDutyCycle(8.5)
        time.sleep(0.5)

        #######

        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.01)
        p1.ChangeDutyCycle(6)
        p2.ChangeDutyCycle(6)

        time.sleep(0.23)

        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.01)
        p1.ChangeDutyCycle(8.5)
        p2.ChangeDutyCycle(8.5)
        time.sleep(0.23)

        ######....

        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.01)
        p1.ChangeDutyCycle(6)
        p2.ChangeDutyCycle(6)

        time.sleep(0.23)

        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.01)
        p1.ChangeDutyCycle(8.5)
        p2.ChangeDutyCycle(8.5)
        time.sleep(0.23)

        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.01)
        p1.ChangeDutyCycle(6)
        p2.ChangeDutyCycle(6)

        time.sleep(0.27)

        ############################### odd partial

        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.01)
        p1.ChangeDutyCycle(8.5)
        p2.ChangeDutyCycle(8.5)

        time.sleep(0.23)

        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.01)
        p1.ChangeDutyCycle(6)
        p2.ChangeDutyCycle(6)

        time.sleep(0.5)

        #######

        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.01)
        p1.ChangeDutyCycle(8.5)
        p2.ChangeDutyCycle(8.5)

        time.sleep(0.23)

        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.01)
        p1.ChangeDutyCycle(6)
        p2.ChangeDutyCycle(6)

        time.sleep(0.23)

        ######....
        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.01)
        p1.ChangeDutyCycle(8.5)
        p2.ChangeDutyCycle(8.5)

        time.sleep(0.23)

        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.01)
        p1.ChangeDutyCycle(6)
        p2.ChangeDutyCycle(6)


        time.sleep(0.23)

        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.01)
        p1.ChangeDutyCycle(8.5)
        p2.ChangeDutyCycle(8.5)

        time.sleep(0.27)

        ####################################second part end

        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.01)
        p1.ChangeDutyCycle(6)
        p2.ChangeDutyCycle(6)

        time.sleep(0.23)

        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.01)
        p1.ChangeDutyCycle(8.5)
        p2.ChangeDutyCycle(8.5)
        time.sleep(0.5)

        #######

        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.01)
        p1.ChangeDutyCycle(6)
        p2.ChangeDutyCycle(6)

        time.sleep(0.23)

        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.01)
        p1.ChangeDutyCycle(8.5)
        p2.ChangeDutyCycle(8.5)
        time.sleep(0.23)

        ######....

        p3.ChangeDutyCycle(5.5)
        p4.ChangeDutyCycle(5.5)
        time.sleep(0.01)
        p1.ChangeDutyCycle(6)
        p2.ChangeDutyCycle(6)

        time.sleep(0.8)

        p3.ChangeDutyCycle(9)
        p4.ChangeDutyCycle(9)
        time.sleep(0.01)
        p1.ChangeDutyCycle(8.5)
        p2.ChangeDutyCycle(8.5)
        time.sleep(1)

        motion1 = motion1 + 1

    p3.ChangeDutyCycle(7.7)
    p4.ChangeDutyCycle(7.1)
    time.sleep(0.01)
    p1.ChangeDutyCycle(7.5)
    p2.ChangeDutyCycle(7.5)
    time.sleep(0.23)


except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()