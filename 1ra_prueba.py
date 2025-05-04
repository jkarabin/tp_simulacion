import random

# variables de estado
ST1 = ST2 = ST3 = 0
VD1 = VD2 = VD3 = DP = CVL = 0
TP1 = TP2 = TP3 = STR = DL = 0

# auxiliares y resultados
T = 0
PRECIO1 = 1196500
PRECIO2 = PRECIO1 * 0.70
PRECIO3 = PRECIO2 * 0.70
FV = 1.0
FP = 1.0
BEN = LIQ = DES = TOT = VDT = 0
diasEspeciales = [5, 167, 228, 328, 359]
factorCosto = 0.8
factorGanancia = 0.2

FLL1 = FLL2 = FLL3 = 1
VENTAS_PERDIDAS = 0

def main():
    global T, FLL1, FLL2, FLL3, ST1, VD1, ST2, STR, ST3, TP1, TP2, TP3
    while T < 356 * 10:
        T += 1
        determinar_fecha_especial()
        if T == FLL1: reponer1()
        if T == FLL2: reponer2()
        if T == FLL3: reponer3()
        calcular_ventas_diarias()
        if ST1 < STR:
            if FLL1 < T: realizar_pedido1()
            if FLL2 < T: realizar_pedido2()
            if FLL3 < T: realizar_pedido3()
        if T % 365 == 0: cerrar_anio()

def determinar_fecha_especial():
    global T, diasEspeciales, FP, FV, DL
    FP = 1.0
    FV = 1.0
    for k in diasEspeciales:
        if T % 365 == k - 365:
            FV = 1.2
    if T % 365 == 0:
        FP = DL
        FV = (0.5 * DL * DL + 1.8 * DL - 1.18) / 100

def cerrar_anio():
    global LIQ, VDT, DES, ST1, ST2, ST3
    LIQ += VDT
    DES += ST3
    ST3 = ST2
    ST2 = ST1
    ST1 = 0

def realizar_pedido1():
    global DP, T, FLL1
    DP = random.randint(2, 5)
    FLL1 = T + DP

def realizar_pedido2():
    global DP, T, FLL2
    DP = random.randint(2, 5)
    FLL2 = T + DP

def realizar_pedido3():
    global DP, T, FLL3
    DP = random.randint(2, 5)
    FLL3 = T + DP

def calcular_ventas_diarias():
    global VD1, VD2, VD3, ST1, ST2, ST3, VDT, BEN, VENTAS_PERDIDAS
    VD1 = random.randint(200, 700)
    VD2 = random.randint(40, 140)
    VD3 = random.randint(8, 28)
    VDT = 0

    # Producto 1
    ventas_posibles1 = min(ST1, VD1 * FV)
    BEN += ventas_posibles1 * PRECIO1 * FP * factorGanancia
    VDT += ventas_posibles1
    VENTAS_PERDIDAS += max(0, VD1 * FV - ST1)
    ST1 = max(ST1 - VD1 * FV, 0)

    # Producto 2
    ventas_posibles2 = min(ST2, VD2 * FV)
    BEN += ventas_posibles2 * PRECIO2 * FP * factorGanancia
    VDT += ventas_posibles2
    VENTAS_PERDIDAS += max(0, VD2 * FV - ST2)
    ST2 = max(ST2 - VD2 * FV, 0)

    # Producto 3
    ventas_posibles3 = min(ST3, VD3 * FV)
    BEN += ventas_posibles3 * PRECIO3 * FP * factorGanancia
    VDT += ventas_posibles3
    VENTAS_PERDIDAS += max(0, VD3 * FV - ST3)
    ST3 = max(ST3 - VD3 * FV, 0)

def reponer1():
    global TOT, ST1, FLL1, BEN, PRECIO1
    ST1 += TP1
    TOT += TP1
    BEN -= PRECIO1 * factorCosto
    FLL1 = 0

def reponer2():
    global TOT, ST2, FLL2, BEN, PRECIO2
    ST2 += TP2
    TOT += TP2
    BEN -= PRECIO2 * factorCosto
    FLL2 = 0

def reponer3():
    global TOT, ST3, FLL3, BEN, PRECIO3
    ST3 += TP3
    TOT += TP3
    BEN -= PRECIO3 * factorCosto
    FLL3 = 0

def reiniciar_variables():
    global ST1, ST2, ST3, VD1, VD2, VD3, DP, CVL
    global T, FV, FP, BEN, LIQ, DES, TOT, VDT, FLL1, FLL2, FLL3, VENTAS_PERDIDAS
    ST1 = ST2 = ST3 = VD1 = VD2 = VD3 = DP = CVL = 0
    T = 0
    FV = FP = 1.0
    BEN = LIQ = DES = TOT = VDT = 0
    FLL1 = FLL2 = FLL3 = 1
    VENTAS_PERDIDAS = 0

def imprimir_resultados():
    print("------ Resultados ------")
    print(f"BEN total: {BEN}")
    print(f"BA (Prom. Beneficio Diario): {BEN*365/T:.2f}")
    print(f"LT (Líquido/Tot): {LIQ/TOT:.2f}")
    print(f"PLA (Prom. Liquidez Anual): {LIQ*365/T:.2f}")
    print(f"PDA (Prom. Demanda Atendida Anual): {DES*365/T:.2f}")
    print(f"Ventas perdidas: {VENTAS_PERDIDAS}")
    print(f"Stock final: ST1={ST1}, ST2={ST2}, ST3={ST3}")

peso_perdidas = 10000 # Penalización por unidad perdida

# Exploración
mejor_valor = float('-inf')
mejor_config = {}

for tp1 in range(8000, 12001, 1000):
    for tp2 in range(3000, 5001, 500):
        for tp3 in range(400, 601, 100):
            for str_ in range(300, 801, 100):
                for dl in range(30, 71, 10):
                    TP1, TP2, TP3, STR, DL = tp1, tp2, tp3, str_, dl
                    reiniciar_variables()
                    main()
                    valor_objetivo = BEN - peso_perdidas * VENTAS_PERDIDAS
                    if valor_objetivo > mejor_valor:
                        mejor_valor = valor_objetivo
                        mejor_config = {
                            "TP1": TP1, "TP2": TP2, "TP3": TP3,
                            "STR": STR, "DL": DL,
                            "BEN": BEN,
                            "VENTAS_PERDIDAS": VENTAS_PERDIDAS,
                            "VALOR_OBJETIVO": valor_objetivo
                        }

# Mostrar mejor configuración
print("---- MEJOR CONFIGURACIÓN ----")
for k, v in mejor_config.items():
    print(f"{k}: {v}")

# Ejecutar una vez más con la mejor combinación
TP1 = mejor_config["TP1"]
TP2 = mejor_config["TP2"]
TP3 = mejor_config["TP3"]
STR = mejor_config["STR"]
DL = mejor_config["DL"]

reiniciar_variables()
main()
imprimir_resultados()