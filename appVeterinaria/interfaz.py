import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# =====================
# VENTANA PRINCIPAL
# =====================
class SistemaVeterinaria:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión Veterinaria")
        self.root.geometry("1050x650")
        self.root.configure(bg="#E8F6FF")

        self.menu_principal()

    # =====================
    # MENÚ PRINCIPAL
    # =====================
    def menu_principal(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        titulo = tk.Label(self.root, text="Sistema de Gestión Veterinaria", 
                          font=("Arial", 26, "bold"), bg="#E8F6FF", fg="#0077AA")
        titulo.pack(pady=40)

        frame_botones = tk.Frame(self.root, bg="#E8F6FF")
        frame_botones.pack()

        botones = [
            ("Clientes", self.ui_clientes),
            ("Mascotas", self.ui_mascotas),
            ("Veterinarios", self.ui_veterinarios),
            ("Razas", self.ui_razas),
            ("Remedios", self.ui_remedios),
            ("Citas", self.ui_citas)
        ]

        for texto, accion in botones:
            b = tk.Button(frame_botones, text=texto, command=accion,
                          width=20, height=2, bg="#A7E5FF", fg="black",
                          font=("Arial", 14), relief="raised", bd=3)
            b.pack(pady=10)

    # =====================
    # UI CLIENTES
    # =====================
    def ui_clientes(self):
        self.limpiar_ventana()

        titulo = tk.Label(self.root, text="Gestión de Clientes", font=("Arial", 22, "bold"))
        titulo.pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack()

        # FORMULARIO
        form = tk.Frame(frame)
        form.grid(row=0, column=0, padx=20)

        campos = ["Nombre Completo", "RUT", "Teléfono", "Dirección", "Correo"]
        self.entry_cliente = {}

        for i, campo in enumerate(campos):
            tk.Label(form, text=campo, font=("Arial", 12)).grid(row=i, column=0, sticky="w", pady=5)
            e = tk.Entry(form, width=30)
            e.grid(row=i, column=1, pady=5)
            self.entry_cliente[campo] = e

        # BOTONES
        botones = tk.Frame(form)
        botones.grid(row=6, column=0, columnspan=2, pady=10)

        for b in ["Registrar", "Editar", "Eliminar", "Buscar"]:
            tk.Button(botones, text=b, width=10).pack(side="left", padx=5)

        # TABLA
        tabla = ttk.Treeview(frame, columns=("Nombre", "RUT", "Fono", "Direccion", "Correo"), show="headings")
        for col in tabla["columns"]:
            tabla.heading(col, text=col)
            tabla.column(col, width=120)
        tabla.grid(row=0, column=1)

    # =====================
    # UI MASCOTAS
    # =====================
    def ui_mascotas(self):
        self.limpiar_ventana()

        titulo = tk.Label(self.root, text="Gestión de Mascotas", font=("Arial", 22, "bold"))
        titulo.pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack()

        form = tk.Frame(frame)
        form.grid(row=0, column=0, padx=20)

        campos = ["Nombre Mascota", "Especie", "Raza", "Edad", "Dueño"]
        self.entry_mascota = {}

        for i, campo in enumerate(campos):
            tk.Label(form, text=campo, font=("Arial", 12)).grid(row=i, column=0, sticky="w", pady=5)
            e = tk.Entry(form, width=30)
            e.grid(row=i, column=1, pady=5)
            self.entry_mascota[campo] = e

        botones = tk.Frame(form)
        botones.grid(row=6, column=0, columnspan=2, pady=10)
        for b in ["Registrar", "Editar", "Eliminar", "Buscar"]:
            tk.Button(botones, text=b, width=10).pack(side="left", padx=5)

        tabla = ttk.Treeview(frame, columns=("Nombre", "Especie", "Raza", "Edad", "Dueño"), show="headings")
        for col in tabla["columns"]:
            tabla.heading(col, text=col)
            tabla.column(col, width=120)
        tabla.grid(row=1, column=0, columnspan=2, pady=20)

    # =====================
    # UI VETERINARIOS
    # =====================
    def ui_veterinarios(self):
        self.limpiar_ventana()

        titulo = tk.Label(self.root, text="Gestión de Veterinarios", font=("Arial", 22, "bold"))
        titulo.pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack()

        form = tk.Frame(frame)
        form.grid(row=0, column=0, padx=20)

        campos = ["Nombre Completo", "Especialidad", "Teléfono", "Correo", "Disponibilidad"]
        self.entry_vet = {}

        for i, campo in enumerate(campos):
            tk.Label(form, text=campo, font=("Arial", 12)).grid(row=i, column=0, pady=5)
            e = tk.Entry(form, width=30)
            e.grid(row=i, column=1, pady=5)
            self.entry_vet[campo] = e

        botones = tk.Frame(form)
        botones.grid(row=6, column=0, columnspan=2, pady=10)
        for b in ["Registrar", "Editar", "Eliminar", "Buscar"]:
            tk.Button(botones, text=b, width=10).pack(side="left", padx=5)

        tabla = ttk.Treeview(frame, columns=("Nombre", "Especialidad", "Fono", "Correo", "Disp"), show="headings")
        for col in tabla["columns"]:
            tabla.heading(col, text=col)
            tabla.column(col, width=120)
        tabla.grid(row=0, column=1)

    # =====================
    # UI RAZAS
    # =====================
    def ui_razas(self):
        self.limpiar_ventana()

        titulo = tk.Label(self.root, text="Gestión de Razas", font=("Arial", 22, "bold"))
        titulo.pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack()

        form = tk.Frame(frame)
        form.grid(row=0, column=0, padx=20)

        campos = ["Nombre Raza", "Especie", "Notas"]
        self.entry_raza = {}

        for i, campo in enumerate(campos):
            tk.Label(form, text=campo, font=("Arial", 12)).grid(row=i, column=0, pady=5)
            e = tk.Entry(form, width=30)
            e.grid(row=i, column=1, pady=5)
            self.entry_raza[campo] = e

        botones = tk.Frame(form)
        botones.grid(row=4, column=0, columnspan=2, pady=10)
        for b in ["Registrar", "Editar", "Eliminar", "Buscar"]:
            tk.Button(botones, text=b, width=10).pack(side="left", padx=5)

        lista = tk.Listbox(frame, width=60, height=15)
        lista.grid(row=0, column=1)

    # =====================
    # UI REMEDIOS
    # =====================
    def ui_remedios(self):
        self.limpiar_ventana()

        titulo = tk.Label(self.root, text="Gestión de Remedios", font=("Arial", 22, "bold"))
        titulo.pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack()

        form = tk.Frame(frame)
        form.grid(row=0, column=0, padx=20)

        campos = ["Nombre Remedio", "Dosis", "Uso", "Stock"]
        self.entry_rem = {}

        for i, campo in enumerate(campos):
            tk.Label(form, text=campo, font=("Arial", 12)).grid(row=i, column=0, pady=5)
            e = tk.Entry(form, width=30)
            e.grid(row=i, column=1, pady=5)
            self.entry_rem[campo] = e

        botones = tk.Frame(form)
        botones.grid(row=5, column=0, columnspan=2, pady=10)
        for b in ["Registrar", "Editar", "Eliminar", "Buscar"]:
            tk.Button(botones, text=b, width=10).pack(side="left", padx=5)

        tabla = ttk.Treeview(frame, columns=("Nombre", "Dosis", "Uso", "Stock"), show="headings")
        for col in tabla["columns"]:
            tabla.heading(col, text=col)
            tabla.column(col, width=120)
        tabla.grid(row=0, column=1)

    # =====================
    # UI CITAS
    # =====================
    def ui_citas(self):
        self.limpiar_ventana()

        titulo = tk.Label(self.root, text="Gestión de Citas", font=("Arial", 22, "bold"))
        titulo.pack(pady=20)

        frame = tk.Frame(self.root)
        frame.pack()

        form = tk.Frame(frame)
        form.grid(row=0, column=0, padx=20)

        campos = ["Cliente", "Mascota", "Veterinario", "Fecha", "Hora", "Motivo"]
        self.entry_cita = {}

        for i, campo in enumerate(campos):
            tk.Label(form, text=campo, font=("Arial", 12)).grid(row=i, column=0, pady=5)
            e = tk.Entry(form, width=30)
            e.grid(row=i, column=1, pady=5)
            self.entry_cita[campo] = e

        botones = tk.Frame(form)
        botones.grid(row=7, column=0, columnspan=2, pady=10)
        for b in ["Registrar cita", "Editar", "Cancelar", "Buscar"]:
            tk.Button(botones, text=b, width=12).pack(side="left", padx=5)

        lista = tk.Listbox(frame, width=60, height=15)
        lista.grid(row=0, column=1)

    # =====================
    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# =====================
# EJECUCIÓN
# =====================
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaVeterinaria(root)
    root.mainloop()

