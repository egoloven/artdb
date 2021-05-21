from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .models import Sex, Type, Artist, PeriodsAndMovements, Artwork
from django.db import models
import datetime

ERROR_JSON = {
    'sex_max_length': '{\"success\": 0, \"error\": \"Sex name max lenght = 20.\"}',
    'sex_already_exists': '{\"success\": 0, \"error\": \"This sex is already exists.\"}',
    'no_error': '{\"success\": 1, \"error\": null}',
    'not_enough_data': '{\"success\": 0, \"error\": \"Not enough data.\"}',
    'delete_id': '{\"success\": 0, \"error\": \"This id is already deleted or doesn`t exist.\"}',
    'type_max_length': '{\"success\": 0, \"error\": \"Type name max lenght = 20.\"}',
    'type_desc_max_length': '{\"success\": 0, \"error\": \"Type description max lenght = 50.\"}',
    'type_already_exists': '{\"success\": 0, \"error\": \"This type is already exists.\"}',
    'artist_birth_date': '{\"success\": 0, \"error\": \"This is the incorrect birth date string format. It should be YYYY-MM-DD.\"}',
    'artist_death_date': '{\"success\": 0, \"error\": \"This is the incorrect death date string format. It should be YYYY-MM-DD.\"}',
    'artist_max_length': '{\"success\": 0, \"error\": \"Artist full name max lenght = 40.\"}',
    'artist_sex_id': '{\"success\": 0, \"error\": \"There is no such sex try other sex id.\"}',
    'artist_no_sex_id': '{\"success\": 0, \"error\": \"No sex id provided.\"}',
    'pm_max_length': '{\"success\": 0, \"error\": \"Period or movement name max lenght = 20.\"}',
    'pm_start_date': '{\"success\": 0, \"error\": \"This is the incorrect start date string format. It should be YYYY-MM-DD.\"}',
    'pm_end_date': '{\"success\": 0, \"error\": \"This is the incorrect end date string format. It should be YYYY-MM-DD.\"}',
    'pm_description': '{\"success\": 0, \"error\": \"Period or movement description max lenght = 50.\"}',
    'pm_already_exists': '{\"success\": 0, \"error\": \"This period or movement is already exists.\"}',
}

def index(request):
    return render(request, 'main/index.html')

def sex(request):
    if request.method == 'GET':
        return sex_get(request)
    if request.method == 'POST':
        return sex_post(request)
    if request.method == 'PUT':
        return sex_put(request)
    if request.method == 'DELETE':
        return sex_delete(request)
    return render(request, 'main/index.html')

def sex_get(request):
    if request.GET:
        id = request.GET['id']
        sex = Sex.objects.filter(id=id)
        json_sex = serializers.serialize('json', sex)
        return HttpResponse(json_sex, content_type='text/json-comment-filtered')

    sex_list = Sex.objects.all()
    json_sex_list = serializers.serialize('json', sex_list)
    return HttpResponse(json_sex_list, content_type='text/json-comment-filtered')

def sex_post(request):
    name = request.GET['name']
    if len(name) > 20:
        return HttpResponse(ERROR_JSON['sex_max_length'], content_type='text/json-comment-filtered')

    if Sex.objects.filter(name=name):
        return HttpResponse(ERROR_JSON['sex_already_exists'], content_type='text/json-comment-filtered')

    new_sex = Sex(name=name)
    new_sex.save()
    return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')

def sex_put(request):
    if 'id' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    if 'name'not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    id = request.GET['id']
    name = request.GET['name']
    if len(name) > 20:
        return HttpResponse(ERROR_JSON['sex_max_length'], content_type='text/json-comment-filtered')

    this_sex = Sex.objects.filter(name=name)
    if this_sex:
        if int(id) != this_sex[0].id:
            return HttpResponse(ERROR_JSON['sex_already_exists'], content_type='text/json-comment-filtered')

    new_sex = Sex(id=id, name=name)
    new_sex.save()
    return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')

def sex_delete(request):
    if 'id' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    id = request.GET['id']
    delete_sex = Sex.objects.filter(id=id)
    if delete_sex:
        delete_sex.delete()
        return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')
    return HttpResponse(ERROR_JSON['delete_id'], content_type='text/json-comment-filtered')

def type(request):
    if request.method == 'GET':
        return type_get(request)
    if request.method == 'POST':
        return type_post(request)
    if request.method == 'PUT':
        return type_put(request)
    if request.method == 'DELETE':
        return type_delete(request)
    return render(request, 'main/index.html')

def type_get(request):
    if request.GET:
        id = request.GET['id']
        type = Type.objects.filter(id=id)
        json_type = serializers.serialize('json', type)
        return HttpResponse(json_type, content_type='text/json-comment-filtered')

    type_list = Type.objects.all()
    json_type_list = serializers.serialize('json', type_list)
    return HttpResponse(json_type_list, content_type='text/json-comment-filtered')

def type_post(request):
    if 'name' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    name = request.GET['name']

    if len(name) > 20:
        return HttpResponse(ERROR_JSON['type_max_length'], content_type='text/json-comment-filtered')

    if Type.objects.filter(name=name):
        return HttpResponse(ERROR_JSON['type_already_exists'], content_type='text/json-comment-filtered')

    if 'description' in request.GET.keys():
        description = request.GET['description']
        if len(description) > 50:
            return HttpResponse(ERROR_JSON['type_desc_max_length'], content_type='text/json-comment-filtered')
        new_type = Type(name=name, description=description)
        new_type.save()
        return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')

    new_type = Type(name=name, description=None)
    new_type.save()
    return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')

def type_put(request):
    if 'id' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    if 'name'not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    id = request.GET['id']
    name = request.GET['name']
    if len(name) > 20:
        return HttpResponse(ERROR_JSON['type_max_length'], content_type='text/json-comment-filtered')

    this_type = Type.objects.filter(name=name)
    if this_type:
        if int(id) != this_type[0].id:
            return HttpResponse(ERROR_JSON['type_already_exists'], content_type='text/json-comment-filtered')

    if 'description' in request.GET.keys():
        description = request.GET['description']
        if len(description) > 50:
            return HttpResponse(ERROR_JSON['type_desc_max_length'], content_type='text/json-comment-filtered')
        new_type = Type(id=id, name=name, description=description)
        new_type.save()
        return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')

    new_type = Type(id=id, name=name)
    new_type.save()
    return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')

def type_delete(request):
    if 'id' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    id = request.GET['id']
    delete_type = Type.objects.filter(id=id)
    if delete_type:
        delete_type.delete()
        return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')
    return HttpResponse(ERROR_JSON['delete_id'], content_type='text/json-comment-filtered')

def artist(request):
    if request.method == 'GET':
        return artist_get(request)
    if request.method == 'POST':
        return artist_post(request)
    if request.method == 'PUT':
        return artist_put(request)
    if request.method == 'DELETE':
        return artist_delete(request)
    return render(request, 'main/index.html')

def artist_get(request):
    if request.GET:
        id = request.GET['id']
        artist = Artist.objects.filter(id=id)
        json_artist = serializers.serialize('json', artist)
        return HttpResponse(json_artist, content_type='text/json-comment-filtered')

    artist_list = Artist.objects.all()
    json_artist_list = serializers.serialize('json', artist_list)
    return HttpResponse(json_artist_list, content_type='text/json-comment-filtered')

def artist_post(request):
    format = "%Y-%m-%d"

    full_name = None
    birth_date = None
    death_date = None
    sex_id = None

    if 'full_name' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    full_name = request.GET['full_name']

    if len(full_name) > 40:
        return HttpResponse(ERROR_JSON['artist_max_length'], content_type='text/json-comment-filtered')

    if 'birth_date' in request.GET.keys():
        birth_date = request.GET['birth_date']

        try:
            datetime.datetime.strptime(birth_date, format)

        except ValueError:
            return HttpResponse(ERROR_JSON['artist_birth_date'], content_type='text/json-comment-filtered')

    if 'death_date' in request.GET.keys():
        death_date = request.GET['death_date']

        try:
            datetime.datetime.strptime(death_date, format)

        except ValueError:
            return HttpResponse(ERROR_JSON['artist_death_date'], content_type='text/json-comment-filtered')

    if 'sex_id' in request.GET.keys():
        sex_id = request.GET['sex_id']

        if not Sex.objects.filter(id=sex_id):
            return HttpResponse(ERROR_JSON['artist_sex_id'], content_type='text/json-comment-filtered')
    else:
        return HttpResponse(ERROR_JSON['artist_no_sex_id'], content_type='text/json-comment-filtered')

    new_artist = Artist(full_name=full_name, birth_date=birth_date, death_date=death_date, sex_id=sex_id)
    new_artist.save()
    return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')

def artist_put(request):
    format = "%Y-%m-%d"

    full_name = None
    birth_date = None
    death_date = None
    sex_id = None
    id = None

    if 'id' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    id = request.GET['id']

    if 'full_name' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    full_name = request.GET['full_name']

    if len(full_name) > 40:
        return HttpResponse(ERROR_JSON['artist_max_length'], content_type='text/json-comment-filtered')

    if 'birth_date' in request.GET.keys():
        birth_date = request.GET['birth_date']

        try:
            datetime.datetime.strptime(birth_date, format)

        except ValueError:
            return HttpResponse(ERROR_JSON['artist_birth_date'], content_type='text/json-comment-filtered')

    if 'death_date' in request.GET.keys():
        death_date = request.GET['death_date']

        try:
            datetime.datetime.strptime(death_date, format)

        except ValueError:
            return HttpResponse(ERROR_JSON['artist_death_date'], content_type='text/json-comment-filtered')

    if 'sex_id' in request.GET.keys():
        sex_id = request.GET['sex_id']

        if not Sex.objects.filter(id=sex_id):
            return HttpResponse(ERROR_JSON['artist_sex_id'], content_type='text/json-comment-filtered')
    else:
        return HttpResponse(ERROR_JSON['artist_no_sex_id'], content_type='text/json-comment-filtered')

    new_artist = Artist(id=id, full_name=full_name, birth_date=birth_date, death_date=death_date, sex_id=sex_id)
    new_artist.save()
    return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')

def artist_delete(request):
    if 'id' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    id = request.GET['id']
    delete_artist = Artist.objects.filter(id=id)
    if delete_artist:
        delete_artist.delete()
        return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')
    return HttpResponse(ERROR_JSON['delete_id'], content_type='text/json-comment-filtered')

def pm(request):
    if request.method == 'GET':
        return pm_get(request)
    if request.method == 'POST':
        return pm_post(request)
    if request.method == 'PUT':
        return pm_put(request)
    if request.method == 'DELETE':
        return pm_delete(request)
    return render(request, 'main/index.html')

def pm_get(request):
    if request.GET:
        id = request.GET['id']
        pm = PeriodsAndMovements.objects.filter(id=id)
        json_pm = serializers.serialize('json', pm)
        return HttpResponse(json_pm, content_type='text/json-comment-filtered')

    pm_list = PeriodsAndMovements.objects.all()
    json_pm_list = serializers.serialize('json', pm_list)
    return HttpResponse(json_pm_list, content_type='text/json-comment-filtered')

def pm_post(request):
    format = "%Y-%m-%d"

    name = None
    start = None
    end = None
    description = None

    if 'name' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    name = request.GET['name']

    if len(name) > 20:
        return HttpResponse(ERROR_JSON['pm_max_length'], content_type='text/json-comment-filtered')

    if 'start' in request.GET.keys():
        start = request.GET['start']

        try:
            datetime.datetime.strptime(start, format)

        except ValueError:
            return HttpResponse(ERROR_JSON['pm_start_date'], content_type='text/json-comment-filtered')

    if 'end' in request.GET.keys():
        end = request.GET['end']

        try:
            datetime.datetime.strptime(end, format)

        except ValueError:
            return HttpResponse(ERROR_JSON['pm_end_date'], content_type='text/json-comment-filtered')

    if 'description' in request.GET.keys():
        description = request.GET['description']

        if len(description) > 50:
            return HttpResponse(ERROR_JSON['pm_description'], content_type='text/json-comment-filtered')

    if PeriodsAndMovements.objects.filter(name=name):
        return HttpResponse(ERROR_JSON['pm_already_exists'], content_type='text/json-comment-filtered')

    new_pm = PeriodsAndMovements(name=name, start=start, end=end, description=description)
    new_pm.save()
    return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')

def pm_put(request):
    format = "%Y-%m-%d"

    name = None
    start = None
    end = None
    description = None
    id = None

    if 'id' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    id = request.GET['id']

    if 'name' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    name = request.GET['name']

    if len(name) > 20:
        return HttpResponse(ERROR_JSON['pm_max_length'], content_type='text/json-comment-filtered')

    if 'start' in request.GET.keys():
        start = request.GET['start']

        try:
            datetime.datetime.strptime(start, format)

        except ValueError:
            return HttpResponse(ERROR_JSON['pm_start_date'], content_type='text/json-comment-filtered')

    if 'end' in request.GET.keys():
        end = request.GET['end']

        try:
            datetime.datetime.strptime(end, format)

        except ValueError:
            return HttpResponse(ERROR_JSON['pm_end_date'], content_type='text/json-comment-filtered')

    if 'description' in request.GET.keys():
        description = request.GET['description']

        if len(description) > 50:
            return HttpResponse(ERROR_JSON['pm_description'], content_type='text/json-comment-filtered')

    this_pm = PeriodsAndMovements.objects.filter(name=name)
    if this_pm:
        if int(id) != this_pm[0].id:
            return HttpResponse(ERROR_JSON['pm_already_exists'], content_type='text/json-comment-filtered')

    new_pm = PeriodsAndMovements(id=id, name=name, start=start, end=end, description=description)
    new_pm.save()
    return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')

def pm_delete(request):
    if 'id' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    id = request.GET['id']
    delete_artist = PeriodsAndMovements.objects.filter(id=id)
    if delete_artist:
        delete_artist.delete()
        return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')
    return HttpResponse(ERROR_JSON['delete_id'], content_type='text/json-comment-filtered')

def artwork(request):
    if request.method == 'GET':
        return artwork_get(request)
    if request.method == 'POST':
        return artwork_post(request)
    if request.method == 'PUT':
        return artwork_put(request)
    if request.method == 'DELETE':
        return artwork_delete(request)
    return render(request, 'main/index.html')

def artwork_get(request):
    if request.GET:
        id = request.GET['id']
        artwork = Artwork.objects.filter(id=id)
        json_artwork = serializers.serialize('json', artwork)
        return HttpResponse(json_artwork, content_type='text/json-comment-filtered')

    artwork_list = Artwork.objects.all()
    json_artwork_list = serializers.serialize('json', artwork_list)
    return HttpResponse(json_artwork_list, content_type='text/json-comment-filtered')

def artwork_post(request):
    format = "%Y-%m-%d"

    name = None
    creation_date = None
    description = None
    authors_id = None
    type_id = None
    pms_id = None

    if 'name' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    name = request.GET['name']

    if len(name) > 30:
        return HttpResponse(ERROR_JSON['artwork_max_length'], content_type='text/json-comment-filtered')

    if 'creation_date' in request.GET.keys():
        creation_date = request.GET['creation_date']

        try:
            datetime.datetime.strptime(creation_date, format)

        except ValueError:
            return HttpResponse(ERROR_JSON['artwork_start_date'], content_type='text/json-comment-filtered')

    if 'description' in request.GET.keys():
        description = request.GET['description']

        if len(description) > 60:
            return HttpResponse(ERROR_JSON['artwork_description'], content_type='text/json-comment-filtered')

    if 'authors_id' in request.GET.keys():
        authors_id = eval(request.GET['authors_id'])
        for author_id in authors_id:
            i = int(author_id)
            if not Artist.objects.filter(id=i):
                return HttpResponse(ERROR_JSON['artwork_author_id'], content_type='text/json-comment-filtered')

    if 'pms_id' in request.GET.keys():
        pms_id = eval(request.GET['pms_id'])
        for pm_id in pms_id:
            i = int(pm_id)
            if not PeriodsAndMovements.objects.filter(id=i):
                return HttpResponse(ERROR_JSON['artwork_pm_id'], content_type='text/json-comment-filtered')

    if 'type_id' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    type_id = int(request.GET['type_id'])

    new_artwork = Artwork(name=name, creation_date=creation_date, arttype_id=type_id, description=description)
    new_artwork.save()

    if authors_id != None:
        for author_id in authors_id:
            i = int(author_id)
            new_artwork.author.add(Artist.objects.filter(id=i)[0])

    if pms_id != None:
        for pm_id in pms_id:
            i = int(pm_id)
            new_artwork.pm.add(PeriodsAndMovements.objects.filter(id=i)[0])
    return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')

def artwork_put(request):
    format = "%Y-%m-%d"

    id = None
    name = None
    creation_date = None
    description = None
    authors_id = None
    type_id = None
    pms_id = None

    if 'id' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    id = request.GET['id']

    if 'name' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    name = request.GET['name']

    if len(name) > 30:
        return HttpResponse(ERROR_JSON['artwork_max_length'], content_type='text/json-comment-filtered')

    if 'creation_date' in request.GET.keys():
        creation_date = request.GET['creation_date']

        try:
            datetime.datetime.strptime(creation_date, format)

        except ValueError:
            return HttpResponse(ERROR_JSON['artwork_start_date'], content_type='text/json-comment-filtered')

    if 'description' in request.GET.keys():
        description = request.GET['description']

        if len(description) > 60:
            return HttpResponse(ERROR_JSON['artwork_description'], content_type='text/json-comment-filtered')

    if 'authors_id' in request.GET.keys():
        authors_id = eval(request.GET['authors_id'])
        for author_id in authors_id:
            i = int(author_id)
            if not Artist.objects.filter(id=i):
                return HttpResponse(ERROR_JSON['artwork_author_id'], content_type='text/json-comment-filtered')

    if 'pms_id' in request.GET.keys():
        pms_id = eval(request.GET['pms_id'])
        for pm_id in pms_id:
            i = int(pm_id)
            if not PeriodsAndMovements.objects.filter(id=i):
                return HttpResponse(ERROR_JSON['artwork_pm_id'], content_type='text/json-comment-filtered')

    if 'type_id' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    type_id = int(request.GET['type_id'])

    new_artwork = Artwork(id=id, name=name, creation_date=creation_date, arttype_id=type_id, description=description)
    new_artwork.save()

    new_artwork.author.clear()
    if authors_id != None:
        for author_id in authors_id:
            i = int(author_id)
            new_artwork.author.add(Artist.objects.filter(id=i)[0])

    new_artwork.pm.clear()
    if pms_id != None:
        for pm_id in pms_id:
            i = int(pm_id)
            new_artwork.pm.add(PeriodsAndMovements.objects.filter(id=i)[0])
    return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')

def artwork_delete(request):
    if 'id' not in request.GET.keys():
        return HttpResponse(ERROR_JSON['not_enough_data'], content_type='text/json-comment-filtered')

    id = request.GET['id']
    delete_artist = PeriodsAndMovements.objects.filter(id=id)
    if delete_artist:
        delete_artist.delete()
        return HttpResponse(ERROR_JSON['no_error'], content_type='text/json-comment-filtered')
    return HttpResponse(ERROR_JSON['delete_id'], content_type='text/json-comment-filtered')