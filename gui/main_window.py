from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
                               QHBoxLayout, QWidget, QPushButton, QProgressBar,
                               QTextEdit, QDateEdit, QComboBox, QGroupBox,
                               QGridLayout, QMessageBox, QFileDialog, QTabWidget,
                               QTableWidget, QTableWidgetItem, QHeaderView, QSplitter)
from PySide6.QtCore import Qt, QThread, Signal, QDate, QTimer
from PySide6.QtGui import QFont, QIcon
import sys
import os
from datetime import datetime, timedelta

# Import our modules
from data_collectors.logins import get_logins
from data_collectors.file_shares import get_file_shares
from data_collectors.app_usage import get_app_usage
from report.pdf_generator import DigitalFootprintReport
from utils.helpers import (get_system_info, format_timestamp, truncate_text,
                          create_output_directory, get_unique_filename,
                          save_report_metadata, filter_data_by_date_range)

class DataCollectionThread(QThread):
    """Thread for collecting data to avoid blocking the GUI."""
    progress = Signal(str)
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, collect_logins=True, collect_files=True, collect_apps=True):
        super().__init__()
        self.collect_logins = collect_logins
        self.collect_files = collect_files
        self.collect_apps = collect_apps
        
    def run(self):
        try:
            data = {}
            
            if self.collect_logins:
                self.progress.emit("Collecting login data...")
                data['logins'] = get_logins()
                
            if self.collect_files:
                self.progress.emit("Collecting file shares data...")
                data['file_shares'] = get_file_shares()
                
            if self.collect_apps:
                self.progress.emit("Collecting application usage data...")
                data['app_usage'] = get_app_usage()
                
            self.progress.emit("Data collection completed!")
            self.finished.emit(data)
            
        except Exception as e:
            self.error.emit(f"Error during data collection: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Employee Digital Footprint Summarizer")
        self.setMinimumSize(1200, 800)
        
        # Data storage
        self.collected_data = {}
        self.collection_thread = None
        
        # Setup UI
        self.setup_ui()
        self.setup_connections()
        
        # Load system info
        self.load_system_info()
        
    def setup_ui(self):
        """Setup the main user interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Title
        title_label = QLabel("Employee Digital Footprint Summarizer")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # Setup tabs
        self.setup_collection_tab()
        self.setup_data_tab()
        self.setup_report_tab()
        
        # Status bar
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Ready")
        
    def setup_collection_tab(self):
        """Setup the data collection tab."""
        collection_widget = QWidget()
        layout = QVBoxLayout(collection_widget)
        
        # System info group
        system_group = QGroupBox("System Information")
        system_layout = QGridLayout(system_group)
        
        self.system_info_label = QLabel("Loading system information...")
        system_layout.addWidget(self.system_info_label, 0, 0)
        layout.addWidget(system_group)
        
        # Collection options group
        options_group = QGroupBox("Data Collection Options")
        options_layout = QGridLayout(options_group)
        
        self.collect_logins_cb = QComboBox()
        self.collect_logins_cb.addItems(["Yes", "No"])
        options_layout.addWidget(QLabel("Collect Login Data:"), 0, 0)
        options_layout.addWidget(self.collect_logins_cb, 0, 1)
        
        self.collect_files_cb = QComboBox()
        self.collect_files_cb.addItems(["Yes", "No"])
        options_layout.addWidget(QLabel("Collect File Shares:"), 1, 0)
        options_layout.addWidget(self.collect_files_cb, 1, 1)
        
        self.collect_apps_cb = QComboBox()
        self.collect_apps_cb.addItems(["Yes", "No"])
        options_layout.addWidget(QLabel("Collect App Usage:"), 2, 0)
        options_layout.addWidget(self.collect_apps_cb, 2, 1)
        
        layout.addWidget(options_group)
        
        # Date range group
        date_group = QGroupBox("Date Range (Optional)")
        date_layout = QGridLayout(date_group)
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-7))
        self.start_date.setCalendarPopup(True)
        date_layout.addWidget(QLabel("Start Date:"), 0, 0)
        date_layout.addWidget(self.start_date, 0, 1)
        
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        date_layout.addWidget(QLabel("End Date:"), 1, 0)
        date_layout.addWidget(self.end_date, 1, 1)
        
        layout.addWidget(date_group)
        
        # Collection controls
        controls_layout = QHBoxLayout()
        
        self.collect_button = QPushButton("Collect Data")
        self.collect_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        controls_layout.addWidget(self.collect_button)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        controls_layout.addWidget(self.progress_bar)
        
        layout.addLayout(controls_layout)
        
        # Progress text
        self.progress_text = QTextEdit()
        self.progress_text.setMaximumHeight(100)
        self.progress_text.setPlaceholderText("Collection progress will appear here...")
        layout.addWidget(self.progress_text)
        
        self.tab_widget.addTab(collection_widget, "Data Collection")
        
    def setup_data_tab(self):
        """Setup the data preview tab."""
        data_widget = QWidget()
        layout = QVBoxLayout(data_widget)
        
        # Data summary
        summary_layout = QHBoxLayout()
        
        self.logins_count_label = QLabel("Logins: 0")
        self.files_count_label = QLabel("File Shares: 0")
        self.apps_count_label = QLabel("Applications: 0")
        
        summary_layout.addWidget(self.logins_count_label)
        summary_layout.addWidget(self.files_count_label)
        summary_layout.addWidget(self.apps_count_label)
        summary_layout.addStretch()
        
        layout.addLayout(summary_layout)
        
        # Data tables
        self.data_tables = {}
        
        # Logins table
        logins_group = QGroupBox("Login Events")
        logins_layout = QVBoxLayout(logins_group)
        self.logins_table = QTableWidget()
        self.logins_table.setColumnCount(5)
        self.logins_table.setHorizontalHeaderLabels(['Timestamp', 'Username', 'Host', 'Type', 'Source'])
        self.logins_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        logins_layout.addWidget(self.logins_table)
        self.data_tables['logins'] = self.logins_table
        layout.addWidget(logins_group)
        
        # File shares table
        files_group = QGroupBox("File Shares")
        files_layout = QVBoxLayout(files_group)
        self.files_table = QTableWidget()
        self.files_table.setColumnCount(4)
        self.files_table.setHorizontalHeaderLabels(['Path', 'Type', 'Source', 'Last Accessed'])
        self.files_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        files_layout.addWidget(self.files_table)
        self.data_tables['file_shares'] = self.files_table
        layout.addWidget(files_group)
        
        # App usage table
        apps_group = QGroupBox("Application Usage")
        apps_layout = QVBoxLayout(apps_group)
        self.apps_table = QTableWidget()
        self.apps_table.setColumnCount(5)
        self.apps_table.setHorizontalHeaderLabels(['Name', 'Type', 'Path', 'Start Time', 'Resource Usage'])
        self.apps_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        apps_layout.addWidget(self.apps_table)
        self.data_tables['app_usage'] = self.apps_table
        layout.addWidget(apps_group)
        
        self.tab_widget.addTab(data_widget, "Data Preview")
        
    def setup_report_tab(self):
        """Setup the report generation tab."""
        report_widget = QWidget()
        layout = QVBoxLayout(report_widget)
        
        # Report options
        options_group = QGroupBox("Report Options")
        options_layout = QGridLayout(options_group)
        
        self.report_title = QTextEdit()
        self.report_title.setMaximumHeight(60)
        self.report_title.setPlaceholderText("Enter report title...")
        self.report_title.setPlainText("Employee Digital Footprint Report")
        options_layout.addWidget(QLabel("Report Title:"), 0, 0)
        options_layout.addWidget(self.report_title, 0, 1)
        
        self.output_path = QTextEdit()
        self.output_path.setMaximumHeight(60)
        self.output_path.setPlaceholderText("Output file path...")
        options_layout.addWidget(QLabel("Output Path:"), 1, 0)
        options_layout.addWidget(self.output_path, 1, 1)
        
        layout.addWidget(options_group)
        
        # Report controls
        controls_layout = QHBoxLayout()
        
        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_output_path)
        controls_layout.addWidget(self.browse_button)
        
        self.generate_button = QPushButton("Generate Report")
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        controls_layout.addWidget(self.generate_button)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Report status
        self.report_status = QTextEdit()
        self.report_status.setMaximumHeight(100)
        self.report_status.setPlaceholderText("Report generation status will appear here...")
        layout.addWidget(self.report_status)
        
        self.tab_widget.addTab(report_widget, "Report Generation")
        
    def setup_connections(self):
        """Setup signal connections."""
        self.collect_button.clicked.connect(self.start_data_collection)
        self.generate_button.clicked.connect(self.generate_report)
        
    def load_system_info(self):
        """Load and display system information."""
        try:
            system_info = get_system_info()
            info_text = f"""
            <b>Platform:</b> {system_info['platform']} {system_info['platform_version']}<br>
            <b>Machine:</b> {system_info['machine']}<br>
            <b>Processor:</b> {system_info['processor']}<br>
            <b>Hostname:</b> {system_info['hostname']}<br>
            <b>Current User:</b> {system_info['username']}
            """
            self.system_info_label.setText(info_text)
        except Exception as e:
            self.system_info_label.setText(f"Error loading system info: {e}")
            
    def start_data_collection(self):
        """Start the data collection process."""
        self.collect_button.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_text.clear()
        
        # Get collection options
        collect_logins = self.collect_logins_cb.currentText() == "Yes"
        collect_files = self.collect_files_cb.currentText() == "Yes"
        collect_apps = self.collect_apps_cb.currentText() == "Yes"
        
        if not any([collect_logins, collect_files, collect_apps]):
            QMessageBox.warning(self, "Warning", "Please select at least one data type to collect.")
            self.collect_button.setEnabled(True)
            self.progress_bar.setVisible(False)
            return
        
        # Start collection thread
        self.collection_thread = DataCollectionThread(collect_logins, collect_files, collect_apps)
        self.collection_thread.progress.connect(self.update_progress)
        self.collection_thread.finished.connect(self.data_collection_finished)
        self.collection_thread.error.connect(self.data_collection_error)
        self.collection_thread.start()
        
    def update_progress(self, message):
        """Update progress display."""
        self.progress_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        self.progress_text.ensureCursorVisible()
        
    def data_collection_finished(self, data):
        """Handle data collection completion."""
        self.collected_data = data
        self.collect_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        
        # Update data counts
        self.logins_count_label.setText(f"Logins: {len(data.get('logins', []))}")
        self.files_count_label.setText(f"File Shares: {len(data.get('file_shares', []))}")
        self.apps_count_label.setText(f"Applications: {len(data.get('app_usage', []))}")
        
        # Populate tables
        self.populate_data_tables()
        
        # Switch to data tab
        self.tab_widget.setCurrentIndex(1)
        
        self.status_bar.showMessage("Data collection completed successfully")
        
    def data_collection_error(self, error_message):
        """Handle data collection errors."""
        self.collect_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        QMessageBox.critical(self, "Error", f"Data collection failed: {error_message}")
        self.status_bar.showMessage("Data collection failed")
        
    def populate_data_tables(self):
        """Populate the data preview tables."""
        # Populate logins table
        if 'logins' in self.collected_data:
            self.populate_table(self.logins_table, self.collected_data['logins'], [
                'timestamp', 'username', 'host', 'type', 'source'
            ])
            
        # Populate file shares table
        if 'file_shares' in self.collected_data:
            self.populate_table(self.files_table, self.collected_data['file_shares'], [
                'path', 'type', 'source', 'timestamp'
            ])
            
        # Populate app usage table
        if 'app_usage' in self.collected_data:
            self.populate_table(self.apps_table, self.collected_data['app_usage'], [
                'name', 'type', 'path', 'start_time', 'cpu_percent'
            ])
            
    def populate_table(self, table, data, columns):
        """Populate a table with data."""
        table.setRowCount(len(data))
        
        for row, item in enumerate(data):
            for col, column in enumerate(columns):
                value = item.get(column, '')
                if column == 'timestamp' or column == 'start_time':
                    value = format_timestamp(value)
                elif column == 'path':
                    value = truncate_text(str(value), 40)
                elif column == 'cpu_percent':
                    value = f"{value:.1f}%" if value else "N/A"
                else:
                    value = str(value)
                    
                table.setItem(row, col, QTableWidgetItem(value))
                
    def browse_output_path(self):
        """Browse for output file path."""
        output_dir = create_output_directory()
        filename = get_unique_filename("digital_footprint_report")
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", 
            os.path.join(output_dir, filename),
            "PDF Files (*.pdf)"
        )
        
        if file_path:
            self.output_path.setPlainText(file_path)
            
    def generate_report(self):
        """Generate the PDF report."""
        if not self.collected_data:
            QMessageBox.warning(self, "Warning", "No data available. Please collect data first.")
            return
            
        output_path = self.output_path.toPlainText().strip()
        if not output_path:
            QMessageBox.warning(self, "Warning", "Please specify an output path.")
            return
            
        try:
            self.generate_button.setEnabled(False)
            self.report_status.clear()
            self.report_status.append("Generating report...")
            
            # Get report title
            title = self.report_title.toPlainText().strip()
            if not title:
                title = "Employee Digital Footprint Report"
                
            # Create report
            report_generator = DigitalFootprintReport(output_path)
            
            # Get date range
            start_date = self.start_date.date().toPython()
            end_date = self.end_date.date().toPython()
            
            # Filter data by date range if specified
            filtered_data = {}
            for key, data in self.collected_data.items():
                if start_date and end_date:
                    filtered_data[key] = filter_data_by_date_range(data, start_date, end_date)
                else:
                    filtered_data[key] = data
                    
            # Generate report
            report_path = report_generator.generate_report(
                filtered_data.get('logins', []),
                filtered_data.get('file_shares', []),
                filtered_data.get('app_usage', []),
                user_info={'name': get_system_info()['username']},
                date_range={'start': start_date, 'end': end_date}
            )
            
            # Save metadata
            metadata = {
                'title': title,
                'generated_at': datetime.now().isoformat(),
                'data_counts': {
                    'logins': len(filtered_data.get('logins', [])),
                    'file_shares': len(filtered_data.get('file_shares', [])),
                    'app_usage': len(filtered_data.get('app_usage', []))
                },
                'date_range': {
                    'start': start_date.isoformat() if start_date else None,
                    'end': end_date.isoformat() if end_date else None
                }
            }
            save_report_metadata(report_path, metadata)
            
            self.report_status.append(f"Report generated successfully: {report_path}")
            self.status_bar.showMessage("Report generated successfully")
            
            # Ask if user wants to open the report
            reply = QMessageBox.question(
                self, "Report Generated", 
                f"Report saved to:\n{report_path}\n\nWould you like to open it?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                os.startfile(report_path)
                
        except Exception as e:
            self.report_status.append(f"Error generating report: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to generate report: {str(e)}")
            self.status_bar.showMessage("Report generation failed")
        finally:
            self.generate_button.setEnabled(True)

def run_gui():
    """Run the GUI application."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec()) 