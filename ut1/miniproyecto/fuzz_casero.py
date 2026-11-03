"""PPS UT1 · Fuzzing casero (sin instalar nada).

Lanza miles de entradas raras contra aplicar_descuento y avisa cuando pasa algo
que NO debería pasar:
  - ValueError            -> bien, es un rechazo esperado
  - cualquier otra cosa   -> fallo
  - un resultado absurdo  -> fallo (negativo, mayor que el precio, no es un número...)

Uso:  python3 fuzz_casero.py
"""
import math
import random

from descuentos import aplicar_descuento

RAROS = [0, -0.0, 1e-9, -1, 100, 100.0001, 1e308, -1e308,
         float("inf"), float("-inf"), float("nan")]


def valor_raro():
    if random.random() < 0.3:
        return random.choice(RAROS)
    return random.uniform(-1000, 1000)


def resultado_valido(precio, resultado):
    # ¿Qué condiciones debe cumplir SIEMPRE un precio con descuento?
    # Debe ser un número finito, no negativo y no superar el precio original (considerando redondeo a 2 decimales)
    if not math.isfinite(resultado):
        return False
    if resultado < 0:
        return False
    if resultado > max(precio, round(precio, 2)):
        return False
    return True


def main(intentos=20000):
    random.seed(2026)
    fallos = 0
    for _ in range(intentos):
        precio, pct = valor_raro(), valor_raro()
        try:
            r = aplicar_descuento(precio, pct)
        except ValueError:
            continue
        except Exception as e:
            print(f"EXCEPCIÓN {type(e).__name__}: precio={precio!r} pct={pct!r}")
            fallos += 1
            continue
        if not resultado_valido(precio, r):
            print(f"RESULTADO RARO {r!r}: precio={precio!r} pct={pct!r}")
            fallos += 1
        if fallos >= 10:
            break
    print(f"\n{fallos} fallos en {intentos} intentos")


if __name__ == "__main__":
    main()
