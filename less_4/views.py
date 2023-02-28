from Framework.jinja_templator import render_template
from settings.settings import Application, Logger

site = Application()
logger = Logger(name='views')


class Index:
    def __call__(self, request):
        logger.log(f'views.Index - start')
        return '200 OK', render_template('index.html',
                                         data={
                                             'server_time': request.get('SERVER_DATE_TIME', None),
                                             'moscow_time': request.get('CURRENT_DATE_TIME', None)
                                         })


class Items:
    def __call__(self, request):
        return '200 OK', render_template('items.html',
                                         data={'moscow_time': request.get('CURRENT_DATE_TIME', None)})


class Contacts:
    def __call__(self, request):
        logger.log(f'views.Call - start')
        return '200 OK', render_template('contact.html')


class MeetUpItems:
    def __call__(self, request):
        logger.log(f'views.MeetUpItems - start')
        meetup = site.get_all_meet_up()

        if not meetup:
            return '200 OK', render_template('meetup_list.html', data={}, id=1)

        last = meetup[-1]
        return '200 OK', render_template('meetup_list.html', data={'meetup': meetup}, id=last.id + 1)


class CreateCall:
    def __call__(self, request):
        logger.log(f'views.CreateCall - start')
        if request.get('METHOD') == 'POST':
            request_data = request.get('POST_DATA')
            meetup = site.create_meetup(name=request_data['name'], type=request_data['call_type'])
            site.meetup.append(meetup)

        return '200 OK', render_template('new_call.html', data={'types': site.type_meetup})


class CreateType:
    def __call__(self, request):
        logger.log(f'views.CreateType - start')
        if request.get('METHOD') == 'POST':
            logger.log(f'views.CreateType - start')
            request_data = request.get('POST_DATA')

            name = request_data['name']
            type_meetup = request_data['call_type']
            new_type = site.create_type_meetup(name, type_m=type_meetup)

            site.type_meetup.append(new_type)
            return '200 OK', render_template('type_meetup_list.html', data={'types': site.type_meetup})
        else:
            return '200 OK', render_template('new_type.html')


class TypeMeetUpList:
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

            return '200 OK', render_template('type_meetup_list.html', data={'types': site.type_meetup})
        else:
            types = site.type_meetup
            return '200 OK', render_template('type_meetup_list.html',
                                             data={'types': site.type_meetup})


class CopyCall:
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

        return '200 OK', render_template('meetup_list.html', data={'meetup': site.meetup})
