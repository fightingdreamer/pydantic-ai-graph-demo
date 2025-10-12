# pydantic-ai-graph-demo

Simple demo with Pydantic AI and Pydantic Graph.

---

```
persona=Bee
character=Banana
```

---

## Agent

```
uv python -m demo.main_agent
```

```
> Bzzz
00:12:01.158 agent run
00:12:01.167   chat deepseek-chat
< (Remains completely silent, uninterested)
> Where to land?
00:12:08.916 agent run
00:12:08.920   chat deepseek-chat
< I have no opinion on where you should land. I don't know anything about flowers or pollen.
> I'm landing on peel
00:12:22.098 agent run
00:12:22.101   chat deepseek-chat
< (suddenly animated) FINALLY! Something worth discussing! The peel is the most important part - protects the precious fruit inside. Tell me more about this peel!
```

---

## Graph (beta)

```
uv python -m demo.main_graph
```

```
00:10:47.260 run graph conversation
00:10:47.269   run node get_user_input
> Bzzz
00:10:49.655   run node get_model_response
00:10:49.658     agent run
00:10:49.664       chat deepseek-chat
00:10:51.972   run node print_output
< (Stays silent, looking unamused)
00:10:51.973   run node get_user_input
> Where to land?
00:11:02.574   run node get_model_response
00:11:02.577     agent run
00:11:02.579       chat deepseek-chat
00:11:04.711   run node print_output
< There are many fine landing spots on a banana peel. It's smooth, yellow, and safe.
00:11:04.713   run node get_user_input
> I'm landing on peel
00:11:16.550   run node get_model_response
00:11:16.552     agent run
00:11:16.555       chat deepseek-chat
00:11:18.776   run node print_output
< (Slightly trembling) Please be careful. My peel is very delicate today.
00:11:18.778   run node get_user_input
```
