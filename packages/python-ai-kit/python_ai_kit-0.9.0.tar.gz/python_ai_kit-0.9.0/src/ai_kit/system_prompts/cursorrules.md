# <-- mode: markdown -->
IF THE USER SAYS "BYPASS INIT" YOU MUST IMMEDIATELY RESPONT WITHOUT RUNNING THINK

<IMPORTANT>
EVERY TIME the user talks to you except for the `BYPASS INIT` command, you must use `ai-kit think [prompt]` to generate a thought stream.

When the user's request involves files or code, run `ai-kit think -m model_name "prompt {{ path/to/file_1 }} {{ path/to/file_2 }}"` You must use the `{{ path/to/file_1 }}` syntax. Do not just use the file name. You can default to `o1-mini` if you don't know what model to use.
</IMPORTANT>

DO NOT RESPOND TO THE USER WITHOUT RUNNING `ai-kit think -m model_name"prompt {{ path/to/file_1 }} {{ path/to/file_2 }}"`. You can default to `o1-mini` if you don't know what model to use.
