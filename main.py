import telebot
import cv2
import os

from PIL import Image, ImageSequence
from JSON_Helper import output_to_file, output_to_json, join_outputs
from firstTask import first_task
from fourthTask import fourth_task
from thirdTask import third_task

bot = telebot.TeleBot('1839363129:AAFmC3V9gljO8VqcR5cbKFA8-fTCUE89TrM')


@bot.message_handler(content_types=['text', 'document'])
def get_text_messages(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'C:/Users/Student/Documents/Files/' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        pages = []
        if src.endswith('.tiff'):
            img = Image.open(src)
            for i, page in enumerate(ImageSequence.Iterator(img)):
                new_file_name = src[:-4] + '%' + str(i) + '.tif'
                page.save(new_file_name)
                pages.append(new_file_name)
        else:
            pages.append(src)
        bot.reply_to(message, "Подождите, наши специалисты обрабатывают ваш запрос...")
        outputs = []
        for i in range(len(pages)):
            img = cv2.imread(src)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            output = first_task(img)
            output = third_task(output, src)
            # if output.source.type == 'main':
            outputs.append(output)
        output = join_outputs(outputs)
        output_to_file(output_to_json(output), src)
        # if len(pages) == 1:
        fourth_task(src, outputs[0].text)
        path = src + ".json"
        doc = open(path, 'rb')
        bot.send_document(message.from_user.id, doc)
        for page in pages:
            os.remove(page)
        if os.path.exists(src):
            os.remove(src)
    except Exception as e:
        print(e)
        bot.reply_to(message, "Подождите, наши специалисты пока отдыхают...")


bot.polling(none_stop=True, interval=0)
