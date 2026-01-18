from trains.models import Train


def get_graph() -> dict:
    graph = {}
    qs = Train.objects.all()
    for q in qs:
        graph.setdefault(q.from_city_id, set())
        graph[q.from_city_id].add(q.to_city_id)
    return graph

def get_all_routes(request, form) -> dict:
    graph = get_graph()
    raise ValueError('Немає даних для пошуку')
