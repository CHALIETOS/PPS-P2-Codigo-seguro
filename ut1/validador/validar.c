/* PPS UT1 · Validador de nombre de usuario — versión C (COMPILADO A NATIVO).
 *
 * Ejercicio PPS-E1: localiza PUNTO DE ENTRADA, SINK y VALIDACIÓN y señala
 * DÓNDE PUEDE FALLAR este modelo.
 * Pista: C no tiene seguridad de memoria. Mira los tamaños.
 *
 * Solo si el profesor lo indica (protecciones desactivadas, SOLO laboratorio):
 *   gcc -fno-stack-protector -o validar validar.c
 *   ./validar ana
 *   ./validar $(python3 -c 'print("A"*100)')
 */
#include <stdio.h>
#include <string.h>

void buscar_usuario(const char *nombre) {
    char buffer[32];
    strcpy(buffer, nombre);
    printf("acceso de %s\n", buffer);
}

int main(int argc, char **argv) {
    buscar_usuario(argc > 1 ? argv[1] : "ana");
    return 0;
}
