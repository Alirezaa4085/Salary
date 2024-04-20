// داده‌های نمودار میله‌ای
const barLabels = ["Label1", "Label2", "Label3", "Label4"];
const barData = [50, 75, 120, 90];

// داده‌های نمودار خطی
const lineLabels = ["Label1", "Label2", "Label3", "Label4"];
const lineData = [30, 45, 80, 60];

// تنظیمات نمودار میله‌ای
const barCtx = document.getElementById('barChart').getContext('2d');
const barChart = new Chart(barCtx, {
  type: 'bar',
  data: {
    labels: barLabels,
    datasets: [{
      label: 'نمودار میله‌ای',
      data: barData,
      backgroundColor: 'rgba(75, 192, 192, 0.6)',
      borderColor: 'rgba(75, 192, 192, 1)',
      borderWidth: 1
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});

// تنظیمات نمودار خطی
const lineCtx = document.getElementById('lineChart').getContext('2d');
const lineChart = new Chart(lineCtx, {
  type: 'line',
  data: {
    labels: lineLabels,
    datasets: [{
      label: 'نمودار خطی',
      data: lineData,
      fill: false,
      borderColor: 'rgba(255, 99, 132, 1)',
      borderWidth: 2
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
    }
  }
});