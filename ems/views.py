from ems.decorators import allowed_users
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from datetime import date
from .models import Registration, Event
from datetime import datetime
from django.http import JsonResponse



from .forms import *
from .decorators import *
from .models import *


# ------------------- #
#  Auth Functions #
# ------------------- #


def selection(request):
    return render(request, 'auth/selection.html')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            print(form.errors)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name='participant')
                user.groups.add(group)
                Participant.objects.create(
                    user=user,
                )
                messages.success(request, 'Account created for ' + username )
                return redirect('login')
        context = {
            'form': form
        }
        return render(request, 'auth/registerParticipant.html', context)


def registerPageOrganiser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            print(form.errors)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                group = Group.objects.get(name='organiser')
                user.groups.add(group)
                Organiser.objects.create(
                    user=user,
                )
                messages.success(request, 'Account created for ' + username )
                return redirect('login')
        context = {
            'form': form
        }
        return render(request, 'auth/registerOrganiser.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or password is incorrect')
        context = {}
        return render(request, 'auth/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


# ------------------- #
#  Render Functions #
# ------------------- #


def home(request):
    group = None
    if (request.user.groups.first() != None):
        group = request.user.groups.first().name
    if group == 'participant':
        if request.user.participant.name == None:
            print('Completing participant registration')
            return editProfileParticipant(request, request.user.participant.id)
    elif group == 'organiser':
        if request.user.organiser.name == None:
            print('Completing organiser registration')
            return editProfileOrganiser(request, request.user.organiser.id)
    advertised_events = [event.getEvent() for event in Advertisement.objects.all()[:4]]
    all_events = Event.objects.all()[:6]
    context = {
        'events': advertised_events,
        'all_events': all_events,
    }
    return render(request, 'ems/render/home.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'participant', 'organiser'])
def users(request):
    participants1 = Participant.objects.all()[0::2]
    participants2 = Participant.objects.all()[1::2]
    context = {
        'participants1': participants1,
        'participants2': participants2,
    }
    return render(request, 'ems/render/users.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'participant', 'organiser'])
def events(request):
    events1 = Event.objects.all()[0::2]
    events2 = Event.objects.all()[1::2]
    context = {
        'events1': events1,
        'events2': events2,
    }
    return render(request, 'ems/render/events.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'participant', 'organiser'])
def organisers(request):
    organisers1 = Organiser.objects.all()[0::2]
    organisers2 = Organiser.objects.all()[1::2]
    events_conducted = Event.objects.all().filter
    context = {
        'organisers1': organisers1,
        'organisers2': organisers2,
    }
    return render(request, 'ems/render/organisers.html', context)


@login_required(login_url='login')
def shippers(request):
    shippers = Shipper.objects.all().order_by('-id')
    context = {
        'shippers': shippers
    }
    return render(request, 'ems/render/shippers.html', context)


@login_required(login_url='login')
def shipments(request):
    shipments = Shipment.objects.all().order_by('-id')
    context = {
        'shipments': shipments
    }
    return render(request, 'ems/render/shipments.html', context)


@login_required(login_url='login')
def transactions(request):
    transactions = Transaction.objects.all().order_by('-id')
    context = {
        'transactions': transactions
    }
    return render(request, 'ems/render/transactions.html', context)


@login_required(login_url='login')
def registrations(request):
    registrations = Registration.objects.all().order_by('-id')
    context = {
        'registrations': registrations
    }
    return render(request, 'ems/render/registrations.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'participant', 'organiser'])
def store(request):
    items1 = Item.objects.all()[0::2]
    items2 = Item.objects.all()[1::2]
    context = {
        'items1': items1,
        'items2': items2,
    }
    return render(request, 'ems/render/store.html', context)


# ------------------- #
#  View Functions #
# ------------------- #


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'participant', 'organiser'])
def view_event(request, pk):
    event = Event.objects.get(id=pk)
    number_participants = Registration.objects.all().filter(event=event)
    merchandise = event.organiser.item_set.all()
    context = {
        'event': event,
        'merchandise': merchandise,
        'number_participants': len(number_participants)
    }
    return render(request, 'ems/view/event.html', context)


def view_user(request, pk):
    participant = Participant.objects.get(id=pk)
    events_participated = Registration.objects.all().filter(participant=participant)
    today = date.today()
    age = today.year - participant.dob.year - ((today.month, today.day) < (participant.dob.month, participant.dob.day))
    context = {
        'participant': participant,
        'events_participated': len(events_participated),
        'age': age

    }
    return render(request, 'ems/view/user.html', context)


@login_required
def my_events(request):
    user = request.user
    registrations = Registration.objects.filter(participant=user.participant, event__event_date__gte=datetime.now()).select_related('event')
    return render(request, 'ems/render/my_events.html', {'registrations': registrations})

# ------------------- #
#  Create Functions #
# ------------------- #


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'organiser'])
def createItem(request, pk):
    organiser = Organiser.objects.get(id=pk)
    form = ItemForm(initial={'organiser': organiser})
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')
    context = {
        'form': form
    }
    return render(request, 'forms/add_item.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'participant'])
def createTransaction(request, pk):
    participant = Participant.objects.get(id=pk)
    form = TransactionForm(initial={'participant': participant, 'date': str(date.today())})
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transactions')
    context = {
        'form': form
    }
    return render(request, 'forms/add_transaction.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createShipper(request):
    form = ShipperForm()
    if request.method == 'POST':
        form = ShipperForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shippers')
    context = {
        'form': form
    }
    return render(request, 'forms/add_shipper.html', context)


@allowed_users(allowed_roles=['admin', 'participant'])
def createRegistration(request, pk):
    participant = Participant.objects.get(id=pk)
    form = RegistrationForm(initial={'participant': participant})
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registrations')
    context = {
        'form': form
    }
    return render(request, 'forms/add_registration.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'organiser'])
def createShipment(request, pk):
    organiser = Organiser.objects.get(id=pk)
    form = ShipmentForm(initial={'organiser': organiser})
    if request.method == 'POST':
        form = ShipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shipments')
    context = {
        'form': form
    }
    return render(request, 'forms/add_shipment.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrganiser(request):
    form = OrganiserForm()
    if request.method == 'POST':
        form = OrganiserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('organisers')
    context = {
        'form': form
    }
    return render(request, 'forms/add_organiser.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'organiser'])
def createEvent(request, pk):
    organiser = Organiser.objects.get(id=pk)
    form = EventForm(initial={'organiser': organiser})
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events')
    context = {
        'form': form
    }
    return render(request, 'forms/add_event.html', context)


# ------------------- #
#  Edit Functions #
# ------------------- #


@login_required(login_url='login')
def editProfileParticipant(request, pk):
    participant = Participant.objects.get(id=pk)
    form = ParticipantForm(instance=participant)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, request.FILES, instance=participant)
        print('Form valid:', form.is_valid())
        print(form.errors)
        if form.is_valid():
            form.save()
            print(form)
            return redirect('home')
    context = {
        'participant': participant,
        'form': form
    }
    return render(request, 'ems/user_form.html', context)


@login_required(login_url='login')
def editProfileOrganiser(request, pk):
    organiser = Organiser.objects.get(id=pk)
    form = OrganiserForm(instance=organiser)
    if request.method == 'POST':
        form = OrganiserForm(request.POST, instance=organiser)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'organiser': organiser,
        'form': form
    }
    return render(request, 'ems/organiser_form.html', context)


def register_for_event(request, event_id):
    if request.user.is_authenticated and request.method == 'POST':
        user = request.user
        event_id = int(event_id)
        
        # Check if the user is not already registered for the event
        if not Registration.objects.filter(participant=user.participant, event_id=event_id).exists():
            # Create a new registration record
            Registration.objects.create(participant=user.participant, event_id=event_id)

            # You can add additional logic here if needed

            return JsonResponse({'success': True, 'message': 'Registration successful'})
        else:
            return JsonResponse({'success': False, 'message': 'You are already registered for this event'})

    return JsonResponse({'success': False, 'message': 'Invalid request'})


def my_events(request):
    user = request.user
    all_registrations = Registration.objects.filter(participant=user.participant).select_related('event')

    today = datetime.now().date()

    upcoming_events = all_registrations.filter(event__event_date__gte=today).order_by('event__event_date')
    done_events = all_registrations.filter(event__event_date__lt=today).order_by('-event__event_date')

    context = {
        'upcoming_events': upcoming_events,
        'done_events': done_events,
    }

    return render(request, 'ems/render/my_events.html', context)
