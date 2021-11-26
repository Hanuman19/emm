import decimal
from decimal import Decimal, ROUND_HALF_UP
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib import messages
from decimal import Decimal
import time
from django.contrib.auth.models import User

from .models import Driver, Loko, Region, Norms, Equipment, Settings, Result_trail, Report, Menu,Result_manevr
from .serializers import (DriverListSerializer, 
                         LokoListSerializer,LokoCreateSerializer, 
                         NormListSerializer, RegionSerializer,
                         LokoSelectSerializer, DriverSelectSerializer,
                         NormCreateSerializer, ResultTrailSerializer,
                         ResultTrailListSerializer, ReportSerializer,
                         ReportAreaManevrSerializer, ResultManevrSerializer,
                         DriverCreateSerializer, ReportDriverSerializer,
                         MenuSerializer, ReportLokoSerializer,
                         ReportAreaSerializer, ReportTWSerializer,
                         ResultManevrListSerializer, ReportDataSerializer)
from .function import (functionRegion, functionLoko, NormaKhakasia,
                        NormValidate, ReportKhakasia, functionDriver, differenceReport,
                        deleteOperation, OperationValidate)

class DriverListView(APIView):
    """ Вывод списка машинистов """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):                     
                
        if request.user.groups.filter(name="Admin"): 
            drivers = Driver.objects.all()
            serializer = DriverListSerializer(drivers, many=True)
            return Response(serializer.data)
        else:
            drivers = Driver.objects.filter(region_id=functionRegion(request))
            serializer = DriverListSerializer(drivers, many=True)
            return Response(serializer.data)

    def post(self, request):        
        if Driver.objects.filter(name=request.data['name']).values_list('id').exists() and request.data['id'] == None:
            messages='Такой машинист существует'
            return Response(messages)
        else:                      
            driver = DriverCreateSerializer(data=functionDriver(request))
            if driver.is_valid():                      
                driver.save(id=request.data.get('id'))                                                
                return Response('true',status=201)
            return Response(driver.errors,status=400)


class LokoListView(APIView):
    """Вывод списка локомотивов"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):

        if request.user.groups.filter(name="Admin"):
            loko = Loko.objects.all()
            serializer = LokoListSerializer(loko, many=True)
            return Response(serializer.data)
        else:
            loko = Loko.objects.filter(region=functionRegion(request))            
            serializer = LokoListSerializer(loko, many=True)
            return Response(serializer.data)

    def post(self, request):        
        if Loko.objects.filter(name=request.data['name']).values_list('id') != None and  request.data['id'] == None:
            messages='Такой локомотив существует'            
            return Response(messages)
        else:           
            loko = LokoCreateSerializer(data=functionLoko(request))
            if loko.is_valid():                      
                loko.save(id=request.data.get('id'))
                test = Loko.objects.get(name=request.data['name'], element_type=request.data['element_type'], section=request.data['section'])
                test.region.add(request.data['region'][0])                                 
                return Response('true',status=201)
            return Response(loko.errors,status=400)


class NormListView(APIView):
    """Вывод норм"""

    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request):
        
        if request.user.groups.filter(name="Admin"):  
            return Response('UPS')
        else:               
            norm=Norms.objects.filter(region = functionRegion(request)).order_by('-id')
            serializer=NormListSerializer(norm,many=True) 
            return Response(serializer.data)
        
        

    def post(self, request): 
        mes = NormValidate(request)
        if mes == True:      
            norm = NormCreateSerializer(data=request.data)        
            if norm.is_valid():            
                norm.save(id=request.data.get('id'))             
                return Response('true',status=201)
            return Response(norm.errors,status=400)
        else:            
            return Response(mes)


class RegionListView(APIView):
    """Список регионов"""

    permission_classes = [permissions.IsAuthenticated]

    def get (self, request):        
        if request.user.groups.filter(name="Admin"): 
            region=Region.objects.filter(element_type='section', section=None)
            serializer=RegionSerializer(region,many=True) 
            return Response(serializer.data)
        else:
            role=request.user.groups.all().values_list('id', flat=True)
            region = Region.objects.filter(role=role[0], element_type='section', section=None)
            serializer=RegionSerializer(region,many=True) 
            return Response(serializer.data)

    
class LokoSelectView(APIView):
    """Список типов секций в селект"""

    permission_classes = [permissions.IsAuthenticated]

    def get (self, request):
        if request.user.groups.filter(name="Admin"):
            loko=Loko.objects.filter(element_type='section', section=None)
            serializer=LokoSelectSerializer(loko,many=True) 
            return Response(serializer.data)
        else:
            role=request.user.groups.all().values_list('id', flat=True)
            region = Region.objects.filter(role=role[0], element_type='section', section=None).values_list('id', flat=True)            
            loko=Loko.objects.filter(element_type='section', section=None, region=region[0])           
            serializer=LokoSelectSerializer(loko,many=True) 
            return Response(serializer.data)


class DriverSelectView(APIView):
    """Список машинистов в селект"""

    permission_classes = [permissions.IsAuthenticated]

    def get (self, request):
        if request.user.groups.filter(name="Admin"):           
            return Response('UPS')
        else:
            role=request.user.groups.all().values_list('id', flat=True)
            region = Region.objects.filter(role=role[0], element_type='section', section=None).values_list('id', flat=True)
            driver=Driver.objects.filter(region=region[0])
            serializer=DriverSelectSerializer(driver,many=True) 
            return Response(serializer.data)
    def post (self, request):
        role=request.user.groups.all().values_list('id', flat=True)
        region = Region.objects.filter(role=role[0], element_type='section', section=None).values_list('id', flat=True)

        message = 'Не возможно расчитать норму, проверьте заполненые данные и наличие нормы для данного вида работ'
        result = request.data

class LokoNumberSelectView(APIView):
    """Список типов секций в селект"""

    permission_classes = [permissions.IsAuthenticated]

    def get (self, request):
        if request.user.groups.filter(name="Admin"):           
            return Response('UPS')
        else:
            role=request.user.groups.all().values_list('id', flat=True)
            region = Region.objects.filter(role=role[0], element_type='section', section=None).values_list('id', flat=True)
            loko=Loko.objects.filter(element_type='element', region=region[0])
            serializer=LokoSelectSerializer(loko,many=True) 
            return Response(serializer.data)


class AreaSelectView(APIView):
    """Участок для селекта"""

    permission_classes = [permissions.IsAuthenticated]

    def get (self, request):        
        if request.user.groups.filter(name="Admin"):             
            return Response('UPS')
        else:
            role=request.user.groups.all().values_list('id', flat=True)
            region = Region.objects.filter(role=role[0], element_type ='section').exclude(section = None)                     
            serializer=RegionSerializer(region,many=True)
            return Response(serializer.data)

class StationSelectView(APIView):
    """Станция для селекта"""

    permission_classes = [permissions.IsAuthenticated]

    def get (self, request):        
        if request.user.groups.filter(name="Admin"):             
            return Response('UPS')
        else:
            role=request.user.groups.all().values_list('id', flat=True)            
            region = Region.objects.filter(role=role[0], element_type ='element')            
            serializer=RegionSerializer(region,many=True)           
            return Response(serializer.data)

class SettingsView(APIView):
    """Настройки"""

    def get (self,request): 
        if request.user.groups.filter(name="Admin"):             
            return Response('UPS')
        else:  
            role=request.user.groups.all().values_list('id', flat=True)            
            region = Region.objects.filter(role=role[0], element_type ='section', section = None)     
            settings=Settings.objects.filter(region = region[0]).values_list('settings', flat=True)
            try:
                return Response(settings[0])
            except:
                return Response(status = 400)



class ResultView(APIView):
    """Результаты работы""" 

    def get (self,request, slug):
        if request.user.groups.filter(name="Admin"):             
            return Response('UPS')
        else:
            role=request.user.groups.all().values_list('id', flat=True)            
            region = Region.objects.filter(role=role[0], element_type ='section', section = None)
            if slug == 'trail':
                resultTrail = Result_trail.objects.filter(region = region[0]).order_by('-id')[:5]
                result=ResultTrailListSerializer(resultTrail, many=True)
            else:
                resultManevr = Result_manevr.objects.filter(region = region[0]).order_by('-id')[:5]
                result=ResultManevrListSerializer(resultManevr, many=True)
            return Response(result.data)
    
    def post(self, request):
        role=request.user.groups.all().values_list('id', flat=True)
        user = User.objects.filter(username=request.user).values_list('id', flat=True)               
        region = Region.objects.filter(role=role[0], element_type ='section', section = None).values('id')
        message = 'Не возможно расчитать норму, проверьте заполненые данные и наличие нормы для данного вида работ'
        validateData = OperationValidate(request)
        if validateData==True:
            norm = NormaKhakasia(request)        
            key_norm = 'switch' in norm 
            if key_norm:
                return Response(norm['message']) 
            else: 
                typeLoko = Loko.objects.filter(id=norm['lokoNumber']).values('section')            
                norm['region'] = region[0]['id']
                norm['type_loko'] = typeLoko[0]['section']
                norm['user'] = user[0]            
                report = ReportKhakasia(request, user[0])            
                if norm.get('manevr') == True:
                    serializer=ResultManevrSerializer(data=norm)
                else:
                    serializer=ResultTrailSerializer(data=norm)
                ReportResult=ReportSerializer(data=report)            
                if serializer.is_valid() and ReportResult.is_valid():
                    serializer.save()  
                    ReportResult.save(id=report.get('id'))     
                    return Response('true', status=201)
                else:            
                    return Response(serializer.errors,status=400)
        else:            
            return Response(validateData)

class ResultTrailReport(APIView):
    """Вывод отчетов"""

    permission_classes = [permissions.IsAuthenticated]
    
         
    def post (self,request,slug):
        result = request.data         
        if slug == 'mm':
            report = Report.objects.filter(date=result['dateStart'])
            resultReport = ReportDataSerializer(report, many = True)        
            #trail = Result_trail.objects.filter(dateStart__gt = result['dateStart'], dateEnd__lt=result['dateEnd'])
            #manevr = Result_manevr.objects.filter(dateStart__gt = result['dateStart'], dateEnd__lt=result['dateEnd'])
            #resultTrail=ResultTrailListSerializer(trail, many=True)
            #resultManevr=ResultManevrListSerializer(manevr, many=True)
            #report={'vyvoz':resultTrail.data, 'manevr':resultManevr.data}
            return Response(resultReport.data)           
        elif slug == 'driver':
            report = Result_trail.objects.filter(dateStart__gt = result['dateStart'], dateEnd__lt=result['dateEnd'])
            resultReport=ResultTrailListSerializer(report, many=True)
        elif slug == 'date-now':
            #print(result['date'])
            dateEnd = result['date'] + 133200
            lokoList = Loko.objects.filter(name=result['lokoNumber']).values('id', 'section_id')
            lokoNumber = lokoList[0]['id']
            typeLoko = lokoList[0]['section_id']
            driver = Driver.objects.filter(name = result['driver']).values_list('id')
            report = Result_trail.objects.filter(dateStart__gt = result['date'], dateEnd__lt=dateEnd, lokoNumber = lokoNumber, type_loko = typeLoko, smena = result['smena'], driver = driver[0]).order_by('id')
            reportManevr = Result_manevr.objects.filter(dateStart__gt = result['date'], dateEnd__lt=dateEnd, lokoNumber = lokoNumber, type_loko = typeLoko, smena = result['smena'], driver = driver[0]).order_by('id')
            resultReport=ResultTrailListSerializer(report, many=True) 
            resultManevr=ResultManevrListSerializer(reportManevr, many=True)
            test={'vyvoz':resultReport.data, 'manevr':resultManevr.data}
            #return Response(typeLoko)           
            return Response(test) 
        return Response(resultReport.data)

class ReportID(APIView):
    """Вывод отчета по ID"""

    permission_classes = [permissions.IsAuthenticated]
    
    def get (self,request,pk):      
        report = Report.objects.get(id=pk)
        reportSerializer=ReportLokoSerializer(report)
        return Response(reportSerializer.data)
        
class ReportSlug(APIView):
    def post (self, request, slug):
        result = request.data
        if slug == 'date':
            date = time.strftime("%d %b %Y", time.localtime(result['dateStart']))
            date = int(time.mktime(time.strptime(date, '%d %b %Y'))) 
            report = Report.objects.filter(date = date, driver = result['driver'], smena = result['smena'])
            resultReport=ReportDataSerializer(report, many = True)
        elif slug == 'dateNow':
            date = time.strftime("%d %b %Y", time.localtime(result['dateStart']))
            date = int(time.mktime(time.strptime(date, '%d %b %Y')))
            report = Report.objects.filter(date__lt = date).order_by('-id')[:20]
            resultReport=ReportDataSerializer(report, many = True) 
        return Response(resultReport.data)

class ReportAll(APIView):

    def post(self, request):        
        result = request.data        
        report = Report.objects.filter(date__gte = result['dateStart'], date__lte=result['dateEnd'])
        key_exists = 'report' in result
        if key_exists:
            if result['report'] == 'reportDriver':
                resultReport = ReportDriverSerializer(report, many=True)
            elif result['report'] == 'reportTW':                
                resultReport = ReportTWSerializer(report, many=True)                             
        else:
            resultReport = ReportLokoSerializer(report, many=True)
        return Response(resultReport.data)

class ReportArea(APIView):
    """Отчет по участкам"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request): 
        if request.user.groups.filter(name="Admin"):             
            return Response('UPS')
        else:            
            role=request.user.groups.all().values_list('id', flat=True)            
            region = Region.objects.filter(role=role[0], element_type ='section', section = None)         
            result = request.data            
            if (result.get('text') == 'Vyvoz'):
                key_exists = 'stationDep' in result
                if key_exists:
                    norma = Norms.objects.filter(station_dep=result.get('stationDep'),station_arr=result.get('stationArr'),type_loko=result.get('lokoType'))                
                    if norma:
                        trailResult = Result_trail.objects.filter(dateStart__gte=result.get('dateStart'),dateEnd__lte=result.get('dateEnd'),
                                                                stationDep=result.get('stationDep'),stationArr=result.get('stationArr'),
                                                                type_loko=result.get('lokoType'), region=region[0], area=result.get('area')) 
                                          
                        serializerRes = ReportAreaSerializer(trailResult, many = True)
                        return Response(serializerRes.data)
                    else:
                        messages = [False, 'тут будет текст']
                        return Response(messages)
                else:
                    trailResult = Result_trail.objects.filter(dateStart__gte=result.get('dateStart'),dateEnd__lte=result.get('dateEnd'),region=region[0], area=result.get('area'))  
                    serializerRes = ReportAreaSerializer(trailResult, many = True)
                    return Response(serializerRes.data)
            elif (result.get('text') == 'Manevr'): 
                key_exists = 'station' in result
                if key_exists:
                    manevrResult = Result_manevr.objects.filter(dateStart__gte=result.get('dateStart'),dateEnd__lte=result.get('dateEnd'),
                                                                    station=result.get('station'), area=result.get('area'),
                                                                    type_loko=result.get('lokoType'), region=region[0])                     
                    serializerRes = ReportAreaManevrSerializer(manevrResult, many = True)                            
                    return Response(serializerRes.data)
                else:
                    manevrResult = Result_manevr.objects.filter(dateStart__gte=result.get('dateStart'),dateEnd__lte=result.get('dateEnd'),
                                                                    area=result.get('area'), region=region[0])                     
                    serializerRes = ReportAreaManevrSerializer(manevrResult, many = True)                            
                    return Response(serializerRes.data)


class MenuAll(APIView):
    """Вывод меню"""

    def get (self, request):
        if request.user.groups.filter(name="Admin"):             
            return Response('UPS')
        else:
            role = request.user.groups.all().values_list('id', flat = True)                       
            region = Region.objects.filter(role=role[0], element_type = 'section', section = None)           
            menu = Menu.objects.filter(role = role[0], region = region[0]).order_by('id') 
            result = MenuSerializer(menu, many = True)
            return Response(result.data)


class EditResult(APIView):
    """Изменение результатов"""

    def post (self, request, slug):
        result = request.data 
        key_exists = 'fact_manevr' in result      
        role=request.user.groups.all().values_list('id', flat=True)
        user = User.objects.filter(username=request.user).values_list('id', flat=True)               
        region = Region.objects.filter(role=role[0], element_type ='section', section = None).values('id')
        message = 'Не возможно расчитать норму, проверьте заполненые данные и наличие нормы для данного вида работ'
        section = Loko.objects.filter(name=result['lokoNumber']).values_list('id', flat=True)
        driver = Driver.objects.filter(name=result['driver']).values_list('id', flat=True)
        result['lokoNumber']=section[0]
        result['driver']=driver[0]        
        norm = NormaKhakasia(request, edit = True) 
        key_norm = 'switch' in norm 
        if key_norm:
            return Response(norm['message']) 
        else:
            typeLoko = Loko.objects.filter(id=norm['lokoNumber']).values('section')
            norm['type_loko'] = typeLoko[0]['section']
            if key_exists:
                manevr = Result_manevr.objects.filter(id=result['id']).values()
                norm['manevr'] = True
                diff = differenceReport(manevr, norm.copy())
                report = ReportKhakasia(diff, diff['user'])
                serializer=ResultManevrSerializer(data=norm)
                reportSerializer=ReportSerializer(data=report)                
            else:            
                trail = Result_trail.objects.filter(id=result['id']).values()            
                trailDiff = differenceReport(trail, norm.copy())
                report = ReportKhakasia(trailDiff, trailDiff['user'])            
                serializer=ResultTrailSerializer(data=norm)
                reportSerializer=ReportSerializer(data=report)            
            if serializer.is_valid() and reportSerializer.is_valid():
                serializer.save(id=norm.get('id'))  
                reportSerializer.save(id=report.get('id'))     
                return Response('true', status=201)
            else:            
                return Response(serializer.errors,status=400)

class DeleteOperation(APIView):
    """Удаление операции"""

    def post(self,request):
        result = request.data
        key_exists = 'dellAll' in result
        if key_exists:
            Report.objects.filter(id=result['id']).delete()
            manevr = result['manevr']
            trail = result['trail']
            if trail:            
                for t in trail:                  
                    Result_trail.objects.filter(id=t).delete()
            if manevr:            
                for m in manevr:                    
                    Result_manevr.objects.filter(id=m).delete()
            return Response('true', status=201)
        else: 
            if result['manevr_rabota']==True:
                delOper = Result_manevr.objects.filter(id=result['id'])
            else:
                delOper = Result_trail.objects.filter(id=result['id'])
            deleteMT=delOper.values()
            mtDiff=deleteOperation(deleteMT[0],result['manevr_rabota'])
            mtDiff['date']=result['date']
            if result['manevr_rabota']==True:
                mtDiff['manevr']=True
            report = ReportKhakasia(mtDiff,mtDiff['user_id'])
            reportSerializer=ReportSerializer(data=report)
            if reportSerializer.is_valid():             
                reportSerializer.save(id=result.get('id_report'))            
                delOper.delete()            
                return Response('true', status=201)
            else:            
                return Response(reportSerializer.errors,status=400)
            
        
class EditDriver(APIView):
    """Изменение машиниста в маршрутах"""

    def post (self, request):
        result = request.data
        if result['driver'] != None:        
            Report.objects.filter(id=result['id']).update(driver=result['driver'])
        if result['loko'] != None:
            Report.objects.filter(id=result['id']).update(lokoNumber=result['loko'])
        if result['date'] != None:
            Date_old=Report.objects.filter(id=result['id']).values_list('date', flat=True)
                       
            print(Date_old[0])
        manevr = result['manevr']
        trail = result['trail']
        if trail:            
            for t in trail:
                if result['driver'] != None:
                    Result_trail.objects.filter(id=t).update(driver=result['driver']) 
                if result['loko'] != None:
                    Result_trail.objects.filter(id=t).update(lokoNumber=result['loko']) 
                if result['date'] != None:
                    Date = Result_trail.objects.filter(id=t).values('dateStart', 'dateEnd')
                    date_raznica=result['date']-Date_old[0]
                    dateStart=Date[0]['dateStart']+date_raznica
                    dateEnd=Date[0]['dateEnd']+date_raznica
                    Result_trail.objects.filter(id=t).update(dateStart=dateStart,dateEnd=dateEnd) 
                    if not manevr:
                        Report.objects.filter(id=result['id']).update(date=result['date'])

        if manevr:            
            for m in manevr:
                if result['driver'] != None:
                    Result_manevr.objects.filter(id=m).update(driver=result['driver'])
                if result['loko'] != None:
                    Result_manevr.objects.filter(id=m).update(lokoNumber=result['loko'])
                if result['date'] != None:
                    Date = Result_manevr.objects.filter(id=m).values('dateStart', 'dateEnd')
                    date_raznica=result['date']-Date_old[0]
                    dateStart=Date[0]['dateStart']+date_raznica
                    dateEnd=Date[0]['dateEnd']+date_raznica
                    Result_manevr.objects.filter(id=m).update(dateStart=dateStart,dateEnd=dateEnd)
                    #print(test)
            Report.objects.filter(id=result['id']).update(date=result['date']) 

        return Response('true', status=201)


class ReportContent(APIView):
    """Отчеты для главной страницы"""
    def post(self, request,slug):
        decimal.getcontext().prec = 4
        result = request.data        
        resultReport=Report.objects.filter(date__lte=result['dateStart'], date__gte=result['dateEnd']).values()             
        if slug == 'driver':            
            driver=[]
            driverP=[]
            driverM=[]
            driverP_V=[]
            driverM_V=[]
            driverP_M=[]
            driverM_M=[]
            vyvoz=[],
            test = []
            otvet = {}            
            for val in resultReport: 
                driver.append(val['driver_id'])
            driver=set(driver)
            for val in driver:
                flag = False                
                for res in resultReport:
                    if len(test) == 0:                        
                        key={'driver':val, 'saving':0, 'trail':0, 'manevr':0}
                        test.append(key)                               
                    if val == res['driver_id']:                                              
                        key={'driver':res['driver_id'], 'saving':res['saving_result'], 'trail':res['saving_trail'], 'manevr':res['saving_manevr']}
                        for t in test:                           
                            if t['driver']==res['driver_id']:
                                t['saving']+=res['saving_result']                                                              
                                if res['saving_trail']==None:
                                    res['saving_trail']=0
                                t['trail']+=res['saving_trail']
                                if res['saving_manevr']==None:
                                    res['saving_manevr']=0
                                t['manevr']+=res['saving_manevr']
                                flag=True
                        if flag==False:
                            test.append(key)
            for val in test:
                name = Driver.objects.filter(id=val['driver']).values('name')
                val['driver']=name[0]['name']
                if val['saving'] < 0:
                    driverP.append(val)
                if val['saving'] > 0:
                    driverM.append(val)
                if val['trail'] < 0:
                    driverP_V.append(val)
                if val['trail'] > 0:
                    driverM_V.append(val)
                if val['manevr'] < 0:
                    driverP_M.append(val)
                if val['manevr'] > 0:
                    driverM_M.append(val)
            x = len(driverP)/len(driver)*100
            y = 100 - x
            vyvoz_bur = len(driverP_V)/len(driver)*100
            vyvoz_eco = 100 - vyvoz_bur
            manevr_bur = len(driverP_M)/len(driver)*100
            manevr_eco = 100 - manevr_bur
            otvet['economy']=driverM
            otvet['burnout']=driverP
            otvet['economy_v']=driverM_V
            otvet['burnout_v']=driverP_V
            otvet['economy_m']=driverM_M
            otvet['burnout_m']=driverP_M
            otvet['eco_proc']=y
            otvet['bur_proc']=x
            otvet['eco_vyvoz']=vyvoz_eco
            otvet['bur_vyvoz']=vyvoz_bur
            otvet['eco_manevr']=manevr_eco
            otvet['bur_manevr']=manevr_bur
            #print(otvet)            
        return Response(otvet, status=201)

class Permission(APIView):
    "Реализация некоторых доступов"

    def get(self, request,slug):       
        if slug == 'routesheet':
            role=request.user.groups.all().values_list('name', flat=True)
            for r in role:
                if r == 'Admin' or r == 'khakasia_instructor' or r == 'khakasia_operation':
                    mess=True
                else:
                    mess=False
        return Response(mess)
class User_header(APIView):
    "Вывод имени пользователя"

    def get(self, request):
        test=request.user.first_name
        return Response(test)

