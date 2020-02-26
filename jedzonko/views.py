import string
from datetime import datetime
from django.http import HttpResponse, Http404, HttpRequest
from jedzonko.models import *
from django.shortcuts import render, redirect
from django.views import View
import random
from django.core.paginator import Paginator
from django.contrib import messages


def validation(data):
    return data != ''


def make_int(data):
    try:
        data = int(data)
    except:
        data = ''
    return data


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "test.html", ctx)


class HomePage(View):
    def get(self, request):
        recipes = list(Recipe.objects.all())
        random.shuffle(recipes)
        recipes = recipes[:3]
        context = {
            'recipes': recipes
        }
        return render(request, "index.html", context)


class RecipeDetails(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        path = request.META.get('HTTP_REFERER')
        return render(request, 'app-recipe-details.html', {'recipe': recipe, 'id': id, 'path':path})

    def post(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        like_recipe = request.POST.get("like_recipe")
        if like_recipe == "Polub przepis":
            recipe.votes += 1
        elif like_recipe == "Nie lubię przepisu":
            recipe.votes -= 1
        recipe.save()
        return HttpResponse(self.get(request, id))


class Dashboard(View):
    def get(self, request):
        number_of_recipes = Recipe.objects.count()
        number_of_plans = Plan.objects.count()
        newest_plan = Plan.objects.all().order_by('-pk')[0]
        meals = RecipePlan.objects.filter(plan=newest_plan).order_by('order')
        days = DayName.objects.all().order_by('order')
        context = {
            'number_of_recipe': number_of_recipes,
            'number_of_plan': number_of_plans,
            'newest_plan': newest_plan,
            'meals': meals,
            'days': days,
        }
        return render(request, 'dashboard.html', context=context)


class RecipeAdd(View):
    def get(self, request):
        return render(request, 'app-add-recipe.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        preparation = request.POST.get('preparation')
        ingredients = request.POST.get('ingredients')

        if validation(name) and validation(description) and validation(preparation) and validation(
                ingredients) and validation(make_int(preparation_time)):
            Recipe.objects.create(name=name, description=description, ingredients=ingredients,
                                  preparation_time=int(preparation_time), preparation=preparation)
            return redirect('/recipe/list/')
        info = 'Wypełnij poprawnie wszystkie pola!'
        context = {
            'name': name,
            'description': description,
            'preparation_time': preparation_time,
            'preparation': preparation,
            'ingredients': ingredients,
            'Info': info,
        }
        return render(request, 'app-add-recipe.html', context=context)


class RecipeModify(View):
    def get(self, request, id):
        try:
            recipe = Recipe.objects.get(pk=id)
            return render(request, 'app-edit-recipe.html', {'recipe': recipe})
        except:
            raise Http404

    def post(self, request, id):
        name = request.POST.get('name')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        preparation = request.POST.get('preparation')
        ingredients = request.POST.get('ingredients')
        if validation(name) and validation(description) and validation(preparation) and validation(
                ingredients) and validation(preparation_time):
            Recipe.objects.create(name=name, description=description, ingredients=ingredients,
                                  preparation_time=preparation_time, preparation=preparation)
            return redirect('/recipe/list/')
        messages.add_message(request, messages.INFO, "Wypełnij poprawnie wszystkie pola!")
        return redirect(f'/recipe/modify/{id}')





def Plans(request):
    if request.method == 'GET':
        app_schedules = Plan.objects.all().order_by('name')
        paginator = Paginator(app_schedules, 50)
        page = request.GET.get('page')
        schedules = paginator.get_page(page)
        return render(request, 'app-schedules.html', {'schedules': schedules})
    if request.method == 'POST':
        delete_plan_id = request.POST.get("delete_schedule_id")
        remove_plan_id = make_int(delete_plan_id)
        if validation(remove_plan_id):
            plan_to_remove = Plan.objects.get(pk=remove_plan_id)
            plan_to_remove.delete()
        return redirect('/plan/list/')





class PlanDetails(View):
    def get(self, request, id):
        plan = Plan.objects.get(pk=id)
        recipe_plan = RecipePlan.objects.filter(plan_id=id)
        meals = recipe_plan.order_by('order').order_by('day_name_id')
        days = DayName.objects.all().order_by('order')
        context = {'plan': plan,
                   'days': days,
                   'meals': meals,
                   'recipe_plan': recipe_plan}
        return render(request, 'app-details-schedules.html', context)

    def post(self, request, id):
        delete_meal_id = request.POST.get("delete_meal_id")
        remove_meal_id = make_int(delete_meal_id)
        if validation(remove_meal_id):
            meal_to_remove = RecipePlan.objects.get(pk=remove_meal_id)
            meal_to_remove.delete()
        return redirect(f'/plan/{id}/details')


class PlanAdd(View):
    def get(self, request):
        return render(request, 'app-add-schedules.html')

    def post(self, request):
        name = request.POST.get('name')
        description = request.POST.get('description')

        if validation(name) and validation(description):
            new_plan = Plan.objects.create(name=name, description=description)
            id = new_plan.id
            return redirect(f'/plan/{id}/details')
        return render(request, 'app-add-schedules.html', {'Info': 'Wypełnij poprawnie wszystkie pola!'})


class PlanAddRecipe(View):
    def get(self, request):
        days = DayName.objects.all()
        all_plans = Plan.objects.all()
        recipes = Recipe.objects.all()

        plan_id = request.GET.get('plan_id')
        if plan_id:
            plan = Plan.objects.get(pk=plan_id)
            context = {
                'plan': plan,
                'all_plans': all_plans,
                'days': days,
                'recipes': recipes,
            }
        else:
            context = {
                'all_plans': all_plans,
                'days': days,
                'recipes': recipes,
            }
        return render(request, 'app-schedules-meal-recipe.html', context=context)

    def post(self, request):
        plan_id = request.POST.get('plan_id')
        if plan_id:
            plan = Plan.objects.get(pk=plan_id)
        else:
            plan_id = request.POST.get('plan')
            plan = Plan.objects.get(pk=plan_id)

        meal_name = request.POST.get('meal_name')
        order = request.POST.get('order')

        day_id = request.POST.get('day_name_id')
        day = DayName.objects.get(pk=day_id)

        recipe_id = request.POST.get('recipe_id')
        recipe = Recipe.objects.get(pk=recipe_id)

        RecipePlan.objects.create(meal_name=meal_name, order=order, day_name=day, plan=plan,
                                  recipe=recipe)

        return redirect(f'/plan/{plan_id}/details')





def AppRecipes(request):
    if request.method == 'GET':
        app_recipes = Recipe.objects.all().order_by('-created').order_by('-votes')
        paginator = Paginator(app_recipes, 50)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        return render(request, 'app-recipes.html', {'recipes': recipes})

    if request.method == 'POST':

        submit = request.POST.get('submit')
        if submit == 'szukaj':
            lookup = request.POST.get('q')

            if validation(lookup):
                recipes = Recipe.objects.filter(name__icontains=lookup).order_by('-created').order_by('-votes')
                return render(request, 'app-recipes.html', {'recipes': recipes})
            return redirect('/recipe/list/')
        else:
            delete_recipe_id = request.POST.get("delete_recipe_id")
            remove_recipe_id = make_int(delete_recipe_id)
            if validation(remove_recipe_id):
                recipe_to_remove = Recipe.objects.get(pk=remove_recipe_id)
                recipe_to_remove.delete()
            return redirect('/recipe/list/')


def set_recipe_data():
    for _ in range(0, 150):
        recipe = Recipe()
        letters = string.ascii_lowercase
        recipe.name = ''.join(random.choice(letters) for i in range(16))
        recipe.ingredients = ''.join(random.choice(letters) for i in range(32))
        recipe.description = ''.join(random.choice(letters) for i in range(32))
        recipe.preparation = ''.join(random.choice(letters) for i in range(32))
        recipe.preparation_time = random.randint(1, 240)
        recipe.votes = random.randint(1, 99)
        recipe.save()


def set_plan_data():
    for _ in range(0, 180):
        plan = Plan()
        letters = string.ascii_lowercase
        plan.name = ''.join(random.choice(letters) for i in range(16))
        plan.description = ''.join(random.choice(letters) for i in range(32))
        plan.save()


class PlanModify(View):
    def get(self, request, id):
        try:
            plan = Plan.objects.get(pk=id)
            return render(request, 'app-edit-schedules.html', {'plan': plan})
        except:
            raise Http404

    def post(self, request, id):
        plan = Plan.objects.get(pk=id)
        name = request.POST.get('name')
        description = request.POST.get('description')
        if validation(name) and validation(description):
            plan.name = name
            plan.description = description
            plan.save()
            return redirect('/plan/list/')
        messages.add_message(request, messages.INFO, "Wypełnij poprawnie wszystkie pola!")
        return redirect(f'/recipe/modify/{id}')


class Contact(View):
    def get(self, request):
        try:
            contact = Page.objects.get(slug='contact')
            contact_detail = contact.description.split(",")
            if contact != None:
                return render(request, "contact.html", context={"contact_detail": contact_detail})
        except:
            return redirect("/#contact")


class About(View):
    def get(self, request):
        try:
            about = Page.objects.get(slug='about')
            about_detail = about.description.split(",")
            if about != None:
                return render(request, "about.html", context={"about_detail": about_detail})
        except:
            return redirect("/#about")
