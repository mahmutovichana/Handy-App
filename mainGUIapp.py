import sys
import os
import subprocess
from PySide2.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QDialog, QVBoxLayout, QGridLayout, QWidget
from PySide2.QtGui import QIcon, QFont, QPixmap
from PySide2.QtCore import Qt, QRunnable, QThreadPool
from subprocess import Popen
import pyautogui
from functools import partial

current_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
os.chdir(current_dir)


class ProgramRunner(QRunnable):
    def __init__(self, program, icon):
        super().__init__()
        self.program = program
        self.icon = icon

    def run(self):
        print("Pokrenut je program:", self.program)

        program_files = {
            "obicna_tastatura": os.path.join(current_dir, "main.py"),
            "volume_control": os.path.join(current_dir, "volumeControl.py"),
            "virtual_mouse": os.path.join(current_dir, "virtualMouse.py"),
            "klavijatura_sa_tipkama": os.path.join(current_dir, "mainWithSounds.py")
        }

        if self.program in program_files:
            print("Pokretanje", program_files[self.program])
            python_executable = sys.executable
            command = [python_executable, program_files[self.program], self.icon]
            env = os.environ.copy()
            env["PYTHONPATH"] = ":".join(sys.path)
            Popen(command, env=env)


class ProgramSelectionDialog(QDialog):
    def __init__(self, mainWindow):
        super().__init__()
        self.main_window = mainWindow
        self.setWindowTitle("Handy")
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowIcon(QIcon(os.path.join(current_dir, "HandyLogo.png")))
        self.setFixedSize(600, 275)
        layout = QVBoxLayout()

        program_label = QLabel("Odaberite program:")
        program_label.setStyleSheet("QLabel {font-size: 16px;}")
        layout.addWidget(program_label)

        programs = [
            ("Virtual Keyboard", "obicna_tastatura"),
            ("Volume Control", "volume_control"),
            ("Virtual Mouse", "virtual_mouse"),
            ("Virtual Piano Keyboard", "klavijatura_sa_tipkama")
        ]

        for program_name, program_file_name in programs:
            button = QPushButton(program_name)
            button.clicked.connect(partial(self.select_program, program_file_name))
            button.setStyleSheet(
                "QPushButton { background-color: #4287f5; color: white; border: none; border-radius: 8px; padding: 16px; font-size: 16px;}"
                "QPushButton:hover { background-color: #3275d8; }"
            )
            layout.addWidget(button)

        self.setLayout(layout)
        self.setStyleSheet(mainWindow.styleSheet())

    def select_program(self, program):
        runner = ProgramRunner(program, os.path.join(current_dir, "HandyLogo.png"))
        QThreadPool.globalInstance().start(runner)
        self.accept()
        self.main_window.close()


def main_program(icon):
    print("Glavni program")
    print("Ikona:", icon)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")  # Postavljanje stila aplikacije

    main_window = QMainWindow()
    main_window.setWindowTitle("Handy")
    main_window.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)

    # Postavljanje ikonice prozora
    icon_path = os.path.join(current_dir, "HandyLogo.png")
    app_icon = QIcon(icon_path)
    main_window.setWindowIcon(app_icon)

    central_widget = QWidget()
    main_layout = QGridLayout()
    central_widget.setLayout(main_layout)

    title_label = QLabel("Dobrodošli u Handy aplikaciju!")
    title_label.setAlignment(Qt.AlignCenter)
    title_label.setFont(QFont("Arial", 24, QFont.Bold))
    main_layout.addWidget(title_label, 0, 0, 1, 2)

    image_label = QLabel()
    pixmap = QPixmap(os.path.join(current_dir, "HandyLogo.png"))
    if not pixmap.isNull():
        image_label.setPixmap(pixmap.scaled(300, 350))
    image_label.setAlignment(Qt.AlignCenter)
    main_layout.addWidget(image_label, 1, 1, 2, 1)

    description_label = QLabel(
        "\nHandy je revolucionarna interaktivna aplikacija koja će vas odvesti u svijet futurističkog korisničkog iskustva. "
        "Upotrijebite snagu svog pokreta ruke kako biste kontrolirali različite funkcije i osjetite moć tehnologije na svojoj koži. \n\n"
        "Postanite majstor tipkanja uz besprijekornu virtualnu tastaturu, "
        "podižite ili smanjujte zvuk s lakoćom kroz jednostavne geste, "
        "pomjerajte miša bez dodirivanja računara i zaronite u svijet muzike svirajući virtuelnu klavijaturu. \n\n"
        "Dopustite ruci da postane tvoj moćni alat, istražite sve mogućnosti Handy aplikacije i započnite nevjerojatno putovanje sada!"
    )

    description_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    description_label.setWordWrap(True)
    description_label.setFont(QFont("Arial", 14))
    main_layout.addWidget(description_label, 1, 0, 1, 1)

    main_button = QPushButton("START")
    main_button.setFont(QFont("Arial", 18, QFont.Bold))
    main_button.setStyleSheet(
        "QPushButton { background-color: #4CAF50; color: white; border: none; border-radius: 8px; padding: 16px; }"
        "QPushButton:hover { background-color: #45a049; }")

    program_selection_dialog = ProgramSelectionDialog(main_window)

    def open_program_dialog():
        main_window.close()
        program_selection_dialog.exec_()

    main_button.clicked.connect(open_program_dialog)

    main_layout.addWidget(main_button, 3, 0, 1, 2)

    main_layout.setRowStretch(2, 1)
    main_layout.setColumnStretch(0, 1)
    main_layout.setColumnStretch(1, 1)

    w, h = pyautogui.size()
    main_window.setGeometry(w / 2 - 400, h / 2 - 300, 800, 550)

    main_window.setCentralWidget(central_widget)
    main_window.show()

    main_program(icon_path)

    sys.exit(app.exec_())
