from Framework.jinja_templator import render_template
from settings.settings import Application, Logger, Debug
from settings.settings import Route
from settings.behav_pat import EmailNotifier, SmsNotifier, ListView, CreateView, BaseSerializer

site = Application()
logger = Logger(name='views')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()

routes = {
}


@Route(routes, '/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        logger.log(f'views.Index - start')
        return '200 OK', render_template('index.html',
                                         data={
                                             'server_time': request.get('SERVER_DATE_TIME', None),
                                             'moscow_time': request.get('CURRENT_DATE_TIME', None)
                                         })


@Route(routes, '/contacts/')
class Contacts:
    @Debug(name='Contacts')
    def __call__(self, request):
        logger.log(f'views.Call - start')
        return '200 OK', render_template('contact.html')


@Route(routes, '/meetup/list/')
class MeetUpItems:
    @Debug(name='MeetUpList')
    def __call__(self, request):
        logger.log(f'views.MeetUpItems - start')
        meetup = site.get_all_meet_up()

        if not meetup:
            return '200 OK', render_template('meetup_list.html', id=1, data={})

        last = meetup[-1]
        return '200 OK', render_template('meetup_list.html', id=last.id + 1,
                                         data={
                                             'meetup': meetup
                                         })


@Route(routes, '/category/')
class TypeMeetUpList:
    @Debug(name='TypeMeetUpList')
    def __call__(self, request):
        logger.log(f'views.TypeMeetUpList - start')
        if request.get('METHOD') == 'POST':
            data = request.get('POST_DATA')

            name = data['name']
            type_id = data.get('type_id')

            if type_id:
                type_meetup = site.find_type_meetup_by_id(int(type_id))

            new_type = site.create_type_meetup(name, type_m=type_meetup)

            site.type_meetup.append(new_type)

        return '200 OK', render_template('type_meetup_list.html',
                                         data={
                                             'types': site.type_meetup
                                         })


@Route(routes, '/create-call/')
class CreateCall:
    @Debug(name='New_call')
    def __call__(self, request):
        logger.log(f'views.CreateCall - start')
        if request.get('METHOD') == 'POST':
            request_data = request.get('POST_DATA')
            meetup = site.create_meetup(name=request_data['name'], type=request_data['call_type'])
            site.meetup.append(meetup)

        return '200 OK', render_template('new_call.html',
                                         data={
                                             'types': site.type_meetup,
                                             'meetups': site.meetup
                                         })


@Route(routes, '/create-type/')
class CreateType:
    @Debug(name='New_type')
    def __call__(self, request):
        logger.log(f'views.CreateType - start')
        if request.get('METHOD') == 'POST':
            logger.log(f'views.CreateType - start')
            request_data = request.get('POST_DATA')

            name = request_data['name']
            type_meetup = request_data['call_type']
            new_type = site.create_type_meetup(name, type_m=type_meetup)

            site.type_meetup.append(new_type)
            return '200 OK', render_template('type_meetup_list.html',
                                             data={
                                                 'types': site.type_meetup
                                             })
        else:
            return '200 OK', render_template('new_type.html')


@Route(routes, '/copy-call/')
class CopyCall:
    @Debug(name='Copy_call')
    def __call__(self, request):
        logger.log(f'views.CopyCall - start')
        data = request.get('POST_DATA')
        name = data['name']

        old_call = site.get_call(name)
        if old_call:
            new_name = f'copy_{name}'
            new_call = old_call.new_clone()
            new_call.name = new_name
            site.meetup.append(new_call)

        return '200 OK', render_template('meetup_list.html',
                                         data={
                                             'meetup': site.meetup
                                         })


@Route(routes=routes, url='/user-list/')
class UserListView(ListView):
    queryset = site.user
    template_name = 'user_list.html'


@Route(routes=routes, url='/create-user/')
class UserCreateView(CreateView):
    template_name = 'create_user.html'

    def create_obj(self, data: dict):
        print(data)
        new_user = site.create_user(type_in=data.get('user_type'),name=data.get('name'))
        site.user.append(new_user)
        print(site.user)