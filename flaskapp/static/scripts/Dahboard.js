$(document).ready(function () {
    switch (tab_name){
        case "dash": {setActiveTab('#dashboard');
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
        break};
        case "MyBooks": setActiveTab('#dookShelf'); break;
        case "Publish": setActiveTab('#publish'); break;
        case "my_account": setActiveTab('#account'); break;
    }
    
  
    
    $('#dashboard').click(function(event){
        window.location.href = "/dashboard/dash"
        setActiveTab(this)
        
    })
    $('#dookShelf').click(function(event){
        window.location.href = "/dashboard/MyBooks"
        setActiveTab(this)

    });
    $('#publish').click(function(event){
        window.location.href = "/dashboard/Publish"
        setActiveTab(this)
        

    });
    $('#account').click(function(event){
        window.location.href = "/dashboard/my_account"
        setActiveTab(this)
    });

    $('#edit-btn').click(function () {
        console.log("{{ book.id }}")
        
        fetch(`/get_book_data/${bookId}`)
        .then(response => response.json())
        .then(data => {
            // Populate form fields with fetched data
            document.querySelector('[name="title"]').value = data.title;
            document.querySelector('[name="subtitle"]').value = data.subtitle;
            document.querySelector('[name="description"]').value = data.description;
            document.querySelector('[name="genre"]').value = data.genre;
            document.querySelector('[name="price"]').value = data.price;
            // Add other fields as needed
        })
        .catch(error => console.error('Error fetching data:', error));

       
    });

    function setActiveTab(tab){
        $('.menu-item').each(function () {
            $(this).removeClass("active");
        });
         $(tab).addClass("active");

    }
  


});
