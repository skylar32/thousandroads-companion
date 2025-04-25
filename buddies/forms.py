from django import forms
from buddies.models import Buddy

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