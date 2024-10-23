from langchain_ollama import OllamaLLM  # Importing the Ollama model for language processing
from langchain_core.prompts import ChatPromptTemplate  # Importing the chat prompt template for structured prompts

# Defining the prompt template with clear instructions for the model
template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}\n"
    "Please follow these instructions carefully:\n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}\n"
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response.\n"
    "3. **Empty Response:** If no information matches the description, return an empty string (\" \").\n"
    "4. **Direct Data Only:** Your output should contain only the data explicitly requested, with no other content."
)

# Initializing the Ollama model (Llama3) for handling the language processing task
model = OllamaLLM(model="llama3")

# Function to parse DOM chunks using the Ollama model
def parse_with_ollama(dom_chunks, parse_description):
    prompt_template = ChatPromptTemplate.from_template(template)  # Create a prompt using the provided template
    chain = prompt_template | model  # Connect the prompt to the model (creating a chain for processing)
    parsed_result = []  # List to store the parsed results
    
    # Loop through the DOM content chunks and process each chunk using the model
    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(  # Invoke the model on the current chunk and parse description
            {"dom_content": chunk, "parse_description": parse_description}
        )
        print(f"Parsed batch {i} of {len(dom_chunks)}")  # Print feedback for each parsed chunk
        parsed_result.append(response)  # Add the model's response to the result list
    
    return "\n".join(parsed_result)  # Return the combined results as a single string
