from views import Index, Program, Contacts

routes = {
    '/': Index(),
    '/program/': Program(),
    '/contacts/': Contacts()
}