from enum import Enum
import sqlite3

class Director:
    def __init__(self, first_name: str, birth_year: int, last_name: str, birth_place: str):
        self.first_name = first_name
        self.birth_year = birth_year
        self.last_name = last_name
        self.birth_place = birth_place

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.birth_year}"

class Genre(Enum):
    ACTION = "Action"
    SCI_FI = "Sci-Fi"
    DRAMA = "Drama"
    THRILLER = "Thriller"
    ADVENTURE = "Adventure"

class Movie:
    def __init__(self, name: str, year: int, director: Director, rating: float):
        self.name = name
        self.year = year
        self.director = director
        self.rating = rating
        self.genre = set()
        
    def __str__(self) -> str:
        return f"{self.name} {self.year} {self.director} {self.rating} {self.genre}"

    def add_genre(self, *genres: Genre):
        """
        Add one or more genres to the movie.
        """
        self.genre.update(genres)

# Connect to SQLite database
conn = sqlite3.connect('movies.db')
c = conn.cursor()

# Create a table for movies
c.execute('''CREATE TABLE IF NOT EXISTS movies
             (name TEXT, year INTEGER, director TEXT, rating REAL, genre TEXT)''')

# Function to insert a movie into the database
def insert_movie(movie: Movie):
    genres = ', '.join([genre.value for genre in movie.genre])
    c.execute("INSERT INTO movies VALUES (?, ?, ?, ?, ?)",
              (movie.name, movie.year, f"{movie.director.first_name} {movie.director.last_name}", movie.rating, genres))
    conn.commit()

# Function to update a movie in the database
def update_movie(movie: Movie):
    genres = ', '.join([genre.value for genre in movie.genre])
    c.execute("UPDATE movies SET year=?, director=?, rating=?, genre=? WHERE name=?",
              (movie.year, f"{movie.director.first_name} {movie.director.last_name}", movie.rating, genres, movie.name))
    conn.commit()

# Function to delete a movie from the database
def delete_movie(name: str):
    c.execute("DELETE FROM movies WHERE name=?", (name,))
    conn.commit()

# Function to retrieve all movies from the database
def get_all_movies():
    c.execute("SELECT * FROM movies")
    return c.fetchall()

# Example usage
if __name__ == "__main__":
    # Create a director instance
    director = Director("Joel", 1976, "Silver", "South Orange")

    # Create a movie instance
    movie = Movie("The Matrix", 1999, director, 8.7)
    
    # Add genres to the movie
    movie.add_genre(Genre.ACTION, Genre.SCI_FI)
    
    # Insert movie into the database
    insert_movie(movie)

    # Update movie in the database
    movie.rating = 9.0
    update_movie(movie)

    # Print movie information
    print("Movie Name:", movie.name)
    print("Release Year:", movie.year)
    print("Director:", movie.director)
    print("Rating:", movie.rating)
    print("Genres:", ", ".join(genre.value for genre in movie.genre))

    # Delete movie from the database
    delete_movie(movie.name)

    # Retrieve and print all movies
    print("All Movies:") 
    try: 
        for row in get_all_movies(): 
            print(row) 
    except sqlite3.OperationalError: 
        print("No movies found in the database.")

# Close the database connection
conn.close()