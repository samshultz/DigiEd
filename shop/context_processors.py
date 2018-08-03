def menu(request):
    menu = None
    if 'shop' in request.path.split("/"):
        menu = 'shop'
    else:
        menu = 'home'
    return {'menu': menu}
