from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests

def update_b_label(event):
    # Получаем полное название базовой валюты из словаря и обновляем метку
    code = b_combobox.get()
    name = currencies[code]
    b_label.config(text=name) # Обновляем текст метки


def update_t_label(event):
    # Получаем полное название целевой валюты из словаря и обновляем метку
    code = t_combobox.get()
    name = cur[code]
    t_label.config(text=name)



# определяем функцию exchange для получения курса обмена
def exchange():
    target_code = target_combobox.get().strip()  # получаем и очищаем код целевой валюты
    base_code = base_combobox.get().strip()  # получаем и очищаем код базовой валюты

    if target_code and base_code:  # проверяем, что обе валюты выбраны
        try:  # начинаем блок обработки исключений
            # CoinGecko API v3 — бесплатный эндпоинт
            url = 'https://api.coingecko.com/api/v3/simple/price'  # задаём URL API CoinGecko
            params = {  # создаём словарь с параметрами запроса
                'ids': target_code + ',' + base_code,  # указываем ID двух валют через запятую
                'vs_currencies': 'usd',  # запрашиваем цены в долларах США
                'include_exchange_rate': 'true'  # включаем курс обмена в ответ
            }

            response = requests.get(url, params=params)  # отправляем GET-запрос на сервер
            response.raise_for_status()  # выбрасывает ошибку, если статус ответа не 200
            data = response.json()  # парсим ответ сервера в формат JSON

            # Получаем цены в USD
            target_price_usd = data[target_code]['usd']  # получаем цену целевой валюты в USD
            base_price_usd = data[base_code]['usd']  # получаем цену базовой валюты в USD

            # Рассчитываем кросс-курс
            exchange_rate = target_price_usd / base_price_usd  # вычисляем курс обмена

            base_name = currencies[base_code]  # получаем название базовой валюты из словаря
            target_name = currencies[target_code]  # получаем название целевой валюты из словаря

            mb.showinfo('Курс обмена',  # показываем всплывающее окно с информацией
                        f'1 {base_name} = {exchange_rate:.6f} {target_name}\n'  # строка: 1 базовая = курс целевая
                        f'1 {target_name} = {1/exchange_rate:.6f} {base_name}')  # строка: 1 целевая = курс базовая

        except Exception as er:  # перехватываем любую ошибку
            mb.showerror('Ошибка', str(er))  # показываем всплывающее окно с текстом ошибки
    else:  # если одна из валют не выбрана
        mb.showwarning('Внимание', 'Выберите валюты')  # показываем предупреждение

# Словарь кодов валют и их полных названий
currencies = {
    "USD": "Американский доллар",
    "EUR": "Евро",
    "JPY": "Японская йена",
    "GBP": "Британский фунт стерлингов",
    "AUD": "Австралийский доллар",
    "CAD": "Канадский доллар",
    "CHF": "Швейцарский франк",
    "CNY": "Китайский юань",
    "RUB": "Российский рубль",
    "KZT": "Казахстанский тенге",
    "UZS": "Узбекский сум"
}

# Создание графического интерфейса
window = Tk()
window.title("Курс обмена валюты")
window.geometry("360x300")

Label(text="Базовая валюта:").pack(padx=10, pady=5)
base_combobox = ttk.Combobox(values=list(currencies.keys()))
base_combobox.pack(padx=10, pady=5)
base_combobox.bind("<<ComboboxSelected>>", update_b_label)

b_label = ttk.Label()
b_label.pack(padx=10, pady=10)

Label(text="Целевая валюта:").pack(padx=10, pady=5)
target_combobox = ttk.Combobox(values=list(currencies.keys()))
target_combobox.pack(padx=10, pady=5)
target_combobox.bind("<<ComboboxSelected>>", update_t_label)

t_label = ttk.Label()
t_label.pack(padx=10, pady=10)

Button(text="Получить курс обмена", command=exchange).pack(padx=10, pady=10)

window.mainloop()
