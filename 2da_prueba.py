import random

#Versión optimizada para probar diferentes combinaciones de parámetros

# Definimos función para correr una simulación con ciertos parámetros
def simular(TP1, TP2, TP3, STR, DL):
    # Variables de estado
    ST1 = ST2 = ST3 = 0

    # Variables de control
    PRECIO1 = 1196500
    PRECIO2 = PRECIO1 * 0.70
    PRECIO3 = PRECIO2 * 0.70
    factorCosto = 0.8
    factorGanancia = 0.2

    # Auxiliares
    FV = FP = 1.0
    BEN = LIQ = DES = TOT = VDT = 0
    T = 0
    VENTAS_PERDIDAS = 0

    # Tiempos de entrega ficticios
    FLL1 = FLL2 = FLL3 = 1
    DP = 0

    diasEspeciales = [5, 167, 228, 328, 359]

    while T < 3650:  # Solo 1 año para acelerar
        T += 1

        # Determinar si es día especial
        FV = 1.2 if T % 365 in diasEspeciales else 1.0
        FP = DL if T % 365 == 0 else 1.0
        if T % 365 == 0:
            FV = (0.5 * DL * DL + 1.8 * DL - 1.18) / 100

        # Reposición si llegó el pedido
        if T == FLL1:
            ST1 += TP1
            TOT += TP1
            BEN -= PRECIO1 * factorCosto
            FLL1 = 0
        if T == FLL2:
            ST2 += TP2
            TOT += TP2
            BEN -= PRECIO2 * factorCosto
            FLL2 = 0
        if T == FLL3:
            ST3 += TP3
            TOT += TP3
            BEN -= PRECIO3 * factorCosto
            FLL3 = 0

        # Ventas diarias
        VD1 = random.randint(200, 700)
        VD2 = random.randint(40, 140)
        VD3 = random.randint(8, 28)

        vendidas1 = min(ST1, VD1 * FV)
        BEN += vendidas1 * PRECIO1 * FP * factorGanancia
        VDT += vendidas1
        VENTAS_PERDIDAS += max(0, VD1 * FV - ST1)
        ST1 = max(ST1 - VD1 * FV, 0)

        vendidas2 = min(ST2, VD2 * FV)
        BEN += vendidas2 * PRECIO2 * FP * factorGanancia
        VDT += vendidas2
        VENTAS_PERDIDAS += max(0, VD2 * FV - ST2)
        ST2 = max(ST2 - VD2 * FV, 0)

        vendidas3 = min(ST3, VD3 * FV)
        BEN += vendidas3 * PRECIO3 * FP * factorGanancia
        VDT += vendidas3
        VENTAS_PERDIDAS += max(0, VD3 * FV - ST3)
        ST3 = max(ST3 - VD3 * FV, 0)

        # Si hay poco stock, pedir
        if ST1 < STR and FLL1 < T:
            DP = random.randint(2, 5)
            FLL1 = T + DP
        if ST2 < STR and FLL2 < T:
            DP = random.randint(2, 5)
            FLL2 = T + DP
        if ST3 < STR and FLL3 < T:
            DP = random.randint(2, 5)
            FLL3 = T + DP

    LIQ += VDT
    DES += ST3
    return {
        "TP1": TP1, "TP2": TP2, "TP3": TP3, "STR": STR, "DL": DL,
        "BEN": BEN, "LIQ": LIQ, "VENTAS_PERDIDAS": VENTAS_PERDIDAS
    }

# Búsqueda de mejores combinaciones
mejor_ben = {"BEN": float("-inf")}
mejor_liq = {"LIQ": float("-inf")}
menor_perdidas = {"VENTAS_PERDIDAS": float("inf")}

for TP1 in range(9000, 11001, 1000):
    for TP2 in range(3500, 4501, 500):
        for TP3 in range(400, 601, 100):
            for STR in range(400, 601, 100):
                for DL in range(40, 61, 10):
                    resultado = simular(TP1, TP2, TP3, STR, DL)

                    if resultado["BEN"] > mejor_ben["BEN"]:
                        mejor_ben = resultado.copy()
                    if resultado["LIQ"] > mejor_liq["LIQ"]:
                        mejor_liq = resultado.copy()
                    if resultado["VENTAS_PERDIDAS"] < menor_perdidas["VENTAS_PERDIDAS"]:
                        menor_perdidas = resultado.copy()

# Mostrar resultados
print("\n🟢 Mejor beneficio (BEN):")
print(mejor_ben)

print("\n🔵 Mejor liquidez (LIQ):")
print(mejor_liq)

print("\n🟠 Menores ventas perdidas:")
print(menor_perdidas)
