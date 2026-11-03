# Práctica 2 · Código seguro: del dato al fallo (Entrega)

**CIPFP Cheste · 1º CE Ciberseguridad en Entornos de las TI · Curso 2026-27**  
**Módulo:** Puesta en Producción Segura (5023)  
**Profesor:** José Picón  

---

### Datos del alumno
- **Nombre y apellidos:** Carlos (CHALIETOS)
- **Fecha:** 27/10/2026
- **URL del repositorio:** https://github.com/CHALIETOS/pps-arranque.git

---

## Respuestas a las preguntas de la entrega

### 1. ¿Cuál es el sink más peligroso de `validar.py`? ¿Por qué?

**Respuesta:**

El sink más peligroso es **`os.system("logger acceso de " + nombre)`** (seguido de cerca por `eval(regla)`).

**Justificación técnica:**
1. **Inyección directa de comandos en el Sistema Operativo (Command Injection):**  
   Al pasar la cadena sin escapar directamente a `os.system`, el intérprete invoca el shell del sistema (`/bin/sh`). Un atacante puede introducir metacaracteres de shell (como `;`, `&&`, `|`, `` ` `` o `$()`) dentro del límite de 32 caracteres (por ejemplo: `ana; id` o `ana && whoami`) para ejecutar comandos arbitrarios en la máquina anfitriona con los permisos del usuario que corre el script.
2. **Impacto frente a otros sinks:**
   - `con.execute(consulta)` permite Inyección SQL, pero en este caso la base de datos es una base SQLite temporal en memoria (`:memory:`), por lo que el impacto queda confinado a esa base de datos volátil.
   - `eval(regla)` permite Code Injection en Python, pero depende de la sintaxis válida de Python para no fallar con `SyntaxError` (como ocurrió con comillas mal emparejadas en el test).
   - Por el contrario, `os.system` interactúa directamente con el kernel y el sistema de archivos del sistema operativo, permitiendo a un atacante comprometer totalmente el host, exfiltrar credenciales o instalar puertas traseras.

---

### 2. ¿Qué cobertura tenía `descuentos.py` con el fallo dentro?

**Porcentaje de cobertura inicial:**

- **83%** en `descuentos.py` (y **100%** de las líneas ejecutables de la función `aplicar_descuento`).

**Salida del comando (`coverage report -m`):**

```text
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
descuentos.py            6      1    83%   24
test_descuentos.py      12      0   100%
--------------------------------------------------
TOTAL                   18      1    94%
```

**¿Hay algún test que se dé cuenta del fallo?:**

**No**. Todos los tests iniciales pasaban en verde (3 passed).  
Ninguno de los tests existentes comprobaba porcentajes superiores al 100% ni inferiores al 0% (como el cupón del 150% de la incidencia #17 o descuentos negativos). Esto demuestra que **una alta cobertura de código no garantiza la ausencia de vulnerabilidades o fallos de lógica de negocio**: las líneas se ejecutan, pero no se validan los casos límite ni las precondiciones.

---

### 3. ¿Qué mensaje te dio `pytest` cuando tu test fallaba?

**Salida / Traza del fallo en pytest tras implementar `test_regresion_incidencia_17`:**

```text
=================================== FAILURES ===================================
_________________________ test_regresion_incidencia_17 _________________________

    def test_regresion_incidencia_17():
>       with pytest.raises(ValueError):
             ^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE ValueError

test_descuentos.py:25: Failed
=========================== short test summary info ============================
FAILED test_descuentos.py::test_regresion_incidencia_17 - Failed: DID NOT RAISE ValueError
========================= 1 failed, 3 passed in 0.01s ==========================
```

**Explicación del fallo:**

El mensaje fue **`Failed: DID NOT RAISE ValueError`**.  
El test esperaba que `aplicar_descuento(100, 150)` lanzara una excepción de tipo `ValueError` al recibir un porcentaje superior a 100%. Como el código original no validaba el rango superior de `pct`, calculó `100 * (1 - 1.5) = -50.0` y devolvió un precio negativo en lugar de rechazarlo con la excepción esperada.

---

### 4. ¿Qué valores encontró el fuzzing que tus tests no habían probado?

**Valores anómalos detectados por el fuzzer:**

El fuzzer (`fuzz_casero.py`) detectó valores especiales de coma flotante (`float`) que no se habían contemplado:
- **`float("nan")` (Not a Number):**  
  Con `precio = nan`, la condición `if precio < 0:` devolvía `False` (cualquier comparación relacional contra `NaN` da `False` en Python), por lo que la función calculaba y devolvía `nan`. Al evaluar `resultado >= 0`, `nan >= 0` también devolvía `False`, provocando el mensaje:
  `RESULTADO RARO nan: precio=nan pct=100`
- **`float("inf")` y `float("-inf")` (Infinito):**  
  Precios o porcentajes infinitos producían resultados fuera de la lógica de negocio (precios infinitos).

**Condición añadida a `resultado_valido()` y correcciones realizadas:**

1. En `resultado_valido()` (`fuzz_casero.py`), se verificó mediante el módulo `math`:
   - Que el resultado sea un número finito: `math.isfinite(resultado)`.
   - Que el precio no sea negativo: `resultado >= 0`.
   - Que el precio con descuento no sea superior al precio original: `resultado <= max(precio, round(precio, 2))`.
2. En `descuentos.py`, se añadió validación con `math.isfinite()` tanto para `precio` como para `pct`:
   ```python
   if not isinstance(precio, (int, float)) or not math.isfinite(precio) or precio < 0:
       raise ValueError("precio no válido")
   if not isinstance(pct, (int, float)) or not math.isfinite(pct) or not (0 <= pct <= 100):
       raise ValueError("porcentaje fuera de rango")
   ```
3. Se añadió un nuevo test de regresión `test_regresion_fuzzing_valores_raros` en `test_descuentos.py`.  
Resultado final: **`0 fallos en 20000 intentos`** y **100% de tests pasando**.

---

### 5. URL de tu repositorio

```text
https://github.com/CHALIETOS/pps-arranque.git
```

---

## Checklist de comprobación previa a la entrega (para cuando hagas git)

- [x] Entorno virtual configurado y `.venv/` verificado en `.gitignore`.
- [x] `PPS-E1-lectura.md` completado con la tabla de análisis y correcciones de `validar.py`, `Validar.java` y `validar.c`.
- [x] Test de regresión `test_regresion_incidencia_17` implementado en `test_descuentos.py`.
- [x] `aplicar_descuento` corregido en `descuentos.py` para rechazar porcentajes fuera de [0, 100].
- [x] `resultado_valido` completado en `fuzz_casero.py` con validaciones de `math.isfinite()`.
- [x] `fuzz_casero.py` ejecutado con **0 fallos en 20000 intentos**.
- [x] Suite de tests pasando en verde con 100% de cobertura (`pytest -q` y `coverage report -m`).
- [x] Preguntas contestadas en este documento.
- [ ] Comprobar `git status` (no debe salir `.venv`).
- [ ] Ejecutar `git add ut1 && git commit -m "Práctica 2: PPS-E1 y PPS-E2" && git push`.
