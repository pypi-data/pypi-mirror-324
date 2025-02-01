import pprint

def pprint_limited_dict(data, limit=10):
    trimmed_data = {}
    for key, value in data.items():
        if isinstance(value, (list, tuple, set)):  # 리스트, 튜플, 세트일 경우
            trimmed_data[key] = list(value)[:limit]  # 최대 10개까지만 출력
        else:
            trimmed_data[key] = value  # 다른 타입은 그대로 유지

    pprint.pprint(trimmed_data)