from __future__ import annotations

import typing

import randovania.game.data
import randovania.game.development_state
import randovania.game.generator
import randovania.game.gui
import randovania.game.layout
from randovania.games.prime3.layout.corruption_configuration import CorruptionConfiguration
from randovania.games.prime3.layout.corruption_cosmetic_patches import CorruptionCosmeticPatches
from randovania.games.prime3.layout.preset_describer import CorruptionPresetDescriber

if typing.TYPE_CHECKING:
    from randovania.exporter.game_exporter import GameExporter
    from randovania.exporter.patch_data_factory import PatchDataFactory
    from randovania.interface_common.options import PerGameOptions


def _options() -> type[PerGameOptions]:
    from randovania.games.prime3.exporter.options import CorruptionPerGameOptions

    return CorruptionPerGameOptions


def _gui() -> randovania.game.gui.GameGui:
    from randovania.games.prime3 import gui
    from randovania.games.prime3.layout import progressive_items

    return randovania.game.gui.GameGui(
        tab_provider=gui.prime3_preset_tabs,
        cosmetic_dialog=gui.CorruptionCosmeticPatchesDialog,
        export_dialog=gui.CorruptionGameExportDialog,
        progressive_item_gui_tuples=progressive_items.tuples(),
        game_tab=gui.CorruptionGameTabWidget,
    )


def _generator() -> randovania.game.generator.GameGenerator:
    from randovania.games.prime3.generator.bootstrap import CorruptionBootstrap
    from randovania.games.prime3.generator.pickup_pool.pool_creator import corruption_specific_pool
    from randovania.generator.base_patches_factory import BasePatchesFactory
    from randovania.generator.filler.weights import ActionWeights
    from randovania.generator.hint_distributor import AllJokesHintDistributor

    return randovania.game.generator.GameGenerator(
        pickup_pool_creator=corruption_specific_pool,
        bootstrap=CorruptionBootstrap(),
        base_patches_factory=BasePatchesFactory(),
        hint_distributor=AllJokesHintDistributor(),
        action_weights=ActionWeights(),
    )


def _patch_data_factory() -> type[PatchDataFactory]:
    from randovania.games.prime3.exporter.patch_data_factory import CorruptionPatchDataFactory

    return CorruptionPatchDataFactory


def _exporter() -> GameExporter:
    from randovania.games.prime3.exporter.game_exporter import CorruptionGameExporter

    return CorruptionGameExporter()


def _hash_words() -> list[str]:
    from randovania.games.blank.hash_words import HASH_WORDS

    return HASH_WORDS


game_data: randovania.game.data.GameData = randovania.game.data.GameData(
    short_name="Corruption",
    long_name="Metroid Prime 3: Corruption",
    development_state=randovania.game.development_state.DevelopmentState.DEVELOPMENT,
    presets=[{"path": "starter_preset.rdvpreset"}],
    faq=[
        (
            "What causes the Hypermode vines in Corrupted Pool to disappear?",
            "Collecting the ship item in Hangar Bay removes the vines.",
        ),
        (
            "While fighting Rundas, the game lags and there are pirates and turrets in the way. What causes this?",
            "If you collect the ship item in Hangar Bay before fighting Rundas,"
            " both Rundas and the pirate layers will be active at the same time.",
        ),
        (
            "I have Ship Missiles but I am unable to break the wall in Ancient Courtyard.",
            "To break the wall, you must have the Main Ship Missiles in your inventory.",
        ),
        (
            "The item in Gearworks is blocked off. How do I collect it?",
            "Collecting the item in SkyTown Federation Landing Site unlocks access to the item.",
        ),
        (
            "I don't have Command Visor. Can I still collect the items from the landing sites?",
            "You can fly to either unlocked landing site from an already active one to collect the item.",
        ),
    ],
    hash_words=_hash_words(),
    layout=randovania.game.layout.GameLayout(
        configuration=CorruptionConfiguration,
        cosmetic_patches=CorruptionCosmeticPatches,
        preset_describer=CorruptionPresetDescriber(),
    ),
    options=_options,
    gui=_gui,
    generator=_generator,
    patch_data_factory=_patch_data_factory,
    exporter=_exporter,
)
