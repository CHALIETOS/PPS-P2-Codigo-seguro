// PPS UT1 · Validador de nombre de usuario — versión Java (MÁQUINA VIRTUAL / bytecode).
//
// Ejercicio PPS-E1: localiza PUNTO DE ENTRADA, SINK y VALIDACIÓN, y señala
// DÓNDE PUEDE FALLAR este modelo.
// Pista: el .class se puede decompilar (jadx, procyon). ¿Qué verías tú si lo hicieras?
// (Solo lectura: no hace falta compilarlo.)

import java.sql.*;

public class Validar {

    static boolean validarNombre(String nombre) {
        return nombre != null && nombre.length() > 0 && nombre.length() <= 32;
    }

    static void buscarUsuario(String nombre) throws SQLException {
        if (!validarNombre(nombre)) throw new IllegalArgumentException("nombre no válido");

        Connection con = DriverManager.getConnection("jdbc:sqlite::memory:");
        Statement st = con.createStatement();
        String consulta = "SELECT * FROM usuarios WHERE nombre = '" + nombre + "'";
        st.executeQuery(consulta);

        String apiKey = "LAB-DEMO-NO-REAL-1234";
        System.out.println("acceso de " + nombre);
    }

    public static void main(String[] args) throws SQLException {
        buscarUsuario(args.length > 0 ? args[0] : "ana");
    }
}
