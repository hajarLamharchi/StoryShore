$(document).ready(function () {
    loadDash();
    setActiveTab('#dashboard')
    $('#dashboard').click(function(event){
        loadDash();
        
    })
    $('#dookShelf').click(function(event){
        fetchData('MyBooks');
        setActiveTab(this)

    });
    $('#publish').click(function(event){
        fetchData('Publish');
        setActiveTab(this)
        

    });
    $('#account').click(function(event){
        fetchData('my_account');
        setActiveTab(this)
    });

    function fetchData(file_name){
        fetch('/dashboard/'+file_name)
        .then(response => response.text())
        .then(text => {
            document.querySelector('.content-container').innerHTML = text;
        });
    }
    function setActiveTab(tab){
        $('.menu-item').each(function () {
            $(this).removeClass("active");
        });
         $(tab).addClass("active");

    }
    function loadDash(){
        fetch('/dashboard/dash')
        .then(response => response.text())
        .then(text => {
            document.querySelector('.content-container').innerHTML = text;

            // Initialize Chart.js after the content is loaded
            var ctx = document.getElementById('myChart').getContext('2d');

            const xValues = ["Italy", "France", "Spain", "USA", "Argentina"];
            const yValues = [55, 49, 44, 24, 15];
            const barColors = ["red", "green", "blue", "orange", "brown"];

            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ["11/02/2022", "22/03/2022", "22/04/2022", "22/05/2022", "22/06/2022", "22/07/2022", "22/08/2022", "22/09/2022", "22/10/2022"],
                    datasets: [{
                        label: 'book1',
                        backgroundColor: "#FDD3A2",
                        data: [1, 10, 5, 11, 8, 12, 0, 14, 9],
                    }, {
                        label: 'book2',
                        backgroundColor: "#F5A476",
                        data: [12, 14, 5, 11, 13, 12, 2, 13, 5],
                    }, {
                        label: 'book3',
                        backgroundColor: "#F5C669",
                        data: [5, 3, 5, 11, 20, 12, 4, 6, 6],
                    }, {
                        label: 'book4',
                        backgroundColor: "#F5DA78",
                        data: [20, 7, 5, 17, 13, 12, 17, 3, 11],
                    }],
                },
                options: {
                    tooltips: {
                        displayColors: true,
                        callbacks: {
                            mode: 'x',
                        },
                    },
                    scales: {
                        xAxes: [{
                            stacked: true,
                            gridLines: {
                                display: false,
                            }
                        }],
                        yAxes: [{
                            stacked: true,
                            ticks: {
                                beginAtZero: true,
                            },
                            type: 'linear',
                        }]
                    },
                    responsive: true,
                    legend: { position: 'bottom' },
                }
            });
        });
    }
});
