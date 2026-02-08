from datetime import timedelta

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


def get_graph(qs) -> dict:
    graph = {}
    for q in qs:
        graph.setdefault(q.from_city_id, set())
        graph[q.from_city_id].add(q.to_city_id)
    return graph


def get_all_routes(request, form) -> dict:
    qs = Train.objects.all().order_by('travel_time').select_related('from_city', 'to_city')
    graph = get_graph(qs)
    context = {'form': form}
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    cities = data['cities']
    expected_time = data['expected_time']
    all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
    all_trains = {}
    if not all_ways:
        raise ValueError('Маршруту, що задовільняє цим вимогам не існує')
    if cities:
        cities_id = [city.id for city in cities]
        tmp = []
        for route in all_ways:
            if all(city in route for city in cities_id):
                tmp.append(route)
        if not tmp:
            raise ValueError('Маршрут через ці міста неможливий')
        all_ways = tmp

    for q in qs:
        all_trains.setdefault((q.from_city_id, q.to_city_id), [])
        all_trains[(q.from_city_id, q.to_city_id)].append(q)
    routes = []
    for route in all_ways:
        tmp = {'trains': [], 'total_time': timedelta(0)}
        for i in range(len(route) - 1):
            train_list = all_trains[(route[i], route[i + 1])]
            train = train_list[0]
            tmp['trains'].append(train)
            tmp['total_time'] += train.travel_time
        if tmp['total_time'].total_seconds() // 3600 <  expected_time:
            routes.append(tmp)
    if not routes:
        raise ValueError('Маршрут за такий час неможливий')
    sorted_list = sorted(routes, key=lambda dct: dct['total_time'])
    context['routes'] = sorted_list
    context['from_city'] = from_city
    context['to_city'] = to_city
    return context
