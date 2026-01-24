from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse


class Train(models.Model):
    number = models.CharField(
        max_length=10, unique=True, verbose_name='Номер потягу'
    )
    # travel_time = models.DecimalField(
    #     max_digits=4, decimal_places=2, verbose_name='Час у дорозі'
    # )
    travel_time = models.DurationField(
        verbose_name='Час у дорозі', null=True, blank=True
    )
    from_city = models.ForeignKey(
        'cities.City', on_delete=models.CASCADE, related_name='from_city_set',
        verbose_name='З якого міста'
        # null=True, blank=True
    )
    to_city = models.ForeignKey(
        'cities.City', on_delete=models.CASCADE, related_name='to_city_set',
        verbose_name='До якого міста'
    )

    def clean(self):
        if self.from_city == self.to_city:
            raise ValidationError(
                'Потяг не може приходити до того міста з якого вийшов')
        qs = Train.objects.filter(
            from_city=self.from_city, to_city=self.to_city,
            travel_time=self.travel_time).exclude(pk=self.pk)
        if qs.exists():
            raise ValidationError(
                'Не може бути двох однакових поїздів з однаковим часом')

    def save(self, **kwargs):
        self.clean()
        super().save(**kwargs)


    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Потяг'
        verbose_name_plural = 'Потяги'
        ordering = ['number']

    def get_absolute_url(self):
        return reverse('cities:detail', kwargs={'pk': self.pk})


class TrainTest(models.Model):
    number = models.CharField(
        max_length=10, unique=True, verbose_name='Номер потягу'
    )

    from_city = models.ForeignKey(
        'cities.City', on_delete=models.CASCADE,
        related_name='from_city',
        verbose_name='З якого міста'
        # null=True, blank=True
    )
