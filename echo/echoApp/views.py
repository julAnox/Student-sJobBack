from django.conf import settings
from django.db.models import F
from rest_framework import status
from echoApp.models import *
from echoApp.validators import email_validator
from echoApp.backend import get_user, fast_hash, is_user_auth, is_has_company
from .serializers import CommentSerializer, VacancySerializer, SummarySerializer, CompanySerializer
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response  # Correct import
from echoApp.models import Country, Region, District  # Make sure you're importing the models correctly

@api_view(["GET"])
def get_countries(request):
    countries = Country.objects.all()
    clean_data = []
    for country in countries:
        country_data = {country.title: []}
        regions = Region.objects.filter(country=country)
        for region in regions:
            region_data = {region.title: []}
            districts = District.objects.filter(region=region)
            for district in districts:
                region_data[region.title].append(district.title)
            country_data[country.title].append(region_data)
        clean_data.append(country_data)
    return Response({"clean_data": clean_data})  # Use DRF Response class to return the data


@api_view(["GET", "POST"])
def comments(request):
    if request.method == "GET":
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response({"comments": serializer.data})

    if request.method == "POST":
        if 'user' in request.data and request.data['user'] != '' and request.data['text'] != '':
            Comment.objects.create(user=request.data['user'], text=request.data['text'])
        else:
            user = User.objects.get(id=request.session.get(settings.USER_SESSION_ID)['user'])
            Comment.objects.create(user=f'{user.first_name} {user.last_name}', text=request.data['text'],
                                   photo=user.img)
        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def vacancies(request):
    vacancies = Vacancy.objects.filter(is_publish=True)
    serializer = VacancySerializer(vacancies, many=True)
    return Response({"vacancies": serializer.data})


@api_view(["GET", "POST"])
def vacancy(request, pk):
    try:
        vacancy = Vacancy.objects.get(id=pk)
    except Vacancy.DoesNotExist:
        return Response({"error": "Vacancy not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = VacancySerializer(vacancy)
        return Response({"vacancy": serializer.data})

    elif request.method == "POST":
        vacancy.responses = F('responses') + 1
        vacancy.save()
        Response.objects.create(message=request.data['message'], vacancy_id=pk,
                                user=User.objects.get(id=is_user_auth(request)))
        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def filter_vacancies(request):
    title = request.GET.get('title', '')
    salary = request.GET.get('salary', '')
    currency = request.GET.get('currency', '')
    country = request.GET.get('country', '')
    region = request.GET.get('region', '')
    district = request.GET.get('district', '')
    experience = request.GET.get('experience', '')
    education = request.GET.get('education', '')
    employment = request.GET.get('employment', '')

    vacancies = Vacancy.objects.filter(is_publish=True)

    if country:
        vacancies = vacancies.filter(country=Country.objects.get(title=country))
    if region:
        vacancies = vacancies.filter(region=Region.objects.get(title=region))
    if district:
        vacancies = vacancies.filter(district=District.objects.get(title=district))
    if experience:
        vacancies = vacancies.filter(experience=experience)
    if currency:
        vacancies = vacancies.filter(currency=currency)
    if education:
        vacancies = vacancies.filter(education=education)
    if employment:
        vacancies = vacancies.filter(employment=employment)
    if salary:
        vacancies = vacancies.filter(salary__gt=salary)
    if title:
        vacancies = vacancies.filter(title__icontains=title)

    serializer = VacancySerializer(vacancies, many=True)
    return Response({"vacancies": serializer.data})


@api_view(["GET"])
def summaries(request):
    summaries = Summary.objects.filter(is_publish=True)
    serializer = SummarySerializer(summaries, many=True)
    return Response({"summaries": serializer.data})


@api_view(["GET"])
def summary(request, pk):
    try:
        summary = Summary.objects.get(id=pk)
    except Summary.DoesNotExist:
        return Response({"error": "Summary not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = SummarySerializer(summary)
    return Response({"summary": serializer.data})


@api_view(["POST"])
def login(request):
    context = {}
    if not is_user_auth(request):
        email = request.data.get('email')
        password = request.data.get('password')
        context['error'] = 'Email is invalid'

        if email_validator(email):
            context['error'] = 'This email does not exist'
            if get_user(email):
                context['error'] = 'Incorrect password'
                user_obj = User.objects.filter(email=email, password=fast_hash(password))
                if len(user_obj) == 1:
                    request.session[settings.USER_SESSION_ID] = {'user': user_obj[0].id}
                    return Response({"status": "ok"}, status=status.HTTP_200_OK)
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    return redirect('home')


@api_view(["POST"])
def signup(request):
    if not is_user_auth(request):
        email = request.data.get('email')
        password1 = request.data.get('password1')
        password2 = request.data.get('password2')

        if email_validator(email):
            return Response({"error": "This email already in use"}, status=status.HTTP_400_BAD_REQUEST)
        if not get_user(email):
            if password1 == password2:
                user_obj = User.objects.create(email=email, password=fast_hash(password1))
                request.session[settings.USER_SESSION_ID] = {'user': user_obj.id}
                return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
        return Response({"error": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
    return redirect('home')


@api_view(["GET", "POST"])
def profile(request):
    if not is_user_auth(request):
        return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

    user = User.objects.get(id=is_user_auth(request))
    if request.method == "GET":
        context = {'auth_user': user}
        try:
            company = Company.objects.get(creator=user)
            context['company'] = company
        except Company.DoesNotExist:
            context['company'] = None
        return Response(context)

    elif request.method == "POST":
        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.birthday = request.data.get('birthday', user.birthday)
        user.gender = request.data.get('gender', user.gender)
        user.phone = request.data.get('phone', user.phone)
        user.save()
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


@api_view(["GET"])
def my_summaries(request):
    if is_user_auth(request):
        user = User.objects.get(id=is_user_auth(request))
        summaries = Summary.objects.filter(user=user)
        serializer = SummarySerializer(summaries, many=True)
        return Response({"summaries": serializer.data})
    return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
def create_summary(request):
    user = User.objects.get(id=is_user_auth(request))
    if request.method == "POST":
        vacancy_data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'user': user,
            'experience': request.data.get('experience'),
            'education': request.data.get('education'),
            'employment': request.data.get('employment'),
        }
        Summary.objects.create(**vacancy_data)
        return Response({"status": "ok"}, status=status.HTTP_201_CREATED)
    return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def add_company(request):
    user = is_user_auth(request)
    if user and not is_has_company(user):
        company_data = {
            'title': request.data['title'],
            'country': Country.objects.get(title=request.data['country']),
            'description': request.data['description'],
            'creator_id': user,
            'logo': request.data.get('logo', None),
        }
        company = Company.objects.create(**company_data)
        return Response({"company": CompanySerializer(company).data}, status=status.HTTP_201_CREATED)
    return Response({"error": "User already has a company or is not authenticated"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def my_company(request):
    user = is_user_auth(request)
    if user:
        try:
            company = Company.objects.get(creator=user)
            serializer = CompanySerializer(company)
            return Response({"company": serializer.data})
        except Company.DoesNotExist:
            return Response({"error": "No company found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "User not authenticated"}, status=status.HTTP_401)
