from utils import api
import requests


def update_table_on_load(pathname):
    if pathname == "/":
        response = requests.get(f"{api.API}/records")
        print(f"Response status: {response.status_code}")
        print(f"Response data: {response.json()}")
        if response.status_code == 200:
            return response.json()
    return []


if __name__ == "__main__":
    update_table_on_load("/")
