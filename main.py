# import cv2
# from JSON_Helper import output_to_file, output_to_json
# from firstTask import first_task
#
# img = cv2.imread('aah97e00-page02_1.tif')
# # img = cv2.imread('11963218_doc1.jpg')
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# output = first_task(img)
# output_to_file(output_to_json(output))
import telebot
import cv2
import os
from JSON_Helper import output_to_file, output_to_json
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

        bot.reply_to(message, "Подождите, наши специалисты обрабатывают ваш запрос...")
        img = cv2.imread(src)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        output = first_task(img)
        output = third_task(output, src)
        output_to_file(output_to_json(output), src)
        fourth_task(src, output.text)
        path = src + ".json"
        doc = open(path, 'rb')
        bot.send_document(message.from_user.id, doc)
        os.remove(src)
    except FileNotFoundError:
        pass
        # bot.reply_to(message, str(e))


bot.polling(none_stop=True, interval=0)
