from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie, Theater , Seat, Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
import os
import resend
import razorpay 

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
    if language :
        movies = movies.filter(language__iexact=language)


    
    return render(request,'movies/movie_list.html',{'movies':movies})

def movie_detail(request,movie_id):
    movie = get_object_or_404(Movie, id = movie_id)
    
    return render(request,'movies/movie_detail.html',{
            'movie' : movie,
        })

def theater_list(request,movie_id):
    movies= get_object_or_404(Movie,id=movie_id)
    theater = Theater.objects.filter(movie = movies)
    return render(request,'movies/theater_list.html',{'movie':movies,'theaters':theater})

@login_required(login_url='/login/')
def book_Seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theater)

    # Mark already paid seats as booked
    for seat in seats:
        seat.is_booked = Booking.objects.filter(
            seat=seat,
            is_paid=True
        ).exists()

    if request.method == "POST":
        selected_seats = request.POST.getlist("seats")
        

        if not selected_seats:
            return render(request, "movies/seat_selection.html", {
                "theater": theater,
                "seats": seats,
                "error": "Please select at least one seat."
            })

        try:
            for seat_id in selected_seats:
                seat = get_object_or_404(
                    Seat,
                    id=seat_id,
                    theater=theater
                )

                # Check if seat is already booked
                if Booking.objects.filter(
                    seat=seat,
                    is_paid=True
                ).exists():
                    return render(request, "movies/seat_selection.html", {
                        "theater": theater,
                        "seats": seats,
                        "error": f"Seat {seat.seat_number} is already booked."
                    })

                
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theater.movie,
                    theater=theater,
                    is_paid=False
                )
            

            return redirect("/movies/payment/")

        except Exception as e:
            return render(request, "movies/seat_selection.html", {
                "theater": theater,
                "seats": seats,
                "error": str(e)
            })

    return render(request, "movies/seat_selection.html", {
        "theater": theater,
        "seats": seats
    })



                    
                    
def payment_page(request):

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": 50000, #500(in paise)
        "currency": "INR",
        "payment_capture": "1"
    })
    return render(request,"movies/payment.html",{"payment":payment, 
                                                 "key_id":settings.RAZORPAY_KEY_ID,
                                                   "amount":payment["amount"],
                                                 "order_id": payment['id']})

def payment_success(request):
    bookings = list(
        Booking.objects.filter(
            user=request.user,
            is_paid=False
        )
    )

    if bookings:
        seat_numbers = []
        theater = None
        movie = None

        for booking in bookings:
            seat_numbers.append(booking.seat.seat_number)
            theater = booking.theater
            movie = booking.movie

        Booking.objects.filter(
            id__in=[booking.id for booking in bookings]
        ).update(is_paid=True)

        try:
            resend.api_key = os.environ.get("RESEND_API_KEY")

            result = resend.Emails.send({
                "from": "BookMySeat <onboarding@resend.dev>",
                "to": [request.user.email],
                "subject": "Booking Confirmed",
                "html": f"""
                    <h2>Booking Confirmed</h2>
                    <p>Hi {request.user.username},</p>
                    <p>Your ticket has been booked successfully.</p>
                    <p><strong>Movie:</strong> {movie.name}</p>
                    <p><strong>Theater:</strong> {theater.name}</p>
                    <p><strong>Seats:</strong> {', '.join(seat_numbers)}</p>
                    <p>Enjoy your show!</p>
                    <p>-- BookMySeat Team</p>
                """
            })

            print("EMAIL SENT:", result)

        except Exception as e:
            print("RESEND EMAIL ERROR:", e)

        return render(request,"movies/success.html")
    
    return render(request,"movies/success.html")

def payment_failed(request):
     return render(request,"movies/payment_failed.html")


