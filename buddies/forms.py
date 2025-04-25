from django import forms
from buddies.models import Buddy, PokemonSpecies


class BuddyCreationForm(forms.ModelForm):
    class Meta:
        model = Buddy
        fields = "name", "species", "gender", "fic"
        widgets = {
            "gender": forms.RadioSelect(
                choices=(
                    (None, "Genderless"),
                    (True, "Male"),
                    (False, "Female")
                )
            )
        }

    def __init__(self, *args, **kwargs):
        super(BuddyCreationForm, self).__init__(*args, **kwargs)
        self.fields["species"].queryset = PokemonSpecies.objects.filter(is_basic=True)