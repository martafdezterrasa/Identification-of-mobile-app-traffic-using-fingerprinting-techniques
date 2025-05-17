import matplotlib.pyplot as plt

app_huellas = {
    "adobeacrobat": 471,
    "aliexpress": 1099,
    "amazon": 1620,
    "bbva": 609,
    "blablacar": 531,
    "bolt": 405,
    "burgerking": 732,
    "cabify": 547,
    "caixabank": 650,
    "capcut": 2185,
    "chatgpt": 277,
    "chrome": 594,
    "discord": 262,
    "disney": 431,
    "drive": 249,
    "facebook": 513,
    "glovo": 537,
    "gmail": 362,
    "google": 552,
    "googlemaps": 405,
    "hbomax": 242,
    "imagin": 441,
    "instagram": 478,
    "justeat": 313,
    "messenger": 358,
    "microsoftteams": 493,
    "moovit": 1176,
    "netflix": 589,
    "pinterest": 867,
    "primevideo": 961,
    "renfecercanias": 572,
    "revolut": 437,
    "santander": 639,
    "shein": 958,
    "snapchat": 777,
    "spotify": 685,
    "telepizza": 786,
    "telpark": 495,
    "temu": 985,
    "threads": 444,
    "tiktok": 1596,
    "traductor": 172,
    "ubereats": 136,
    "uber": 281,
    "wallapop": 1226,
    "waze": 351,
    "whatsapp": 211,
    "x": 455,
    "youtube": 763,
    "zoom": 320,
}

#define ranges
ranges = {
    "100-299": [],
    "300-599": [],
    "600-899": [],
    "900-1199": [],
    "1200-1499": [],
    "1500-1799": [],
    "1800-2199": [],
}

# Classify each app in ranges
for app, huellas in app_huellas.items():
    if 100 <= huellas <= 299:
        ranges["100-299"].append(app)
    elif 300 <= huellas <= 599:
        ranges["300-599"].append(app)
    elif 600 <= huellas <= 899:
        ranges["600-899"].append(app)
    elif 900 <= huellas <= 1199:
        ranges["900-1199"].append(app)
    elif 1200 <= huellas <= 1499:
        ranges["1200-1499"].append(app)
    elif 1500 <= huellas <= 1799:
        ranges["1500-1799"].append(app)
    elif 1800 <= huellas <= 2199:
        ranges["1800-2199"].append(app)


for range, apps in ranges.items():
    print(f"\nApps in range {range}: {len(apps)} apps")
    print(apps)


labels = list(ranges.keys())
num_apps = [len(apps) for apps in ranges.values()]

#Create diagram
plt.figure(figsize=(10, 6))
plt.bar(labels, num_apps, color='navy')
plt.xlabel('Range of fingerprints')
plt.ylabel('Number of apps')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('distribution_app_ja4.pdf', format='pdf')

plt.show()
