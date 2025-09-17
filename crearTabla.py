import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

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

def agregar_campo():
    nombre = campo_nombre_entry.get().strip()
    tipo = campo_tipo_combobox.get()
    nulo = campo_nulo_var.get()
    auto_inc = campo_auto_inc_var.get()
    pk = campo_pk_var.get()
    unico = campo_unico_var.get()
    
    if not nombre:
        messagebox.showerror("Error", "El nombre del campo no puede estar vacío")
        return
    
    # Construir la definición del campo
    definicion = f"{nombre} {tipo}"
    
    if nulo == "NOT NULL":
        definicion += " NOT NULL"
    else:
        definicion += " NULL"
    
    if auto_inc:
        definicion += " AUTO_INCREMENT"
    
    if unico:
        definicion += " UNIQUE"
    
    # Agregar a la lista
    campos_listbox.insert(tk.END, definicion)
    
    # Si es clave primaria, agregar a la lista de PKs
    if pk:
        if nombre not in claves_primarias:
            claves_primarias.append(nombre)
    
    # Actualizar lista de campos para FKs
    actualizar_lista_campos_fk()
    
    # Limpiar campos
    campo_nombre_entry.delete(0, tk.END)
    campo_nulo_var.set("NULL")
    campo_auto_inc_var.set(False)
    campo_pk_var.set(False)
    campo_unico_var.set(False)

def eliminar_campo():
    seleccion = campos_listbox.curselection()
    if seleccion:
        campo = campos_listbox.get(seleccion[0])
        campo_nombre = campo.split()[0]
        
        # Eliminar de claves primarias si está
        if campo_nombre in claves_primarias:
            claves_primarias.remove(campo_nombre)
            
        # Eliminar de FKs si está
        for i in range(fk_listbox.size()-1, -1, -1):
            fk_info = fk_listbox.get(i)
            if campo_nombre in fk_info:
                fk_listbox.delete(i)
                
        campos_listbox.delete(seleccion[0])
        actualizar_lista_campos_fk()

def agregar_fk():
    campo_local = fk_campo_local_combobox.get()
    tabla_ref = fk_tabla_ref_entry.get().strip()
    campo_ref = fk_campo_ref_entry.get().strip()
    on_delete = fk_on_delete_combobox.get()
    on_update = fk_on_update_combobox.get()
    
    if not campo_local or not tabla_ref or not campo_ref:
        messagebox.showerror("Error", "Todos los campos de FK son obligatorios")
        return
    
    fk_def = f"FK_{campo_local}_{tabla_ref} FOREIGN KEY ({campo_local}) REFERENCES {tabla_ref}({campo_ref})"
    
    if on_delete != "RESTRICT":
        fk_def += f" ON DELETE {on_delete}"
    
    if on_update != "RESTRICT":
        fk_def += f" ON UPDATE {on_update}"
    
    fk_listbox.insert(tk.END, fk_def)
    
    # Limpiar campos
    fk_tabla_ref_entry.delete(0, tk.END)
    fk_campo_ref_entry.delete(0, tk.END)
    fk_on_delete_combobox.set("RESTRICT")
    fk_on_update_combobox.set("RESTRICT")

def eliminar_fk():
    seleccion = fk_listbox.curselection()
    if seleccion:
        fk_listbox.delete(seleccion[0])

def actualizar_lista_campos_fk():
    # Obtener todos los nombres de campos
    campos = []
    for i in range(campos_listbox.size()):
        campo = campos_listbox.get(i)
        campo_nombre = campo.split()[0]
        campos.append(campo_nombre)
    
    # Actualizar combobox
    fk_campo_local_combobox['values'] = campos
    if campos:
        fk_campo_local_combobox.set(campos[0])

def generar_script():
    nombre_tabla = tabla_nombre_entry.get().strip()
    motor = motor_combobox.get()
    charset = charset_combobox.get()
    
    if not nombre_tabla:
        messagebox.showerror("Error", "El nombre de la tabla no puede estar vacío")
        return
    
    if campos_listbox.size() == 0:
        messagebox.showerror("Error", "Debe agregar al menos un campo a la tabla")
        return
    
    # Construir el script SQL
    script = f"CREATE TABLE {nombre_tabla} (\n"
    
    # Agregar todos los campos
    for i in range(campos_listbox.size()):
        script += f"    {campos_listbox.get(i)}"
        if i < campos_listbox.size() - 1 or claves_primarias or fk_listbox.size() > 0:
            script += ","
        script += "\n"
    
    # Agregar clave primaria si hay
    if claves_primarias:
        script += f"    PRIMARY KEY ({', '.join(claves_primarias)})"
        if fk_listbox.size() > 0:
            script += ","
        script += "\n"
    
    # Agregar claves foráneas si hay
    for i in range(fk_listbox.size()):
        script += f"    {fk_listbox.get(i)}"
        if i < fk_listbox.size() - 1:
            script += ","
        script += "\n"
    
    script += f"\n) ENGINE={motor} DEFAULT CHARSET={charset};"
    
    # Mostrar el script
    script_text.delete(1.0, tk.END)
    script_text.insert(tk.END, script)

def limpiar_todo():
    tabla_nombre_entry.delete(0, tk.END)
    campos_listbox.delete(0, tk.END)
    fk_listbox.delete(0, tk.END)
    claves_primarias.clear()
    script_text.delete(1.0, tk.END)
    campo_nulo_var.set("NULL")
    campo_auto_inc_var.set(False)
    campo_pk_var.set(False)
    campo_unico_var.set(False)
    fk_on_delete_combobox.set("RESTRICT")
    fk_on_update_combobox.set("RESTRICT")

# Variables globales
claves_primarias = []

# Crear ventana principal
root = tk.Tk()
root.title("Generador de Scripts SQL para MySQL")
root.geometry("900x800")
root.resizable(True, True)

# Título
titulo = tk.Label(root, text="Generador de Scripts CREATE TABLE para MySQL", 
                 font=("Arial", 16, "bold"))
titulo.pack(pady=10)

# Frame para información de la tabla
tabla_frame = ttk.LabelFrame(root, text="Información de la tabla")
tabla_frame.pack(pady=5, padx=20, fill="x")

# Nombre de la tabla
ttk.Label(tabla_frame, text="Nombre de la tabla:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
tabla_nombre_entry = ttk.Entry(tabla_frame, width=30)
tabla_nombre_entry.grid(row=0, column=1, pady=5, padx=5)

# Motor de almacenamiento
ttk.Label(tabla_frame, text="Motor:").grid(row=0, column=2, sticky="w", pady=5, padx=5)
motor_combobox = ttk.Combobox(tabla_frame, values=["InnoDB", "MyISAM", "MEMORY", "CSV", "ARCHIVE"], width=15)
motor_combobox.grid(row=0, column=3, pady=5, padx=5)
motor_combobox.set("InnoDB")

# Charset
ttk.Label(tabla_frame, text="Charset:").grid(row=0, column=4, sticky="w", pady=5, padx=5)
charset_combobox = ttk.Combobox(tabla_frame, values=["utf8mb4", "utf8", "latin1", "ascii"], width=15)
charset_combobox.grid(row=0, column=5, pady=5, padx=5)
charset_combobox.set("utf8mb4")

# Frame para agregar campos
campos_frame = ttk.LabelFrame(root, text="Agregar campos")
campos_frame.pack(pady=5, padx=20, fill="x")

# Campos de entrada para el campo
ttk.Label(campos_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
campo_nombre_entry = ttk.Entry(campos_frame, width=20)
campo_nombre_entry.grid(row=0, column=1, pady=5, padx=5)

ttk.Label(campos_frame, text="Tipo:").grid(row=0, column=2, sticky="w", pady=5, padx=5)
campo_tipo_combobox = ttk.Combobox(campos_frame, values=DATA_TYPES, width=15)
campo_tipo_combobox.grid(row=0, column=3, pady=5, padx=5)
campo_tipo_combobox.set("VARCHAR(255)")

ttk.Label(campos_frame, text="Nulo:").grid(row=0, column=4, sticky="w", pady=5, padx=5)
campo_nulo_var = tk.StringVar(value="NULL")
campo_nulo_combobox = ttk.Combobox(campos_frame, textvariable=campo_nulo_var, 
                                  values=["NULL", "NOT NULL"], width=10)
campo_nulo_combobox.grid(row=0, column=5, pady=5, padx=5)

campo_auto_inc_var = tk.BooleanVar()
campo_auto_inc_check = ttk.Checkbutton(campos_frame, text="Auto Increment", variable=campo_auto_inc_var)
campo_auto_inc_check.grid(row=1, column=0, pady=5, padx=5)

campo_pk_var = tk.BooleanVar()
campo_pk_check = ttk.Checkbutton(campos_frame, text="Clave Primaria", variable=campo_pk_var)
campo_pk_check.grid(row=1, column=1, pady=5, padx=5)

campo_unico_var = tk.BooleanVar()
campo_unico_check = ttk.Checkbutton(campos_frame, text="Único", variable=campo_unico_var)
campo_unico_check.grid(row=1, column=2, pady=5, padx=5)

# Botones para agregar/eliminar campos
botones_frame = ttk.Frame(campos_frame)
botones_frame.grid(row=2, column=0, columnspan=6, pady=10)

agregar_btn = ttk.Button(botones_frame, text="Agregar Campo", command=agregar_campo)
agregar_btn.pack(side=tk.LEFT, padx=5)

eliminar_btn = ttk.Button(botones_frame, text="Eliminar Campo Seleccionado", command=eliminar_campo)
eliminar_btn.pack(side=tk.LEFT, padx=5)

# Lista de campos agregados
campos_list_frame = ttk.LabelFrame(root, text="Campos de la tabla")
campos_list_frame.pack(pady=5, padx=20, fill="both", expand=True)

campos_listbox = tk.Listbox(campos_list_frame, height=6)
campos_listbox.pack(pady=5, padx=5, fill="both", expand=True)

# Frame para claves foráneas
fk_frame = ttk.LabelFrame(root, text="Claves Foráneas (FK)")
fk_frame.pack(pady=5, padx=20, fill="x")

# Campos para FK
ttk.Label(fk_frame, text="Campo local:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
fk_campo_local_combobox = ttk.Combobox(fk_frame, width=20)
fk_campo_local_combobox.grid(row=0, column=1, pady=5, padx=5)

ttk.Label(fk_frame, text="Tabla referencia:").grid(row=0, column=2, sticky="w", pady=5, padx=5)
fk_tabla_ref_entry = ttk.Entry(fk_frame, width=20)
fk_tabla_ref_entry.grid(row=0, column=3, pady=5, padx=5)

ttk.Label(fk_frame, text="Campo referencia:").grid(row=0, column=4, sticky="w", pady=5, padx=5)
fk_campo_ref_entry = ttk.Entry(fk_frame, width=20)
fk_campo_ref_entry.grid(row=0, column=5, pady=5, padx=5)

ttk.Label(fk_frame, text="ON DELETE:").grid(row=1, column=0, sticky="w", pady=5, padx=5)
fk_on_delete_combobox = ttk.Combobox(fk_frame, values=FK_ACTIONS, width=10)
fk_on_delete_combobox.grid(row=1, column=1, pady=5, padx=5)
fk_on_delete_combobox.set("RESTRICT")

ttk.Label(fk_frame, text="ON UPDATE:").grid(row=1, column=2, sticky="w", pady=5, padx=5)
fk_on_update_combobox = ttk.Combobox(fk_frame, values=FK_ACTIONS, width=10)
fk_on_update_combobox.grid(row=1, column=3, pady=5, padx=5)
fk_on_update_combobox.set("RESTRICT")

# Botones para FK
fk_botones_frame = ttk.Frame(fk_frame)
fk_botones_frame.grid(row=2, column=0, columnspan=6, pady=10)

agregar_fk_btn = ttk.Button(fk_botones_frame, text="Agregar FK", command=agregar_fk)
agregar_fk_btn.pack(side=tk.LEFT, padx=5)

eliminar_fk_btn = ttk.Button(fk_botones_frame, text="Eliminar FK Seleccionada", command=eliminar_fk)
eliminar_fk_btn.pack(side=tk.LEFT, padx=5)

# Lista de FKs
fk_list_frame = ttk.LabelFrame(root, text="Claves Foráneas Definidas")
fk_list_frame.pack(pady=5, padx=20, fill="both", expand=True)

fk_listbox = tk.Listbox(fk_list_frame, height=4)
fk_listbox.pack(pady=5, padx=5, fill="both", expand=True)

# Botones para generar y limpiar
acciones_frame = ttk.Frame(root)
acciones_frame.pack(pady=10)

generar_btn = ttk.Button(acciones_frame, text="Generar Script SQL", command=generar_script)
generar_btn.pack(side=tk.LEFT, padx=5)

limpiar_btn = ttk.Button(acciones_frame, text="Limpiar Todo", command=limpiar_todo)
limpiar_btn.pack(side=tk.LEFT, padx=5)

# Área para mostrar el script generado
script_frame = ttk.LabelFrame(root, text="Script SQL Generado")
script_frame.pack(pady=5, padx=20, fill="both", expand=True)

script_text = scrolledtext.ScrolledText(script_frame, width=80, height=12, font=("Consolas", 10))
script_text.pack(pady=5, padx=5, fill="both", expand=True)

# Información adicional
info_text = """
Instrucciones:
1. Ingrese el nombre de la tabla
2. Seleccione el motor y charset (opcional)
3. Defina los campos: nombre, tipo, y propiedades
4. Agregue los campos a la lista
5. Defina claves foráneas si es necesario
6. Haga clic en 'Generar Script SQL'
7. Copie el script generado y ejecútelo en su base de datos MySQL

Notas:
- Las claves primarias se agregarán automáticamente al script
- Las claves foráneas requieren: campo local, tabla referencia y campo referencia
- Puede especificar acciones ON DELETE y ON UPDATE para las FKs
- Puede eliminar campos/FKs seleccionándolos y haciendo clic en los botones correspondientes
"""
info_label = ttk.Label(root, text=info_text, justify=tk.LEFT)
info_label.pack(pady=5, padx=20, anchor="w")

# Inicializar la lista de campos para FK
actualizar_lista_campos_fk()

# Ejecutar la aplicación
root.mainloop()