from gpiozero import AngularServo
import time

# Conecte o servo angular à porta GPIO 17 (ou outra porta de sua escolha)
servo = AngularServo(17, min_angle=0, max_angle=180, initial_angle=0)

# Ajuste para um movimento mais rápido e suave
step = 5
delay = 0.01

try:
    while True:
        # Suavemente interpole o movimento do servo para o ângulo desejado
        servo.angle += step

        if servo.angle >= 180 or servo.angle <= 0:
            step = -step  # Inverte a direção ao atingir os limites

        time.sleep(delay)

except KeyboardInterrupt:
    pass

# Certifique-se de liberar o servo ao final do programa
servo.close()
