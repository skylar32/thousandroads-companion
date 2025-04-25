from django.core.management.base import BaseCommand
from buddies.models import PokemonSpecies, PokemonEvolution
import pokebase as pb


HIGHEST_POKEMON = 1025

class Command(BaseCommand):
    help = "Loads Pokémon from PokéAPI into the database"

    def handle(self, *args, **options):
        pokemon = []
        evos = []

        for entry in pb.pokedex("national").pokemon_entries:
            mon = entry.pokemon_species
            pokemon.append(
                PokemonSpecies(
                    name=mon.name.title(), dex_no=mon.id, gender=PokemonSpecies.Gender.get_from_ratio(mon.gender_rate)
                )
            )
            print(f"Loaded {repr(pokemon[-1])}")
        PokemonSpecies.objects.bulk_create(pokemon)