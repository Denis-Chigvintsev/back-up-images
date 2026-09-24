import io, sys
import requests
import json
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

text = input("введите текст , который будет отображен на картинке: ")

url = f"https://cataas.com/cat/says/{text}"

try:
    response = requests.get(url)
except:
    print(f"данные кошечного API не подошли- выхожу из программы")
    sys.exit()
if response.status_code != 200:
    print(
        f"данные кошечного API не подошли- выхожу из программы {response.status_code}"
    )
    sys.exit()

image = response.content

filename = f"./AIE-8/{text}.jpg"

current_dir = Path().cwd()


with open(".token", encoding="utf-8") as f:
    token = f.read()

with open(f"{filename}", "wb") as f:
    f.write(image)

params = {"path": "AIE-8"}

y_url = "https://cloud-api.yandex.net/v1/disk/resources"


headers = {"Authorization": f"OAuth {token}"}

response = requests.put(y_url, params=params, headers=headers)

params = {
    "path": f"AIE-8/{text}.jpg",
    "overwrite": True,
}

response = requests.get(f"{y_url}/upload", headers=headers, params=params)

upload_url = response.json()["href"]

with open(f"{filename}", "rb") as f:
    requests.put(upload_url, files={"file": f})

data = {
    "filename_relative": filename,
    "file_size": Path(f"{current_dir}/AIE-8/{text}.jpg").stat().st_size,
}

if Path(f"{current_dir}/AIE-8/file_stat.json").exists() == True:
    with open(
        f"{current_dir}/AIE-8/file_stat.json",
        "r",
        encoding="utf-8",
    ) as f:
        full_data = json.load(f)
        full_data.append(data)
else:
    full_data = [data]

with open(
    f"{current_dir}/AIE-8/file_stat.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(full_data, f, ensure_ascii=False, indent=2)
