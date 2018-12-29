from django.db import models
from django.conf import settings


class Deck(models.Model):
    name = models.CharField(max_length=20, default='deck')

    @staticmethod
    def create_instance():
        deck = Deck()
        deck.save()
        for choice, name in Card.CARD_CHOICES:
            for i in range(3):
                card = Card(suit=choice, deck=deck, user=None)
                card.save()
        deck.save()

    def draw_card(deck):
        available_cards = deck.card_set.filter(user=None).order_by('?')
        return available_cards.first()


class Card(models.Model):
    DUKE = 'DU'
    CONTESSA = 'CO'
    AMBASSADOR = 'AM'
    CAPTAIN = 'CP'
    ASSASSIN = 'AS'
    CARD_CHOICES = (
        (DUKE, 'Duke'),
        (CONTESSA, 'Contessa'),
        (AMBASSADOR, 'Ambassador'),
        (CAPTAIN, 'Captain'),
        (ASSASSIN, 'Assassin'),
    )
    suit = models.CharField(max_length=2,
                            help_text='Enter the card name',
                            choices=CARD_CHOICES,
                            default=DUKE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    deck = models.ForeignKey(
        'Deck',
        on_delete=models.CASCADE,
    )
    revealed = models.BooleanField(default=False)

    def __str__(self):
        return '%s %s %s' % (self.get_suit_display(), self.pk, self.user)
