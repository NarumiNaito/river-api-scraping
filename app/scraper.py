from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import time

load_dotenv()

SCRAPE_URL = os.getenv("SCRAPE_URL")

FLAG_MEANINGS = {
    '*': '暫定値',
    '$': '欠測',
    '#': '閉局',
    '-': '未登録',
}

def get_water_data():
    base_url = "https://www1.river.go.jp"
    html_url = SCRAPE_URL

    chrome_options = Options()
    chrome_options.binary_location = "/usr/bin/chromium"
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")

    service = Service(executable_path="/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    a_tag = None
    soup = None

    try:
        for attempt in range(3):
            print(f"ページ取得試行 {attempt + 1}")
            driver.get(html_url)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='.dat']"))
                )
            except Exception as e:
                print("要素待機中にエラー:", e)
                time.sleep(2)
                continue

            soup = BeautifulSoup(driver.page_source, "lxml")
            a_tag = soup.find("a", href=re.compile(r"/dat/dload/download/.*\.dat$"))
            if a_tag:
                print(".dat リンク取得成功")
                break
            else:
                print(".dat リンクが見つかりません。再試行します")
                time.sleep(2)

        if not a_tag:
            raise Exception("ページに .dat ファイルのリンクが見つかりませんでした")

    finally:
        driver.quit()

    dat_path = a_tag["href"]
    dat_url = dat_path if dat_path.startswith("http") else base_url + dat_path

    dat_res = requests.get(dat_url)
    raw_text = dat_res.content.decode("cp932", errors="replace")
    lines = raw_text.splitlines()

    metadata = {}
    data_lines = []

    for i, line in enumerate(lines):
        if i == 0 and line.startswith("リアルタイム10分水位一覧表"):
            metadata["サイト名"] = line
        elif i in (1, 2, 3, 4) and "," in line:
            k, v = line.split(",", 1)
            metadata[k] = v
        elif line.startswith("#"):
            continue
        else:
            data_lines.append(line)

    data = []
    for line in data_lines:
        parts = line.split(",")
        if len(parts) < 3:
            continue

        date_str = parts[0]
        time_str = parts[1]
        value = parts[2]
        raw_flag = parts[3] if len(parts) > 3 else ""
        flag_meaning = FLAG_MEANINGS.get(raw_flag, "") if raw_flag else ""

        if flag_meaning == "未登録":
            continue
        if flag_meaning == "閉局":
            value = "-"

        if time_str == "24:00":
            dt_date = datetime.strptime(date_str, "%Y/%m/%d").date() + timedelta(days=1)
            dt = datetime.combine(dt_date, datetime.min.time())
            display_date = dt_date.strftime("%Y/%m/%d")
            display_time = "00:00"
        else:
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y/%m/%d %H:%M")
            display_date = date_str
            display_time = time_str

        data.append({
            "date": display_date,
            "time": display_time,
            "value": value,
            "flag": flag_meaning,
            "_dt": dt
        })

    data.sort(key=lambda r: r["_dt"], reverse=True)
    for r in data:
        del r["_dt"]

    return {
        "metadata": metadata,
        "data": data,
        "source_dat_url": dat_url
    }
