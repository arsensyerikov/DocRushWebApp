from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import httpx

app = FastAPI()

# Підключення статичних файлів (не буде використовуватися для CSS, оскільки стилі будуть вбудовані)
app.mount("/static", StaticFiles(directory="static"), name="static")

API_KEY = "2dbeea3765300ed7ea3b5d6c0034d3d9"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Додаємо список міст і курортів України
CITIES = [
    "Київ", "Львів", "Одеса", "Харків", "Дніпро", "Запоріжжя", "Миколаїв", "Чернівці", 
    "Полтава", "Херсон", "Черкаси", "Рівне", "Івано-Франківськ", "Суми", "Житомир", 
    "Тернопіль", "Луцьк", "Кропивницький", "Хмельницький", "Ужгород", "Кам'янець-Подільський"
]

RESORTS = [
    "Трускавець", "Поляниця", "Затока", "Ялта", "Алушта", "Євпаторія", "Бердянськ", 
    "Скадовськ", "Генічеськ", "Коктебель", "Луганськ", "Одеса", "Залізний Порт"
]

async def get_weather(city: str):
    # Формуємо запит до OpenWeather API
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",  # Температура в градусах Цельсія
        "lang": "uk"  # Мова — українська
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, params=params)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            return None

@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""
    <html>
        <head>
            <title>Погода в Україні</title>
            <style>
                /* Загальні стилі */
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(to bottom, #4facfe, #00f2fe);
                    color: #333;
                    text-align: center;
                    line-height: 1.6;
                }}

                header {{
                    background-color: rgba(0, 0, 0, 0.5);
                    color: #ffffff;
                    padding: 20px 0;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }}

                h1, h2, p {{
                    margin: 20px 0;
                }}

                ul {{
                    list-style: none;
                    padding: 0;
                    margin: 20px auto;
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                }}

                ul li {{
                    margin: 10px;
                }}

                a {{
                    text-decoration: none;
                    color: #ffffff;
                    font-weight: bold;
                    background: rgba(0, 0, 0, 0.3);
                    padding: 10px 20px;
                    border-radius: 20px;
                    transition: all 0.3s ease;
                }}

                a:hover {{
                    background: rgba(255, 255, 255, 0.2);
                    transform: scale(1.1);
                }}

                .weather-info {{
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                    display: inline-block;
                    margin: 20px;
                    text-align: left;
                }}

                .weather-info h2 {{
                    margin-bottom: 10px;
                }}

                .weather-info p {{
                    font-size: 1.2rem;
                }}

                img {{
                    width: 100px;
                    height: 100px;
                }}

                footer {{
                    margin-top: 40px;
                    font-size: 0.9rem;
                    color: rgba(255, 255, 255, 0.7);
                }}
            </style>
        </head>
        <body>
            <header>
                <h1>Погода в Україні</h1>
                <p>Дізнайтесь актуальну погоду у містах і курортах України</p>
            </header>
            <main>
                <h2>Пошук:</h2>
                <input type="text" id="searchInput" onkeyup="search()" placeholder="Пошук міста чи курорту..." />
                <h2>Категорії:</h2>
                <h3>Міста України:</h3>
                <ul id="citiesList">
                    <!-- Міста будуть додані сюди через JavaScript -->
                </ul>
                <h3>Курорти України:</h3>
                <ul id="resortsList">
                    <!-- Курорти будуть додані сюди через JavaScript -->
                </ul>
            </main>
            <footer>
                <p>© 2024 Сайт про погоду в Україні</p>
            </footer>
        </body>
        <script>
            const cities = {CITIES};
            const resorts = {RESORTS};

            function displayList() {{
                const cityList = document.getElementById('citiesList');
                const resortList = document.getElementById('resortsList');
                
                cityList.innerHTML = cities.map(city => `<li><a href="/weather?city=${{city}}">${{city}}</a></li>`).join('');
                resortList.innerHTML = resorts.map(resort => `<li><a href="/weather?city=${{resort}}">${{resort}}</a></li>`).join('');
            }}

            function search() {{
                const input = document.getElementById('searchInput').value.toLowerCase();
                const filteredCities = cities.filter(city => city.toLowerCase().includes(input));
                const filteredResorts = resorts.filter(resort => resort.toLowerCase().includes(input));

                const cityList = document.getElementById('citiesList');
                const resortList = document.getElementById('resortsList');

                cityList.innerHTML = filteredCities.map(city => `<li><a href="/weather?city=${{city}}">${{city}}</a></li>`).join('');
                resortList.innerHTML = filteredResorts.map(resort => `<li><a href="/weather?city=${{resort}}">${{resort}}</a></li>`).join('');
            }}

            // Відображаємо списки на сторінці при завантаженні
            displayList();
        </script>
    </html>
    """

@app.get("/weather", response_class=HTMLResponse)
async def weather(city: str):
    weather_data = await get_weather(city)
    
    if weather_data:
        name = weather_data['name']
        temp = weather_data['main']['temp']
        weather_desc = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon}.png"
        return f"""
        <html>
            <head>
                <title>Погода в {name}</title>
                <style>
                    /* Всі стилі для сторінки погоди */
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background: linear-gradient(to bottom, #4facfe, #00f2fe);
                        color: #333;
                        text-align: center;
                        line-height: 1.6;
                    }}

                    header {{
                        background-color: rgba(0, 0, 0, 0.5);
                        color: #ffffff;
                        padding: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }}

                    .weather-info {{
                        background-color: #ffffff;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                        display: inline-block;
                        margin: 20px;
                        text-align: left;
                    }}

                    .weather-info h2 {{
                        margin-bottom: 10px;
                    }}

                    .weather-info p {{
                        font-size: 1.2rem;
                    }}

                    img {{
                        width: 100px;
                        height: 100px;
                    }}

                    footer {{
                        margin-top: 40px;
                        font-size: 0.9rem;
                        color: rgba(255, 255, 255, 0.7);
                    }}
                </style>
            </head>
            <body>
                <header>
                    <h1>Погода в {name}</h1>
                </header>
                <main>
                    <div class="weather-info">
                        <h2>Температура: {temp}°C</h2>
                        <p>Опис: {weather_desc}</p>
                        <img src="{icon_url}" alt="Weather icon">
                    </div>
                    <a href="/">Назад до головної сторінки</a>
                </main>
                <footer>
                    <p>© 2024 Сайт про погоду в Україні</p>
                </footer>
            </body>
        </html>
        """
    else:
        return f"""
        <html>
            <head>
                <title>Помилка</title>
                <style>
                    /* Всі стилі для сторінки помилки */
                    body {{
                        font-family: Arial, sans-serif;
                        margin: 0;
                        padding: 0;
                        background: linear-gradient(to bottom, #4facfe, #00f2fe);
                        color: #333;
                        text-align: center;
                        line-height: 1.6;
                    }}

                    header {{
                        background-color: rgba(0, 0, 0, 0.5);
                        color: #ffffff;
                        padding: 20px 0;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                    }}

                    footer {{
                        margin-top: 40px;
                        font-size: 0.9rem;
                        color: rgba(255, 255, 255, 0.7);
                    }}
                </style>
            </head>
            <body>
                <header>
                    <h1>Не вдалося отримати дані про погоду</h1>
                </header>
                <main>
                    <p>Вибачте, але погода для міста {city} не знайдена.</p>
                    <a href="/">Назад до головної сторінки</a>
                </main>
                <footer>
                    <p>© 2024 Сайт про погоду в Україні</p>
                </footer>
            </body>
        </html>
        """
