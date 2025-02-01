# MonsterUI

> Combine the simplicity of FastHTML with the power of TailwindCSS

## Installation

To install this library, uses

`pip install MonsterUI`


## Getting Started


Go to the MonsterUI [Getting Started Page](https://monsterui.answer.ai/getting_started).  It is the #1 best way to learn to get started.

### TLDR

Run `python file.py` on this to start:

```python
from fasthtml.common import *
from monsterui.all import *

# Choose a theme color (blue, green, red, etc)
hdrs = Theme.blue.headers()

# Create your app with the theme
app, rt = fast_app(hdrs=hdrs)

@rt
def index():
    socials = (('github','https://github.com/AnswerDotAI/MonsterUI'),
               ('twitter','https://twitter.com/isaac_flath/'),
               ('linkedin','https://www.linkedin.com/in/isaacflath/'))
    return Titled("Your First App",
        Card(
            H1("Welcome!"),
            P("Your first MonsterUI app", cls=TextPresets.muted_sm),
            P("I'm excited to see what you build with MonsterUI!"),
            footer=DivLAligned(*[UkIconLink(icon,href=url) for icon,url in socials])))

serve()
```

## LLM context files

Using LLMs for development is a best practice way to get started and explore. While LLMs cannot code for you, they can be helpful assistants. You must check, refactor, test, and vet any code any LLM generates for you - but they are helpful productivity tools.  Take a look inside the `llms.txt` file to see links to particularly useful context files!

- [llms.txt](https://raw.githubusercontent.com/AnswerDotAI/MonsterUI/refs/heads/main/docs/llms.txt): Links to what is included
- [llms-ctx.txt](https://raw.githubusercontent.com/AnswerDotAI/MonsterUI/refs/heads/main/docs/llms-ctx.txt): MonsterUI Documentation Pages
- [API list](https://raw.githubusercontent.com/AnswerDotAI/MonsterUI/refs/heads/main/docs/apilist.txt): API list for MonsterUI (included in llms-ctx.txt)

In addition you can add `/md` (for markdown) to a url to get a markdown representation and `/rmd` for rendered markdown representation (nice for looking to see what would be put into context.  

### Step by Step

To get started, check out:

1. Start by importing the modules as follows:

```python
from fasthtml.common import *
from monsterui.all import *
```

2. Instantiate the app with the MonsterUI headers

```python
app = FastHTML(hdrs=Theme.blue.headers())

# Alternatively, using the fast_app method
app, rt = fast_app(hdrs=Theme.slate.headers())
```
>*The color option can be any of the theme options available out of the box*

From here, you can explore the API Reference & examples to see how to implement the components. You can also check out these demo videos in the documentation page

- MonsterUI [Getting Started Page](https://monsterui.answer.ai/getting_started)

More resources and improvements to the documentation will be added here soon!
