import datetime
import os
import time

from json_parser import *


class LightHouseAnalytics:

    REPORT_NAME_FORMAT = "URL_report_{}"
    REPORT_PATH = "C:\\PythonResults\\"     # change this path to your preference
    SAMPLE_URLS = [
        "https://importsem.com/use-python-to-automate-lighthouse-reports/",
        "https://github.com/oliseulean/Google-Lighthouse-Automation-Script/blob/main/lighthouse.py",
    ]
    PRESET = "desktop"

    def __init__(self):
        self._total_transfer_size = 0
        self._total_unused_css_size = 0
        self._total_unused_js_size = 0
        self._total_percentage_of_unused_css = 0
        self._total_percentage_of_unused_js = 0
        self._total_css_urls, self._total_js_urls, self._list_of_all_images = [], [], []

    @staticmethod
    def _get_date():
        return datetime.datetime.now().strftime("%m-%d-%y")

    def _check_report_folder(self):
        if not os.path.exists(self.REPORT_PATH):
            os.mkdir(self.REPORT_PATH)

    def start_web_analysis(self):
        self._check_report_folder()
        count = 0
        for url in self.SAMPLE_URLS:
            count += 1
            print('Starting web analysis for {0} ..'.format(url))
            os.popen(
                'lighthouse --quiet --chrome-flags="--headless" --disable-storage-reset="true" --preset=' +
                self.PRESET + ' --output=json --output-path=' + self.REPORT_PATH +
                self.REPORT_NAME_FORMAT.format(count) + '_' + self._get_date() + '.json ' + url)
            time.sleep(10)
            json_filename = os.path.join(self.REPORT_PATH, self.REPORT_NAME_FORMAT.format(count) + '_'
                                         + self._get_date() + '.json')
            time.sleep(10)

            with open(json_filename, encoding="utf-8") as json_data:
                json.load(json_data)
                print('Output saved successfully.')

    def collect_analysis_results(self):
        files = [f for f in os.listdir(self.REPORT_PATH)]
        for file in files:
            json_data = get_json_data(os.path.join(self.REPORT_PATH, file))
            self._total_transfer_size += get_total_transfer_size(json_data)
            css_value1, css_value2, css_value3 = get_unused_css_details(json_data)
            self._total_css_urls.append(css_value1)
            self._total_unused_css_size += css_value2
            self._total_percentage_of_unused_css += css_value3
            js_value1, js_value2, js_value3 = get_unused_js_details(json_data)
            self._total_js_urls.append(js_value1)
            self._total_unused_js_size += js_value2
            self._total_percentage_of_unused_js += js_value3
            self._list_of_all_images.append(get_images_details(json_data))

    def get_total_transfer_size(self):
        return self._total_transfer_size

    def get_total_css_urls(self):
        return self._total_css_urls

    def get_total_js_urls(self):
        return self._total_js_urls

    def get_total_unused_css_in_bytes(self):
        return self._total_unused_css_size

    def get_total_unused_js_in_bytes(self):
        return self._total_unused_js_size

    def get_total_percentage_of_unused_css(self):
        css_percentage = round(self._total_percentage_of_unused_css / len(self.SAMPLE_URLS), 2)
        return css_percentage

    def get_total_percentage_of_unused_js(self):
        js_percentage = round(self._total_percentage_of_unused_js / len(self.SAMPLE_URLS), 2)
        return js_percentage

    def get_list_of_images(self):
        return self._list_of_all_images


if __name__ == "__main__":
    web_analytics = LightHouseAnalytics()
    web_analytics.start_web_analysis()
    web_analytics.collect_analysis_results()
    print("Total transfer size in bytes: ", web_analytics.get_total_transfer_size())
    print("All concerned CSS urls: ", web_analytics.get_total_css_urls())
    print("All concerned JS urls: ", web_analytics.get_total_js_urls())
    print("Total unused CSS in bytes: ", web_analytics.get_total_unused_css_in_bytes())
    print("Total unused JS in bytes: ", web_analytics.get_total_unused_js_in_bytes())
    print("Average percentage of unused CSS: ", web_analytics.get_total_percentage_of_unused_css())
    print("Average percentage of unused JS: ", web_analytics.get_total_percentage_of_unused_js())
    print("List of all images: ", web_analytics.get_list_of_images())
