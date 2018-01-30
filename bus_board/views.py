from django.shortcuts import render, redirect
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from .models import BusOrganisation, Route, Bus, Schedule, Ticket
from datetime import datetime, date
from .forms import TicketForm
import uuid
import phonenumbers
# from django.utils import urlencode

def home(request):
    '''
    view function for landing page
    '''
    return render(request, 'home.html')

def search_results(request):
    '''
    View function to get the the requested departure and arrival locations from the database and display to the user
    '''
    try:
        title = 'Result'

        if ('depature-location' in request.GET and request.GET['depature-location']) and ('arrival-location' in request.GET and request.GET['arrival-location']) and ('travel-date' in request.GET and request.GET['travel-date']):

            # Get the input departure
            search_departure_location = request.GET.get('depature-location').title()

            # Get the input arrival location
            search_arrival_location = request.GET.get('arrival-location').title()

            # Get the input date
            travel_date = request.GET.get('travel-date')

            # Convert string input to date type
            convert_to_date = datetime.strptime(travel_date, '%Y-%m-%d').date()

            # Get the route 
            result_route = Route.get_search_route(search_departure_location,search_arrival_location)

            # Check if route exists found
            if result_route != None :
                print(result_route.id)

                # Schedule with the same depature date
                schedule_with_depature_date = Schedule.get_departure_buses(convert_to_date, result_route.id)

                if len(schedule_with_depature_date) > 0:

                    for schedule in schedule_with_depature_date:

                        estimation_duration = Schedule.get_travel_estimation(schedule.id)

                    return render(request, 'search.html', {'title':title, 'search_departure_location':search_departure_location, 'search_arrival_location':search_arrival_location, 'convert_to_date':convert_to_date, 'buses':schedule_with_depature_date, 'estimation_duration':estimation_duration})

                else:
                    no_scheduled_bus_message = 'No scheduled buses'

                    return render(request, 'search.html', {'title':title, 'no_scheduled_bus_message':no_scheduled_bus_message, 'search_departure_location':search_departure_location, 'search_arrival_location':search_arrival_location, 'convert_to_date':convert_to_date})

        # Otherwise
        else:
            
            no_route_message = 'Bus route not found'

            return render(request, 'search.html', {'title':title, 'no_route_message':no_route_message, 'search_departure_location':search_departure_location, 'search_arrival_location':search_arrival_location, 'convert_to_date':convert_to_date})
    
    except ObjectDoesNotExist:

        return redirect(Http404)

def bus_details(request, bus_schedule_id):
    '''
    View function to display a form for the user to fill to get a ticket
    '''
    try:
        # args = {}

        selected_bus = Schedule.get_single_schedule(bus_schedule_id)

        title = f'{selected_bus.bus.bus_organisation} Schedule Details'

        if request.method == 'POST':
            
            form = TicketForm(request.POST)

            if form.is_valid():
                
                ticket = form.save(commit=False)

                ticket.schedule = selected_bus

                ticket.ticket_number = uuid.uuid4()

                ticket.save()

                ticket_id = ticket.id

                # return redirect('/ticket/' + str(ticket_id))
                return redirect(mobile_payment, ticket_id)

        else:

            form = TicketForm()

        # args['form'] = form

        return render(request, 'bus_details.html', {'title':title, 'form':form, 'selected_bus':selected_bus})

    except ObjectDoesNotExist:

         return redirect(Http404)

def mobile_payment(request, ticket_id):
    '''
    Function that carries out the payment process 
    '''
    # Get ticket with a given id 
    ticket = Ticket.get_single_ticket(ticket_id)

    print(ticket)
    
    #Specify your credentials
    # username = "Bus-board"
    # username = "sandbox"
    # apiKey   = "f50f85e67fa88fe5c30ba5f184dbd3d7c7bdef5e98440a183de19eb33cfbb6f5"

    #Create an instance of our awesome gateway class and pass your credentials
    # gateway = AfricasTalkingGateway(username, apiKey, "sandbox")

    #*************************************************************************************
    #  NOTE: If connecting to the sandbox:
    #
    #  1. Use "sandbox" as the username
    #  2. Use the apiKey generated from your sandbox application
    #     https://account.africastalking.com/apps/sandbox/settings/key
    #  3. Add the "sandbox" flag to the constructor
    #
    #  gateway = AfricasTalkingGateway(username, apiKey, "sandbox");
    #**************************************************************************************

    # Specify the name of your Africa's Talking payment product
    # productName  = "Nairobi-Nakuru"

    # The phone number of the customer checking out
    # phoneNumber  = "+2547283822478"

    # The 3-Letter ISO currency code for the checkout amount
    # currencyCode = "KES"

    # The checkout amount
    # amount = 2.00

    # Any metadata that you would like to send along with this request
    # This metadata will be  included when we send back the final payment notification
    # metadata = {"agentId"   : "654",
    #             "productId" : "321"}
    # try:
        # Initiate the checkout. If successful, you will get back a transactionId
        # transactionId = gateway.initiateMobilePaymentCheckout(
        # productName,
        # phoneNumber,
        # currencyCode,
        # amount,
        # metadata)
        # print "The transactionId is " + transactionId
        
    # except AfricasTalkingGatewayException, e:
    #     print "Received error response: %s" % str(e)

