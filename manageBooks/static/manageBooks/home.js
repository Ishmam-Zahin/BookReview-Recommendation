function writeData(data, elementId){
    if(data.volumeInfo == undefined) return
    const  element = document.getElementById(elementId)
    element.innerHTML += `
    <div class="card _xinfo">
    <img src="${function start(){
        if(data.volumeInfo.imageLinks != undefined){
            if(data.volumeInfo.imageLinks.thumbnail != undefined){
                return data.volumeInfo.imageLinks.thumbnail
            }
            else{
                return "/static/manageBooks/resources/brokenImage.jpg"
            }
        }
        else return "/static/manageBooks/resources/brokenImage.jpg"
    }()}" class="card-img-top" alt="Loading . . .">
    <div class="card-body">
    <h5 class="card-title">Title:<br>${data.volumeInfo.title}</h5>
    <a href="/details/${data.id}" class="btn btn-primary">Show details</a>
    </div>
    </div>
    `
}

async function showRecentBooks(bookIds){
    document.getElementById("recentBooks").innerHTML = ""
    for(let i=0; i<bookIds.viewIds.length; i++){
        const p = await fetch(("https://www.googleapis.com/books/v1/volumes/"+bookIds.viewIds[i].bookId))
        const data = await p.json()
        writeData(data, "recentBooks")
        // console.log("one")
    }
    document.getElementById("recentReviewedBooks").innerHTML = ""
    for(let i=0; i<bookIds.reviewIds.length; i++){
        const p = await fetch(("https://www.googleapis.com/books/v1/volumes/"+bookIds.reviewIds[i].bookId))
        const data = await p.json()
        writeData(data, "recentReviewedBooks")
        // console.log("two")
    }
    document.getElementById("topViewedBooks").innerHTML = ""
    for(let i=0; i<bookIds.topViewIds.length; i++){
        const p = await fetch(("https://www.googleapis.com/books/v1/volumes/"+bookIds.topViewIds[i].bookId))
        const data = await p.json()
        writeData(data, "topViewedBooks")
        // console.log("three")
    }
    document.getElementById("topRatedBooks").innerHTML = ""
    for(let i=0; i<bookIds.topRateIds.length; i++){
        const p = await fetch(("https://www.googleapis.com/books/v1/volumes/"+bookIds.topRateIds[i].bookId))
        const data = await p.json()
        writeData(data, "topRatedBooks")
        // console.log("four")
    }
}

async function getRecentBooks(){
    const p = await fetch("/getRecentBooks/12")
    const bookIds = await p.json()
    // console.log(bookIds)
    showRecentBooks(bookIds)
}
getRecentBooks()
