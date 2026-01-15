"""
FileScope - Professional Finder Tool with Glowing Animated Hybrid Progress Bar
"""

import os
import sys
import subprocess
import platform
from PySide6.QtWidgets import (
    QApplication, QWidget, QFileDialog, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QListWidget, QComboBox, QProgressBar,
    QMessageBox
)
from PySide6.QtCore import Qt, QThread, Signal, QTimer
from PySide6.QtGui import QIcon

def resource_path(file_name):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, file_name)

# ---------------------- WORKER THREAD ----------------------
class SearchWorker(QThread):
    found = Signal(str)
    progress = Signal(int)
    finished = Signal()

    def __init__(self, root_path, search_type, query):
        super().__init__()
        self.root_path = root_path
        self.search_type = search_type
        self.query = query.lower()
        self._running = True

    def stop(self):
        self._running = False

    def run(self):
        total_folders = sum(len(dirs) for _, dirs, _ in os.walk(self.root_path))
        total_folders = max(total_folders, 1)
        processed_folders = 0

        for root, dirs, files in os.walk(self.root_path):
            if not self._running:
                break

            # Folder search
            if self.search_type == "Folder Name":
                for d in dirs:
                    if not self._running:
                        break
                    path = os.path.join(root, d)
                    if self.query in d.lower():
                        self.found.emit(path)

            # File search
            for f in files:
                if not self._running:
                    break
                path = os.path.join(root, f)
                try:
                    if self.search_type == "File Name":
                        if self.query in f.lower():
                            self.found.emit(path)
                    elif self.search_type == "Word in File":
                        with open(path, "r", encoding="utf-8", errors="ignore") as file:
                            if self.query in file.read().lower():
                                self.found.emit(path)
                except Exception:
                    pass

            processed_folders += 1
            percent = int((processed_folders / total_folders) * 100)
            self.progress.emit(percent)

        self.finished.emit()

# ---------------------- UI ----------------------
class FinderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(resource_path("logo.ico")))
        self.setWindowTitle("FileScope - Professional Finder Tool")
        self.setMinimumSize(950, 550)
        self.root_path = ""
        self.worker = None
        self.match_count = 0
        self.smooth_value = 0
        self.target_progress = 0
        self.glow_pos = 0
        self.build_ui()

    def build_ui(self):
        main_layout = QVBoxLayout()

        # Title
        title = QLabel("📁 FileScope")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("Title")

        # Controls
        controls = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select root folder...")
        self.path_input.setReadOnly(True)

        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_folder)

        self.search_type = QComboBox()
        self.search_type.addItems(["Folder Name", "File Name", "Word in File"])

        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter search text")
        self.query_input.returnPressed.connect(self.start_search)

        self.search_btn = QPushButton("Search")
        self.search_btn.clicked.connect(self.start_search)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.cancel_search)
        self.cancel_btn.setEnabled(False)

        about_btn = QPushButton("About")
        about_btn.clicked.connect(self.show_about)

        controls.addWidget(self.path_input)
        controls.addWidget(browse_btn)
        controls.addWidget(self.search_type)
        controls.addWidget(self.query_input)
        controls.addWidget(self.search_btn)
        controls.addWidget(self.cancel_btn)
        controls.addWidget(about_btn)

        # Progress bar (start empty)
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setMaximum(100)  # empty at start
        self.progress_bar.setValue(0)

        # Results and counter
        self.results_list = QListWidget()
        self.results_list.itemDoubleClicked.connect(self.open_item)
        self.match_counter_label = QLabel("Matches found: 0")
        self.match_counter_label.setAlignment(Qt.AlignRight)

        main_layout.addWidget(title)
        main_layout.addLayout(controls)
        main_layout.addWidget(self.progress_bar)
        main_layout.addWidget(self.results_list)
        main_layout.addWidget(self.match_counter_label)

        self.setLayout(main_layout)
        self.apply_styles()

        # Timer for smooth animation and glow
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress_smooth)
        self.timer.start(15)  # small interval for smooth movement

    # ---------------------- FUNCTIONS ----------------------
    def show_about(self):
        QMessageBox.information(
            self,
            "About FileScope",
            "🏢 FileScope - Professional File & Folder Finder\n\n"
            "FileScope helps businesses and individuals quickly locate folders, files, "
            "or content inside files. Provides fast, efficient, and intuitive search.\n\n"
            "Key Features:\n"
            "• Search folders by name\n"
            "• Search files by name\n"
            "• Search for words inside files\n"
            "• Smooth hybrid glowing progress bar\n"
            "• Live match counter\n"
            "• Cancelable search\n"
            "• Double-click to open files/folders\n"
            "• Press Enter to search\n\n"
            "🏢 Built by MateTools\n"
            "🌐 Website: https://matetools.gumroad.com"
        )

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.root_path = folder
            self.path_input.setText(folder)

    def start_search(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait()

        if not self.root_path:
            self.results_list.clear()
            self.results_list.addItem("Please select a root folder.")
            return
        query = self.query_input.text().strip()
        if not query:
            self.results_list.clear()
            self.results_list.addItem("Please enter a search query.")
            return

        self.results_list.clear()
        # Start indeterminate glow only when search begins
        self.progress_bar.setMaximum(0)
        self.smooth_value = 0
        self.target_progress = 0
        self.glow_pos = 0
        self.match_count = 0
        self.update_counter()

        self.search_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)

        self.worker = SearchWorker(self.root_path, self.search_type.currentText(), query)
        self.worker.found.connect(self.add_result)
        self.worker.progress.connect(self.set_target_progress)
        self.worker.finished.connect(self.search_finished)
        self.worker.start()

    def add_result(self, path):
        self.results_list.addItem(path)
        self.match_count += 1
        self.update_counter()

    def update_counter(self):
        self.match_counter_label.setText(f"Matches found: {self.match_count}")

    def set_target_progress(self, value):
        if self.progress_bar.maximum() == 0:
            # Switch from indeterminate to real progress
            self.progress_bar.setMaximum(100)
        self.target_progress = value

    def update_progress_smooth(self):
        # Smooth progress animation
        if self.progress_bar.maximum() != 0 and self.smooth_value < self.target_progress:
            self.smooth_value += 1
            self.progress_bar.setValue(self.smooth_value)

        # Glow effect animation
        self.glow_pos = (self.glow_pos + 1) % 200
        gradient_pos = self.glow_pos / 200
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                border: 1px solid #334155;
                border-radius: 6px;
                background-color: #020617;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(
                    x1:{gradient_pos}, y1:0, x2:{gradient_pos+0.2}, y2:0,
                    stop:0 #2563eb, stop:0.5 #60a5fa, stop:1 #2563eb
                );
                border-radius: 6px;
            }}
        """)

    def cancel_search(self):
        if self.worker:
            self.worker.stop()

    def search_finished(self):
        self.search_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(100)
        if self.results_list.count() == 0:
            self.results_list.addItem("No results containing all your search terms were found.")
        self.worker = None

    def open_item(self, item):
        path = item.text()
        if os.path.exists(path):
            try:
                if platform.system() == "Windows":
                    os.startfile(path)
                elif platform.system() == "Darwin":
                    subprocess.Popen(["open", path])
                else:
                    subprocess.Popen(["xdg-open", path])
            except Exception as e:
                print(f"Failed to open {path}: {e}")

    def closeEvent(self, event):
        if self.worker:
            self.worker.stop()
            self.worker.wait()
        event.accept()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #0f172a;
                color: #e5e7eb;
                font-size: 14px;
            }
            QLineEdit, QComboBox, QListWidget {
                background-color: #020617;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 6px;
            }
            QPushButton {
                background-color: #2563eb;
                border: none;
                border-radius: 6px;
                padding: 8px 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
            QPushButton:disabled {
                background-color: #475569;
            }
            QLabel#Title {
                font-size: 22px;
                font-weight: bold;
                margin: 10px 0;
            }
        """)

# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FinderApp()
    window.show()
    sys.exit(app.exec())
