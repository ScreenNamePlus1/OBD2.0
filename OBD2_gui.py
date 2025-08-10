import obd
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import time

class OBDGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OBD-II Diagnostic Tool")
        self.root.geometry("600x400")
        
        self.connection = None
        self.monitoring = False
        
        # Port entry
        tk.Label(root, text="OBD-II Port (e.g., COM3 or /dev/ttyUSB0):").pack(pady=5)
        self.port_entry = tk.Entry(root, width=50)
        self.port_entry.pack()
        self.port_entry.insert(0, "/dev/ttyUSB0")  # Default value
        
        # Connect button
        self.connect_btn = tk.Button(root, text="Connect", command=self.connect_obd)
        self.connect_btn.pack(pady=10)
        
        # Status label
        self.status_label = tk.Label(root, text="Status: Disconnected", fg="red")
        self.status_label.pack()
        
        # DTC button and text area
        tk.Button(root, text="Read DTCs", command=self.read_dtc).pack(pady=5)
        self.dtc_text = scrolledtext.ScrolledText(root, height=5, width=70)
        self.dtc_text.pack(pady=5)
        
        # Real-time data labels
        self.rpm_label = tk.Label(root, text="RPM: N/A")
        self.rpm_label.pack()
        self.speed_label = tk.Label(root, text="Speed: N/A")
        self.speed_label.pack()
        self.coolant_label = tk.Label(root, text="Coolant Temp: N/A")
        self.coolant_label.pack()
        
        # Monitor button
        self.monitor_btn = tk.Button(root, text="Start Monitoring", command=self.toggle_monitoring)
        self.monitor_btn.pack(pady=10)
        
    def connect_obd(self):
        port = self.port_entry.get()
        try:
            self.connection = obd.OBD(port, baudrate=38400, protocol=None, fast=False)
            if self.connection.is_connected():
                self.status_label.config(text="Status: Connected", fg="green")
                messagebox.showinfo("Success", "Connected to OBD-II adapter!")
            else:
                raise Exception("Connection failed")
        except Exception as e:
            self.status_label.config(text="Status: Disconnected", fg="red")
            messagebox.showerror("Error", f"Failed to connect: {str(e)}")
    
    def read_dtc(self):
        if not self.connection or not self.connection.is_connected():
            messagebox.showerror("Error", "Not connected to OBD-II adapter.")
            return
        
        self.dtc_text.delete(1.0, tk.END)
        dtc_response = self.connection.query(obd.commands.GET_DTC)
        if dtc_response.is_null():
            self.dtc_text.insert(tk.END, "No diagnostic trouble codes found.\n")
        else:
            self.dtc_text.insert(tk.END, "Diagnostic Trouble Codes:\n")
            for code in dtc_response.value:
                self.dtc_text.insert(tk.END, f" - {code}\n")
    
    def update_realtime_data(self):
        if not self.connection or not self.connection.is_connected():
            return
        
        params = {
            "RPM": obd.commands.RPM,
            "Speed": obd.commands.SPEED,
            "Coolant Temp": obd.commands.COOLANT_TEMP
        }
        
        for name, cmd in params.items():
            response = self.connection.query(cmd)
            if not response.is_null():
                value = response.value
                if name == "RPM":
                    self.rpm_label.config(text=f"RPM: {value}")
                elif name == "Speed":
                    self.speed_label.config(text=f"Speed: {value}")
                elif name == "Coolant Temp":
                    self.coolant_label.config(text=f"Coolant Temp: {value}")
            else:
                if name == "RPM":
                    self.rpm_label.config(text="RPM: N/A")
                elif name == "Speed":
                    self.speed_label.config(text="Speed: N/A")
                elif name == "Coolant Temp":
                    self.coolant_label.config(text="Coolant Temp: N/A")
    
    def monitoring_loop(self):
        while self.monitoring:
            self.update_realtime_data()
            time.sleep(2)
    
    def toggle_monitoring(self):
        if not self.connection or not self.connection.is_connected():
            messagebox.showerror("Error", "Not connected to OBD-II adapter.")
            return
        
        if self.monitoring:
            self.monitoring = False
            self.monitor_btn.config(text="Start Monitoring")
        else:
            self.monitoring = True
            self.monitor_btn.config(text="Stop Monitoring")
            threading.Thread(target=self.monitoring_loop, daemon=True).start()

def main():
    root = tk.Tk()
    app = OBDGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
