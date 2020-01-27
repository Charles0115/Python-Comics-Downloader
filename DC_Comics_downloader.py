import os
import requests
from lxml import etree

# from https://readcomicsonline.ru/

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

# General spider, change the name, number of chapters, and path.
base_url = 'https://readcomicsonline.ru/comic/darkseid-special-2017/{}'
url = 'https://readcomicsonline.ru/uploads/manga/darkseid-special-2017/chapters/{}/{}'


path = 'E:\DC Comics'
path = os.path.join(path, 'Darkseid Special')

if not os.path.exists(path):
    os.mkdir(path)

for chapter in range(1, 2):
    response = requests.get(base_url.format(str(chapter)), headers=HEADERS)
    text = response.text
    html = etree.HTML(text)
    pages = html.xpath("//select[@id='page-list']//option[last()]/text()")[0]
    image_style = html.xpath("//img[@class='img-responsive scan-page']/@src")[0].split('.')[-1]

    for image_index in range(1, int(pages)+1):
        if image_index < 10:
            true_url = url.format(str(chapter), '0' + str(image_index))
        else:
            true_url = url.format(str(chapter), str(image_index))

        true_url = true_url + '.' + image_style.strip()

        image_path = os.path.join(path, true_url.split('/')[-2] + '_' + true_url.split('/')[-1])

        r = requests.get(true_url)
        f = open(image_path, "wb")
        f.write(r.content)
        f.close()

    print('Chapter ' + str(chapter) + ' done')




# For DC Universe Rebirth ONLY. Change the chapter, path, and number of pages
# base_url = 'https://readcomicsonline.ru/comic/dc-comics-rebirth/{}'
# url = 'https://readcomicsonline.ru/uploads/manga/dc-comics-rebirth/chapters/{}/{}'
#
#
# path = 'E:\DC Comics\Rebirth'
# path = os.path.join(path, 'Cyborg')
#
# if not os.path.exists(path):
#     os.mkdir(path)
#
# chapter = 'cyborg-rebirth'
# response = requests.get(base_url.format(chapter), headers=HEADERS)
# text = response.text
# html = etree.HTML(text)
# image_style = html.xpath("//img[@class='img-responsive scan-page']/@src")[0].split('.')[-1]
#
# for image_index in range(1, 26):
#     if image_index < 10:
#         true_url = url.format(chapter, ('0' + str(image_index)))
#     else:
#         true_url = url.format(chapter, str(image_index))
#
#     true_url = true_url + '.' + image_style.strip()
#
#     image_path = os.path.join(path, true_url.split('/')[-1])
#
#     r = requests.get(true_url)
#     f = open(image_path, "wb")
#     f.write(r.content)
#     f.close()
#
# print(chapter + ' done')




# For Annual ONLY. Change the url, base_url, chapter, path, folder name and number of pages
# base_url = 'https://readcomicsonline.ru/comic/green-lanterns-2016/{}'
# url = ' https://readcomicsonline.ru/uploads/manga/green-lanterns-2016/chapters/{}/{}'
#
#
# path = 'E:\DC Comics\Rebirth\Green Lantern'
# path = os.path.join(path, 'Annual')
#
# if not os.path.exists(path):
#     os.mkdir(path)
#
# chapter = 'Annual-1'
# response = requests.get(base_url.format(chapter), headers=HEADERS)
# text = response.text
# html = etree.HTML(text)
# image_style = html.xpath("//img[@class='img-responsive scan-page']/@src")[0].split('.')[-1]
#
# for image_index in range(1, 44):
#     if image_index < 10:
#         true_url = url.format(chapter, ('0' + str(image_index)))
#     else:
#         true_url = url.format(chapter, str(image_index))
#
#     true_url = true_url + '.' + image_style.strip()
#
#     image_path = os.path.join(path, true_url.split('/')[-1])
#
#     r = requests.get(true_url)
#     f = open(image_path, "wb")
#     f.write(r.content)
#     f.close()
#
# print(chapter + ' done')