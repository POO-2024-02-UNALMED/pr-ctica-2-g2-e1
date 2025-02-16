# src/UDManager/uiMain/fieldFrame.py

import tkinter as tk

class FieldFrame(tk.Frame):
    def __init__(self, parent, tituloCriterios, criterios, tituloValores, valores=None, habilitado=None):
        super().__init__(parent, bd=2, relief="groove")

        self.criterios = criterios
        self.entry_widgets = {}

        # columnas
        label_criterios = tk.Label(self, text=tituloCriterios, font=('Arial', 10, 'bold'))
        label_valores   = tk.Label(self, text=tituloValores,   font=('Arial', 10, 'bold'))

        label_criterios.grid(row=0, column=0, padx=5, pady=5)
        label_valores.grid(row=0, column=1, padx=5, pady=5)

        # Valores Iniciales
        if valores is None:
            valores = ["" for _ in criterios]
        if habilitado is None:
            habilitado = []

        # Creacion de cada filaa (criterio y entrada)
        for i, crit in enumerate(criterios, start=1):
            lbl = tk.Label(self, text=crit)
            lbl.grid(row=i, column=0, sticky="e", padx=5, pady=2)

            entry = tk.Entry(self)
            entry.insert(0, valores[i-1])
            # Si el criterio está en 'habilitado', lo ponemos en readonly
            if crit in habilitado:
                entry.config(state="readonly")
            entry.grid(row=i, column=1, sticky="we", padx=5, pady=2)

            self.entry_widgets[crit] = entry

        # Permitir que la columna de valores se expanda
        self.columnconfigure(1, weight=1)

    # Retorna el valor ingresado en el campo correspondiente a 'criterio'.
    def getValue(self, criterio):
        entry = self.entry_widgets.get(criterio)
        if entry:
            return entry.get()
        return None

    # Permite asignar un valor programáticamente a un campo.
    def setValue(self, criterio, valor):
        entry = self.entry_widgets.get(criterio)
        if entry:
            #Si estaba readonly, pasarlo a normal para modificarlo y volver a readonly
            if entry.cget("state") == "readonly":
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, valor)
                entry.config(state="readonly")
            else:
                entry.delete(0, tk.END)
                entry.insert(0, valor)