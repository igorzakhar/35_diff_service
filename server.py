import pathlib

from aiohttp import web
import aiohttp_jinja2
import jinja2

from diff import htmldiff


PROJ_ROOT = pathlib.Path(__file__).parent.parent
TEMPLATES_ROOT = pathlib.Path(__file__).parent / 'templates'


def setup_jinja(app):
    loader = jinja2.FileSystemLoader(str(TEMPLATES_ROOT))
    jinja2_env = aiohttp_jinja2.setup(app, loader=loader)
    return jinja2_env


def setup_routes(app, project_root):
    router = app.router
    router.add_get('/', index)
    router.add_post('/api/v1/htmldiff', api_htmldiff)
    router.add_static(
        '/static/',
        path=str(project_root / 'static'),
        name='static'
    )


@aiohttp_jinja2.template('index.html')
async def index(request):
    return {}


async def api_htmldiff(request):
    try:
        data = await request.json()
        diff_result = htmldiff(data['text1'], data['text2'])
        return web.json_response({'result': diff_result})
    except ValueError as err:
        return web.Response(status=400)


def main():
    app = web.Application()
    setup_jinja(app)
    setup_routes(app, PROJ_ROOT)

    web.run_app(app, host='localhost', port=8080)


if __name__ == '__main__':
    main()
