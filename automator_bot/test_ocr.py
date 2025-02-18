import os

from services.ai_service import AIService

def test_ocr():
    # Используем существующий файл из папки images
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, "images", "photo_20250217_001719.jpg")
    
    print(f"Путь к изображению: {image_path}")
    print("🔄 Тестирование OCR...")
    
    # Проверяем существование файла
    if not os.path.exists(image_path):
        print(f"❌ Файл не найден: {image_path}")
        return
        
    print("✅ Файл найден")
    result = AIService.analyze_image(image_path)
    print("\n📝 Результат:")
    print(result)

if __name__ == "__main__":
    test_ocr() 