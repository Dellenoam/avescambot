import os

from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from ScamBotUpdate.models import Update

link = os.environ['link']
adm_key = os.environ['adm_key']
bot_key = os.environ['bot_key']


@csrf_exempt
def update(request):
    if request.method == 'POST':
        content = request.POST.dict()
        if content['key'] == adm_key:
            vcode = content['vcode']
            fname = content['fname'] + '.exe'
            flink = link + fname
            Update.objects.create(vcode=vcode, fname=fname, flink=flink)
            Update.objects.filter(id__lt=Update.objects.all().order_by('id').last().id).delete()
            return JsonResponse({'success': True, 'message': 'Данные были успешно загружены'})
        elif content['key'] == bot_key:
            update_base = Update.objects.all()
            flink = update_base[0].flink
            fname = update_base[0].fname
            vcode = update_base[0].vcode
            return JsonResponse({'success': True, 'message': 'Данные успешно получены',
                                 'flink': flink, 'fname': fname, 'vcode': vcode})
        else:
            return JsonResponse({'success': False,
                                 'message': 'Не удалось обработать запрос, проверьте правильность отправленных данных'})
    else:
        raise Http404()
