from django.db import models
from forum.models import Fic, Member
from django.utils.translation import gettext_lazy as _


class PokemonSpecies(models.Model):
    class Gender(models.IntegerChoices):
        NULL = 0, _("Genderless")
        MALE = 1, _("Always male")
        FEMALE = 2, _("Always female")
        BOTH = 3, _("Male or female")

        @classmethod
        def get_from_ratio(cls, g: int) -> "PokemonSpecies.Gender":
            if g < 0:
                return cls.NULL
            elif g == 0:
                return cls.MALE
            elif g == 255:
                return cls.FEMALE
            else:
                return cls.BOTH

    name = models.CharField(max_length=32)
    dex_no = models.PositiveSmallIntegerField()
    gender = models.PositiveSmallIntegerField(choices=Gender.choices)

    def __repr__(self):
        return f'<PokemonSpecies: #{str(self.dex_no).zfill(4)} {self.name}>'

class PokemonEvolution(models.Model):
    class EvolutionMethod(models.IntegerChoices):
        LEVEL = 0, _("Level-up")
        FRIENDSHIP = 1, _("High friendship")
        TRADE = 2, _("Trade")
        ITEM = 3, _("Use item")
    base_form = models.ForeignKey(PokemonSpecies, on_delete=models.CASCADE, related_name="evolutions")
    evolved_form = models.ForeignKey(PokemonSpecies, on_delete=models.CASCADE)
    method = models.PositiveSmallIntegerField(choices=EvolutionMethod.choices)
    level = models.PositiveSmallIntegerField(null=True, default=None)

class Buddy(models.Model):
    name = models.CharField(max_length=50, help_text="A nickname for your writing buddy.")
    species = models.ForeignKey(
        PokemonSpecies, on_delete=models.CASCADE,help_text="The Pokémon species for your writing buddy."
    )
    gender = models.BooleanField(null=True, blank=True, help_text="The gender for your writing buddy.")
    xp = models.PositiveIntegerField(default=0)
    fic = models.OneToOneField(Fic, on_delete=models.CASCADE)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.species}"