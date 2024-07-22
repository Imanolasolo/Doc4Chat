Here's a `README.md` for your `Doc4Chat` project:

```markdown
# Doc4Chat

**Doc4Chat** is an interactive application powered by Botarmy Hub that allows you to chat with a knowledge assistant based on the content of a PDF file you upload. It leverages OpenAI's language models to provide responses based on your document's content.

## Features

- **Upload PDF Knowledge Base**: Upload a PDF file containing the information you want to chat about.
- **Ask Questions**: Enter your questions and get answers based on the content of your uploaded PDF.
- **Powered by OpenAI**: Utilizes OpenAI's language models to generate responses.

## Installation

To get started with Doc4Chat, you need to set up your environment. Follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Imanolasolo/Doc4Chat.git
   cd Doc4Chat
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   Ensure you have `pip` installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   streamlit run Doc4Chat.py
   ```

## Usage

1. **Input OpenAI API Key**:
   Enter your OpenAI API key in the sidebar. [Get a free OpenAI API key](https://gptforwork.com/help/knowledge-base/create-openai-api-key).

2. **Upload Knowledge Base PDF**:
   Upload the PDF file that contains the information you want to chat about.

3. **Ask Questions**:
   Type your questions in the input box and click 'Ask' to get responses based on your uploaded knowledge base.

## Example

Once the app is running, you will see the following features:

- A sidebar with fields for API key input, instructions, and links.
- An upload button for your PDF file.
- A text input for asking questions.

## Contributing

If you'd like to contribute to Doc4Chat, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, please contact [Imanol Asolo](mailto:jjusturi@gmail.com).

## Acknowledgements

- Powered by Botarmy Hub.
- Utilizes OpenAI language models.
```
