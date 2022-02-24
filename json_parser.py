import json


def get_json_data(file):
    json_file = open(file, encoding='utf-8')
    json_data = json.load(json_file)
    return json_data


def get_unused_js_details(json_data):
    unused_js_items = json_data['audits']['unused-javascript']['details']['items']
    js_urls = list()
    js_wasted_bytes, js_wasted_percentage = 0, 0
    for item in unused_js_items:
        js_urls.append(item['url'])
        js_wasted_bytes += item['wastedBytes']
        js_wasted_percentage += item['wastedPercent']
    return js_urls, js_wasted_bytes, js_wasted_percentage / len(unused_js_items)


def get_unused_css_details(json_data):
    unused_css_items = json_data['audits']['unused-css-rules']['details']['items']
    css_urls = list()
    css_wasted_bytes, css_wasted_percentage = 0, 0
    for item in unused_css_items:
        css_urls.append(item['url'])
        css_wasted_bytes += item['wastedBytes']
        css_wasted_percentage += item['wastedPercent']
    return css_urls, css_wasted_bytes, css_wasted_percentage / len(unused_css_items)


def get_network_requests_details(json_data):
    network_reqs_items = json_data['audits']['network-requests']['details']['items']
    return network_reqs_items


def get_total_transfer_size(json_data):
    network_reqs_items = get_network_requests_details(json_data)
    total_transfer_size = 0
    for item in network_reqs_items:
        total_transfer_size += item['transferSize']

    return total_transfer_size


def get_images_details(json_data):
    network_reqs_items = get_network_requests_details(json_data)
    image_details = list()
    for item in network_reqs_items:
        if item['resourceType'] == "Image":
            image_dict = {
                'url': item['url'],
                'mimeType': item['mimeType'],
                'transferSize': item['transferSize'],
                'resourceSize': item['resourceSize']
            }
            image_details.append(image_dict)

    return image_details


def get_seo_score(json_data):
    seo = json_data["categories"]["seo"]["score"] * 100
    return seo


def get_accessibility_score(json_data):
    accessibility = json_data["categories"]["accessibility"]["score"] * 100
    return accessibility


def get_performance_score(json_data):
    performance = json_data["categories"]["performance"]["score"] * 100
    return performance


def get_best_practices_score(json_data):
    best_practices = json_data["categories"]["best-practices"]["score"] * 100
    return best_practices


# if __name__ == "__main__":
#     file = "lighthouse_output.json"
#     data = get_json_data(file)
#     print(get_best_practices_score(data))
