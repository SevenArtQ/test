import pandas as pd
import os
from datetime import datetime
import io

class ExcelService:
    EXCEL_DIR = "excel_files"
    
    @staticmethod
    async def read_excel(file_path: str) -> str:
        """Чтение Excel файла и возврат информации о нем"""
        try:
            df = pd.read_excel(file_path)
            info = (
                f"📊 Информация о файле:\n"
                f"Количество строк: {len(df)}\n"
                f"Количество столбцов: {len(df.columns)}\n"
                f"Столбцы: {', '.join(df.columns)}\n\n"
                f"Первые 5 строк:\n{df.head().to_string()}"
            )
            return info
        except Exception as e:
            print(f"Ошибка при чтении Excel файла: {e}")
            return "Ошибка при чтении файла"
            
    @staticmethod
    async def edit_excel(file_path: str, commands: str) -> str:
        """Редактирование Excel файла на основе команд"""
        try:
            df = pd.read_excel(file_path)
            
            # Разбираем команды
            if "сортировать" in commands.lower():
                column = commands.split("по")[1].strip()
                df = df.sort_values(by=column)
            
            elif "фильтровать" in commands.lower():
                condition = commands.split("где")[1].strip()
                df = df.query(condition)
                
            elif "добавить столбец" in commands.lower():
                column_name = commands.split("столбец")[1].strip()
                df[column_name] = ""
                
            elif "удалить столбец" in commands.lower():
                column_name = commands.split("столбец")[1].strip()
                df = df.drop(columns=[column_name])
            
            # Сохраняем изменения
            output_path = f"{ExcelService.EXCEL_DIR}/edited_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            os.makedirs(ExcelService.EXCEL_DIR, exist_ok=True)
            df.to_excel(output_path, index=False)
            
            return output_path
        except Exception as e:
            print(f"Ошибка при редактировании Excel файла: {e}")
            return "Ошибка при редактировании файла"
            
    @staticmethod
    async def create_excel(data: str) -> str:
        """Создание нового Excel файла из данных"""
        try:
            # Парсим данные из текста
            lines = data.strip().split('\n')
            headers = lines[0].split(',')
            rows = [line.split(',') for line in lines[1:]]
            
            df = pd.DataFrame(rows, columns=headers)
            
            # Сохраняем файл
            output_path = f"{ExcelService.EXCEL_DIR}/new_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
            os.makedirs(ExcelService.EXCEL_DIR, exist_ok=True)
            df.to_excel(output_path, index=False)
            
            return output_path
        except Exception as e:
            print(f"Ошибка при создании Excel файла: {e}")
            return "Ошибка при создании файла" 