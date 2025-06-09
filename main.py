import requests
from bs4 import BeautifulSoup

url = "https://www1.river.go.jp/cgi-bin/DspWaterData.exe?KIND=9&ID=304031284403020"
res = requests.get(url)
res.encoding = 'EUC-JP'
soup = BeautifulSoup(res.text, 'lxml')

print("ページタイトル:", soup.title.text)

iframe = soup.find('iframe')
if iframe:
    iframe_url = iframe.get('src')
    if not iframe_url.startswith('http'):
        iframe_url = 'https://www1.river.go.jp' + iframe_url
    print("iframeのURL:", iframe_url)

    iframe_res = requests.get(iframe_url)
    iframe_res.encoding = 'EUC-JP'
    iframe_soup = BeautifulSoup(iframe_res.text, 'lxml')

    table = iframe_soup.find('table')
    if table:
        rows = table.find_all('tr')
        for row in rows:
            cols = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
            print(cols)
    else:
        print("データが見つかりませんでした")
else:
    print("データが見つかりませんでした")
