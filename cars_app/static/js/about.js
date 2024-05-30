// $(document).ready(function() {
//     function countUp(element, endValue, duration) {
//         let startValue = 0;
//         let increment = endValue / (duration / 10);

//         function updateCount() {
//             startValue += increment;
//             element.text(Math.ceil(startValue));
//             if (startValue < endValue) {
//                 setTimeout(updateCount, 10);
//             } else {
//                 element.text(endValue);
//             }
//         }

//         updateCount();
//     }

//     countUp($('#sales'), 1532, 2000);   
//     countUp($('#visitors'), 114323, 2000); 
//     countUp($('#contracts'), 367, 2000);  

//     const ctx = document.getElementById('salesChart').getContext('2d');
//     const salesChart = new Chart(ctx, {
//         type: 'line',
//         data: {
//             labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
//             datasets: [{
//                 label: 'Monthly Sales',
//                 data: [120, 150, 180, 220, 240, 200, 180, 210, 250, 280, 300, 320],
//                 backgroundColor: 'rgba(255, 152, 0, 0.2)',
//                 borderColor: '#ff9800',
//                 borderWidth: 2,
//                 fill: true,
//             }]
//         },
//         options: {
//             responsive: true,
//             scales: {
//                 x: {
//                     beginAtZero: true,
//                 },
//                 y: {
//                     beginAtZero: true,
//                 }
//             }
//         }
//     });
// });
