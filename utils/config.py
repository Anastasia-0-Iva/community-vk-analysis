import requests

ACCESS_TOKEN = "09ce6e1b09ce6e1b09ce6e1bc60af3786a009ce09ce6e1b60d38249e71a7d4808878917"
GROUP_URL = "https://vk.com/nordfilter"

def extract_group_name(url):
    clean_url = url.split('?')[0]
    group_name = clean_url.split('/')[-1]
    return group_name

group_name = extract_group_name(GROUP_URL)
#print(f"Ищем группу: '{group_name}'")

response = requests.get('https://api.vk.com/method/groups.getById', params={
    'group_ids': group_name,
    'access_token': ACCESS_TOKEN,
    'v': '5.131',
    'fields': 'members_count,name'
})

#print("Ответ API:", response.json())