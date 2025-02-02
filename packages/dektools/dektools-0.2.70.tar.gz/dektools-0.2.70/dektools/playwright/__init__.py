import playwright
import patchright
from playwright.sync_api import sync_playwright as sync_playwright_default
from patchright.sync_api import sync_playwright as sync_playwright_stealth
from playwright.async_api import async_playwright as async_playwright_default
from patchright.async_api import async_playwright as async_playwright_stealth
from ..ext.image import image_extensions
from ..ext.font import font_extensions
from ..ext.audio import audio_extensions
from ..ext.video import video_extensions
from ..web.url import get_url_ext
from .route import RouteTool


def sync_playwright(stealth=True):
    if stealth:
        return sync_playwright_stealth()
    else:
        return sync_playwright_default()


def async_playwright(stealth=True):
    if stealth:
        return async_playwright_stealth()
    else:
        return async_playwright_default()


def is_stealth(obj):
    if isinstance(obj, type):
        cls = obj
    else:
        cls = obj.__class__
    return cls.__module__.startswith(patchright.__name__)


def get_playwright_name(stealth: bool):
    return patchright.__name__ if stealth else playwright.__name__


async def fix_stealth_mode(context):
    if is_stealth(context):
        await RouteTool(True).context_route_all(context)


def get_resource_type(request):
    default = request.resource_type
    if default == 'other':
        ext = get_url_ext(request.url)
        if ext == '.css':
            return 'stylesheet'
        elif ext == 'js':
            return 'script'
        elif ext in audio_extensions or ext in video_extensions:
            return 'media'
        if ext in image_extensions:
            return 'image'
        elif ext in font_extensions:
            return 'font'
    return request.resource_type
