data = {};
reviews = {}

const generateReviews = function (){
    let str = ""
    for(let i=0; i<reviews.reviews.length; i++){
        str += `<p><span>By ${reviews.reviews[i].userName}</span>: <br> ${reviews.reviews[i].message}</P>`
    }
    return str
}

function showReviews(){
    const reviews = document.getElementById("dShowReviews")
    reviews.innerHTML = generateReviews()
}

async function getReviews(bookId){
    const endpoint  = "http://127.0.0.1:8000/getReviews/"+bookId
    const p = await fetch(endpoint)
    reviews = await p.json()

    showReviews()
}

function showResult(bookId, totalViews, rating){
    const image = document.getElementById("dImage")
    const info = document.getElementById("dInfo")
    if(data.volumeInfo.imageLinks.thumbnail != undefined){
        image.innerHTML = `<img src="${data.volumeInfo.imageLinks.thumbnail}" alt="no image" width="100%" height="100%">` 
    }
    else{
        image.innerHTML = "IMAGE NOT AVAILABLE"
    }

    info.innerHTML = `<p><span>Author Name: </span>${data.volumeInfo.authors[0]}</p>
    <p><span>Publisher Name: </span>${data.volumeInfo.publisher}</p>
    <p><span>Publish Date: </span>${data.volumeInfo.publishedDate}</p>
    <p><span>Total Views: </span>${totalViews}</p>
    <p><span>Rating: </span>${rating}</p>`

    const dsc = document.getElementById("dDsc")
    dsc.innerHTML = `<span>Description: </span>${data.volumeInfo.description}`

    getReviews(bookId)
}

async function getData(bookId, totalViews, rating){
    endpoint = "https://www.googleapis.com/books/v1/volumes/"+bookId
    console.log(endpoint);
    try{
        const p = await fetch(endpoint)
        data = await p.json()
        console.log(data)
        showResult(bookId, totalViews, rating)
    }
    catch(err){
        console.log(err.message)
    }
}