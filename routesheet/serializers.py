from django.db import models
from django.db.models import fields
from rest_framework import serializers

from .models import Driver, Loko, Norms, Region, Settings, Result_trail, Report, Result_manevr, Menu


class DriverListSerializer(serializers.ModelSerializer):
    """ Список машинистов """

    area = serializers.SlugRelatedField(slug_field="name", read_only=True)
    region = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Driver
        fields = "__all__"

class DriverCreateSerializer(serializers.ModelSerializer):
    """Добавление локомотивов"""    
    
    class Meta:
        model = Driver
        fields = "__all__"

    def create(self, validated_data):      
        driver = Driver.objects.update_or_create(
            id = validated_data.get('id', None),                       
            defaults={
                'name': validated_data.get("name"),
                'area': validated_data.get('area'),
                'region': validated_data.get('region')            
            }
        )                 
        return driver

class FilterLokoListSerializer(serializers.ListSerializer):
    """Фильтр локомотивов, только parents"""

    def to_representation(self, data):
        data = data.exclude(section = None)        
        return super().to_representation(data)


class LokoListSerializer(serializers.ModelSerializer):
    """ Список локомотивов"""
    
    region = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    section = serializers.SlugRelatedField(slug_field="name", read_only=True)
    
    

    class Meta:
        list_serializer_class = FilterLokoListSerializer
        model = Loko
        fields = ("id", "name", "region", "section", "active")


class LokoCreateSerializer(serializers.ModelSerializer):
    """Добавление локомотивов"""    
    
    class Meta:
        model = Loko
        fields = "__all__"


    def create(self, validated_data):      
        loko = Loko.objects.update_or_create(
            id = validated_data.get('id', None),                       
            defaults={'element_type': validated_data.get("element_type"),
                        'section': validated_data.get("section"),
                        'name': validated_data.get("name"),           
            }
        )                 
        return loko

class NormListSerializer(serializers.ModelSerializer):
    """Список норм"""
    
    region = serializers.SlugRelatedField(slug_field="name", read_only=True)
    area = serializers.SlugRelatedField(slug_field="name", read_only=True)
    station = serializers.SlugRelatedField(slug_field="name", read_only=True)
    station_arr = serializers.SlugRelatedField(slug_field="name", read_only=True)
    station_dep = serializers.SlugRelatedField(slug_field="name", read_only=True)
    type_loko=serializers.SlugRelatedField(slug_field="name", read_only=True)
    
    class Meta:
        model = Norms
        fields = "__all__"

class NormCreateSerializer(serializers.ModelSerializer):
    """Добавление и обновление норм"""

    class Meta:
        model = Norms
        fields = "__all__"

    def create(self, validated_data):      
        norm = Norms.objects.update_or_create(
            id = validated_data.get('id', None),                       
            defaults={
                        'type_work':validated_data.get("type_work"),
                        'station_dep':validated_data.get("station_dep"),
                        'station_arr':validated_data.get("station_arr"),
                        'norma_reserv':validated_data.get("norma_reserv"),
                        'norma_fix':validated_data.get("norma_fix"),
                        'type_loko':validated_data.get("type_loko"),
                        'distance':validated_data.get("distance"),
                        'coeff':validated_data.get("coeff"),
                        'region':validated_data.get("region"),
                        'area':validated_data.get("area"),                        
                        'norm_manevr':validated_data.get("norm_manevr"),
                        'norm_plain':validated_data.get("norm_plain"),                       
                        'ov':validated_data.get("ov"),
                    }            
        )
        return norm


class RegionSerializer(serializers.ModelSerializer):
    """Сериализация списка регионов, станций и участков для селекта"""   
    
    section = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:  
        model = Region
        fields = ("id", "name", "section")

class LokoSelectSerializer(serializers.ModelSerializer):
    """Сериализация списка типов и номеров секций для селекта"""   
    
    class Meta:
        model = Loko
        fields = ("id", "name")


class DriverSelectSerializer(serializers.ModelSerializer):
    """Сериализация списка машинистов для селекта"""   
    
    class Meta:
        model = Driver
        fields = ("id", "name") 

class ResultTrailSerializer(serializers.ModelSerializer):
    """Сериализация вывозной работы, результаты"""         

    class Meta:
        model = Result_trail
        fields = "__all__"

    def create(self, validated_data):      
        result = Result_trail.objects.update_or_create(
            id = validated_data.get('id'),                       
            defaults = {  
                        'area':validated_data.get('area'),                        
                        'double':validated_data.get('double'),
                        'sectionDouble':validated_data.get('sectionDouble'),
                        'stationDep':validated_data.get("stationDep"),
                        'stationArr':validated_data.get("stationArr"),
                        'weight':validated_data.get("weight"),
                        'gp':validated_data.get("gp"),
                        'pv':validated_data.get("pv"),
                        'work_time':validated_data.get("work_time"),
                        'dt_start':validated_data.get('dt_start'),
                        'dt_end':validated_data.get('dt_end'),
                        'fact':validated_data.get("fact"),                        
                        'norm':validated_data.get("norm"),
                        'saving':validated_data.get("saving"),                        
                        'lokoNumber':validated_data.get("lokoNumber"),
                        'type_loko':validated_data.get('type_loko'),
                        'dateStart':validated_data.get('dateStart'),
                        'smena':validated_data.get('smena'),
                        'dateEnd':validated_data.get('dateEnd'),
                        'user':validated_data.get('user'),
                        'driver':validated_data.get('driver'),                        
                        'region':validated_data.get('region')                        
                    }            
        )
        return result



class ResultManevrSerializer(serializers.ModelSerializer):
    """Сериализация маневровой работы, результаты"""         

    class Meta:
        model = Result_manevr
        fields = "__all__"

    def create(self, validated_data):      
        result = Result_manevr.objects.update_or_create(
            id = validated_data.get('id'),                       
            defaults = {  
                        'area':validated_data.get('area'),  
                        'station':validated_data.get("station"),                        
                        'gp':validated_data.get("gp"),
                        'pv':validated_data.get("pv"),
                        'work_time_manevr':validated_data.get("work_time_manevr"),
                        'dtStartManevr':validated_data.get('dtStartManevr'),
                        'dtEndManevr':validated_data.get('dtEndManevr'),
                        'fact_manevr':validated_data.get("fact_manevr"),                        
                        'norm_manevr':validated_data.get("norm_manevr"),
                        'saving_manevr':validated_data.get("saving_manevr"),                        
                        'lokoNumber':validated_data.get("lokoNumber"),
                        'type_loko':validated_data.get('type_loko'),
                        'dateStart':validated_data.get('dateStart'),
                        'smena':validated_data.get('smena'),
                        'dateEnd':validated_data.get('dateEnd'),
                        'user':validated_data.get('user'),
                        'driver':validated_data.get('driver'),
                        'obduv':validated_data.get('obduv'),
                        'obrabotka':validated_data.get('obrabotka'),
                        'prostoy':validated_data.get('prostoy'),
                        'thrust':validated_data.get('thrust'), 
                        'equipment':validated_data.get('equipment'),
                        'region':validated_data.get('region'),
                        'xx':validated_data.get('xx'),
                        'burning':validated_data.get('burning'),
                        'bort':validated_data.get('bort')
                    }            
        )
        return result

class ResultTrailListSerializer(serializers.ModelSerializer):
    """Вывод просчитанных норм вывозной работы"""

    region = serializers.SlugRelatedField(slug_field="name", read_only=True)    
    stationArr = serializers.SlugRelatedField(slug_field="name", read_only=True)
    stationDep = serializers.SlugRelatedField(slug_field="name", read_only=True)
    driver = serializers.SlugRelatedField(slug_field="name", read_only=True) 
    lokoNumber = serializers.SlugRelatedField(slug_field="name", read_only=True) 
    numberDouble = serializers.SlugRelatedField(slug_field="name", read_only=True) 
    sectionDouble = serializers.SlugRelatedField(slug_field="name", read_only=True)
    type_loko = serializers.SlugRelatedField(slug_field="name", read_only=True) 
    
    class Meta:
        model = Result_trail
        fields = "__all__"


class ResultManevrListSerializer(serializers.ModelSerializer):
    """Вывод просчитанных норм маневровой работы"""

    region = serializers.SlugRelatedField(slug_field="name", read_only=True)    
    station = serializers.SlugRelatedField(slug_field="name", read_only=True)    
    driver = serializers.SlugRelatedField(slug_field="name", read_only=True) 
    lokoNumber = serializers.SlugRelatedField(slug_field="name", read_only=True) 
    
    class Meta:
        model = Result_manevr
        fields = "__all__"

class ReportDriverSerializer(serializers.ModelSerializer):
    """Отчет по машинистам"""

    driver = serializers.SlugRelatedField(slug_field="name", read_only=True)
    lokoNumber = serializers.SlugRelatedField(slug_field="name", read_only=True) 

    class Meta:
        model = Report
        fields = "__all__"

class ReportLokoSerializer(serializers.ModelSerializer):
    """Сериализация для отчетов локомотивы"""

    typeLoko = serializers.SlugRelatedField(slug_field="name", read_only=True)
    lokoNumber = serializers.SlugRelatedField(slug_field="name", read_only=True)
    driver = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Report
        fields = "__all__"

class ReportTWSerializer(serializers.ModelSerializer):
    """Сериализация для отчетов локомотивы"""

    typeLoko = serializers.SlugRelatedField(slug_field="name", read_only=True)
    lokoNumber = serializers.SlugRelatedField(slug_field="name", read_only=True)
    area = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Report
        fields = ('area' ,'typeLoko', 'lokoNumber','work_time_trail','work_time_manevr', 'work_time_prostoy', 'date', 'smena')

class ReportSerializer(serializers.ModelSerializer):
    """Добавление и обновление отчетов"""

    #driver = serializers.SlugRelatedField(slug_field="name", read_only=True)
    #area = serializers.SlugRelatedField(slug_field="name", read_only=True)
    #typeLoko = serializers.SlugRelatedField(slug_field="name", read_only=True)
    #lokoNumber = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Report
        fields = "__all__"

    def create(self, validated_data):      
        report = Report.objects.update_or_create(
            id = validated_data.get('id'),                       
            defaults = {  
                        'smena':validated_data.get("smena"),
                        'driver':validated_data.get("driver"),
                        'date':validated_data.get("date"),
                        'weight':validated_data.get("weight"),
                        'gp':validated_data.get("gp"),
                        'pv':validated_data.get("pv"),
                        'work_time_trail':validated_data.get("work_time_trail"),
                        'fact_trail':validated_data.get("fact_trail"),
                        'norm_trail':validated_data.get("norm_trail"),
                        'saving_trail':validated_data.get("saving_trail"),
                        'work_time_manevr':validated_data.get("work_time_manevr"),
                        'fact_manevr':validated_data.get("fact_manevr"),
                        'norm_manevr':validated_data.get("norm_manevr"),
                        'saving_manevr':validated_data.get("saving_manevr"),
                        'fact_result':validated_data.get("fact_result"),
                        'norm_result':validated_data.get("norm_result"),
                        'saving_result':validated_data.get("saving_result"),
                        'smenaStart':validated_data.get("smenaStart"),
                        'smenaEnd':validated_data.get("smenaEnd"),
                        'region':validated_data.get("region"),
                        'lokoNumber':validated_data.get("lokoNumber"),
                        'typeLoko':validated_data.get("typeLoko"),
                        'area':validated_data.get("area"),
                        'user':validated_data.get("user"),
                        'work_time_prostoy':validated_data.get("work_time_prostoy"),
                        'dtStart':validated_data.get("dtStart"),
                        'dtEnd':validated_data.get("dtEnd"),                        
                    }            
        )
        return report

class MenuSerializer(serializers.ModelSerializer):
    """Сериализация меню"""

    class Meta:
        model = Menu
        fields = "__all__"

class ReportAreaSerializer(serializers.ModelSerializer):
    """Сериализация для отчета по участкам"""
    
    stationDep = serializers.SlugRelatedField(slug_field="name", read_only=True)
    stationArr = serializers.SlugRelatedField(slug_field="name", read_only=True)
    driver = serializers.SlugRelatedField(slug_field="name", read_only=True)
    type_loko = serializers.SlugRelatedField(slug_field="name", read_only=True)
    lokoNumber = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Result_trail
        fields = "__all__"

class ReportAreaManevrSerializer(serializers.ModelSerializer):
    """Сериализация для отчета по участкам маневровой работы"""    
    
    station = serializers.SlugRelatedField(slug_field="name", read_only=True)
    driver = serializers.SlugRelatedField(slug_field="name", read_only=True)
    type_loko = serializers.SlugRelatedField(slug_field="name", read_only=True)
    lokoNumber = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Result_manevr
        fields = "__all__"

class ReportDataSerializer(serializers.ModelSerializer):
    """Сериализация для вывода отчета на странице ввода"""

    driver = serializers.SlugRelatedField(slug_field="name", read_only=True)
    lokoNumber = serializers.SlugRelatedField(slug_field="name", read_only=True)

    class Meta:
        model = Report
        fields = ('id' ,'date', 'driver', 'smena', 'lokoNumber')

