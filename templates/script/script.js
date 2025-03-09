'use strict';


async function get_data(){
    try{
        const response = await fetch("http://127.0.0.1:8000/book/books")

        if (!response.ok){
            throw new Error("Failed to fetch books.");
        }

        const result = await response.json();
        return result;
    }
    catch(error){
        console.log(error);
    }
}


async function show_books(){
    const element = document.querySelector("ul")
    const books = await get_data();

    for (const book of books){
        const li = document.createElement("li")
        let el_book = element.appendChild(li)
        el_book.innerHTML = `${book.name}`
    }
}


show_books()
