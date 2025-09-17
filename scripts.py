import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import random
import datetime

# Lista de tipos de datos comunes en MySQL
DATA_TYPES = [
    "INT", "VARCHAR(255)", "TEXT", "DATE", "DATETIME", "TIMESTAMP",
    "DECIMAL(10,2)", "FLOAT", "DOUBLE", "BOOLEAN", "ENUM", "BLOB",
    "TINYINT", "SMALLINT", "MEDIUMINT", "BIGINT", "CHAR", "TIME",
    "YEAR", "BINARY", "VARBINARY", "TINYBLOB", "MEDIUMBLOB", "LONGBLOB",
    "TINYTEXT", "MEDIUMTEXT", "LONGTEXT"
]

# Acciones ON para claves foráneas
FK_ACTIONS = ["RESTRICT", "CASCADE", "SET NULL", "NO ACTION"]

# Funciones MySQL comunes
MYSQL_FUNCTIONS = [
    "COUNT", "SUM", "AVG", "MIN", "MAX", "CONCAT", "NOW", "DATE_FORMAT",
    "UPPER", "LOWER", "SUBSTRING", "ROUND", "COALESCE", "IFNULL"
]

# Tipos de joins
JOIN_TYPES = ["INNER JOIN", "LEFT JOIN", "RIGHT JOIN", "FULL JOIN"]

class MySQLGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MySQL Script Generator Pro")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Variables globales
        self.claves_primarias = []
        self.tablas = ["usuarios", "productos", "pedidos", "clientes", "empleados"]
        
        # Configurar estilo
        self.setup_styles()
        
        # Crear notebook (pestañas)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Crear las pestañas
        self.create_database_tab()
        self.create_table_tab()
        self.create_insert_tab()
        self.create_select_tab()
        self.create_update_tab()
        self.create_delete_tab()
        self.create_procedure_tab()
        self.create_view_tab()
        self.create_trigger_tab()
        
        # Barra de estado
        self.status_bar = ttk.Label(root, text="Listo", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_styles(self):
        style = ttk.Style()
        style.configure("TNotebook.Tab", padding=[10, 5])
        style.configure("Title.TLabel", font=("Arial", 12, "bold"))
        style.configure("Header.TFrame", background="#f0f0f0")
    
    def create_database_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="CREATE DATABASE")
        
        title = ttk.Label(tab, text="Generador de Script CREATE DATABASE", style="Title.TLabel")
        title.pack(pady=10)
        
        frame = ttk.LabelFrame(tab, text="Parámetros de la Base de Datos")
        frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(frame, text="Nombre de la Base de Datos:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.db_name_entry = ttk.Entry(frame, width=30)
        self.db_name_entry.grid(row=0, column=1, pady=5, padx=5)
        self.db_name_entry.insert(0, "mi_basedatos")
        
        ttk.Label(frame, text="Charset:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.db_charset_combo = ttk.Combobox(frame, values=["utf8mb4", "utf8", "latin1"], width=15)
        self.db_charset_combo.grid(row=1, column=1, pady=5, padx=5)
        self.db_charset_combo.set("utf8mb4")
        
        ttk.Label(frame, text="Collation:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.db_collation_combo = ttk.Combobox(frame, values=["utf8mb4_unicode_ci", "utf8mb4_general_ci", "utf8_unicode_ci", "latin1_swedish_ci"], width=20)
        self.db_collation_combo.grid(row=2, column=1, pady=5, padx=5)
        self.db_collation_combo.set("utf8mb4_unicode_ci")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Generar Script", command=self.generate_database_script).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=lambda: self.db_script_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        self.db_script_text = scrolledtext.ScrolledText(tab, width=80, height=10, font=("Consolas", 10))
        self.db_script_text.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_table_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="CREATE TABLE")
        
        title = ttk.Label(tab, text="Generador de Script CREATE TABLE", style="Title.TLabel")
        title.pack(pady=10)
        
        # Frame para información de la tabla
        table_frame = ttk.LabelFrame(tab, text="Información de la tabla")
        table_frame.pack(pady=5, padx=20, fill="x")
        
        ttk.Label(table_frame, text="Nombre de la tabla:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.table_name_entry = ttk.Entry(table_frame, width=30)
        self.table_name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(table_frame, text="Motor:").grid(row=0, column=2, sticky="w", pady=5, padx=5)
        self.engine_combo = ttk.Combobox(table_frame, values=["InnoDB", "MyISAM", "MEMORY", "CSV", "ARCHIVE"], width=15)
        self.engine_combo.grid(row=0, column=3, pady=5, padx=5)
        self.engine_combo.set("InnoDB")
        
        ttk.Label(table_frame, text="Charset:").grid(row=0, column=4, sticky="w", pady=5, padx=5)
        self.charset_combo = ttk.Combobox(table_frame, values=["utf8mb4", "utf8", "latin1", "ascii"], width=15)
        self.charset_combo.grid(row=0, column=5, pady=5, padx=5)
        self.charset_combo.set("utf8mb4")
        
        # Frame para agregar campos
        fields_frame = ttk.LabelFrame(tab, text="Agregar campos")
        fields_frame.pack(pady=5, padx=20, fill="x")
        
        ttk.Label(fields_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.field_name_entry = ttk.Entry(fields_frame, width=20)
        self.field_name_entry.grid(row=0, column=1, pady=5, padx=5)
        
        ttk.Label(fields_frame, text="Tipo:").grid(row=0, column=2, sticky="w", pady=5, padx=5)
        self.field_type_combo = ttk.Combobox(fields_frame, values=DATA_TYPES, width=15)
        self.field_type_combo.grid(row=0, column=3, pady=5, padx=5)
        self.field_type_combo.set("VARCHAR(255)")
        
        ttk.Label(fields_frame, text="Nulo:").grid(row=0, column=4, sticky="w", pady=5, padx=5)
        self.field_null_combo = ttk.Combobox(fields_frame, values=["NULL", "NOT NULL"], width=10)
        self.field_null_combo.grid(row=0, column=5, pady=5, padx=5)
        self.field_null_combo.set("NULL")
        
        self.field_ai_var = tk.BooleanVar()
        self.field_ai_check = ttk.Checkbutton(fields_frame, text="Auto Increment", variable=self.field_ai_var)
        self.field_ai_check.grid(row=1, column=0, pady=5, padx=5)
        
        self.field_pk_var = tk.BooleanVar()
        self.field_pk_check = ttk.Checkbutton(fields_frame, text="Clave Primaria", variable=self.field_pk_var)
        self.field_pk_check.grid(row=1, column=1, pady=5, padx=5)
        
        self.field_unique_var = tk.BooleanVar()
        self.field_unique_check = ttk.Checkbutton(fields_frame, text="Único", variable=self.field_unique_var)
        self.field_unique_check.grid(row=1, column=2, pady=5, padx=5)
        
        btn_frame = ttk.Frame(fields_frame)
        btn_frame.grid(row=2, column=0, columnspan=6, pady=10)
        
        ttk.Button(btn_frame, text="Agregar Campo", command=self.add_field).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Eliminar Campo", command=self.remove_field).pack(side=tk.LEFT, padx=5)
        
        # Lista de campos
        list_frame = ttk.LabelFrame(tab, text="Campos de la tabla")
        list_frame.pack(pady=5, padx=20, fill="both", expand=True)
        
        self.fields_listbox = tk.Listbox(list_frame, height=8)
        self.fields_listbox.pack(pady=5, padx=5, fill="both", expand=True)
        
        # Botones finales
        action_frame = ttk.Frame(tab)
        action_frame.pack(pady=10)
        
        ttk.Button(action_frame, text="Generar Script", command=self.generate_table_script).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Limpiar Todo", command=self.clear_table_fields).pack(side=tk.LEFT, padx=5)
        
        # Área de script
        self.table_script_text = scrolledtext.ScrolledText(tab, width=80, height=10, font=("Consolas", 10))
        self.table_script_text.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_insert_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="INSERT")
        
        title = ttk.Label(tab, text="Generador de Script INSERT", style="Title.TLabel")
        title.pack(pady=10)
        
        frame = ttk.LabelFrame(tab, text="Parámetros INSERT")
        frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(frame, text="Tabla:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.insert_table_combo = ttk.Combobox(frame, values=self.tablas, width=20)
        self.insert_table_combo.grid(row=0, column=1, pady=5, padx=5)
        self.insert_table_combo.set("usuarios")
        
        ttk.Label(frame, text="Número de registros:").grid(row=0, column=2, sticky="w", pady=5, padx=5)
        self.insert_count_spin = ttk.Spinbox(frame, from_=1, to=100, width=10)
        self.insert_count_spin.grid(row=0, column=3, pady=5, padx=5)
        self.insert_count_spin.set(5)
        
        ttk.Label(frame, text="Campos (separados por coma):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.insert_fields_entry = ttk.Entry(frame, width=50)
        self.insert_fields_entry.grid(row=1, column=1, columnspan=3, pady=5, padx=5, sticky="we")
        self.insert_fields_entry.insert(0, "nombre, email, fecha_registro")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Generar Script", command=self.generate_insert_script).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=lambda: self.insert_script_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        self.insert_script_text = scrolledtext.ScrolledText(tab, width=80, height=15, font=("Consolas", 10))
        self.insert_script_text.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_select_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="SELECT")
        
        title = ttk.Label(tab, text="Generador de Script SELECT", style="Title.TLabel")
        title.pack(pady=10)
        
        frame = ttk.LabelFrame(tab, text="Parámetros SELECT")
        frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(frame, text="Tabla:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.select_table_combo = ttk.Combobox(frame, values=self.tablas, width=20)
        self.select_table_combo.grid(row=0, column=1, pady=5, padx=5)
        self.select_table_combo.set("usuarios")
        
        ttk.Label(frame, text="Campos ( * para todos):").grid(row=0, column=2, sticky="w", pady=5, padx=5)
        self.select_fields_entry = ttk.Entry(frame, width=30)
        self.select_fields_entry.grid(row=0, column=3, pady=5, padx=5)
        self.select_fields_entry.insert(0, "*")
        
        ttk.Label(frame, text="Condición WHERE:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.select_where_entry = ttk.Entry(frame, width=30)
        self.select_where_entry.grid(row=1, column=1, pady=5, padx=5)
        self.select_where_entry.insert(0, "id > 10")
        
        ttk.Label(frame, text="Ordenar por:").grid(row=1, column=2, sticky="w", pady=5, padx=5)
        self.select_order_entry = ttk.Entry(frame, width=30)
        self.select_order_entry.grid(row=1, column=3, pady=5, padx=5)
        self.select_order_entry.insert(0, "fecha_registro DESC")
        
        ttk.Label(frame, text="Límite:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.select_limit_spin = ttk.Spinbox(frame, from_=0, to=1000, width=10)
        self.select_limit_spin.grid(row=2, column=1, pady=5, padx=5)
        self.select_limit_spin.set(10)
        
        ttk.Label(frame, text="Agrupar por:").grid(row=2, column=2, sticky="w", pady=5, padx=5)
        self.select_group_entry = ttk.Entry(frame, width=30)
        self.select_group_entry.grid(row=2, column=3, pady=5, padx=5)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Generar Script", command=self.generate_select_script).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=lambda: self.select_script_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        self.select_script_text = scrolledtext.ScrolledText(tab, width=80, height=15, font=("Consolas", 10))
        self.select_script_text.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_update_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="UPDATE")
        
        title = ttk.Label(tab, text="Generador de Script UPDATE", style="Title.TLabel")
        title.pack(pady=10)
        
        frame = ttk.LabelFrame(tab, text="Parámetros UPDATE")
        frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(frame, text="Tabla:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.update_table_combo = ttk.Combobox(frame, values=self.tablas, width=20)
        self.update_table_combo.grid(row=0, column=1, pady=5, padx=5)
        self.update_table_combo.set("usuarios")
        
        ttk.Label(frame, text="Valores a actualizar:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.update_set_entry = ttk.Entry(frame, width=50)
        self.update_set_entry.grid(row=1, column=1, columnspan=3, pady=5, padx=5, sticky="we")
        self.update_set_entry.insert(0, "nombre = 'Nuevo Nombre', email = 'nuevo@email.com'")
        
        ttk.Label(frame, text="Condición WHERE:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.update_where_entry = ttk.Entry(frame, width=50)
        self.update_where_entry.grid(row=2, column=1, columnspan=3, pady=5, padx=5, sticky="we")
        self.update_where_entry.insert(0, "id = 1")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Generar Script", command=self.generate_update_script).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=lambda: self.update_script_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        self.update_script_text = scrolledtext.ScrolledText(tab, width=80, height=10, font=("Consolas", 10))
        self.update_script_text.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_delete_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="DELETE")
        
        title = ttk.Label(tab, text="Generador de Script DELETE", style="Title.TLabel")
        title.pack(pady=10)
        
        frame = ttk.LabelFrame(tab, text="Parámetros DELETE")
        frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(frame, text="Tabla:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.delete_table_combo = ttk.Combobox(frame, values=self.tablas, width=20)
        self.delete_table_combo.grid(row=0, column=1, pady=5, padx=5)
        self.delete_table_combo.set("usuarios")
        
        ttk.Label(frame, text="Condición WHERE:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.delete_where_entry = ttk.Entry(frame, width=50)
        self.delete_where_entry.grid(row=1, column=1, columnspan=3, pady=5, padx=5, sticky="we")
        self.delete_where_entry.insert(0, "id = 1")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Generar Script", command=self.generate_delete_script).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=lambda: self.delete_script_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        self.delete_script_text = scrolledtext.ScrolledText(tab, width=80, height=10, font=("Consolas", 10))
        self.delete_script_text.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_procedure_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="PROCEDURE")
        
        title = ttk.Label(tab, text="Generador de Procedimientos Almacenados", style="Title.TLabel")
        title.pack(pady=10)
        
        frame = ttk.LabelFrame(tab, text="Parámetros del Procedimiento")
        frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(frame, text="Nombre del procedimiento:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.proc_name_entry = ttk.Entry(frame, width=30)
        self.proc_name_entry.grid(row=0, column=1, pady=5, padx=5)
        self.proc_name_entry.insert(0, "usp_obtener_usuario")
        
        ttk.Label(frame, text="Parámetros (ej: IN id INT):").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.proc_params_entry = ttk.Entry(frame, width=50)
        self.proc_params_entry.grid(row=1, column=1, columnspan=3, pady=5, padx=5, sticky="we")
        self.proc_params_entry.insert(0, "IN usuario_id INT")
        
        ttk.Label(frame, text="Cuerpo del procedimiento:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.proc_body_text = scrolledtext.ScrolledText(frame, width=70, height=8, font=("Consolas", 10))
        self.proc_body_text.grid(row=2, column=1, columnspan=3, pady=5, padx=5, sticky="we")
        self.proc_body_text.insert(1.0, "SELECT * FROM usuarios WHERE id = usuario_id;")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Generar Script", command=self.generate_procedure_script).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=lambda: self.proc_script_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        self.proc_script_text = scrolledtext.ScrolledText(tab, width=80, height=10, font=("Consolas", 10))
        self.proc_script_text.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_view_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="VIEW")
        
        title = ttk.Label(tab, text="Generador de Vistas", style="Title.TLabel")
        title.pack(pady=10)
        
        frame = ttk.LabelFrame(tab, text="Parámetros de la Vista")
        frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(frame, text="Nombre de la vista:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.view_name_entry = ttk.Entry(frame, width=30)
        self.view_name_entry.grid(row=0, column=1, pady=5, padx=5)
        self.view_name_entry.insert(0, "vista_usuarios")
        
        ttk.Label(frame, text="Consulta SELECT:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.view_select_text = scrolledtext.ScrolledText(frame, width=70, height=8, font=("Consolas", 10))
        self.view_select_text.grid(row=1, column=1, columnspan=3, pady=5, padx=5, sticky="we")
        self.view_select_text.insert(1.0, "SELECT id, nombre, email FROM usuarios WHERE activo = 1")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Generar Script", command=self.generate_view_script).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=lambda: self.view_script_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        self.view_script_text = scrolledtext.ScrolledText(tab, width=80, height=10, font=("Consolas", 10))
        self.view_script_text.pack(pady=10, padx=20, fill="both", expand=True)
    
    def create_trigger_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="TRIGGER")
        
        title = ttk.Label(tab, text="Generador de Triggers", style="Title.TLabel")
        title.pack(pady=10)
        
        frame = ttk.LabelFrame(tab, text="Parámetros del Trigger")
        frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(frame, text="Nombre del trigger:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.trigger_name_entry = ttk.Entry(frame, width=30)
        self.trigger_name_entry.grid(row=0, column=1, pady=5, padx=5)
        self.trigger_name_entry.insert(0, "trg_after_insert_usuario")
        
        ttk.Label(frame, text="Tabla:").grid(row=0, column=2, sticky="w", pady=5, padx=5)
        self.trigger_table_combo = ttk.Combobox(frame, values=self.tablas, width=15)
        self.trigger_table_combo.grid(row=0, column=3, pady=5, padx=5)
        self.trigger_table_combo.set("usuarios")
        
        ttk.Label(frame, text="Tiempo:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.trigger_time_combo = ttk.Combobox(frame, values=["BEFORE", "AFTER"], width=10)
        self.trigger_time_combo.grid(row=1, column=1, pady=5, padx=5)
        self.trigger_time_combo.set("AFTER")
        
        ttk.Label(frame, text="Evento:").grid(row=1, column=2, sticky="w", pady=5, padx=5)
        self.trigger_event_combo = ttk.Combobox(frame, values=["INSERT", "UPDATE", "DELETE"], width=10)
        self.trigger_event_combo.grid(row=1, column=3, pady=5, padx=5)
        self.trigger_event_combo.set("INSERT")
        
        ttk.Label(frame, text="Cuerpo del trigger:").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.trigger_body_text = scrolledtext.ScrolledText(frame, width=70, height=8, font=("Consolas", 10))
        self.trigger_body_text.grid(row=2, column=1, columnspan=3, pady=5, padx=5, sticky="we")
        self.trigger_body_text.insert(1.0, "INSERT INTO log_usuario (accion, usuario_id, fecha) VALUES ('INSERT', NEW.id, NOW());")
        
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(btn_frame, text="Generar Script", command=self.generate_trigger_script).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpiar", command=lambda: self.trigger_script_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        self.trigger_script_text = scrolledtext.ScrolledText(tab, width=80, height=10, font=("Consolas", 10))
        self.trigger_script_text.pack(pady=10, padx=20, fill="both", expand=True)
    
    # Métodos para generar scripts
    def generate_database_script(self):
        db_name = self.db_name_entry.get().strip()
        charset = self.db_charset_combo.get()
        collation = self.db_collation_combo.get()
        
        if not db_name:
            messagebox.showerror("Error", "El nombre de la base de datos es obligatorio")
            return
        
        script = f"CREATE DATABASE {db_name}\n"
        script += f"CHARACTER SET = {charset}\n"
        script += f"COLLATE = {collation};\n\n"
        script += f"USE {db_name};"
        
        self.db_script_text.delete(1.0, tk.END)
        self.db_script_text.insert(tk.END, script)
        self.status_bar.config(text="Script CREATE DATABASE generado con éxito")
    
    def add_field(self):
        name = self.field_name_entry.get().strip()
        type_ = self.field_type_combo.get()
        null = self.field_null_combo.get()
        ai = self.field_ai_var.get()
        pk = self.field_pk_var.get()
        unique = self.field_unique_var.get()
        
        if not name:
            messagebox.showerror("Error", "El nombre del campo es obligatorio")
            return
        
        field_def = f"{name} {type_}"
        
        if null == "NOT NULL":
            field_def += " NOT NULL"
        else:
            field_def += " NULL"
        
        if ai:
            field_def += " AUTO_INCREMENT"
        
        if unique:
            field_def += " UNIQUE"
        
        self.fields_listbox.insert(tk.END, field_def)
        
        if pk:
            self.claves_primarias.append(name)
        
        self.field_name_entry.delete(0, tk.END)
        self.field_ai_var.set(False)
        self.field_pk_var.set(False)
        self.field_unique_var.set(False)
    
    def remove_field(self):
        selection = self.fields_listbox.curselection()
        if selection:
            field = self.fields_listbox.get(selection[0])
            field_name = field.split()[0]
            
            if field_name in self.claves_primarias:
                self.claves_primarias.remove(field_name)
            
            self.fields_listbox.delete(selection[0])
    
    def clear_table_fields(self):
        self.fields_listbox.delete(0, tk.END)
        self.claves_primarias = []
        self.table_script_text.delete(1.0, tk.END)
        self.table_name_entry.delete(0, tk.END)
    
    def generate_table_script(self):
        table_name = self.table_name_entry.get().strip()
        engine = self.engine_combo.get()
        charset = self.charset_combo.get()
        
        if not table_name:
            messagebox.showerror("Error", "El nombre de la tabla es obligatorio")
            return
        
        if self.fields_listbox.size() == 0:
            messagebox.showerror("Error", "Debe agregar al menos un campo a la tabla")
            return
        
        script = f"CREATE TABLE {table_name} (\n"
        
        for i in range(self.fields_listbox.size()):
            script += f"    {self.fields_listbox.get(i)}"
            if i < self.fields_listbox.size() - 1 or self.claves_primarias:
                script += ","
            script += "\n"
        
        if self.claves_primarias:
            script += f"    PRIMARY KEY ({', '.join(self.claves_primarias)})"
        
        script += f"\n) ENGINE={engine} DEFAULT CHARSET={charset};"
        
        self.table_script_text.delete(1.0, tk.END)
        self.table_script_text.insert(tk.END, script)
        self.status_bar.config(text="Script CREATE TABLE generado con éxito")
    
    def generate_insert_script(self):
        table = self.insert_table_combo.get()
        count = int(self.insert_count_spin.get())
        fields = self.insert_fields_entry.get().strip()
        
        if not table or not fields:
            messagebox.showerror("Error", "La tabla y los campos son obligatorios")
            return
        
        field_list = [f.strip() for f in fields.split(",")]
        script = f"INSERT INTO {table} ({fields}) VALUES\n"
        
        for i in range(count):
            values = []
            for field in field_list:
                if "nombre" in field.lower():
                    values.append(f"'Usuario {i+1}'")
                elif "email" in field.lower():
                    values.append(f"'usuario{i+1}@example.com'")
                elif "fecha" in field.lower():
                    values.append("NOW()")
                elif "activo" in field.lower():
                    values.append("1")
                else:
                    values.append(f"'{i+1}'")
            
            script += f"    ({', '.join(values)})"
            if i < count - 1:
                script += ",\n"
            else:
                script += ";\n"
        
        self.insert_script_text.delete(1.0, tk.END)
        self.insert_script_text.insert(tk.END, script)
        self.status_bar.config(text="Script INSERT generado con éxito")
    
    def generate_select_script(self):
        table = self.select_table_combo.get()
        fields = self.select_fields_entry.get().strip()
        where = self.select_where_entry.get().strip()
        order = self.select_order_entry.get().strip()
        limit = self.select_limit_spin.get()
        group = self.select_group_entry.get().strip()
        
        if not table or not fields:
            messagebox.showerror("Error", "La tabla y los campos son obligatorios")
            return
        
        script = f"SELECT {fields} FROM {table}"
        
        if where:
            script += f" WHERE {where}"
        
        if group:
            script += f" GROUP BY {group}"
        
        if order:
            script += f" ORDER BY {order}"
        
        if limit and int(limit) > 0:
            script += f" LIMIT {limit}"
        
        script += ";"
        
        self.select_script_text.delete(1.0, tk.END)
        self.select_script_text.insert(tk.END, script)
        self.status_bar.config(text="Script SELECT generado con éxito")
    
    def generate_update_script(self):
        table = self.update_table_combo.get()
        set_clause = self.update_set_entry.get().strip()
        where = self.update_where_entry.get().strip()
        
        if not table or not set_clause:
            messagebox.showerror("Error", "La tabla y los valores a actualizar son obligatorios")
            return
        
        script = f"UPDATE {table} SET {set_clause}"
        
        if where:
            script += f" WHERE {where}"
        
        script += ";"
        
        self.update_script_text.delete(1.0, tk.END)
        self.update_script_text.insert(tk.END, script)
        self.status_bar.config(text="Script UPDATE generado con éxito")
    
    def generate_delete_script(self):
        table = self.delete_table_combo.get()
        where = self.delete_where_entry.get().strip()
        
        if not table:
            messagebox.showerror("Error", "La tabla es obligatoria")
            return
        
        script = f"DELETE FROM {table}"
        
        if where:
            script += f" WHERE {where}"
        
        script += ";"
        
        self.delete_script_text.delete(1.0, tk.END)
        self.delete_script_text.insert(tk.END, script)
        self.status_bar.config(text="Script DELETE generado con éxito")
    
    def generate_procedure_script(self):
        name = self.proc_name_entry.get().strip()
        params = self.proc_params_entry.get().strip()
        body = self.proc_body_text.get(1.0, tk.END).strip()
        
        if not name or not body:
            messagebox.showerror("Error", "El nombre y el cuerpo del procedimiento son obligatorios")
            return
        
        script = f"DELIMITER //\n"
        script += f"CREATE PROCEDURE {name}"
        
        if params:
            script += f"({params})"
        
        script += "\nBEGIN\n"
        script += f"    {body}\n"
        script += "END //\n"
        script += "DELIMITER ;"
        
        self.proc_script_text.delete(1.0, tk.END)
        self.proc_script_text.insert(tk.END, script)
        self.status_bar.config(text="Script PROCEDURE generado con éxito")
    
    def generate_view_script(self):
        name = self.view_name_entry.get().strip()
        select = self.view_select_text.get(1.0, tk.END).strip()
        
        if not name or not select:
            messagebox.showerror("Error", "El nombre y la consulta SELECT son obligatorios")
            return
        
        script = f"CREATE VIEW {name} AS\n"
        script += f"{select};"
        
        self.view_script_text.delete(1.0, tk.END)
        self.view_script_text.insert(tk.END, script)
        self.status_bar.config(text="Script VIEW generado con éxito")
    
    def generate_trigger_script(self):
        name = self.trigger_name_entry.get().strip()
        table = self.trigger_table_combo.get()
        time = self.trigger_time_combo.get()
        event = self.trigger_event_combo.get()
        body = self.trigger_body_text.get(1.0, tk.END).strip()
        
        if not name or not table or not body:
            messagebox.showerror("Error", "El nombre, tabla y cuerpo del trigger son obligatorios")
            return
        
        script = f"DELIMITER //\n"
        script += f"CREATE TRIGGER {name} {time} {event} ON {table}\n"
        script += "FOR EACH ROW\n"
        script += "BEGIN\n"
        script += f"    {body}\n"
        script += "END //\n"
        script += "DELIMITER ;"
        
        self.trigger_script_text.delete(1.0, tk.END)
        self.trigger_script_text.insert(tk.END, script)
        self.status_bar.config(text="Script TRIGGER generado con éxito")

if __name__ == "__main__":
    root = tk.Tk()
    app = MySQLGeneratorApp(root)
    root.mainloop()