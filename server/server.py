import json
import os

from flask import Flask, request, jsonify

app = Flask(__name__)
DATA_FILE = './server/animals.json'


def load_data():
    """
    Загружает данные из JSON-файла.
    Если файл не существует, создаёт его с пустым списком.
    """
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w') as f:
            json.dump([], f)
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        data = []
    return data


def save_data(data):
    """Сохраняет данные в JSON-файл с отступами для читаемости."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)


@app.route('/get_all', methods=['GET'])
def get_all():
    """Эндпоинт для получения списка всех животных."""
    animals = load_data()
    return jsonify(animals), 200


@app.route('/get_name/<name>', methods=['GET'])
def get_name(name):
    """Эндпоинт для получения данных питомца по имени."""
    animals = load_data()
    for pet in animals:
        if pet["Имя"] == name:
            return jsonify(pet), 200
    return jsonify({"error": "Питомец не найден"}), 404


@app.route('/create_pet', methods=['POST'])
def create_pet():
    """
    Эндпоинт для создания нового питомца.
    Ожидается JSON с полями:
      - "Животное": str
      - "Имя": str (уникально)
      - "Возраст": int
      - "Цвет глаз": str
      - "Есть ли дети": bool
    """
    new_pet = request.get_json()
    if not new_pet:
        return jsonify({"error": "Нет данных в запросе"}), 400

    required_fields = ["Животное", "Имя", "Возраст", "Цвет глаз", "Есть ли дети"]
    for field in required_fields:
        if field not in new_pet:
            return jsonify({"error": f"Отсутствует поле '{field}'"}), 400

    animals = load_data()
    # Проверяем уникальность имени
    for pet in animals:
        if pet["Имя"] == new_pet["Имя"]:
            return jsonify({"error": "Питомец с таким именем уже существует"}), 400

    animals.append(new_pet)
    save_data(animals)
    return jsonify(new_pet), 201


@app.route('/change_pet/<name>', methods=['PUT'])
def change_pet(name):
    """
    Эндпоинт для изменения данных питомца.
    Принимает JSON, содержащий один или несколько обновляемых ключей.
    Обновляет только переданные поля.
    """
    update_fields = request.get_json()
    if not update_fields:
        return jsonify({"error": "Нет данных для обновления"}), 400

    animals = load_data()
    for i, pet in enumerate(animals):
        if pet["Имя"] == name:
            pet.update(update_fields)
            animals[i] = pet
            save_data(animals)
            return jsonify(pet), 200

    return jsonify({"error": "Питомец не найден"}), 404


@app.route('/delete_pet/<name>', methods=['DELETE'])
def delete_pet(name):
    """Эндпоинт для удаления питомца по имени."""
    animals = load_data()
    for i, pet in enumerate(animals):
        if pet["Имя"] == name:
            removed_pet = animals.pop(i)
            save_data(animals)
            return jsonify(removed_pet), 200
    return jsonify({"error": "Питомец не найден"}), 404


if __name__ == '__main__':
    app.run(debug=True)
