var updateBtns = document.getElementsByClassName('update-cart')

for(i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product
        var action = this.dataset.action

        if(user === "AnonymousUser"){
            console.log('')
        }
        else {
            updateUserOrder(productId,action)
        }
    })
}

function updateUserOrder(productId,action){
    var url = '/update_item/'
    var csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;  // Ensure csrftoken is set correctly

    fetch(url,{
        method :'POST',
        headers : {
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId':productId,
            'action':action,
        })
    })
    .then((response) => {
        console.log('Response status:', response.status);  // Log response status
        if (!response.ok) {
            console.log(response)
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then((data) => {
        console.log('data', data)
        location.reload()

    })
    .catch((error) => {
        console.error('Fetch error:', error);
    });

}
