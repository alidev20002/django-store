var addBtn = document.getElementById('add-cart')
if (addBtn != null) {
    addBtn.addEventListener('click', function() {
        var product_id = this.dataset.product
        var quantity = document.getElementById('quantity').value
        if (user == 'AnonymousUser'){
            alert('برای خرید اول باید وارد حساب خود شوید')
        }else{
            addCart(product_id, quantity)
        }
    })
}

var delBtn = document.getElementById('del-cart')
if (delBtn != null) {
    delBtn.addEventListener('click', function() {
        var product_id = this.dataset.product
        if (user == 'AnonymousUser'){
            alert('برای حذف خرید اول باید وارد حساب خود شوید')
        }else{
            delCart(product_id)
        }
    })    
}

var qtyup = document.getElementById('qtyup')
var qtydown = document.getElementById('qtydown')
qtyup.addEventListener('click', function() {
    var product_id = this.dataset.product
    var action = this.dataset.action
    if (user == 'AnonymousUser'){
        alert('برای تغییر در سبد خرید اول باید وارد حساب خود شوید')
    }else{
        editCart(product_id, action)
    } 
})
qtydown.addEventListener('click', function() {
    var product_id = this.dataset.product
    var action = this.dataset.action
    if (user == 'AnonymousUser'){
        alert('برای تغییر در سبد خرید اول باید وارد حساب خود شوید')
    }else{
        editCart(product_id, action)
    } 
})

var addf = document.getElementById('add-favor')
if (addf != null) {
    addf.addEventListener('click', function() {
        var product_id = this.dataset.product
        if (user == 'AnonymousUser'){
            alert('برای افزودن به لیست علاقه مندی باید اول وارد حساب خود شوید')
        }else{
            favor(product_id)
        }
    })
}
var delf = document.getElementById('del-favor')
if (delf != null) {
    delf.addEventListener('click', function() {
        var product_id = this.dataset.product
        if (user == 'AnonymousUser'){
            alert('برای حذف از لیست علاقه مندی باید اول وارد حساب خود شوید')
        }else{
            favor(product_id)
        }
    })
}

function addCart(product_id, quantity) {
    var url = 'cart/add'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({'product_id':product_id, 'quantity':quantity})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        location.reload()
    })
}

function delCart(product_id) {
    var url = 'cart/del'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({'product_id':product_id})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        location.reload()
    })
}

function editCart(product_id, action) {
    var url = 'cart/edit'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({'product_id':product_id, 'action': action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        location.reload()
    })
}

function favor(product_id) {
    var url = 'favor/edit'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
            },
            body:JSON.stringify({'product_id':product_id})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        location.reload()
    })
}