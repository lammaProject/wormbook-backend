import os
import shutil
import uuid
from typing import Optional
import open3d as o3d
import trimesh

from fastapi import UploadFile, File, Form, HTTPException
import numpy as np
from pathlib import Path

from trimesh import scene

from app.config.settings import UPLOAD_CONFIG
from app.database.books import create_book_db, get_book_db, get_books_db
from app.schemas.books import BookCreate, CategoryEnum


BOOK_WIDTH = 0.15  # метры
BOOK_HEIGHT = 0.22  # метры
BOOK_THICKNESS = 0.03  # метры


def process_file(file_type, file, author):
    print(file_type, file, "file")
    file_location = os.path.join(UPLOAD_CONFIG["BOOKS_COVER"], author, file.filename)
    os.makedirs(os.path.dirname(file_location), exist_ok=True)

    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return file_location
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Не удалось сохранить файл {file_type}: {str(e)}",
        )


async def get_book(book_id: Optional[int] = None):
    if book_id is None:
        return None
    return await get_book_db(book_id)


async def get_books():
    """
    Получает список всех книг.

    Returns:
        list: Список всех книг в базе данных.
    """
    return await get_books_db()


def create_textured_book_mesh(front_path, back_path, bottom_path, pages_path):
    """
    Создает 3D модель книги с текстурами используя trimesh
    """
    # Параметры книги
    width = 1.0
    height = 1.5
    depth = 0.2

    # Создаем отдельные меши для каждой стороны книги
    # Передняя сторона (фронт обложки)
    front_vertices = np.array(
        [[0, 0, 0], [width, 0, 0], [width, height, 0], [0, height, 0]]
    )
    front_faces = np.array([[0, 1, 2], [0, 2, 3]])
    front_uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])

    # Задняя сторона (задняя обложка)
    back_vertices = np.array(
        [[0, 0, depth], [width, 0, depth], [width, height, depth], [0, height, depth]]
    )
    back_faces = np.array([[0, 2, 1], [0, 3, 2]])
    back_uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])

    # Боковые стороны (страницы)
    right_vertices = np.array(
        [[width, 0, 0], [width, 0, depth], [width, height, depth], [width, height, 0]]
    )
    right_faces = np.array([[0, 1, 2], [0, 2, 3]])
    right_uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])

    # Нижняя сторона (дно)
    bottom_vertices = np.array(
        [[0, 0, 0], [width, 0, 0], [width, 0, depth], [0, 0, depth]]
    )
    bottom_faces = np.array([[0, 1, 2], [0, 2, 3]])
    bottom_uv = np.array([[0, 0], [1, 0], [1, 1], [0, 1]])

    # Создаем материалы
    front_material = trimesh.visual.material.PBRMaterial(baseColorTexture=front_path)
    back_material = trimesh.visual.material.PBRMaterial(baseColorTexture=back_path)
    pages_material = trimesh.visual.material.PBRMaterial(baseColorTexture=pages_path)
    bottom_material = trimesh.visual.material.PBRMaterial(baseColorTexture=bottom_path)

    # Создаем меши с текстурами
    front_mesh = trimesh.Trimesh(
        vertices=front_vertices,
        faces=front_faces,
        visual=trimesh.visual.TextureVisuals(uv=front_uv, material=front_material),
    )

    back_mesh = trimesh.Trimesh(
        vertices=back_vertices,
        faces=back_faces,
        visual=trimesh.visual.TextureVisuals(uv=back_uv, material=back_material),
    )

    right_mesh = trimesh.Trimesh(
        vertices=right_vertices,
        faces=right_faces,
        visual=trimesh.visual.TextureVisuals(uv=right_uv, material=pages_material),
    )

    bottom_mesh = trimesh.Trimesh(
        vertices=bottom_vertices,
        faces=bottom_faces,
        visual=trimesh.visual.TextureVisuals(uv=bottom_uv, material=bottom_material),
    )

    # Создаем сцену и добавляем в нее меши
    scene = trimesh.Scene()
    scene.add_geometry(front_mesh)
    scene.add_geometry(back_mesh)
    scene.add_geometry(right_mesh)
    scene.add_geometry(bottom_mesh)

    # В основной функции для экспорта используйте:
    # trimesh.exchange.export.export_mesh(scene, str(output_path), file_type='glb')

    return scene


async def create_book(
    front_file: UploadFile = File(...),
    back_file: UploadFile = File(...),
    bot_file: UploadFile = File(...),
):
    """
    Создает 3D модель книги с текстурами для Three.js.
    """
    try:
        # Чтение содержимого файлов в память
        front_content = await front_file.read()
        back_content = await back_file.read()
        bottom_content = await bot_file.read()

        # Создаем уникальный ID для книги
        book_id = str(uuid.uuid4())

        # Создаем директорию для сохранения модели
        output_dir = Path("uploads") / "books_cover"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Получаем путь к шаблону страниц
        pages_path = Path("upload") / "pages.jpg"
        if not pages_path.exists():
            raise HTTPException(status_code=404, detail="Template pages file not found")

        # Временно сохраняем изображения (trimesh требует файлы на диске)
        temp_dir = Path("uploads") / "temp"
        temp_dir.mkdir(parents=True, exist_ok=True)

        front_path = temp_dir / f"{book_id}_front.jpg"
        back_path = temp_dir / f"{book_id}_back.jpg"
        bottom_path = temp_dir / f"{book_id}_bottom.jpg"

        with open(front_path, "wb") as f:
            f.write(front_content)
        with open(back_path, "wb") as f:
            f.write(back_content)
        with open(bottom_path, "wb") as f:
            f.write(bottom_content)

        # Создаем текстурированную 3D модель книги
        scene = create_textured_book_mesh(
            str(front_path), str(back_path), str(bottom_path), str(pages_path)
        )

        # Сохраняем в формате glTF/GLB для Three.js
        output_path = output_dir / f"{book_id}.glb"
        trimesh.exchange.export.export_mesh(scene, str(output_path), file_type="glb")

        # Удаляем временные файлы после создания модели
        front_path.unlink(missing_ok=True)
        back_path.unlink(missing_ok=True)
        bottom_path.unlink(missing_ok=True)

        return {"book_id": book_id, "model_path": str(output_path)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating book: {str(e)}")
