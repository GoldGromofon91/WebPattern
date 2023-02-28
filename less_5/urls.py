from views import Index, Contacts, MeetUpItems, CreateCall, TypeMeetUpList, CreateType, CopyCall

routes = {
    '/': Index(),
    '/contacts/': Contacts(),
    '/meetup/list/': MeetUpItems(),
    '/create-call/': CreateCall(),
    '/category/': TypeMeetUpList(),
    '/create-type/': CreateType(),
    '/copy-call/': CopyCall()
}
