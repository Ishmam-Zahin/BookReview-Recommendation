function writeHtml(books){
    str = ""
    for(let i=0; i<books.length; i++){
        str+=`
            <div class="card _xinfo">
            <img src="${function start(){
            if(books[i].imageLink != "undefined"){
                return books[i].imageLink
            }
            else return "/static/manageBooks/resources/brokenImage.jpg"
        }()}" class="card-img-top" alt="Loading . . .">
        <div class="card-body">
        <h5 class="card-title">Title:<br>${books[i].title}</h5>
        <a href="/details/${books[i].bookId}" class="btn btn-primary">Show details</a>
        </div>
        </div>
        `
    }
    return str;
}

async function getRecentBooks(){
    const p = await fetch("/getRecentBooks/12")
    const books = await p.json()
    // console.log(books)
    document.getElementById('recentBooks').innerHTML = writeHtml(books.viewBooks)
    document.getElementById('recentReviewedBooks').innerHTML = writeHtml(books.reviewBooks)
    document.getElementById('topViewedBooks').innerHTML = writeHtml(books.topViewBooks)
    document.getElementById('topRatedBooks').innerHTML = writeHtml(books.topRateBooks)
}
getRecentBooks()
