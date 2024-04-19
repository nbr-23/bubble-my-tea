setTimeout(function() {
    var successMessage = document.getElementById('successMessage');
    if (successMessage) {
        successMessage.style.display = 'none';
    }
}, 5000); 


function changeQuantity(type, id) {
    var quantityInput = document.getElementById('quantity_' + id);
    var currentQuantity = parseInt(quantityInput.value);
    if (type === 'inc') {
        quantityInput.value = currentQuantity + 1;
    } else if (type === 'dec') {
        if (currentQuantity > 1) {
            quantityInput.value = currentQuantity - 1;
        }
    }
}


function addToCart(productId, quantity) {
    fetch("/add_to_cart/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `product_id=${productId}&quantity=${quantity}`
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            console.error(data.error);
            const successMessage = document.getElementById('successMessageShop');
            successMessage.textContent = "Erreur : " + data.error;
            successMessage.classList.remove('hidden');
            setTimeout(() => {
                successMessage.classList.add('hidden');
            }, 3000);
        } else {
            console.log(data.message);  // Optionnel, pour le debugging
            const successMessage = document.getElementById('successMessageShop');
            successMessage.textContent = data.message;  // 'Produit ajouté au panier'
            successMessage.classList.remove('hidden');
            setTimeout(() => {
                successMessage.classList.add('hidden');
            }, 3000);
        }
    })
    .catch(error => {
        console.error('Erreur lors de l\'ajout au panier:', error);
        const successMessage = document.getElementById('successMessageShop');
        successMessage.textContent = "Erreur lors de l'ajout au panier: " + error.message;
        successMessage.classList.remove('hidden');
        setTimeout(() => {
            successMessage.classList.add('hidden');
        }, 3000);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function removeItem(itemId) {
    fetch(`{% url 'remove_from_cart' %}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({ 'item_id': itemId })
    }).then(response => response.json())
      .then(data => {
        if (data.success) {
            window.location.reload();  // Reload the page to update the cart
        } else {
            alert('There was an error removing the item.');
        }
    });
}


