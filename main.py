import streamlit as st
from scrapper import (scrape_website, split_dom_content, clean_body_content, extract_body_content)
from parse import parse_with_ollama
import sys
# Set the title of the web app
st.title("AI Web Scraper")

# Input field to get the website URL from the user
url = st.text_input("Enter a Website URL:")

# Button to trigger the scraping process when clicked
if st.button("Scrape Title"):
    st.write("Scraping the website...")  # Provide feedback to the user
    result = scrape_website(url)  # Call function to scrape the website content
    body_content = extract_body_content(result)  # Extract the body content from the scraped data
    cleaned_content = clean_body_content(body_content)  # Clean the extracted body content
    st.session_state.dom_content = cleaned_content  # Save cleaned content in session state for later use
    # Expander to display the scraped content in a text area
    with st.expander("View Dom Content"):
        st.text_area("DOM CONTENT", cleaned_content, height=300)  # Display the cleaned DOM content

# Check if there is DOM content in session state
if "dom_content" in st.session_state:
    # Input field for the user to enter what they want to parse from the scraped content
    parse_description = st.text_area("Describe what you want to parse?")
    # Button to trigger the parsing process
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the Content")  # Provide feedback to the user
            dom_chunks = split_dom_content(st.session_state.dom_content)  # Split the content into chunks for parsing
            result = parse_with_ollama(dom_chunks, parse_description)  # Parse the content based on user description
            st.write(result)  # Display the parsed result
