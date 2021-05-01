def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('state', '/state')
    config.add_route('publish', '/publish', request_method='POST')
    config.add_route('reserve', '/reserve')
