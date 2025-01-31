from litellm import completion, token_counter
import logging
import traceback

from .messages import System, User, Assistant, ToolCall, ToolResult, Dynamic, from_dict, to_dict

class Chat:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.messages = []
        self.tools = {}
        
        # Set up logging with a unique namespace
        self.logger = logging.getLogger(f"ploppie.chat.{id(self)}")  # Using unique ID per instance
        # Force this logger to propagate up to parent loggers
        self.logger.propagate = True
        # Always set initial level
        self.logger.setLevel(logging.DEBUG if self.kwargs.get("verbose", False) else logging.INFO)
        
        # Remove any existing handlers to prevent duplicate logging
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG if self.kwargs.get("verbose", False) else logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def __str__(self):
        return f"<Chat(messages={len(self.messages)}, tools={len(self.tools)})>"
    
    def to_dict(self):
        return [to_dict(m) for m in self.messages]
    
    def from_dict(self, dict):
        # Clear existing messages
        self.messages = []
        
        # Convert each dict to a Message, skipping any ToolCall or ToolResult messages
        for m in dict:
            if m["type"] == "ToolResult":
                continue

            if m["type"] == "Assistant":
                m["data"]["tool_calls"] = []

            self.messages.append(from_dict(m))

    def token_counter(self, messages):
        return token_counter(
            model=self.kwargs.get("model", "gpt-4o-mini"),
            messages=messages
        )
    
    def dynamic(self):
        """
        Decorator for adding a dynamic message to the chat.
        The decorated function will be called whenever the message needs to be retrieved.
        The function should return a Message object.
        """
        def decorator(func):
            # Find an existing Dynamic message that has no callback and assign the function to it
            # Useful when restoring a chat from a database where the callback cannot be serialized, 
            # and we want to re-assign the dynamic message at the same position in the chat
            for message in self.messages:
                if isinstance(message, Dynamic):
                    if message._callback == None:
                        message._callback = func
                        return func
                    
            # Create a Dynamic message that will call the function when needed
            message = Dynamic(func)
            
            # Add the message to the chat
            self.messages.append(message)
            return func
        
        return decorator

    def tool(self, description: str):
        """
        Decorator for adding a tool to the chat
        """
        def decorator(func):
            self.tools[func.__name__] = {
                "description": description,
                "parameters": func.__annotations__,
                "function": func
            }
            return func
        return decorator
    
    @property
    def tools_to_dict(self):
        """
        Converts the tools to the OpenAI JSON schema format
        """
        tools_dict = []
        for name, tool in self.tools.items():
            # Skip internal/private tools (starting with __)
            if name.startswith("__"):
                continue
            
            tool_dict = {
                "type": "function",
                "function": { 
                    "name": name,
                    "description": tool["description"],
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
            
            # Add each parameter as a property
            for param, annotation in tool["parameters"].items():
                if param == "return": continue
                
                # Get parameter type and description
                param_type = "string"  # default type
                param_desc = ""

                # Debug logging
                self.logger.debug(f"Processing parameter {param} with annotation {annotation}")
                
                if isinstance(annotation, str):
                    # Handle string annotations (e.g., "str: description")
                    if ": " in annotation:
                        type_str, param_desc = annotation.split(": ", 1)
                        param_type = type_str.lower().strip()
                    else:
                        param_type = annotation.lower().strip()
                        param_desc = f"Parameter of type {param_type}"
                elif isinstance(annotation, type):
                    # Handle type objects (e.g., str, int)
                    param_type = annotation.__name__.lower()
                    param_desc = f"Parameter of type {param_type}"
                elif hasattr(annotation, "__origin__"):
                    # Handle typing annotations (e.g., List[str], Optional[int])
                    param_type = str(annotation).lower()
                    param_desc = f"Parameter of type {param_type}"
                else:
                    # For any other case, convert to string representation
                    param_type = str(type(annotation).__name__).lower()
                    param_desc = f"Parameter of type {param_type}"
                
                # Map Python types to JSON Schema types
                type_mapping = {
                    "str": "string",
                    "string": "string",
                    "int": "number",
                    "float": "number",
                    "bool": "boolean",
                    "dict": "object",
                    "list": "array",
                    "typing.list": "array",
                    "typing.dict": "object",
                    "typing.optional": "string"  # Default to string for optional
                }
                
                mapped_type = type_mapping.get(param_type, "string")
                self.logger.debug(f"Mapped {param_type} to {mapped_type}")
                
                tool_dict["function"]["parameters"]["properties"][param] = {
                    "type": mapped_type,
                    "description": param_desc  # Now using the string description instead of the type object
                }
                tool_dict["function"]["parameters"]["required"].append(param)
            
            tools_dict.append(tool_dict)
            
        return tools_dict
    
    @property
    def messages_to_dict(self):
        """
        Converts the messages to the OpenAI message format
        """

        # Filter out any assistant messages with tool calls that don't have corresponding tool results
        filtered_messages = []
        i = 0

        while i < len(self.messages):
            message = self.messages[i]
            
            # If this is an assistant message with tool calls
            if isinstance(message, Assistant) and message.data.get("tool_calls"):
                # Look ahead for tool results for each tool call
                tool_calls = message.data["tool_calls"]
                all_tools_have_results = True
                
                # Check if all tool calls have corresponding results
                for tool_call in tool_calls:
                    found_result = False
                    for j in range(i + 1, len(self.messages)):
                        if isinstance(self.messages[j], ToolResult):
                            if self.messages[j].data.get("tool_call_id") == tool_call.id:
                                found_result = True
                                break
                    if not found_result:
                        all_tools_have_results = False
                        break
                
                # Only keep the message if all its tool calls have results
                if all_tools_have_results:
                    filtered_messages.append(message)
            else:
                filtered_messages.append(message)
            
            i += 1
            
        self.messages = filtered_messages
        return [m.to_json() for m in self.messages if m.to_json() is not None]
    
    def system(self, message: str):
        """
        Adds a system message to the chat
        """
        self.messages.append(System(content=message))
        return self
    
    def user(self, message: str):
        """
        Adds a user message to the chat
        """
        self.messages.append(User(content=message))
        return self
    
    def assistant(self, message: str):
        """
        Adds an assistant message to the chat
        """
        self.messages.append(Assistant(content=message))
        return self
    
    def append(self, message):
        """
        Appends a message to the chat
        """
        if isinstance(message, list):
            self.messages.extend(message)
        else:
            self.messages.append(message)
        return self

    def send(self, message: str):
        """
        Sends a user message to the LLM and automatically handles the response
        """
        self.messages.append(User(content=message))
        return self.ready()
    
    def call_tool(self, tool_call: ToolCall):
        """
        Calls a tool with the given ToolCall object, used internally by the ready() method
        """
        tool_result = self.tools[tool_call.name]["function"](**tool_call.arguments)
        
        self.logger.debug(f"Tool call {tool_call.name} returned")

        self.messages.append(ToolResult(
            content=str(tool_result),
            name=tool_call.name,
            tool_call_id=tool_call.id
        ))

    @property
    def stream(self):
        """
        Whether to stream the response from the LLM
        """
        return self.kwargs.get("stream", False)
    
    def parse_chunk(self, chunk):
        """
        Parses a chunk from the LLM and returns the content and any tool calls
        Returns a tuple of (content, tool_calls)
        """
        chunk_data = chunk.json()
        delta = chunk_data["choices"][0]["delta"]
        
        content = delta.get("content", "")
        tool_calls = delta.get("tool_calls", [])
                    
        return content, tool_calls

    def ready(self):
        """
        Sends the messages to the LLM and handles the response
        """
        responses = []
        
        try:
            response = completion(
                messages=self.messages_to_dict,
                tools=self.tools_to_dict if self.tools else None,
                **self.kwargs
            )
        except Exception as e:
            self.logger.error(f"Fatal error in completion: {e}")
            self.logger.error(traceback.format_exc())
            raise e
        
        if self.stream:
            current_content = ""
            current_tool_calls = []
            
            # Create an initial Assistant message to hold the streaming content
            assistant_message = Assistant(content="", tool_calls=[])
            self.messages.append(assistant_message)
            
            try:
                for chunk in response:
                    content, tool_calls = self.parse_chunk(chunk)
                    
                    # Update the current content
                    if content:
                        current_content += content
                        assistant_message.data["content"] = current_content
                        yield content
                    
                    # Update tool calls
                    if tool_calls:
                        # Consolidate tool calls by ID
                        for tool_call in tool_calls:
                            # Find existing tool call with same index
                            existing_call = None
                            for call in current_tool_calls:
                                if call["index"] == tool_call["index"]:
                                    existing_call = call
                                    break
                            
                            if existing_call:
                                # Update existing call with new data
                                if tool_call["id"]:
                                    existing_call["id"] = tool_call["id"]
                                if tool_call["function"]["name"]:
                                    existing_call["function"]["name"] += tool_call["function"]["name"]
                                if tool_call["function"]["arguments"]:
                                    existing_call["function"]["arguments"] += tool_call["function"]["arguments"]
                            else:
                                # Add new tool call
                                current_tool_calls.append(tool_call)
                        
                        assistant_message.data["tool_calls"] = current_tool_calls
                
                # After the stream is done, process any tool calls
                if current_tool_calls:
                    self.logger.debug(f"Processing {len(current_tool_calls)} tool calls")

                    tool_calls = []

                    for tool_call in current_tool_calls:

                        tool_call = ToolCall(
                            name=tool_call["function"]["name"],
                            arguments=tool_call["function"].get("arguments", ""),
                            id=tool_call["id"]
                        )

                        tool_calls.append(tool_call)

                        self.logger.debug(f"Executing tool call {tool_call.name}")
                        self.call_tool(tool_call)
                        
                    assistant_message.data["tool_calls"] = tool_calls

                    # Make another request to get the response after tool calls
                    return self.ready()
                
            except Exception as e:
                self.logger.error(f"Error during streaming: {e}")
                self.logger.error(traceback.format_exc())
                raise e
            
        else:
            # Non-streaming mode (existing code)
            response = response.json()
            message = response["choices"][0]["message"]

            tool_calls = []
            if "tool_calls" in message:
                if isinstance(message["tool_calls"], list):
                    tool_calls = [
                        ToolCall(
                            name=t["function"]["name"],
                            arguments=t["function"]["arguments"],
                            id=t["id"]
                        ) for t in message["tool_calls"]
                    ]

            content = message["content"] or ""
            self.messages.append(Assistant(
                content=content, 
                tool_calls=tool_calls
            ))

            if content:
                responses.append(content)

            if tool_calls:
                self.logger.debug(f"Processing {len(tool_calls)} tool calls")
                for tool_call in tool_calls:
                    self.logger.debug(f"Executing tool call {tool_call.name}")
                    self.call_tool(tool_call)
                return self.ready()
            
            return responses
