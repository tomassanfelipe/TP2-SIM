from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QFormLayout, QComboBox, QLabel, QLineEdit, QPushButton, QTextEdit)
from PyQt5.QtGui import QIntValidator
from proceso_numeros import procesar_exponencial, procesar_normal, procesar_uniforme
from generar_tablas import generar_tabla 
from generar_hist import histograma  

class InterfazG(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.form_layout = QFormLayout()

        self.dist_combo = QComboBox(self)
        self.dist_combo.addItems(["Seleccionar Distribución", "Uniforme", "Normal", "Exponencial"])
        self.form_layout.addRow("Seleccionar Distribución:", self.dist_combo)

        # Uniforme
        self.sample_label = QLabel("Valor de la muestra (hasta 1.000.000):")
        self.sample_input = QLineEdit()
        self.sample_input.setValidator(QIntValidator(1, 1000000, self))

        self.lower_label = QLabel("Valor A:")
        self.lower_input = QLineEdit()
        self.lower_input.setValidator(QIntValidator(self))

        self.upper_label = QLabel("Valor B:")
        self.upper_input = QLineEdit()
        self.upper_input.setValidator(QIntValidator(self))

        self.interval_label = QLabel("Número de Intervalos:")
        self.interval_combo = QComboBox(self)
        self.interval_combo.addItems(["10", "15", "20", "25"])

        self.form_layout.addRow(self.sample_label, self.sample_input)
        self.form_layout.addRow(self.lower_label, self.lower_input)
        self.form_layout.addRow(self.upper_label, self.upper_input)
        self.form_layout.addRow(self.interval_label, self.interval_combo)

        # Normal
        self.normal_sample_label = QLabel("Valor de la muestra (hasta 1.000.000):")
        self.normal_sample_input = QLineEdit()
        self.normal_sample_input.setValidator(QIntValidator(1, 1000000, self))

        self.mean_label = QLabel("Valor de la Media:")
        self.mean_input = QLineEdit()
        self.mean_input.setValidator(QIntValidator(self))

        self.deviation_label = QLabel("Valor de la Desviación Estándar:")
        self.deviation_input = QLineEdit()
        self.deviation_input.setValidator(QIntValidator(self))

        self.form_layout.addRow(self.normal_sample_label, self.normal_sample_input)
        self.form_layout.addRow(self.mean_label, self.mean_input)
        self.form_layout.addRow(self.deviation_label, self.deviation_input)

        # Exponencial
        self.expo_sample_label = QLabel("Valor de la muestra (hasta 1.000.000):")
        self.expo_sample_input = QLineEdit()
        self.expo_sample_input.setValidator(QIntValidator(1, 1000000, self))

        self.expo_mean_label = QLabel("Valor de la Media:")
        self.expo_mean_input = QLineEdit()
        self.expo_mean_input.setValidator(QIntValidator(self))

        self.form_layout.addRow(self.expo_sample_label, self.expo_sample_input)
        self.form_layout.addRow(self.expo_mean_label, self.expo_mean_input)

        self.dist_combo.currentIndexChanged.connect(self.actualizar_campos)
        layout.addLayout(self.form_layout)

        # Botones con funcionalidad
        self.boton_generar_numeros = QPushButton("Generar Números", self)
        self.boton_generar_numeros.clicked.connect(self.generar_numeros)
        
        self.boton_mostrar_numeros = QPushButton("Mostrar Números", self)
        self.boton_mostrar_numeros.clicked.connect(self.mostrar_numeros)

        self.boton_histograma = QPushButton("Mostrar Histograma", self)
        self.boton_histograma.clicked.connect(self.mostrar_histograma)
        
        self.boton_tabla = QPushButton("Mostrar Tabla de Frecuencia", self)
        self.boton_tabla.clicked.connect(self.mostrar_tabla_frecuencia)

        layout.addWidget(self.boton_generar_numeros)
        layout.addWidget(self.boton_mostrar_numeros)
        layout.addWidget(self.boton_histograma)
        layout.addWidget(self.boton_tabla)

        self.boton_volver = QPushButton("Volver", self)
        self.boton_volver.clicked.connect(self.volver)
        layout.addWidget(self.boton_volver)
        self.boton_volver.setVisible(False)

        self.resultado_texto = QTextEdit(self)
        self.resultado_texto.setReadOnly(True)
        layout.addWidget(self.resultado_texto)

        self.setLayout(layout)
        self.actualizar_campos()

        # Estilos de la interfaz
        self.setStyleSheet("""
            QWidget {
                font-size: 12pt;
                background-color: #f0f0f0;
            }
            QLabel {
                color: #333;
            }
            QLineEdit, QComboBox {
                background-color: #fff;
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                margin: 5px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #388e3c;
            }
            QComboBox {
                background-color: #e0e0e0;
            }
            QComboBox:hover {
                background-color: #d4d4d4;
            }
            QLineEdit:focus {
                border-color: #4CAF50;
            }
        """)

    # Funciones para manejar la lógica de la interfaz
    def actualizar_campos(self):
        selected_dist = self.dist_combo.currentText() # ve que eligio el user
        
        if hasattr(self, 'numeros'):
            del self.numeros     # limpia resultados 
            
        self.resultado_texto.clear()

        for widget in [         # oculta lo que no sea propio de la pantalla
            self.sample_label, self.sample_input,
            self.lower_label, self.lower_input,
            self.upper_label, self.upper_input,
            self.interval_label, self.interval_combo,
            self.normal_sample_label, self.normal_sample_input,
            self.mean_label, self.mean_input,
            self.deviation_label, self.deviation_input,
            self.expo_sample_label, self.expo_sample_input,
            self.expo_mean_label, self.expo_mean_input
        ]:
            widget.setVisible(False)

        if selected_dist == "Seleccionar Distribución":
            self.boton_volver.setVisible(False)  # oculta el volver si no esta en una pantalla de distribucion
            return

        self.boton_volver.setVisible(True)
        
        # segun la distribucion muestra los campos de entrada que corresponden
        if selected_dist == "Uniforme":
            for widget in [ 
                self.sample_label, self.sample_input,
                self.lower_label, self.lower_input,
                self.upper_label, self.upper_input,
                self.interval_label, self.interval_combo
            ]:
                widget.setVisible(True)

        elif selected_dist == "Normal":
            for widget in [
                self.normal_sample_label, self.normal_sample_input,
                self.mean_label, self.mean_input,
                self.deviation_label, self.deviation_input,
                self.interval_label, self.interval_combo
            ]:
                widget.setVisible(True)

        elif selected_dist == "Exponencial":
            for widget in [
                self.expo_sample_label, self.expo_sample_input,
                self.expo_mean_label, self.expo_mean_input,
                self.interval_label, self.interval_combo
            ]:
                widget.setVisible(True)

    def generar_numeros(self):
        distribucion = self.dist_combo.currentText()  # lee que eligio el usuario
        self.resultado_texto.clear()

        if distribucion == "Uniforme":
            n = self.sample_input.text()
            a = self.lower_input.text()
            b = self.upper_input.text()

            if not n or not a or not b: # valida que esten todos los campos
                self.resultado_texto.setPlainText("Por favor completá todos los campos.")
                return

            try: 
                self.numeros = procesar_uniforme(n, a, b)
                self.resultado_texto.setPlainText("Números generados con éxito.")
            except Exception as e:
                self.resultado_texto.setPlainText(f"Error: {e}")

        elif distribucion == "Normal":
            n = self.normal_sample_input.text()
            media = self.mean_input.text()
            desviacion = self.deviation_input.text()

            if not n or not media or not desviacion: # valida que esten todos los campos
                self.resultado_texto.setPlainText("Por favor completá todos los campos.")
                return

            try:
                self.numeros = procesar_normal(n, media, desviacion)
                self.resultado_texto.setPlainText("Números generados con éxito.")
            except Exception as e:
                self.resultado_texto.setPlainText(f"Error: {e}")

        elif distribucion == "Exponencial":
            n = self.expo_sample_input.text()
            media = self.expo_mean_input.text()

            if not n or not media: # valida que esten todos los campos
                self.resultado_texto.setPlainText("Por favor completá todos los campos.")
                return

            try:
                self.numeros = procesar_exponencial(n, media)
                self.resultado_texto.setPlainText("Números generados con éxito.")
            except Exception as e:
                self.resultado_texto.setPlainText(f"Error: {e}")
        
        else:
            self.resultado_texto.setPlainText("Selecciona una distribucion valida.") # si queres generar numeros y esta en seleccionar distribucion

    def mostrar_numeros(self):
        if not hasattr(self, 'numeros') or not self.numeros: # valida si se generaron numeros
            self.resultado_texto.setPlainText("Primero generá los números.")
            return

        texto_resultado = "Números generados:\n\n"
        texto_resultado += "\n".join(map(str, self.numeros))
        self.resultado_texto.setPlainText(texto_resultado)

    def volver(self):
        self.dist_combo.setCurrentIndex(0)
        self.actualizar_campos()
        self.resultado_texto.clear()

        for input_field in [   # limpia las entradas de texto si toca volver
            self.sample_input, self.lower_input, self.upper_input,
            self.normal_sample_input, self.mean_input, self.deviation_input,
            self.expo_sample_input, self.expo_mean_input
        ]:
            input_field.clear()

        self.interval_combo.setCurrentIndex(0) # resetea los combo box

        if hasattr(self, 'numeros'):  # borra la lista de numeros que se generaron
            del self.numeros
        
    def mostrar_histograma(self):
        try:
            if not hasattr(self, 'numeros') or not self.numeros:  # verifica la creacion de numeros
                self.resultado_texto.setPlainText("Primero generá los números.")
                return

            intervalos = int(self.interval_combo.currentText())  # lee los intervalos seleccionado
        
            histograma(self.numeros, bins=intervalos) # llama a la funcion y le pasa los intervalos que eligio el user

        except Exception as e:
            self.resultado_texto.setPlainText(f"Error al generar histograma: {e}")        
    
    def mostrar_tabla_frecuencia(self):
        try:
            if not hasattr(self, 'numeros') or not self.numeros:  # valida que haya generado numeros
                self.resultado_texto.setPlainText("Primero generá los números.")
                return

            intervalos = self.interval_combo.currentText()  # lee los intervalos seleccionados
            
            tabla = generar_tabla(self.numeros, int(intervalos)) # llama la funcion y genero la tabla
            self.resultado_texto.setPlainText("Tabla de Frecuencia:\n\n" + tabla)

        except Exception as e:
            self.resultado_texto.setPlainText(f"Error al generar tabla: {e}")
    
if __name__ == "__main__":
    app = QApplication([])
    ventana = InterfazG()
    ventana.setWindowTitle("Generador de Distribuciones")
    ventana.resize(600, 700)
    ventana.show()
    app.exec_()