import os
from datetime import date, timedelta, datetime
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.encoding import smart_str
from urllib3.exceptions import ConnectTimeoutError
from RSSI.rssi_utils.influx import hoster
from RSSI.rssi_utils.updater import get_sensor
from run.models import RssiDataMore, RssiDataLess
from RSSI.rssi_utils.dicts import return_dict, return_dict_erlang


def rssi_show_dicts(request):
    sensors = ['R407', 'RNGU', 'R401', 'R403', 'R301', 'R502', 'R508', 'R514', 'R403s1', 'R405', 'R415', 'R420']
    for sensor in sensors:
        try:
            lines, more = get_sensor(sensor)
            RssiDataLess.objects.create(host=sensor, data=lines)
            RssiDataMore.objects.create(host=sensor, data=more)
        except ConnectTimeoutError:
            print(f"Connection timeout for sensor {sensor}")
            messages.warning(request, f'Підключення до хосту {sensor} не вдалося')
            return redirect('homepage')

    messages.success(request, 'Дані було зібрано успішно!')
    return redirect('homepage')


def get_data_less(day, month):
    data = RssiDataLess.objects.filter(host='R401', time__day=day, time__month=month).last()
    data1 = RssiDataLess.objects.filter(host='R403', time__day=day, time__month=month).last()
    data2 = RssiDataLess.objects.filter(host='R407', time__day=day, time__month=month).last()
    data3 = RssiDataLess.objects.filter(host='R301', time__day=day, time__month=month).last()
    data4 = RssiDataLess.objects.filter(host='R405', time__day=day, time__month=month).last()
    data5 = RssiDataLess.objects.filter(host='R415', time__day=day, time__month=month).last()
    data6 = RssiDataLess.objects.filter(host='R420', time__day=day, time__month=month).last()
    data7 = RssiDataLess.objects.filter(host='R502', time__day=day, time__month=month).last()
    data8 = RssiDataLess.objects.filter(host='R508', time__day=day, time__month=month).last()
    data9 = RssiDataLess.objects.filter(host='R514', time__day=day, time__month=month).last()
    data10 = RssiDataLess.objects.filter(host='R403s1', time__day=day, time__month=month).last()
    data11 = RssiDataLess.objects.filter(host='RNGU', time__day=day, time__month=month).last()
    timedate = data11.time.strftime('%Y-%m-%d')
    return data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, timedate


def get_data_more(day, month):
    data = RssiDataMore.objects.filter(host='R401', time__day=day, time__month=month).last()
    data1 = RssiDataMore.objects.filter(host='R403', time__day=day, time__month=month).last()
    data2 = RssiDataMore.objects.filter(host='R407', time__day=day, time__month=month).last()
    data3 = RssiDataMore.objects.filter(host='R301', time__day=day, time__month=month).last()
    data4 = RssiDataMore.objects.filter(host='R405', time__day=day, time__month=month).last()
    data5 = RssiDataMore.objects.filter(host='R415', time__day=day, time__month=month).last()
    data6 = RssiDataMore.objects.filter(host='R420', time__day=day, time__month=month).last()
    data7 = RssiDataMore.objects.filter(host='R502', time__day=day, time__month=month).last()
    data8 = RssiDataMore.objects.filter(host='R508', time__day=day, time__month=month).last()
    data9 = RssiDataMore.objects.filter(host='R514', time__day=day, time__month=month).last()
    data10 = RssiDataMore.objects.filter(host='R403s1', time__day=day, time__month=month).last()
    data11 = RssiDataMore.objects.filter(host='RNGU', time__day=day, time__month=month).last()
    timedate = data11.time.strftime('%Y-%m-%d')
    return data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, timedate


def graph_less(request):
    datenow = date.today()
    day = datenow.day
    month = datenow.month
    if request.method == 'GET':
        date_string = request.GET.get('data-input')
        if date_string:
            day, month = date_string.split('-')[2], date_string.split('-')[1]
    try:
        data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, timedate = get_data_less(
            day, month)

        dicts = return_dict(data)
        dicts1 = return_dict(data1)
        dicts2 = return_dict(data2)
        dicts3 = return_dict(data3)
        dicts4 = return_dict(data4)
        dicts5 = return_dict(data5)
        dicts6 = return_dict(data6)
        dicts7 = return_dict(data7)
        dicts8 = return_dict(data8)
        dicts9 = return_dict(data9)
        dicts10 = return_dict(data10)
        dicts11 = return_dict(data11)
    except AttributeError:
        messages.warning(request, 'Дані відсутні за цей період')
        return redirect('less')
    context = {
        'datetime': timedate,
        'keys': dicts.keys(),
        'dicts': dicts.values(),
        'dicts1': dicts1.values(),
        'dicts2': dicts2.values(),
        'dicts3': dicts3.values(),
        'dicts4': dicts4.values(),
        'dicts5': dicts5.values(),
        'dicts6': dicts6.values(),
        'dicts7': dicts7.values(),
        'dicts8': dicts8.values(),
        'dicts9': dicts9.values(),
        'dicts10': dicts10.values(),
        'dicts11': dicts11.values(),
    }

    return render(request, 'page.html', context)


def graph_more(request):
    datenow = date.today()
    day = datenow.day
    month = datenow.month
    if request.method == 'GET':
        date_string = request.GET.get('data-input')
        if date_string:
            day, month = date_string.split('-')[2], date_string.split('-')[1]
    try:
        data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, timedate = get_data_more(
            day, month)

        dicts = return_dict(data)
        dicts1 = return_dict(data1)
        dicts2 = return_dict(data2)
        dicts3 = return_dict(data3)
        dicts4 = return_dict(data4)
        dicts5 = return_dict(data5)
        dicts6 = return_dict(data6)
        dicts7 = return_dict(data7)
        dicts8 = return_dict(data8)
        dicts9 = return_dict(data9)
        dicts10 = return_dict(data10)
        dicts11 = return_dict(data11)
    except AttributeError:
        messages.warning(request, 'Дані відсутні за цей період')
        return redirect('more')

    context = {
        'datetime': timedate,
        'keys': dicts.keys(),
        'dicts': dicts.values(),
        'dicts1': dicts1.values(),
        'dicts2': dicts2.values(),
        'dicts3': dicts3.values(),
        'dicts4': dicts4.values(),
        'dicts5': dicts5.values(),
        'dicts6': dicts6.values(),
        'dicts7': dicts7.values(),
        'dicts8': dicts8.values(),
        'dicts9': dicts9.values(),
        'dicts10': dicts10.values(),
        'dicts11': dicts11.values(),
    }

    return render(request, 'page.html', context)


def download_excel(request):
    port = request.POST.get('host')
    file_path = "data.xlsx"
    if os.path.exists(file_path):
        os.remove(file_path)
    try:
        hoster(port)
    except ConnectTimeoutError:
        messages.warning(request, f'З`єднання з {port} відсутнє')
        return redirect('homepage')
    with open(file_path, 'rb') as excel_file:
        response = HttpResponse(excel_file.read(),
                                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_path)
    return response


def chart_more(request):
    datenow = date.today()
    day = datenow.day
    month = datenow.month
    if request.method == 'GET':
        date_string = request.GET.get('data-input')
        if date_string:
            day, month = date_string.split('-')[2], date_string.split('-')[1]
    try:
        data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, timedate = get_data_more(
            day, month)

        dict = return_dict(data)
        dict1 = return_dict(data1)
        dict2 = return_dict(data2)
        dict3 = return_dict(data3)
        dict4 = return_dict(data4)
        dict5 = return_dict(data5)
        dict6 = return_dict(data6)
        dict7 = return_dict(data7)
        dict8 = return_dict(data8)
        dict9 = return_dict(data9)
        dict10 = return_dict(data10)
        dict11 = return_dict(data11)
    except AttributeError:
        messages.warning(request, 'Дані відсутні за цей період')
        return redirect('chart_more')

    context = {
        'datetime': timedate,
        'type': 'More',
        'keys': list(dict1.keys()),
        'values': list(dict.values()),
        'values1': list(dict1.values()),
        'values2': list(dict2.values()),
        'values3': list(dict3.values()),
        'values4': list(dict4.values()),
        'values5': list(dict5.values()),
        'values6': list(dict6.values()),
        'values7': list(dict7.values()),
        'values8': list(dict8.values()),
        'values9': list(dict9.values()),
        'values10': list(dict10.values()),
        'values11': list(dict11.values()),
    }

    return render(request, 'charts.html', context)


def chart_less(request):
    datenow = date.today()
    day = datenow.day
    month = datenow.month
    if request.method == 'GET':
        date_string = request.GET.get('data-input')
        if date_string:
            day, month = date_string.split('-')[2], date_string.split('-')[1]
    try:
        data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, timedate = get_data_less(
            day, month)

        dict = return_dict(data)
        dict1 = return_dict(data1)
        dict2 = return_dict(data2)
        dict3 = return_dict(data3)
        dict4 = return_dict(data4)
        dict5 = return_dict(data5)
        dict6 = return_dict(data6)
        dict7 = return_dict(data7)
        dict8 = return_dict(data8)
        dict9 = return_dict(data9)
        dict10 = return_dict(data10)
        dict11 = return_dict(data11)
    except AttributeError:
        messages.warning(request, 'Дані відсутні за цей період')
        return redirect('chart_less')

    context = {
        'datetime': timedate,
        'type': 'Less',
        'keys': list(dict1.keys()),
        'values': list(dict.values()),
        'values1': list(dict1.values()),
        'values2': list(dict2.values()),
        'values3': list(dict3.values()),
        'values4': list(dict4.values()),
        'values5': list(dict5.values()),
        'values6': list(dict6.values()),
        'values7': list(dict7.values()),
        'values8': list(dict8.values()),
        'values9': list(dict9.values()),
        'values10': list(dict10.values()),
        'values11': list(dict11.values()),
    }

    return render(request, 'charts.html', context)


def get_data_by_day_less(request):
    yesterday = date.today() - timedelta(days=1)
    data = RssiDataLess.objects.filter(host='R401', time__day=yesterday.day)
    return HttpResponse(data.last().data)


def homepage(request):
    return render(request, 'index.html')


def page_not_found(request, exception):
    return render(request, '404.html')


def server_error(request):
    return render(request, '500.html')


def table_erlang_more(request):
    datenow = date.today()
    day = datenow.day
    month = datenow.month
    if request.method == 'GET':
        date_string = request.GET.get('data-input')
        if date_string:
            day, month = date_string.split('-')[2], date_string.split('-')[1]
    try:
        data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, timedate = get_data_more(
            day, month)
        dicts = return_dict_erlang(data)
        dicts1 = return_dict_erlang(data1)
        dicts2 = return_dict_erlang(data2)
        dicts3 = return_dict_erlang(data3)
        dicts4 = return_dict_erlang(data4)
        dicts5 = return_dict_erlang(data5)
        dicts6 = return_dict_erlang(data6)
        dicts7 = return_dict_erlang(data7)
        dicts8 = return_dict_erlang(data8)
        dicts9 = return_dict_erlang(data9)
        dicts10 = return_dict_erlang(data10)
        dicts11 = return_dict_erlang(data11)
        print(dicts8)
    except AttributeError:
        messages.warning(request, 'Дані відсутні за цей період')
        return redirect('table_erlang_more')

    context = {
        'datetime': timedate,
        'keys': dicts.keys(),
        'dicts': dicts.values(),
        'dicts1': dicts1.values(),
        'dicts2': dicts2.values(),
        'dicts3': dicts3.values(),
        'dicts4': dicts4.values(),
        'dicts5': dicts5.values(),
        'dicts6': dicts6.values(),
        'dicts7': dicts7.values(),
        'dicts8': dicts8.values(),
        'dicts9': dicts9.values(),
        'dicts10': dicts10.values(),
        'dicts11': dicts11.values(),
    }

    return render(request, 'page.html', context)


def table_erlang_less(request):
    datenow = date.today()
    day = datenow.day
    month = datenow.month
    if request.method == 'GET':
        date_string = request.GET.get('data-input')
        if date_string:
            day, month = date_string.split('-')[2], date_string.split('-')[1]
    try:
        data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, timedate = get_data_less(
            day, month)
        dicts = return_dict_erlang(data)
        dicts1 = return_dict_erlang(data1)
        dicts2 = return_dict_erlang(data2)
        dicts3 = return_dict_erlang(data3)
        dicts4 = return_dict_erlang(data4)
        dicts5 = return_dict_erlang(data5)
        dicts6 = return_dict_erlang(data6)
        dicts7 = return_dict_erlang(data7)
        dicts8 = return_dict_erlang(data8)
        dicts9 = return_dict_erlang(data9)
        dicts10 = return_dict_erlang(data10)
        dicts11 = return_dict_erlang(data11)
    except AttributeError:
        messages.warning(request, 'Дані відсутні за цей період')
        return redirect('table_erlang_more')

    context = {
        'datetime': timedate,
        'keys': dicts.keys(),
        'dicts': dicts.values(),
        'dicts1': dicts1.values(),
        'dicts2': dicts2.values(),
        'dicts3': dicts3.values(),
        'dicts4': dicts4.values(),
        'dicts5': dicts5.values(),
        'dicts6': dicts6.values(),
        'dicts7': dicts7.values(),
        'dicts8': dicts8.values(),
        'dicts9': dicts9.values(),
        'dicts10': dicts10.values(),
        'dicts11': dicts11.values(),
    }

    return render(request, 'page.html', context)


def graph_log_more(request):
    datenow = date.today()
    day = datenow.day
    month = datenow.month
    if request.method == 'GET':
        date_string = request.GET.get('data-input')
        if date_string:
            day, month = date_string.split('-')[2], date_string.split('-')[1]
    try:
        data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, timedate = get_data_more(
            day, month)

        dict = return_dict_erlang(data)
        dict1 = return_dict_erlang(data1)
        dict2 = return_dict_erlang(data2)
        dict3 = return_dict_erlang(data3)
        dict4 = return_dict_erlang(data4)
        dict5 = return_dict_erlang(data5)
        dict6 = return_dict_erlang(data6)
        dict7 = return_dict_erlang(data7)
        dict8 = return_dict_erlang(data8)
        dict9 = return_dict_erlang(data9)
        dict10 = return_dict_erlang(data10)
        dict11 = return_dict_erlang(data11)
    except AttributeError:
        messages.warning(request, 'Дані відсутні за цей період')
        return redirect('chart_log_more')

    context = {
        'datetime': timedate,
        'type': 'More',
        'keys': list(dict1.keys()),
        'values': list(dict.values()),
        'values1': list(dict1.values()),
        'values2': list(dict2.values()),
        'values3': list(dict3.values()),
        'values4': list(dict4.values()),
        'values5': list(dict5.values()),
        'values6': list(dict6.values()),
        'values7': list(dict7.values()),
        'values8': list(dict8.values()),
        'values9': list(dict9.values()),
        'values10': list(dict10.values()),
        'values11': list(dict11.values()),
    }
    return render(request, 'charts.html', context)


def graph_log_less(request):
    datenow = date.today()
    day = datenow.day
    month = datenow.month
    if request.method == 'GET':
        date_string = request.GET.get('data-input')
        if date_string:
            day, month = date_string.split('-')[2], date_string.split('-')[1]
    try:
        data, data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, timedate = get_data_less(
            day, month)

        dict = return_dict_erlang(data)
        dict1 = return_dict_erlang(data1)
        dict2 = return_dict_erlang(data2)
        dict3 = return_dict_erlang(data3)
        dict4 = return_dict_erlang(data4)
        dict5 = return_dict_erlang(data5)
        dict6 = return_dict_erlang(data6)
        dict7 = return_dict_erlang(data7)
        dict8 = return_dict_erlang(data8)
        dict9 = return_dict_erlang(data9)
        dict10 = return_dict_erlang(data10)
        dict11 = return_dict_erlang(data11)
    except AttributeError:
        messages.warning(request, 'Дані відсутні за цей період')
        return redirect('chart_log_less')

    context = {
        'datetime': timedate,
        'type': 'More',
        'keys': list(dict1.keys()),
        'values': list(dict.values()),
        'values1': list(dict1.values()),
        'values2': list(dict2.values()),
        'values3': list(dict3.values()),
        'values4': list(dict4.values()),
        'values5': list(dict5.values()),
        'values6': list(dict6.values()),
        'values7': list(dict7.values()),
        'values8': list(dict8.values()),
        'values9': list(dict9.values()),
        'values10': list(dict10.values()),
        'values11': list(dict11.values()),
    }
    return render(request, 'charts.html', context)
