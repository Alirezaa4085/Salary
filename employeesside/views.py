from django.shortcuts import render, redirect, get_object_or_404
from account.models import UserProfile
from account.forms import UserProfileForm 
from django.http import JsonResponse




# This view is called 'Fill_Mycompany_form' and renders the template 'profile.html'
# with a queryset of UserProfile objects filtered by the current logged-in user.
# The current logged-in user is obtained from the request object.
# The queryset of UserProfile objects is then passed to the template as a context
# variable named 'user_profiles'.
def Fill_Mycompany_form(request):
    # get the current logged-in user
    current_user = request.user
    # filter the UserProfile queryset by the current logged-in user
    user_profiles = UserProfile.objects.filter(user=current_user)
    # render the template 'profile.html' with the queryset of UserProfile objects
    return render(request, 'profile.html', {'user_profiles': user_profiles})




# This view is called 'add_profile' and renders the template 'add_profile.html'
# with a form to add a new UserProfile instance.
# The form is populated with data from the request.
# If the form is valid, a new UserProfile instance is created with the data
# from the form and the user attribute set to the current logged-in user.
# The new UserProfile instance is then saved to the database.
# The view redirects to the 'Fill_Mycompany_form' view.
def add_profile(request):
    # If the request method is POST (i.e., a form has been submitted)
    if request.method == 'POST':
        # Instantiate a UserProfileForm with data from the request
        form = UserProfileForm(request.POST)
        # If the form is valid (i.e., all required fields are present and valid)
        if form.is_valid():
            # Get the current logged-in user
            user = request.user
            # Create a new UserProfile instance with data from the form
            profile = form.save(commit=False)
            # Set the user attribute of the new UserProfile instance to the current logged-in user
            profile.user = user
            # Save the new UserProfile instance to the database
            profile.save()
            # Redirect to the 'Fill_Mycompany_form' view
            return redirect('Fill_Mycompany_form')
    # If the request method is not POST, create a blank form
    else:
        form = UserProfileForm()
    # Render the template 'add_profile.html' with the form as a context variable
    return render(request, 'add_profile.html', {'form': form})

def edit_profile(request, pk):
    """This view retrieves a UserProfile object from the database based on
    the primary key (pk) passed in the URL by the user. It then instantiates
    a UserProfileForm with the retrieved UserProfile object as its instance
    argument. If the request method is POST and the form is valid, the form is
    saved to the database and the user is redirected to the 'Fill_Mycompany_form'
    view, otherwise the form is rendered with the template 'edit_profile.html'
    and the retrieved UserProfile object is passed as a context variable named
    'form'.
    """
    user_profile = UserProfile.objects.get(pk=pk)
    form = UserProfileForm(request.POST or None, instance=user_profile)
    if request.method == 'POST' and form.is_valid():
        """If the request method is POST and the form is valid,
        save the form to the database and redirect the user to
        the 'Fill_Mycompany_form' view.
        """
        form.save()
        return redirect('Fill_Mycompany_form')
    """If the request method is not POST or if the form is not valid,
    render the template 'edit_profile.html' with the retrieved
    UserProfile object as a context variable named 'form'.
    """
    return render(request, 'edit_profile.html', {'form': form})



def delete_profile(request, profile_id):
    """
    This view handles DELETE request to delete a user profile object.
    It deletes the object and returns a success message in JSON format.
    """
    if request.method == 'DELETE':
        # Check if profile_id is 1
        if profile_id == 1:
            return JsonResponse({'message': 'Deletion of default profile is not allowed.'}, status=400)
        
        # Retrieve the profile object
        profile = get_object_or_404(UserProfile, pk=profile_id)
        
        # Delete the profile object
        profile.delete()
        
        return JsonResponse({'message': 'Profile deleted successfully.'})
    else:
        return JsonResponse({'message': 'Invalid request method.'}, status=400)