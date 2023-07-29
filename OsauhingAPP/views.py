from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

#mudelid ja serializerid
from OsauhingAPP.models import Isikud, Osauhing, Osauhing_Isikud
from OsauhingAPP.serializers import IsikudSerializer, Osauhing_IsikudSerializer, OsauhingSerializer

# Create your views here.
    
'''
link - /isik/<num>, kus num on id mudelis Isikud
GET - valjastab isiku andmed, otsib id jargi
'''
@csrf_exempt
def IsikAPI(request, id = 0):
    if request.method == 'GET':
        try:
            isik = Isikud.objects.get(id = id)
            if isik.isikutyyp == 'J':
                # kui isik on J, siis kuvame ka lisainfo
                osauhing = Osauhing.objects.get(isik=id)
                #osauhingu asutaja andmed
                oi = Osauhing_Isikud.objects.filter(osauhing = osauhing.id)
                oi2 = Osauhing_IsikudSerializer(oi, many=True)

                osauhing_isikud_isik_id= Osauhing_Isikud.objects.filter(osauhing = osauhing.id).values_list('isik')
                asutajad = Isikud.objects.filter(id__in = osauhing_isikud_isik_id)
                asutajad_serializer = IsikudSerializer(asutajad, many=True)
                asutajad_norm = {}
                
                for asutaja in asutajad_serializer.data:
                    for lisainfo in oi2.data:
                        if asutaja['id'] == lisainfo['isik']:
                            asutajad_norm[asutaja['id']] = {
                                'id':asutaja['id'],
                                'isikutyyp': asutaja['isikutyyp'],
                                'isosauhing': asutaja['isosauhing'],
                                'nimi': asutaja['nimi'],
                                'perenimi': asutaja['perenimi'],
                                'kood': asutaja['kood'],
                                'osauhinguOsa':lisainfo['osauhinguOsa'],
                                'isasutaja':lisainfo['isasutaja']
                                }
                            

                #teeme oma json
                x = {
                    "id": isik.id,
                    "isikutyyp": isik.isikutyyp,
                    "isosauhing": isik.isosauhing,
                    "nimi": isik.nimi,
                    "kood": isik.kood,
                    "asutamiseKP": osauhing.asutamisekp,
                    "kogukapital": osauhing.kogukapital,
                    "asutajad": asutajad_norm
                }
                return JsonResponse(x, safe=False)
            else:
                # kui isik ei ole F, siis kuvame isiku andmeid
                isik_serializer = IsikudSerializer(isik)
                return JsonResponse(isik_serializer.data, safe=False)
        except:
            return JsonResponse("Failed to find", safe=False)

'''
link - /create
POST - kontrollib ja loob andmeid.
'''
@csrf_exempt 
def createAPI(request):
    if request.method == 'POST':
        # loeme vastuvoetud andmed
        try:
            data = JSONParser().parse(request)
            nimi = data['nimi']
            registrikood = data['registrikood']
            Asutamiskuupaev = data['Asutamiskuupäev']
            Kogukapital = data['Kogukapital']
            asutajad = data['asutajad']
        except:
            return JsonResponse("Failed to read", safe=False)
        
        # otsime andmed
        try:
            # kontrollime, kas sisestatud andmed baasis olemas. Kui olemas tagastame veateade
            o_kood = Isikud.objects.filter(isosauhing = True , kood = registrikood).count()
            o_nimi = Isikud.objects.filter(isosauhing = True , nimi = nimi).count()
            if (o_kood == 1):
                return JsonResponse("selle registrikoodiga osauhing juba registreeritud", safe=False)
            elif(o_kood >= 2):
                return JsonResponse("Votke uhendus helpdeskiga, tekkis viga baasis", safe=False)
            elif (o_nimi == 1):
                return JsonResponse("selle nimega osauhing juba registreeritud", safe=False)
            elif(o_kood >= 2 ):
                return JsonResponse("Votke uhendus helpdeskiga, tekkis viga baasis", safe=False)
            else:
                # otsime iga asutaja
                for asutaja in asutajad:
                    try:
                        leitudAsutaja = Isikud.objects.get(kood = asutaja['kood'])
                        if((leitudAsutaja.nimi != asutaja['nimi']) or (leitudAsutaja.perenimi != asutaja['perenimi'])):
                        #isik leitud, aga andmed erinevad
                            return JsonResponse("IK "+asutaja['kood']+" leitud, aga nimi ei klapi", safe=False)
                        #isik leitud salvestada pole vaja
                    except:
                        pass
                        #isik pole leitud vaja salvestada
                        #return JsonResponse("IK "+asutaja['kood']+" pole leitud", safe=False)

        except:
            return JsonResponse("Failed to find", safe=False)
        
        # salvestame andmeid
        try:
            # loome andmed
            t_isikud_osauhing_data = {
                "isikutyyp": "J", 
                "isosauhing": True,
                "nimi": nimi,
                "perenimi": None,
                "kood": registrikood
            }

            # kasutame serializer ja kui andmed korras - salvestame 
            try:
                isik_serializer = IsikudSerializer(data=t_isikud_osauhing_data)
                if isik_serializer.is_valid():
                    isik_serializer.save()
                    #return JsonResponse("Added Successfully", safe=False)
            except:
                return JsonResponse("Failed to add t_isikud_osauhing_data", safe=False)
            
            # meil vaja osauhingu_id, et luua seos
            osauhingID = Isikud.objects.get(isosauhing = True , kood = registrikood)
            
            # loome andmed
            t_osauhing_osauhing_data = {
                "isik": osauhingID.id, # osauhingu id isiku tabelis
                "asutamisekp": Asutamiskuupaev,
                "kogukapital": Kogukapital
            }
            # kasutame serializer ja kui andmed korras - salvestame
            try:
                osauhing_serializer = OsauhingSerializer(data=t_osauhing_osauhing_data)
                if osauhing_serializer.is_valid(raise_exception=True):
                    osauhing_serializer.save()
                    #return JsonResponse("Added Successfully", safe=False)
            except:
                return JsonResponse("Failed to add t_osauhing_osauhing_data", safe=False)
            
            # nuud asutajad
            for asutaja in asutajad:
                    try:
                        leitudAsutaja = Isikud.objects.get(kood = asutaja['kood'])
                        #isik leitud, salvestada isiku andmed pole vaja

                    except:
                        #isik pole leitud vaja salvestada
                        if(asutaja['isikutyyp'] == 'F'):
                            t_isikud_asutaja_data = {
                                "isikutyyp": asutaja['isikutyyp'], 
                                "isosauhing": False,
                                "nimi": asutaja['nimi'],
                                "perenimi": asutaja['perenimi'],
                                "kood": asutaja['kood'] 
                            }
                        else:
                            t_isikud_asutaja_data = {
                                "isikutyyp": asutaja['isikutyyp'], 
                                "isosauhing": False,
                                "nimi": asutaja['nimi'],
                                "perenimi": None,
                                "kood": asutaja['kood'] 
                            }
                        
                        # kasutame serializer ja kui andmed korras - salvestame
                        try:
                            asutaja_serializer = IsikudSerializer(data=t_isikud_asutaja_data)
                            if asutaja_serializer.is_valid():
                                asutaja_serializer.save()
                                #return JsonResponse("Added Successfully", safe=False)
                        except:
                            return JsonResponse("Failed to add t_isikud_asutaja_data", safe=False)
                        leitudAsutaja = Isikud.objects.get(kood = asutaja['kood'])

                    # nuud loome seos isik-osauhing
                    try:
                        # vaja osauhingu_id
                        osauhing = Osauhing.objects.get(isik = osauhingID.id)

                        # loome andmed
                        t_osauhing_isikud_asytaja_data = {
                        "osauhing": osauhing.id, # osauhingu id osauhingu tabelis
                        "isik": leitudAsutaja.id,# asutaja id isiku tabelis
                        "osauhinguOsa": asutaja['osauhinguOsa'],
                        "isasutaja": True
                        }

                        # kasutame serializer ja kui andmed korras - salvestame
                        try:
                            osauhing_asutaja_serializer = Osauhing_IsikudSerializer(data=t_osauhing_isikud_asytaja_data)
                            if osauhing_asutaja_serializer.is_valid():
                                osauhing_asutaja_serializer.save()
                                #return JsonResponse("Added Successfully", safe=False)
                        except:
                            return JsonResponse("Failed to add t_osauhing_isikud_asytaja_data", safe=False)
                    except:
                        return JsonResponse("Failed to safe asutaja-osauhing seos", safe=False)
            
            successAnswer = f'Added Successfully//{osauhingID.id}'
            return JsonResponse(successAnswer, safe=False)                       
        except:
            return JsonResponse("Failed to safe", safe=False)

'''
link - /edit
PUT - kontrollib, muudab ja salvestab saadetud andmed.
muudab Kogukapital, asutajate osa ja lisab veel asutajad. (uued asutajad - isasutaja: False)
'''
@csrf_exempt 
def muudaAPI(request):
    if request.method == 'PUT':
        # loeme vastuvoetud andmed
        # kui koik on korras, siis tegeleme edasi
        # kui midagi on vale, siis tagastame veateade
        try:
            data = JSONParser().parse(request)
            registrikood = data['registrikood']
            Kogukapital = data['Kogukapital']
            Asutamiskuupaev = data['Asutamiskuupäev']
            asutajad = data['asutajad']
            uued_asutajad = data['uued_asutajad']
        except:
            return JsonResponse("Failed to read", safe=False)
        
        # otsime andmed
        try:   
            o_kood = Isikud.objects.filter(isosauhing = True , kood = registrikood).count()
            if(o_kood >= 2):
                return JsonResponse("Votke uhendus helpdeskiga, tekkis viga baasis", safe=False)
            else:
                # pole veel teada, kas uued asutajad baasis olmas. kontrollime andmeid
                for asutaja in uued_asutajad:
                    try:
                        leitudAsutaja = Isikud.objects.get(kood = asutaja['kood'])
                        if((leitudAsutaja.nimi != asutaja['nimi']) or (leitudAsutaja.perenimi != asutaja['perenimi'])):
                        #isik leitud, aga andmed erinevad
                            return JsonResponse("IK "+asutaja['kood']+" leitud, aga nimi ei klapi", safe=False)
                        #isik leitud salvestada pole vaja
                    except:
                        pass
                        #isik pole leitud vaja salvestada
                        #return JsonResponse("IK "+asutaja['kood']+" pole leitud", safe=False)
        except:
            return JsonResponse("Failed to find during update", safe=False)
        
        # salvestame andmeid
        try:
            # leiame osauhingu andmed            
            osauhingID = Isikud.objects.get(isosauhing = True , kood = registrikood)
            osauhing = Osauhing.objects.get(isik = osauhingID.id)
            
            # satistame parandatud andmed
            t_osauhing_osauhing_data = {
                "id": osauhing.id,
                "isik": osauhingID.id, # osauhingu id isiku tabelis
                "asutamisekp": Asutamiskuupaev,
                "kogukapital": Kogukapital
            }
            
            # kasutame serializer ja kui andmed korras - salvestame 
            try:
                osauhing_serializer = OsauhingSerializer(osauhing, data=t_osauhing_osauhing_data)
                if osauhing_serializer.is_valid():
                    osauhing_serializer.save()
                    #return JsonResponse("Updated", safe=False)
            except:
                return JsonResponse("Failed to add t_osauhing_osauhing_data", safe=False)
            
            # juba registreeritud asutajad
            for asutaja in asutajad:
                #asutaja juba baasis olemas, seega vaja ainult leida
                leitudAsutaja = Isikud.objects.get(kood = asutaja['kood'])

                # nuud uuendame seos isik-osauhing
                try:
                    # leiame asutaja andmed, osauhingu andmed juba varem leitud
                    osauhing_asutaja = Osauhing_Isikud.objects.get(osauhing = osauhing.id,isik = leitudAsutaja.id )

                    # satistame parandatud andmed
                    t_osauhing_isikud_asytaja_data = {
                    "id": osauhing_asutaja.id,
                    "osauhing": osauhing.id, # osauhingu id osauhingu tabelis
                    "isik": leitudAsutaja.id,# asutaja id isiku tabelis
                    "osauhinguOsa": asutaja['osauhinguOsa'],
                    "isasutaja": osauhing_asutaja.isasutaja
                    }

                    # kasutame serializer ja kui andmed korras - salvestame 
                    try:
                        osauhing_asutaja_serializer = Osauhing_IsikudSerializer(osauhing_asutaja, data=t_osauhing_isikud_asytaja_data)
                        if osauhing_asutaja_serializer.is_valid():
                            osauhing_asutaja_serializer.save()
                    except:
                        return JsonResponse("Failed to update t_osauhing_isikud_asytaja_data", safe=False)
                except:
                    return JsonResponse("Failed to update asutaja-osauhing seos", safe=False)
            
            # uued registreeritud asutajad
            for asutaja in uued_asutajad:
                    try:
                        leitudAsutaja = Isikud.objects.get(kood = asutaja['kood'])
                        #isik baasis olemas, salvestada isiku andmed pole vaja
                    except:
                        #isik pole leitud vaja salvestada
                        if(asutaja['isikutyyp'] == 'F'):
                            t_isikud_asutaja_data = {
                                "isikutyyp": asutaja['isikutyyp'], 
                                "isosauhing": False,
                                "nimi": asutaja['nimi'],
                                "perenimi": asutaja['perenimi'],
                                "kood": asutaja['kood'] 
                            }
                        else:
                            t_isikud_asutaja_data = {
                                "isikutyyp": asutaja['isikutyyp'], 
                                "isosauhing": False,
                                "nimi": asutaja['nimi'],
                                "perenimi": None,
                                "kood": asutaja['kood'] 
                            }
                        
                        # kasutame serializer ja kui andmed korras - salvestame 
                        try:
                            asutaja_serializer = IsikudSerializer(data=t_isikud_asutaja_data)
                            if asutaja_serializer.is_valid():
                                asutaja_serializer.save()
                                #return JsonResponse("Added Successfully", safe=False)
                        except:
                            return JsonResponse("Failed to add t_isikud_asutaja_data", safe=False)
                        leitudAsutaja = Isikud.objects.get(kood = asutaja['kood'])

                    # nuud loome seos isik-osauhing
                    try:
                        # leiame asutaja andmed
                        osauhing = Osauhing.objects.get(isik = osauhingID.id)

                        # satistame parandatud andmed
                        t_osauhing_isikud_asytaja_data = {
                        "osauhing": osauhing.id, # osauhingu id osauhingu tabelis
                        "isik": leitudAsutaja.id,# asutaja id isiku tabelis
                        "osauhinguOsa": asutaja['osauhinguOsa'],
                        "isasutaja": False
                        }

                        # kasutame serializer ja kui andmed korras - salvestame 
                        try:
                            osauhing_asutaja_serializer = Osauhing_IsikudSerializer(data=t_osauhing_isikud_asytaja_data)
                            if osauhing_asutaja_serializer.is_valid():
                                osauhing_asutaja_serializer.save()
                                #return JsonResponse("Added Successfully", safe=False)
                        except:
                            return JsonResponse("Failed to add t_osauhing_isikud_asytaja_data", safe=False)
                    except:
                        return JsonResponse("Failed to safe asutaja-osauhing seos", safe=False)
                    
            successAnswer = f'Updated Successfully//{osauhingID.id}'
            return JsonResponse(successAnswer, safe=False)  
                                 
        except:
            return JsonResponse("Failed to Update", safe=False)
    

    
'''
link - /otsing
param - otsing <str,num> (nimi, perenimi voi kood), otsing_checked (true - osauhing, false - osanikud)
GET - otsib ja valjastab leitud andmeid
'''
def OtsingAPI(request, id = 0):    
    if request.method == 'GET':
        #votame saadetud otsingu param.
        otsing = request.GET.get('otsing', None)
        otsing_checked = request.GET.get('otsing_checked', None)

        # kui otsingu vali pole tyhi, siis otsime
        #  kui tyhi, siis valjastame tyhjus
        if otsing:
            # kontrollime, kas me otsime osauhingu andmed voi lihtsalt isiku andmed (osaniku andmed)
            if (otsing_checked == 'true'):
                # osauhingu otsimine
                try:
                    isikud = Isikud.objects.filter(
                        isikutyyp = 'J', isosauhing = True, kood__icontains=otsing
                        ).order_by('nimi', 'kood') | Isikud.objects.filter(
                        isikutyyp = 'J', isosauhing = True, nimi__icontains=otsing
                        ).order_by('nimi', 'kood')
                except:
                    return JsonResponse("osauhingu otsimine ebaonnestunud", safe=False)  
            else:
                # osaniku otsimine
                try:
                    isikud = Isikud.objects.filter(
                        kood__icontains=otsing
                        ).order_by('nimi', 'perenimi', 'kood') | Isikud.objects.filter(
                        nimi__icontains=otsing
                        ).order_by('nimi', 'perenimi', 'kood') | Isikud.objects.filter(
                            perenimi__icontains=otsing
                            ).order_by('nimi', 'perenimi', 'kood')
                except:
                    return JsonResponse("isiku otsimine ebaonnestunud", safe=False) 
        else:
            # otsinguvali tyhi
            return JsonResponse([], safe=False)

        isikud_serializer = IsikudSerializer(isikud, many=True)
        return JsonResponse(isikud_serializer.data, safe=False)
