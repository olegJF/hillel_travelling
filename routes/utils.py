from trains.models import Train


def dfs_paths(graph, start, goal):
    """
    Функція пошуку усіх можливих маршрутів з одного міста в інше.
    """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph() -> dict:
    graph = {}
    qs = Train.objects.all()
    for q in qs:
        graph.setdefault(q.from_city_id, set())
        graph[q.from_city_id].add(q.to_city_id)
    return graph

def get_all_routes(request, form) -> dict:
    graph = get_graph()
    context = {'form': form}
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
    if not all_ways:
        raise ValueError('Маршруту, що задовільняє цим вимогам не існує')
    return context
