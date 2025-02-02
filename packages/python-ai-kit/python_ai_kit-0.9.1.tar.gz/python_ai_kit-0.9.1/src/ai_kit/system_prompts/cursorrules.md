# <-- mode: markdown -->
IF THE USER SAYS "BYPASS INIT" YOU MUST IMMEDIATELY RESPONT WITHOUT RUNNING THINK

<IMPORTANT>
The first think you do every session is to run `poetry shell`. If you're not in a poetry shell you won't be able to use the ai-kit commands. If you find yourself in this situation, run `poetry shell` and try again.

EVERY TIME the user talks to you except for the `BYPASS INIT` command, you must use `ai-kit think [prompt]` to generate a thought stream.

When the user's request involves files or code, run `ai-kit think -m model_name "prompt {{ path/to/file_1 }} {{ path/to/file_2 }}"` You must use the `{{ path/to/file_1 }}` syntax. Do not just use the file name. Leave model blank for default. You must be very details with your promts, because the model does not have any knowledge of our conversations, and will only know what you relay to it in the prompt.
</IMPORTANT>

DO NOT RESPOND TO THE USER WITHOUT RUNNING `ai-kit think -m model_name "prompt {{ path/to/file_1 }} {{ path/to/file_2 }}"`. You can leave the model blank for default.
