import os
from database import Database
from dadata_api import DadataAPI

class AddressSuggestTool:
    def __init__(self):
        self.db = Database(db_path='settings.db')
        self.api_key = self.load_api_key()
        self.dadata_api = DadataAPI(api_key=self.api_key)

    def load_api_key(self):
        api_key = self.db.get_setting("api_key")
        if not api_key:
            api_key = input("Введите ваш API ключ: ")
            self.db.set_setting("api_key", api_key)
        return api_key
    
    def update_settings_menu(self):
        print("Настройки:")
        print("1. Базовый URL к сервису dadata")
        print("2. API ключ для сервиса dadata")
        print("3. Язык (en/ru)")

    def run(self):
        while True:
            user_input = input("Введите ваш адрес (или введите 'settings' чтобы изменить параметры, или 'exit' чтобы выйти): ")

            if user_input.lower() == "exit":
                break

            if user_input.lower() == "debug":
                print(self.db.get_all())

            elif user_input.lower() == "settings":
                self.update_settings_menu()
                option = int(input("Выберите опцию для обновления (введите номер): "))
                if option == 1:
                    new_base_url = input("Введите новый базовый URL: ")
                    self.db.set_setting("base_url", new_base_url)
                elif option == 2:
                    new_api_key = input("Введите новый API ключ: ")
                    self.db.set_setting("key", new_api_key)
                elif option == 3:
                    new_language = input("Выберите новый язык (en/ru): ")
                    self.db.set_setting("language", new_language)
                else:
                    print("Некорректный выбор.")

            else:
                suggestions = self.dadata_api.suggest_address(query=user_input, language=self.db.get_setting("language"))
                self.display_suggestions(suggestions)

    def display_suggestions(self, suggestions):
        if not suggestions:
            print("Совпадений нет.")
            return

        print("Совпадения:")
        for idx, suggestion in enumerate(suggestions, start=1):
            print(f"{idx}. {suggestion['value']}")

        selected_index = input("Выберите адрес (введите номер адреса) или введите 'exit' чтобы выйти: ")

        if selected_index.lower() == "exit":
            return

        try:
            selected_index = int(selected_index)
            selected_suggestion = suggestions[selected_index - 1]
            dadata_query = selected_suggestion["unrestricted_value"]
            latitude, longitude = self.dadata_api.get_coordinates(dadata_query)
            print(f"Coordinates: Latitude {latitude}, Longitude {longitude}")
        except (ValueError, IndexError):
            print("Invalid selection. Please enter a valid number.")

if __name__ == "__main__":
    tool = AddressSuggestTool()
    tool.run()