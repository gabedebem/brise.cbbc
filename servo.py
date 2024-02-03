import RPi.GPIO as GPIO
from pony import orm
import time
import config
import servo

servoPIN = 12
SLEEP = 0.05
STEP = 0.1
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)
servo = GPIO.PWM(servoPIN, 50)  # GPIO 12 for PWM with 50Hz
servo.start(0)

@orm.db_session
def girar_angulo(brise) -> None:
    # Ajuste posicao inicial (60)
    angle = brise.teta + 60
    try:
        # Rotacao de 180* variando de 2 e 12 => 2 + ((angulo)/19)
        pwm = 2 + (angle / 19)
        brise.pwm_servo = brise.pwm_servo or 4 # Posicao inicial
        passo = STEP if (pwm > brise.pwm_servo) else -STEP
        # print(f'pwm_servo={brise.pwm_servo}; pwm={pwm};')
        for i in range(int(brise.pwm_servo*100), int(pwm*100), int(passo*100)):
            servo.ChangeDutyCycle(i/100)
            # print(f'passo={i/100}')
            time.sleep(SLEEP)
        # Atualiza PWM atual
        brise.pwm_servo = pwm
    finally:
        time.sleep(SLEEP)
        servo.ChangeDutyCycle(0) # Para o servo


def girar_angulo_teste(teta: float) -> None:
    # Ajuste posicao inicial (50)?
    angle = teta + 50
    # Equacao de ajuste entre angulo do motor e das aletas
    angle = (angle - 43.98) / 21.99
    try:
        # Rotacao de 180* variando de 2 e 12 => 2 + ((angulo)/19)
        pwm = 2 + (angle / 19)
        passo = STEP if (pwm > config.pwm_servo) else -STEP
        # print(f'pwm_servo={pwm_servo}; pwm={pwm};')
        for i in range(int(config.pwm_servo*100), int(pwm*100), int(passo*100)):
            servo.ChangeDutyCycle(i/100)
            # print(f'passo={i/100}')
            time.sleep(SLEEP)
        # Atualiza PWM atual
        config.pwm_servo = pwm
    finally:
        time.sleep(SLEEP)
        servo.ChangeDutyCycle(0) # Para o servo