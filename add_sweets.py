from menu import db_session, Sweets

sweet_item = [

	{
		'sweets_name': 'творожное_кольцо' , 
		'day_week': 'понедельник',
		'price': '15.30',
	},
	{
		'sweets_name': 'капкейк' , 
		'day_week': 'вторник',
		'price': '19.00',
	},
	{
		'sweets_name': 'трубочки' , 
		'day_week': 'среда',
		'price': '13.56',
	},
	{
		'sweets_name': 'брауни' , 
		'day_week': 'четверг',
		'price': '15.30',
	},
	{
		'sweets_name': 'капкейк' , 
		'day_week': 'пятница',
		'price': '32.15',
	},
	{
		'sweets_name': 'чизкейк' , 
		'day_week': 'суббота',
		'price': '34.12',
	},
	{
		'sweets_name': 'штрудель' , 
		'day_week': 'воскресенье',
		'price': '25.45',
	}
]


for a in sweet_item:
	sweet = Sweets(a['sweets_name'], a['day_week'], a['price'])
	db_session.add(sweet)


db_session.commit()

