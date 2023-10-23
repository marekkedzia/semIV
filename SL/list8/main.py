import csv
import sys
import tempfile

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QLabel, QSlider, QLineEdit, QWidget, QPushButton, QVBoxLayout, QTableWidget, \
    QSplitter, QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QApplication, QHeaderView
import folium


class LogViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.details_label = QLabel()
        self.statistics_label = QLabel()

        def create_status_bar():
            self.statusBar().showMessage('No data to display')

        def create_menubar():
            menubar = self.menuBar()
            file_menu = menubar.addMenu('File')
            edit_menu = menubar.addMenu('Edit')
            view_menu = menubar.addMenu('View')
            help_menu = menubar.addMenu('Help')

            open_file_action = file_menu.addAction('Open')
            open_file_action.triggered.connect(self.open_file)

            copy_action = edit_menu.addAction('Copy')
            paste_action = edit_menu.addAction('Paste')
            copy_action.triggered.connect(self.copy_data)
            paste_action.triggered.connect(self.paste_data)

            toggle_columns_action = view_menu.addAction('Toggle Columns')
            toggle_columns_action.triggered.connect(self.toggle_columns)

            about_action = help_menu.addAction('About')
            about_action.triggered.connect(self.show_about)

        def create_central_widget():
            self.central_widget = QWidget()
            self.setCentralWidget(self.central_widget)
            self.layout = QVBoxLayout(self.central_widget)
            self.splitter = QSplitter(Qt.Orientation.Horizontal)

        def create_table_widget():
            self.table_widget = QTableWidget()
            self.splitter.addWidget(self.table_widget)

            self.table_widget.setShowGrid(True)
            self.table_widget.setAlternatingRowColors(True)
            self.table_widget.horizontalHeader().setSectionResizeMode(
                QHeaderView.ResizeMode.Stretch)

            self.table_widget.setMaximumWidth(800)
            self.table_widget.cellClicked.connect(self.cell_clicked)
            font_color = QColor(255, 255, 255)
            palette = self.table_widget.palette()
            palette.setColor(QPalette.ColorRole.Text, font_color)
            self.table_widget.setPalette(palette)
            self.load_initial_data()

            self.layout.addWidget(self.splitter)

        def create_details_and_statistics_widget():
            self.details_and_statistics_widget = QWidget()
            self.details_and_statistics_layout = QVBoxLayout(self.details_and_statistics_widget)
            self.splitter.addWidget(self.details_and_statistics_widget)

            self.details_and_statistics_layout.addWidget(self.details_label)

            self.details_and_statistics_layout.addWidget(self.statistics_label)

        def create_search_widget():
            self.search_widget = QWidget()
            self.search_layout = QVBoxLayout(self.search_widget)
            self.details_and_statistics_layout.addWidget(self.search_widget)

            self.search_fields_layout = QVBoxLayout()
            self.search_ship_name_input = QLineEdit()
            self.search_ship_name_input.setPlaceholderText("Nazwa statku")
            self.search_fields_layout.addWidget(self.search_ship_name_input)
            self.search_commander_input = QLineEdit()
            self.search_commander_input.setPlaceholderText("Dowódca")
            self.search_fields_layout.addWidget(self.search_commander_input)
            self.search_uboat_input = QLineEdit()
            self.search_uboat_input.setPlaceholderText("Nazwa U-Boota")
            self.search_fields_layout.addWidget(self.search_uboat_input)
            self.search_layout.addLayout(self.search_fields_layout)

            self.search_button = QPushButton('Wyszukaj')
            self.search_button.clicked.connect(self.search)
            self.search_layout.addWidget(self.search_button)

        def create_tonnage_sliders():
            tonnage_max = 15000
            self.tonnage_slider_layout = QVBoxLayout()

            self.tonnage_min_label = QLabel("Tonnage from: 0")
            self.tonnage_slider_layout.addWidget(self.tonnage_min_label)

            self.tonnage_min_slider = QSlider(Qt.Orientation.Horizontal)
            self.tonnage_min_slider.setMinimum(0)
            self.tonnage_min_slider.setMaximum(tonnage_max)
            self.tonnage_min_slider.valueChanged.connect(self.tonnage_slider_changed)
            self.tonnage_slider_layout.addWidget(self.tonnage_min_slider)

            self.tonnage_max_label = QLabel(f"Tonnage to: {tonnage_max}")
            self.tonnage_slider_layout.addWidget(self.tonnage_max_label)

            self.tonnage_max_slider = QSlider(Qt.Orientation.Horizontal)
            self.tonnage_max_slider.setMinimum(0)
            self.tonnage_max_slider.setMaximum(tonnage_max)
            self.tonnage_max_slider.setValue(tonnage_max)
            self.tonnage_max_slider.valueChanged.connect(self.tonnage_slider_changed)
            self.tonnage_slider_layout.addWidget(self.tonnage_max_slider)

            self.search_layout.addLayout(self.tonnage_slider_layout)

            self.splitter.setSizes([800, 600])

        def init_ui():
            create_status_bar()
            create_menubar()
            create_central_widget()
            create_table_widget()
            create_details_and_statistics_widget()
            create_search_widget()
            create_tonnage_sliders()

        init_ui()

        self.setWindowTitle("Sunk merchants ships")
        self.setGeometry(100, 100, 1200, 800)

        self.all_data = []
        self.load_all_data()

    def load_all_data(self):
        with open('data/sunk.merchants.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.all_data = [row for row in reader]

    def search(self):
        self.filter_data()

    def filter_data(self):
        ship_name_search_text = self.search_ship_name_input.text().lower()
        commander_search_text = self.search_commander_input.text().lower()
        uboat_search_text = self.search_uboat_input.text().lower()
        tonnage_min = self.tonnage_min_slider.value()
        tonnage_max = self.tonnage_max_slider.value()

        filtered_data = [row for row in self.all_data if
                         (not ship_name_search_text or ship_name_search_text in row['ship_name'].lower()) and
                         (not commander_search_text or commander_search_text in row['commander'].lower()) and
                         (not uboat_search_text or uboat_search_text in row['uboat'].lower()) and
                         (tonnage_min <= int(row['tonnage'].replace(',', '')) <= tonnage_max)
                         ]

        self.update_table(filtered_data)

    def update_table(self, data):
        self.table_widget.setRowCount(0)
        for row in data:
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(row['ship_name']))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(row['nationality']))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(row['date']))
            self.table_widget.setItem(row_position, 3, QTableWidgetItem(row['uboat']))
            self.table_widget.setItem(row_position, 4, QTableWidgetItem(row['commander']))
            self.table_widget.setItem(row_position, 5, QTableWidgetItem(row['tonnage']))
            self.table_widget.setItem(row_position, 6, QTableWidgetItem(row['convoy']))
            self.table_widget.setItem(row_position, 7, QTableWidgetItem(row['coordinates']))

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Log File', '', 'CSV Files (*.csv);;All Files (*)')
        if file_name:
            self.statusBar().showMessage(f'Opened {file_name}')
            self.load_data(file_name)
        else:
            self.statusBar().showMessage('No file selected')

    def load_initial_data(self):
        file_name = 'data/sunk.merchants.csv'
        self.load_data(file_name)

    def load_data(self, file_name):
        with open(file_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(8)
            self.table_widget.setHorizontalHeaderLabels(
                ['Ship Name', 'Nationality', 'Date', 'Sunk by', 'Uboat commander', 'Tonnage', 'Convoy', 'Coordinates'])
            for row in reader:
                row_position = self.table_widget.rowCount()
                self.table_widget.insertRow(row_position)
                self.table_widget.setItem(row_position, 0, QTableWidgetItem(row['ship_name']))
                self.table_widget.setItem(row_position, 1, QTableWidgetItem(row['nationality']))
                self.table_widget.setItem(row_position, 2, QTableWidgetItem(row['date']))
                self.table_widget.setItem(row_position, 3, QTableWidgetItem(row['uboat']))
                self.table_widget.setItem(row_position, 4, QTableWidgetItem(row['commander']))
                self.table_widget.setItem(row_position, 5, QTableWidgetItem(row['tonnage']))
                self.table_widget.setItem(row_position, 6, QTableWidgetItem(row['convoy']))
                self.table_widget.setItem(row_position, 7, QTableWidgetItem(row['coordinates']))
            self.statusBar().showMessage(f'Data loaded from {file_name}')

            self.show_details()
            self.show_statistics()

    def show_details(self):
        row_position = self.table_widget.currentRow()
        if row_position == -1:
            row_position = 0

        ship_name_item = self.table_widget.item(row_position, 0)
        nationality_item = self.table_widget.item(row_position, 1)
        date_item = self.table_widget.item(row_position, 2)

        if ship_name_item is None or nationality_item is None or date_item is None:
            return

        ship_name = ship_name_item.text()
        nationality = nationality_item.text()
        date = date_item.text()

        with open("data/sunk.merchants.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row["ship_name"] == ship_name and row["nationality"] == nationality and row["date"] == date:
                    data = row
                    break

        position = data["coordinates"].strip("[]").replace("'", "").replace("(", "").replace(")", "").split(", ")
        lat, lon = float(position[0]), float(position[1])

        map_html = self.generate_map(lat, lon)

        details = f"""
    <table style="border-collapse: collapse; width: 100%;">
        <tr>
            <th style="border: 1px solid black; padding: 5px;">Attribute</th>
            <th style="border: 1px solid black; padding: 5px;">Value</th>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Ship Name</td>
            <td style="border: 1px solid black; padding: 5px;">{ship_name}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Nationality</td>
            <td style="border: 1px solid black; padding: 5px;">{nationality}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Date</td>
            <td style="border: 1px solid black; padding: 5px;">{date}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Sunk by</td>
            <td style="border: 1px solid black; padding: 5px;">{data['uboat']}, commanded by: {data['commander']}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Tonnage</td>
            <td style="border: 1px solid black; padding: 5px;">{data['tonnage']}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Convoy</td>
            <td style="border: 1px solid black; padding: 5px;">{data['convoy']}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Sunk coordinates</td>
            <td style="border: 1px solid black; padding: 5px;">{data['coordinates']}</td>
        </tr>
        <tr>
            <td style="border: 1px solid black; padding: 5px;">Map</td>
            <td style="border: 1px solid black; padding: 5px;"><a href='{map_html}'>Open Map</a></td>
        </tr>
    </table>
    """

        self.details_label.setText(details)
        self.details_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
        self.details_label.setOpenExternalLinks(True)

    def generate_map(self, lat, lon):
        m = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker([lat, lon]).add_to(m)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as map_file:
            m.save(map_file)
            map_file.close()

            return 'file://' + map_file.name

    def cell_clicked(self, row, column):
        self.show_details()
        self.show_statistics()

    def copy_data(self):
        QMessageBox.information(self, "Copy", "This is where you implement the copy functionality.")

    def paste_data(self):
        QMessageBox.information(self, "Paste", "This is where you implement the paste functionality.")

    def toggle_columns(self):
        if self.table_widget.columnWidth(7) == 0:
            self.table_widget.setColumnWidth(7, 200)
            self.statusBar().showMessage('Coordinates column is now visible')
        else:
            self.table_widget.setColumnWidth(7, 0)
            self.statusBar().showMessage('Coordinates column is now hidden')

    def show_about(self):
        QMessageBox.about(self, "About Log Viewer",
                          "Log Viewer is a simple application to view ship sinking logs with additional details and statistics.")

    def tonnage_slider_changed(self):
        min_value = self.tonnage_min_slider.value()
        max_value = self.tonnage_max_slider.value()
        self.tonnage_min_label.setText(f"Tonnage from: {min_value}")
        self.tonnage_max_label.setText(f"Tonnage to: {max_value}")
        self.search()

    def show_statistics(self):
        total_ships = self.table_widget.rowCount()
        total_tonnage = 0
        nationality_count = {}
        uboat_count = {}
        commander_count = {}

        for row in range(total_ships):
            tonnage = int(self.table_widget.item(row, 5).text().replace(',', ''))
            total_tonnage += tonnage

            nationality = self.table_widget.item(row, 1).text()
            if nationality in nationality_count:
                nationality_count[nationality] += 1
            else:
                nationality_count[nationality] = 1

            uboat = self.table_widget.item(row, 3).text()
            if uboat in uboat_count:
                uboat_count[uboat] += 1
            else:
                uboat_count[uboat] = 1

            commander = self.table_widget.item(row, 4).text()
            if commander in commander_count:
                commander_count[commander] += 1
            else:
                commander_count[commander] = 1

        if not nationality_count:
            self.statistics_label.setText("No statistics available.")
            return

        most_common_nationality = max(nationality_count, key=nationality_count.get)
        most_common_uboat = max(uboat_count, key=uboat_count.get)
        most_common_commander = max(commander_count, key=commander_count.get)

        statistics_text = f"<h3>Statistics</h3><p>Total Ships: {total_ships}</p><p>Total Tonnage: {total_tonnage:,}</p><p>Most common nationality: {most_common_nationality} ({nationality_count[most_common_nationality]})</p><p>Most active U-Boat: {most_common_uboat} ({uboat_count[most_common_uboat]})</p><p>Most successful commander: {most_common_commander} ({commander_count[most_common_commander]})</p>"
        self.statistics_label.setText(statistics_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = LogViewer()
    viewer.show()
    sys.exit(app.exec())
