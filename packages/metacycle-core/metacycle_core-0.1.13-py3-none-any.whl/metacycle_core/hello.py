from aiohttp import web
import aiohttp_cors
import socketio
import carla
from bleak import BleakScanner

from metacycle_core.bluetooth import BLECyclingService

from rich.pretty import pprint

origins = [
    "http://localhost:1420",  # dev server run by npm tauri
    "http://127.0.0.1:62210",  # this server itself
    "tauri://localhost",  # compiled Tauri app on Linux
    "http://tauri.localhost",  # compiled Tauri app on Windows
]

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)

# Configure permissive CORS for aiohttp
cors_options = aiohttp_cors.ResourceOptions(
    allow_credentials=True,
    expose_headers="*",
    allow_headers="*",
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
)
cors = aiohttp_cors.setup(app, defaults={origin: cors_options for origin in origins})


async def index(request):
    """Serve the client-side application."""
    return web.Response(text="<h1>Hey babe</h1>", content_type="text/html")


@sio.event
def connect(sid, environ):
    print("connect ", sid)


@sio.event
async def chat_message(sid, data):
    print("message ", data)
    await sio.emit("chat_message", f"Right back at ya, {data}")
    print("Finished sending message:", data)


@sio.event
def disconnect(sid):
    print("disconnect ", sid)


# This is how you return a whole html site, for example.
# app.router.add_static('/static', 'static')
# app.router.add_get('/', index)


@sio.event
async def bt_discover_all(sid):
    print("Scanning all nearby bluetooth devices...")
    devices = await BleakScanner.discover(timeout=2, return_adv=True)
    for k, v in devices.items():
        ble_device, advertisement_data = v
        print(advertisement_data)
    await sio.emit("bt_discover_results", str(devices))


relevant_devices = {
    # don't use dict.from_keys with empty list as argument because it is shared
    "smart_trainer": [],
    "sterzo": [],
}


@sio.event
async def bt_discover_devices_with_relevant_services(sid):
    """
    Scans, then filters for devices that advertise characteristics that we want.
    This gives us a preliminary list of one or more devices that are relevant to us.
    The user should be presented with the results from this function.
    Frontend logic will handle selection from the list, and so on.
    """
    print("Discovering relevant devices...")
    global relevant_devices

    devices = await BleakScanner.discover(timeout=2, return_adv=True)

    # reset relevant_device list first
    for k in relevant_devices:
        relevant_devices[k] = list()

    for k, v in devices.items():
        _ble_device, advertisement_data = v
        service_uuids = advertisement_data.service_uuids

        # Careful with this logic! See BLECyclingService for how Sterzos can be correctly found.
        if (
            (BLECyclingService.ELITE.value in service_uuids)
            and (BLECyclingService.FITNESS.value not in service_uuids)
            and (BLECyclingService.POWERMETER.value not in service_uuids)
        ):
            # Just 'ELITE' is not sufficient, we need to ensure it doesnt have FTMS or powermeter.
            relevant_devices["sterzo"].append(v)
        elif (BLECyclingService.FITNESS.value in service_uuids) and (
            BLECyclingService.POWERMETER.value in service_uuids
        ):
            # We assume smart trainers have FTMS and Powermeter abilities
            relevant_devices["smart_trainer"].append(v)

    pprint(relevant_devices)

    await sio.emit(
        "bt_discover_devices_with_relevant_services_results", str(relevant_devices)
    )


carla_client = None
kill_carla_client = False


from enum import Enum, auto
class CarlaClientStatus(Enum):
    '''
    This enum is sent through 'carla_client_status' socketio channel to notify frontend.
    This code is duplicated and manually synced with a similar enum on frontend.
    '''
    CONNECT_SUCCESS = auto()
    CONNECT_FAILURE = auto()
    DISCONNECT_SUCCESS = auto()
    DISCONNECT_FAILURE = auto()


import pygame
import base64
from metacycle_core.carla_interface import World

from metacycle_core.carla_interface import Reporter

import io
import cv2

carla_client = None

async def carla_game(carla_client):
    global kill_carla_client
    pygame.init()
    pygame.font.init()

    # todo: start GPX recorder
    sim_world = carla_client.get_world()
    print(f"Sim world debug: {sim_world}")
    carla_client.load_world_if_different("Town07")

    # We want Asynchronous server-client and variable time step, which is the default

    # Set variable delta seconds
    settings = sim_world.get_settings()
    settings.fixed_delta_seconds = None # Set a variable time-step
    sim_world.apply_settings(settings)

    # set synchronous mode
    settings = sim_world.get_settings()
    settings.synchronous_mode = False # Enables asynchronous mode
    sim_world.apply_settings(settings)

    pygame_display = pygame.display.set_mode((1280, 720), flags=pygame.HIDDEN | pygame.DOUBLEBUF | pygame.HWSURFACE) # These flags are pretty important for performance
    pygame.display.flip()

    reporter = Reporter(1280, 720, None)

    world = World(sim_world, reporter)

    # controller here
    sim_world.wait_for_tick()

    clock = pygame.time.Clock()

    try:
        while not kill_carla_client:                    
            world.world.wait_for_tick()
            world.tick(clock)
            world.render(pygame_display)
            pygame.display.flip()


            # An efficient way to send frame over socketIO as bas64-encoded JPEG.
            # Previously, I tried using 'pygame.surfarray.array3d(screen_surface)'
            # and OpenCV methods to post-progress, 
            # but using pygame.image.save with in-memory buffer is simpler and more efficient
            screen_surface = pygame.display.get_surface()

            screen_buffer = pygame.surfarray.array3d(screen_surface)
            screen_buffer = cv2.cvtColor(screen_buffer, cv2.COLOR_RGB2BGR)
            screen_buffer = cv2.rotate(screen_buffer, cv2.ROTATE_90_CLOCKWISE)
            # mirror horizontally
            screen_buffer = cv2.flip(screen_buffer, 1)
            jpeg_quality = 70
            _, buffer = cv2.imencode('.jpg', screen_buffer, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
            jpeg_bytes = buffer.tobytes()
            
            # buffer = io.BytesIO()
            # pygame.image.save(screen_surface, buffer, "JPEG")
            # jpeg_bytes = buffer.getvalue()
            # buffer.close()
            # jpg_as_text = base64.b64encode(jpeg_bytes).decode()

            # await sio.emit('carla_game_frame', jpeg_bytes)

    finally:
        # save gpx file

        if world is not None:
            world.destroy()
        
        pygame.quit()
        print("Exited carla simulation")

import asyncio
import time
async def mjpeg_stream(request):
    '''
    Serve MJPEG stream of carla frames.
    Should be called after carla client connection reports success
    '''
    async def frame_generator():
        global kill_carla_client

        pygame.init()
        pygame.font.init()

        # todo: start GPX recorder
        sim_world = carla_client.get_world()
        print(f"Sim world debug: {sim_world}")
        carla_client.load_world_if_different("Town07")

        # We want Asynchronous server-client and variable time step, which is the default

        # Set variable delta seconds
        settings = sim_world.get_settings()
        settings.fixed_delta_seconds = None # Set a variable time-step
        sim_world.apply_settings(settings)

        # set synchronous mode
        settings = sim_world.get_settings()
        settings.synchronous_mode = False # Enables asynchronous mode
        sim_world.apply_settings(settings)

        pygame_display = pygame.display.set_mode((1280, 720), flags=pygame.HIDDEN | pygame.DOUBLEBUF | pygame.HWSURFACE) # These flags are pretty important for performance
        pygame.display.flip()

        reporter = Reporter(1280, 720, None)

        world = World(sim_world, reporter)

        # controller here 
        sim_world.wait_for_tick()

        clock = pygame.time.Clock()

        try:
            while not kill_carla_client:
                # world.world.wait_for_tick() # Don't wait here because instead of waiting, we should be asyncio sleeping in order to give other tasks room to run.
                world.tick(clock)
                world.render(pygame_display)
                pygame.display.flip()

                screen_surface = pygame.display.get_surface()

                # Feel free to remove the legacy way
                # as soon as we're confident that the new method works well
                USE_LEGACY_WAY = False # default is False
                if USE_LEGACY_WAY:
                    # Consumes more CPU, but provides control over JPEG quality
                    # Smaller JPEG file size doesn't impact much of anything
                    screen_buffer = pygame.surfarray.array3d(screen_surface)
                    screen_buffer = cv2.cvtColor(screen_buffer, cv2.COLOR_RGB2BGR)
                    screen_buffer = cv2.rotate(screen_buffer, cv2.ROTATE_90_CLOCKWISE)
                    screen_buffer = cv2.flip(screen_buffer, 1)
                    jpeg_quality = 70
                    _, buffer = cv2.imencode('.jpg', screen_buffer, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])
                    jpeg_bytes = buffer.tobytes()
                else:
                    buffer = io.BytesIO()
                    pygame.image.save(screen_surface, buffer, "JPEG")
                    jpeg_bytes = buffer.getvalue()
                    buffer.close()

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' +
                       jpeg_bytes + b'\r\n')
                
                # This sleep is very important,
                # because it allows other SocketIO async requests to go through.
                # Without it, this function effectively blocks everything else
                # Because it doesn't leave any room for other async tasks
                # It should correspond to 1/fps - processing time for the above logic
                await asyncio.sleep(0.006) # 0.016 (60FPS) - 0.01 (processing time)
        finally:
            # save gpx file
            if world is not None:
                world.destroy()
            
            pygame.quit()
            print("Exited carla simulation")
    return web.Response(
        body=frame_generator(),
        status=200,
        content_type='multipart/x-mixed-replace; boundary=frame'
    )

app.router.add_get('/stream', mjpeg_stream)

@sio.event
async def establish_carla_client_connection(sid):
    await sio.emit('carla_client_status', 'CONNECT_SUCCESS')
    global carla_client
    global kill_carla_client
    kill_carla_client = False
    if carla_client is None:
        carla_client = carla.Client(host="127.0.0.1", port=2000, worker_threads=0)
        try:
            server_version = carla_client.get_server_version()
            print(f"Connected to carla server with version: {server_version}")
            print(f"Carla maps: {carla_client.get_available_maps()}")
            await sio.emit('carla_client_status', str(CarlaClientStatus.CONNECT_SUCCESS.name))

            # a little bit of intricate workflow is required from here on.
            # when the frontend receives a successful 'carla_client_status',
            # it is responsible for making a request to the /stream endpoint,
            # which triggers the 'mjpeg_stream' function above (typically by creating a new <img> element)
            # whose job is to create the carla player and start the MJPEG stream.

        except RuntimeError:
            print("Failed to connect to carla server")
            await sio.emit('carla_client_status', str(CarlaClientStatus.CONNECT_FAILURE.name))

    print("Finished establishing carla client connection")


@sio.event
async def sever_carla_client_connection(sid):
    global carla_client
    global kill_carla_client
    kill_carla_client = True
    try:
        
        if carla_client is not None:
            del carla_client
            carla_client = None
            print("Finished severing carla client connection")
            await sio.emit('carla_client_status', CarlaClientStatus.DISCONNECT_SUCCESS.name)
        else:
            print("No active CARLA connection to sever")
            await sio.emit('carla_client_status', CarlaClientStatus.DISCONNECT_SUCCESS.name)
    except Exception as e:
        print(f"Error while severing CARLA connection: {e}")
        await sio.emit('carla_client_status', CarlaClientStatus.DISCONNECT_FAILURE.name)


def main():
    web.run_app(app, port=62210)


if __name__ == "__main__":
    main()
