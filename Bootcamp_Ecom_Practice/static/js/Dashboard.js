document.addEventListener('DOMContentLoaded', function () {
    const chartCanvas = document.getElementById('revenueChart');
    
    // Retrieve data from data attributes
    const productNamesData = chartCanvas.getAttribute('data-product-names');
    const revenuesData = chartCanvas.getAttribute('data-revenues');

    // Parse the JSON data
    let productNames = [];
    let revenues = [];

    try {
        productNames = JSON.parse(productNamesData);
        revenues = JSON.parse(revenuesData);
    } catch (e) {
        console.error('Error parsing chart data:', e);
    }

    // Check if there are products to display
    if (productNames.length > 0 && revenues.length > 0) {
        const ctx = chartCanvas.getContext('2d');
        const revenueChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: productNames,
                datasets: [{
                    label: 'Revenue ($)',
                    data: revenues,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { 
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Revenue ($)'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Products'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: false,
                        text: 'Revenue by Best Selling Products'
                    }
                }
            }
        });
    } else {
        // Hide the chart canvas if there's no data
        chartCanvas.style.display = 'none';
    }
});