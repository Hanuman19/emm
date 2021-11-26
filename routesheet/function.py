import decimal
from django.db.models.fields import NullBooleanField
from .models import Driver, Region, Loko, Norms, Result_trail, Report, Result_manevr
from decimal import Decimal, ROUND_HALF_UP
import time
from django.contrib.auth.models import User
from datetime import datetime, date


def functionRegion(request):  
    id_role=request.user.groups.values_list('id',flat=True)                 
    id_region=Region.objects.filter(role=id_role[0], section_id=None).values_list('id', flat=True)
    return id_region[0]

def functionDriver(request):
    id_role=request.user.groups.values_list('id',flat=True)  
    id_region=Region.objects.filter(role=id_role[0], section_id=None).values_list('id', flat=True)       
    request.data['region']=id_region[0]    
    return request.data

def functionLoko(request):    
    id_role=request.user.groups.values_list('id',flat=True)                   
    id_region=Region.objects.filter(role=id_role[0], section_id=None).values_list('id', flat=True)       
    id_numberLoko=Loko.objects.filter(name=request.data['section']).values_list('id', flat=True)  
    region=[]
    region.append(id_region[0])      
    request.data['region']=region
    request.data['section']=id_numberLoko[0]    
    return request.data 

def functionNorms(request):    
    if request.data.get('region')!=None:
        id_region=Region.objects.filter(name=request.data['region'][0]).values_list('id', flat=True)        
        request.data['region']=id_region[0]        
        return request.data
    return request.data


def NormaKhakasia(request, edit=False):
    """Расчет нормы для хакасии"""
    decimal.getcontext().prec = 4
    result = request.data 
    section = result['lokoNumber']
    typeLoko = Loko.objects.filter(id=section).values('section', 'name')
    typeLoko = typeLoko[0]
    lokoType = Loko.objects.filter(id=typeLoko['section']).values('name') 
    lokoType = lokoType[0] 
    key_exists = 'fact_manevr' in result
    if key_exists: #Расчет нормы намманевровую работу
        resultManevr = Result_manevr.objects.filter(dateStart=result['dateStart'], dateEnd=result['dateEnd'],
                                                    lokoNumber=result['lokoNumber']).values('id')
        if resultManevr and edit == False:
            message = {'switch': False, 'message':'Данная операция есть в базе данных'}
            return message
        else:
            if result['thrust'] == True:
                data = Norms.objects.filter(station = result['station']).values('coeff','distance')
                if data != None:           
                    norm = Decimal((data[0]['coeff'] * data[0]['distance'] * result['weight'])/1000)            
                    saving = Decimal(norm)-Decimal(result['fact_manevr'])                    
                    result['norm_manevr'] = Decimal(norm).quantize(Decimal("1.0"), ROUND_HALF_UP) 
                    result['saving_manevr'] = Decimal(saving).quantize(Decimal("1.0"), ROUND_HALF_UP)  
                    return(result)
                else:
                    message = {'switch': False, 'message':'Данной нормы не существует'} 
                    return message
            else:                
                if result['prostoy'] == True:
                    norma = Norms.objects.filter(station_dep=None,station_arr=None,type_loko=typeLoko['section']).values_list('norm_plain', flat=True)
                elif result['obrabotka'] == True:
                    norma = Norms.objects.filter(station_dep=None,station_arr=None,type_loko=typeLoko['section']).values_list('ov', flat=True)
                elif result['burning'] == True:
                    norma = Norms.objects.filter(station_dep=None,station_arr=None,type_loko=typeLoko['section']).values_list('burning', flat=True)
                else:
                    norma = Norms.objects.filter(station_dep=None,station_arr=None,type_loko=typeLoko['section']).values_list('norm_manevr', flat=True)
                if norma != None:
                    if result['equipment'] != 0:
                        norm = Decimal(result['fact_manevr'])
                    elif result['xx'] == True:
                        norm = Decimal(result['fact_manevr'])
                        #print(norm) 
                    else:                   
                        norm = norma[0] * result['work_time_manevr']
                    saving = Decimal(norm)-Decimal(result['fact_manevr'])  
                    #print(saving)                  
                    result['norm_manevr'] = Decimal(norm).quantize(Decimal("1.0"), ROUND_HALF_UP) 
                    result['saving_manevr'] = Decimal(saving).quantize(Decimal("1.0"), ROUND_HALF_UP)  
                    return(result)
                else:
                    message = {'switch': False, 'message':'Данной нормы не существует'} 
                    return message
    else: # Расчет нормы на вывозную работу
        if result['gp']==None or result['gp']=='':        
            gp=0
        else:
            gp=int(result['gp'])
        if result['pv']==None or result['pv']=='':        
            pv=0
        else:
            pv=int(result['pv'])    
        dateStart=result['dateStart']        
        stationDep=result['stationDep']
        stationArr=result['stationArr']
        date = time.strftime("%d %b %Y", time.localtime(dateStart))
        date=int(time.mktime(time.strptime(date, '%d %b %Y')))
        fact=result['fact']
        """Проверка наличая данной работы"""
        resultTrale = Result_trail.objects.filter(dateStart=result['dateStart'],dateEnd=result['dateEnd'],stationArr=stationArr,stationDep=stationDep,lokoNumber=result['lokoNumber']).values('id')            
        
        if resultTrale and edit == False:
            message = {'switch': False, 'message':'Данная операция есть в базе данных'} 
            return message
        else:
            if gp == 0 and pv == 0:
                normaReserv = Norms.objects.filter(station_dep=stationDep,station_arr=stationArr,type_loko=typeLoko['section']).values_list('norma_reserv', flat=True) 
                if normaReserv.exists():               
                    saving = normaReserv[0]-Decimal(fact)
                    result['norm'] = Decimal(normaReserv[0]).quantize(Decimal("1.0"), ROUND_HALF_UP)
                    result['saving'] = Decimal(saving).quantize(Decimal("1.0"), ROUND_HALF_UP)   
                    return result
                else:
                    message = {'switch': False, 'message':'Данной нормы не существует'} 
                    return message
            else:                            
                param = Norms.objects.filter(station_dep=stationDep,station_arr=stationArr,type_loko=typeLoko['section']).values('distance','coeff','norma_fix')            
                                                   
                if (param.exists() == False):
                    message = {'switch': False, 'message':'Данной нормы не существует'} 
                    return message                
                else:
                    param=param[0]  
                    if param['norma_fix'] == None:
                        try:
                            norma = Decimal(((gp*90 + pv*24) * param['distance'] * param['coeff'])/1000)
                            saving = Decimal(norma)-Decimal(fact)        
                            result['norm'] = Decimal(norma).quantize(Decimal("1.0"), ROUND_HALF_UP)
                            result['saving'] = Decimal(saving).quantize(Decimal("1.0"), ROUND_HALF_UP)
                        except TypeError:                            
                            message = {'switch': False, 'message':'Данной нормы не существует'} 
                            return message
                    if param['norma_fix'] != None:
                        norma = param['norma_fix']
                        saving = norma-fact
                        result['norm'] = Decimal(norma).quantize(Decimal("1.0"), ROUND_HALF_UP) 
                        result['saving'] = Decimal(saving).quantize(Decimal("1.0"), ROUND_HALF_UP)
                    if result['double'] == True:
                        doubleLoko=Loko.objects.filter(id=result['sectionDouble']).values_list('name', flat=True)
                        doubleLoko=doubleLoko[0]                                      
                        if result['sectionDouble'] == typeLoko['section']:
                            norma=norma/2
                        elif (lokoType['name'] =='ТЭМ7' or lokoType['name'] =='ТЭМ7(А)') and (doubleLoko=='ТЭМ7' or doubleLoko=='ТЭМ7(А)'):
                            norma=norma/2
                        elif (lokoType['name'] =='ТЭМ18' or lokoType['name'] =='ТЭМ2(18)') and (doubleLoko=='ТЭМ18' or doubleLoko=='ТЭМ2(18)'): 
                            norma=norma/2
                        elif (lokoType['name'] =='ТЭМ18' or lokoType['name'] =='ТЭМ2(18)') and (doubleLoko=='ТЭМ7' or doubleLoko=='ТЭМ7(А)'):
                            norma = Decimal(norma) * Decimal(0.3)
                        elif (lokoType['name'] =='ТЭМ7' or lokoType['name'] =='ТЭМ7(А)') and (doubleLoko=='ТЭМ18' or doubleLoko=='ТЭМ2(18)'):
                            norma = Decimal(norma) * Decimal(0.7)
                        saving = norma-fact
                        result['norm'] = Decimal(norma).quantize(Decimal("1.0"), ROUND_HALF_UP) 
                        result['saving'] = Decimal(saving).quantize(Decimal("1.0"), ROUND_HALF_UP)                         
                    return result

def NormValidate(request):
    norma = request.data    
    if norma['type_work']=='vyvoz':
        if norma['id'] == None:
            result = Norms.objects.filter(type_loko=norma['type_loko'],station_arr=norma['station_arr'],station_dep=norma['station_dep']).count()            
            if result != 0:
                message = 'Данная норма существует'                
                return message
            else:
                message = True               
                return message
        else:
            message = True            
            return message
    elif norma['type_work']=='manevr':
        if norma['id'] == None:
            result = Norms.objects.filter(type_loko=norma['type_loko'],region=norma['region'],station_arr=None,station_dep=None).count()            
            if result != 0:
                message = 'Нельзя добавить нормы, измените текущюю'                
                return message
            else:
                message = True               
                return message
        else:
            message = True            
            return message
    else:
        message = 'Не определенный вид работ'
        return message


def ReportKhakasia(request, user):
    """Запись результатов"""     
    decimal.getcontext().prec = 4
    try:
        result = request.data.copy()
    except AttributeError:
        result = request          

    #date = time.strftime("%d %b %Y", time.localtime(result['dateStart']))
    #date=int(time.mktime(time.strptime(date, '%d %b %Y'))) 
    #date_end=date+86400 
    print(result['date']) 
    date=result['date']
    if result['gp']==None or result['gp']=='':        
        gp=0
    else:
        gp=int(result['gp'])
    if result['pv']==None or result['pv']=='':        
        pv=0
    else:
        pv=int(result['pv'])
    key_driver = 'driver' in result
    if key_driver:
        report=Report.objects.filter(date=date, smena=result['smena'], driver=result['driver'], lokoNumber=result['lokoNumber']).values()           
    else:
        report=Report.objects.filter(date=date, smena=result['smena'], driver=result['driver_id'], lokoNumber=result['lokoNumber_id']).values()
    if report:
        report=report[0]
        for i in report:
            if report[i] == None: 
                report[i] = 0                         
        for i in result:
            if result[i] == None: 
                result[i] = 0 
        key_exists = 'manevr' in result
        key_bortStart = 'dtBortStart' in result
        if key_exists:
            #print(result['dtEndManevr']) 
            if result['prostoy'] == True: 
                report['work_time_prostoy']+=result['work_time_manevr']
            else:                      
                report['work_time_manevr']+=result['work_time_manevr']
            report['fact_manevr']+=result['fact_manevr']
            report['norm_manevr']+=result['norm_manevr']
            report['saving_manevr']+=result['saving_manevr'] 
            report['norm_result']+=result['norm_manevr']
            if result['bort'] == True:
                print(result['bort'])
                #print(result['dtEnd'])
                print(result)
                if result['dtBortStart']==0 or result['dtBortStart']==None:
                    report['fact_result']=report['dtStart']-int(result['dtBortEnd'])               
                    report['dtEnd']=result['dtBortEnd']
                else:
                    report['fact_result']=report['dtStart']-report['dtEnd']
            else:
                report['fact_result']+=result['fact_manevr']
                report['dtEnd']=result['dtEndManevr']
            report['saving_result']=report['norm_result']-report['fact_result']
            report['lokoNumber']=report['lokoNumber_id']
            report['region']=report['region_id']
            report['typeLoko']=report['typeLoko_id']
            report['driver']=report['driver_id']
            report['area']=report['area_id']
            report['user']=report['user_id']
            report['dateEnd']=result['dateEnd']
            
        else:                      
            report['gp']+=gp
            report['pv']+=pv
            report['work_time_trail']+=result['work_time']
            report['fact_trail']+=result['fact']
            report['norm_trail']+=result['norm']
            report['saving_trail']+=result['saving']            
            report['norm_result']+=result['norm']
            if result['bort'] == True:
                report['fact_result']=report['dtStart']-int(result['dtBortEnd'])
                report['dtEnd']=result['dtBortEnd']
            else:
                report['fact_result']+=result['fact']
                report['dtEnd']=result['dt_end']
            report['saving_result']=report['norm_result']-report['fact_result'] 
            report['lokoNumber']=report['lokoNumber_id']
            report['region']=report['region_id']
            report['typeLoko']=report['typeLoko_id']
            report['driver']=report['driver_id']
            report['area']=report['area_id']
            report['user']=report['user_id']
            report['dateEnd']=result['dateEnd']                  
        return report
    else:
        typeLoko=Loko.objects.filter(id=result['lokoNumber']).values_list('section', flat=True)  
        region = Region.objects.filter(id=result['area']).values_list('section', flat=True)
        key_exists = 'manevr' in result
        if key_exists: 
            if result['prostoy'] == True:
                report = {'work_time_prostoy':result['work_time_manevr']}  
            else:
                report ={'work_time_manevr':result['work_time_manevr']} 
            if result['bort'] == True:
                fact = int(result['dtBortStart']) - int(result['dtBortEnd']) + int(result['equipment'])
                saving = result['norm_manevr'] - fact
                report.update({'saving_result':saving,'fact_result':fact,'dtStart':result['dtBortStart'], 'dtEnd':result['dtBortEnd']})
            else:
                report.update({'saving_result':result['saving_manevr'],'fact_result':result['fact_manevr'],'dtStart':result['dtStartManevr'], 'dtEnd':result['dtEndManevr']})    
            report.update({'date':date,'fact_manevr':result['fact_manevr'],
                   'norm_manevr':result['norm_manevr'],'saving_manevr':result['saving_manevr'],
                   'norm_result':result['norm_manevr'], 'smena':result['smena'], 
                   'lokoNumber':result['lokoNumber'],'region':region[0],'typeLoko':typeLoko[0], 'driver':result['driver'],'area':result['area'], 'user':user, 
                   'smenaStart':result['dateStart'], 'smenaEnd':result['dateEnd'], 'bort':result['bort']}) 
        else: 
            if result['bort'] == True:
                fact = result['dt_start'] - result['dt_end']
                saving = result['norm'] - fact
                report={'fact_result':fact,'saving_result':result['saving'],'dtStart':result['dtBortStart'], 'dtEnd':result['dtBortEnd']}
            else:
                report={'fact_result':result['fact'],'saving_result':result['saving'],'dtStart':result['dt_start'], 'dtEnd':result['dt_end']}      
            report.update({'date':date,'gp':result['gp'],'pv':result['pv'],'work_time_trail':result['work_time'],'fact_trail':result['fact'],
                   'norm_trail':result['norm'],'saving_trail':result['saving'],
                   'norm_result':result['norm'], 'smena':result['smena'], 
                   'lokoNumber':result['lokoNumber'],'region':region[0],'typeLoko':typeLoko[0], 'driver':result['driver'],'area':result['area'], 'user':user,
                   'smenaStart':result['dateStart'], 'smenaEnd':result['dateEnd'],'dtStart':result['dt_start'], 'dtEnd':result['dt_end'], 'bort':result['bort']})
        return report
      
def differenceReport (tm, norm):    
    """Разница после редактирования"""  
    #print(tm)
    key_exists = 'fact_manevr' in tm[0]   
    #norm['weight']=tm['weight']
    #norm['gp']=norm['gp']-tm['gp']
    norm['pv'] -= tm[0]['pv']
    if key_exists:
        norm['dtStartManevr'] -= tm[0]['dtStartManevr']
        norm['dtEndManevr'] -= tm[0]['dtEndManevr']
        norm['work_time_manevr'] -= tm[0]['work_time_manevr']
        norm['fact_manevr'] -= tm[0]['fact_manevr']
        norm['norm_manevr'] -= tm[0]['norm_manevr']
        norm['saving_manevr'] -= tm[0]['saving_manevr']
        #if tm[0]['bort'] == True:

    else:
        norm['gp']=norm['gp']-tm[0]['gp']
        norm['dt_start'] -= tm[0]['dt_start']
        norm['dt_end'] -= tm[0]['dt_end']
        norm['work_time'] -= tm[0]['work_time']
        norm['fact'] -= tm[0]['fact']
        norm['norm'] -= tm[0]['norm']
        norm['saving'] -= tm[0]['saving']
    return norm   

def deleteOperation(delete, manevr):
    """Разница после удаления""" 
    if manevr == True:
        delete['work_time_manevr'] = delete['work_time_manevr'] * (-1)
        delete['fact_manevr'] = delete['fact_manevr'] * (-1)
        delete['norm_manevr'] = delete['norm_manevr'] * (-1)
        delete['saving_manevr'] = delete['saving_manevr'] * (-1)
        delete['gp'] = delete['gp'] * (-1)
        delete['pv'] = delete['pv'] * (-1)
    else:
        delete['work_time'] = delete['work_time'] * (-1)
        delete['fact'] = delete['fact'] * (-1)
        delete['norm'] = delete['norm'] * (-1)
        delete['saving'] = delete['saving'] * (-1)
        delete['gp'] = delete['gp'] * (-1)
        delete['pv'] = delete['pv'] * (-1)
    #print(delete)
    return delete


def OperationValidate(request):
    """Проверки ввода операции"""
    data = request.data    
    Smena = Report.objects.filter(date=data['date'],lokoNumber=data['lokoNumber'], smena=data['smena']).values('driver_id','work_time_trail','work_time_manevr','work_time_prostoy')
    lokoNumber = Loko.objects.filter(id = data['lokoNumber']).values_list('name', flat=True)    
    if Smena.exists():
         Result = Smena[0]
         driver = Driver.objects.filter(id=Result['driver_id']).values_list('name', flat=True) 
         if data['driver'] == Result['driver_id']:
            driverAccess =  True
            if Result['work_time_trail'] == None:
                Result['work_time_trail']=0                 
            if Result['work_time_manevr'] == None:
                Result['work_time_manevr']=0
            if Result['work_time_prostoy'] == None:
                Result['work_time_prostoy']=0 
            timeFull=Result['work_time_trail']+Result['work_time_manevr']+Result['work_time_prostoy']            
            driverAccess =  True
            messageOper='Проверьте правильность заполнения данных, время работы получается больше 13 часов, проверьте прошлые внесенные данные, время работ'
            if 'work_time_manevr' in data:
                if (timeFull + data['work_time_manevr'])>800:
                    return messageOper
                else:
                    operationAccess = True 
                    print(operationAccess)           
            elif 'work_time' in data:
                if (timeFull + data['work_time'])>800:
                    return messageOper
                else:
                    operationAccess = True
                    print(operationAccess)
            if  operationAccess == True and  driverAccess==True:
                return True 
         else:            
            if data['smena_driver']==True:                
                operationAccess = True
                return True
            else:          
                message='Проверьте правильность заполнения данных, {0} смена {1} на локомотиве № {2} работал машинист {3}'.format(datetime.fromtimestamp(data['date']).date().strftime("%d.%m.%Y"), data['smena'],lokoNumber[0], driver[0])
                return message
    else:
        return True

    