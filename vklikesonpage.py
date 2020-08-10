import json, time
from requests import get, post

VK_TOKEN_5122 = "" # 5.122 + permission for photos

BASE_QUERY_LINK = "https://api.vk.com/method/"

def add_param(url, name, value, is_first):
    if is_first:
        return url + name + "=" + value
    return url + "&" + name + "=" + value

def get_user_id_by_short_link(short_link):
    global BASE_QUERY_LINK, VK_TOKEN_5122
    cur_url = BASE_QUERY_LINK + "users.get?"
    cur_url = add_param(cur_url, "user_ids", short_link, 1)
    cur_url = add_param(cur_url, "v", "5.122", 0)
    cur_url = add_param(cur_url, "access_token", VK_TOKEN_5122, 0)
    response = get(cur_url)
    user_json = json.loads(response.text)["response"][0]
    return user_json["id"]

def get_list_of_photos(user_id):
    global BASE_QUERY_LINK, VK_TOKEN_5122
    cur_url = BASE_QUERY_LINK + "photos.getAll?"
    cur_url = add_param(cur_url, "v", "5.122", 1)
    cur_url = add_param(cur_url, "access_token", VK_TOKEN_5122, 0)
    cur_url = add_param(cur_url, "owner_id", str(user_id), 0)
    response = get(cur_url)
    photos_json = json.loads(response.text)["response"]["items"]
    list_of_ids = []
    for item in photos_json:
        list_of_ids.append(item["id"])
    return list_of_ids

def get_persons_under_the_photo(owner_id, photo_id):
    global BASE_QUERY_LINK, VK_TOKEN_5122
    cur_url = BASE_QUERY_LINK + "likes.getList?"
    cur_url = add_param(cur_url, "v", "5.122", 1)
    cur_url = add_param(cur_url, "access_token", VK_TOKEN_5122, 0)
    cur_url = add_param(cur_url, "owner_id", str(owner_id), 0)
    cur_url = add_param(cur_url, "item_id", str(photo_id), 0)
    cur_url = add_param(cur_url, "type", "photo", 0)
    response = get(cur_url)
    list_of_users_ids = json.loads(response.text)
    if "response" in list_of_users_ids:
        list_of_users_ids = list_of_users_ids["response"]["items"]
    else:
        print("error")
        print(list_of_users_ids)
    return list_of_users_ids

def get_data_about_person_by_id(user_id):
    global BASE_QUERY_LINK, VK_TOKEN_5122
    cur_url = BASE_QUERY_LINK + "users.get?"
    cur_url = add_param(cur_url, "user_ids", str(user_id), 1)
    cur_url = add_param(cur_url, "v", "5.122", 0)
    cur_url = add_param(cur_url, "access_token", VK_TOKEN_5122, 0)
    response = get(cur_url)
    user_json = json.loads(response.text)["response"][0]
    return user_json["first_name"] + " " + user_json["last_name"]

def main():
    link = str(input("Введи короткий адрес страницы человека : ").strip())
    query_user_id = get_user_id_by_short_link(link)
    time.sleep(1)
    list_of_ids = get_list_of_photos(query_user_id)
    time.sleep(1)
    user_id_to_count_of_likes = {}
    for i in range(len(list_of_ids)):
        list_of_users_ids = get_persons_under_the_photo(query_user_id, list_of_ids[i])
        time.sleep(0.25)
        for user_id in list_of_users_ids:
            if user_id in user_id_to_count_of_likes:
                user_id_to_count_of_likes[user_id] += 1
            else:
                user_id_to_count_of_likes[user_id] = 1
    sorted_names_by_like = []
    for user_id in list(user_id_to_count_of_likes.keys()):
        name = get_data_about_person_by_id(user_id)
        time.sleep(0.25)
        sorted_names_by_like.append([user_id_to_count_of_likes[user_id], name, user_id])

    sorted_names_by_like.sort()
    sorted_names_by_like = sorted_names_by_like[::-1]
    pos = 1
    for person in sorted_names_by_like:
        print("#" + str(pos) + ". " + str(person[1]) + " " + str(person[0]) + " vk.com/id" + str(person[2]))
        pos += 1

main()




