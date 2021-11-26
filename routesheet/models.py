from django.db import models
from django.contrib.auth.models import Group, User


class Region(models.Model):
    """Регионы-участки-станции"""

    SECTION= 'section'
    ELEMENT = 'element'

    REGION_TYPES = (        
        (SECTION, 'родитель'),
        (ELEMENT, 'элемент')
    )

    name=models.CharField("Название",max_length=100)
    element_type=models.CharField("Тип элемента", max_length=50, choices=REGION_TYPES)
    section=models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name="Родитель", blank=True, null=True, default=0, related_name="Area")
    role = models.ManyToManyField(Group, verbose_name="роли")
    date_start=models.IntegerField("Дата создания",blank=True, null=True)
    date_update=models.IntegerField("Дата обновления",blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Регион-участок-станция"
        verbose_name_plural = "Регионы-участки-станции"

class Loko(models.Model):
    """Тип и номер локомотивов"""
    SECTION= 'section'
    ELEMENT = 'element'

    LOKO_TYPES = (        
        (SECTION, 'родитель'),
        (ELEMENT, 'элемент')
    )
    name=models.CharField("Название",max_length=100)
    element_type=models.CharField("Тип элемента", max_length=50, choices=LOKO_TYPES)
    section=models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name="Родитель", blank=True, null=True, related_name="children")
    date_start=models.IntegerField("Дата создания",blank=True, null=True)
    date_update=models.IntegerField("Дата обновления",blank=True, null=True)
    region=models.ManyToManyField(Region, verbose_name="Регион",related_name="loko_region")
    active=models.BooleanField("Активен",null=True, default=True)

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = "Локомотив"
        verbose_name_plural = "Локомотивы"


class Driver(models.Model):
    #Машинисты
    name=models.CharField("ФИО",max_length=150)    
    area=models.ForeignKey(Region, on_delete=models.SET_NULL, verbose_name="Участок", blank=True, null=True, related_name="driver_area")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, verbose_name="Регион", blank=True, null=True, related_name="driver_region")
    active=models.BooleanField("Активен",null=True, default=True)
    tabel=models.IntegerField("Табельный номер",null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Машинист"
        verbose_name_plural = "Машинисты"

class Mileage(models.Model):
    """Пробеги"""

    mileage = models.IntegerField("Пробег")
    number_loko = models.ForeignKey(Loko, verbose_name="№ локомотива", on_delete=models.CASCADE)   

    class Meta:
        verbose_name = "Пробег"
        verbose_name_plural = "Пробеги"



class Equipment(models.Model):
    """Экипировки"""

    equi_dt = models.IntegerField("Экипировка ДТ", blank=True, null=True)
    equi_oil = models.IntegerField("Экипировка маслом",blank=True, null=True )
    number_loko = models.ForeignKey(Loko,verbose_name="№ локомотива", on_delete=models.SET_NULL, blank=True, null=True)
    date = models.IntegerField("Дата экипировки")
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, verbose_name="Регион", blank=True, null=True)

    def __str__(self):
        return self.equi_dt

class Norms(models.Model):
    """Нормы"""

    VYVOZ= 'vyvoz'
    MANEVR = 'manevr'

    WORK_TYPES = (        
        (VYVOZ, 'Вывозная работа'),
        (MANEVR, 'Маневровая работа')
    )
    type_work=models.CharField("Вид работы", max_length=50, choices=WORK_TYPES, default=MANEVR)
    station_dep=models.ForeignKey(Region, on_delete=models.SET_NULL, verbose_name="Станция отправления",blank=True, null=True, related_name="station_depp")
    station_arr=models.ForeignKey(Region, on_delete=models.SET_NULL, verbose_name="Станция прибытия",blank=True, null=True, related_name="station_arr")
    norma_reserv=models.DecimalField("Норма резервом", max_digits=6, decimal_places=3, blank=True, null=True)
    norma_fix=models.DecimalField("Фиксированная норма", max_digits=6, decimal_places=3, blank=True, null=True)
    type_loko = models.ForeignKey(Loko,verbose_name="Тип локомотива", on_delete=models.CASCADE)
    distance=models.DecimalField("Дистанция", max_digits=6, decimal_places=3, blank=True, null=True)
    coeff=models.DecimalField("Коэффициент удельного расхода", max_digits=6, decimal_places=3, blank=True, null=True)
    region=models.ForeignKey(Region, on_delete=models.SET_NULL, verbose_name="Регион", related_name="region", null=True)
    area=models.ForeignKey(Region, on_delete=models.SET_NULL, verbose_name="Участок", related_name="area",blank=True, null=True)
    station=models.ForeignKey(Region, on_delete=models.SET_NULL, verbose_name="Станция", blank=True, null=True, related_name="station")
    norm_manevr=models.DecimalField("Норма маневров", max_digits=6, decimal_places=3, blank=True, null=True)
    norm_plain=models.DecimalField("Норма простоев", max_digits=6, decimal_places=3, blank=True, null=True)
    double_in_tail=models.BooleanField("С толкачем", blank=True, null=True)
    no_double=models.BooleanField("Без толкача", blank=True, null=True)
    double_in_head=models.BooleanField("Толкач", blank=True, null=True)
    ov=models.DecimalField("Обработка состава", max_digits=6, decimal_places=3, blank=True, null=True)
    burning = models.DecimalField("Прожиг", max_digits=6, decimal_places=3, blank=True, null=True)
    
    

    class Meta:
        verbose_name = "Норма"
        verbose_name_plural = "Нормы"


class Result_manevr(models.Model):
    """Результаты маневровой работы"""

    
    driver=models.ForeignKey(Driver,on_delete=models.CASCADE, verbose_name="Машинист", default=0)
    dateStart=models.IntegerField("Время начала", blank=True, null=True)
    dateEnd=models.IntegerField("Время окончания")
    smena=models.IntegerField("смена")
    dtStartManevr=models.IntegerField("Дт на начало операции")
    dtEndManevr=models.IntegerField("Дт на конец операции")
    work_time_manevr=models.IntegerField("Общее время работы")
    fact_manevr=models.IntegerField("Фактический расход ДТ")
    norm_manevr=models.DecimalField("Нормированный расход ДТ",max_digits=6, decimal_places=1, null=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, verbose_name="Регион", blank=True, null=True)
    saving_manevr = models.DecimalField("Экономия",max_digits=6, decimal_places=1, null=True)
    obduv = models.BooleanField("Обдув вагонов", blank=True, null=True)
    obrabotka = models.BooleanField("Обработка вагонов", blank=True, null=True)
    prostoy = models.BooleanField("Простой", blank=True, null=True)
    thrust = models.BooleanField("Вытяжка", blank=True, null=True)    
    equipment = models.IntegerField("Экипировка", blank=True, null=True)
    lokoNumber=models.ForeignKey(Loko,on_delete=models.CASCADE, verbose_name="№ секции")
    station=models.ForeignKey(Region,on_delete=models.CASCADE, verbose_name="Станция", related_name="stationManevr")
    area=models.ForeignKey(Region,on_delete=models.CASCADE, verbose_name="Участок", related_name="areaManevr")
    type_loko = models.ForeignKey(Loko, on_delete = models.CASCADE, verbose_name = "Тип секции", related_name="type_loko_manevr")
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Имя пользователя", related_name="user_manevr")
    gp = models.IntegerField("Груженные вагоны", blank=True, null=True, default=0)
    pv = models.IntegerField("Порожние вагоны", blank=True, null=True, default=0)
    xx = models.BooleanField("Холодный простой", blank=True, null=True)
    burning = models.BooleanField("Прожиг", blank=True, null=True)
    bort = models.BooleanField("Борт не работает",blank=True, null=True, default=False)

    class Meta:
        verbose_name = "Маневровая работа"
        verbose_name_plural = "Маневровые работы"



class Result_trail(models.Model):
    """Результаты вывозной работы"""

    stationDep=models.ForeignKey(Region,on_delete=models.CASCADE, verbose_name="Станция отправления", related_name="stationDep")
    stationArr=models.ForeignKey(Region,on_delete=models.CASCADE, verbose_name="Станция прибытия", related_name="stationArr")    
    driver=models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name="Машинист", default=0)
    lokoNumber=models.ForeignKey(Loko,on_delete=models.CASCADE, verbose_name="№ секции")
    type_loko = models.ForeignKey(Loko, on_delete = models.CASCADE, verbose_name = "Тип секции", related_name="type_loko")
    dateStart=models.IntegerField("Время начала")
    dateEnd=models.IntegerField("Время окончания")
    smena=models.IntegerField("смена")
    weight=models.IntegerField("Весс поезда", blank=True, null=True, default=0)
    gp=models.IntegerField("Груженные вагоны", blank=True, null=True, default=0)
    pv=models.IntegerField("Порожние вагоны", blank=True, null=True, default=0)
    dt_start=models.IntegerField("Дт на начало операции")
    dt_end=models.IntegerField("Дт на конец операции")
    work_time=models.IntegerField("Общее время работы")
    fact=models.IntegerField("Фактический расход ДТ")
    norm=models.DecimalField("Нормированный расход ДТ",max_digits=6, decimal_places=1, null=True)
    saving = models.DecimalField("Экономия",max_digits=6, decimal_places=1, null=True)    
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, verbose_name="Регион", related_name="resultStation", blank=True, null=True)
    area=models.ForeignKey(Region,on_delete=models.CASCADE, verbose_name="Участок", related_name="areaTrail")
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Имя пользователя", related_name="user_trail")
    double = models.BooleanField("Двойная тяга", blank=True, null=True)
    sectionDouble = models.ForeignKey(Loko,on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Тип 2-й секции", related_name="type_loko_double")
    numberDouble = models.ForeignKey(Loko,on_delete=models.SET_NULL, blank=True, null=True, verbose_name = "Номер 2-й секции", related_name="number_loko_double")
    bort = models.BooleanField("Борт не работает",blank=True, null=True, default=False)


    class Meta:
        verbose_name = "Вывощная работа"
        verbose_name_plural = "Вывозная работы"

class Report(models.Model):
    """Отчеты"""

    date = models.IntegerField("Дата смены")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name="Машинист", default=0)
    typeLoko = models.ForeignKey(Loko,on_delete=models.CASCADE, related_name='typeLoko', verbose_name="Тип секции")
    lokoNumber = models.ForeignKey(Loko,on_delete=models.CASCADE,related_name='lokoNumber', verbose_name="№ секции")
    smena=models.IntegerField("смена")
    weight=models.IntegerField("Весс поезда", blank=True, null=True, default=0)
    gp=models.IntegerField("Груженные вагоны", blank=True, null=True, default=0)
    pv=models.IntegerField("Порожние вагоны", blank=True, null=True, default=0)
    work_time_trail=models.IntegerField("Общее время вывозной работы",blank=True, null=True, default=0)
    fact_trail=models.IntegerField("Фактический расход ДТ на вывозной работе",blank=True, null=True, default=0)
    norm_trail=models.DecimalField("Нормированный расход ДТ на вывозной работе",max_digits=6, decimal_places=1, null=True, default=0)
    saving_trail = models.DecimalField("Экономия на вывозной работе",max_digits=6, decimal_places=1, null=True, default=0)
    work_time_manevr=models.IntegerField("Общее время работы маневровой работы",blank=True, null=True, default=0)
    fact_manevr=models.IntegerField("Фактический расход ДТ маневровой работы",blank=True, null=True, default=0)
    norm_manevr=models.DecimalField("Нормированный расход ДТ маневровой работы",max_digits=6, decimal_places=1, null=True, default=0)    
    saving_manevr = models.DecimalField("Экономия на маневровой работе",max_digits=6, decimal_places=1, null=True, default=0)
    fact_result=models.IntegerField("Фактический расход ДТ за смену",blank=True, null=True, default=0)
    norm_result=models.DecimalField("Нормированный расход ДТ за смену",max_digits=6, decimal_places=1, null=True, default=0)    
    saving_result = models.DecimalField("Экономия ДТ за смену",max_digits=6, decimal_places=1, null=True, default=0)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Регион")
    smenaStart=models.IntegerField("Начало смены", blank=True, null=True, default=0)
    smenaEnd=models.IntegerField("Окончание смены", blank=True, null=True, default=0)
    dtStart=models.IntegerField("ДТ на начало смены", blank=True, null=True, default=0)
    dtEnd=models.IntegerField("ДТ на окончание смены", blank=True, null=True, default=0)
    area=models.ForeignKey(Region, on_delete=models.SET_NULL, verbose_name="Участок",related_name='areaReport', blank=True, null=True)
    work_time_prostoy=models.IntegerField("Общее время простоя",blank=True, null=True, default=0)
    user = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Имя пользователя", related_name="user_report")
    bort = models.BooleanField("Борт не работает",blank=True, null=True, default=False)

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
    
class Settings(models.Model):
    """Настройки"""

    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name="Регион")
    settings = models.TextField("Настройки",blank=True, null=True)
   
class Menu(models.Model):
    """Менюшки"""

    MAINMENU= 'main_menu'
    MENU = 'left_menu'

    MENU_TYPES = (        
        (MAINMENU, 'Главное меню'),
        (MENU, 'Подменю')
    )

    name = models.CharField("Название",max_length=100)
    element_type = models.CharField("Тип элемента", max_length=50, choices=MENU_TYPES)
    section = models.ForeignKey('self', on_delete=models.SET_NULL, verbose_name="Меню", blank=True, null=True)    
    region = models.ManyToManyField(Region, verbose_name="Регион")
    role = models.ManyToManyField(Group, verbose_name="роли")
    link = models.CharField("Ссылка на компонент", max_length=100)

    def __str__(self):
        return self.name
    

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"