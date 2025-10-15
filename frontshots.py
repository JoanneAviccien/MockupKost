from nicegui import ui
import networkx as nx
import matplotlib.pyplot as plt
import backshots as bs

with ui.row().classes('w-full h-screen').style('background-color: #07294d'):
    with ui.splitter(value=30).classes('w-full h-full') as splitter:
        with splitter.before:
            with ui.card().style('background-color: #FF7F00').classes('w-full'):
                ui.input(placeholder='Cari kosan') \
                .props('input-style="color: #00008B" rounded outlined dense') \
                .classes('bg-white rounded-full w-full')
            
            # Create scroll area as a container
            scroll_container = ui.scroll_area().classes('w-full flex-grow')
            
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
                                    ui.button("Lihat Rute")

        with splitter.after:
            with ui.column().classes('w-full h-screen'):
                # Store view state and current area data
                view_state = {
                    'initial_xlim': None,
                    'initial_ylim': None,
                    'current_area': {'name': 'Sarijadi', 'kosan': 'Kosan P Sarijadi Asih'}
                }
                
                def load_area_graph(area_name):
                    area_data = {
                        'Sarijadi': {'file': 'mapdb/sarijadi.json', 'kosan': 'Kosan P Sarijadi Asih'},
                        'Ciwaruga': {'file': 'mapdb/ciwaruga.json', 'kosan': 'Kosan O Ciwaruga Bahagia'},
                        'Gegerkalong': {'file': 'mapdb/gegerkalong.json', 'kosan': 'Kosan F Gegerkalong Hijau'}
                    }
                    
                    # Update current area
                    view_state['current_area']['name'] = area_name
                    view_state['current_area']['kosan'] = area_data[area_name]['kosan']
                    
                    # Clear and redraw the graph
                    ax.clear()
                    now_viewing = bs.loadgraphdb(area_data[area_name]['file'])
                    
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
                        pos = nx.forceatlas2_layout(now_viewing, seed=314)
                        shortpath, shortest_path_length = bs.polbanpath('Kosan P Sarijadi Asih','Polban', now_viewing)
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