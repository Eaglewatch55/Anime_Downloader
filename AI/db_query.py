from tinydb import TinyDB, Query

db = TinyDB("C:/Users/orlan/Desktop/CURSOS-PROYECTOS/Proyectos/0. Herramientas/3. Anime Downloader/ch_registry.json")
data = Query()

def add_show(show_name, last_episode, url_list):
    """Add a new anime show to the database.

    Args:
        show_name: The name of the anime show.
        last_episode: The number of the most recently downloaded episode.
        url_list: The URL of the anime show's episode list on the animeflv.net website.
    """
    db.insert({"show": show_name, "current_episode": last_episode, "list_url": url_list})

def show_data(show_name):
    """Retrieve the data for a given anime show from the database.

    Args:
        show_name: The name of the anime show.

    Returns:
        A dictionary containing the data for the given anime show.
    """
    show_data = db.search(data.show == show_name)[0]
    return show_data

def all_shows(attribute=None):
    """Retrieve a list of all anime shows in the database.

    Args:
        attribute: (optional) The name of the attribute to retrieve for each show.
                   If not specified, the default attribute is "show".

    Returns:
        A list of all anime shows in the database.
    """
    show_list = db.all()
    shows = []

    if attribute is None:
        attribute = "show"

    for element in show_list:
        shows.append(element[attribute])

    return shows

def delete_show(show_name):
    """Delete a given anime show from the database.

    Args:
        show_name: The name of the anime show to delete.
    """
    db.remove(data.show == show_name)

def update_chapter(show_name):
    """Update the current episode number for a given anime show.

    Args:
        show_name: The name of the anime show.
    """
    current_episode = show_data(show_name)["current_episode"] + 1
    db.update({"current_episode": current_episode}, data.show == show_name)