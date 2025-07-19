from pymongo import MongoClient
from pymongo.server_api import ServerApi
import atexit

client = MongoClient(
    "mongodb+srv://de07:QZ7LB0Imy5xcYc8z@cluster0.zl0sgnm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

db = client["test"]
collection = db["cats"]

def get_all_cats():
    """Повертає всі документи з колекції."""
    try:
        if collection.count_documents({}) == 0:
            raise ValueError("No documents found")
        return collection.find({})
    except Exception as e:
        print(f"Error fetching all cats: {e}")
        return []

def find_cat_by_name(name):
    """Повертає документ кота за ім'ям."""
    try:
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        return collection.find_one({"name": name})
    except Exception as e:
        print(f"Error finding cat by name: {e}")
        return None

def update_cat_age_by_name(name, age):
    """Оновлює вік кота за ім'ям."""
    try:
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a non-negative integer")
        return collection.update_one({"name": name}, {"$set": {"age": age}})
    except Exception as e:
        print(f"Error updating cat age: {e}")
        return None

def add_new_feature(name, feature):
    """Додає нову властивість до документу за ім'ям."""
    try:
        if not isinstance(feature, str):
            raise ValueError("Feature must be a string")
        return collection.update_one({"name": name}, {"$push": {"features": feature}})
    except Exception as e:
        print(f"Error adding new feature: {e}")
        return None

def delete_document(name):
    """Видаляє документ з колекції за ім'ям."""
    try:
        if not isinstance(name, str):
            raise ValueError("Name must be a string")
        return collection.delete_one({"name": name})
    except Exception as e:
        print(f"Error deleting document: {e}")
        return None


def delete_all():
    """Видаляє всі документи з колекції."""
    try:
        if collection.estimated_document_count() == 0:
            raise ValueError("No documents to delete")
        return collection.delete_many({})
    except Exception as e:
        print(f"Error deleting all documents: {e}")
        return None


#Виведення всіх записів із колекції
print("📄 Show all cats:")

cats = get_all_cats()
if cats:
    for cat in cats:
        print(cat)
else:
    print("No cats found.")

#Інформація про кота за ім'ям
print("\n🔍 Find cat by name:")
cat_name = "Murka"
cat = find_cat_by_name(cat_name)
if cat:
    print(f"Cat found: {cat}")
else:
    print(f"No cat found with name {cat_name}.")

#Оновлення віку кота
print("\n🔄 Update cat age:")
age_update = update_cat_age_by_name(cat_name, 5)
if age_update and age_update.modified_count > 0:
    print(f"Cat {cat_name} age updated successfully.")
else:
    print(f"Failed to update age for cat {cat_name}.")

#Додавання нової властивості до кота
print("\n➕ Add new feature to cat:")
feature_add = add_new_feature(cat_name, "Loves to chase laser pointers")
if feature_add and feature_add.modified_count > 0:
    print(f"Feature added to cat {cat_name} successfully.")
else:
    print(f"Failed to add feature to cat {cat_name}.")

#Видалення документа за ім'ям
print("\n🗑️ Delete document by name:")
delete_result = delete_document(cat_name)
if delete_result and delete_result.deleted_count > 0:
    print(f"Document for cat {cat_name} deleted successfully.")
else:
    print(f"Failed to delete document for cat {cat_name}.")

#Видалення всіх документів з колекції
print("\n🗑️ Delete all documents:")
delete_all_result = delete_all()
if delete_all_result and delete_all_result.deleted_count > 0:
    print("All documents deleted successfully.")
else:
    print("No documents to delete or deletion failed.")


#Закриття з'єднання з MongoDB при завершенні програми
atexit.register(client.close)