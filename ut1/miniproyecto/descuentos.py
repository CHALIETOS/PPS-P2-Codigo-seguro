"""PPS UT1 · Mini-proyecto para la práctica de pruebas y cobertura (PPS-E2).

INCIDENCIA #17 (reportada por soporte): un cliente aplicó un cupón del 150 %
y la tienda le devolvió un precio NEGATIVO (le "regalamos" dinero).
Tu trabajo: escribir primero el TEST DE REGRESIÓN que reproduce el fallo,
verlo en rojo, corregir el código y verlo en verde.
"""
import math


def aplicar_descuento(precio: float, pct: float) -> float:
    """Aplica un descuento porcentual a un precio.

    Reglas:
      - precio >= 0 y finito (no NaN ni inf)
      - 0 <= pct <= 100 y finito (no NaN ni inf)
    Un porcentaje o precio fuera de rango debe RECHAZARSE (ValueError), no calcularse.
    """
    if not isinstance(precio, (int, float)) or not math.isfinite(precio) or precio < 0:
        raise ValueError("precio no válido")
    if not isinstance(pct, (int, float)) or not math.isfinite(pct) or not (0 <= pct <= 100):
        raise ValueError("porcentaje fuera de rango")
    return round(precio * (1 - pct / 100), 2)


def es_precio_valido(precio: float) -> bool:
    return isinstance(precio, (int, float)) and math.isfinite(precio) and precio >= 0

