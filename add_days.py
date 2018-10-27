import csv
from datetime import datetime, date, time

from menu import Items, db_session, Sweets

sweets_day = []
u = Items

with open('sweets-schedule.csv', 'r', encoding='ANSI') as f:
	fields = ['items_name','day_week']
	reader = csv.DictReader(f, fields, delimiter=';')
	for row in reader:
		sweety = u.query.filter(Items.items_name == row['items_name']).first()
		row['sweets_id'] = sweety.id
		print(sweety)
#		sweets_day.append(row)

#		print(row['day_week'])
#   	row['day_week'] = datetime.date.strptime(row['day_week'], '%A')
#   	row['day_week'] = datetime.datetime.weekday(row['day_week'], '%u')
#		row['published'] = datetime.datetime.strptime(row['published'],'%d.%m.%y %H:%M')
#	    weekday - день недели в виде числа, понедельник - 0, воскресенье - 6.
#		sweety = u.query.filters(Items.items_name == row['items_name']).first()
#		print(sweety)
'''
for sweety_data in sweets_day:
	sweety = Sweets(sweety_data['items_name'], sweety_data['day_week'], sweety_data['sweets_id'])
	db_session.add(sweety)
db_session.commit()


#print(sweets_day)

'''