from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Route(models.Model):
    name = models.CharField(
        max_length=10, unique=True, verbose_name='Назва маршруту'
    )
    total_time = models.DurationField(
        verbose_name='Час у дорозі'
    )
    from_city = models.ForeignKey(
        'cities.City', on_delete=models.CASCADE, related_name='from_city_route',
        verbose_name='З якого міста'
    )
    to_city = models.ForeignKey(
        'cities.City', on_delete=models.CASCADE, related_name='to_city_route',
        verbose_name='До якого міста'
    )
    trains = models.ManyToManyField('trains.Train', verbose_name='Список поїздів')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Користувач',
        null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршрути'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('cities:detail', kwargs={'pk': self.pk})
