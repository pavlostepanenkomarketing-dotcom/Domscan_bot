import requests

def estimate_price(name, acr, bl, aby):
    score = 0
    length = len(name)

    # 1. Длина имени домена
    if length <= 3:
        score += 35
    elif length <= 5:
        score += 25

    # 2. Возраст домена
    if aby and aby > 0:
        age = 2025 - aby
        if age >= 15:
            score += 25
        elif age >= 10:
            score += 15

    # 3. ACR — авторитет домена
    if acr >= 40:
        score += 30
    elif acr >= 25:
        score += 20

    # 4. Backlinks — обратные ссылки
    if bl >= 10:
        score += 12
    elif bl >= 3:
        score += 5

    # 5. Конвертация баллов → цена
    if score >= 90:
        return 80000
    elif score >= 80:
        return 50000
    elif score >= 70:
        return 30000
    elif score >= 60:
        return 20000
    elif score >= 50:
        return 10000
    return 3000


def load_domains():
    """
    В ЭТОМ МЕСТЕ потом вставим ссылку на твой CSV с peew.de.
    Пока стоит временный demo-файл.
    """

    url = "https://raw.githubusercontent.com/datasets/url-short-domain-list/main/data/domains.csv"

    try:
        data = requests.get(url, timeout=10).text.split("\n")
    except:
        return []

    domains = []
    for row in data[1:50]:  # для примера берем 50 строк
        parts = row.split(",")

        if len(parts) < 1:
            continue

        domain = parts[0]
        name = domain.split(".")[0]

        # временные значения (позже заменим на реальные)
        acr = len(name) * 3
        bl = len(name) % 7
        aby = 2010

        price = estimate_price(name, acr, bl, aby)

        if price >= 20000:
            domains.append({
                "domain": domain,
                "price": price,
                "acr": acr,
                "bl": bl,
                "aby": aby
            })

    return domains
