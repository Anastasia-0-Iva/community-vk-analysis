import requests
from datetime import datetime
from utils.config import ACCESS_TOKEN
from utils.user_ID import get_all_subscribers

all_members = get_all_subscribers()

def get_user_details(all_members):
    all_data = []

    for i in range(0, len(all_members), 100):
        data = all_members[i:i+100]

        #Запрос к API
        response = requests.get('https://api.vk.com/method/users.get', params={
            'user_ids': ','.join(str(id) for id in data),
            'fields': 'bdate,sex,city',
            'access_token': ACCESS_TOKEN,
            'v': '5.131'

        })

        response_data = response.json()

        if 'response' in response_data:
            all_data.extend(response_data['response'])

    return all_data

#Разделяем по полу и подсчитываем пользователей
def count_genders(all_data):
    man = 0
    woman = 0
    for user  in all_data:
        if user['sex'] == 1:
            woman += 1
        elif user['sex'] == 2:
            man += 1
    return man, woman

#Вычисляем возраст по дате рождения и разделяем по полу
def count_age(all_data):
    man_age = []
    woman_age = []
    for user in all_data:
        if 'bdate' in user and user['bdate']:
            bdate_str = user['bdate']

            try:
                birth_date = datetime.strptime(bdate_str, '%d.%m.%Y')
                today = datetime.now()
                age = today.year - birth_date.year

                if today.month < birth_date.month or (today.month == birth_date.month and today.day < birth_date.day):
                    age -= 1

                if user.get('sex') == 1:
                    woman_age.append(age)
                elif user.get('sex') == 2:
                    man_age.append(age)
            except:
                user['age'] = None
    return man_age, woman_age

#Получаем города пользователей
def count_city(all_data):
    city_dict = {}

    for user in all_data:
        if 'city' in user and user['city']:
            city_name = user['city']['title']
            if city_name in city_dict:
                city_dict[city_name] += 1
            else:
                city_dict[city_name] = 1
    return city_dict



if __name__ == "__main__":
    #Данные пользователей
    user_data = get_user_details(all_members)

    #Анализ по полу
    men_count, women_count = count_genders(user_data)
    total_gender = men_count + women_count

    men_percent = (men_count / total_gender) * 100 if total_gender > 0 else 0
    women_percent = (women_count / total_gender) * 100 if total_gender > 0 else 0

    print(f"Мужчины: {men_count} ({men_percent:.1f}%)")
    print(f"Женщины: {women_count} ({women_percent:.1f}%)")

    #Средний возраст
    men_ages, women_ages = count_age(user_data)
    if men_ages:
        print(f"Средний возраст мужчин: {sum(men_ages) / len(men_ages):.0f}")
    if women_ages:
        print(f"Средний возраст женщин: {sum(women_ages) / len(women_ages):.0f}")

    #Анализ городов
    cities = count_city(user_data)
    total = sum(cities.values())
    for city, count in sorted(cities.items(), key=lambda x: x[1], reverse=True):
        print(f"   {city}: {count} ({count / total * 100:.1f}%)")

    #Можно посмотреть только топ-10 городов

    #top_cities = sorted(cities.items(), key=lambda x: x[1], reverse=True)[:10]
    #top10_total = sum(count for city, count in top_cities)
    #for city, count in top_cities:
    #    print(f"   {city}: {count} ({count / top10_total * 100:.1f}%)")




