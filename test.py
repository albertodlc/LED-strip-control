import ledStrip

MAC_ADDR = [
            "85:58:1B:08:AD:ED", # Mesa 1
            "85:58:1B:08:97:4D", # Mesa 2
            "85:58:1B:08:C6:67", # Mesa 3
            "52:14:00:00:C6:A9" # Techo
            ]

for m in MAC_ADDR:
    dc = ledStrip.DeviceControl(m)
    dc.notifications()
    dc.close_connection()
