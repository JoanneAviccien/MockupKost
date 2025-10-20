from nicegui import ui, Client
import networkx as nx
import matplotlib.pyplot as plt
import backshots as bs

@ui.page('/')
def main_page(client: Client):
    client.content.classes('p-0')
    with ui.row().classes('w-full h-screen').style('background-color: #07294d'):
        with ui.splitter(value=30).classes('w-full h-full') as splitter:
            with splitter.before:
                with ui.card().style('background-color: #FF7F00').classes('w-full'):
                    with ui.row().classes('w-full gap-2'):
                        search_input = ui.input(placeholder='Cari kosan') \
                        .props('input-style="color: #00008B" rounded outlined dense') \
                        .classes('bg-white rounded-full flex-grow')
                        
                        search_button = ui.button('Go', color='green', on_click=lambda: search_kosan()) \
                        .classes('bg-white text-white rounded-full px-4')
                        
                        clear_button = ui.button('Clear', color='red', on_click=lambda: clear_search()) \
                        .classes('bg-white text-white rounded-full px-4')
                
                # Create scroll area as a container
                scroll_container = ui.scroll_area().classes('w-full flex-grow')
                
                # Store current graph for search functionality
                current_graph = None
                
                def search_kosan():
                    """Search for kosan based on input and highlight on map"""
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
                    update_kosan_cards_filtered(current_graph, search_term)
                    
                    ui.notify(f'Ditemukan kosan: {found_kosan}', color='positive')
                
                def clear_search():
                    """Clear search and show all kosans"""
                    search_input.value = ''
                    if current_graph is not None:
                        # Reload the current area to show all kosans
                        load_area_graph(view_state['current_area']['name'])
                        ui.notify('Pencarian dibersihkan', color='info')
                
                def highlight_searched_kosan(kosan_name):
                    """Highlight specific kosan path on the map using showhighlightpath"""
                    if current_graph is None:
                        return
                    
                    # Clear current plot
                    ax.clear()
                    
                    # Get current area data for layout
                    area_name = view_state['current_area']['name']
                    
                    # Set layout based on area
                    match area_name:
                        case 'Sarijadi':
                            pos = nx.forceatlas2_layout(current_graph, seed=314)
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

                def update_kosan_cards_filtered(graph, search_term):
                    """Update kosan cards showing only filtered results"""
                    scroll_container.clear()
                    
                    # Get all paths data
                    paths_data = bs.calculate_all_paths_to_polban(graph)
                    
                    # Filter kosans based on search term
                    filtered_kosans = {k: v for k, v in paths_data.items() 
                                     if search_term.lower() in k.lower()}
                    
                    if not filtered_kosans:
                        with scroll_container:
                            ui.label('Tidak ditemukan kosan yang sesuai').classes('text-black text-center p-4')
                        return
                    
                    # Create cards for filtered kosans
                    with scroll_container:
                        for kosan, data in filtered_kosans.items():
                            with ui.card().style('background-color: #FFFFFF; border-color: #00008B').classes('border-2 w-fit'):
                                with ui.grid(columns=2):
                                    ui.image('./mockup_kosan.png').classes('size-32')
                                    with ui.row():
                                        ui.label(kosan).classes('text-black font-bold')
                                        ui.label(f"Jarak ke Polban: {data['formatted_distance']}").classes('text-black text-sm')
                                        ui.label('Rp 1.500.000/bulan').classes('text-black')
                                        ui.button("Lihat Rute", on_click=lambda k=kosan: highlight_searched_kosan(k))
                
                def update_kosan_cards(graph):
                    # Clear existing content in scroll container
                    scroll_container.clear()
                    
                    # Get all paths data
                    paths_data = bs.calculate_all_paths_to_polban(graph)
                    
                    # Create cards for each kosan within the scroll container
                    with scroll_container:
                        for kosan, data in paths_data.items():
                            with ui.card().style('background-color: #FFFFFF; border-color: #00008B').classes('border-2 w-fit'):
                                with ui.grid(columns=2):
                                    ui.image('./mockup_kosan.png').classes('size-32')
                                    with ui.row():
                                        ui.label(kosan).classes('text-black font-bold')
                                        ui.label(f"Jarak ke Polban: {data['formatted_distance']}").classes('text-black text-sm')
                                        ui.label('Rp 1.500.000/bulan').classes('text-black')
                                        ui.button("Lihat Rute", on_click=lambda k=kosan: highlight_searched_kosan(k))

            with splitter.after:
                with ui.column().classes('w-full h-screen'):
                    # Store view state and current area data
                    view_state = {
                        'initial_xlim': None,
                        'initial_ylim': None,
                        'current_area': {'name': 'Sarijadi', 'kosan': 'Kosan Grhya Sahitya Sarijadi'}
                    }
                    
                    def load_area_graph(area_name):
                        area_data = {
                            'Sarijadi': {'file': 'mapdb/sarijadi.json', 'kosan': 'Kosan Grhya Sahitya Sarijadi'},
                            'Ciwaruga': {'file': 'mapdb/ciwaruga.json', 'kosan': 'Kosan Na Jeges 98 Babakan'},
                            'Gegerkalong': {'file': 'mapdb/gegerkalong.json', 'kosan': 'Kosan Gegerkalong Hilir'}
                        }
                        
                        # Update current area
                        view_state['current_area']['name'] = area_name
                        view_state['current_area']['kosan'] = area_data[area_name]['kosan']
                        
                        # Clear and redraw the graph
                        ax.clear()
                        now_viewing = bs.loadgraphdb(area_data[area_name]['file'])
                        
                        # Store current graph for search functionality
                        nonlocal current_graph
                        current_graph = now_viewing
                        
                        # Set layout based on area
                        match area_name:
                            case 'Sarijadi':
                                pos = nx.forceatlas2_layout(now_viewing, seed=314)
                            case 'Ciwaruga':
                                pos = nx.spring_layout(now_viewing, seed=123)
                            case 'Gegerkalong':
                                pos = nx.forceatlas2_layout(now_viewing, seed=69)
                            case _:
                                pos = nx.forceatlas2_layout(now_viewing, seed=314)
                                
                        # Draw initial path
                        shortpath, shortest_path_length = bs.polbanpath(area_data[area_name]['kosan'], 'Polban', now_viewing)
                        bs.showhighlightpath(now_viewing, ax, pos, shortpath)
                        
                        # Update kosan cards with the new graph data
                        update_kosan_cards(now_viewing)

                        plot.update()
                    
                        view_state['initial_xlim'] = ax.get_xlim()
                        view_state['initial_ylim'] = ax.get_ylim()
                        
                        ui.notify(f'Berhasil memuat peta kost {area_name}', color='positive')
                    
                    with ui.card().classes('flex-grow overflow-hidden'):
                        plot = ui.matplotlib().classes('w-full h-full')
                        with plot.figure as fig:
                            ax = fig.gca()
                            
                            # Initial graph load
                            now_viewing = bs.loadgraphdb('mapdb/sarijadi.json')
                            
                            # Store current graph for search functionality
                            current_graph = now_viewing
                            
                            pos = nx.forceatlas2_layout(now_viewing, seed=314)
                            shortpath, shortest_path_length = bs.polbanpath('Kosan Grhya Sahitya Sarijadi','Polban', now_viewing)
                            bs.showhighlightpath(now_viewing,ax,pos,shortpath)
                            
                            # Load initial kosan cards
                            update_kosan_cards(now_viewing)
                            
                            fig.canvas.toolbar_visible = False
                            fig.canvas.header_visible = False
                            fig.canvas.resizable = False
                            fig.canvas.capture_scroll = True
                            
                            # Initialize view state with initial view limits
                            view_state['initial_xlim'] = ax.get_xlim()
                            view_state['initial_ylim'] = ax.get_ylim()
                    
                    def reset_view():
                        if view_state['initial_xlim'] is not None and view_state['initial_ylim'] is not None:
                            ax.set_xlim(view_state['initial_xlim'])
                            ax.set_ylim(view_state['initial_ylim'])
                            plot.update()
                        else:
                            load_area_graph(view_state['current_area']['name'])
                    
                    def zoom_view(factor):
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
                    
                    def move_view(dx, dy):
                        curr_xlim = ax.get_xlim()
                        curr_ylim = ax.get_ylim()
                
                        x_range = curr_xlim[1] - curr_xlim[0]
                        y_range = curr_ylim[1] - curr_ylim[0]
                        x_move = x_range * dx
                        y_move = y_range * dy
                    
                        ax.set_xlim([curr_xlim[0] - x_move, curr_xlim[1] - x_move])
                        ax.set_ylim([curr_ylim[0] - y_move, curr_ylim[1] - y_move])
                        plot.update()
                        
                    with ui.card().classes('w-full flex-none').style('background-color: #FFFFFF;'):
                        with ui.row().classes('w-full flex justify-between items-center'):
                            with ui.row().classes('gap-1'):
                                ui.button('Reset', on_click=lambda: reset_view(), color='#fecf33')
                                ui.button('Zoom In', on_click=lambda: zoom_view(0.8), color='#fecf33')
                                ui.button('Zoom Out', on_click=lambda: zoom_view(1.2), color='#fecf33')
                                with ui.dropdown_button('Opsi Daerah Kost', auto_close=True, color='#fecf33'):
                                    ui.item('Sarijadi', on_click=lambda: load_area_graph('Sarijadi'))
                                    ui.item('Ciwaruga', on_click=lambda: load_area_graph('Ciwaruga'))
                                    ui.item('Gegerkalong', on_click=lambda: load_area_graph('Gegerkalong'))
                            
                            with ui.row().classes('gap-1'):
                                ui.button(on_click=lambda: move_view(0, -0.1), color='#fecf33').props('icon=north')
                                ui.button(on_click=lambda: move_view(0, 0.1), color='#fecf33').props('icon=south')
                                ui.button(on_click=lambda: move_view(0.1, 0), color='#fecf33').props('icon=west')
                                ui.button(on_click=lambda: move_view(-0.1, 0), color='#fecf33').props('icon=east')

ui.run(port=8080)