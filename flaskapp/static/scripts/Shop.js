$(document).ready(function(){
    
});
function addToCart(bookId){
    fetch("/addToCart/"+bookId,{ method: 'POST'})
    .then(Response=>{
    })
}