from django.contrib import admin
from django import forms


from .models import Driver, Loko, Region, Mileage, Norms, Settings, Report, Menu, Result_trail, Result_manevr


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region")
    list_display_links = ("name",)

@admin.register(Loko)
class LokoAdmin(admin.ModelAdmin):
    list_display = ("id","name","element_type", "section")
    list_display_links = ("name",)

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name","element_type", "section")
    list_display_links = ("name",)   

#class LokoAdminForm(forms.ModelForm):
 #   def __init__(self, *args, **kwargs):
  #      super().__init__(*args, **kwargs)
   #     self.fields['number_loko'].queryset = self.instance.number_loko.filter(element_type = "element")



@admin.register(Norms)
class NormsAdmin(admin.ModelAdmin):
    list_display = ("id","type_work","type_loko", "region","area","station", "station_dep","station_arr", "distance", 
    "coeff", "norma_reserv","norma_fix","norm_manevr", "norm_plain", "ov")
    list_display_links = ("type_loko",)   
    fieldsets = (
        (None, {
            "fields": (("type_work","type_loko"),)
        }),
        (None, {
            "fields": (("region","area","station"),)
        }), 
        (None, {
            "fields": (("station_dep","station_arr"),)
        }),
        (None, {
            "fields": (("distance", "coeff", "norma_reserv","norma_fix"),)
        }),
        (None, {
            "fields": (("norm_manevr", "norm_plain", "ov", "burning"),)
        }),               
        )
    
    
@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display=("id","region","settings")
    list_display_links = ("region",) 

@admin.register(Report)
class SettingsAdmin(admin.ModelAdmin):
    list_display=("id","driver","date","fact_result","norm_result","saving_result", "lokoNumber")
    list_display_links = ("driver",) 

@admin.register(Result_trail)
class SettingsAdmin(admin.ModelAdmin):
    list_display=("id","driver","dateStart","fact","norm","saving","lokoNumber" )
    list_display_links = ("driver",)

@admin.register(Result_manevr)
class SettingsAdmin(admin.ModelAdmin):
    list_display=("id","driver","dateStart","fact_manevr","norm_manevr","saving_manevr", "lokoNumber")
    list_display_links = ("driver",)

@admin.register(Menu)
class SettingsAdmin(admin.ModelAdmin):
    list_display=("id","name","element_type")
    list_display_links = ("name",)  

