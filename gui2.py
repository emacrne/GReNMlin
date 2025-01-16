from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                           QWidget, QLabel, QLineEdit, QPushButton, QComboBox, 
                           QListWidget, QGroupBox, QTabWidget, QGridLayout, 
                           QTextEdit, QMessageBox)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import grn
import simulator

class NetworkDesignerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.input_values = {}
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Gene Regulatory Network Designer")
        self.setGeometry(100, 100, 1200, 800)
        self.network = grn.grn()
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        control_panel = self.create_control_panel()
        viz_panel = self.create_visualization_panel()
        main_layout.addWidget(control_panel, stretch=1)
        main_layout.addWidget(viz_panel, stretch=1)
        self.statusBar().showMessage("Ready")
        
    def create_control_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_species_tab(), "Species")
        self.tabs.addTab(self.create_genes_tab(), "Genes")
        self.tabs.addTab(self.create_simulation_tab(), "Simulation")
        layout.addWidget(self.tabs)
        return panel
    
    def create_species_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        input_group = QGroupBox("Add Input Species (Regulators)")
        input_layout = QVBoxLayout()
        self.input_name = QLineEdit()
        add_input_btn = QPushButton("Add Input Species")
        add_input_btn.clicked.connect(self.add_input_species)
        input_layout.addWidget(QLabel("Name:"))
        input_layout.addWidget(self.input_name)
        input_layout.addWidget(add_input_btn)
        input_group.setLayout(input_layout)
        species_group = QGroupBox("Regular Species (Products)")
        species_layout = QVBoxLayout()
        self.species_name = QLineEdit()
        self.species_delta = QLineEdit()
        add_species_btn = QPushButton("Add Species")
        add_species_btn.clicked.connect(self.add_species)
        species_layout.addWidget(QLabel("Name:"))
        species_layout.addWidget(self.species_name)
        species_layout.addWidget(QLabel("Delta (degradation rate):"))
        species_layout.addWidget(self.species_delta)
        species_layout.addWidget(add_species_btn)
        species_group.setLayout(species_layout)
        list_group = QGroupBox("Current Species")
        list_layout = QVBoxLayout()
        self.species_list = QListWidget()
        list_layout.addWidget(self.species_list)
        list_group.setLayout(list_layout)
        delete_species_btn = QPushButton("Delete Selected Species")
        delete_species_btn.clicked.connect(self.delete_selected_species)
        list_layout.addWidget(delete_species_btn)
        layout.addWidget(input_group)
        layout.addWidget(species_group)
        layout.addWidget(list_group)
        return tab
    
    def create_genes_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
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
        reg_group = QGroupBox("Regulators")
        reg_layout = QVBoxLayout()
        self.reg_name = QComboBox()
        self.reg_type = QComboBox()
        self.reg_type.addItems(["1", "-1"])
        self.reg_kd = QLineEdit()
        self.reg_n = QLineEdit()
        add_reg_btn = QPushButton("Add Regulator")
        add_reg_btn.clicked.connect(self.add_regulator)
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
        genes_list_group = QGroupBox("Current Genes")
        genes_list_layout = QVBoxLayout()
        self.genes_list = QListWidget()
        genes_list_layout.addWidget(self.genes_list)
        delete_gene_btn = QPushButton("Delete Selected Gene")
        delete_gene_btn.clicked.connect(self.delete_selected_gene)
        genes_list_layout.addWidget(delete_gene_btn)
        genes_list_group.setLayout(genes_list_layout)
        add_gene_btn = QPushButton("Create Gene")
        add_gene_btn.clicked.connect(self.create_gene)
        layout.addWidget(props_group)
        layout.addWidget(reg_group)
        layout.addWidget(genes_list_group)
        layout.addWidget(add_gene_btn)
        return tab
    
    def create_visualization_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        viz_group = QGroupBox("Network Visualization")
        viz_layout = QVBoxLayout()
        self.network_canvas = FigureCanvas(plt.figure(figsize=(6, 6)))
        viz_layout.addWidget(self.network_canvas)
        viz_group.setLayout(viz_layout)
        sim_group = QGroupBox("Simulation Results")
        sim_layout = QVBoxLayout()
        self.sim_canvas = FigureCanvas(plt.figure(figsize=(6, 4)))
        sim_layout.addWidget(self.sim_canvas)
        sim_group.setLayout(sim_layout)
        layout.addWidget(viz_group)
        layout.addWidget(sim_group)
        return panel
    
    def create_simulation_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        single_group = QGroupBox("Single Simulation")
        single_layout = QVBoxLayout()
        
        input_group = QGroupBox("Input Species Values")
        input_layout = QVBoxLayout()
        self.input_fields_widget = QWidget()
        self.input_fields_layout = QGridLayout(self.input_fields_widget)
        self.update_input_fields()
        input_layout.addWidget(self.input_fields_widget)
        input_group.setLayout(input_layout)
        single_layout.addWidget(input_group)
        
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
        param_layout.addWidget(QLabel("Initial Values (R0, 'random' or comma-separated):"), row, 0)
        param_layout.addWidget(self.single_r0, row, 1)
        
        param_group.setLayout(param_layout)
        single_layout.addWidget(param_group)
        
        run_btn = QPushButton("Run Simulation")
        run_btn.clicked.connect(self.run_single_simulation)
        single_layout.addWidget(run_btn)
        single_group.setLayout(single_layout)
        layout.addWidget(single_group)
        
        sequence_group = QGroupBox("Sequence Simulation")
        sequence_layout = QVBoxLayout()
        
        seq_param_group = QGroupBox("Sequence Parameters")
        seq_param_layout = QGridLayout()
        
        self.t_single = QLineEdit("100")
        self.seq_ins_factor = QLineEdit("1")
        
        row = 0
        seq_param_layout.addWidget(QLabel("Time per Input (t_single):"), row, 0)
        seq_param_layout.addWidget(self.t_single, row, 1)
        
        row += 1
        seq_param_layout.addWidget(QLabel("Input Scale Factor:"), row, 0)
        seq_param_layout.addWidget(self.seq_ins_factor, row, 1)
        
        seq_param_group.setLayout(seq_param_layout)
        sequence_layout.addWidget(seq_param_group)
        
        self.sequence_input = QTextEdit()
        self.sequence_input.setMinimumHeight(100)
        self.sequence_input.setMaximumHeight(150)
        self.sequence_input.setPlaceholderText("[(100,0), (0,100), (100,100)]")
        sequence_layout.addWidget(self.sequence_input)
        
        run_sequence_btn = QPushButton("Run Sequence")
        run_sequence_btn.clicked.connect(self.run_sequence_simulation)
        sequence_layout.addWidget(run_sequence_btn)
        
        sequence_group.setLayout(sequence_layout)
        layout.addWidget(sequence_group)
        
        return tab
    
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
        try:
            name = self.validate_species_name(self.input_name.text())
            self.network.add_input_species(name)
            self.species_list.addItem(f"Input: {name}")
            self.input_name.clear()
            self.update_network_view()
            self.update_species_combobox()
            self.update_input_fields()
            self.statusBar().showMessage(f"Input species '{name}' added successfully", 3000)
        except ValueError as e:
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
        self.network_canvas.figure.clear()
        ax = self.network_canvas.figure.add_subplot(111)
        species = self.network.species_names
        n_species = len(species)
        angles = np.linspace(0, 2*np.pi, n_species, endpoint=False)
        pos_x = np.cos(angles)
        pos_y = np.sin(angles)
        for i, (x, y, name) in enumerate(zip(pos_x, pos_y, species)):
            color = 'lightblue' if name in self.network.input_species_names else 'lightgreen'
            ax.add_patch(plt.Circle((x, y), 0.1, color=color))
            ax.text(x, y, name, ha='center', va='center')
        for gene in self.network.genes:
            for reg in gene.get('regulators', []):
                source = species.index(reg['name'])
                target = species.index(gene['products'][0]['name'])
                dx = pos_x[target] - pos_x[source]
                dy = pos_y[target] - pos_y[source]
                color = 'green' if reg['type'] == 1 else 'red'
                ax.arrow(pos_x[source], pos_y[source], dx*0.8, dy*0.8,
                        head_width=0.05, color=color, alpha=0.6)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.set_aspect('equal')
        ax.axis('off')
        self.network_canvas.draw()
    
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
        if not name:
            raise ValueError("Species name cannot be empty")
        if name in self.network.species_names:
            raise ValueError(f"Species '{name}' already exists")
        if not name.isalnum():
            raise ValueError("Species name must be alphanumeric")
        return name.strip()
    
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
        current_item = self.species_list.currentItem()
        if current_item:
            text = current_item.text()
            species_name = text.split(":")[1].split("(")[0].strip()
            if species_name in self.network.species_names:
                self.network.genes = [g for g in self.network.genes 
                                    if species_name not in [r['name'] for r in g['regulators']]
                                    and species_name not in [p['name'] for p in g['products']]]
                if species_name in self.network.input_species_names:
                    self.network.input_species_names.remove(species_name)
                self.network.species = [s for s in self.network.species if s['name'] != species_name]
                self.network.species_names.remove(species_name)
                self.species_list.takeItem(self.species_list.row(current_item))
                self.update_network_view()
                self.update_species_combobox()
                self.update_input_fields()
                self.statusBar().showMessage(f"Species '{species_name}' deleted", 3000)
    
    def recreate_simulation_tab(self):
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == "Simulation":
                new_tab = self.create_simulation_tab()
                self.tabs.removeTab(i)
                self.tabs.insertTab(i, new_tab, "Simulation")
                break
    
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

if __name__ == "__main__":
    app = QApplication([])
    window = NetworkDesignerGUI()
    window.show()
    app.exec_()
