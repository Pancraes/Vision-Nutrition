function graph(xaxis, yaxis, zvals) {
  let data = [];
    for (let i = 0; i < xaxis.length; i++) {
      data.push({x: xaxis[i], y: yaxis[i], name: zvals[i]});
    }
  let ctx = document.getElementById('myChart');

  // Create data
  const datas = {
    datasets: [{
      label: 'League of Legends',
      data: data,
      backgroundColor: 'rgb(255, 99, 132)',
      borderColor: 'rgb(255, 99, 132)',
      fill: false,
      trendlineLinear: {
        style: "rgb(43 ,66 ,255, 0.3)",
        lineStyle: "solid",
        width: 3
      }
    }],
  };

  // Plugin for labels on scatter points
  const scatterDataLabels = {
    id: 'scatterDataLabels',
    afterDatasetsDraw(chart,args,options) {
      const { ctx } = chart;
      ctx.save();
      ctx.font = '12px sans-serif';
      for (let i = 0; i < chart.config.data.datasets[0].data.length; i++) {
        const textWidth = ctx.measureText(chart.config.data.datasets[0].data[i].name).width;
        ctx.fillText(chart.config.data.datasets[0].data[i].name, chart.
          getDatasetMeta(0).data[i].x - (textWidth/2), chart.getDatasetMeta(0).data[i].y - 10)
      }
    }
  }

  // config
  const config = {
    type: 'scatter',
    data: datas,
    options: {
      maintainAspectRatio: true,
      aspectRatio: 2.2,
      radius: 5,
      hoverRadius: 7,
      scales: {
        x: {
          title: {
            display: true,
            text: 'Summoner Level',
            font: {
              size: 20
            }
          }
        },
        y: {
          title: {
            display: true,
            text: 'Mastery Accumulated on Champion',
            font: {
              size: 20
            }
          }
        }
      }
    },
    plugins: [scatterDataLabels]
  };

  const myChart = new Chart(ctx, config);
}
