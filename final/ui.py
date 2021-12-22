import time
from tkinter import *
from final import build_rail_graph
from graph_class import Train


def search_network():
    count_begin = time.time()
    start_vertex = station_reference[start.get()]
    destination_vertex = station_reference[destination.get()]
    start_text = f'station name{start_vertex.name}   id: {start_vertex.id}'
    destination_text = f'station name{destination_vertex.name}   id: {destination_vertex.id}'
    display_start = Label(text=start_text).pack()
    display_destination = Label(text=destination_text).pack()
    if search_in_map:
        distance, path = current_graph.search_after_map_build(
            str(start_vertex.id),
            str(destination_vertex.id))
    else:
        distance, path = current_graph.search_dijistras(
            str(start_vertex.id),
            str(destination_vertex.id))
    shortest_path_duration_text = f'shortest duration : {distance} '
    shortest_path_duration_label = Label(text=shortest_path_duration_text).pack()
    shortest_path_text = f'path: {str(path)} '
    shortest_path_duration_label = Label(text=shortest_path_text).pack()
    count_end = time.time()
    time_for_search = Label(text=str(count_end - count_begin)).pack()


root = Tk()
root.geometry("400x400")

current_graph = build_rail_graph()
search_in_map = 0

start = StringVar()
station_reference = current_graph.get_named_dict_of_vertices()
stations_list = sorted(station_reference.keys())
start.set("--select station--")
start_station_drop = OptionMenu(root, start, *stations_list)
start_station_drop.pack()
# destination_station_drop =

destination = StringVar()
destination.set("--select station--")
destination_station_drop = OptionMenu(root, destination, *stations_list)
destination_station_drop.pack()

search_button = Button(root, text="search trains", command=search_network).pack()

"""New features"""


# managing station
def create_manage_station_Window():
    def station_window_call_back(*args):
        station_name = station_setting.get()
        station = station_reference[station_name]
        print(station.is_active)
        button_text = StringVar()
        button_text.set(
            f'Toggle Station status({station.is_active})'
        )
        status_button = Button(station_window,
                               text=button_text.get(),
                               command=lambda: station.toggle_status()).pack()
        print(station.is_active)

        print(station)

    station_window = Toplevel(root)
    station_window.geometry("400x400")

    station_setting = StringVar()
    station_setting.set("--select station--")
    station_setting.trace("w", station_window_call_back)
    station_drop = OptionMenu(station_window, station_setting, *stations_list)
    station_drop.pack()

    close_station_button = Button(station_window,
                                  text="cancel",
                                  command=station_window.destroy).pack()


def create_manage_train_Window():
    def train_window_call_back(*args):
        train_name = train_setting.get()
        train = Train.get_object_from_name(train_name)
        print(train.is_active)
        button_text = StringVar()
        button_text.set(
            f'Toggle train status({train.is_active})'
        )
        statu_button = Button(train_window,
                              text=button_text.get(),
                              command=lambda: train.toggle_status()).pack()
        print(train.is_active)

        print(train)

    train_window = Toplevel(root)
    train_window.geometry("400x400")

    trains = Train.trains
    train_names = [Train.trains[id].name for id in Train.trains.keys()]
    train_setting = StringVar()
    train_setting.set("--select train--")
    train_setting.trace("w", train_window_call_back)
    train_drop = OptionMenu(train_window, train_setting, *train_names)
    train_drop.pack()

    close_train_button = Button(train_window,
                                text="cancel",
                                command=train_window.destroy).pack()


manage_station_button = Button(root,
                               text="manage stations",
                               command=create_manage_station_Window)

manage_station_button.pack()

manage_train_button = Button(root,
                             text="manage trains",
                             command=create_manage_train_Window)

manage_train_button.pack()

close_application_button = Button(root,
                                  text="close application",
                                  command=root.destroy).pack()

root.mainloop()
