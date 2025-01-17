from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QWidget, QLabel, QLineEdit, QPushButton, QComboBox, 
                           QListWidget, QGroupBox, QTabWidget, QGridLayout, 
                           QTextEdit, QMessageBox, QStyleFactory, QMenu, QAction, 
                           QScrollArea, QFileDialog, QSplitter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import grn
import simulator
import importlib
import networkx as nx
import json
#import PyQt5_stylesheets

class NetworkDesignerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.input_values = {}
        self.current_theme = "dark"  # Default theme
        self.network = grn.grn()  # Initialize network first
        
        # Set up window icon
        self.dark_icon = QIcon("icons/gremlin_icon.png")
        self.light_icon = QIcon("icons/gremlin-icon-light.png")
        self.setWindowIcon(self.dark_icon)  # Default icon
        
        self.create_theme_menu()
        self.apply_style()
        self.init_ui()
        
    def create_theme_menu(self):
        # Create theme menu
        self.theme_menu = QMenu(self)
        
        # Load theme icons
        dark_icon = QIcon("icons/gremlin_icon.png")
        light_icon = QIcon("icons/gremlin-icon-light.png")
        
        # Add theme options with icons
        dark_action = QAction(dark_icon, "Gremlin (Dark Mode)", self)
        light_action = QAction(light_icon, "Mogwai (Light Mode)", self)
        
        # Connect actions
        dark_action.triggered.connect(lambda: self.change_theme("dark"))
        light_action.triggered.connect(lambda: self.change_theme("light"))
        
        # Add actions to menu
        self.theme_menu.addAction(dark_action)
        self.theme_menu.addAction(light_action)
        
        # Create settings button with current theme icon
        self.theme_button = QPushButton(self)
        self.theme_button.setIcon(dark_icon)  # Default icon
        self.theme_button.setFixedSize(32, 32)
        self.theme_button.clicked.connect(self.show_theme_menu)
        self.theme_button.setToolTip("Change Theme")
    
    def show_theme_menu(self):
        # Show theme menu at button position
        self.theme_menu.exec_(self.theme_button.mapToGlobal(self.theme_button.rect().bottomLeft()))
    
    def change_theme(self, theme):
        self.current_theme = theme
        # Update window icon and theme button icon
        if theme == "dark":
            icon = QIcon("icons/gremlin_icon.png")
        else:
            icon = QIcon("icons/gremlin-icon-light.png")
        
        self.setWindowIcon(icon)
        self.theme_button.setIcon(icon)
        self.apply_style()
    
    def apply_style(self):
        if self.current_theme == "dark":
            self.apply_dark_theme()
        elif self.current_theme == "light":
            self.apply_light_theme()
    
    def apply_dark_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
                font-size: 1pt;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-size: 10pt;
            }
            QGroupBox {
                font-size: 11pt;
                font-weight: bold;
                border: 1px solid #404040;
                border-radius: 3px;
                margin-top: 0.5em;
                padding: 0.5em;
                background-color: #333333;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 3px 0 3px;
            }
            QPushButton {
                background-color: #404040;
                color: white;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 3px;
                min-height: 30px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
                border: 1px solid #666666;
            }
            QPushButton[class="primary"] {
                background-color: #2196F3;
                border: 1px solid #1976D2;
            }
            QPushButton[class="primary"]:hover {
                background-color: #1976D2;
            }
            QPushButton[class="danger"] {
                background-color: #f44336;
                border: 1px solid #d32f2f;
            }
            QPushButton[class="danger"]:hover {
                background-color: #d32f2f;
            }
            QPushButton[class="success"] {
                background-color: #4CAF50;
                border: 1px solid #388E3C;
            }
            QPushButton[class="success"]:hover {
                background-color: #388E3C;
            }
            QLineEdit {
                background-color: #404040;
                color: white;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 3px;
                min-height: 18px;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
            QComboBox {
                background-color: #404040;
                color: white;
                border: 1px solid #555555;
                border-radius: 3px;
                padding: 3px;
                min-height: 25px;
                font-size: 12pt;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                border-top: 3px solid #ffffff;
                width: 0;
                height: 0;
                margin-right: 3px;
            }
            QListWidget {
                background-color: #404040;
                color: white;
                border: 1px solid #555555;
                border-radius: 3px;
            }
            QTextEdit {
                background-color: #404040;
                color: white;
                border: 1px solid #555555;
                border-radius: 3px;
            }
            QTabWidget::pane {
                border: 1px solid #404040;
                background-color: #333333;
            }
            QTabBar::tab {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 6px 10px;
                border: 1px solid #404040;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-size: 10pt;
            }
            QTabBar::tab:selected {
                background-color: #333333;
                border-bottom: none;
            }
            QTabBar::tab:hover {
                background-color: #383838;
            }
            QLabel {
                color: #ffffff;
                font-size: 10pt;
            }
            QStatusBar {
                background-color: #333333;
                color: #ffffff;
            }
        """)
    
    def apply_light_theme(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f0f0;
                color: #000000;
                font-size: 10pt;
            }
            QWidget {
                background-color: #f0f0f0;
                color: #000000;
                font-size: 10pt;
            }
            QGroupBox {
                font-size: 11pt;
                font-weight: bold;
                border: 1px solid #cccccc;
                border-radius: 3px;
                margin-top: 0.5em;
                padding: 0.5em;
                background-color: #ffffff;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 3px 0 3px;
            }
            QPushButton {
                background-color: #e0e0e0;
                color: black;
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 3px;
                min-height: 30px;
                font-size: 10pt;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
                border: 1px solid #bbbbbb;
            }
            QPushButton[class="primary"] {
                background-color: #2196F3;
                color: white;
                border: 1px solid #1976D2;
            }
            QPushButton[class="primary"]:hover {
                background-color: #1976D2;
            }
            QPushButton[class="danger"] {
                background-color: #f44336;
                color: white;
                border: 1px solid #d32f2f;
            }
            QPushButton[class="danger"]:hover {
                background-color: #d32f2f;
            }
            QPushButton[class="success"] {
                background-color: #4CAF50;
                color: white;
                border: 1px solid #388E3C;
            }
            QPushButton[class="success"]:hover {
                background-color: #388E3C;
            }
            QLineEdit {
                background-color: white;
                color: black;
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 3px;
                min-height: 20px;
                font-size: 10pt;
            }
            QLineEdit:focus {
                border: 1px solid #2196F3;
            }
            QComboBox {
                background-color: white;
                color: black;
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 3px;
                min-height: 25px;
                font-size: 10pt;
            }
            QListWidget, QTextEdit {
                background-color: white;
                color: black;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                color: black;
                padding: 8px 10px;
                border: 1px solid #cccccc;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-size: 10pt;
            }
            QTabBar::tab:selected {
                background-color: white;
            }
            QTabBar::tab:hover {
                background-color: #d0d0d0;
            }
            QLabel {
                color: black;
                font-size: 10pt;
            }
            QStatusBar {
                background-color: #f0f0f0;
                color: black;
            }
        """)
   
    def init_ui(self):
        self.setWindowTitle("GReNMlin - Gene Regulatory Network Designer")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(800, 600)
        
        # Create main container
        main_container = QWidget()
        self.setCentralWidget(main_container)
        main_layout = QHBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins for better splitter appearance
        
        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Create left panel with scroll
        left_scroll = QScrollArea()
        left_scroll.setWidgetResizable(True)
        left_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        left_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create left panel with tabs
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create header with theme button and file menu
        header = QHBoxLayout()
        
        # Create file menu button
        file_menu = QMenu(self)
        load_action = QAction('Load Network', self)
        save_action = QAction('Save Network', self)
        load_action.setShortcut('Ctrl+O')
        save_action.setShortcut('Ctrl+S')
        load_action.triggered.connect(self.load_network)
        save_action.triggered.connect(self.save_network)
        file_menu.addAction(load_action)
        file_menu.addAction(save_action)
        
        file_button = QPushButton("File")
        file_button.setFixedSize(50, 32)
        file_button.clicked.connect(lambda: file_menu.exec_(file_button.mapToGlobal(file_button.rect().bottomLeft())))
        
        header.addWidget(file_button)
        header.addStretch()
        header.addWidget(self.theme_button)
        left_layout.addLayout(header)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setDocumentMode(True)
        
        # Create and add tabs
        self.species_tab = self.create_species_tab()
        self.genes_tab = self.create_genes_tab()
        self.simulation_tab = self.create_simulation_tab()
        self.steady_state_tab = self.create_steady_state_tab()
        
        self.tab_widget.addTab(self.species_tab, "Species")
        self.tab_widget.addTab(self.genes_tab, "Genes")
        self.tab_widget.addTab(self.simulation_tab, "Simulation")
        self.tab_widget.addTab(self.steady_state_tab, "Steady State")
        
        left_layout.addWidget(self.tab_widget)
        
        # Add left panel to scroll area
        left_scroll.setWidget(left_panel)
        
        # Create right visualization panel with scroll area
        viz_scroll = QScrollArea()
        viz_scroll.setWidgetResizable(True)
        viz_panel = self.create_visualization_panel()
        viz_scroll.setWidget(viz_panel)
        
        # Add panels to splitter
        splitter.addWidget(left_scroll)
        splitter.addWidget(viz_scroll)
        
        # Set initial sizes (30% left, 70% right)
        splitter.setSizes([300, 700])
        
        # Add splitter to main layout
        main_layout.addWidget(splitter)
        
        self.statusBar().showMessage("Ready")
        
        # Add theme button to top-left corner
        self.theme_button.move(10, 10)
        
    def create_control_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Style the tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)  # More modern look for tabs
        self.tabs.addTab(self.create_species_tab(), "Species")
        self.tabs.addTab(self.create_genes_tab(), "Genes")
        self.tabs.addTab(self.create_simulation_tab(), "Simulation")
        
        layout.addWidget(self.tabs)
        return panel
    
    def create_species_tab(self):
        """Create the species tab with input fields and lists"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input species section
        input_group = QGroupBox("Add Input Species")
        input_layout = QGridLayout()
        
        self.input_species_name = QLineEdit()
        add_input_btn = QPushButton("Add Input Species")
        add_input_btn.clicked.connect(self.add_input_species)
        add_input_btn.setProperty("class", "success")
        
        input_layout.addWidget(QLabel("Name:"), 0, 0)
        input_layout.addWidget(self.input_species_name, 0, 1)
        input_layout.addWidget(add_input_btn, 1, 0, 1, 2)
        
        input_group.setLayout(input_layout)
        
        # Regular species section
        species_group = QGroupBox("Add Regular Species")
        species_layout = QGridLayout()
        
        self.species_name = QLineEdit()
        self.species_delta = QLineEdit()
        add_species_btn = QPushButton("Add Species")
        add_species_btn.clicked.connect(self.add_species)
        add_species_btn.setProperty("class", "success")
        
        species_layout.addWidget(QLabel("Name:"), 0, 0)
        species_layout.addWidget(self.species_name, 0, 1)
        species_layout.addWidget(QLabel("Delta (δ):"), 1, 0)
        species_layout.addWidget(self.species_delta, 1, 1)
        species_layout.addWidget(add_species_btn, 2, 0, 1, 2)
        
        species_group.setLayout(species_layout)
        
        # Species list
        list_group = QGroupBox("Current Species")
        list_layout = QVBoxLayout()
        self.species_list = QListWidget()
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_selected_species)
        delete_btn.setProperty("class", "danger")
        
        list_layout.addWidget(self.species_list)
        list_layout.addWidget(delete_btn)
        list_group.setLayout(list_layout)
        
        # Add all sections to main layout
        layout.addWidget(input_group)
        layout.addWidget(species_group)
        layout.addWidget(list_group)
        
        return tab
    
    def create_genes_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Properties group
        props_group = QGroupBox("Gene Properties")
        props_layout = QVBoxLayout()
        self.gene_alpha = QLineEdit()
        self.gene_logic = QComboBox()
        self.gene_logic.addItems(["and", "or"])
        props_layout.addWidget(QLabel("Alpha (production rate):"))
        props_layout.addWidget(self.gene_alpha)
        props_layout.addWidget(QLabel("Logic Type:"))
        props_layout.addWidget(self.gene_logic)
        props_group.setLayout(props_layout)
        
        # Regulators group
        reg_group = QGroupBox("Regulators")
        reg_layout = QVBoxLayout()
        self.reg_name = QComboBox()
        self.reg_type = QComboBox()
        self.reg_type.addItems(["1", "-1"])
        self.reg_kd = QLineEdit()
        self.reg_n = QLineEdit()
        add_reg_btn = QPushButton("Add Regulator")
        add_reg_btn.clicked.connect(self.add_regulator)
        add_reg_btn.setProperty("class", "success")
        reg_layout.addWidget(QLabel("Name:"))
        reg_layout.addWidget(self.reg_name)
        reg_layout.addWidget(QLabel("Type:"))
        reg_layout.addWidget(self.reg_type)
        reg_layout.addWidget(QLabel("Kd:"))
        reg_layout.addWidget(self.reg_kd)
        reg_layout.addWidget(QLabel("n:"))
        reg_layout.addWidget(self.reg_n)
        reg_layout.addWidget(add_reg_btn)
        self.regulators_list = QListWidget()
        reg_layout.addWidget(QLabel("Current Regulators:"))
        reg_layout.addWidget(self.regulators_list)
        reg_group.setLayout(reg_layout)
        
        # Current genes group
        genes_list_group = QGroupBox("Current Genes")
        genes_list_layout = QVBoxLayout()
        
        # Add gene buttons at the top
        gene_buttons_layout = QHBoxLayout()
        add_gene_btn = QPushButton("Create Gene")
        add_gene_btn.clicked.connect(self.create_gene)
        add_gene_btn.setProperty("class", "success")
        delete_gene_btn = QPushButton("Delete Selected Gene")
        delete_gene_btn.clicked.connect(self.delete_selected_gene)
        delete_gene_btn.setProperty("class", "danger")
        gene_buttons_layout.addWidget(add_gene_btn)
        gene_buttons_layout.addWidget(delete_gene_btn)
        genes_list_layout.addLayout(gene_buttons_layout)
        
        # Add genes list
        self.genes_list = QListWidget()
        genes_list_layout.addWidget(self.genes_list)
        genes_list_group.setLayout(genes_list_layout)
        
        # Add all groups to main layout
        layout.addWidget(props_group)
        layout.addWidget(reg_group)
        layout.addWidget(genes_list_group)
        
        return tab
    
    def create_visualization_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        
        v_splitter = QSplitter(Qt.Vertical)
        
        # Network visualization
        viz_group = QGroupBox("Network Visualization")
        viz_layout = QVBoxLayout()
        
        toolbar = QHBoxLayout()
        
        # Zoom buttons
        zoom_buttons = QHBoxLayout()
        zoom_in_btn = QPushButton("+")
        zoom_out_btn = QPushButton("-")
        reset_zoom_btn = QPushButton("Reset")
        
        zoom_in_btn.setFixedSize(30, 30)
        zoom_out_btn.setFixedSize(30, 30)
        reset_zoom_btn.setFixedSize(60, 30)
        
        zoom_in_btn.clicked.connect(lambda: self.zoom_network(1.2))
        zoom_out_btn.clicked.connect(lambda: self.zoom_network(0.8))
        reset_zoom_btn.clicked.connect(self.reset_network_zoom)
        
        zoom_buttons.addWidget(zoom_in_btn)
        zoom_buttons.addWidget(zoom_out_btn)
        zoom_buttons.addWidget(reset_zoom_btn)
        
        toolbar.addLayout(zoom_buttons)
        toolbar.addStretch()
        
        # Save button
        save_btn = QPushButton("💾")  # Fixed save icon
        save_btn.setFixedSize(30, 30)
        save_btn.setToolTip("Save Network Visualization")
        save_btn.clicked.connect(lambda: self.save_visualization('network'))
        toolbar.addWidget(save_btn)
        
        viz_layout.addLayout(toolbar)
        
        # Create figure for network visualization
        self.network_fig = plt.figure(figsize=(6, 6))
        self.network_canvas = FigureCanvas(self.network_fig)
        viz_layout.addWidget(self.network_canvas)
        viz_group.setLayout(viz_layout)
        
        # Simulation results
        sim_group = QGroupBox("Simulation Results")
        sim_layout = QVBoxLayout()
        
        # Add save button for simulation (right-aligned)
        sim_toolbar = QHBoxLayout()
        sim_toolbar.addStretch()  # Push save button to right
        save_sim_btn = QPushButton("💾")
        save_sim_btn.setFixedSize(30, 30)
        save_sim_btn.setToolTip("Save Simulation Results")
        save_sim_btn.clicked.connect(lambda: self.save_visualization('simulation'))
        sim_toolbar.addWidget(save_sim_btn)
        sim_layout.addLayout(sim_toolbar)
        
        self.sim_canvas = FigureCanvas(plt.figure(figsize=(6, 4)))
        sim_layout.addWidget(self.sim_canvas)
        sim_group.setLayout(sim_layout)
        
        # Add groups to vertical splitter
        v_splitter.addWidget(viz_group)
        v_splitter.addWidget(sim_group)
        
        # Set initial sizes (60% network, 40% simulation)
        v_splitter.setSizes([600, 400])
        
        # Add splitter to layout
        layout.addWidget(v_splitter)
        
        return panel
    
    def create_simulation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Create tabs for different simulation types
        sim_tabs = QTabWidget()
        sim_tabs.addTab(self.create_single_sim_tab(), "Single Run")
        sim_tabs.addTab(self.create_sequence_sim_tab(), "Sequence")
        
        layout.addWidget(sim_tabs)
        return tab
    
    def create_steady_state_tab(self):
        """Create parent tab for steady state analysis"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Create nested tab widget for steady state
        steady_state_tabs = QTabWidget()
        
        # Create and add sub-tabs
        single_steady_tab = self.create_single_steady_tab()
        multiple_steady_tab = self.create_multiple_steady_tab()
        
        steady_state_tabs.addTab(single_steady_tab, "Single Steady State")
        steady_state_tabs.addTab(multiple_steady_tab, "Multiple Steady States")
        
        layout.addWidget(steady_state_tabs)
        return tab
    
    def create_single_steady_tab(self):
        """Create tab for single steady state analysis"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input values section
        input_group = QGroupBox("Input Species Values")
        input_layout = QVBoxLayout()
        self.steady_input_fields_widget = QWidget()
        self.steady_input_fields_layout = QGridLayout(self.steady_input_fields_widget)
        self.update_steady_input_fields()  # New method to update input fields
        input_layout.addWidget(self.steady_input_fields_widget)
        input_group.setLayout(input_layout)
        
        # Parameters
        param_group = QGroupBox("Analysis Parameters")
        param_layout = QGridLayout()
        
        self.single_steady_ins_factor = QLineEdit("1")
        
        row = 0
        param_layout.addWidget(QLabel("Input Scale Factor:"), row, 0)
        param_layout.addWidget(self.single_steady_ins_factor, row, 1)
        
        param_group.setLayout(param_layout)
        
        # Add groups to layout
        layout.addWidget(input_group)
        layout.addWidget(param_group)
        
        # Run button
        run_btn = QPushButton("Find Steady State")
        run_btn.clicked.connect(self.run_steady_single)
        run_btn.setProperty("class", "success")
        layout.addWidget(run_btn)
        
        return tab
    
    def create_multiple_steady_tab(self):
        """Create tab for multiple steady state analysis"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Parameters
        param_group = QGroupBox("Analysis Parameters")
        param_layout = QGridLayout()
        
        self.multiple_steady_ins_factor = QLineEdit("1")
        self.multiple_steady_rep_num = QLineEdit("10")
        
        row = 0
        param_layout.addWidget(QLabel("Input Scale Factor:"), row, 0)
        param_layout.addWidget(self.multiple_steady_ins_factor, row, 1)
        
        row += 1
        param_layout.addWidget(QLabel("Number of Repetitions:"), row, 0)
        param_layout.addWidget(self.multiple_steady_rep_num, row, 1)
        
        param_group.setLayout(param_layout)
        layout.addWidget(param_group)
        
        # Run button
        run_btn = QPushButton("Find Multiple Steady States")
        run_btn.clicked.connect(self.run_steady_multiple)
        run_btn.setProperty("class", "success")
        layout.addWidget(run_btn)
        
        return tab
    
    def update_steady_input_fields(self):
        """Update input fields for steady state analysis based on current network"""
        # Clear existing fields
        while self.steady_input_fields_layout.count():
            item = self.steady_input_fields_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add fields for each input species
        if hasattr(self, 'network'):
            if not self.network.input_species_names:
                label = QLabel("No input species defined. Add input species in the Species tab.")
                self.steady_input_fields_layout.addWidget(label, 0, 0, 1, 2)
            else:
                self.steady_input_values = {}  # Create new dict for steady state inputs
                for i, name in enumerate(self.network.input_species_names):
                    self.steady_input_fields_layout.addWidget(QLabel(f"{name}:"), i, 0)
                    input_field = QLineEdit("0")
                    self.steady_input_fields_layout.addWidget(input_field, i, 1)
                    self.steady_input_values[name] = input_field
    
    def run_steady_single(self):
        """Run single steady state simulation"""
        try:
            if not hasattr(self, 'network'):
                QMessageBox.warning(self, "Error", "No network defined")
                return
            
            if not self.network.input_species_names:
                QMessageBox.warning(self, "Error", "No input species defined")
                return
            
            # Get input values and apply scale factor
            ins_factor = float(self.single_steady_ins_factor.text())
            IN = []
            for name in self.network.input_species_names:
                value = float(self.steady_input_values[name].text()) * ins_factor
                IN.append(value)
            
            # Generate equations and model
            self.network.generate_equations()
            self.network.generate_model()
            
            # Import the generated model directly
            import model
            importlib.reload(model)
            
            # Create initial state with input values fixed
            n_inputs = len(IN)
            n_others = len(self.network.species_names) - n_inputs
            initial_state = np.concatenate([IN, np.zeros(n_others)])
            
            # Run simulation using solve_model directly
            steady_state = model.solve_model_steady(initial_state)
            
            # For input species, use the original input values
            steady_state[:n_inputs] = IN
            
            # Plot steady state results
            self.sim_canvas.figure.clear()
            fig = self.sim_canvas.figure
            
            # Create two subplots
            ax1 = fig.add_subplot(211)  # Bar plot
            ax2 = fig.add_subplot(212)  # Text results
            
            # Bar plot
            ax1.bar(self.network.species_names, steady_state)
            ax1.set_ylabel('Concentration')
            ax1.set_title('Steady State Results')
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
            
            # Text results
            results_text = "Steady State Values:\n\n"
            for i, name in enumerate(self.network.species_names):
                results_text += f"{name}: {steady_state[i]:.3f}\n"
            
            ax2.text(0.1, 0.5, results_text, 
                    transform=ax2.transAxes, 
                    verticalalignment='center',
                    fontfamily='monospace')
            ax2.axis('off')
            
            fig.tight_layout()
            self.sim_canvas.draw()
            
            # Update status bar
            self.statusBar().showMessage("Steady state calculation completed", 3000)
            
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def run_steady_multiple(self):
        """Run multiple steady state simulations"""
        try:
            # Get parameters
            eps = float(self.multi_eps.text())
            ins_factor = float(self.multi_ins_factor.text())
            rep_num = int(self.multi_rep_num.text())
            
            # Get custom input combinations if provided
            ins_def = None
            if self.multi_input_text.toPlainText().strip():
                ins_def = eval(self.multi_input_text.toPlainText())
            
            # Find steady states
            df = simulator.get_steady(
                self.network,
                rep_num=rep_num,
                INS_def=ins_def,
                INS_factor=ins_factor,
                eps=eps
            )
            
            # Save results to CSV
            filename = "steady_states.csv"
            df.to_csv(filename)
            
            # Show results
            msg = QMessageBox()
            msg.setWindowTitle("Steady States Results")
            msg.setText(f"Found {len(df)} steady states.\nResults saved to {filename}\n\nFirst few steady states:\n\n{df.head().to_string()}")
            msg.exec_()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Steady states computation failed: {str(e)}")
    
    def update_input_fields(self):
        while self.input_fields_layout.count():
            item = self.input_fields_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        row = 0
        self.input_values = {}
        if not self.network.input_species_names:
            label = QLabel("No input species defined. Add input species in the Species tab.")
            self.input_fields_layout.addWidget(label, 0, 0, 1, 2)
        else:
            for species in self.network.input_species_names:
                label = QLabel(f"Value for {species}:")
                value = QLineEdit("0")
                self.input_fields_layout.addWidget(label, row, 0)
                self.input_fields_layout.addWidget(value, row, 1)
                self.input_values[species] = value
                row += 1
    
    def add_regulator(self):
        try:
            name = self.reg_name.currentText()
            reg_type = int(self.reg_type.currentText())
            kd, n = self.validate_regulator()
            regulator = {
                'name': name,
                'type': reg_type,
                'Kd': kd,
                'n': n
            }
            self.current_regulators = getattr(self, 'current_regulators', [])
            self.current_regulators.append(regulator)
            self.reg_kd.clear()
            self.reg_n.clear()
            self.update_regulators_list()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def create_gene(self):
        try:
            alpha = self.validate_gene()
            logic_type = self.gene_logic.currentText()
            if hasattr(self, 'current_regulators') and self.current_regulators:
                gene_info = {
                    'alpha': alpha,
                    'regulators': self.current_regulators,
                    'products': [{'name': 'Y'}],
                    'logic_type': logic_type
                }
                self.network.add_gene(**gene_info)
                regulators_str = ", ".join(f"{r['name']}" for r in self.current_regulators)
                self.genes_list.addItem(f"Gene: α={alpha}, Logic={logic_type}, Regulators=[{regulators_str}]")
                self.current_regulators = []
                self.gene_alpha.clear()
                self.update_regulators_list()
                self.update_network_view()
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def update_regulators_list(self):
        if not hasattr(self, 'regulators_list'):
            self.regulators_list = QListWidget()
        self.regulators_list.clear()
        if hasattr(self, 'current_regulators'):
            for reg in self.current_regulators:
                self.regulators_list.addItem(
                    f"{reg['name']} (type={reg['type']}, Kd={reg['Kd']}, n={reg['n']})"
                )
    
    def update_species_combobox(self):
        self.reg_name.clear()
        self.reg_name.addItems(self.network.species_names)
    
    def add_input_species(self):
        name = self.input_species_name.text()
        if name:
            try:
                self.network.add_input_species(name)
                self.update_species_list()
                self.update_species_combobox()
                self.update_input_fields()
                self.update_steady_input_fields()
                self.update_network_view()
                self.input_species_name.clear()
                self.statusBar().showMessage(f"Input species '{name}' added successfully", 3000)
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def add_species(self):
        try:
            name = self.validate_species_name(self.species_name.text())
            delta = self.validate_float_input(self.species_delta.text(), "Delta", min_val=0)
            self.network.add_species(name, delta)
            self.species_list.addItem(f"Species: {name} (δ={delta})")
            self.species_name.clear()
            self.species_delta.clear()
            self.update_network_view()
            self.update_species_combobox()
            self.statusBar().showMessage(f"Species '{name}' added successfully", 3000)
        except ValueError as e:
            QMessageBox.warning(self, "Error", str(e))
    
    def update_network_view(self):
        """Update the network visualization"""
        try:
            # Clear previous figure
            self.network_fig.clear()
            ax = self.network_fig.add_subplot(111)
            
            # Get species and positions
            species = self.network.species_names
            n_species = len(species)
            angles = np.linspace(0, 2*np.pi, n_species, endpoint=False)
            pos_x = np.cos(angles)
            pos_y = np.sin(angles)
            
            # Store positions for hover functionality
            self.node_positions = {}
            for i, name in enumerate(species):
                self.node_positions[name] = (pos_x[i], pos_y[i])
            
            # Draw nodes and labels
            for i, (x, y, name) in enumerate(zip(pos_x, pos_y, species)):
                color = 'lightblue' if name in self.network.input_species_names else 'lightgreen'
                ax.add_patch(plt.Circle((x, y), 0.1, color=color))
                ax.text(x, y, name, ha='center', va='center')
            
            # Draw edges (regulations)
            for gene in self.network.genes:
                for reg in gene.get('regulators', []):
                    source = species.index(reg['name'])
                    target = species.index(gene['products'][0]['name'])
                    dx = pos_x[target] - pos_x[source]
                    dy = pos_y[target] - pos_y[source]
                    color = 'green' if reg['type'] == 1 else 'red'
                    ax.arrow(pos_x[source], pos_y[source], dx*0.8, dy*0.8,
                            head_width=0.05, color=color, alpha=0.6)
            
            # Set view limits with some padding
            ax.set_xlim(-1.5, 1.5)
            ax.set_ylim(-1.5, 1.5)
            ax.set_aspect('equal')
            ax.axis('off')
            
            # Store initial limits for zoom reset
            self.initial_xlim = ax.get_xlim()
            self.initial_ylim = ax.get_ylim()
            
            # Create hover annotation
            self.annot = ax.annotate("", 
                                    xy=(0, 0), 
                                    xytext=(20, 20),
                                    bbox=dict(
                                        boxstyle='round4',
                                        fc='white',
                                        ec='gray',
                                        alpha=0.9,
                                        pad=0.5
                                    ),
                                    xycoords='data',
                                    textcoords='offset points',
                                    ha='left')
            self.annot.set_visible(False)
            
            # Connect hover event
            self.network_canvas.mpl_connect('motion_notify_event', self.on_hover)
            
            # Update canvas
            self.network_fig.tight_layout()
            self.network_canvas.draw()
            
        except Exception as e:
            self.statusBar().showMessage(f"Error updating network view: {str(e)}", 3000)
    
    def on_hover(self, event):
        """Handle hover events to show additional information"""
        if event.inaxes and hasattr(self, 'node_positions'):
            try:
                # Find closest node
                min_dist = float('inf')
                closest_node = None
                
                for name, (x, y) in self.node_positions.items():
                    dist = np.sqrt((x - event.xdata)**2 + (y - event.ydata)**2)
                    if dist < min_dist and dist < 0.15:  # Detection threshold
                        min_dist = dist
                        closest_node = name
                
                if closest_node:
                    # Build hover text
                    hover_text = f"Species: {closest_node}\n"
                    if closest_node in self.network.input_species_names:
                        hover_text += "Type: Input Species\n"
                    else:
                        for species in self.network.species:
                            if species['name'] == closest_node:
                                hover_text += f"Type: Regular Species\nDelta: {species['delta']}\n"
                    
                    # Add regulation information
                    incoming_regs = []
                    outgoing_regs = []
                    for gene in self.network.genes:
                        for reg in gene['regulators']:
                            if reg['name'] == closest_node:
                                outgoing_regs.append(
                                    f"→ {gene['products'][0]['name']}\n"
                                    f"  Type: {'Activation' if reg['type']==1 else 'Repression'}\n"
                                    f"  Kd: {reg['Kd']}\n"
                                    f"  n: {reg['n']}"
                                )
                            if gene['products'][0]['name'] == closest_node:
                                if reg['name'] != closest_node:
                                    incoming_regs.append(
                                        f"← {reg['name']}\n"
                                        f"  Type: {'Activation' if reg['type']==1 else 'Repression'}\n"
                                        f"  Kd: {reg['Kd']}\n"
                                        f"  n: {reg['n']}"
                                    )
                    
                    if incoming_regs:
                        hover_text += "\nIncoming Regulations:\n" + "\n".join(incoming_regs)
                    if outgoing_regs:
                        hover_text += "\nOutgoing Regulations:\n" + "\n".join(outgoing_regs)
                    
                    # Update annotation
                    x, y = self.node_positions[closest_node]
                    self.annot.xy = (x, y)
                    self.annot.set_text(hover_text)
                    self.annot.set_visible(True)
                else:
                    self.annot.set_visible(False)
                
                self.network_canvas.draw_idle()
                
            except Exception as e:
                self.statusBar().showMessage(f"Error handling hover: {str(e)}", 3000)
    
    def zoom_network(self, factor):
        """Zoom the network view by the given factor"""
        ax = self.network_fig.gca()
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        
        # Calculate new limits
        xcenter = (xlim[1] + xlim[0]) / 2
        ycenter = (ylim[1] + ylim[0]) / 2
        
        xwidth = (xlim[1] - xlim[0]) / factor
        ywidth = (ylim[1] - ylim[0]) / factor
        
        # Set new limits
        ax.set_xlim([xcenter - xwidth/2, xcenter + xwidth/2])
        ax.set_ylim([ycenter - ywidth/2, ycenter + ywidth/2])
        
        self.network_canvas.draw_idle()
    
    def reset_network_zoom(self):
        """Reset zoom to original view"""
        if hasattr(self, 'initial_xlim') and hasattr(self, 'initial_ylim'):
            ax = self.network_fig.gca()
            ax.set_xlim(self.initial_xlim)
            ax.set_ylim(self.initial_ylim)
            self.network_canvas.draw_idle()
    
    def run_single_simulation(self):
        try:
            if not self.network.input_species_names:
                raise ValueError("No input species defined. Please add input species first.")
            
            IN = []
            for species in self.network.input_species_names:
                if species not in self.input_values:
                    self.recreate_simulation_tab()
                    raise ValueError(f"Please set value for {species}")
                value_text = self.input_values[species].text()
                if not value_text:
                    raise ValueError(f"Please enter a value for {species}")
                IN.append(float(value_text))
            IN = np.array(IN)
            
            if not self.network.genes:
                raise ValueError("No genes defined. Please add genes first.")
            
            t_end = float(self.sim_time.text())
            ins_factor = float(self.single_ins_factor.text())
            
            n_rs = len(self.network.species_names) - len(self.network.input_species_names)
            r0 = self.parse_r0_input(self.single_r0.text(), n_rs)
            
            T, Y = simulator.simulate_single(
                self.network, 
                IN, 
                t_end=t_end, 
                INS_factor=ins_factor,
                R0=r0,
                plot_on=False
            )
            
            self.plot_simulation_results(T, Y)
            self.statusBar().showMessage("Simulation completed", 3000)
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid input: {str(e)}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Simulation failed: {str(e)}")
    
    def run_sequence_simulation(self):
        try:
            sequence = eval(self.sequence_input.toPlainText())
            if not isinstance(sequence, list) or not all(isinstance(x, tuple) for x in sequence):
                raise ValueError("Sequence must be a list of tuples")
            
            t_single = float(self.t_single.text())
            ins_factor = float(self.seq_ins_factor.text())
            
            T, Y = simulator.simulate_sequence(
                self.network, 
                sequence, 
                t_single=t_single,
                INS_factor=ins_factor,
                plot_on=False
            )
            
            self.plot_simulation_results(T, Y)
            self.statusBar().showMessage("Sequence simulation completed", 3000)
        except ValueError as e:
            self.statusBar().showMessage(f"Error: {str(e)}", 5000)
        except Exception as e:
            self.statusBar().showMessage(f"Simulation failed: {str(e)}", 5000)
    
    def plot_simulation_results(self, T, Y):
        self.sim_canvas.figure.clear()
        ax = self.sim_canvas.figure.add_subplot(111)
        for i, species in enumerate(self.network.species_names):
            ax.plot(T, Y[:, i], label=species)
        ax.set_xlabel('Time')
        ax.set_ylabel('Concentration')
        ax.set_title('Simulation Results')
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()
        ax.margins(x=0.05, y=0.1)
        self.sim_canvas.figure.tight_layout()
        self.sim_canvas.draw()
    
    def validate_species_name(self, name):
        """Validate species name"""
        if not name:
            raise ValueError("Species name cannot be empty")
        if name in self.network.species_names:
            raise ValueError(f"Species '{name}' already exists")
        return name
    
    def validate_float_input(self, value, name, min_val=None, max_val=None):
        try:
            float_val = float(value)
            if min_val is not None and float_val < min_val:
                raise ValueError(f"{name} must be greater than {min_val}")
            if max_val is not None and float_val > max_val:
                raise ValueError(f"{name} must be less than {max_val}")
            return float_val
        except ValueError:
            raise ValueError(f"{name} must be a valid number")
    
    def validate_regulator(self):
        if not self.reg_name.currentText():
            raise ValueError("Please select a species for the regulator")
        kd = self.validate_float_input(self.reg_kd.text(), "Kd", min_val=0)
        n = self.validate_float_input(self.reg_n.text(), "n", min_val=0)
        return kd, n
    
    def validate_gene(self):
        if not hasattr(self, 'current_regulators') or not self.current_regulators:
            raise ValueError("Gene must have at least one regulator")
        alpha = self.validate_float_input(self.gene_alpha.text(), "Alpha", min_val=0)
        return alpha
    
    def delete_selected_species(self):
        """Delete the selected species from the list"""
        selected = self.species_list.currentItem()
        if selected:
            try:
                # Extract species name from the list item text
                text = selected.text()
                name = text.split(":")[1].split("(")[0].strip()
                
                # Remove from network
                if text.startswith("Input"):
                    self.network.input_species_names.remove(name)
                for i, species in enumerate(self.network.species):
                    if species['name'] == name:
                        self.network.species.pop(i)
                        break
                
                # Remove from species_names list
                if name in self.network.species_names:
                    self.network.species_names.remove(name)
                
                # Update UI
                self.update_species_list()
                self.update_species_combobox()
                self.update_input_fields()
                self.update_steady_input_fields()
                self.update_network_view()
                
                self.statusBar().showMessage(f"Species '{name}' deleted successfully", 3000)
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))
    
    def recreate_simulation_tab(self):
        """Recreate the simulation tab with updated input fields"""
        try:
            # Create new simulation tab
            new_tab = self.create_simulation_tab()
            
            # Find and replace the simulation tab
            for i in range(self.tab_widget.count()):
                if self.tab_widget.tabText(i) == "Simulation":
                    self.tab_widget.removeTab(i)
                    self.tab_widget.insertTab(i, new_tab, "Simulation")
                    self.tab_widget.setCurrentIndex(i)  # Switch to the simulation tab
                    break
            
            # Update input fields
            self.update_input_fields()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to recreate simulation tab: {str(e)}")
    
    def delete_selected_gene(self):
        current_item = self.genes_list.currentItem()
        if current_item:
            index = self.genes_list.row(current_item)
            if 0 <= index < len(self.network.genes):
                del self.network.genes[index]
                self.genes_list.takeItem(index)
                self.update_network_view()
                self.statusBar().showMessage("Gene deleted", 3000)
    
    def parse_r0_input(self, r0_text, n_rs):
        """Parse R0 input text to get initial values"""
        if r0_text.strip().lower() == 'random':
            return np.random.random(n_rs)
        elif r0_text.strip().lower() == 'zeros':
            return np.zeros(n_rs)
        else:
            try:
                values = [float(x.strip()) for x in r0_text.split(',')]
                if len(values) != n_rs:
                    raise ValueError(f"Expected {n_rs} values for R0, got {len(values)}")
                return np.array(values)
            except ValueError:
                raise ValueError("Invalid R0 format. Use 'random', 'zeros', or comma-separated numbers")
    
    def create_single_sim_tab(self):
        """Create tab for single simulation"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Input values section
        input_group = QGroupBox("Input Values")
        input_layout = QVBoxLayout()
        self.input_fields_widget = QWidget()
        self.input_fields_layout = QGridLayout(self.input_fields_widget)
        
        # Important: Check for input species and create fields
        if hasattr(self, 'network') and self.network.input_species_names:
            row = 0
            self.input_values = {}  # Reset input values dictionary
            for species in self.network.input_species_names:
                label = QLabel(f"Value for {species}:")
                value = QLineEdit("0")
                self.input_fields_layout.addWidget(label, row, 0)
                self.input_fields_layout.addWidget(value, row, 1)
                self.input_values[species] = value
                row += 1
        else:
            label = QLabel("No input species defined. Add input species in the Species tab.")
            self.input_fields_layout.addWidget(label, 0, 0, 1, 2)
        
        input_layout.addWidget(self.input_fields_widget)
        input_group.setLayout(input_layout)
        
        # Parameters
        param_group = QGroupBox("Simulation Parameters")
        param_layout = QGridLayout()
        
        self.sim_time = QLineEdit("10.0")
        self.single_ins_factor = QLineEdit("1")
        self.single_r0 = QLineEdit("random")
        
        row = 0
        param_layout.addWidget(QLabel("Simulation Time (seconds):"), row, 0)
        param_layout.addWidget(self.sim_time, row, 1)
        
        row += 1
        param_layout.addWidget(QLabel("Input Scale Factor:"), row, 0)
        param_layout.addWidget(self.single_ins_factor, row, 1)
        
        row += 1
        param_layout.addWidget(QLabel("Initial Values (R0):"), row, 0)
        param_layout.addWidget(self.single_r0, row, 1)
        
        param_group.setLayout(param_layout)
        layout.addWidget(input_group)
        layout.addWidget(param_group)
        
        run_btn = QPushButton("Run Simulation")
        run_btn.clicked.connect(self.run_single_simulation)
        run_btn.setProperty("class", "success")
        layout.addWidget(run_btn)
        
        return tab
    
    def create_sequence_sim_tab(self):
        """Create tab for sequence simulation"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Parameters
        param_group = QGroupBox("Sequence Parameters")
        param_layout = QGridLayout()
        
        self.t_single = QLineEdit("100")
        self.seq_ins_factor = QLineEdit("1")
        
        row = 0
        param_layout.addWidget(QLabel("Time per Input (t_single):"), row, 0)
        param_layout.addWidget(self.t_single, row, 1)
        
        row += 1
        param_layout.addWidget(QLabel("Input Scale Factor:"), row, 0)
        param_layout.addWidget(self.seq_ins_factor, row, 1)
        
        param_group.setLayout(param_layout)
        layout.addWidget(param_group)
        
        # Sequence input
        input_group = QGroupBox("Input Sequence")
        input_layout = QVBoxLayout()
        self.sequence_input = QTextEdit()
        self.sequence_input.setMinimumHeight(100)
        self.sequence_input.setMaximumHeight(150)
        self.sequence_input.setPlaceholderText("[(100,0), (0,100), (100,100)]")
        input_layout.addWidget(self.sequence_input)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        run_sequence_btn = QPushButton("Run Sequence")
        run_sequence_btn.clicked.connect(self.run_sequence_simulation)
        run_sequence_btn.setProperty("class", "success")
        layout.addWidget(run_sequence_btn)
        
        return tab

    def update_species_list(self):
        """Update the species list widget with current species"""
        self.species_list.clear()
        for name in self.network.input_species_names:
            self.species_list.addItem(f"Input: {name}")
        for species in self.network.species:
            if species['name'] not in self.network.input_species_names:
                self.species_list.addItem(f"Species: {species['name']} (δ={species['delta']})")

    def save_visualization(self, viz_type):
        """Save the current visualization as an image"""
        try:
            # Get file name from user
            file_name, _ = QFileDialog.getSaveFileName(
                self, 
                "Save Visualization",
                "",
                "PNG Files (*.png);;All Files (*)"
            )
            
            if file_name:
                if not file_name.endswith('.png'):
                    file_name += '.png'
                
                if viz_type == 'network':
                    self.network_fig.savefig(file_name, bbox_inches='tight', dpi=300)
                else:  # simulation
                    self.sim_canvas.figure.savefig(file_name, bbox_inches='tight', dpi=300)
                
                self.statusBar().showMessage(f"Saved visualization to {file_name}", 3000)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save visualization: {str(e)}")

    def save_network(self):
        """Save complete network configuration"""
        try:
            # Prepare network data in example_grn.json format
            network_data = {
                'species': [
                    {
                        'name': species['name'],
                        'delta': species['delta']
                    }
                    for species in self.network.species
                ],
                'genes': [
                    {
                        'alpha': gene['alpha'],
                        'regulators': gene['regulators'],
                        'products': gene['products'],
                        'logic_type': gene['logic_type']
                    }
                    for gene in self.network.genes
                ]
            }
            
            # Get save location from user
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save Network Configuration",
                "",
                "JSON Files (*.json);;All Files (*)"
            )
            
            if file_name:
                if not file_name.endswith('.json'):
                    file_name += '.json'
                
                # Save to file
                with open(file_name, 'w') as f:
                    json.dump(network_data, f, indent=2)
                
                self.statusBar().showMessage(f"Network saved to {file_name}", 3000)
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save network: {str(e)}")

    def load_network(self):
        """Load network configuration from file"""
        try:
            # Get file from user
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                "Load Network Configuration",
                "",
                "JSON Files (*.json);;All Files (*)"
            )
            
            if file_name:
                # Load from file
                with open(file_name, 'r') as f:
                    network_data = json.load(f)
                
                # Create new network
                self.network = grn.grn()
                
                # Load species and determine input species
                self.network.species = network_data['species']
                self.network.genes = network_data['genes']
                
                # Determine input species (those that aren't products of any gene)
                product_names = set()
                for gene in self.network.genes:
                    for product in gene['products']:
                        product_names.add(product['name'])
                
                # Input species are those that aren't products
                self.network.input_species_names = [
                    species['name'] 
                    for species in self.network.species 
                    if species['name'] not in product_names
                ]
                
                # Update species names list
                self.network.species_names = [s['name'] for s in self.network.species]
                
                # Clear existing values
                self.input_values = {}
                self.current_regulators = []
                
                # Important: Create new simulation tab before updating fields
                new_sim_tab = self.create_simulation_tab()
                
                # Update all UI elements
                self.update_species_list()
                self.update_species_combobox()
                self.update_network_view()
                self.update_genes_list()
                
                # Replace simulation tab
                for i in range(self.tab_widget.count()):
                    if self.tab_widget.tabText(i) == "Simulation":
                        self.tab_widget.removeTab(i)
                        self.tab_widget.insertTab(i, new_sim_tab, "Simulation")
                        break
                
                self.statusBar().showMessage(f"Network loaded from {file_name}", 3000)
        
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load network: {str(e)}")

    def update_genes_list(self):
        """Update the genes list with current genes"""
        self.genes_list.clear()
        for gene in self.network.genes:
            regulators_str = ", ".join(f"{r['name']}" for r in gene['regulators'])
            self.genes_list.addItem(
                f"Gene: α={gene['alpha']}, Logic={gene['logic_type']}, "
                f"Regulators=[{regulators_str}]"
            )

if __name__ == "__main__":
    app = QApplication([])
    window = NetworkDesignerGUI()
    window.show()
    app.exec_()
