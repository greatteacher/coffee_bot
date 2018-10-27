from menu import db_session, Items

ItemList = [

	{
		'items_name': 'творожное_кольцо' , 
		'desciption': 'кольцо с творогом',
		'price': '15.30',
	},
	{
		'items_name': 'капкейк' , 
		'desciption': 'кекс шоколадный',
		'price': '19.00',
	},
	{
		'items_name': 'трубочки' , 
		'desciption': 'вафельные трубочки с варенной сгущенкой',
		'price': '25.45',
	},
	{
		'items_name': 'брауни' , 
		'desciption': 'шоколадная сладость',
		'price': '15.30',
	},
	{
		'items_name': 'хот дог' , 
		'desciption': 'сосиска в булке',
		'price': '32.15',
	},
	{
		'items_name': 'чизкейк' , 
		'desciption': 'сырный тортик',
		'price': '34.12',
	},
	{
		'items_name': 'шарлотка' , 
		'desciption': 'пирог яблочный',
		'price': '25.45',
	}
]


for a in ItemList:
	item = Items(a['items_name'], a['desciption'], a['price'])
	db_session.add(item)


db_session.commit()

