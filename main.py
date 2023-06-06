from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QTreeView, QHBoxLayout, QMessageBox, QFileDialog
from PyQt5.QtGui import QStandardItem, QStandardItemModel
import sys
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class FinanceApp(QMainWindow):
    def __init__(self):
        super(FinanceApp, self).__init__()

        # Set window title
        self.setWindowTitle("Finance App")

        # Set window size
        self.setGeometry(100, 100, 800, 600)

        # Create main widget
        main_widget = QWidget()

        # Create vertical layout for main widget
        self.layout = QVBoxLayout()
        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        # Create input fields and labels
        self.interest_rate_label = QLabel("Interest Rate (%)")
        self.interest_rate_input = QLineEdit()
        row1.addWidget(self.interest_rate_label)
        row1.addWidget(self.interest_rate_input)

        self.initial_investment_label = QLabel("Initial Investment ($)")
        self.initial_investment_input = QLineEdit()
        row1.addWidget(self.initial_investment_label)
        row1.addWidget(self.initial_investment_input)

        self.num_years_label = QLabel("Number of Years")
        self.num_years_input = QLineEdit()
        row1.addWidget(self.num_years_label)
        row1.addWidget(self.num_years_input)

        
        # Create TreeView for results
        self.model = QStandardItemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        row2.addWidget(self.tree_view)
        
        # Create plot widget
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        row2.addWidget(self.canvas)

        self.layout.addLayout(row1)
        self.layout.addLayout(row2)
        # Create calculate button
        self.calculate_button = QPushButton("Calculate")
        self.layout.addWidget(self.calculate_button)

        # Create reset button
        self.reset_button = QPushButton("Reset")
        self.layout.addWidget(self.reset_button)
        
        
        
        

        # Set main widget layout
        main_widget.setLayout(self.layout)

        # Set main widget as central widget
        self.setCentralWidget(main_widget)

        # Connect buttons to slots
        self.calculate_button.clicked.connect(self.calculate_compound_interest)
        self.reset_button.clicked.connect(self.reset_app)

    def calculate_compound_interest(self):
    # Get input values
        interest_rate = float(self.interest_rate_input.text())
        initial_investment = float(self.initial_investment_input.text())
        num_years = int(self.num_years_input.text())

        # Clear previous results
        self.model.clear()

        # Add column headers to the tree view
        self.model.setHorizontalHeaderLabels(["Year", "Total"])

        # Calculate compound interest and add results to tree view
        total = initial_investment
        for year in range(1, num_years + 1):
            total += total * (interest_rate / 100)
            item_year = QStandardItem(str(year))
            item_total = QStandardItem("{:.2f}".format(total))
            self.model.appendRow([item_year, item_total])

        # Update chart with results
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        years = list(range(1, num_years + 1))
        totals = [initial_investment * (1 + interest_rate / 100) ** year for year in years]     # Fix the formula here
        ax.plot(years, totals)
        ax.set_xlabel("Year")
        ax.set_ylabel("Total")
        self.canvas.draw()
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_results)
        self.layout.addWidget(self.save_button)
        

    def save_results(self):
    # Open a file dialog to choose a directory
        dir_path = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dir_path:
            # Create a subfolder within the selected directory
            folder_path = os.path.join(dir_path, "Results")
            os.makedirs(folder_path, exist_ok=True)

            # Save the results to a CSV file within the subfolder
            file_path = os.path.join(folder_path, "results.csv")
            with open(file_path, "w") as file:
                file.write("Year,Total\n")
                for row in range(self.model.rowCount()):
                    year = self.model.index(row, 0).data()
                    total = self.model.index(row, 1).data()
                    file.write("{},{}\n".format(year, total))

            # Show a message box to indicate successful save
            QMessageBox.information(self, "Save Results", "Results saved successfully in '{}'".format(folder_path))
        else:
            QMessageBox.warning(self, "Save Results", "No directory selected.")


    def reset_app(self):
        # Clear input fields and tree view
        self.interest_rate_input.clear()
        self.initial_investment_input.clear()
        self.num_years_input.clear()
        self.model.clear()
        self.figure.clear()
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    finance_app = FinanceApp()
    finance_app.show()
    app.exec_()



       
