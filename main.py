import heapq
import matplotlib.pyplot as plt
import networkx as nx


def visualize_cable_connection(cables):
    # Перетворимо список кабелів на мін-купу
    heapq.heapify(cables)

    total_cost = 0  # Змінна для зберігання загальних витрат
    steps = []  # Список для зберігання кроків об'єднання кабелів

    while len(cables) > 1:
        # Витягуємо два найменші кабелі
        first_min = heapq.heappop(cables)
        second_min = heapq.heappop(cables)

        # Об'єднуємо їх і додаємо витрати на з'єднання
        cost = first_min + second_min
        total_cost += cost

        # Додаємо новий об'єднаний кабель назад до купи
        heapq.heappush(cables, cost)

        # Зберігаємо крок для подальшої візуалізації
        steps.append((first_min, second_min, cost, list(cables)))

    return total_cost, steps


def draw_heap(heap, ax, title):
    G = nx.DiGraph()
    labels = {}

    def add_edges(parent_idx):
        # Додаємо ребра для дерева купи
        left_idx = 2 * parent_idx + 1
        right_idx = 2 * parent_idx + 2
        if left_idx < len(heap):
            G.add_edge(parent_idx, left_idx)
            add_edges(left_idx)
        if right_idx < len(heap):
            G.add_edge(parent_idx, right_idx)
            add_edges(right_idx)

    for i in range(len(heap)):
        G.add_node(i, label=heap[i])
        labels[i] = heap[i]

    if heap:
        add_edges(0)

    # Використовуємо функцію hierarchy_pos для правильного розташування вузлів у вигляді піраміди
    pos = hierarchy_pos(G, 0) if heap else {}
    nx.draw(
        G,
        pos,
        labels=labels,
        with_labels=True,
        node_size=2000,
        node_color="skyblue",
        ax=ax,
    )
    ax.set_title(title)


def hierarchy_pos(G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos


def _hierarchy_pos(
    G,
    root,
    width=1.0,
    vert_gap=0.2,
    vert_loc=0,
    xcenter=0.5,
    pos=None,
    parent=None,
    parsed=None,
):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    if parsed is None:
        parsed = {root}
    else:
        parsed.add(root)
    neighbors = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        neighbors.remove(parent)
    if len(neighbors) != 0:
        dx = width / 2
        nextx = xcenter - width / 2 - dx / 2
        for neighbor in neighbors:
            nextx += dx
            pos[neighbor] = (nextx, vert_loc - vert_gap)
            pos = _hierarchy_pos(
                G,
                neighbor,
                width=dx,
                vert_gap=vert_gap,
                vert_loc=vert_loc - vert_gap,
                xcenter=nextx,
                pos=pos,
                parent=root,
                parsed=parsed,
            )
    return pos


def plot_steps(steps):
    # Створюємо підплоти для кожного кроку
    fig, axs = plt.subplots(len(steps), 1, figsize=(10, 5 * len(steps)))

    if len(steps) == 1:
        axs = [axs]

    for i, (first_min, second_min, cost, cables) in enumerate(steps):
        draw_heap(
            cables,
            axs[i],
            f"Step {i + 1}: Combine {first_min} and {second_min} -> New Cable {cost}",
        )

    plt.tight_layout()
    plt.show()


# Приклад використання
cables = [4, 3, 2, 6]
total_cost, steps = visualize_cable_connection(cables)
print(f"Мінімальні загальні витрати на з'єднання кабелів: {total_cost}")

plot_steps(steps)
