from django.test import TestCase
from django.urls import reverse

from cities.models import City
from routes.forms import RouteForm


class TrainTestCase(TestCase):
    fixtures = ('data.json',)

    def setUp(self):
        self.kyiv = City.objects.filter(name='Київ').first()
        self.dnipro = City.objects.filter(name='Дніпро').first()
        self.mykolaiv = City.objects.filter(name='Миколаїв').first()
        self.lutsk = City.objects.filter(name='Луцьк').first()

    def test_home_view(self):
        """Перевірка шаблону"""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='routes/home.html')

    def test_login_required(self):
        """Перевірка на необхідність авторизації"""
        response = self.client.post(reverse('add_route'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/add_route/')
        response = self.client.post(reverse('save_route'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login/?next=/save_route/')

    def test_messages_error_no_route(self):
        """ Виникнення помилки при побудові неїснуючого маршруту"""
        data = {
            'from_city': self.kyiv.id, 'to_city': self.kyiv.id,
            'expected_time': 12
        }
        response = self.client.post(reverse('find_routes'), data=data)
        self.assertContains(
            response, 'Маршруту, що задовільняє цим вимогам не існує', 1, 200
        )

    def test_messages_error_no_route_city(self):
        """ Маршрут через ці міста неможливий"""
        data = {
            'from_city': self.kyiv.id, 'to_city': self.dnipro.id,
            'expected_time': 12, 'cities': [self.lutsk.id]
        }
        response = self.client.post(reverse('find_routes'), data=data)
        self.assertContains(
            response, 'Маршрут через ці міста неможливий', 1, 200
        )

    def test_messages_error_no_time(self):
        """ Виникнення помилки Маршрут за такий час неможливий"""
        data = {
            'from_city': self.kyiv.id, 'to_city': self.dnipro.id,
            'expected_time': 9, 'cities': []
        }
        response = self.client.post(reverse('find_routes'), data=data)
        self.assertContains(
            response, 'Маршрут за такий час неможливий', 1, 200
        )

    def test_valid_form(self):
        """Перевірка валідної форми"""
        data = {
            'from_city': self.kyiv.id, 'to_city': self.dnipro.id,
            'expected_time': 9, 'cities': []
        }
        form = RouteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        """Перевірка неповної форми"""
        data = {
            'from_city': self.kyiv.id, 'to_city': self.dnipro.id,
            'cities': []
        }
        form = RouteForm(data=data)
        self.assertFalse(form.is_valid())
