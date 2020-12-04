from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views import generic
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError

from .models import Suggestions, Comment, UserProfile, Post, Category, Favorite
from django.contrib.auth.models import User

from django.conf import settings
from django.contrib.auth import logout
# Create your views here.


class IndexView(generic.TemplateView):
    template_name = 'home/index.html'

def accounts_view(request):
        return render(request, "accounts.html")


def categories(request):
    catgories = list(Category.objects.all())
    return render(request, "categories.html", {'catgories': catgories})


def singleCategory(request, categorySlug):
    get_category = Category.objects.get(slug=categorySlug)
    posts = list(Post.objects.filter(category=get_category))
    
    return render(request, "posts.html", {'posts': posts, 'category': get_category})


def comment(request, categorySlug, postSlug):
    get_category = Category.objects.get(slug=categorySlug)
    post = Post.objects.get(slug=postSlug)
    comments = list(Comment.objects.filter(post=post))

    return render(request, "comment.html", {'post': post, 'comments': comments, 'category': get_category})


def postComment(request):
    data_in = request.POST.copy()
    post = data_in['post']
    name = data_in['name']
    comments = data_in['comments']

    print("Debug:", post, name, comments)
    comment_model = Comment()
    comment_model.post = Post.objects.get(id=post)
    comment_model.author = name
    comment_model.text = comments
    comment_model.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def myProfile(request):
    data = {}
    data['first_name'] = request.user.first_name
    data['last_name'] = request.user.last_name
    data['email'] = request.user.email
    # IF USER HAS USER PROFILE MADE, pull from that data
    try:
        profile = UserProfile.objects.get(user=request.user)
        data['email'] = profile.my_email
        data['first_name'] = profile.my_first_name
        data['last_name'] = profile.my_last_name
        data['phone'] = profile.phone
        data['address'] = profile.address
        data['city'] = profile.city
        data['state'] = profile.state
        data['zip_code'] = profile.zip_code
        favorites = Favorite.objects.filter(user=profile)
        data['favorites'] = []
        for fav in favorites:
            if fav not in data['favorites']:
                data['favorites'].append(fav.name)

    # If user does not have user profile made, pull from the standard user data

    except UserProfile.DoesNotExist:  # change to extend exception?
        data['email'] = request.user.email
        data['first_name'] = request.user.first_name
        data['last_name'] = request.user.last_name

    data['categories'] = list(Category.objects.all())
    return render(request, "my-profile.html", data)



def myProfileAction(request):

    # Take in the data from the button press
    data_in = request.POST.copy()

    # If the profile has been made, get the objects from the profile
    try:
        new_profile = UserProfile.objects.get(user=request.user)

    # If the profile has not been made, create a new profile that extends the default user
    # profile from the authentication
    except UserProfile.DoesNotExist:
        new_profile = UserProfile()  # Create new user profile
        new_profile.user = User.objects.get(id=request.user.id)  # Populate user field with extension from default user

    # NOTE: the following will only save phone number, not the other stuff; will figure out how to do that later
    new_profile.my_first_name = data_in['first_name']  # Save inputted first name in the my_first_name field
    new_profile.my_last_name = data_in['last_name']  # Save inputted last name in the my_last_name field
    new_profile.my_email = data_in['email']  # Save inputted email in the my_email field
    new_profile.phone = data_in['phone']  # Save inputted phone number in the phone field
    new_profile.address = data_in['address'] # Save inputs about address
    new_profile.city = data_in['city']  # Save inputs about City
    new_profile.state = data_in['state']  # Save inputs about State
    new_profile.zip_code = data_in['zip_code']  # Save inputs about address

    # To check for favorites, first get all of the favorites data from the form
    favorites_form = request.POST.getlist('favorites[]')

    # We want to delete all previous favorites first. Filter by current user profile, and delete all of the favorites
    # associated with that user.
    Favorite.objects.filter(user=UserProfile.objects.get(user=request.user)).delete()

    # Now, we want to add in all of the favorites the user has chosen.
    for fav in favorites_form:
        new_fav = Favorite()
        new_fav.name = fav
        new_fav.user = new_profile
        new_fav.save() # Make sure to save each favorite

    new_profile.save()  # Save changes made to the UserProfile

    return redirect('/')

def contact_form(request):
    email = request.user.email
    first_name = request.user.first_name
    last_name = request.user.last_name
    form = ContactForm(initial={'email': email, 'name': first_name + ' ' + last_name})
    text = request.GET.get('text', '')
    text = 'To whom it may concern, name is '+ first_name + ' ' + last_name+'.'+'\n\n\b'+text+'\n\nSincerely, \n'+ first_name + ' ' + last_name
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f'Civic Connect Message from: {form.cleaned_data["name"]}'
            dataIn = request.POST.copy()
            message = dataIn["message"]
            sender = ("hondacivicsuva@gmail.com")
            recipient_email = dataIn["recipient_email"]
            recipients = [recipient_email]
            try:
                send_mail(subject, message, sender, recipients, fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return redirect("/thankyou/")
    return render(request, "contact.html", {'form': form, 'text': text})


# Contact From/ Sendgrid template taken from: https://github.com/the-kodechamp/django_blog_tutorial/blob/master/blog/templates

def feedback(request):
    categories_list = list(Category.objects.all())

    if request.method == "POST":
        contact = Suggestions()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        contact.name = name
        contact.email = email
        contact.subject = subject
        contact.message = message
        contact.save()
        return redirect("/thankyou/")
    return render(request, 'feedback.html', {'categories': categories_list})

def thankyou(request):
    return render(request, "thankyou.html")


def logout_view(request):
    logout(request)
    return render(request, "logout.html")

def generate(request):
    email = request.user.email
    first_name = request.user.first_name
    last_name = request.user.last_name

    text = request.GET.get('text', '')
    text = 'To whom it may concern, name is '+ first_name + ' ' + last_name+'.'+'\n\n\b'+text+'\n\nSincerely, \n'+ first_name + ' ' + last_name
    if request.method == 'POSTED':
        if form.is_valid():
            dataIn = request.POSTED.copy()
            message = dataIn["message"]
            try:
                send_mail(subject, message, fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            return redirect("/thankyou/")
    return render(request, "generate.html", { 'text': text})   