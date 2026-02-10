import re


def extract_json(text):
    match = re.search(r"<JSON>(.*?)</JSON>", text, re.S) or re.search(r"{(.*?)}", text, re.S)
    print("match", match)

    if not match:
        return None
    
    json_text = match.group(1)
    return json_text
