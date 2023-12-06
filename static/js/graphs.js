// graphs.js
function renderGraph(canvasId, data, options) {
    var ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line', // Change as needed
        data: data,
        options: options
    });
}

// Dummy data for the 7-day overview graph
var sevenDayData = {
    labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7'],
    datasets: [{
        label: 'Daily PnL',
        data: [12, 19, 3, 5, 2, 3, 10],
        backgroundColor: 'rgba(0, 123, 255, 0.5)',
        borderColor: 'rgba(0, 123, 255, 1)',
        borderWidth: 1
    }]
};

var sevenDayOptions = {
    scales: {
        y: {
            beginAtZero: true
        }
    }
};

window.onload = function() {
    renderGraph('sevenDayGraph', sevenDayData, sevenDayOptions);
};
