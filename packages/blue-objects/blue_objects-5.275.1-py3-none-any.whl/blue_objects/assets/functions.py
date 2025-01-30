import os
from typing import List
import glob
from tqdm import tqdm

from blueness import module

from blue_objects import objects, file
from blue_objects.env import abcli_path_git
from blue_objects import NAME
from blue_objects.logger import logger


NAME = module.name(__file__, NAME)


def publish(
    object_name: str,
    list_of_extensions: List[str],
    log: bool = True,
) -> bool:
    logger.info(
        "{}.publish {} / {}".format(
            NAME,
            object_name,
            ", ".join(list_of_extensions),
        )
    )

    for extension in tqdm(list_of_extensions):
        for filename in glob.glob(
            objects.path_of(
                filename=f"*.{extension}",
                object_name=object_name,
            )
        ):
            published_filename = os.path.join(
                abcli_path_git,
                "assets",
                object_name,
                file.name_and_extension(filename),
            )

            if extension in ["png", "jpg", "jpeg", "gif"]:
                if not file.copy(
                    filename,
                    published_filename,
                    log=log,
                ):
                    return False

            if extension == "geojson":
                success, gdf = file.load_geodataframe(filename)
                if not success:
                    return False

                gdf = gdf.to_crs("EPSG:4326")

                if not file.save_geojson(published_filename, gdf):
                    return False

    logger.info(f"🔗  https://github.com/kamangir/assets/tree/main/{object_name}")

    return True
