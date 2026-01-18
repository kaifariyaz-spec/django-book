from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie, Theater , Seat, Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings

def movie_list(request):
    search_query = request.GET.get('search')
    if search_query:
        movies = Movie.objects.filter(name__icontains = search_query)
    else:
        movies= Movie.objects.all()
    
    genre = request.GET.get('genre')
    if genre :
        movies = movies.filter(genre__iexact=genre)

    language = request.GET.get('language')
    if genre :
        movies = movies.filter(language__iexact=language)


    
    return render(request,'movies/movie_list.html',{'movies':movies})


def theater_list(request,movie_id):
    movies= get_object_or_404(Movie,id=movie_id)
    theater = Theater.objects.filter(movie = movies)
    return render(request,'movies/theater_list.html',{'movie':movies,'theaters':theater})

@login_required(login_url='/login/')
def book_Seats(request, theater_id):
    theaters = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theaters)

    if request.method == "POST":
        selected_seats = request.POST.getlist('seats')

        print("SELECTED:", selected_seats)  # DEBUG

        if not selected_seats:
            return render(request, "movies/seat_selection.html", {
                "theaters": theaters,
                "seats": seats,
                "error": "Please select at least one seat"
            })

        for seat_id in selected_seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theaters)

            if seat.is_booked:
                continue

            Booking.objects.create(
                user=request.user,
                seat=seat,
                movie=theaters.movie,
                theater=theaters
            )

            seat.is_booked = True
            seat.save()

            # SEND BOOKING CONFIRMATION EMAIL
            send_mail(
                subject= "Booking Confirmed🎫",
                message= f"""
                Hi {request.user.username},

                Your booking is confirmed!

                Movie : {theaters.movie.name}
                Theater : {theaters.name}
                Seat : {seat.seat_number}

                Enjoy the show!
                BookMySeat Team
                """,

                from_email=settings.EMAIL_HOST_USER,

                recipient_list=[request.user.email],
                fail_silently=False,

            
          

            )


        return redirect("profile")  # or wherever your profile page is

    return render(request, "movies/seat_selection.html", {
        "theaters": theaters,
        "seats": seats
    })






