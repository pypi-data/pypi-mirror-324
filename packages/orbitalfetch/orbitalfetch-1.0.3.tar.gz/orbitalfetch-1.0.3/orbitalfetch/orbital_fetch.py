import os
import time
import math
import requests
import rasterio
import mercantile
import numpy as np
from PIL import Image
from io import BytesIO
from rasterio.transform import from_bounds
from concurrent.futures import ThreadPoolExecutor, as_completed

# Satellite URL Options
SATELLITE_URLS = {
    "google": "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",  # Google Satellite
    "esri": "https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"  # ESRI World Imagery
}

MAX_WORKERS = 20  # Adjust based on internet speed & CPU

class OrbitalFetch:
    """A class for downloading high-resolution satellite imagery from Google or ESRI and saving as GeoTIFF."""

    def __init__(self, output_path, bbox, target_resolution=1.0, tile_size=256, overwrite=True, satellite_source="google"):
        self.output_path = output_path
        self.bbox = bbox
        self.target_resolution = target_resolution
        self.tile_size = tile_size
        self.overwrite = overwrite
        self.satellite_source = satellite_source.lower()
        self.satellite_url = SATELLITE_URLS.get(self.satellite_source, SATELLITE_URLS["google"])
        self.zoom = self.calculate_zoom_for_resolution()
    
    def calculate_zoom_for_resolution(self):
        """Determine appropriate zoom level for target resolution in meters per pixel."""
        zoom = math.log2(156543.03 / self.target_resolution)
        return int(round(zoom))

    def download_tile(self, tile, max_retries=3):
        """Download a single tile with retries."""
        url = self.satellite_url.format(x=tile.x, y=tile.y, z=self.zoom)
        retries = 0
        while retries < max_retries:
            try:
                response = requests.get(url, stream=True, timeout=10)
                if response.status_code == 200:
                    return tile, Image.open(BytesIO(response.content))
            except requests.exceptions.RequestException:
                pass
            retries += 1
            time.sleep(2)  # Wait before retrying
        return tile, None  # Return None if failed after max retries

    def fetch(self):
        """Downloads and saves the satellite imagery as a GeoTIFF."""
        if os.path.exists(self.output_path) and not self.overwrite:
            print(f"File {self.output_path} already exists. Skipping download.")
            return self.output_path

        min_lon, min_lat, max_lon, max_lat = self.bbox
        tiles = list(mercantile.tiles(min_lon, min_lat, max_lon, max_lat, self.zoom))
        total_tiles = len(tiles)
        
        print(f"Using zoom level: {self.zoom} for {self.target_resolution}m per pixel resolution from {self.satellite_source.upper()}.")
        print(f"Total tiles to download: {total_tiles} from {self.satellite_source.upper()}.")

        image_grid = []
        downloaded_tiles = 0
        failed_tiles = 0

        # Use ThreadPoolExecutor for parallel downloading
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_tile = {executor.submit(self.download_tile, tile): tile for tile in tiles}

            for i, future in enumerate(as_completed(future_to_tile)):
                tile, img = future.result()
                if img:
                    image_grid.append((tile, img))
                    downloaded_tiles += 1
                else:
                    failed_tiles += 1

                if (i + 1) % 1000 == 0 or i == total_tiles - 1:
                    print(f"Progress: {downloaded_tiles}/{total_tiles} downloaded, {failed_tiles} failed")

        if not image_grid:
            raise ValueError("No satellite images downloaded.")

        # Stitch images together
        tile_width, tile_height = self.tile_size, self.tile_size
        rows = max(t.y for t, _ in image_grid) - min(t.y for t, _ in image_grid) + 1
        cols = max(t.x for t, _ in image_grid) - min(t.x for t, _ in image_grid) + 1
        stitched_image = Image.new("RGB", (cols * tile_width, rows * tile_height))

        min_x = min(t.x for t, _ in image_grid)
        min_y = min(t.y for t, _ in image_grid)
        for tile, img in image_grid:
            x_offset = (tile.x - min_x) * tile_width
            y_offset = (tile.y - min_y) * tile_height
            stitched_image.paste(img, (x_offset, y_offset))
            img.close()

        # Convert bounding box to projected coordinates
        transform = from_bounds(min_lon, min_lat, max_lon, max_lat, stitched_image.width, stitched_image.height)

        # Save as GeoTIFF
        with rasterio.open(
            self.output_path,
            "w",
            driver="GTiff",
            height=stitched_image.height,
            width=stitched_image.width,
            count=3,
            dtype=np.uint8,
            crs="EPSG:4326",
            transform=transform,
        ) as dst:
            dst.write(np.array(stitched_image).transpose(2, 0, 1))

        print(f"\nFinal Report:")
        print(f"- Total tiles requested: {total_tiles}")
        print(f"- Successfully downloaded: {downloaded_tiles}")
        print(f"- Failed tiles: {failed_tiles}")
        print(f"\nSaved {self.satellite_source.upper()} Satellite image to {self.output_path} with ~{self.target_resolution}m/px resolution.")

        return self.output_path
