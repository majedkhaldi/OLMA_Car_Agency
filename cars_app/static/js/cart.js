<<<<<<< HEAD
document.addEventListener('DOMContentLoaded', function() {
    function updateTotals() {
        let totalQuantity = 0;
        let totalPrice = 0;
        let quantities = {};

        document.querySelectorAll('.quantity').forEach(function(input) {
            let quantity = parseInt(input.value);
            let price = parseFloat(input.dataset.price);
            let carId = input.dataset.id;

            totalQuantity += quantity;
            totalPrice += quantity * price;

            quantities[carId] = quantity;
        });

        localStorage.setItem('totalQuantity', totalQuantity);
        localStorage.setItem('totalPrice', totalPrice.toFixed(2));
        localStorage.setItem('quantities', JSON.stringify(quantities));

        document.getElementById('totalQuantity').textContent = totalQuantity;
        document.getElementById('totalPrice').textContent = totalPrice.toFixed(2);
    }

    function loadTotalsFromStorage() {
        let totalQuantity = localStorage.getItem('totalQuantity');
        let totalPrice = localStorage.getItem('totalPrice');
        let quantities = JSON.parse(localStorage.getItem('quantities'));

        if (totalQuantity !== null) {
            document.getElementById('totalQuantity').textContent = totalQuantity;
        }
        if (totalPrice !== null) {
            document.getElementById('totalPrice').textContent = totalPrice;
        }
        if (quantities !== null) {
            document.querySelectorAll('.quantity').forEach(function(input) {
                let carId = input.dataset.id;
                if (quantities[carId] !== undefined) {
                    input.value = quantities[carId];
                }
            });
        }
    }

    document.querySelectorAll('.quantity').forEach(function(input) {
        input.addEventListener('input', updateTotals);
    });


    loadTotalsFromStorage();

    updateTotals();
});
=======
document.addEventListener('DOMContentLoaded', function() {
    function updateTotals() {
        let totalQuantity = 0;
        let totalPrice = 0;
        let quantities = {};

        document.querySelectorAll('.quantity').forEach(function(input) {
            let quantity = parseInt(input.value);
            let price = parseFloat(input.dataset.price);
            let carId = input.dataset.id;

            totalQuantity += quantity;
            totalPrice += quantity * price;

            quantities[carId] = quantity;
        });

        localStorage.setItem('totalQuantity', totalQuantity);
        localStorage.setItem('totalPrice', totalPrice.toFixed(2));
        localStorage.setItem('quantities', JSON.stringify(quantities));

        document.getElementById('totalQuantity').textContent = totalQuantity;
        document.getElementById('totalPrice').textContent = totalPrice.toFixed(2);
    }

    function loadTotalsFromStorage() {
        let totalQuantity = localStorage.getItem('totalQuantity');
        let totalPrice = localStorage.getItem('totalPrice');
        let quantities = JSON.parse(localStorage.getItem('quantities'));

        if (totalQuantity !== null) {
            document.getElementById('totalQuantity').textContent = totalQuantity;
        }
        if (totalPrice !== null) {
            document.getElementById('totalPrice').textContent = totalPrice;
        }
        if (quantities !== null) {
            document.querySelectorAll('.quantity').forEach(function(input) {
                let carId = input.dataset.id;
                if (quantities[carId] !== undefined) {
                    input.value = quantities[carId];
                }
            });
        }
    }

    document.querySelectorAll('.quantity').forEach(function(input) {
        input.addEventListener('input', updateTotals);
    });


    loadTotalsFromStorage();

    updateTotals();
});
>>>>>>> master
