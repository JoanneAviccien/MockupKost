from nicegui import ui
import networkx as nx
import backend as bs

def search_kosan(search_input, current_graph, highlight_searched_kosan, update_kosan_cards_filtered, scroll_container, gender_filter=None, price_filter=None, distance_filter=None):
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
    update_kosan_cards_filtered(current_graph, search_term, scroll_container, highlight_searched_kosan, gender_filter, price_filter, distance_filter)
    
    ui.notify(f'Ditemukan kosan: {found_kosan}', color='positive')

def clear_search(search_input, current_graph, load_area_graph, view_state, highlight_callback, gender_filter=None, price_filter=None, distance_filter=None):
    # hapus pencarian dan tampilkan semua kosan
    search_input.value = ''
    if gender_filter is not None:
        gender_filter.value = 'Semua Gender'
    if price_filter is not None:
        price_filter.value = 'Semua Harga'
    if distance_filter is not None:
        distance_filter.value = 'Semua Jarak'
    if current_graph is not None:
        # Reload the current area to show all kosans
        load_area_graph(view_state['current_area']['name'], highlight_callback)
        ui.notify('Pencarian dibersihkan', color='info')

def filter_kosan_by_attributes(graph, search_term='', gender_filter='Semua Gender', price_filter='Semua Harga', distance_filter='Semua Jarak'):
    """Filter kosan based on search term, gender, price, and distance"""
    paths_data = bs.calculate_all_paths_to_polban(graph)
    
    filtered_kosans = {}
    
    for kosan, data in paths_data.items():
        # Check search term
        if search_term and search_term.lower() not in kosan.lower():
            continue
            
        # Check gender filter
        if gender_filter != 'Semua Gender' and data['gender'] != gender_filter:
            continue
            
        # Check price filter
        if price_filter != 'Semua Harga':
            price = data['price']
            if price_filter == 'Di bawah Rp 1.000.000' and price >= 1000000:
                continue
            elif price_filter == 'Rp 1.000.000 - Rp 1.500.000' and (price < 1000000 or price > 1500000):
                continue
            elif price_filter == 'Rp 1.500.000 - Rp 2.000.000' and (price < 1500000 or price > 2000000):
                continue
            elif price_filter == 'Di atas Rp 2.000.000' and price <= 2000000:
                continue
        
        # Check distance filter
        if distance_filter != 'Semua Jarak':
            distance = data['distance']
            if distance == float('inf'):  # No path available
                continue
            elif distance_filter == 'Di bawah 500 meter' and distance >= 500:
                continue
            elif distance_filter == '500 - 1000 meter' and (distance < 500 or distance > 1000):
                continue
            elif distance_filter == '1000 - 1500 meter' and (distance < 1000 or distance > 1500):
                continue
            elif distance_filter == 'Di atas 1500 meter' and distance <= 1500:
                continue
        
        filtered_kosans[kosan] = data
    
    return filtered_kosans

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
            pos = nx.forceatlas2_layout(current_graph, seed=729)
        case 'Ciwaruga':
            pos = nx.forceatlas2_layout(current_graph, seed=729)
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

def update_kosan_cards_filtered(graph, search_term, scroll_container, highlight_callback, gender_filter='Semua Gender', price_filter='Semua Harga', distance_filter='Semua Jarak'):
    # update kartu kosan yang udah difilter
    scroll_container.clear()
    
    # Get filtered kosans based on all criteria
    filtered_kosans = filter_kosan_by_attributes(graph, search_term, gender_filter, price_filter, distance_filter)
    
    if not filtered_kosans:
        with scroll_container:
            ui.label('Tidak ditemukan kosan yang sesuai dengan filter').classes('text-black text-center p-4')
        return
    
    with scroll_container:
        for kosan, data in filtered_kosans.items():
            with ui.card().style('background-color: #FFFFFF; border-color: #00008B').classes('w-full mb-4'):
                with ui.grid(columns=2).classes('h-full'):
                    ui.image('./assets/mockup_kosan.png').classes('object-fill rounded')
                    with ui.column().classes('flex-1 justify-between h-full'):
                        ui.label(kosan).classes('text-black font-bold text-lg leading-tight break-words').style('line-height: 1.2; max-height: 2.4em; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;')
                        with ui.row().classes('justify-between items-center mt-2'):
                            ui.label(f"Jarak: {data['formatted_distance']}").classes('text-black text-sm')
                            ui.label(f"Harga: {data['formatted_price']}").classes('font-semibold text-green-600 text-sm')
                        with ui.row().classes('justify-between items-center mt-1'):
                            ui.label(f"Gender: {data['gender']}").classes('font-semibold text-blue-600 text-sm')
                            ui.button("Lihat Rute", on_click=lambda k=kosan: highlight_callback(k), color='orange').classes('text-xs px-3 py-1')

def update_kosan_cards(graph, scroll_container, highlight_callback, gender_filter='Semua Gender', price_filter='Semua Harga', distance_filter='Semua Jarak'):
    scroll_container.clear()
    
    # Get filtered kosans based on gender, price, and distance filters
    filtered_kosans = filter_kosan_by_attributes(graph, '', gender_filter, price_filter, distance_filter)
    
    with scroll_container:
        for kosan, data in filtered_kosans.items():
            with ui.card().style('background-color: #FFFFFF; border-color: #00008B').classes('w-full mb-4'):
                with ui.grid(columns=2).classes('h-full'):
                    ui.image('./assets/mockup_kosan.png').classes('object-fill rounded')
                    with ui.column().classes('flex-1 justify-between h-full'):
                        ui.label(kosan).classes('text-black font-bold text-lg leading-tight break-words').style('line-height: 1.2; max-height: 2.4em; overflow: hidden; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;')
                        with ui.row().classes('justify-between items-center mt-2'):
                            ui.label(f"Jarak: {data['formatted_distance']}").classes('text-black text-sm')
                            ui.label(f"Harga: {data['formatted_price']}").classes('font-semibold text-green-600 text-sm')
                        with ui.row().classes('justify-between items-center mt-1'):
                            ui.label(f"Gender: {data['gender']}").classes('font-semibold text-blue-600 text-sm')
                            ui.button("Lihat Rute", on_click=lambda k=kosan: highlight_callback(k), color='orange').classes('text-xs px-3 py-1')

def apply_filters(current_graph, search_input, gender_filter, price_filter, distance_filter, scroll_container, highlight_callback):
    """Apply all active filters and update the display"""
    if current_graph is None:
        ui.notify('Tidak ada data kosan yang tersedia', color='negative')
        return
    
    search_term = search_input.value.lower().strip()
    gender_value = gender_filter.value if gender_filter else 'Semua Gender'
    price_value = price_filter.value if price_filter else 'Semua Harga'
    distance_value = distance_filter.value if distance_filter else 'Semua Jarak'
    
    # Update the display with filtered results
    update_kosan_cards_filtered(current_graph, search_term, scroll_container, highlight_callback, gender_value, price_value, distance_value)
    
    # Show notification about active filters
    active_filters = []
    if search_term:
        active_filters.append(f"Pencarian: '{search_input.value}'")
    if gender_value != 'Semua Gender':
        active_filters.append(f"Gender: {gender_value}")
    if price_value != 'Semua Harga':
        active_filters.append(f"Harga: {price_value}")
    if distance_value != 'Semua Jarak':
        active_filters.append(f"Jarak: {distance_value}")
    
    if active_filters:
        ui.notify(f"Filter aktif: {', '.join(active_filters)}", color='info')

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
            pos = nx.forceatlas2_layout(current_graph, seed=729)
        case 'Ciwaruga':
            pos = nx.forceatlas2_layout(current_graph, seed=729)
        case 'Gegerkalong':
            pos = nx.forceatlas2_layout(current_graph, seed=69)
        case _:
            pos = nx.forceatlas2_layout(current_graph, seed=314)
            
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