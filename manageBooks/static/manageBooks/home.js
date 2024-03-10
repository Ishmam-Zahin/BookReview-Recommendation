function writeData(data, elementId){
    if(data.volumeInfo == undefined) return
    const element = document.getElementById(elementId)
    // console.log(data)
    element.innerHTML += `<div class="rxContainer"><p class="title"><a href="/details/${data.id}">${data.volumeInfo.title}</a></p><p class="image">${function start(){
        str = ""
        if(data.volumeInfo.imageLinks != undefined){
            if(data.volumeInfo.imageLinks.thumbnail != undefined){
                str = `<img src="${data.volumeInfo.imageLinks.thumbnail}" alt="no image">`
            }
            else{
                str = "IMAGE NOT AVAILABLE"
            }
        }
        else{
            str = "IMAGE NOT AVAILABLE"
        }

        return str
    }()}</P></div>`
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
    const p = await fetch("/getRecentBooks/18")
    const bookIds = await p.json()
    console.log(bookIds)
    showRecentBooks(bookIds)
}
getRecentBooks()
