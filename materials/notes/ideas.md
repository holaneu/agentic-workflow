
# -----------------------------------
# TODOs / Feature ideas
# -----------------------------------

file storage file structure
  - user/<user id>/files/<file path>
  - for testing purpose the user id will be some fixed string (e.g. vlada), later, once the use login system will be implemented, the user id will be id of the user from user DB (some kind of hash or dynamicaly generated id etc.).

list of items (files, databases)
  - page for listing
  - page for item detail

structured output - json schema
  - openai
  - gemini
  - mistral

search_web_google(query)

integrate github repo commit/push
commit_to_github()
fetch_from_github()

download_youtube_video_transcript()

download_youtube_video()

convert_markdown_to_html()

convert_html_to_markdown()

save_as_printable_html()

I have an assistant "generate questions" – an idea for a workflow – after the step of generating questions on a certain topic, take these questions, possibly also attach the original prompt for generating the questions (or its summarized version) at the beginning for context, and ask for the generation of another X questions.

assistents
generate file name
generate title

convert yaml to json

generate date in format YYYY-MM-DD

analyze text - extract action steps

run sellenium py code

generate standalone self-contained SPA web page (similar to Claude's artifact)

comment on topic

analyze text - semantic analysis

generate py code

execute py code

synonyms

UI - conversation message 
  - button "Use as an input"
  - button "Add to database"
  - button "Save as file" (markdown)

UI - file attachments (documents, text files, images, sound files?)

integrate openai whisper api

integrate elevenLabs api

render markdown within UI, in "response section"

vlastni dat. struktura (pro konverzace, workflows, assistanty atd.), prenos dat/zprav mezi funkcemi (input/output), cast z toho pouzitelne pro logovani, zpetne pujde (ulozene do souboru) prochazet a filtrovat, vyhledavat, analyzovat.

logging of workflows
  - own json data structure for workflow

integrate antropic api

integrate llama api

integrate deepseek api

workflow: story_writing
  input
  create criteria (assistant: story criteria creator)
  write story based on criteria (assistant: writer)
  check content and provide feedback to writer (assistant: content editor)
  update story based on feedback from content editor (assistant: writer)
  read story and provide feedback to writer (assistant: ctitical reader)
  update story based on feedback from critical reader (assistant: writer)
  final output

classify input

self-development
  pick topics for a day

diary

projects / tasks
  create task item
  generate action-steps
  categorize task under project
  update task (status)

publish post to web / blog

email
  get new email
  read single email
  send email

news
  get news and filter topic
  read single news
