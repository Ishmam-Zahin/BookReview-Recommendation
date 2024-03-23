function writeBooksToAuthor(books){
    const element = document.getElementById("recommendAuthor")
    for(let i=0; i<books.items.length; i++){
        element.innerHTML += `
        <div class="card _xinfo">
        <img src="${function start(){
        if(books.items[i].volumeInfo.imageLinks != undefined){
            if(books.items[i].volumeInfo.imageLinks.thumbnail != undefined){
                return books.items[i].volumeInfo.imageLinks.thumbnail
            }
            else{
                return "/static/manageBooks/resources/brokenImage.jpg"
            }
        }
        else return "/static/manageBooks/resources/brokenImage.jpg"
        }()}" class="card-img-top" alt="Loading . . .">
        <div class="card-body">
        <h5 class="card-title">Title:<br>${books.items[i].volumeInfo.title}</h5>
        <a href="/details/${books.items[i].id}" class="btn btn-primary">Show details</a>
        </div>
        </div>
        `
    }
    // recommendBooksByGenre()
}

async function getBooks(endpoint){
    const p = await fetch(endpoint)
    const books = await p.json()
    // console.log(books)
    writeBooksToAuthor(books)
}

function recommendBooksByAuthor(){
        authName = document.getElementById("authorName").getAttribute("data-author")
        authName = authName.split(" ")
        // console.log(authName)
        endpoint = "https://www.googleapis.com/books/v1/volumes?q="
        for(let i=0; i<authName.length; i++){
            if(i != authName.length-1) endpoint += "inauthor:"+authName[i]+"+"
            else endpoint += "inauthor:"+authName[i]
        }
        endpoint += "&printType=books&maxResults=10&orderBy=newest&key=AIzaSyDvwGOI6Fi7m7N3x_VeDaQt60C8iPZeruc"
        getBooks(endpoint)
        // console.log(endpoint)
}

const generateReviews = function (){
    let str = ""
    for(let i=0; i<reviews.reviews.length; i++){
        str += `<p><span>By ${reviews.reviews[i].userName}</span>: <br> ${reviews.reviews[i].message}</P>`
    }
    return str
}

function showReviews(){
    const reviews = document.getElementById("dShowReviews")
    reviews.innerHTML += generateReviews()

    recommendBooksByAuthor()
}

async function getReviews(){
    const bookId = document.getElementById("maintitle").getAttribute("data-id")
    const endpoint  = "/getReviews/"+bookId
    const p = await fetch(endpoint)
    reviews = await p.json()

    showReviews()
}
getReviews()

// function showResult(bookId, totalViews, rating){
//     const image = document.getElementById("dImage")
//     const info = document.getElementById("dInfo")
//     const title = document.getElementById("maintitle")
//     title.innerHTML += `${data.volumeInfo.title}`
//     if(data.volumeInfo.imageLinks != undefined){
//         if(data.volumeInfo.imageLinks.thumbnail != undefined){
//             image.innerHTML = `<img src="${data.volumeInfo.imageLinks.thumbnail}" alt="no image" width="100%" height="100%">` 
//         }
//         else{
//             image.innerHTML = "IMAGE NOT AVAILABLE"
//         }
//     }
//     else{
//         image.innerHTML = "IMAGE NOT AVAILABLE"
//     }

//     info.innerHTML += `<p><span>Author Name: </span>${data.volumeInfo.authors[0]}</p>
//     <p><span>Publisher Name: </span>${data.volumeInfo.publisher}</p>
//     <p><span>Publish Date: </span>${data.volumeInfo.publishedDate}</p>
//     <p><span>Total Views: </span>${totalViews}</p>
//     <p><span>Rating: </span>${rating}</p>`

//     const dsc = document.getElementById("dDsc")
//     dsc.innerHTML = `<span>Description: </span><br>${data.volumeInfo.description}`

//     getReviews(bookId)
// }

// async function getData(bookId, totalViews, rating){
//     endpoint = "https://www.googleapis.com/books/v1/volumes/"+bookId
//     console.log(endpoint);
//     try{
//         const p = await fetch(endpoint)
//         data = await p.json()
//         // console.log(data)
//         showResult(bookId, totalViews, rating)
//     }
//     catch(err){
//         console.log(err.message)
//     }
// }