import requests
import time
from utils.config import ACCESS_TOKEN

def get_subscribers():
    response = requests.get('https://api.vk.com/method/groups.getMembers', params={
        'group_id': 140592125,
        'access_token': ACCESS_TOKEN,
        'v': '5.131',
        'count':1000
    })
    return response


def get_all_subscribers():
    first_response = get_subscribers()

    response_data = first_response.json()
    if 'error' in response_data:
        print("Ошибка API:", response_data['error']['error_msg'])
        return []


    total_count = response_data['response']['count']
    #print(f"Всего участников: {total_count}")

    all_members = []

    for offset in range(0, total_count, 1000):
        count = min(1000, total_count - offset)

        response = requests.get('https://api.vk.com/method/groups.getMembers', params={
            'group_id': 140592125,
            'access_token': ACCESS_TOKEN,
            'v': '5.131',
            'count': count,
            'offset': offset
        })

        time.sleep(1)

        new_members = response.json()['response']['items']
        all_members.extend(new_members)
        #print(f"Получено {len(new_members)} участников, offset = {offset}")

    return all_members




result = get_all_subscribers()
print(f"Всего собрано: {len(result)} участников")
#for i, user_id in enumerate(result[:20]):  # первые 20
#    print(f"{i+1}. {user_id}")

if __name__ == "__main__":
    all_members = result





