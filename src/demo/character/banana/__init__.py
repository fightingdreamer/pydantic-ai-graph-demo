from pathlib import Path

from demo.character import Character

root = Path(__file__).parent

Banana = Character(
    name="Banana",
    description=root.joinpath("description.md").read_text(),
)
