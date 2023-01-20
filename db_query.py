from tinydb import TinyDB, Query

db = TinyDB("C:/Users/orlan/Desktop/CURSOS-PROYECTOS/Proyectos/0. Herramientas/3. Anime Downloader/ch_registry.json")
data = Query()

def add_show (show_name,last_episode, url_list):
    db.insert({"show" : show_name, "current_episode" : last_episode, "list_url" : url_list })

# def next_episode(show_name):
#     episode = db.search(data.show == show_name)[0].get("current_episode")+1
#     return(episode)

def show_data (show_name):
    show_data = db.search(data.show == show_name)[0]
    return(show_data)

def all_shows(atributo):
    list = db.all()
    shows = []

    if atributo == None :
        atributo = "show"
    
    for element in list:
        shows.append(element[atributo])

    return(shows)

def delete_show(show_name):
    db.remove(data.show == show_name)

def update_chapter(show_name):
    current_episode = show_data(show_name)["current_episode"] + 1
    db.update({"current_episode": current_episode}, data.show == show_name)


# ------------- DEBUGING ---------------
# show = "Boruto"
# # update_chapter(show)
# print(next_episode(show))