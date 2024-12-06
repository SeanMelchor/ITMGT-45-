document.querySelectorAll('.add-to-cart').forEach(button => {
    button.addEventListener('click', function() {
        const productElement = this.closest('.product');
        const productId = productElement.getAttribute('data-id');
        const productName = productElement.getAttribute('data-name');
        const productPrice = parseFloat(productElement.getAttribute('data-price'));

        const product = {
            id: productId,
            name: productName,
            price: parseFloat(productPrice),
            quantity: 1
        };

        let cart = JSON.parse(localStorage.getItem('cart')) || [];
        const existingProduct = cart.find(item => item.id === productId);

        if (existingProduct) {
            existingProduct.quantity += 1;
        } else {
            cart.push(product);
        }

        localStorage.setItem('cart', JSON.stringify(cart));

        console.log('Cart data:', cart); // Debugging line
        alert(`${productName} has been added to your cart!`);
    });
});

document.getElementById('search-button').addEventListener('click', function () {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const products = document.querySelectorAll('.product');

    let found = false;

    products.forEach(product => {
        const productName = product.getAttribute('data-name').toLowerCase();

        if (productName.includes(searchInput)) {
            found = true;

            // Scroll to the product
            product.scrollIntoView({ behavior: 'smooth', block: 'center' });

            // Highlight the product
            product.classList.add('highlight');

            // Remove the highlight after a delay
            setTimeout(() => product.classList.remove('highlight'), 2000);
        }
    });

    if (!found) {
        alert('Product not found!');
    }
});

document.getElementById('apply-filters').addEventListener('click', function() {
    const category = document.getElementById('category-filter').value;
    const sort = document.getElementById('sort-by').value;

    let url = '/products/';
    let params = [];

    if (category) {
        params.push(`category=${encodeURIComponent(category)}`);
    }

    if (sort) {
        params.push(`sort=${encodeURIComponent(sort)}`);
    }

    if (params.length > 0) {
        url += '?' + params.join('&');
    }

    window.location.href = url;
});
