import requests
import json
import csv
import time
import random

title = {
    'id': 'id',
    'screen_name': '用户名',
    'gender': '性别',
    'statuses_count': '微博数',
    'followers_count': '粉丝数',
    'follow_count': '关注数',
    'description': '个人简介',
    'urank': '微博等级',
    'mbrank': '会员等级',
    'verified': '是否认证',
    'verified_type': '认证类型',
    'verified_reason': '认证信息',
    'text': '包含关键词微博',
    'reposts_count': '转发数',
    'comments_count': '评论数',
    'attitudes_count': '点赞数'
}


def get_json(params):
    """获取网页中json数据"""
    url = 'https://m.weibo.cn/api/container/getIndex?'
    r = requests.get(url, params=params)
    return r.json()


def get_user_info(user_id):
    """获取用户信息"""
    params = {'containerid': '100505' + str(user_id)}
    js = get_json(params)
    user_info = {}
    if js['ok']:
        info = js['data']['userInfo']
        user_info['id'] = user_id
        user_info['screen_name'] = info.get('screen_name', '')
        user_info['gender'] = info.get('gender', '')
        user_info['statuses_count'] = info.get('statuses_count', 0)
        user_info['followers_count'] = info.get('followers_count', 0)
        user_info['follow_count'] = info.get('follow_count', 0)
        user_info['description'] = info.get('description', '')
        user_info['urank'] = info.get('urank', 0)
        user_info['mbrank'] = info.get('mbrank', 0)
        user_info['verified'] = info.get('verified', False)
        user_info['verified_type'] = info.get('verified_type', 0)
        user_info['verified_reason'] = info.get('verified_reason', '')

    return user_info


def write_file(source_file, target_file):
    with open(source_file) as file:

        result = json.load(file)
        key_list = []
        user_list = []
        for x in result:
            user = get_user_info(x['user_id'])
            user['text'] = x['text']
            user['reposts_count'] = x['reposts_count']
            user['comments_count'] = x['comments_count']
            user['attitudes_count'] = x['attitudes_count']
            print(user)
            user_list.append(user)
            time.sleep(random.randint(2, 5))

        for key in user_list[0].keys():
            key_list.append(key)

        with open(target_file, "w") as csvfile:
            writer = csv.writer(csvfile)

            # 先写入columns_name
            writer.writerow([title.get(key) for key in key_list])
            # 写入多行用writerows
            items = []
            for x in user_list:
                result_list = []
                for key in key_list:
                    result_list.append(x.get(key))

                items.append(result_list)
                writer.writerow(result_list)


if __name__ == '__main__':
    write_file('result_护发-0-100.json', 'hufa.csv')
