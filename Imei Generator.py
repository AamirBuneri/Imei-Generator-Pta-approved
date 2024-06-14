import sys
import random
import pyperclip
import webbrowser
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QGroupBox, QDesktopWidget
from PyQt5.QtCore import Qt

class IMEIGenerator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main layout
        vbox = QVBoxLayout()

        # Model selection
        model_groupbox = QGroupBox("Select Phone Model")
        hbox_model = QHBoxLayout()
        self.model_label = QLabel("Model:")
        hbox_model.addWidget(self.model_label)
        self.models_dropdown = QComboBox()
        self.models_dropdown.addItem("Select Model")
        for model in phone_models:
            self.models_dropdown.addItem(model[0])
        hbox_model.addWidget(self.models_dropdown)
        model_groupbox.setLayout(hbox_model)
        vbox.addWidget(model_groupbox)

        # Quantity input
        quantity_groupbox = QGroupBox("Enter Quantity")
        hbox_quantity = QHBoxLayout()
        self.quantity_label = QLabel("Quantity:")
        hbox_quantity.addWidget(self.quantity_label)
        self.quantity_entry = QLineEdit()
        hbox_quantity.addWidget(self.quantity_entry)
        quantity_groupbox.setLayout(hbox_quantity)
        vbox.addWidget(quantity_groupbox)

        # Custom IMEI input
        custom_imei_groupbox = QGroupBox("Enter Custom IMEI")
        hbox_custom_imei = QHBoxLayout()
        self.imei_label = QLabel("IMEI:")
        hbox_custom_imei.addWidget(self.imei_label)
        self.imei_entry = QLineEdit()
        hbox_custom_imei.addWidget(self.imei_entry)
        custom_imei_groupbox.setLayout(hbox_custom_imei)
        vbox.addWidget(custom_imei_groupbox)

        # Generate buttons
        hbox_buttons = QHBoxLayout()
        self.generate_button = QPushButton("Generate IMEI", self)
        self.generate_button.clicked.connect(self.generate_imei)
        hbox_buttons.addWidget(self.generate_button)
        self.custom_generate_button = QPushButton("Generate Custom IMEI", self)
        self.custom_generate_button.clicked.connect(self.generate_custom_imei)
        hbox_buttons.addWidget(self.custom_generate_button)
        vbox.addLayout(hbox_buttons)

        # Output text area
        self.output_text = QTextEdit()
        vbox.addWidget(self.output_text)

        # Additional website button
        hbox_extra_buttons = QHBoxLayout()
        additional_website_button = QPushButton("Mobiles Number Details Finder")
        additional_website_button.clicked.connect(self.open_random_website)
        hbox_extra_buttons.addWidget(additional_website_button)
        vbox.addLayout(hbox_extra_buttons)

        # About and website buttons
        hbox_extra_buttons = QHBoxLayout()
        about_button = QPushButton("About")
        about_button.clicked.connect(self.show_about)
        hbox_extra_buttons.addWidget(about_button)
        website_button = QPushButton("Open Website")
        website_button.clicked.connect(self.open_website)
        hbox_extra_buttons.addWidget(website_button)
        vbox.addLayout(hbox_extra_buttons)

        self.setLayout(vbox)
        self.setWindowTitle("IMEI Generator By Aamir Buneri")

        self.setStyleSheet("""
            QWidget {
                background-color: #222;
                color: #fff;
            }
            QGroupBox {
                border: 1px solid #555;
                border-radius: 5px;
            }
            QLabel {
                color: #fff;
                font-size: 14px;
            }
            QLineEdit {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 5px;
                color: #fff;
                padding: 2px;
                font-size: 14px;
            }
            QTextEdit {
                background-color: #333;
                border: 1px solid #555;
                border-radius: 5px;
                color: #fff;
                padding: 2px;
                font-size: 16px; /* Increased font size */
            }
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #4CAF50, stop: 1 #258B7B);
                border: none;
                border-radius: 10px;
                padding: 10px 20px;
                color: white;
            }
            QPushButton:hover {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #258B7B, stop: 1 #4CAF50);
            }
        """)

        # Set the window size
        self.resize(800, 700) # Increased height
        # Center the window
        self.center()

    def center(self):
        # Get the screen geometry
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        # Move the window center to the screen center
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def generate_imei(self):
        selected_model_index = self.models_dropdown.currentIndex()
        if selected_model_index == 0:
            self.output_text.append("Please select a model.")
            return
        
        selected_model = phone_models[selected_model_index - 1]
        model_name = selected_model[0]
        imei_prefix = selected_model[1]
        
        try:
            quantity = int(self.quantity_entry.text())
        except ValueError:
            self.output_text.append("Please enter a valid quantity.")
            return
        
        self.output_text.clear()  
        self.output_text.append(f"Generating {quantity} IMEI numbers for {model_name}:\n")
        
        imei_list = []
        for j in range(1, quantity + 1):
            random_digits = ''.join(str(random.randint(0, 9)) for _ in range(4))
            imei = imei_prefix[:-4] + random_digits
            self.output_text.append(imei)
            imei_list.append(imei)

        # Auto-save generated IMEI numbers to a text file
        self.save_imei_to_file(model_name, imei_list)

    def generate_custom_imei(self):
        imei = self.imei_entry.text()
        try:
            int(imei)  # Check if IMEI is a valid number
        except ValueError:
            self.output_text.append("Please enter a valid 15-digit IMEI.")
            return
        
        quantity = self.quantity_entry.text()
        try:
            quantity = int(quantity)
        except ValueError:
            self.output_text.append("Please enter a valid quantity.")
            return
        
        self.output_text.clear()  
        self.output_text.append(f"Generating {quantity} IMEI numbers based on the custom IMEI:\n")
        
        imei_list = []
        for _ in range(quantity):
            random_digits = ''.join(str(random.randint(0, 9)) for _ in range(4))
            new_imei = imei[:-4] + random_digits
            self.output_text.append(new_imei)
            imei_list.append(new_imei)

        # Auto-save generated IMEI numbers to a text file
        self.save_imei_to_file("Custom_IMEI", imei_list)

    def save_imei_to_file(self, model_name, imei_list):
        filename = f"{model_name.replace(' ', '_')}_IMEI.txt"
        header = f"Programmer: Aamir Buneri\nMobile Number: +923107591374\nEmail: aamirbuneri1046@gmail.com\n\n"
        with open(filename, 'w') as f:
            f.write(header)
            f.write("\n".join(imei_list))

    def show_about(self):
        about_text = "This application is developed by Aamir Buneri.\nContact: aamirbuneri1046@gmail.com"
        self.output_text.append(about_text)

    def open_website(self):
        webbrowser.open("https://dirbs.pta.gov.pk/", new=2)

    def open_random_website(self):
        websites = [
            "https://www.example.com",
            "https://www.randomwebsite.com",
            "https://www.anotherexample.com"
        ]
        random_website = random.choice(websites)
        webbrowser.open(random_website, new=2)

# Define phone models and IMEI prefixes
phone_models = [
    ("Select Model", ""),
    ("Spark Go 6", "35446262244952"),
    ("Nokia 106", "35939224912282"),
    ("Lava Iris 810", "35608507762070"),
    ("Samsung J7", "35450309224848"),
    ("Vivo S1 Pro", "8612660479806"),
    ("Infinix Smart 4", "35597511486703"),
    ("Oppo Cph2269", "86477205795395"),
    ("Apple iPhone 6S Plus (A1687)", "35328607262722"),
    ("Vivo Y15s", "86446505708183"),  # Added Vivo Y15s model
    ("Galaxy A03", "35645273050872"),
    ("TECNO CAMON 30", "35745068047794"),
    ("QMobile 3G Lite", "35583407008957"),
    ("Galaxy S10+", "35465310690811"),
    ("Samsung SM-B310E", "35350307456514"),
    ("Nokia 3310 DS", "35733008057872"),
    ("Huawei E5330s-2 Device", "86898802915890"),
    ("ZTE MF920U DEVICE", "86603405138323"),
    ("Huawei E5573 Device", "86135003450191"),
    ("Redmi 13C", "86105207704408"),
    ("X Mobile 1000 Music", "35343663042218"),
    ("CPH1923", "86323504030343"),
    ("MF673 Wifi Device", "35754308114149"),
    ("Mf 937 Jazz", "86388105066349"),
    ("A25", "35922374299277"),
    ("Xmobile Power Plus", "35504617012601"),
    ("Hello tech 7", "35943957017154")
]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    imei_generator = IMEIGenerator()
    imei_generator.show()
    sys.exit(app.exec_())
