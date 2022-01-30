from views import Index, Items, Contacts

routes = {
    '/': Index(),
    '/items/': Items(),
    '/contacts/': Contacts()
}