asistenti:
- analyzuj tento clanek a napis jeho zobecnenou (obecnou) charakteristiku. Cil je v nekolika bodech popsat styl, tema, delku, ton clanku.
  - priklad vystupu:
    - tema:
    - styl:
    - ton:
    - delka:
    - mira odbornosti: <cislene skore odbornosti od 1 do 10 kde 10 je nejvice odborne>
- synonyma
- na zklade zdroje napis X otazek, ktere se ptaji na podstatne informace uvedene ve zdroji. 
  - Priklad zdroje: V ceske republice je hodne rek. Nejdelsi reka CR je Vltava. Nejvyznamenjsi pritoky reky Vltavy jsou Berounka a Sazava. Vltava se vleva do reky Labe ve meste Melnik.
  - Priklady otazek: Jake je nejdelsi reka v CR? Jake jsou nejvyznamnejsi pritoky Vltaby? Do jake reky se vleva Vltava? Ve kterm meste se nachazi soutok Vltavy a Labe?

Pridat "Run tool" nebo "Run assistant" - zjednoduseni - nemusim vytvaret workflow pro testovani toolu nebo asistenta, zaroven se to muze hodit, kdyz chci rychle ziskat nejaky vystup bez aplikace komplexnejsiho workflow.

UI - Pod nebo k sekci vystupu pridat tlacitko "Use as an input"

UI - file attachments (documents, text files, images, sound files?)

integrate some OCR functions

integrate openai whisper api

integrate github repo commit/push

integrate eleven labs api

render markdown within UI, in "response section"

vlastni dat. struktura (pro konverzace, workflows, assistanty atd.), prenos dat/zprav mezi funkcemi (input/output), cast z toho pouzitelne pro logovani, zpetne pujde (ulozene do souboru) prochazet a filtrovat, vyhledavat, analyzovat.

show reponse in the UI (pass response retrieved within app.py workflow to the server - index.html)

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


get text content from url

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

commit to git remote

email
  get new email
  read single email
  send email

news
  get news and filter topic
  read single news

search internet

func to convert image to base64 so it can be uploaded to ai models

