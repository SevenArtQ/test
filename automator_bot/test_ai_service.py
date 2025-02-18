from services.ai_service import AIService
import time

def test_ai():
    test_prompts = [
        "Привет, как дела?",
        "Расскажи анекдот",
        "Что такое Python?",
        "Напиши короткое стихотворение о программировании"
    ]
    
    print("Тестируем AI сервис...")
    for prompt in test_prompts:
        print(f"\nЗапрос: {prompt}")
        try:
            response = AIService.generate_response(prompt)
            print(f"Ответ: {response}")
        except Exception as e:
            print(f"Ошибка: {str(e)}")
        
        # Небольшая пауза между запросами
        time.sleep(2)

# Запускаем тест
if __name__ == "__main__":
    test_ai() 