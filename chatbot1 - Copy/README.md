# Religious Places Chatbot

A chatbot application that provides information about religious places such as temples, churches, mosques, etc. Users can ask about history, nearby tourist attractions, transportation options, accommodations, and locations.

## Features

- Interactive chat interface with real-time responses
- Information about various religious places around the world
- Details on history, tourist attractions, transportation, and accommodation options
- Simple, clean UI designed for easy navigation

## Technology Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **Database**: MongoDB

## Prerequisites

- Python 3.7 or higher
- MongoDB installed and running
- Web browser

## Installation and Setup

1. **Clone the repository**

```
git clone <repository-url>
cd religious-places-chatbot
```

2. **Install Python dependencies**

```
pip install -r requirements.txt
```

3. **Set up the MongoDB database**

Ensure MongoDB is running, then run:

```
python init_db.py
```

This will create a database named `religious_places_db` with a collection named `places` containing sample data.

4. **Start the Flask server**

```
python app.py
```

5. **Open the application**

Open `index.html` in a web browser.

## How to Use

1. Type a question in the chat input or click on one of the suggestion chips
2. The chatbot will respond with relevant information about religious places
3. You can ask questions like:
   - "Tell me about the history of Golden Temple"
   - "What are the tourist attractions near Vatican City?"
   - "How to reach Ajmer Sharif?"
   - "What are some budget accommodations in Varanasi?"
   - "Where is Bodhgaya located?"

## Extending the Application

### Adding More Religious Places

To add more religious places to the database, edit the `init_db.py` file and add new entries to the `sample_places` list.

### Improving the UI

You can enhance the UI by modifying the `styles.css` file to change colors, layouts, or add new features.

### Adding New Features

- User authentication
- Multi-language support
- Image galleries of religious places
- Interactive maps
- Tour booking integration

## License

[MIT License](LICENSE)

## Contact

For questions or support, please contact [your contact info]. 