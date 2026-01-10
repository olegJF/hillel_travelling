from django.contrib import admin

from trains.models import Train

class TrainAdmin(admin.ModelAdmin):

    class Meta:
        model = Train

    list_display = ('id', 'number', 'travel_time', 'from_city', 'to_city')
    list_editable = ('travel_time', 'number',)

admin.site.register(Train, TrainAdmin)
