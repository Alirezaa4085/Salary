document.addEventListener("DOMContentLoaded", function() {
  // Fetch data from the server
  fetch('/get_monthly_totals/')
      .then(response => response.json())
      .then(data => {
          console.log('Fetched Data:', data);

          // Create the Area Chart with the fetched data
          var ctx = document.getElementById("myAreaChart").getContext("2d");
          var myAreaChart = new Chart(ctx, {
              type: 'line',
              data: {
                  labels: data.labels,
                  datasets: [{
                      label: "Earnings",
                      lineTension: 0.3,
                      backgroundColor: "rgba(78, 115, 223, 0.05)",
                      borderColor: "rgba(78, 115, 223, 1)",
                      pointRadius: 3,
                      pointBackgroundColor: "rgba(78, 115, 223, 1)",
                      pointBorderColor: "rgba(78, 115, 223, 1)",
                      pointHoverRadius: 3,
                      pointHoverBackgroundColor: "rgba(78, 115, 223, 1)",
                      pointHoverBorderColor: "rgba(78, 115, 223, 1)",
                      pointHitRadius: 10,
                      pointBorderWidth: 2,
                      data: [data.monthly_income_total], // Use the fetched monthly_income_total
                  }],
              },
              options: {
                  // Your chart options here
              },
          });
      })
      .catch(error => {
          console.error('Error fetching monthly totals:', error);
      });
});
