from datetime import datetime, date, time

from glob import glob
from menu import Sweets, Items

import re

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.ext import MessageHandler, CommandHandler, ConversationHandler, RegexHandler, Filters

coffee_main_menu_markup = ReplyKeyboardMarkup([['Menu_button'],
											  ['Special_offers'],
											  ['Checkout'],
											  ['Contact_info']])

bakery_main_menu_markup = ReplyKeyboardMarkup([['Добавить в корзину'],
												['Вчера','Послезавтра'],
												['Завтра','Через 3 дня'],
												['Назад']])


from settings import ADMIN_ID, ADMIN_EMAIL
from settings import weekday, dtoday, yestd, daltaday, yesterday, tomorrow, day_after_tmr, in_three
from utils import send_mail

for sweet in Sweets.query.filter(Sweets.day_week==weekday).all():
	bakery = sweet.items_name
amount = 0

def Send_todays_menu(bot, update, user_data):
	update.message.reply_text('Today is ' + bakery + '! Вы можете Добавить в корзину или посмотреть на будущее, или что уже упустили',
							  reply_markup = bakery_main_menu_markup )
	return 'sweet_of_day_state'    

def Send_tomorrows_menu(bot, update, user_data):
	update.message.reply_text('Tomorrow will be  ' + tomorrow )
	return 'sweet_of_day_state'    
def Send_day_after_tomorrow_menu(bot, update, user_data):
	update.message.reply_text('Day after tomorrow will be  ' + day_after_tmr )
	return 'sweet_of_day_state' 
def Send_in_three_menu(bot, update, user_data):
	update.message.reply_text('in three days will be  ' + in_three )
	return 'sweet_of_day_state' 
def Send_yesterdays_menu(bot, update, user_data):
	update.message.reply_text('yesterday was  ' + yesterday )
	return 'sweet_of_day_state' 


def coffee_main_menu_handler(bot, update, user_data):
	update.message.reply_text(
		'Добро пожаловать в Звездный доллар кафе\n'+
		'жмите соотвествующую кнопку:',
		reply_markup=coffee_main_menu_markup)
	user_id =  update.message.from_user['id']
	user_data[user_id] = {'id':user_id}
	if 'cart' not in user_data[user_id].keys() :
		user_data[user_id]['cart']=[]
	return 'cafe_main_menu_state'  #(Menu_button)$','^(Special_offers)$'


def menu_button_handler(bot, update, user_data):
	update.message.reply_text('Выберите категорию или вернитесь назад:',
							  reply_markup=ReplyKeyboardMarkup([['Кофеёк'],
																['Плюшки'],
																['Прочее'],
																['Назад']]))
	user_data['coffee'] = {}  # строчка создает пустой словарь для кофе 
	user_data['coffee']['menu_page'] = 0 #  обнуляет страницу в меню с пиццей 
	return 'cafe_menu_state'   # клава    [Кофеёк] [напитка]


def print_coffee_menu(bot, update, user_data): # ф-ия выбирает номер пиццы
	coffee_photos = glob('images/coffee/coffee*.jp*g')
	dct = {}
	for i in coffee_photos:
		k = re.search(r'coffee(\d+)\.j', i)
		dct[k.group(1)] = i
	optional_buttons =[['Checkout', 'Назад']]

	markup = [[str(i + 1)] for i in range(0,4)] + optional_buttons
	for i in range(0,4):      
		with open(dct[str(i)], 'rb') as f:
			bot.send_photo(chat_id=update.message.chat.id, photo=f)
	update.message.reply_text('Выберите Кофеёк:', reply_markup=ReplyKeyboardMarkup(markup, resize_keyboard=True)) 



def coffee_category_handler(bot, update, user_data):
	print_coffee_menu(bot, update, user_data)
	return 'coffee_choise_state'  # показывает клаву ^\d+$',  '^Пред\.|След\.|Назад$' переделалла на кнопку Checkout


def add_coffee_to_cart_handler(bot, update, user_data):
	coffee_index = update.message.text
	user_data[update.message.from_user['id']]['cart'].append(coffee_index)
	update.message.reply_text(f'Кофеёк №{coffee_index} добавлен в корзину')


def checkout_handler(bot, update, user_data):
	user_id =  update.message.from_user['id']
	cart = user_data[user_id]['cart']
	if not len(cart):
		update.message.reply_text('Ваша корзина пуста', reply_markup=ReplyKeyboardMarkup([['Назад']]))
	else:
		for i in sorted(set(cart)):
			update.message.reply_text(f'{i}x{cart.count(i)}, Цена: tbd\n')
		update.message.reply_text( f'{amount}х {bakery}\n Для изменения заказа, нажмите соотвествующую кнопку', 
			reply_markup = ReplyKeyboardMarkup([['Изменить заказ'],['Назад'],['Сделать заказ']]))
	return 'cafe_checkout_state'


def change_cart_handler(bot, update, user_data):
	user_id =  update.message.from_user['id']
	cart = user_data[user_id]['cart']
	markup = [[f'{i}x{cart.count(i)} -1'] for i in sorted(set(cart))]
	markup.extend([['Назад']])
	update.message.reply_text('Для уменьшения колличества позиций на 1\n'+
		'нажмите соотвествующую кнопку',
		reply_markup = ReplyKeyboardMarkup(markup, resize_keyboard=True))
	return 'removeing_from_cart_state'


def remove_from_cart_handler(bot, update, user_data):
	item = re.search(r'(\w+)x\w\s*-1', update.message.text).group(1)
	user_id = update.message.from_user['id']
	cart = user_data[user_id]['cart']
	cart.remove(item)
	return change_cart_handler(bot, update, user_data)


def order_coffee_handler(bot, update, user_data):
	user_id =  update.message.from_user['id']
	cart = user_data[user_id]['cart']
	update.message.reply_text(f'У вас в корзине {amount}х {bakery} ',
		reply_markup = ReplyKeyboardMarkup([['Назад'],['Отправить заказ']]))
	for i in sorted(set(cart)):
		update.message.reply_text(f'{i}x{cart.count(i)}, Цена: tbd\n')
	return 'cafe_make_order_state'


def send_order_handler(bot, update, user_data):
	user_id =  update.message.from_user['id']
	msg = f'Пользователь {user_id} сделал заказ:\n'+f'{user_data[user_id]["cart"]}'
	bot.send_message(ADMIN_ID, msg)
	send_mail(msg, ADMIN_EMAIL)
	update.message.reply_text('Спасибо за заказ, вам позвонит оператор')
	return coffee_main_menu_handler(bot, update, user_data)



def sweets_category_handler(bot, update, user_data):
	Cupcake_list = glob('images/coffee/sweet_c*.jp*g')
	Cupcake_pic = choice(Cupcake_list)
	bot.send_photo(chat_id=update.message.chat.id, photo=open(Cupcake_pic, 'rb'))
	update.message.reply_text( 'Сегодня у нас из вкусняшек, chocolate cupcake from Marisha')
	return 'end'



def send_HotDog_description(bot, update, user_data):
	Kor_list = glob('coffee/sweet_hot*.jp*g')
	Kor_pic = choice(Kor_list)
	bot.send_photo(chat_id=update.message.chat.id, photo=open(Kor_pic, 'rb'))
	update.message.reply_text('сосиска в булке c горчичкой и томатным соусом',
		reply_markup=sweets_main_menu)
	return 'end'


def send_Browny_description(bot, update, user_data):
	Brown_list = glob('coffee/sweet_b*.jp*g')
	Brown_pic = choice(Brown_list)
	bot.send_photo(chat_id=update.message.chat.id, photo=open(Brown_pic, 'rb'))
	update.message.reply_text('bakery with lots of chocolate',
		reply_markup=sweets_main_menu)
	return 'end'


def send_Kozinka_description(bot, update, user_data):
	Kor_list = glob('coffee/sweet_k*.jp*g')
	Kor_pic = choice(Kor_list)
	bot.send_photo(chat_id=update.message.chat.id, photo=open(Kor_pic, 'rb'))
	update.message.reply_text('песочная корзинка с белковым кремом', 
		reply_markup=sweets_main_menu)
	return 'end'


def send_Sharlotka_description(bot, update, user_data):
	Kor_list = glob('coffee/sweet_sh*.jp*g')
	Kor_pic = choice(Kor_list)
	bot.send_photo(chat_id=update.message.chat.id, photo=open(Kor_pic, 'rb'))
	update.message.reply_text('sponge with apples inside and cinnamon on the top', 
		reply_markup=sweets_main_menu)
	return 'end'



def send_Cupcacke_description(bot, update, user_data):
	Kor_list = glob('coffee/sweet_c*.jp*g')
	Kor_pic = choice(Kor_list)
	bot.send_photo(chat_id=update.message.chat.id, photo=open(Kor_pic, 'rb'))
	update.message.reply_text( 'chocolate cupcake from Marisha', 
		reply_markup=sweets_main_menu)
	return 'end'


def send_Americano_description(bot, update, user_data):
	Dan_list = glob('coffee/coffee1*.jp*g')
	Dan_pic = choice(Dan_list)
	bot.send_photo(chat_id=update.message.chat.id, photo=open(Dan_pic, 'rb'))
	update.message.reply_text( 'just black coffee',
		reply_markup = coffee_main_menu)
	return 'end'


def send_Capuccino_description(bot, update, user_data):
	Dan_list = glob('coffee/coffee2*.jp*g')
	Dan_pic = choice(Dan_list)
	bot.send_photo(chat_id=update.message.chat.id, photo=open(Dan_pic, 'rb'))
	update.message.reply_text( 'coffee with milk',
		reply_markup = coffee_main_menu)
	return 'end'


def send_Latte_description(bot, update, user_data):
	Lat_list = glob('coffee/coffee3*.jp*g')
	Lat_pic = choice(Lat_list)
	bot.send_photo(chat_id=update.message.chat.id, photo=open(Lat_pic, 'rb'))
	update.message.reply_text( 'coffee rich of milk, more than in Capuccino',
		reply_markup = coffee_main_menu)
	return 'end'


def send_Glase_description(bot, update, user_data):
	Glase_list = glob('coffee/coffee4*.jp*g')
	Glase_pic = choice(Glase_list)
	bot.send_photo(chat_id=update.message.chat.id, photo=open(Glase_pic, 'rb'))
	update.message.reply_text( 'coffee with spoon of ice-cream',
		reply_markup = coffee_main_menu)
	return 'end'


def contact_info_handler(bot, update, user_data):
	update.message.reply_text('This is contact info button')
	return 'end'


def drinks_category_handler(bot, update, user_data):
	update.message.reply_text('Здесь будет выбор напитков')
	return 'end'


def other_category_handler(bot, update, user_data):
	update.message.reply_text('Здесь будет прочее')
	return 'end'


def back_cafe_menu(bot, update, user_data):
	update.message.reply_text(
		'Для просмотра меню, акций,\nкорзины или контактной\n'+
		'информации\nнажмите соотвествующую кнопку:',
		reply_markup=coffee_main_menu_markup)
	print(user_data[update.message.from_user['id']]) # печатает в командной строке кто и что заказал.
	return 'cafe_main_menu_state'  #(Menu_button)$','^(Special_offers)$' корзина контактная инфа

def add_backery_to_cart_handler(bot, update, user_data):
	global amount
	amount+=1
	update.message.reply_text(f' добавлено!  в корзине {amount}х {bakery}')
	return 'sweet_of_day_state' 
	# coffee_index = update.message.text
	# user_data[update.message.from_user['id']]['cart'].append(coffee_index)
	# update.message.reply_text(f'Кофеёк №{coffee_index} добавлен в корзину')