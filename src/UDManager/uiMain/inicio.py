# src/UDManager/uiMain/inicio.py

import os
import math
import tkinter as tk
from tkinter import messagebox
from src.UDManager.uiMain.app import Application
from PIL import Image, ImageTk

class InicioWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        # Configuración de la ventana y estilo
        self.configure(bg="#ecf0f1")
        self.title("Inicio - UDManager")
        self.geometry("800x600")
        self.setupMenu()

        # Tamaño base para el escalado
        self.BASE_WIDTH = 800
        self.BASE_HEIGHT = 600

        absoluteBase = r"uiMain"

        # MARCO PRINCIPAL
        self.mainFrame = tk.Frame(self, bg="#ecf0f1")
        self.mainFrame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Dividir en dos bloques: izquierda (P1) y derecha (P2)
        p1Frame = tk.Frame(self.mainFrame, bg="white", bd=2, relief="groove")
        p1Frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        p2Frame = tk.Frame(self.mainFrame, bg="white", bd=2, relief="groove")
        p2Frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.mainFrame.grid_columnconfigure(0, weight=1)
        self.mainFrame.grid_columnconfigure(1, weight=1)
        self.mainFrame.grid_rowconfigure(0, weight=1)

        # P1 se divide en P3 (superior) y P4 (inferior)
        p3Frame = tk.Frame(p1Frame, bg="white", bd=2, relief="ridge")
        p3Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        p4Frame = tk.Frame(p1Frame, bg="white", bd=2, relief="ridge")
        p4Frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # P3: Mensaje de bienvenida
        welcome_text = (
            "Bienvenido a UDManager\n\n"
            "Aquí podrás realizar:\n"
            "   • Reservas de recintos deportivos\n"
            "   • Torneos personalizados\n"
            "   • Eventos no deportivos en las instalaciones\n"
            "   • Inscripciones a grupos de deportes formativos\n"
            "   • Pagos relacionados con actividades de la Unidad Deportiva"
        )
        welcomeLabel = tk.Label(p3Frame, text=welcome_text,
                                font=("Helvetica", 16, "bold"),
                                fg="#2c3e50", bg="white",
                                justify="center", anchor="center")
        welcomeLabel.pack(padx=10, pady=10, expand=True)

        # P4: Botón "Ingresar al Sistema" con imagen y texto
        try:
            self.image1 = tk.PhotoImage(file="image1.png")
            print("Cargada image1.png")
        except Exception as e:
            print("Error al cargar image1.png:", e)
            self.image1 = tk.PhotoImage(width=200, height=150)
        try:
            self.image2 = tk.PhotoImage(file="image2.png")
            print("Cargada image2.png")
        except Exception as e:
            print("Error al cargar image2.png:", e)
            self.image2 = tk.PhotoImage(width=200, height=150)
        try:
            self.image3 = tk.PhotoImage(file="image3.png")
            print("Cargada image3.png")
        except Exception as e:
            print("Error al cargar image3.png:", e)
            self.image3 = tk.PhotoImage(width=200, height=150)
        try:
            self.image4 = tk.PhotoImage(file="image4.png")
            print("Cargada image4.png")
        except Exception as e:
            print("Error al cargar image4.png:", e)
            self.image4 = tk.PhotoImage(width=200, height=150)
        try:
            self.image5 = tk.PhotoImage(file="image5.png")
            print("Cargada image5.png")
        except Exception as e:
            print("Error al cargar image5.png:", e)
            self.image5 = tk.PhotoImage(width=200, height=150)
        self.originalImageList = [self.image1, self.image2, self.image3, self.image4, self.image5]
        self.imageList = self.originalImageList[:]
        self.currentImageIndex = 0

        self.enterButton = tk.Button(p4Frame,
                                     text="Ingresar al Sistema",
                                     image=self.imageList[self.currentImageIndex],
                                     compound="top",
                                     font=("Helvetica", 14, "bold"),
                                     fg="white",
                                     bg="#3498db",
                                     activebackground="#2980b9",
                                     relief="flat",
                                     bd=0,
                                     highlightthickness=0,
                                     command=self.enterSystem)
        self.enterButton.pack(expand=True, anchor="center", pady=10)
        self.enterButton.bind("<Enter>", self.onImageEnter)
        self.enterButton.bind("<Leave>", self.onImageLeave)

        # P2: Dividido en P5 (superior) y P6 (inferior)
        p5Frame = tk.Frame(p2Frame, bg="white", bd=2, relief="ridge")
        p5Frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        p6Frame = tk.Frame(p2Frame, bg="white", bd=2, relief="ridge")
        p6Frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True, padx=10, pady=10)
        p6Frame.grid_columnconfigure(0, weight=1)
        p6Frame.grid_columnconfigure(1, weight=1)
        p6Frame.grid_rowconfigure(0, weight=1)
        p6Frame.grid_rowconfigure(1, weight=1)

        # P5: Cargar hojas de vida (CV) desde archivos de texto en la carpeta cvs
        parentDir = os.path.dirname(absoluteBase)
        cvDir = os.path.join(parentDir, "cvs")
        self.cv1 = self.readFile(os.path.join(cvDir, "cv1.txt"))
        self.cv2 = self.readFile(os.path.join(cvDir, "cv2.txt"))
        self.cv3 = self.readFile(os.path.join(cvDir, "cv3.txt"))
        self.cv4 = self.readFile(os.path.join(cvDir, "cv4.txt"))
        self.resumeList = [self.cv1, self.cv2, self.cv3, self.cv4]
        for i in range(len(self.resumeList)):
            if not self.resumeList[i]:
                self.resumeList[i] = "CV no disponible."
        self.currentResumeIndex = 0
        self.resumeLabel = tk.Label(p5Frame,
                                    text=self.resumeList[self.currentResumeIndex],
                                    font=("Helvetica", 12),
                                    bg="white",
                                    fg="#2c3e50",
                                    wraplength=300,
                                    justify="left")
        self.resumeLabel.pack(padx=10, pady=10)
        self.resumeLabel.bind("<Enter>", self.changeResume)

        # P6: Cargar imágenes de desarrolladores
        self.originalDevImages = self.loadDevImagesManual(0, absoluteBase)
        self.devImages = self.originalDevImages[:]
        self.photoLabel1 = tk.Label(p6Frame, image=self.devImages[0], bg="white")
        self.photoLabel1.grid(row=0, column=0, padx=5, pady=5)
        self.photoLabel2 = tk.Label(p6Frame, image=self.devImages[1], bg="white")
        self.photoLabel2.grid(row=0, column=1, padx=5, pady=5)
        self.photoLabel3 = tk.Label(p6Frame, image=self.devImages[2], bg="white")
        self.photoLabel3.grid(row=1, column=0, padx=5, pady=5)
        self.photoLabel4 = tk.Label(p6Frame, image=self.devImages[3], bg="white")
        self.photoLabel4.grid(row=1, column=1, padx=5, pady=5)
        self.photoLabels = [self.photoLabel1, self.photoLabel2, self.photoLabel3, self.photoLabel4]

        self.mainFrame.bind("<Configure>", self.on_resize)

    def readFile(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error al leer {filepath}: {e}")
            return ""

    def setupMenu(self):
        try:
            menuBar = tk.Menu(self)
            inicioMenu = tk.Menu(menuBar, tearoff=0)
            inicioMenu.add_command(label="Salir", command=self.quit)
            inicioMenu.add_command(label="Descripción del sistema", command=self.showDescription)
            menuBar.add_cascade(label="Inicio", menu=inicioMenu)
            self.config(menu=menuBar)
        except Exception as e:
            print("Error en setupMenu:", e)

    def onImageEnter(self, event):
        self.currentImageIndex = (self.currentImageIndex + 1) % len(self.imageList)
        self.enterButton.config(image=self.imageList[self.currentImageIndex])

    def onImageLeave(self, event):
        pass

    def changeResume(self, event):
        self.currentResumeIndex = (self.currentResumeIndex + 1) % len(self.resumeList)
        self.resumeLabel.config(text=self.resumeList[self.currentResumeIndex])
        if self.currentResumeIndex == 0:
            newDevImages = self.loadDevImagesManual(0, "uiMain")
        elif self.currentResumeIndex == 1:
            newDevImages = self.loadDevImagesManual(1, "uiMain")
        elif self.currentResumeIndex == 2:
            newDevImages = self.loadDevImagesManual(2, "uiMain")
        elif self.currentResumeIndex == 3:
            newDevImages = self.loadDevImagesManual(3, "uiMain")
        else:
            newDevImages = [tk.PhotoImage(width=100, height=100)] * 4

        self.devImages = newDevImages[:]
        self.photoLabel1.config(image=self.devImages[0])
        self.photoLabel1.image = self.devImages[0]
        self.photoLabel2.config(image=self.devImages[1])
        self.photoLabel2.image = self.devImages[1]
        self.photoLabel3.config(image=self.devImages[2])
        self.photoLabel3.image = self.devImages[2]
        self.photoLabel4.config(image=self.devImages[3])
        self.photoLabel4.image = self.devImages[3]
        self.on_resize(None)

    def loadDevImagesManual(self, developerIndex, absoluteBase):
        if developerIndex == 0:
            try:
                dev1_1 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev1_1.png"))
            except Exception as e:
                print("Error al cargar dev1_1.png:", e)
                dev1_1 = tk.PhotoImage(width=100, height=100)
            try:
                dev1_2 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev1_2.png"))
            except Exception as e:
                print("Error al cargar dev1_2.png:", e)
                dev1_2 = tk.PhotoImage(width=100, height=100)
            try:
                dev1_3 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev1_3.png"))
            except Exception as e:
                print("Error al cargar dev1_3.png:", e)
                dev1_3 = tk.PhotoImage(width=100, height=100)
            try:
                dev1_4 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev1_4.png"))
            except Exception as e:
                print("Error al cargar dev1_4.png:", e)
                dev1_4 = tk.PhotoImage(width=100, height=100)
            return [dev1_1, dev1_2, dev1_3, dev1_4]
        elif developerIndex == 1:
            try:
                dev2_1 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev2_1.png"))
            except Exception as e:
                print("Error al cargar dev2_1.png:", e)
                dev2_1 = tk.PhotoImage(width=100, height=100)
            try:
                dev2_2 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev2_2.png"))
            except Exception as e:
                print("Error al cargar dev2_2.png:", e)
                dev2_2 = tk.PhotoImage(width=100, height=100)
            try:
                dev2_3 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev2_3.png"))
            except Exception as e:
                print("Error al cargar dev2_3.png:", e)
                dev2_3 = tk.PhotoImage(width=100, height=100)
            try:
                dev2_4 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev2_4.png"))
            except Exception as e:
                print("Error al cargar dev2_4.png:", e)
                dev2_4 = tk.PhotoImage(width=100, height=100)
            return [dev2_1, dev2_2, dev2_3, dev2_4]
        elif developerIndex == 2:
            try:
                dev3_1 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev3_1.png"))
            except Exception as e:
                print("Error al cargar dev3_1.png:", e)
                dev3_1 = tk.PhotoImage(width=100, height=100)
            try:
                dev3_2 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev3_2.png"))
            except Exception as e:
                print("Error al cargar dev3_2.png:", e)
                dev3_2 = tk.PhotoImage(width=100, height=100)
            try:
                dev3_3 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev3_3.png"))
            except Exception as e:
                print("Error al cargar dev3_3.png:", e)
                dev3_3 = tk.PhotoImage(width=100, height=100)
            try:
                dev3_4 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev3_4.png"))
            except Exception as e:
                print("Error al cargar dev3_4.png:", e)
                dev3_4 = tk.PhotoImage(width=100, height=100)
            return [dev3_1, dev3_2, dev3_3, dev3_4]
        elif developerIndex == 3:
            try:
                dev4_1 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev4_1.png"))
            except Exception as e:
                print("Error al cargar dev4_1.png:", e)
                dev4_1 = tk.PhotoImage(width=100, height=100)
            try:
                dev4_2 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev4_2.png"))
            except Exception as e:
                print("Error al cargar dev4_2.png:", e)
                dev4_2 = tk.PhotoImage(width=100, height=100)
            try:
                dev4_3 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev4_3.png"))
            except Exception as e:
                print("Error al cargar dev4_3.png:", e)
                dev4_3 = tk.PhotoImage(width=100, height=100)
            try:
                dev4_4 = tk.PhotoImage(file=os.path.join(absoluteBase, "dev4_4.png"))
            except Exception as e:
                print("Error al cargar dev4_4.png:", e)
                dev4_4 = tk.PhotoImage(width=100, height=100)
            return [dev4_1, dev4_2, dev4_3, dev4_4]
        else:
            blank = tk.PhotoImage(width=100, height=100)
            return [blank, blank, blank, blank]

    def on_resize(self, event):
        from PIL import Image, ImageTk

        new_w = self.winfo_width()
        new_h = self.winfo_height()
        scale = min(new_w / self.BASE_WIDTH, new_h / self.BASE_HEIGHT)

        btn_files = ["image1.png", "image2.png", "image3.png", "image4.png", "image5.png"]
        new_image_list = []
        for i, file in enumerate(btn_files):
            try:
                pil_img = Image.open(file)
            except Exception as e:
                print(f"Error al abrir {file}: {e}")
                pil_img = Image.new("RGB", (200, 150), "white")
            orig_size = pil_img.size
            new_size = (max(1, int(orig_size[0] * scale)), max(1, int(orig_size[1] * scale)))
            resized = pil_img.resize(new_size, Image.LANCZOS)
            new_image_list.append(ImageTk.PhotoImage(resized))
        self.imageList = new_image_list
        self.enterButton.config(image=self.imageList[self.currentImageIndex])
        self.enterButton.image = self.imageList[self.currentImageIndex]

        dev_index = self.currentResumeIndex
        dev_files = [f"dev{dev_index+1}_{i}.png" for i in range(1, 5)]
        new_dev_images = []
        for i, file in enumerate(dev_files):
            try:
                pil_img = Image.open(file)
            except Exception as e:
                print(f"Error al abrir {file}: {e}")
                pil_img = Image.new("RGB", (100, 100), "white")
            orig_size = pil_img.size
            new_size = (max(1, int(orig_size[0] * scale)), max(1, int(orig_size[1] * scale)))
            resized = pil_img.resize(new_size, Image.LANCZOS)
            new_dev_images.append(ImageTk.PhotoImage(resized))
        self.devImages = new_dev_images
        self.photoLabel1.config(image=self.devImages[0])
        self.photoLabel1.image = self.devImages[0]
        self.photoLabel2.config(image=self.devImages[1])
        self.photoLabel2.image = self.devImages[1]
        self.photoLabel3.config(image=self.devImages[2])
        self.photoLabel3.image = self.devImages[2]
        self.photoLabel4.config(image=self.devImages[3])
        self.photoLabel4.image = self.devImages[3]

    def showDescription(self):
        description = (
            "El sistema de gestión permite editar y consultar la información del sistema.\n"
            "Incluye funcionalidades para manejar eventos, inscripciones, pagos, reservas y torneos."
        )
        messagebox.showinfo("Descripción del sistema", description)

    def enterSystem(self):
        self.destroy()
        from src.UDManager.uiMain.app import Application
        app = Application()
        app.mainloop()

if __name__ == "__main__":
    inicioWindow = InicioWindow()
    inicioWindow.originalImageList = inicioWindow.imageList[:]
    inicioWindow.originalDevImages = inicioWindow.devImages[:]
    inicioWindow.mainloop()
