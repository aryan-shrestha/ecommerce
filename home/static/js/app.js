var addToCartBtns = document.querySelectorAll(".cartBtn")

for(var i=0; i < addToCartBtns.length; i++){
    addToCartBtns[i].addEventListener('click', function(){
        var productSlug = this.dataset.productslug
        var action = this.dataset.action
        console.log('productSlug:', productSlug, 'action:', action)
        console.log('User:', user)
        if(user === 'AnonymousUser'){
            console.log("Not logged in")
            window.location.href = '/login'
        }
        else{
            addToCart(productSlug, action)
        }
    })
}

function addToCart(productSlug, action){
    console.log("User is logged in, sending data")
    
    var url = 'cart/add-to-cart/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,        
        },
        body:JSON.stringify({'productSlug': productSlug, 'action': action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data:', data)
    })
}