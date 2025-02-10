import graphviz

from inputs import *


edges = set()
dot = graphviz.Graph(engine="neato")


def new_edge(head, tail):
    if (head, tail) not in edges:
        dot.edge(head, tail)
        edges.add((head, tail))


def is_inbound(i, j):
    return 0 <= i < len(grid) and 0 <= j < len(grid[0])


def count_R_neighbors(i, j):
    r_neighbors = 0
    v_neighbors = 0
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))

    for x, y in dirs:
        ci, cj = i + x, j + y

        if not is_inbound(ci, cj):
            continue

        cell = str(grid[ci][cj]).strip()

        if cell == 'R':
            r_neighbors += 1
        elif cell != '':
            v_neighbors += 1

    return r_neighbors, v_neighbors


def R_dfs(i, j, visited, vertices, origin):
    if not is_inbound(i, j):
        return

    cell = str(grid[i][j]).strip()

    if cell == '' or cell == 'X':
        return

    if (i, j) in visited:
        return
    visited.add((i, j))

    if cell != 'R':
        if origin != cell:
            new_edge(origin, cell)
        return
    if vertices.get((i, j)) is not None:
        new_edge(origin, vertices[(i, j)])
        return

    R_dfs(i + 1, j, visited, vertices, origin)
    R_dfs(i - 1, j, visited, vertices, origin)
    R_dfs(i, j + 1, visited, vertices, origin)
    R_dfs(i, j - 1, visited, vertices, origin)


def dfs(id_, i, j, vertices):
    if not is_inbound(i, j):
        return
    
    cell = str(grid[i][j]).strip()

    if cell == 'R':
        R_dfs(i, j, set(), vertices, id_)

    if cell != id_:
        return
    
    grid[i][j] = 'X'  # Mark as visited
    dfs(id_, i + 1, j, vertices)
    dfs(id_, i - 1, j, vertices)
    dfs(id_, i, j + 1, vertices)
    dfs(id_, i, j - 1, vertices)


def main():
    buildings = dict()
    intersections = dict()
    deadends = dict()
    set_storage_ids = set(storage_ids)  # Convert into a set for O(1) lookup

    for i, line in enumerate(grid):
        for j, row in enumerate(line):
            cell = str(row).strip()

            if cell == '' or buildings.get(cell) is not None:
                continue

            if cell == 'R':
                rs, vs = count_R_neighbors(i, j)
                if rs > 2:
                    dot.node(
                        name=f"Intersection{len(intersections) + 1}",
                        label=f"Intersection {len(intersections) + 1}",
                        color="blue",
                        pos=f"{j + 1},{len(grid) - i}!"
                    )
                    intersections[(i, j)] = f"Intersection{len(intersections) + 1}"
                elif (rs < 2 and vs == 0) or rs == 0:
                    dot.node(
                        name=f"Deadend{len(deadends) + 1}",
                        label=f"Deadend {len(deadends) + 1}",
                        pos=f"{j + 1},{len(grid) - i}!"
                    )
                    deadends[(i, j)] = f"Deadend{len(deadends) + 1}"
                continue

            buildings[cell] = (i, j)

            if cell in set_storage_ids:
                label = f'Storage {cell}'
                color = 'green'
            else:
                label = f'Building {cell}'
                color = 'red'

            dot.node(
                name=cell,
                label=label,
                color=color,
                pos=f"{j + 1},{len(grid) - i}!"
            )

    vertices = intersections | deadends
    for key, (i, j) in buildings.items():
        dfs(key, i, j, vertices)
    for (i, j), val in vertices.items():
        grid[i][j] = val
        dfs(val, i, j, vertices)

    dot.render('graph', format='png', view=True)


if __name__ == '__main__':
    main()

"""
Imagine uma grade grande (algo como 200 por 200) de espaços. Cada espaço na grade 
pode ser parte de um prédio, parte de uma estrada ou estar vazio. Se um espaço for um 
prédio, ele terá o ID desse prédio; todos os espaços que fazem parte do mesmo prédio 
devem ser contíguos e ter o mesmo ID de prédio. Se um espaço for uma estrada, ele 
simplesmente é marcado como estrada. 
 
Alguns prédios são especiais: são armazéns (você tem uma lista de quais IDs de prédios 
são armazéns e quais não são). Um prédio está conectado a outro prédio se houver um 
caminho contínuo de ladrilhos de estrada entre os dois. As estradas são conectadas apenas 
em direções ortogonais, não na diagonal. 
 
A largura da estrada é importante: uma estrada com dois ladrilhos de largura é diferente de 
uma estrada com um ladrilho de largura. 
 
Seu código deve pegar a grade e transformá-la em um grafico, onde os vértices 
representam conexões entre estradas, e os pesos dos vértices representam as larguras das 
estradas. Os nós do grafico devem representar prédios, interseções de estradas, mudanças 
na estrada (por exemplo, onde uma estrada de 2 ladrilhos de largura se torna uma de 1 
ladrilho de largura) e terminações de estradas. 
 
Pode ser útil fazer com que seu código gere código Graphviz para que você não precise 
renderizar o grafico manualmente.  
"""
