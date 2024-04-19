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
    console.log('Ajout au panier:', productId, 'Quantité:', quantity);
}


function addToCart(productId, quantity) {
    fetch("/add_to_cart/", {  // Utilisez l'alias 'add_to_cart' si configuré pour générer l'URL
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')  // Obtenez le CSRF token depuis les cookies
        },
        body: `product_id=${productId}&quantity=${quantity}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);  // Affiche 'Produit ajouté au panier'
        }
    })
    .catch(error => console.error('Erreur lors de l\'ajout au panier:', error));
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
