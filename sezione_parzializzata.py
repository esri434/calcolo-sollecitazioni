
import math

# Definizione delle proprietà della sezione e dei materiali
b = 30  # larghezza della sezione in cm
h = 50  # altezza della sezione in cm
d = 45  # altezza utile della sezione in cm (distanza dal bordo superiore all'asse delle armature in trazione)
cover = 3  # copriferro in cm
A_s_bottom = 20  # area dell'armatura longitudinale in intradosso in cm^2
A_s_top = 20  # area dell'armatura longitudinale in estradosso in cm^2
f_ck = 30  # resistenza caratteristica del calcestruzzo in MPa
f_yk = 500  # resistenza caratteristica dell'acciaio in MPa

# Coppie di azioni agenti (N in kN, M in kNm)
actions = [
    (1000, 50),
    (1500, 75),
    (2000, 100)
]

# Funzione per calcolare la posizione dell'asse neutro
def calculate_neutral_axis(N, M):
    a = A_s_bottom * f_yk + A_s_top * f_yk
    b = -N * 1000 - A_s_bottom * f_yk * (d - cover) - A_s_top * f_yk * cover
    c = -M * 1000000
    delta = b**2 - 4*a*c
    if delta < 0:
        raise ValueError("Delta negativo, impossibile calcolare l'asse neutro.")
    x1 = (-b + math.sqrt(delta)) / (2*a)
    x2 = (-b - math.sqrt(delta)) / (2*a)
    return max(x1, x2)

# Funzione per calcolare le sollecitazioni nel calcestruzzo e nell'acciaio
def calculate_stresses(N, M):
    x = calculate_neutral_axis(N, M)
    sigma_c = (N * 1000 - A_s_bottom * f_yk * (d - x) / d - A_s_top * f_yk * x / d) / (b * x)
    sigma_s_bottom = f_yk * (d - x) / d
    sigma_s_top = f_yk * x / d
    return sigma_c, sigma_s_bottom, sigma_s_top

# Calcolo delle sollecitazioni per ciascuna coppia di azioni
for N, M in actions:
    sigma_c, sigma_s_bottom, sigma_s_top = calculate_stresses(N, M)
    print(f"For N={{N}} kN and M={{M}} kNm:")
    print(f"Stress in concrete: {{sigma_c:.2f}} MPa")
    print(f"Stress in bottom steel: {{sigma_s_bottom:.2f}} MPa")
    print(f"Stress in top steel: {{sigma_s_top:.2f}} MPa")
    print()
