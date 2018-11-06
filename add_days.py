import csv
import locale # для руских дней недели
from datetime import datetime, date, time

from menu import Items, db_session, Sweets
# locale.setlocale(locale.LC_ALL,'ru_RU') # сделать русские дни недели...
sweets_day = []
u = Items

with open('sweets-schedule2.csv', 'r', encoding='ANSI') as f:
	fields = ['items_name', 'day_id', 'day_week','day_week2']
	reader = csv.DictReader(f, fields, delimiter=';')
	for row in reader:
		sweety = u.query.filter(Items.items_name == row['items_name']).first()
		row['sweets_id'] = sweety.id
		sweets_day.append(row)
	# print(sweets_day)


for sweety_data in sweets_day:
	bakery = Sweets(sweety_data['items_name'], sweety_data['day_id'], sweety_data['day_week'],sweety_data['day_week2'], sweety_data['sweets_id'])
	db_session.add(bakery)
db_session.commit()







#print(sweets_day)
		# print('*********************')
		# print('+++++++++++++++++++++')
