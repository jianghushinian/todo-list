from . import todo, static

routes = {
    **todo.routes,
    **static.routes,
}
