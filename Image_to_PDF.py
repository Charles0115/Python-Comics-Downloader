import os
import img2pdf
from PIL import Image
import shutil
import warnings

path = 'E:/comics/[TVKD]C94_Chinese_Doujinshi_Category_Full'
pdf_path = 'E:/comics/PDF2'
if not os.path.exists(pdf_path):
    os.mkdir(pdf_path)

warnings.filterwarnings('error')

for f in os.listdir(path):
    print("start " + f)

    image_path = os.path.join(path, f)
    os.chdir(image_path)

    specific_pdf_path = os.path.join(pdf_path, f + '.pdf')

    with open(specific_pdf_path, "wb") as fp:
        for i in os.listdir(os.getcwd()):
            if i.endswith(".png"):
                try:
                    img2pdf.convert(i)
                except Warning:
                    image = Image.open(i)
                    newImage = image.convert("RGB")
                    newImage.save(i)
                    image.close()

        try:
            fp.write(img2pdf.convert([i for i in os.listdir(os.getcwd()) if i.endswith(".png") or i.endswith(".jpg")]))
        except Warning:
            print(f + "has problem")
            fp.close()
            os.chdir(path)
        else:
            fp.close()
            os.chdir(path)
            shutil.rmtree(image_path)     # delete the folder and everything in it
            print(f + " done")



def remove_transparency(im, bg_colour=(255, 255, 255)):

    # Only process if image has transparency (http://stackoverflow.com/a/1963146)
    if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):

        # Need to convert to RGBA if LA format due to a bug in PIL (http://stackoverflow.com/a/1963146)
        alpha = im.convert('RGBA').split()[-1]

        # Create a new background image of our matt color.
        # Must be RGBA because paste requires both images have the same format
        # (http://stackoverflow.com/a/8720632  and  http://stackoverflow.com/a/9459208)
        bg = Image.new("RGBA", im.size, bg_colour + (255,))
        bg.paste(im, mask=alpha)
        return bg

    else:
        return im







# specific_pdf_path = os.path.join(pdf_path, '(C94) [Argyle◇check、わんとんランド組合 (こまめ丸)] とろ娘17 チノちゃんはじめました!3 (ご注文はうさぎですか ) [中国翻訳]' + '.pdf')
# with open(specific_pdf_path, 'wb') as fp:
#     fp.write(img2pdf.convert([i for i in os.listdir(os.getcwd()) if i.endswith(".png") or i.endswith(".jpg")]))
# fp.close()


# specific_pdf_path = os.path.join(pdf_path, '(C94) [50on! (愛上陸)] 催眠性指導 4 妊娠体験指導(試) [中国翻訳]' + '.pdf')
# with open(specific_pdf_path, "wb") as fp:
#     os.chdir(path)
#     try:
#         for i in os.listdir(os.getcwd()):
#             image = Image.open(i)
#             remove_transparency(image)
#         fp.write(img2pdf.convert([i for i in os.listdir(os.getcwd()) if i.endswith(".png") or i.endswith(".jpg")]))
#     except Exception as e:
#
#         print(e)
#         fp.close()
#         os.chdir(path)
#     else:
#         fp.close()
#         os.chdir(path)
#         # shutil.rmtree(image_path)     # delete the folder and everything in it
#         print(" done")



