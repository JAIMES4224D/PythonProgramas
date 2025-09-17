import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

def generar_codigo():
    url = url_entry.get()
    user = user_entry.get()
    password = password_entry.get()
    
    if not url or not user:
        messagebox.showerror("Error", "Por favor, complete la URL y el usuario")
        return
    
    codigo = f"""import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ConexionBD {{
    private static final String URL = "{url}";
    private static final String USER = "{user}";
    private static final String PASSWORD = "{password}";
    
    public static Connection getConnection() throws SQLException {{
        try {{
            // Cargar el driver (opcional en versiones recientes de JDBC)
            Class.forName("com.mysql.cj.jdbc.Driver");
        }} catch (ClassNotFoundException e) {{
            throw new SQLException("Driver MySQL no encontrado", e);
        }}
        
        return DriverManager.getConnection(URL, USER, PASSWORD);
    }}
    
    public static void main(String[] args) {{
        try (Connection conn = getConnection()) {{
            if (conn != null) {{
                System.out.println("Conexión exitosa a la base de datos");
            }} else {{
                System.out.println("Error: No se pudo establecer la conexión");
            }}
        }} catch (SQLException e) {{
            System.err.println("Error de conexión: " + e.getMessage());
            e.printStackTrace();
        }}
    }}
}}"""
    
    codigo_text.delete(1.0, tk.END)
    codigo_text.insert(tk.END, codigo)

# Crear ventana principal
root = tk.Tk()
root.title("Generador de Código Java para MySQL")
root.geometry("700x600")
root.resizable(True, True)

# Título
titulo = tk.Label(root, text="Generador de Código de Conexión Java a MySQL", 
                 font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# Frame para los campos de entrada
frame_entrada = ttk.Frame(root)
frame_entrada.pack(pady=10, padx=20, fill="x")

# Campo para la URL
url_label = ttk.Label(frame_entrada, text="URL de la base de datos:")
url_label.grid(row=0, column=0, sticky="w", pady=5)
url_entry = ttk.Entry(frame_entrada, width=50)
url_entry.grid(row=0, column=1, padx=5, pady=5)
url_entry.insert(0, "jdbc:mysql://localhost:3306/nombre_bd")

# Campo para el usuario
user_label = ttk.Label(frame_entrada, text="Usuario:")
user_label.grid(row=1, column=0, sticky="w", pady=5)
user_entry = ttk.Entry(frame_entrada, width=50)
user_entry.grid(row=1, column=1, padx=5, pady=5)
user_entry.insert(0, "root")

# Campo para la contraseña
password_label = ttk.Label(frame_entrada, text="Contraseña:")
password_label.grid(row=2, column=0, sticky="w", pady=5)
password_entry = ttk.Entry(frame_entrada, width=50, show="*")
password_entry.grid(row=2, column=1, padx=5, pady=5)

# Botón para generar código
generar_btn = ttk.Button(root, text="Generar Código Java", command=generar_codigo)
generar_btn.pack(pady=10)

# Área de texto para mostrar el código generado
codigo_label = ttk.Label(root, text="Código generado:")
codigo_label.pack(anchor="w", padx=20)

codigo_text = scrolledtext.ScrolledText(root, width=80, height=20, font=("Consolas", 10))
codigo_text.pack(pady=10, padx=20, fill="both", expand=True)

# Información adicional
info_text = """
Instrucciones:
1. Complete la URL de conexión (ej: jdbc:mysql://localhost:3306/mi_basedatos)
2. Ingrese su nombre de usuario de MySQL
3. Ingrese su contraseña (opcional)
4. Haga clic en 'Generar Código Java'
5. Copie el código generado a su proyecto Java

Requisitos:
- Asegúrese de tener el conector MySQL para Java en su classpath
- Descargue el driver desde: https://dev.mysql.com/downloads/connector/j/
"""
info_label = ttk.Label(root, text=info_text, justify=tk.LEFT)
info_label.pack(pady=5, padx=20, anchor="w")

# Ejecutar la aplicación
root.mainloop()