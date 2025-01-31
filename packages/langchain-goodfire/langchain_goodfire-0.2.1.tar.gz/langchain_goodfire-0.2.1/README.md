# LangChain Goodfire Integration

This package contains the LangChain integration for the Goodfire API.

## Installation

```bash
pip install langchain-goodfire
```

## Usage

```python
from langchain_goodfire import ChatGoodfire
from langchain_core.messages import SystemMessage, HumanMessage
import goodfire

chat = ChatGoodfire(
    model=goodfire.Variant("meta-llama/Llama-3.3-70B-Instruct"),
    goodfire_api_key="your-api-key"
)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Hello!")
]

response = chat.invoke(messages)
print(response)
```

## Development

To install the package in development mode:

```bash
pip install -e .
```

## Testing

Run tests using pytest:

```bash
pytest tests/
```


## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For support, please open an issue on the GitHub repository.
