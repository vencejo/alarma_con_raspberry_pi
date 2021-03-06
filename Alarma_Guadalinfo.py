# *******************************************************************************************************
# Alarma_Guadalinfo.py
# Este programa mediante un sensor de movimientos detecta a todo aquel que entre al salon de Guadalinfo, 
# le hace una foto, lo avisa con un mensaje sonoro y cuelga la foto en la cuenta de twitter de @raspbebot
# 
# ********************************************************************************************************

import RPi.GPIO as GPIO
import time
import os
from twython import Twython

# define los pines que son de entrada y salida 
GPIO.setmode(GPIO.BOARD)
GPIO.setup (11, GPIO.IN)
GPIO.setup (12, GPIO.OUT)
GPIO.setup (13, GPIO.IN)
GPIO.setup (15, GPIO.OUT)

# Datos de la cuenta de twitter de @raspbebot
CONSUMER_KEY = 'y65gX1XzZ4fmeGJBbbQ'
CONSUMER_SECRET = 'GWxr1Vqg7zFW2oTR5N1CN0ZPw1wOy1VSaOXczklzis'
ACCESS_KEY = '1635231295-upESx6zFjY0oVRjre9mBP3Hp6OA0krhEKWdD3a6'
ACCESS_SECRET = 'cFxHzCtlCSNmpnnQEBxAn6PXMDFcLR61J8vyKmrpmU'

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET) #se accede a twitter

def zumba(tiempo):
  p=GPIO.PWM(15, 500)
  p.start(5.0)
  time.sleep(tiempo)
  p.stop()
  

def desarmarAlarma():
      print "alarma desarmada"
      time.sleep(.1)
      
def parpadeo(numVeces):
      GPIO.output(12, True)
      while numVeces > 0:
            GPIO.output(12, True)
            time.sleep(.5)
            GPIO.output(12, False)
            time.sleep(.5)
            numVeces -=1

def enciendeLed():
      GPIO.output(12,False)

def apagarLed():
      GPIO.output(12,True)

def pulsadorPulsado():
      return not GPIO.input(11)

def movimientoDetectado():
      return GPIO.input(13)
         
print "Programma de alarma iniciado, pulse el boton para armarla"
while True:
      if pulsadorPulsado() :
            if movimientoDetectado(): 
                  print "no se puede armar la alarma, por favor desaloje la sala. "
                  zumba (1)
            else: 
                  active = True
                  activated = False
                  time.sleep(.1)
                  if not pulsadorPulsado():
                        print "Alarma Armada"
                        while active:
                              enciendeLed()
                              if pulsadorPulsado():
                                    desarmarAlarma()
                                    active=False
                              if movimientoDetectado():
				#que la camara haga la fotos
				os.system ("fswebcam -r 320x240 -S 5 --title 'alarm' --subtitle 'alarm' --info 'Monitor: guadarasp' --save foto_alarma.jpg") #que camara haga foto
				#la foto es mandada a la cuenta de twitter de @raspbebot
                                photo = open('foto_alarma.jpg', 'rb')
				api.update_status_with_media(status='Intruso detectectado en el #Guadalinfo de #Sorbas por la #raspberryPi', media=photo)
				print "***** ALARMA, INTUSO DETECTADO!!!!! *****"
                                #ejecuta un mensaje sonoro por el altavoz
                                os.system ("./textovoz.sh 'Atencion esta siendo detectado, vayase por donde ha venido o sufrira las consecuencias'")
                                zumba(3)
                                activated=True
                                apagarLed()
                                parpadeo(10)
                                activated=False
                                time.sleep(5)
                                activated=True
                                while activated :
				  if pulsadorPulsado():
				    time.sleep(.1)
                                    desarmarAlarma()
                                    active=False
                                    activated=False
                                               
      else:
            apagarLed()
            
      
                                                   
                                    
  
