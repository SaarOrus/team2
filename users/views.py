from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from event.models import Event, UserEvent


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    events = Event.manager.all()
    user_events = UserEvent.objects.filter(userID=request.user.profile.id)
    events = [user_event.eventID for user_event in user_events]
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'events': events,
        'user_id': request.user.id
    }

    return render(request, 'users/profile.html', context)
