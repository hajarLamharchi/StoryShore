$(document).ready(function(){
    
});
function addToCart(bookId){
    console.log(bookId)
    fetch("/addToCart/"+bookId,{ method: 'POST'})
    .then(Response=>{
        console.log(Response)
    })
}