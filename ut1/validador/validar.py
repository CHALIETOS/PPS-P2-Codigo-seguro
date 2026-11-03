#!/usr/bin/env python3
"""PPS UT1 · Validador de nombre de usuario — versión Python (INTERPRETADO).

Ejercicio PPS-E1: localiza el PUNTO DE ENTRADA, el SINK (o sinks) y la VALIDACIÓN,
y señala DÓNDE PUEDE FALLAR este modelo de ejecución.

Pista: en un lenguaje interpretado, el código fuente viaja al servidor y hay
construcciones que ejecutan cadenas como si fueran código.
"""
import os
import sqlite3


def validar_nombre(nombre: str) -> bool:
    return 0 < len(nombre) <= 32


def buscar_usuario(nombre: str):
    if not validar_nombre(nombre):
        raise ValueError("nombre no válido")

    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE usuarios (nombre TEXT)")
    consulta = "SELECT * FROM usuarios WHERE nombre = '" + nombre + "'"
    con.execute(consulta)

    os.system("logger acceso de " + nombre)

    regla = "len('" + nombre + "') > 0"
    return eval(regla)


if __name__ == "__main__":
    import sys
    print(buscar_usuario(sys.argv[1] if len(sys.argv) > 1 else "ana"))
