import g4f
import base64
import os
from datetime import datetime

def test_all_providers():
    # Путь к вашей фотографии
    image_path = r"D:\Загрузки\98ddac63a383fe536cee05094b79a58f.jpg"
    
    # Проверяем существование файла
    if not os.path.exists(image_path):
        print(f"❌ Ошибка: Файл не найден: {image_path}")
        return
        
    print(f"✅ Файл найден: {image_path}")
    
    # Читаем изображение
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Получаем все доступные провайдеры
    all_providers = []
    for provider in dir(g4f.Provider):
        if not provider.startswith('_'):  # Пропускаем внутренние атрибуты
            provider_obj = getattr(g4f.Provider, provider)
            if hasattr(provider_obj, 'create_completion'):
                all_providers.append((provider_obj, "gpt-3.5-turbo"))

    print(f"\nНайдено {len(all_providers)} провайдеров")
    print("\n🔄 Тестирование провайдеров для анализа изображений...")
    print("-" * 50)

    working_providers = []

    for provider, model in all_providers:
        try:
            print(f"\nТестируем {provider.__name__}")
            
            response = g4f.ChatCompletion.create(
                model=model,
                messages=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Что изображено на этой картинке? Ответь кратко на русском языке."
                        },
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{image_data}"
                        }
                    ]
                }],
                provider=provider
            )
            
            if response and len(str(response).strip()) > 0:
                print(f"✅ Успешно! Ответ: {str(response)[:100]}...")
                working_providers.append((provider.__name__, model))
            else:
                print("❌ Нет ответа")
                
        except Exception as e:
            print(f"❌ Ошибка: {str(e)}")

    print("\n" + "=" * 50)
    print("📊 Результаты тестирования:")
    print(f"Всего протестировано: {len(all_providers)}")
    print(f"Работает: {len(working_providers)}")
    print("\nРабочие провайдеры:")
    for name, model in working_providers:
        print(f"- {name} ({model})")

if __name__ == "__main__":
    test_all_providers() 