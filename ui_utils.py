from nicegui import ui
import networkx as nx
import backshots as bs

def search_kosan(search_input, current_graph, highlight_searched_kosan, update_kosan_cards_filtered, scroll_container):
    # cari kosan berdasarkan input user
    search_term = search_input.value.lower().strip()
    if not search_term:
        ui.notify('Masukkan nama kosan untuk dicari', color='warning')
        return
    
    if current_graph is None:
        ui.notify('Tidak ada data kosan yang tersedia', color='negative')
        return
    
    # Search for matching kosan names
    matching_kosan = []
    for node in current_graph.nodes():
        if search_term in node.lower():
            matching_kosan.append(node)
    
    if not matching_kosan:
        ui.notify(f'Tidak ditemukan kosan dengan nama "{search_input.value}"', color='negative')
        return
    
    # If multiple matches, show the first one
    found_kosan = matching_kosan[0]
    
    # Highlight the found kosan path on the map using showhighlightpath
    highlight_searched_kosan(found_kosan)
    
    # Update kosan cards to show only the searched kosan
    update_kosan_cards_filtered(current_graph, search_term, scroll_container, highlight_searched_kosan)
    
    ui.notify(f'Ditemukan kosan: {found_kosan}', color='positive')

def clear_search(search_input, current_graph, load_area_graph, view_state, highlight_callback):
    # hapus pencarian dan tampilkan semua kosan
    search_input.value = ''
    if current_graph is not None:
        # Reload the current area to show all kosans
        load_area_graph(view_state['current_area']['name'], highlight_callback)
        ui.notify('Pencarian dibersihkan', color='info')

def highlight_searched_kosan(kosan_name, current_graph, view_state, ax, plot):
    # highlight jalan dari kosan yang dicari
    if current_graph is None:
        return
    
    # Clear current plot
    ax.clear()
    
    # Get current area data for layout
    area_name = view_state['current_area']['name']
    
    # set layout berdasarkan area
    match area_name:
        case 'Sarijadi':
            pos = nx.spring_layout(current_graph, seed=314, method='energy')
        case 'Ciwaruga':
            pos = nx.spring_layout(current_graph, seed=123)
        case 'Gegerkalong':
            pos = nx.forceatlas2_layout(current_graph, seed=69)
        case _:
            pos = nx.forceatlas2_layout(current_graph, seed=314)
    
    # Calculate shortest path from found kosan to Polban
    try:
        shortpath, shortest_path_length = bs.polbanpath(kosan_name, 'Polban', current_graph)
        # Use showhighlightpath to display the path
        bs.showhighlightpath(current_graph, ax, pos, shortpath)
    except nx.NetworkXNoPath:
        ui.notify(f'Tidak ada jalur dari {kosan_name} ke Polban', color='negative')
        return
    
    plot.update()

def update_kosan_cards_filtered(graph, search_term, scroll_container, highlight_callback):
    # update kartu kosan yang udah difilter
    scroll_container.clear()
    
    # ambil data semua jalur
    paths_data = bs.calculate_all_paths_to_polban(graph)
    
    filtered_kosans = {k: v for k, v in paths_data.items() 
                        if search_term.lower() in k.lower()}
    
    if not filtered_kosans:
        with scroll_container:
            ui.label('Tidak ditemukan kosan yang sesuai').classes('text-black text-center p-4')
        return
    
    with scroll_container:
        for kosan, data in filtered_kosans.items():
            with ui.card().style('background-color: #FFFFFF; border-color: #00008B').classes('border-2 w-fit'):
                with ui.grid(columns=2):
                    ui.image('./mockup_kosan.png').classes('size-32')
                    with ui.row():
                        ui.label(kosan).classes('text-black font-bold')
                        ui.label(f"Jarak ke Polban: {data['formatted_distance']}").classes('text-black text-sm')
                        ui.label('Rp 1.500.000/bulan').classes('text-black')
                        ui.button("Lihat Rute", on_click=lambda k=kosan: highlight_callback(k))

def update_kosan_cards(graph, scroll_container, highlight_callback):
    scroll_container.clear()
    
    # ambil data semua jalur
    paths_data = bs.calculate_all_paths_to_polban(graph)
    
    with scroll_container:
        for kosan, data in paths_data.items():
            with ui.card().style('background-color: #FFFFFF; border-color: #00008B').classes('border-2 w-fit'):
                with ui.grid(columns=2):
                    ui.image('./mockup_kosan.png').classes('size-32')
                    with ui.row():
                        ui.label(kosan).classes('text-black font-bold')
                        ui.label(f"Jarak ke Polban: {data['formatted_distance']}").classes('text-black text-sm')
                        ui.label('Rp 1.500.000/bulan').classes('text-black')
                        ui.button("Lihat Rute", on_click=lambda k=kosan: highlight_callback(k))
def reset_view(view_state, ax, plot, load_area_graph, highlight_callback):
                        if view_state['initial_xlim'] is not None and view_state['initial_ylim'] is not None:
                            ax.set_xlim(view_state['initial_xlim'])
                            ax.set_ylim(view_state['initial_ylim'])
                            plot.update()
                        else:
                            load_area_graph(view_state['current_area']['name'], highlight_callback)
                    
def zoom_view(factor, ax, plot):
    curr_xlim = ax.get_xlim()
    curr_ylim = ax.get_ylim()
    new_xlim = [
        curr_xlim[0] + (curr_xlim[1]-curr_xlim[0])*(1-factor)/2,
        curr_xlim[1] - (curr_xlim[1]-curr_xlim[0])*(1-factor)/2
    ]
    new_ylim = [
        curr_ylim[0] + (curr_ylim[1]-curr_ylim[0])*(1-factor)/2,
        curr_ylim[1] - (curr_ylim[1]-curr_ylim[0])*(1-factor)/2
    ]
    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)
    plot.update()

def move_view(dx, dy, ax, plot):
    curr_xlim = ax.get_xlim()
    curr_ylim = ax.get_ylim()

    x_range = curr_xlim[1] - curr_xlim[0]
    y_range = curr_ylim[1] - curr_ylim[0]
    x_move = x_range * dx
    y_move = y_range * dy

    ax.set_xlim([curr_xlim[0] - x_move, curr_xlim[1] - x_move])
    ax.set_ylim([curr_ylim[0] - y_move, curr_ylim[1] - y_move])
    plot.update()

def load_area_graph(area_name, view_state, ax, plot, scroll_container, highlight_callback):
    area_data = {
        'Sarijadi': {'file': 'mapdb/sarijadi.json', 'kosan': 'Kosan Grhya Sahitya Sarijadi'},
        'Ciwaruga': {'file': 'mapdb/ciwaruga.json', 'kosan': 'Kosan Na Jeges 98 Babakan'},
        'Gegerkalong': {'file': 'mapdb/gegerkalong.json', 'kosan': 'Kosan Gegerkalong Hilir'}
    }
    
    # update area yang sedang dilihat
    view_state['current_area']['name'] = area_name
    view_state['current_area']['kosan'] = area_data[area_name]['kosan']
    
    # hapus dan gambar ulang graph
    ax.clear()
    now_viewing = bs.loadgraphdb(area_data[area_name]['file'])
    
    # simpan graph untuk fungsi search
    current_graph = now_viewing
    
    # set layout berdasarkan area
    match area_name:
        case 'Sarijadi':
            pos = nx.forceatlas2_layout(now_viewing, seed=314)
        case 'Ciwaruga':
            pos = nx.spring_layout(now_viewing, seed=123)
        case 'Gegerkalong':
            pos = nx.forceatlas2_layout(now_viewing, seed=69)
        case _:
            pos = nx.forceatlas2_layout(now_viewing, seed=314)
            
    # gambar jalur awal
    shortpath, shortest_path_length = bs.polbanpath(area_data[area_name]['kosan'], 'Polban', now_viewing)
    bs.showhighlightpath(now_viewing, ax, pos, shortpath)
    
    # update kartu kosan dengan data graph baru
    update_kosan_cards(now_viewing, scroll_container, highlight_callback)

    plot.update()

    view_state['initial_xlim'] = ax.get_xlim()
    view_state['initial_ylim'] = ax.get_ylim()
    
    ui.notify(f'Berhasil memuat peta kost {area_name}', color='positive')
    
    return current_graph