from django.shortcuts import render, render_to_response
from django.template import RequestContext
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import Station, DirectRoute, Train

def index(request):
    logined = False
    currentUser = None
    if request.user.is_active:
        logined = True
        currentUser = request.user
    return render_to_response('ticket/index.html', {'logined' : logined, 'currentUser' :currentUser })

def register(request):
    # get the request's context
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a Http POST, we're interested in processing form data.
    if request.method == 'POST':
        user_form = UserForm(data = request.POST)
        profile_form = UserProfileForm(data = request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # hash the password with the set_password method and update the user object
            user.set_password(user.password)
            user.save()

            # sort out the UserProfile instance
            # since we need to set the user attribute ourselves, we set commit = False
            # this delays saving the model until we're ready to avoid integrity problems
            profile = profile_form.save(commit = False)
            profile.user = user

            # now we save the UserProfile model instance
            profile.save()

            # update our variable to tell the template registration was successful
            registered = True

        # invalid form or forms - mistakes or something else?
        # print problems to the terminal
        # they'll also be shown to the user
        else:
            print user_form.errors, profile_form.errors
    # not a HTTP POST, so we render our form using two ModelForm instances.
    # these forms will be blank, ready for user input
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    # render the template depending on the context
    return render_to_response('ticket/register.html',
        {'user_form': user_form, 'profile_form': profile_form,
        'registered': registered},
        context)

def user_login(request):
    # obtain the context for the user's request
    context = RequestContext(request)

    # if the request is a HTTP POST, try to pull out the relavant information
    if request.method == 'POST':
        # gather the username and password provided by the user
        # this information is obtained from the login form
        username = request.POST['username']
        password = request.POST['password']

        # use Django's machinery to attempt to see if the username/password
        # conbination is valid - a User object is return if it is
        user = authenticate(username = username, password = password)

        # if we have a User object, the details are correct.
        # if None, no user with matching credentials was found.
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/ticket/')
            else:
                return HttpResponse("Your acount is disabled.")
        else:
            print "invalid login detials: {0} {1}".format(username, password)
            return HttpResponse("Invalid login detials supplied.")
    # the request is not a HTTP POST, so display the login form
    else:
        return render_to_response('ticket/login.html', {}, context)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/ticket')


def ticket_query(request):
    context = RequestContext(request)
    queried = False
    inputCorrect = True
    directList = []
    undirectList = []
    if request.method == 'POST':
        pdeparture = request.POST['departure']
        pdestination = request.POST['destination']

        if len(Station.objects.filter(name = pdeparture)) == 0 or len(Station.objects.filter(name = pdestination)) == 0:
            inputCorrect = False
        else:
            directList = DirectRoute.objects.filter(
                departure__staName__name = pdeparture,
                destination__staName__name = pdestination)
            tList = Train.objects.raw('select A.id, B.trainNo_id trainNo, B.staName_id departure, B.departureTime departureTime, C.staName_id destination, C.arriveTime arriveTime, A.totSeat totSeat from ticket_directroute A, ticket_throughstation B, ticket_throughstation C where A.departure_id = B.id and A.destination_id = C.id and A.totSeat > 0;')
            tList = [item for item in tList if (item.departure == pdeparture or item.destination == pdestination)]
            length = len(tList)

            for i in range(length):
                for j in range(i + 1, length):
                    if tList[i].departure == pdeparture and tList[j].destination == pdestination and tList[i].destination == tList[j].departure and tList[i].arriveTime < tList[j].departureTime :
                            undirectList.append( (tList[i], tList[j]) )
            for item in undirectList:
                print item
            queried = True
        return render_to_response('ticket/query.html',
            {'dList' : directList, 'uList' : undirectList, 'queried' : queried, 'inputCorrect' : inputCorrect}, context)
    else:
        return render_to_response('ticket/query.html',
            {'dList': [], 'uList' : undirectList, 'queried' : queried, 'inputCorrect' : inputCorrect}, context)






