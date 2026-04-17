import sys
import threading
import time
import rclpy
from PyQt5.QtWidgets import (QApplication, QTreeWidget, QTreeWidgetItem, 
                             QVBoxLayout, QWidget, QHeaderView, QLabel, QHBoxLayout, QGridLayout)
from PyQt5.QtCore import Qt

# Importing the logic from inspector_logic.py
from .inspector_logic import DetailedInspector, CommSignals

class MainUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Industrial ROS2 Inspector | Global Performance Monitor")
        self.resize(1200, 850)

        self.topic_hz_data = {} 
        self.last_time = {}

        self.signals = CommSignals()
        self.signals.add_topic.connect(self.on_add_topic)
        self.signals.update_data.connect(self.on_update_data)

        # --- Top Summary Dashboard ---
        summary_container = QGridLayout()
        
        self.total_hz_label = QLabel("Total Hz: 0.00 Hz")
        self.avg_hz_label = QLabel("Avg Hz: 0.00 Hz")
        self.total_ms_label = QLabel("Total Period: 0.00 ms")
        self.avg_ms_label = QLabel("Avg Period: 0.00 ms")
        
        # Industrial Styling
        label_style = """
            font-weight: bold; 
            font-size: 13px; 
            color: #1B5E20; 
            background-color: #E8F5E9;
            padding: 8px; 
            border: 1px solid #C8E6C9; 
            border-radius: 4px;
        """
        for lbl in [self.total_hz_label, self.avg_hz_label, self.total_ms_label, self.avg_ms_label]:
            lbl.setStyleSheet(label_style)
            lbl.setAlignment(Qt.AlignCenter)

        summary_container.addWidget(self.total_hz_label, 0, 0)
        summary_container.addWidget(self.avg_hz_label, 0, 1)
        summary_container.addWidget(self.total_ms_label, 1, 0)
        summary_container.addWidget(self.avg_ms_label, 1, 1)

        # --- Tree Widget ---
        self.tree = QTreeWidget()
        self.tree.setColumnCount(3)
        self.tree.setHeaderLabels(["Topic / Node Hierarchy", "Frequency / Type", "Period (ms)"])
        self.tree.header().setSectionResizeMode(0, QHeaderView.Stretch)
        
        self.topic_parents = {}
        self.live_data_items = {}

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(summary_container)
        main_layout.addWidget(self.tree)
        self.setLayout(main_layout)

        self.running = True
        self.start_timer()

    def start_timer(self):
        if self.running:
            self.refresh_calculations()
            threading.Timer(1.0, self.start_timer).start()

    def on_add_topic(self, name, t_type, pub_nodes, sub_nodes):
        parent = QTreeWidgetItem(self.tree)
        parent.setText(0, name)
        parent.setText(1, "0.00 Hz")
        parent.setCheckState(0, Qt.Checked) 
        self.topic_parents[name] = parent
        self.topic_hz_data[name] = []
        self.last_time[name] = time.time()

        # Nodes Info
        pub_root = QTreeWidgetItem(parent)
        pub_root.setText(0, f"→ Publishers ({len(pub_nodes)})")
        for node in pub_nodes: QTreeWidgetItem(pub_root).setText(0, f" • {node}")

        sub_root = QTreeWidgetItem(parent)
        sub_root.setText(0, f"← Subscribers ({len(sub_nodes)})")
        for node in sub_nodes: QTreeWidgetItem(sub_root).setText(0, f" • {node}")

        # Data Field
        data_root = QTreeWidgetItem(parent)
        data_root.setText(0, "▼ Live Data")
        self.live_data_items[name] = QTreeWidgetItem(data_root)
        self.live_data_items[name].setText(0, "Streaming...")
        self.live_data_items[name].setFirstColumnSpanned(True)

    def on_update_data(self, topic, formatted_msg):
        now = time.time()
        if topic in self.last_time:
            diff = now - self.last_time[topic]
            if diff > 0: self.topic_hz_data[topic].append(1.0 / diff)
        self.last_time[topic] = now

        if topic in self.live_data_items:
            if self.topic_parents[topic].checkState(0) == Qt.Checked:
                p = self.live_data_items[topic].parent()
                if p and p.isExpanded(): self.live_data_items[topic].setText(0, formatted_msg)

    def refresh_calculations(self):
        total_hz = 0.0
        active_count = 0

        for topic, hz_list in self.topic_hz_data.items():
            if self.topic_parents[topic].checkState(0) == Qt.Checked:
                if hz_list:
                    avg_hz = sum(hz_list) / len(hz_list)
                    ms = 1000.0 / avg_hz
                    self.topic_parents[topic].setText(1, f"{avg_hz:.2f} Hz")
                    self.topic_parents[topic].setText(2, f"{ms:.2f} ms")
                    total_hz += avg_hz
                    active_count += 1
                self.topic_hz_data[topic] = [] 
            else:
                self.topic_parents[topic].setText(1, "OFF")
                self.topic_parents[topic].setText(2, "---")

        # Dashboard Logic
        if active_count > 0:
            avg_hz_val = total_hz / active_count
            total_ms_val = 1000.0 / total_hz if total_hz > 0 else 0.0
            avg_ms_val = 1000.0 / avg_hz_val if avg_hz_val > 0 else 0.0
        else:
            avg_hz_val = total_ms_val = avg_ms_val = 0.0

        # Update Dashboard Labels
        self.total_hz_label.setText(f"Total Throughput: {total_hz:.2f} Hz")
        self.avg_hz_label.setText(f"Average Frequency: {avg_hz_val:.2f} Hz")
        self.total_ms_label.setText(f"Combined Period: {total_ms_val:.2f} ms")
        self.avg_ms_label.setText(f"Global Avg Period: {avg_ms_val:.2f} ms")

    def closeEvent(self, event):
        self.running = False
        event.accept()

def main():
    rclpy.init()
    app = QApplication(sys.argv)
    ui = MainUI()
    node = DetailedInspector(ui.signals)
    threading.Thread(target=rclpy.spin, args=(node,), daemon=True).start()
    ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()