from os.path import splitext
import aiofiles

from fastapi import APIRouter, Request, UploadFile
from fastapi.templating import Jinja2Templates

from database import CreateReadUpdateDelete, check_id
from schemes import BookScheme, EditBookScheme, DeleteBookScheme

router = APIRouter()
crud = CreateReadUpdateDelete()

jinja_template = Jinja2Templates(directory="templates")


@router.get("/")
async def root(request: Request):
    return jinja_template.TemplateResponse("index.html", {"request": request,
                                                    "name": "Kirill",
                                                    "list": list(range(1, 6))})


@router.get("/book_template")
async def book_template(request: Request):
    return jinja_template.TemplateResponse("template.html", {"request": request})


@router.get("/books")
async def get_all_books():
    books = await crud.read()
    return books


@router.post("/add_book")
async def add_book(book: BookScheme):
    await crud.create(book.name)
    return {"message": "book create successful"}


@router.post("/upload_cover/{book_id}")
async def upload_cover(book_id: int, cover: UploadFile):
    filename = cover.filename
    resolution = splitext(filename)[1]

    if resolution in [".jpg", ".png"]:
        if await check_id(id=book_id):
            async with aiofiles.open(f"covers/{book_id}_book_cover.jpg", "wb") as file:
                content = await cover.read()
                await file.write(content)
                return {"message": "cover upload successful"}
        else:
            return {"message": "book with so id is not defined"}
    else:
        return {"message": "not allowed type of file"}


@router.put("/edit_book")
async def edit_book(book: EditBookScheme):
    result = await crud.update(book_id=book.id, new_name=book.name)
    if result is None:
        return {"message": "book is not defined"}
    else:
        return {"message": "book update successful"}


@router.delete("/delete_book")
async def delete_book(book: DeleteBookScheme):
    result = await crud.delete(book_id=book.id)
    if result is None:
        return {"message": "book is not defined"}
    else:
        return {"message": "book delete successful"}
