import requests
from bs4 import BeautifulSoup
import json

def parse_namaz_times_combined(regions, year, months, start_day, end_day):
    combined_result = {
        "regions": []
    }

    namaz_names = ["Тонг", "Қуёш", "Пешин", "Аср", "Шом", "Хуфтон"]

    for region_id, region_name in regions.items():
        print(f"📥 Загрузка: {region_name}")
        region_data = {
            "id": region_id,
            "name_uz": region_name,
            "dates": []
        }

        for month in months:
            url = f"https://islom.uz/vremyanamazov/{region_id}/{month}"
            print(f"  → {url}")
            response = requests.get(url)
            if response.status_code != 200:
                print(f"❌ Ошибка загрузки: {url}")
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", {"class": "table"})

            if not table:
                print("❌ Таблица не найдена")
                continue

            rows = table.find_all("tr")[1:]

            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 8:
                    continue

                try:
                    day = int(cols[0].text.strip())
                except ValueError:
                    continue

                if (month == months[0] and day < start_day) or (month == months[-1] and day > end_day):
                    continue

                date_str = f"{year}-{month:02d}-{day:02d}"
                times = [cols[i].text.strip() for i in range(2, 8)]

                date_entry = {
                    "date": date_str,
                    "data": [
                        {"name": namaz, "time": time}
                        for namaz, time in zip(namaz_names, times)
                    ]
                }

                region_data["dates"].append(date_entry)

        combined_result["regions"].append(region_data)

    filename = "namoz_times.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(combined_result, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Все данные сохранены в '{filename}'")


regions = {
    27: "Tashkent",
    1: "Andijan",
    4: "Bukhara",
    5: "Gulistan",
    18: "Samarkand",
    15: "Namangan",
    14: "Navoi",
    9: "Djizak",
    16: "Nukus",
    25: "Karshi",
    26: "Kokand",
    21: "Xiva",
    13: "Margilan",
    37: "Fergana",
    78: "Urgench",
    74: "Termez"
}


parse_namaz_times_combined(
    regions=regions,
    year=2025,
    months=[8,9,10,11, 12],
    start_day=10,
    end_day=31
)
