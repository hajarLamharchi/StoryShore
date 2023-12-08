$(document).ready(function () {
    window.addToCart = function(bookId, bookName){

        fetch("/addToCart/"+bookId,{ method: 'POST'}).then(()=>{
            
           
            if ($(".notification").length === 0)
            {
                notify(bookName + " is added to your cart");
            }
            else{
                $(".notification").remove();
                notify(bookName + " is added to your cart");
            }
        })
    }
    
});

function notify(text){
    let notif = $("<div>").addClass("notification");
    notif.text(text)
    $("body").append(notif);
    setTimeout(function(){
        notif.remove();
    }, 3000)
    return notif;
}
