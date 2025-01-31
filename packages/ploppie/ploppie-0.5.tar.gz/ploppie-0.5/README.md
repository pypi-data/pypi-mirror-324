# Ploppie

A high-level, stupid-simple Pythonic LiteLLM abstraction layer for implementing simple chat workflows, with tools. Supports vision and audio models. Includes facilities for easy (de)serialization of chat histories. 

So stupid that I couldn't come up with a better name.

## Installation

```bash
pip install ploppie
```

## Example Usage

### Simple chat
```python
from ploppie import Chat

chat = Chat()

response = chat.system("You are a helpful assistant.") \
    .user("What is the capital of France?") \
    .ready()

print(response)
```

### Chat with tools
```python
from ploppie import Chat

chat = Chat(model="gpt-4o-mini")

@chat.tool("Perform mathematical calculations")
def calculate(expression: "str: The expression to calculate"):
    return eval(expression)
    
print(chat.send("What is 2502 * 2502, and 2858 - 28592? Please tell me the results."))
```

### Chat with vision
```python
from ploppie import Chat
from ploppie.messages import Image

chat = Chat(model="gpt-4o-mini")

response = chat.system("You are a helpful assistant.") \
    .user(Image(file_handle=open("beautiful_landscape.png", "rb"))) \
    .ready()

print(response)
```

### Utility
```python
from ploppie import Utility
from datetime import datetime

utility = Utility(model="gpt-4o-mini")
time_of_day = datetime.now().strftime("%I:%M %p")

print(f"Time of day: {time_of_day}")

response = utility.selector(
    f"Pick a color that best matches the sky for this time of day: {time_of_day}",
    options=[
        "red",
        "blue",
        "green",
        "yellow",
        "purple",
        "orange",
        "pink",
    ]
)

print(response)
```

See the examples directory for more information.