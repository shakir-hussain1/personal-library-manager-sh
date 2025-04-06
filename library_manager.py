import streamlit as st
import pandas as pd
import json
import os
import random
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from streamlit_lottie import st_lottie

#Styling
st.markdown(
    """
<style>
.stApp{
    background-color: lightblue;
    color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# File path for saving and loading library data
LIBRARY_FILE = 'library.json'

# Load library data from file if it exists
def load_library():
    if os.path.exists(LIBRARY_FILE):
        with open(LIBRARY_FILE, 'r') as file:
            return json.load(file)
    else:
        return []

# Save library data to file
def save_library(library):
    with open(LIBRARY_FILE, 'w') as file:
        json.dump(library, file)

# Display the statistics
def display_statistics(library):
    total_books = len(library)
    if total_books == 0:
        st.write("No books in the library.")
        return
    read_books = sum(1 for book in library if book['read_status'])
    percentage_read = (read_books / total_books) * 100
    st.write(f"Total books: {total_books}")
    st.write(f"Books read: {read_books}")
    st.write(f"Percentage read: {percentage_read:.2f}%")

# Add a book to the library
def add_book(library):
    title = st.text_input("Enter the book title:")
    author = st.text_input("Enter the author name:")
    publication_year = st.number_input("Enter the publication year:", min_value=0, max_value=datetime.now().year, step=1)
    genre = st.text_input("Enter the genre:")
    read_status = st.checkbox("Have you read this book?")
    
    if st.button("Add Book"):
        if title and author and genre:
            new_book = {
                'title': title,
                'author': author,
                'publication_year': publication_year,
                'genre': genre,
                'read_status': read_status
            }
            library.append(new_book)
            save_library(library)
            st.success(f"'{title}' by {author} added to your library.")
        else:
            st.error("Please fill in all the fields.")

# Remove a book from the library
def remove_book(library):
    title = st.text_input("Enter the title of the book you want to remove:")
    
    if st.button("Remove Book"):
        book_to_remove = None
        for book in library:
            if book['title'].lower() == title.lower():
                book_to_remove = book
                break
        
        if book_to_remove:
            library.remove(book_to_remove)
            save_library(library)
            st.success(f"'{title}' has been removed from your library.")
        else:
            st.error("Book not found.")

# Search for a book by title or author
def search_books(library):
    query = st.text_input("Search by title or author:")
    
    if query:
        search_results = [book for book in library if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]
        
        if search_results:
            for book in search_results:
                st.write(f"Title: {book['title']}")
                st.write(f"Author: {book['author']}")
                st.write(f"Publication Year: {book['publication_year']}")
                st.write(f"Genre: {book['genre']}")
                st.write(f"Read Status: {'Read' if book['read_status'] else 'Unread'}")
                st.write("---")
        else:
            st.write("No books found matching your query.")

# Display all books
def display_all_books(library):
    if library:
        for book in library:
            st.write(f"Title: {book['title']}")
            st.write(f"Author: {book['author']}")
            st.write(f"Publication Year: {book['publication_year']}")
            st.write(f"Genre: {book['genre']}")
            st.write(f"Read Status: {'Read' if book['read_status'] else 'Unread'}")
            st.write("---")
    else:
        st.write("No books in your library.")

# Main function for the Streamlit interface
def main():
    st.title("Personal Library Manager")

    # Load the library
    library = load_library()

    # Display a Lottie animation or image
    try:
        st_lottie("https://assets9.lottiefiles.com/packages/lf20_Qwe9bV.json", speed=1, width=500, height=500, key="library")
    except Exception as e:
        #st.warning("Failed to load Lottie animation. Displaying placeholder image.")
        st.image("plms.jpeg", width=500)

    # Menu system
    menu = ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Display Statistics", "Exit"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Add a Book":
        add_book(library)
    elif choice == "Remove a Book":
        remove_book(library)
    elif choice == "Search for a Book":
        search_books(library)
    elif choice == "Display All Books":
        display_all_books(library)
    elif choice == "Display Statistics":
        display_statistics(library)
    elif choice == "Exit":
        st.write("Exiting the program...")
        time.sleep(2)  # Show exit message for a couple of seconds

if __name__ == "__main__":
    main()
