from django.shortcuts import render, redirect ,get_object_or_404
from .models import Movie, Theater , Seat, Booking
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.core.mail import send_mail
from django.conf import settings
import os
import resend
import razorpay 
from django.utils import timezone
from datetime import timedelta
from django.http import HttpResponse

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
    # expired_bookings = Booking.objects.filter(is_paid=False)

    # for booking in expired_bookings:
    #     if booking.created_at + timedelta(minutes=5) < timezone.now():
    #         booking.delete()

    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater_id=theater_id)

    for seat in seats:
        seat.is_booked = Booking.objects.filter(seat=seat,is_paid=True).exists()

    if request.method == "GET":
        return render(request,"movies/seat_selection.html",{
            "theater": theater,
            "seats": seats
        })

    if request.method == "POST":
        selected_seats = request.POST.getlist('seats')

        if not selected_seats:
            return render(request,"movies/seat_selection.html",{
                "theater" : theater,
                "seats" : seats,
                "error" : "Please select at least one seat"

            })
        booked_seats = []

        for seat_id in selected_seats:
            seat = Seat.objects.get(id=seat_id)
            
            booking, created = Booking.objects.get_or_create(
                seat=seat,
                defaults= {
                    "user" : request.user,
                    "movie" : theater.movie,
                    "theater" : theater,
                    "is_paid" : False
            }
            )
            
            if created:
                booked_seats.append(seat.seat_number)
                
            return redirect("payment_page")

            return render(request,"movies/seat_selection.html",{
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
    bookings = Booking.objects.filter(user=request.user,is_paid=False)

    if bookings.exists():
        bookings.update(is_paid = True)
        seat_numbers = []
        theater = None
        movie = None

        for booking in bookings:
            seat_numbers.append(booking.seat.seat_number)
            theater = booking.theater
            movie = booking.movie
        
            try:
                    resend.api_key=os.environ.get("RESEND_API_KEY")
                    resend.Emails.send({
                        "from": "BookMySeat<onboarding@resend.dev>",
                        "to": [request.user.email],
                        "subject": "Booking Confirmed🎫",
                        "html": f""" <h2>Booking Confirmed</h2>
                        <p>Hi {request.user.username},</p>
                        <p>Your payment was successful.</p>
                        <p><strong>Movie:</strong>{movie.name}</p>
                        <p><strong>Theater:</strong>{theater.name}</p>
                        <p><strong>Seats:</strong> {','.join(seat_numbers)}</p><br>
                        <p>Enjoy your show!</p>
                        <p>--BookMySeat Team</p>
                        """
                        })
            except Exception as e:
                        print("Resend email error:", e)    
                    
        

        return HttpResponse("Payment Success Working!!")





