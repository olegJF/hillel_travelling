from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from trains.models import Train

User = get_user_model()

class TrainTestCase(TestCase):
    fixtures = ('data.json',)

    def setUp(self):
        self.admin = User.objects.get(username='oleg')
        self.user = User.objects.get(username='qwerty')
        self.train = Train.objects.select_related('from_city', 'to_city').first()

    def test_object_duplicate(self):
        """ Виникнення помилки при дублюванні назви"""
        train = Train(number=self.train.number)
        with self.assertRaises(ValidationError):
            train.full_clean()

    def test_user_cannot_create_object(self):
        """Звичайний юзер не може створювати нові поїзди"""
        before = Train.objects.all().count()
        self.client.force_login(self.user)
        response = self.client.post(reverse('trains:create'), {'number': 'Bonn'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        after = Train.objects.all().count()
        self.assertEqual(before, after)

    def test_admin_can_create_object(self):
        """Адмін може створювати нові поїзди"""
        before = Train.objects.all().count()
        self.client.force_login(self.admin)
        data = {'number': '111', 'from_city': self.train.from_city_id,
                'to_city': self.train.to_city_id, 'travel_time': 12545874}
        response = self.client.post(reverse('trains:create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/trains/')
        after = Train.objects.all().count()
        self.assertEqual(before + 1, after)
        train = Train.objects.filter(number='111').first()
        self.assertIsNotNone(train)
        self.assertEqual(train.number, '111')
        url = train.get_absolute_url()
        self.assertEqual(url, f'/trains/{train.id}/')

    def test_cbv_detail_view(self):
        """Перевірка шаблону"""
        response = self.client.get(reverse(
            'trains:detail', kwargs={'pk': self.train.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='trains/detail.html')

    def test_login_required(self):
        """Перевірка на необхідність авторизації"""
        response = self.client.post(reverse('trains:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/trains/update/1/')
        response = self.client.post(reverse('trains:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/trains/delete/1/')
        response = self.client.post(reverse('trains:create'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/trains/add/')

    def test_object_duplicate_time(self):
        """ Виникнення помилки при дублюванні часу у дорозі"""
        data = {
            'number': '111', 'from_city_id': self.train.from_city_id,
            'to_city': self.train.to_city, 'travel_time': self.train.travel_time
        }
        train = Train(**data)
        with self.assertRaises(ValidationError):
            train.full_clean()
        try:
            train.full_clean()
        except ValidationError as e:
            self.assertIn(
                'Не може бути двох однакових поїздів з однаковим часом',
                e.messages
            )

    def test_object_one_city(self):
        """ Виникнення помилки при однакових містах відправлення та прибуття"""
        data = {'number': '111', 'from_city_id': self.train.from_city_id,
                'to_city': self.train.from_city,
                'travel_time': '23:34:06'
                }
        train = Train(**data)
        with self.assertRaises(ValidationError):
            train.full_clean()
        try:
            train.full_clean()
        except ValidationError as e:
            self.assertIn(
                'Потяг не може приходити до того міста з якого вийшов',
                e.messages
            )
