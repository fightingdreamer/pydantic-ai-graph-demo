import asyncio
from dataclasses import dataclass
from dataclasses import field
from textwrap import dedent

import logfire
from pydantic_ai import Agent
from pydantic_ai import ModelMessage
from pydantic_ai import ModelSettings
from pydantic_ai import RunContext
from pydantic_graph import End
from pydantic_graph.beta import GraphBuilder
from pydantic_graph.beta import StepContext

from demo.character import Character
from demo.character.banana import Banana
from demo.persona import Persona
from demo.persona.bee import Bee

logfire.configure(send_to_logfire="if-token-present")
logfire.instrument_pydantic_ai()


@dataclass
class State:
    all_messages: list[ModelMessage] = field(default_factory=list[ModelMessage])


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


g = GraphBuilder(
    name="conversation",
    state_type=State,
    deps_type=Deps,
    output_type=End,
)


@g.step
async def get_user_input(ctx: StepContext[State, Deps, None]) -> str | End:
    _ = ctx
    try:
        return input("> ")
    except (EOFError, KeyboardInterrupt):
        return End(None)


@g.step
async def get_model_response(ctx: StepContext[State, Deps, str]) -> str:
    result = await agent.run(
        user_prompt=ctx.inputs,
        deps=ctx.deps,
        message_history=ctx.state.all_messages,
    )
    new_messages = result.new_messages()
    ctx.state.all_messages.extend(new_messages)
    return result.output


@g.step
async def print_output(ctx: StepContext[State, Deps, str]) -> None:
    print("<", ctx.inputs)


g.add(
    g.edge_from(g.start_node).to(get_user_input),
    g.edge_from(get_user_input).to(
        g.decision()
        .branch(g.match(End).to(g.end_node))
        .branch(g.match(str).to(get_model_response)),
    ),
    g.edge_from(get_model_response).to(print_output),
    g.edge_from(print_output).to(get_user_input),
)

graph = g.build()


async def main():
    state = State()
    deps = Deps(
        persona=Bee,
        character=Banana,
    )
    await graph.run(state=state, deps=deps)


if __name__ == "__main__":
    asyncio.run(main())
