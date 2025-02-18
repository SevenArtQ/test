import g4f

def test_all_combinations():
    providers = [
        g4f.Provider.GptGo,
        g4f.Provider.Bing,
        g4f.Provider.GeekGpt,
        g4f.Provider.Aichat,
        g4f.Provider.ChatgptDemo,
        g4f.Provider.OnlineGpt,
        g4f.Provider.AiChatOnline,
        g4f.Provider.Phind
    ]
    
    models = [
        "gpt-3.5-turbo",
        "gpt-4",
        "claude-2",
        "gemini-pro",
        "llama-2",
        "palm"
    ]
    
    working_combinations = []
    
    for provider in providers:
        print(f"\nТестируем провайдера: {provider.__name__}")
        for model in models:
            print(f"  Модель: {model}")
            try:
                response = g4f.ChatCompletion.create(
                    model=model,
                    messages=[{"role": "user", "content": "Привет, как дела?"}],
                    provider=provider,
                    stream=False
                )
                print(f"  Ответ: {response}")
                working_combinations.append((provider.__name__, model))
            except Exception as e:
                print(f"  Ошибка: {str(e)}")
    
    return working_combinations

# Запускаем тест
working_combinations = test_all_combinations()

print("\nРабочие комбинации:")
for provider, model in working_combinations:
    print(f"Провайдер: {provider}, Модель: {model}")

if not working_combinations:
    print("\nНе нашли работающих комбинаций") 