from . import todo, static, auth

routes = {
    **todo.routes,
    **static.routes,
    **auth.routes,
}
