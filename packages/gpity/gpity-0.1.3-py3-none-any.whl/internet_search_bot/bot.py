# internet_search_bot/bot.py
import os
import json
import requests
from deep_translator import GoogleTranslator

class InternetSearchBot:
    def __init__(self):
        self.learning_data = "learning_data.json"
        self.load_learning_data()

    def load_learning_data(self):
        """Загружает сохранённые данные обучения."""
        if os.path.exists(self.learning_data):
            with open(self.learning_data, "r", encoding="utf-8") as file:
                self.learning = json.load(file)
        else:
            self.learning = {}

    def save_learning_data(self):
        """Сохраняет данные обучения в файл."""
        with open(self.learning_data, "w", encoding="utf-8") as file:
            json.dump(self.learning, file, ensure_ascii=False, indent=4)

    def search_internet(self, query):
        """Ищет информацию в интернете с помощью DuckDuckGo API."""
        try:
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1,  # Убираем HTML-теги из результатов
                "no_redirect": 1,
            }
            response = requests.get(url, params=params)
            data = response.json()

            # Возвращаем первый результат (краткое описание)
            if data.get("AbstractText"):
                return data["AbstractText"]
            elif data.get("RelatedTopics"):
                for topic in data["RelatedTopics"]:
                    if topic.get("Text"):
                        return topic["Text"]
            else:
                return None
        except Exception as e:
            print(f"Ошибка при поиске в интернете: {e}")
            return None

    def get_response(self, user_input):
        """Генерирует ответ на основе ввода пользователя."""
        user_input = user_input.lower()

        # Переводим запрос на английский, если он на русском
        if not self.is_english(user_input):
            translated_query = GoogleTranslator(source='ru', target='en').translate(user_input)
        else:
            translated_query = user_input

        # Если ответ уже есть в сохранённых данных, используем его
        if translated_query in self.learning:
            return self.learning[translated_query]

        # Иначе ищем информацию в интернете
        search_result = self.search_internet(translated_query)
        if search_result:
            # Переводим ответ на русский
            translated_result = GoogleTranslator(source='en', target='ru').translate(search_result)
            # Сохраняем найденную информацию для будущего использования
            self.learning[translated_query] = translated_result
            self.save_learning_data()
            return translated_result
        else:
            return "Извините, я не смог найти информацию по вашему запросу."

    def is_english(self, text):
        """Проверяет, является ли текст на английском языке."""
        return all(ord(c) < 128 for c in text)
