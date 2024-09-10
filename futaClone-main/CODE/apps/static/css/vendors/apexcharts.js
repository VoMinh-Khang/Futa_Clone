var options = {
    series: [{
        name: "Tickets",
        data: [40, 70, 20, 90, 36, 80, 30, 91, 60]
    }, {
        name: "Customer",
        data: [20, 30, 90, 40, 56, 20, 70, 21, 10]
    }],
    colors: ['#ff6855', '#009344'],
    chart: {
        height: 260,
        type: 'line',
    },
    dataLabels: {
        enabled: false
    },
    stroke: {
        curve: 'smooth'
    },
    title: {
        text: 'Tickets and Customer by Month',
        align: 'left'
    },
    grid: {
        row: {
            colors: ['transparent', 'transparent'], // takes an array which will be repeated on columns
            opacity: 0.5
        },
    },
    xaxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep'],
    },
    legend: {
        position: 'top'
    },

    title: {
        text: 'Charts',
        align: 'left',
        margin: 10,
        offsetX: 0,
        offsetY: 0,
        floating: false,
        style: {
            fontSize: '16px',
            fontWeight: '700',
            fontFamily: 'SFProVietsub',
            color: '#333333'
        },
    }
};

var chart = new ApexCharts(document.querySelector(".performance-chart"), options);
chart.render();

var option_pie = {
    series: [53, 55, 59, 17, 10],
    labels: ['Ticket', 'Express', 'Package', 'Invest', 'Other'],
    chart: {
        type: 'donut',
        height: 280,
    },
    dataLabels: {
        enabled: true,
        style: {
            fontSize: '10px',
            fontWeight: '100',
            color: '#333333',
            fontFamily: 'SFProVietsub',
        },
    },
    colors: ['#d486db', '#ffc979', '#79bfff', '#009344', '#ff4848'],
    title: {
        text: 'Income StatisticIncome',
        align: 'left',
        style: {
            fontSize: '16px',
            fontWeight: '700',
            fontFamily: 'SFProVietsub',
            color: '#333333',
        },
    },
    legend: {
        offsetY: 0,
        position: 'bottom',
    }
};

var chart_pie = new ApexCharts(document.querySelector(".performance-pie"), option_pie);
chart_pie.render();