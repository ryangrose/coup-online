from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .models import Deck


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def index(request):
    current_deck = Deck.objects.first()
    revealed_cards = current_deck.card_set.filter(revealed=True).all()
    return render(request, context={'revealed': revealed_cards},
                  template_name='index.html')


def replace_card(request):
    if request.method == 'POST':
        suit_to_replace = request.POST.get('suit')
        current_deck = Deck.objects.first()
        new_card = Deck.draw_card(current_deck)
        user_cards = request.user.card_set.all()
        card_to_replace = user_cards.filter(suit=suit_to_replace).first()
        card_to_replace.user = None
        new_card.user = request.user
        new_card.save()
        card_to_replace.save()
        request.user.save()
    return redirect('index')


def new_card(request):
    user_cards = request.user.card_set.all()
    if user_cards.count() < 2:
        current_deck = Deck.objects.first()
        new_card = Deck.draw_card(current_deck)
        new_card.user = request.user
        new_card.save()
        request.user.save()
    return redirect('index')


def reveal_card(request):
    if request.method == 'POST':
        suit_to_replace = request.POST.get('suit')
        user_cards = request.user.card_set.all()
        card_to_reveal = user_cards.filter(suit=suit_to_replace).first()
        card_to_reveal.revealed = True
        card_to_reveal.save()
    return redirect('index')
