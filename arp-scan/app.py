# app.py

import gradio as gr
from arp_check import ARPSpoofDetector
import time

detector = ARPSpoofDetector()

def check_arp_spoofing():
    detector.start_sniffing()
    while True:
        time.sleep(5)
        if detector.is_spoofed():
            alerts = detector.get_alerts()
            latest_alert = alerts[-1]
            message = f"ARP Spoofing Detected!\n\nTime: {latest_alert['timestamp']}\n" \
                      f"IP: {latest_alert['ip']}\nReal MAC: {latest_alert['real_mac']}\n" \
                      f"Fake MAC: {latest_alert['fake_mac']}"
            return message
        else:
            return "No ARP spoofing detected."

def arp_status_update():
    """Run the function every few seconds to update ARP status"""
    return check_arp_spoofing()

# Gradio Interface
with gr.Blocks() as gui:
    gr.Markdown("# ARP Spoof Detector")

    output_box = gr.Textbox(label="ARP Spoof Detection Status", placeholder="Monitoring...", lines=10)

    start_button = gr.Button("Start Detection")

    # Action to update detection status every 5 seconds
    start_button.click(arp_status_update, outputs=output_box, every=5)

# Run the interface
if __name__ == "__main__":
    detector.start_sniffing()
    gui.launch(server_name="0.0.0.0", server_port=3000)
