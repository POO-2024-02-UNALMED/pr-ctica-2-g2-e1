import tkinter as tk

class FieldFrame(tk.Frame):
    def __init__(self, parent, TitleCriteria, Criteria, TitleValues, Values=None, ReadOnly=None):
        super().__init__(parent, bd=2, relief="groove")
        self.criteria = Criteria
        self.entryWidgets = {}

        # Encabezados de columnas
        labelCriteria = tk.Label(self, text=TitleCriteria, font=('Arial', 10, 'bold'))
        labelValues   = tk.Label(self, text=TitleValues,   font=('Arial', 10, 'bold'))
        labelCriteria.grid(row=0, column=0, padx=5, pady=5)
        labelValues.grid(row=0, column=1, padx=5, pady=5)

        # Valores iniciales
        if Values is None:
            Values = ["" for _ in Criteria]
        if ReadOnly is None:
            ReadOnly = []

        # Creación de cada fila (criterio y Entry)
        for i, crit in enumerate(Criteria, start=1):
            lbl = tk.Label(self, text=crit)
            lbl.grid(row=i, column=0, sticky="e", padx=5, pady=2)

            entry = tk.Entry(self)
            entry.insert(0, Values[i-1])
            if crit in ReadOnly:
                entry.config(state="readonly")
            entry.grid(row=i, column=1, sticky="we", padx=5, pady=2)
            self.entryWidgets[crit] = entry

        # Permitir que la columna de valores se expanda
        self.columnconfigure(1, weight=1)

    def getValue(self, Criterion):
        entry = self.entryWidgets.get(Criterion)
        if entry:
            return entry.get()
        return None

    def setValue(self, Criterion, Value):
        entry = self.entryWidgets.get(Criterion)
        if entry:
            if entry.cget("state") == "readonly":
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, Value)
                entry.config(state="readonly")
            else:
                entry.delete(0, tk.END)
                entry.insert(0, Value)
