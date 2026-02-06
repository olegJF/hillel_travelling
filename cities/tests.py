from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from cities.models import City

User = get_user_model()

class CityTestCase(TestCase):
    fixtures = ('data.json',)

    def setUp(self):
        self.admin = User.objects.get(username='oleg')
        self.user = User.objects.get(username='qwerty')

    def test_object_duplicate(self):
        """ Виникнення помилки при дублюванні назви"""
        city = City(name='Київ')
        with self.assertRaises(ValidationError):
            city.full_clean()

    def test_user_cannot_create_object(self):
        """Звичайний юзер не може створювати нові міста"""
        before = City.objects.all().count()
        self.client.force_login(self.user)
        response = self.client.post(reverse('cities:create'), {'name': 'Bonn'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        after = City.objects.all().count()
        self.assertEqual(before, after)

    def test_admin_can_create_object(self):
        """Адмін може створювати нові міста"""
        before = City.objects.all().count()
        self.client.force_login(self.admin)
        response = self.client.post(reverse('cities:create'), {'name': 'Bonn'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cities/')
        after = City.objects.all().count()
        self.assertEqual(before + 1, after)
        city = City.objects.filter(name='Bonn').first()
        self.assertIsNotNone(city)
        self.assertEqual(city.name, 'Bonn')
        url = city.get_absolute_url()
        self.assertEqual(url, f'/cities/{city.id}/')

    def test_cbv_detail_view(self):
        """Перевірка шаблону"""
        city = City.objects.filter(name='Київ').first()
        response = self.client.get(reverse('cities:detail', kwargs={'pk': city.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='cities/detail.html')

    def test_login_required(self):
        """Перевірка на необхідність авторизації"""
        response = self.client.post(reverse('cities:update', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/cities/update/1/')
        response = self.client.post(reverse('cities:delete', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/cities/delete/1/')
        response = self.client.post(reverse('cities:create'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/cities/add/')
