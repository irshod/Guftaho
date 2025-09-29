# Гуфтугў (Guftaho) - Tajik Poetry Library

🌟 A comprehensive digital library of Tajik poetry featuring works from renowned Tajik poets.

## Features

- 📚 Extensive collection of Tajik poetry
- 🔍 Advanced search functionality
- 📖 Organized by poets and books
- 📱 Responsive design for all devices
- 🌙 Dark mode support
- 📋 Copy and share poems
- 🎨 Modern, elegant UI

## Technology Stack

- **Backend**: Django 5.2.6
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite3 (development)
- **Styling**: Custom CSS with modern design system
- **Icons**: Unicode emojis

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/guftaho.git
cd guftaho
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Visit `http://127.0.0.1:8000` to view the application.

## Project Structure

```
guftaho/
├── guftaho/           # Main project settings
├── poetry/            # Poetry app (models, views, etc.)
├── templates/         # HTML templates
├── static/           # CSS, JS, and static assets
├── manage.py         # Django management script
└── requirements.txt  # Python dependencies
```

## Usage

### Admin Panel
Access the admin panel at `/admin/` to:
- Add poets, books, and poems
- Manage content
- Configure site settings

### User Interface
- **Home**: Browse latest poems and featured content
- **Search**: Find poems by title, content, or poet
- **Poet Details**: View poet information and their works
- **Book Details**: Browse poems within a specific book
- **Poem Details**: Read full poems with sharing options

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is created with ❤️ for preserving and promoting Tajik culture and literature.

## Acknowledgments

- Built for the preservation and promotion of Tajik poetry
- Designed with accessibility and user experience in mind
- Responsive design ensures accessibility across all devices

---

**بо ❤️ барои ҳифзу ташри фарҳанги тоҷик сохта шуд**  
*Made with ❤️ for preserving and promoting Tajik culture*