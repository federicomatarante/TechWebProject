import json
from datetime import datetime
from json import JSONDecodeError
from pprint import pprint
from typing import Union

from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST, require_GET
from django.views.generic import DetailView, TemplateView

from GymApp.models import GymUser
from GymApp.utils import send_pdf, _get_or_error
from base_views import SearchListView
from mealplans.models import MealPlan, Meal, Ingredient, MealDay


class UserMealPlanView(DetailView):
    model = MealPlan
    template_name = 'usermealplan.html'
    context_object_name = 'mealplan'

    def get_object(self, queryset=None):
        try:
            index = int(self.request.GET['index']) if 'index' in self.request.GET else 0
            mealPlan = MealPlan.objects.filter(user=self.request.user).order_by('-creation_date')[index]
            return mealPlan
        except IndexError:
            return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_object() is None:
            return context
        index = int(self.request.GET['index']) if 'index' in self.request.GET else 0
        mealplans = MealPlan.objects.filter(user=self.request.user).count()
        context['prev_mealplan_url'] = (reverse_lazy('meaplan') + "?index=" + str(index - 1)) if index != 0 else None
        context['next_mealplan_url'] = (reverse_lazy('meaplan') + "?index=" + str(
            index + 1)) if index != mealplans - 1 else None
        return context


class ManageMealPlansView(SearchListView):
    template_name = 'manage_mealplans.html'

    def __init__(self):
        super().__init__(GymUser, 'username', 'gymusers', 10)

    def search(self, string: str):
        return GymUser.objects.filter(username__istartswith=string)

    def get_url(self, obj) -> str:
        if MealPlan.objects.filter(user=obj, actual_end_date=None).exists():
            return reverse_lazy('edit_mealplan', kwargs={'userName': obj.username})
        return reverse_lazy('create_mealplan', kwargs={'userName': obj.username})

    def get_name(self, obj) -> str:
        return obj.username


class EditMealPlanView(TemplateView):
    template_name = 'mealplanedit.html'

    def get_object(self):
        return MealPlan.objects.filter(user=self.request.user).order_by('-creation_date').first()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userName'] = self.kwargs['userName']
        context['index'] = self.kwargs['index'] if 'index' in self.kwargs else 0
        meal_plan = self.get_object()
        mealPlanJson = {
            'id': meal_plan.id,
            'expirationDay': meal_plan.expected_end_date.strftime('%Y-%m-%d'),
            'days': [
                {
                    'day': day.day,
                    'meals': [
                        {
                            'name': meal.name,
                            'ingredients': [
                                {
                                    'name': ingredient.name,
                                    'quantity': ingredient.quantity,
                                    'unit': ingredient.quantityType
                                } for ingredient in meal.ingredients.all()]
                        } for meal in day.meals.all()]
                } for day in meal_plan.mealDays.all()
            ]
        }
        context['mealPlan'] = json.dumps(mealPlanJson)

        return context


class CreateMealPlanView(TemplateView):
    template_name = 'mealplancreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['userName'] = self.kwargs['userName']
        context['index'] = self.kwargs['index'] if 'index' in self.kwargs else 0
        return context


@require_POST
def save_mealPlan(request, userName):
    try:
        body = json.loads(request.body)
        pprint(body)
        expiration_date = datetime.strptime(_get_or_error(body, 'expirationDay', str), '%Y-%m-%d')
        user = GymUser.objects.get(username=userName)
        mealPlanId = body.get('id')
        if mealPlanId:
            meal_plan = MealPlan.objects.get(id=mealPlanId)
            meal_plan.expected_end_date = expiration_date
            meal_plan.save()
            meal_plan.mealDays.all().delete()
        else:
            meal_plan = MealPlan(expected_end_date=expiration_date, user=user)
            meal_plan.save()
        days = _get_or_error(body, 'days', list)
        for day in days:
            day_number = _get_or_error(day, 'day', int)
            meal_day = MealDay(day=day_number, mealPlan=meal_plan)
            meal_day.save()
            meals = _get_or_error(day, 'meals', list)
            for parsed_meal in meals:
                meal_name = _get_or_error(parsed_meal, 'name', str)
                meal = Meal(name=meal_name, mealDay=meal_day)
                meal.save()
                ingredients = _get_or_error(parsed_meal, 'ingredients', list)
                for parsed_ingredient in ingredients:
                    ingredient_name = _get_or_error(parsed_ingredient, 'name', str)
                    ingredient_quantity = _get_or_error(parsed_ingredient, 'quantity', int)
                    ingredient_unit = _get_or_error(parsed_ingredient, 'unit', str)
                    ingredient = Ingredient(name=ingredient_name, quantity=ingredient_quantity,
                                            quantityType=ingredient_unit, meal=meal)
                    ingredient.save()
    except JSONDecodeError:
        return HttpResponse(status=400, content='Invalid JSON')
    except ValueError:
        return HttpResponse(status=400, content='Invalid values')
    except GymUser.DoesNotExist:
        return HttpResponse(status=404, content='User does not exist')

    return HttpResponse(status=200)


@require_GET
def download_mealPlan(request):
    index = int(request.GET.get('index')) if request.GET.get('index') else 0
    mealPlan = MealPlan.objects.filter(user=request.user).order_by('-creation_date')[index]
    rendered_html = render_to_string('mealplan_pdf.html', {'mealplan': mealPlan})
    return send_pdf(rendered_html, f'workout_{index}')
