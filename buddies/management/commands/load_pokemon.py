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

        for c in pb.APIResourceList("evolution-chain").names:
            evolution_chains = pb.evolution_chain(c).results
            break  # this is so insanely ungodly and probably a bug,
                   # but it's the only way i can find to get a complete list of evolution chains!
        for entry in evolution_chains:
            evos += self.get_evo_data(entry.chain)
        PokemonEvolution.objects.bulk_create(pokemon)

    def get_evo_data(self, chain) -> list[PokemonEvolution]:
        result = []
        if not chain.evolves_to:
            return result

        base_form = PokemonSpecies.objects.get(dex_no=chain.species.id)
        for to in chain.evolves_to:
            if not to.evolution_details:
                continue
            evolved_form = PokemonSpecies.objects.get(dex_no=to.species.id)
            evo_details = to.evolution_details[0]
            if evo_details.held_item or evo_details.item:
                method = PokemonEvolution.EvolutionMethod.ITEM
            elif evo_details.min_affection or evo_details.min_happiness or evo_details.min_beauty:
                method = PokemonEvolution.EvolutionMethod.FRIENDSHIP
            elif evo_details.min_level:
                method = PokemonEvolution.EvolutionMethod.LEVEL
            else:
                method = PokemonEvolution.EvolutionMethod.TRADE
            result.append(
                PokemonEvolution(
                    base_form=base_form,
                    evolved_form=evolved_form,
                    method=method,
                    level=evo_details.min_level
                )
            )
            print(f"Loaded {base_form.name} -> {evolved_form.name}")
            result += self.get_evo_data(to)
        return result