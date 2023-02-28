from views import Index, Items, Contacts, MeetUpItems, CreateCall, TypeMeetUpList, CreateType, CopyCall

routes = {
    '/': Index(),
    '/items/': Items(),
    '/contacts/': Contacts(),
    '/meetup/list/': MeetUpItems(),
    '/create-call/': CreateCall(),
    '/category/': TypeMeetUpList(),
    '/create-type/': CreateType(),
    '/copy-call/': CopyCall()
}
