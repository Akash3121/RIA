from django.http import JsonResponse
from django.shortcuts import render
from .models import User, Movie, Checkout
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request, 'bricksmasher_app/home.html')

def account(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        if not User.objects.filter(email=email).exists():
            User.objects.create(first_name=first_name, last_name=last_name, email=email)
            message = "Account created successfully!"
        else:
            message = "Email already exists! Account not created."
        return render(request, 'bricksmasher_app/account.html', {'message': message})
    return render(request, 'bricksmasher_app/account.html')

def movie(request):
    movies = Movie.objects.all().order_by('title')
    return render(request, 'bricksmasher_app/movie.html', {'movies': movies})

@csrf_exempt
def rent(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            checkouts = Checkout.objects.filter(user=user)
            movies_in_stock = Movie.objects.exclude(id__in=[checkout.movie.id for checkout in checkouts])
            return render(request, 'bricksmasher_app/rent.html', {'user': user, 'checkouts': checkouts, 'movies_in_stock': movies_in_stock})
        else:
            message = "User not found. Please enter a valid email."
            return render(request, 'bricksmasher_app/rent.html', {'message': message})
    return render(request, 'bricksmasher_app/rent.html')
def db_user(request):
    if request.method == 'GET':
        email = request.GET.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            return JsonResponse(user.to_dict(), safe=False)
        else:
            return JsonResponse({'error': 'User not found'}, status=404)
    elif request.method == 'POST':
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if not User.objects.filter(email=email).exists():
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email)
            return JsonResponse(user.to_dict(), safe=False)
        else:
            return JsonResponse({'error': 'Email already exists'}, status=400)

def db_movie(request):
    if request.method == 'GET':
        user_id = request.GET.get("user_id")
        movie_id = request.GET.get("movie_id")
        movies = Movie.objects.all().order_by('title')
        return JsonResponse([movie.to_dict() for movie in movies], safe=False)
    elif request.method == 'POST':
        user_id = request.POST.get("user_id")
        movie_id = request.POST.get("movie_id")
        action = request.POST.get("action")
        if action == 'new':
            title = request.POST.get("title").strip()
            if not title or Movie.objects.filter(title=title).exists():
                return JsonResponse({'error': 'Invalid movie title'}, status=400)
            else:
                movie = Movie.objects.create(title=title, in_stock=1, checked_out=0)
                movies = Movie.objects.all().order_by('title')
                return JsonResponse([movie.to_dict() for movie in movies], safe=False)
        elif action in ['add', 'remove']:
            movie_id = request.POST.get("movie_id")
            movie = Movie.objects.filter(id=movie_id).first()
            if not movie:
                return JsonResponse({'error': 'Invalid movie ID'}, status=400)
            if action == 'add':
                movie.in_stock += 1
            elif action == 'remove':
                if movie.in_stock > 0:
                    movie.in_stock -= 1
                else:
                    return JsonResponse({'error': 'No copies in stock'}, status=400)
            movie.save()
            movies = Movie.objects.all().order_by('title')
            return JsonResponse([movie.to_dict() for movie in movies], safe=False)

def db_rent(request):
    if request.method == 'GET':
        user_id = request.GET.get("user_id")
        movie_id = request.GET.get("movie_id")

        filters = {}
        if user_id:
            filters['user_id'] = user_id
        if movie_id:
            filters['movie_id'] = movie_id

        checkouts = Checkout.objects.filter(**filters)
        return JsonResponse([checkout.to_dict() for checkout in checkouts], safe=False)

    elif request.method == 'POST':
        user_id = request.POST.get("user_id")
        movie_id = request.POST.get("movie_id")
        action = request.POST.get("action")

        user = User.objects.filter(id=user_id).first()
        movie = Movie.objects.filter(id=movie_id).first()

        if not user or not movie:
            return JsonResponse({'error': 'Invalid user or movie ID'}, status=400)

        if action == 'rent':
            if movie.in_stock == 0:
                return JsonResponse({'error': 'No copies in stock'}, status=400)
            if Checkout.objects.filter(user=user, movie=movie).exists():
                return JsonResponse({'error': 'Movie already checked out by user'}, status=400)
            if Checkout.objects.filter(user=user).count() >= 3:
                return JsonResponse({'error': 'User has reached maximum limit of 3 movies'}, status=400)

            movie.in_stock -= 1
            movie.checked_out += 1
            movie.save()

            checkout = Checkout.objects.create(user=user, movie=movie)

        elif action == 'return':
            checkout = Checkout.objects.filter(user=user, movie=movie).first()
            if not checkout:
                return JsonResponse({'error': 'Movie not checked out by user'}, status=400)

            movie.in_stock += 1
            movie.checked_out -= 1
            movie.save()

            checkout.delete()

        checkouts = Checkout.objects.filter(user=user)
        return JsonResponse([checkout.to_dict() for checkout in checkouts], safe=False)
