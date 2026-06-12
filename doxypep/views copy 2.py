from django.shortcuts import render
from  django.db.models import Count
from .models import Culture, Kb, Patient
from django.db.models.functions import TruncMonth, TruncDate
from django.utils import timezone
from django.shortcuts import render

def get_participantChart():
    '''
    This is syncing graph where both graphs can be tracked at the same time.
    The Doxycycline graph will show the percentage of participants with positives for each culture.
    The Non-Doxycycline graph will show the percentage of participants with negatives for each culture.
    The x-axis will be the visit number and the y-axis will be the percentage of participants.

    The method:
    1. First get the total number of active (status = True or 1) participants in the study.
    2. Then get the number of participants taking doxycycline versus not taking doxycycline.
    3. Going into the culture table, filter participants with positive cultures results (1) for each isolate by visit number and doxycycline status.
    4. Count the amount of positive cultures for each isolate by visit number and doxycycline status.
    5. Divide the count of positive cultures by the total number of participants with respective doxy status.
    6. Append 0s to the data list of there are no positive cultures in that visit number.
    7. The data is passed into the .html file which will pass the data into 'syncingchart.js' to render the graph.
    '''
    isolates = ['phar_sa', 'nas_sa', 'rec_sa', 'rec_esbl', 'rec_mac'] 
    value = 1
    doxy_participant = []
    nodoxy_participant = []

    doxypatients = Patient.objects.filter(status=True).filter(treatment=True)
    doxypatients = [item.id for item in doxypatients]

    nodoxypatients = Patient.objects.filter(status=True).filter(treatment=False)
    nodoxypatients = [item.id for item in nodoxypatients]

    visit = (Culture.objects.values('visit_num').distinct())
    visit = [item['visit_num'] for item in visit]
    # print(visit)

    culture = Culture.objects.filter(patient_num_id__in=doxypatients)

    doxy_total = (
        Culture.objects
        .filter(patient_num_id__in=doxypatients)
        .values('visit_num')
        .annotate(count=Count('id'))
    )
    doxy_total = [item['count'] for item in doxy_total]
    # print(doxy_total)

    nondoxy_total = (
        Culture.objects
        .filter(patient_num_id__in=nodoxypatients)
        .values('visit_num')
        .annotate(count=Count('id'))
    )
    nondoxy_total = [item['count'] for item in nondoxy_total]
    # print(nondoxy_total)

    for item in isolates:
        key = f"{item}__icontains"
        counts = (
            Culture.objects
            .filter(**{key:value})
            .filter(patient_num_id__in=doxypatients)
            .values('visit_num')
            .annotate(count=Count('id'))
        )
        data_point = [item['count'] for item in counts]
        # print(data_point)

        for i in range(len(data_point)):
            data_point[i] = int(data_point[i]/doxy_total[i] * 100)

        doxy_participant.append({
            'name': item,
            'data': data_point
        })
        
        max_visit = max(len(item['data']) for item in doxy_participant)
        for item in doxy_participant:
            while len(item['data']) < max_visit:
                item['data'].append(0)

    for item in isolates:
        key = f"{item}__icontains"
        counts = (
            Culture.objects
            .exclude(**{key:value})
            .filter(patient_num_id__in=nodoxypatients)
            .values('visit_num')
            .annotate(count=Count('id'))
        )
        data = [item['count'] for item in counts]
        print(data)

        for i in range(len(data)):
            data[i] = int(data[i]/nondoxy_total[i] * 100)

        nodoxy_participant.append({
            'name': item,
            'data': data
        })
        
        max_visit = max(len(item['data']) for item in nodoxy_participant)
        for item in nodoxy_participant:
            while len(item['data']) < max_visit:
                item['data'].append(0)

    # print("Doxy:", doxy_participant)
    # print("Non-Doxy:", nodoxy_participant)

    doxy_count = (
        Culture.objects
        .filter(patient_num_id__in=doxypatients)
        .values('visit_num')
        .annotate(count=Count('id'))
    )
    doxy_count = [item['count'] for item in doxy_count]
    print("Doxy Count:", doxy_count)

    nondoxy_count = (
        Culture.objects
        .filter(patient_num_id__in=nodoxypatients)
        .values('visit_num')
        .annotate(count=Count('id'))
    )
    nondoxy_count = [item['count'] for item in nondoxy_count]
    print("Non-Doxy Count:", nondoxy_count)

    context = {
        'doxy': doxy_participant,
        'nodoxy': nodoxy_participant,
        'doxy_total': doxy_count,
        'nodoxy_total': nondoxy_count,
        'labels': visit
    }
    # print(context)

    return {'syncingChart': context}

def get_multiChart():
    isolates = ['phar_sa', 'nas_sa', 'rec_sa', 'rec_esbl', 'rec_mac'] 
    value = 1 
    queryset = []

    visit = (Culture.objects.values('visit_num').distinct())
    visit = [item['visit_num'] for item in visit]

    total = (Culture.objects.values('visit_num').annotate(count=Count('id')))
    total = [item['count'] for item in total]
    print(total)

    for item in isolates:
        key = f"{item}__icontains"
        query = (
            Culture.objects
            .filter(**{key:value})
            .values('visit_num')
            .annotate(count=Count('id'))
        )
        print(query)

        data_point = [item['count'] for item in query]
        print(data_point)

        for i in range(len(data_point)):
            # print(item, data_point[i], total[i])
            data_point[i] = int(data_point[i]/total[i] * 100)

        queryset.append({
            'name': item,
            'data': data_point
        })
        
        max_visit = max(len(item['data']) for item in queryset)
        for item in queryset:
            while len(item['data']) < max_visit:
                item['data'].append(0)

    context = {
        'series': queryset,
        'labels': visit
    }
    print(queryset)

    return {'multiChart': context}
'''
def get_treedata():
    tree = []

    total = (
        Culture.objects
        .values('id')
        .annotate(count=Count('id'))
    )
    data = len([item['count'] for item in total])
    print(data)

    tree.append(data)
    print(tree)

    nasal = (
        Culture.objects
        .filter(nas_sa__isnull=False)
    )
    nas_data = len([item.id for item in nasal])

    tree.append(nas_data)
    print(tree)

    nas_pos = (
        Culture.objects
        .filter(nas_sa__isnull=False)
        .filter(nas_sa__icontains=1)
    )
    nas_pos_data = len([item.id for item in nas_pos])
    tree.append(nas_pos_data)
    print(tree)

    nas_kb = (
        Kb.objects
        .filter(sample_type=6)
    )

    nas_kb = len([item.id for item in nas_kb])
    tree.append(nas_kb)
    print(tree)

    nas_neg_data = nas_data - nas_pos_data
    tree.append(nas_neg_data)
    print(tree)

    pharygneal = (
        Culture.objects
        .filter(phar_sa__isnull=False)
    )
    phar_data = len([item.id for item in pharygneal])
    tree.append(phar_data)
    print(tree)

    phar_pos = (
        Culture.objects
        .filter(phar_sa__isnull=False)
        .filter(phar_sa__icontains=1)
    )
    phar_pos_data = len([item.id for item in phar_pos])
    tree.append(phar_pos_data)
    print(tree)

    phar_kb = (
        Kb.objects
        .filter(sample_type=4)
    )
    phar_kb = len([item.id for item in phar_kb])
    tree.append(phar_kb)
    print(tree)

    phar_neg_data = phar_data - phar_pos_data
    tree.append(phar_neg_data)
    print(tree)

    rectal = (
        Culture.objects
        .filter(rec_sa__isnull=False)
    )
    rec_data = len([item.id for item in rectal])

    tree.append(rec_data)
    print(tree)

    rec_pos = (
        Culture.objects
        .filter(rec_sa__isnull=False)
        .filter(rec_sa__icontains=1)
    )
    rec_pos_data = len([item.id for item in rec_pos])
    tree.append(rec_pos_data)
    print(tree)

    rec_kb = (
        Kb.objects
        .filter(sample_type=5)
    )
    rec_kb = len([item.id for item in rec_kb])
    tree.append(rec_kb)
    print(tree)

    rec_neg_data = rec_data - rec_pos_data
    tree.append(rec_neg_data)
    print(tree)

    tree_data = {
        "name": f"Total Collection<br>{tree[0]}",
        "children": [
            {
                "name": f"Nasal<br>{tree[1]}",
                "children": [
                    {
                        "name": f"Postive<br>{tree[2]}",
                        "children": [
                            {
                                "name": f"KB Assay<br>{tree[3]}",
                                "children": [
                                    {"name": "WGS"},
                                ]
                            },
                        ]
                    }, {"name": f"Negative<br>{tree[4]}"}]
            },
            {
                "name": f"Pharyngeal<br>{tree[5]}",
                "children": [
                    {
                        "name": f"Postive<br>{tree[6]}",
                        "children": [
                            {
                                "name": f"KB Assay<br>{tree[7]}",
                                "children": [
                                    {"name": "WGS"},
                                ]
                            },
                        ]
                    }, {"name": f"Negative<br>{tree[8]}"}]
            },
            {
                "name": f"Rectal<br>{tree[9]}",
                "children": [
                    {
                        "name": f"Postive<br>{tree[10]}",
                        "children": [
                            {
                                "name": f"KB Assay<br>{tree[11]}",
                                "children": [
                                    {"name": "WGS"},
                                ]
                            },
                        ]
                    }, {"name": f"Negative<br>{tree[12]}"}]
            }
        ]
    }

    return {'tree_data': tree_data}
'''
def get_pieChart(database):
    # Equivalent to SELECT 'organism', COUNT(*) FROM `wgs` GROUP BY 'organism';

    query = database.objects.filter(status=True).values('patient_type').annotate(count=Count('patient_type'))
    print(query)

    # Building an array
    labelData = [item['patient_type'] for item in query]
    seriesData = [item['count'] for item in query]
    context = {
        'labels': labelData,
        'series': seriesData
    }

    return {'pieChart': context}

# Create your views here.
def archive(request):
    tree = get_treedata()
    tree_data = tree['tree_data']

    query = Patient.objects.filter(status=True).values('patient_type').annotate(count=Count('patient_type'))
    print(query)

    data = get_pieChart(Patient)
    data = data['pieChart']

    print(data)

    for item in data['labels']:
        if item == True:
            data['labels'][data['labels'].index(item)] = 'Doxycycline'
        elif item == False:
            data['labels'][data['labels'].index(item)] = 'Control'

    print(data['labels'])

    context = {
        'pie_labels': data['labels'],
        'pie_series': data['series'],
        'pie_title': 'Patient Type Distribution'
    }

    multiline = get_participantChart()
    multiline = multiline['syncingChart']

    sync = {
        'doxy_series': multiline['doxy'],
        'nodoxy_series': multiline['nodoxy'],
        'x_labels': multiline['labels'],
        'doxy_total': multiline['doxy_total'],
        'nodoxy_total': multiline['nodoxy_total']
    }
    print(sync)
    
    return render(request, 'archive.html', {'pie_data': context, 'tree_data': tree_data, 'data': sync})

def dashboard(request):

    query = Patient.objects.filter(status=True).values('patient_type').annotate(count=Count('patient_type'))
    print(query)

    data = get_pieChart(Patient)
    data = data['pieChart']

    print(data)

    for item in data['labels']:
        if item == True:
            data['labels'][data['labels'].index(item)] = 'Doxycycline'
        elif item == False:
            data['labels'][data['labels'].index(item)] = 'Control'

    print(data['labels'])

    context = {
        'pie_labels': data['labels'],
        'pie_series': data['series'],
        'pie_title': 'Patient Type Distribution'
    }

    multiline = get_participantChart()
    multiline = multiline['syncingChart']

    sync = {
        'doxy_series': multiline['doxy'],
        'nodoxy_series': multiline['nodoxy'],
        'x_labels': multiline['labels'],
        'doxy_total': multiline['doxy_total'],
        'nodoxy_total': multiline['nodoxy_total']
    }
    print(sync)
    
    return render(request, 'dashboard.html', {'pie_data': context, 'data': sync})