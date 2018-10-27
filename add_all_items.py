import csv
#from datetime import datetime, date, time
import datetime
from menu import Items, db_session
#from menu import Sweets

items_list = []
u = Items 

with open('items.csv', 'r', encoding='ANSI') as f:
	fields = ['items_name','price','description', 'appointment']
	reader = csv.DictReader(f, fields, delimiter=';')
	for row in reader:
		items_list.append(row)


for items_data in items_list:
	item = Items(items_data['items_name'],items_data['price'],items_data['description'], items_data['appointment'])
	db_session.add(item)

db_session.commit()
#print(items_list)