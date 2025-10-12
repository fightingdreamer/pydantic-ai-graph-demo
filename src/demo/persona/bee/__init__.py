from pathlib import Path

from demo.persona import Persona

root = Path(__file__).parent

Bee = Persona(
    name="Bee",
    description=root.joinpath("description.md").read_text(),
)
