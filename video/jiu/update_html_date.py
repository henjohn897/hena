import re
import os
from datetime import datetime, timedelta

# বর্তমান ফোল্ডার
FOLDER = os.getcwd()

# BD Time
now = datetime.utcnow() + timedelta(hours=6)
current_time = now.strftime("%Y-%m-%dT%H:%M:%S+06:00")

# 🔹 Full-width English লেটারগুলোকে Normal English বানানোর ফাংশন
def normalize_fullwidth(text):
    # ইউনিকোডে full-width ASCII ０〜９ → 0〜9, Ａ〜Ｚ → A〜Z, ａ〜ｚ → a〜z
    result = []
    for ch in text:
        code = ord(ch)
        if 0xFF10 <= code <= 0xFF19:  # full-width 0–9
            ch = chr(code - 0xFF10 + ord('0'))
        elif 0xFF21 <= code <= 0xFF3A:  # full-width A–Z
            ch = chr(code - 0xFF21 + ord('A'))
        elif 0xFF41 <= code <= 0xFF5A:  # full-width a–z
            ch = chr(code - 0xFF41 + ord('a'))
        result.append(ch)
    return "".join(result)

# 🔹 Date regex — অনেক ফরম্যাট ধরবে
date_pattern = re.compile(
    r"(\d{1,2}\s*(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*\d{4}"
    r"|\d{1,2}\s*(?:January|February|March|April|May|June|July|August|September|October|November|December)\s*\d{4}"
    r"|\d{4}[-/]\d{2}[-/]\d{2})",
    re.IGNORECASE
)

# 🔹 সব HTML ফাইল লুপ
for file in os.listdir(FOLDER):
    if file.endswith(".html") or file.endswith(".htm"):
        path = os.path.join(FOLDER, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # full-width লেটারগুলো normalize করে নেই
        normalized_content = normalize_fullwidth(content)

        # তারিখ রেপ্লেস করি
        updated = re.sub(date_pattern, current_time, normalized_content)

        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)

        print(f"✅ Updated: {file}")

print("✅ DONE — All HTML dates replaced with:", current_time)
