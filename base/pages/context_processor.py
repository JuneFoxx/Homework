

def header_data(request):
    menu_list = [
        {
            'name': "Главная",
            'base_url': 'pages:index',
            'parametr': ''
        },
        {
            'name': "О нас",
            'base_url': 'pages:about',
            'parametr': ''
        },
        {
            'name': "Галерея",
            'base_url': 'pages:gallery',
            'parametr': ''
        },
        {
            'name': "Контакты",
            'base_url': 'pages:contacts',
            'parametr': ''
        },
        
    ]
    
    return {'menu_list': menu_list}