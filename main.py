import io, sys
import requests
import json
from pathlib import Path
from halo import Halo

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


class CataasClient:

    URL = "https://cataas.com/cat"
    FILE_DIR = "./AIE-8"
    CURRENT_DIR = Path().cwd()

    def __init__(self, text):
        self.text = text

    def get_json(self):
        spinner = Halo(text="файл с надписью готовится к скачиванию")
        spinner.start()
        url = f"{self.URL}/says/{self.text}"
        headers = {"Accept": "application/json"}
        try:
            response = requests.get(url, headers=headers)

        except requests.HTTPError as http_err:
            print(f"HTTP ошибка (код {response.status_code}): {http_err}")
            sys.exit()
        except ConnectionError as conn_err:
            print(f"Ошибка подключения к серверу: {conn_err}")
            sys.exit()
        except requests.Timeout as time_err:
            print(f"Время ожидания ответа истекло: {time_err}")
            sys.exit()
        except requests.RequestException as req_err:
            print(f"Общая ошибка при обработке запроса: {req_err}")
            sys.exit()
        except ValueError:
            print("структура данных от АПИ неправильная")
            sys.exit()
        except:
            print(f"прочая ошибка   (код {response.status_code}  ")
            sys.exit()

        image_url = response.json()["url"]

        spinner.succeed("файл готов к скачиванию")
        return image_url

    def write_photo(self, image_url):
        spinner = Halo(
            text="теперь загружаю из интернета на Ваш компьютер фото кошки с Вашей надписью",
            spinner="arrow",
        )
        spinner.start()

        try:
            response = requests.get(image_url)

        except requests.HTTPError as http_err:
            print(f"HTTP ошибка (код {response.status_code}): {http_err}")
            sys.exit()
        except ConnectionError as conn_err:
            print(f"Ошибка подключения к серверу: {conn_err}")
            sys.exit()
        except requests.Timeout as time_err:
            print(f"Время ожидания ответа истекло: {time_err}")
            sys.exit()
        except requests.RequestException as req_err:
            print(f"Общая ошибка при обработке запроса: {req_err}")
            sys.exit()
        except ValueError:
            print("структура данных от АПИ неправильная")
            sys.exit()
        except:
            print(f"прочая ошибка   (код {response.status_code}  ")
            sys.exit()

        image = response.content

        Path(f"{self.FILE_DIR}").mkdir(parents=True, exist_ok=True)

        filename = f"{self.FILE_DIR}/{self.text}.jpg"

        with open(filename, "wb") as f:
            f.write(image)

        data = {
            "filename_relative": filename,
            "file_size": Path(f"{self.CURRENT_DIR}/AIE-8/{text}.jpg").stat().st_size,
        }

        if Path(f"{self.CURRENT_DIR}/AIE-8/file_stat.json").exists() == True:
            with open(
                f"{self.CURRENT_DIR}/AIE-8/file_stat.json",
                "r",
                encoding="utf-8",
            ) as f:
                full_data = json.load(f)
                full_data.append(data)
        else:
            full_data = [data]

        with open(
            f"{self.CURRENT_DIR}/AIE-8/file_stat.json",
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(full_data, f, ensure_ascii=False, indent=2)

        spinner.succeed("файл на Ваш компьютер загружен")


class Yandex:

    Y_URL = "https://cloud-api.yandex.net/v1/disk/resources"

    FOLDER_EXISTS = False

    def __init__(self, token):
        self.token = token

    def write_to_ydisk(self, text, image_url):

        spinner = Halo(
            text="теперь пытаюсь записать файл на яндекс диск", spinner="arrow"
        )
        spinner.start()

        params = {"path": "AIE-8"}

        headers = {"Authorization": f"OAuth {self.token}"}

        try:
            response = requests.put(self.Y_URL, params=params, headers=headers)

        except requests.HTTPError as http_err:
            print(f"HTTP ошибка (код {response.status_code}): {http_err}")
            sys.exit()
        except ConnectionError as conn_err:
            print(f"Ошибка подключения к серверу: {conn_err}")
            sys.exit()
        except requests.Timeout as time_err:
            print(f"Время ожидания ответа истекло: {time_err}")
            sys.exit()
        except requests.RequestException as req_err:
            print(f"Общая ошибка при обработке запроса: {req_err}")
            sys.exit()
        except ValueError:
            print("структура данных от АПИ неправильная")
            sys.exit()
        except:
            print(f"прочая ошибка   (код {response.status_code}  ")
            sys.exit()

        if response.status_code == 409:
            self.FOLDER_EXISTS = True

        params = {
            "url": image_url,
            "path": f"AIE-8/{text}.jpg",
        }

        try:
            response = requests.post(
                f"{self.Y_URL}/upload", headers=headers, params=params
            )

        except requests.HTTPError as http_err:
            print(f"HTTP ошибка (код {response.status_code}): {http_err}")
            sys.exit()
        except ConnectionError as conn_err:
            print(f"Ошибка подключения к серверу: {conn_err}")
            sys.exit()
        except requests.Timeout as time_err:
            print(f"Время ожидания ответа истекло: {time_err}")
            sys.exit()
        except requests.RequestException as req_err:
            print(f"Общая ошибка при обработке запроса: {req_err}")
            sys.exit()
        except ValueError:
            print("структура данных от АПИ неправильная")
            sys.exit()
        except:
            print(f"прочая ошибка   (код {response.status_code}  ")
            sys.exit()

        if self.FOLDER_EXISTS == False:
            spinner.succeed(
                f"файл пошел к Вам на яндекс диск - статус ответа: {response.status_code}"
            )
        else:
            spinner.succeed(f"""Папка на яндекс диске AIE-8 уже была создана раньше. 
    поэтому записываю в уже существующую папку 
    сейчас файл уходит к Вам на яндекс диск 
    До свидания!""")


if __name__ == "__main__":

    text = input("введите текст , который будет отображен на картинке: ")

    catas = CataasClient(text)

    image_url = catas.get_json()

    catas.write_photo(image_url)

    with open(".token", encoding="utf-8") as f:
        token = f.read()

    yandex = Yandex(token)

    yandex.write_to_ydisk(text, image_url)
