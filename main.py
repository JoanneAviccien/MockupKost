from nicegui import ui, Client
import networkx as nx
import matplotlib.pyplot as plt
import backend as bs
import ui_utils as utils

@ui.page('/')
def main_page(client: Client):
    client.content.classes('p-0')
    with ui.row().classes('w-full h-screen').style('background-color: #07294d'):
        with ui.splitter(value=30).classes('w-full h-full') as splitter:
            with splitter.before:
                with ui.card().style('background-color: #FF7F00').classes('w-full square-corners').style('border-radius: 0'):
                    # Search section
                    with ui.row().classes('w-full gap-2 mb-3'):
                        search_input = ui.input(placeholder='Cari kosan') \
                        .props('input-style="color: #00008B" rounded outlined dense') \
                        .classes('bg-white rounded-full flex-grow')
                        
                        search_button = ui.button('Go', color='green', on_click=lambda: search_kosan()) \
                        .classes('bg-white text-white rounded-full px-4')
                        
                        clear_button = ui.button('Clear', color='red', on_click=lambda: clear_search()) \
                        .classes('bg-white text-white rounded-full px-4')
                    
                    # Filter section
                    with ui.row().classes('w-full gap-2'):
                        gender_filter = ui.select(
                            options=['Semua Gender', 'Putri', 'Putra', 'Campur'],
                            value='Semua Gender',
                            label='Filter Gender',
                            on_change=lambda: apply_filters()
                        ).props('outlined dense').classes('bg-white rounded flex-1')
                        
                        price_filter = ui.select(
                            options=['Semua Harga', 'Di bawah Rp 1.000.000', 'Rp 1.000.000 - Rp 1.500.000', 'Rp 1.500.000 - Rp 2.000.000', 'Di atas Rp 2.000.000'],
                            value='Semua Harga',
                            label='Filter Harga',
                            on_change=lambda: apply_filters()
                        ).props('outlined dense').classes('bg-white rounded flex-1')
                        
                        distance_filter = ui.select(
                            options=['Semua Jarak', 'Di bawah 500 meter', '500 - 1000 meter', '1000 - 1500 meter', 'Di atas 1500 meter'],
                            value='Semua Jarak',
                            label='Filter Jarak',
                            on_change=lambda: apply_filters()
                        ).props('outlined dense').classes('bg-white rounded flex-1')
                        
                        filter_button = ui.button('Filter', color='blue', on_click=lambda: apply_filters()) \
                        .classes('bg-white text-white rounded px-4')
                
                # Create scroll area as a container
                scroll_container = ui.scroll_area().classes('w-full flex-grow')
                
                # Store current graph for search functionality
                current_graph = None
                
                def search_kosan():
                    # cari kosan berdasarkan input user
                    utils.search_kosan(search_input, current_graph, highlight_searched_kosan, update_kosan_cards_filtered, scroll_container, gender_filter, price_filter, distance_filter)
                
                def clear_search():
                    # hapus pencarian dan tampilkan semua kosan
                    utils.clear_search(search_input, current_graph, load_area_graph, view_state, highlight_searched_kosan, gender_filter, price_filter, distance_filter)
                
                def apply_filters():
                    # terapkan filter gender, harga, dan jarak
                    utils.apply_filters(current_graph, search_input, gender_filter, price_filter, distance_filter, scroll_container, highlight_searched_kosan)
                
                def highlight_searched_kosan(kosan_name):
                    # highlight jalan dari kosan yang dicari
                    utils.highlight_searched_kosan(kosan_name, current_graph, view_state, ax, plot)

                def update_kosan_cards_filtered(graph, search_term, scroll_container, highlight_callback, gender_filter_param=None, price_filter_param=None, distance_filter_param=None):
                    # update kartu kosan yang udah difilter
                    gender_value = gender_filter_param.value if gender_filter_param else (gender_filter.value if gender_filter else 'Semua Gender')
                    price_value = price_filter_param.value if price_filter_param else (price_filter.value if price_filter else 'Semua Harga')
                    distance_value = distance_filter_param.value if distance_filter_param else (distance_filter.value if distance_filter else 'Semua Jarak')
                    utils.update_kosan_cards_filtered(graph, search_term, scroll_container, highlight_callback, gender_value, price_value, distance_value)
                
                def update_kosan_cards(graph, scroll_container, highlight_callback):
                    gender_value = gender_filter.value if gender_filter else 'Semua Gender'
                    price_value = price_filter.value if price_filter else 'Semua Harga'
                    distance_value = distance_filter.value if distance_filter else 'Semua Jarak'
                    utils.update_kosan_cards(graph, scroll_container, highlight_callback, gender_value, price_value, distance_value)

            with splitter.after:
                with ui.column().classes('w-full h-screen place-items-center').style('background-color: #FFFFFF'):
                    view_state = {
                        'initial_xlim': None,
                        'initial_ylim': None,
                        'current_area': {'name': 'Sarijadi', 'kosan': 'Kosan Grhya Sahitya Sarijadi'}
                    }
                    
                    def load_area_graph(area_name, highlight_callback=None):
                        nonlocal current_graph
                        if highlight_callback is None:
                            highlight_callback = highlight_searched_kosan
                        current_graph = utils.load_area_graph(area_name, view_state, ax, plot, scroll_container, highlight_callback)
                    
                    with ui.card().classes('flex-grow overflow-hidden no-shadow'):
                        plot = ui.matplotlib().classes('w-full h-full')
                        with plot.figure as fig:
                            ax = fig.gca()
                            
                            now_viewing = bs.loadgraphdb('mapdb/sarijadi.json')
                            
                            current_graph = now_viewing
                            
                            pos = nx.forceatlas2_layout(current_graph, seed=729)
                            shortpath, shortest_path_length = bs.polbanpath('Kosan Grhya Sahitya Sarijadi','Polban', now_viewing)
                            bs.showhighlightpath(now_viewing,ax,pos,shortpath)
                            
                            update_kosan_cards(now_viewing, scroll_container, highlight_searched_kosan)
                            
                            fig.canvas.toolbar_visible = False
                            fig.canvas.header_visible = False
                            fig.canvas.resizable = False
                            fig.canvas.capture_scroll = True
                            
                            view_state['initial_xlim'] = ax.get_xlim()
                            view_state['initial_ylim'] = ax.get_ylim()
                    
                    def reset_view():
                        utils.reset_view(view_state, ax, plot, load_area_graph, highlight_searched_kosan)
                    
                    def zoom_view(factor):
                        utils.zoom_view(factor, ax, plot)
                    
                    def move_view(dx, dy):
                        utils.move_view(dx, dy, ax, plot)
                        
                    with ui.card().classes('w-full flex-none no-shadow').style('background-color: #FFFFFF;'):
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

ui.run(port=67, title='Aplikasi Pemetaan Kosan Polban', native=True, window_size=(1366, 768))