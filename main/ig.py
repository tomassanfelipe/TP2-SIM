from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QFormLayout, QComboBox, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QIntValidator

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Creo el formulario de entrada
        self.form_layout = QFormLayout()

        # ComboBox para seleccionar la distribución
        self.dist_combo = QComboBox(self)
        self.dist_combo.addItems(["Seleccionar Distribución", "Uniforme", "Normal", "Exponencial"])
        self.form_layout.addRow("Seleccionar Distribución:", self.dist_combo)

        # Label y campo para el valor de la muestra (para uniforme y exponencial)
        self.sample_label = QLabel("Valor de la muestra (hasta 1.000.000):")
        self.sample_input = QLineEdit()
        # Validator para solo números
        self.sample_input.setValidator(QIntValidator(1, 1000000, self))

        # Label y campo para el valor inferior (para uniforme)
        self.lower_label = QLabel("Valor Inferior A:")
        self.lower_input = QLineEdit()
        self.lower_input.setValidator(QIntValidator(self))

        # Label y campo para el valor superior (para uniforme)
        self.upper_label = QLabel("Valor Superior B:")
        self.upper_input = QLineEdit()
        self.upper_input.setValidator(QIntValidator(self))

        # Label y campo para el número de intervalos (para uniforme y exponencial)
        self.interval_label = QLabel("Número de Intervalos:")
        self.interval_combo = QComboBox(self)
        self.interval_combo.addItems(["10", "15", "20", "25"])

        # Agregar los campos al formulario
        self.form_layout.addRow(self.sample_label, self.sample_input)
        self.form_layout.addRow(self.lower_label, self.lower_input)
        self.form_layout.addRow(self.upper_label, self.upper_input)
        self.form_layout.addRow(self.interval_label, self.interval_combo)

        # Nuevos campos para la distribución normal
        self.normal_sample_label = QLabel("Valor de la muestra (hasta 1.000.000):")
        self.normal_sample_input = QLineEdit()
        self.normal_sample_input.setValidator(QIntValidator(1, 1000000, self))

        self.mean_label = QLabel("Valor de la Media:")
        self.mean_input = QLineEdit()
        self.mean_input.setValidator(QIntValidator(self))

        self.deviation_label = QLabel("Valor de la Desviación Estándar:")
        self.deviation_input = QLineEdit()
        self.deviation_input.setValidator(QIntValidator(self))

        # Nuevos campos para la distribución exponencial
        self.expo_sample_label = QLabel("Valor de la muestra (hasta 1.000.000):")
        self.expo_sample_input = QLineEdit()
        self.expo_sample_input.setValidator(QIntValidator(1, 1000000, self))

        self.expo_mean_label = QLabel("Valor de la Media:")
        self.expo_mean_input = QLineEdit()
        self.expo_mean_input.setValidator(QIntValidator(self))

        # Agregar los nuevos campos para distribución exponencial
        self.form_layout.addRow(self.expo_sample_label, self.expo_sample_input)
        self.form_layout.addRow(self.expo_mean_label, self.expo_mean_input)

        # Agregar los nuevos campos para distribución normal
        self.form_layout.addRow(self.normal_sample_label, self.normal_sample_input)
        self.form_layout.addRow(self.mean_label, self.mean_input)
        self.form_layout.addRow(self.deviation_label, self.deviation_input)

        # Al cambiar la selección, actualizar los campos
        self.dist_combo.currentIndexChanged.connect(self.actualizar_campos)

        # Agregar el formulario al layout principal
        layout.addLayout(self.form_layout)

        # Botones
        self.boton_mostrar_numeros = QPushButton("Mostrar Números", self)
        self.boton_histograma = QPushButton("Mostrar Histograma", self)
        self.boton_tabla = QPushButton("Mostrar Tabla de Frecuencia", self)

        # Agregar los botones al layout
        layout.addWidget(self.boton_mostrar_numeros)
        layout.addWidget(self.boton_histograma)
        layout.addWidget(self.boton_tabla)

        # Botón Volver
        self.boton_volver = QPushButton("Volver", self)
        self.boton_volver.clicked.connect(self.volver)

        # Agregar el botón Volver al layout, pero estará oculto inicialmente
        layout.addWidget(self.boton_volver)
        self.boton_volver.setVisible(False)

        self.setLayout(layout)

        # Inicialmente, oculta todos los campos
        self.actualizar_campos()

        # Estilos CSS
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

    def actualizar_campos(self):
        selected_dist = self.dist_combo.currentText()

        # Esconde todos los campos por defecto
        self.sample_label.setVisible(False)
        self.sample_input.setVisible(False)
        self.lower_label.setVisible(False)
        self.lower_input.setVisible(False)
        self.upper_label.setVisible(False)
        self.upper_input.setVisible(False)
        self.interval_label.setVisible(False)
        self.interval_combo.setVisible(False)

        self.normal_sample_label.setVisible(False)
        self.normal_sample_input.setVisible(False)
        self.mean_label.setVisible(False)
        self.mean_input.setVisible(False)
        self.deviation_label.setVisible(False)
        self.deviation_input.setVisible(False)

        self.expo_sample_label.setVisible(False)
        self.expo_sample_input.setVisible(False)
        self.expo_mean_label.setVisible(False)
        self.expo_mean_input.setVisible(False)

        # Si no se ha seleccionado una distribución, no mostrar nada
        if selected_dist == "Seleccionar Distribución":
            self.boton_volver.setVisible(False)
            return

        if selected_dist == "Uniforme":
            # Mostrar solo los campos específicos para la distribución uniforme
            self.sample_label.setVisible(True)
            self.sample_input.setVisible(True)
            self.lower_label.setVisible(True)
            self.lower_input.setVisible(True)
            self.upper_label.setVisible(True)
            self.upper_input.setVisible(True)
            self.interval_label.setVisible(True)
            self.interval_combo.setVisible(True)

        elif selected_dist == "Normal":
            # Mostrar los campos específicos para la distribución normal
            self.normal_sample_label.setVisible(True)
            self.normal_sample_input.setVisible(True)
            self.mean_label.setVisible(True)
            self.mean_input.setVisible(True)
            self.deviation_label.setVisible(True)
            self.deviation_input.setVisible(True)
            self.interval_label.setVisible(True)
            self.interval_combo.setVisible(True)

        elif selected_dist == "Exponencial":
            # Mostrar los campos específicos para la distribución exponencial
            self.expo_sample_label.setVisible(True)
            self.expo_sample_input.setVisible(True)
            self.expo_mean_label.setVisible(True)
            self.expo_mean_input.setVisible(True)
            self.interval_label.setVisible(True)
            self.interval_combo.setVisible(True)

        # Mostrar el botón Volver cuando se selecciona una distribución
        self.boton_volver.setVisible(True)

    def volver(self):
        # Resetear todos los campos y volver al estado inicial
        self.dist_combo.setCurrentIndex(0)
        self.actualizar_campos()

if __name__ == "__main__":
    app = QApplication([])  
    ventana = MiVentana()
    ventana.show()
    app.exec_()
