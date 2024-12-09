# import networkx as nx
# import matplotlib.pyplot as plt
# import os
# from .grammar import get_expression_tree

# def generate_tree_image(expression):
#     try:
#         # Crear un grafo dirigido
#         G = nx.DiGraph()
        
#         def add_nodes_edges(node, parent_id=None):
#             # Generar un ID único para este nodo
#             current_id = len(G.nodes)
            
#             # Agregar el nodo al grafo
#             G.add_node(current_id, label=str(node.value))
            
#             # Si tiene padre, agregar la conexión
#             if parent_id is not None:
#                 G.add_edge(parent_id, current_id)
            
#             # Procesar recursivamente los hijos
#             if hasattr(node, 'left') and node.left is not None:
#                 add_nodes_edges(node.left, current_id)
#             if hasattr(node, 'right') and node.right is not None:
#                 add_nodes_edges(node.right, current_id)
                
#             return current_id

#         # Obtener el árbol de expresión y construir el grafo
#         expr_tree = get_expression_tree(expression)
#         if expr_tree:
#             add_nodes_edges(expr_tree)

#         # Configurar el estilo del gráfico
#         plt.figure(figsize=(10, 8))
#         pos = nx.spring_layout(G)
        
#         # Dibujar los nodos
#         nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
#                              node_size=1000, alpha=0.9)
#         nx.draw_networkx_edges(G, pos, edge_color='gray', 
#                              arrows=True, arrowsize=20)
        
#         # Agregar las etiquetas
#         labels = nx.get_node_attributes(G, 'label')
#         nx.draw_networkx_labels(G, pos, labels, font_size=16)
        
#         # Asegurar que existe el directorio static
#         os.makedirs('static', exist_ok=True)
        
#         # Guardar la imagen
#         image_path = os.path.join('static', 'tree.png')
#         plt.savefig(image_path, format='png', bbox_inches='tight')
#         plt.close()  # Cerrar la figura para liberar memoria
        
#         return image_path

#     except Exception as e:
#         print(f"Error al generar el árbol: {str(e)}")
#         raise e

import networkx as nx
import matplotlib.pyplot as plt
import os
from .grammar import get_expression_tree

def generate_tree_image(expression):
    try:
        # Crear un grafo dirigido
        G = nx.DiGraph()
        
        def add_nodes_edges(node, parent_id=None, level=0):
            if node is None:
                return None
                
            current_id = len(G.nodes)
            
            # Determinar el tipo de nodo y su estilo
            is_operator = node.type == 'operator'
            
            # Crear la etiqueta según el tipo de nodo
            label = str(node.value)
            
            # Agregar el nodo al grafo con información de nivel
            G.add_node(current_id, 
                      label=label,
                      level=level,
                      is_operator=is_operator)
            
            # Si tiene padre, agregar la conexión
            if parent_id is not None:
                G.add_edge(parent_id, current_id)
            
            # Procesar hijos para operadores
            if node.left:
                add_nodes_edges(node.left, current_id, level + 1)
            if node.right:
                add_nodes_edges(node.right, current_id, level + 1)
                
            return current_id

        # Obtener y construir el árbol
        expr_tree = get_expression_tree(expression)
        if expr_tree:
            add_nodes_edges(expr_tree)

        # Configurar el estilo del gráfico
        plt.figure(figsize=(12, 8))
        
        # Usar un layout jerárquico
        pos = nx.kamada_kawai_layout(G)
        
        # Ajustar las posiciones para que sea más jerárquico
        for node, (x, y) in pos.items():
            level = G.nodes[node]['level']
            pos[node] = (x, -level * 0.3)  # Ajustar la posición vertical según el nivel

        # Separar nodos de operadores y números
        operator_nodes = [n for n, attr in G.nodes(data=True) if attr['is_operator']]
        number_nodes = [n for n, attr in G.nodes(data=True) if not attr['is_operator']]
        
        # Dibujar los nodos de operadores (más grandes y en un color distintivo)
        nx.draw_networkx_nodes(G, pos, 
                             nodelist=operator_nodes,
                             node_color='lightgreen', 
                             node_size=2000,
                             node_shape='s')  # Cuadrados para operadores
        
        # Dibujar los nodos de números (más pequeños y en otro color)
        nx.draw_networkx_nodes(G, pos, 
                             nodelist=number_nodes,
                             node_color='lightblue', 
                             node_size=1500,
                             node_shape='o')  # Círculos para números
        
        # Dibujar las conexiones
        nx.draw_networkx_edges(G, pos, 
                             edge_color='gray',
                             arrows=True, 
                             arrowsize=20,
                             arrowstyle='->',
                             width=2)
        
        # Agregar las etiquetas
        labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos, labels, font_size=16, font_weight='bold')
        
        # Eliminar los ejes
        plt.axis('off')
        
        # Ajustar los márgenes
        plt.margins(0.2)
        
        # Asegurar que existe el directorio static
        os.makedirs('static', exist_ok=True)
        
        # Guardar la imagen con alta calidad
        image_path = os.path.join('static', 'tree.png')
        plt.savefig(image_path, 
                   format='png', 
                   bbox_inches='tight',
                   dpi=300,
                   facecolor='white',
                   edgecolor='none',
                   pad_inches=0.5)
        plt.close()
        
        return image_path

    except Exception as e:
        print(f"Error al generar el árbol: {str(e)}")
        raise e