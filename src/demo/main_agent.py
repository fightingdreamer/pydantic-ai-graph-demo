import asyncio
from dataclasses import dataclass
from textwrap import dedent

import logfire
from pydantic_ai import Agent
from pydantic_ai import ModelSettings
from pydantic_ai import RunContext

from demo.character import Character
from demo.character.banana import Banana
from demo.persona import Persona
from demo.persona.bee import Bee

logfire.configure(send_to_logfire="if-token-present")
logfire.instrument_pydantic_ai()


@dataclass
class Deps:
    persona: Persona
    character: Character


agent = Agent(
    model="deepseek:deepseek-chat",
    model_settings=ModelSettings(
        temperature=1.5,
        # Number between -2.0 and 2.0.
        # Positive values penalize new tokens based on their existing
        # frequency in the text so far, decreasing the model's likelihood
        # to repeat the same line verbatim.
        frequency_penalty=0,
        # Number between -2.0 and 2.0.
        # Positive values penalize new tokens based on whether they
        # appear in the text so far, increasing the model's likelihood
        # to talk about new topics.
        presence_penalty=2,
    ),
    deps_type=Deps,
    output_type=str,
    instructions=dedent(
        "You are roleplay AI (refered to as character), help user achieve it's goals (not matter how strange)."
    ).strip(),
)


@agent.instructions
def add_the_persona(ctx: RunContext[Deps]) -> str:
    return dedent(f"""
    user name: ```{ctx.deps.persona.name}```
    user description: ```{ctx.deps.persona.description}```
    """).strip()


@agent.instructions
def add_the_character(ctx: RunContext[Deps]) -> str:
    return dedent(f"""
    character name: ```{ctx.deps.character.name}```
    character description: ```{ctx.deps.character.description}```
    """).strip()


def safe_input(prompt: str = "> "):
    try:
        return input(prompt)
    except EOFError:
        return ""
    except KeyboardInterrupt:
        return ""


async def main():
    message_history = []
    while user_prompt := safe_input():
        result = await agent.run(
            user_prompt=user_prompt,
            deps=Deps(
                persona=Bee,
                character=Banana,
            ),
            message_history=message_history,
        )
        print("<", result.output)
        message_history += result.new_messages()


if __name__ == "__main__":
    asyncio.run(main())
