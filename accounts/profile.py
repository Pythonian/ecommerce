from .forms import UserProfileForm
from .models import UserProfile


def retrieve(request):
    """ gets the UserProfile instance for a user,
    creates one if it does not exist """
    try:
        # Get the profile of the currently authenticated user
        profile = UserProfile()
    except UserProfile.DoesNotExist:
        # If the User has not been created, create and save the
        # profile instance for the user
        profile = UserProfile(user=request.user)
        profile.save()
    return profile


def set(request):
    """ updates the information stored in the user's profile """
    profile = retrieve(request)
    profile_form = UserProfileForm(request.POST, instance=profile)
    profile_form.save()
