from tinydb import TinyDB, Query


data = Query()

# DB_CONFIG QUERIES
def save_paths():
    db_config = TinyDB ("config.json")
    save_path_table = db_config.table("save_path")
    return(save_path_table.all())

# DB_SHOW QUERIES
db_shows = TinyDB("show_db.json")

def add_show (show_name,last_episode, url_list):
    db_shows.insert({"show": show_name, 
                     "current_episode": last_episode, 
                     "list_url": url_list })

def show_data (show_name):
    show_data = db_shows.search(data.show == show_name)[0]
    return(show_data)

def all_shows(atributo):
    list = db_shows.all()
    shows = []

    if atributo == None :
        atributo = "show"
    
    for element in list:
        shows.append(element[atributo])

    return(shows)

def delete_show(show_name):
    db_shows.remove(data.show == show_name)

def update_chapter(show_name):
    current_episode = show_data(show_name)["current_episode"] + 1
    db_shows.update({"current_episode": current_episode}, data.show == show_name)