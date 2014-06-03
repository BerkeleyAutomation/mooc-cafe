function gender(){

    var width = 710,
    height = 404,
    radius = Math.min(width, height) / 2;

    var color = d3.scale.ordinal()
    .range(["#8da0cb", "#fc8d62","#66c2a5"]);

    var arc = d3.svg.arc()
    .outerRadius(radius - 10)
    .innerRadius(0);

    var pie = d3.layout.pie()
    .sort(null)
    .value(function(d) { return d.number; });

    var svg = d3.select("#gender").append("svg")
    .attr("width", '100%')
    .attr("height", '100%')
    //.attr('viewBox','0 0 '+Math.min(width,height)+' '+Math.min(width,height))
    //.attr('preserveAspectRatio','xMinYMin')
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + Math.min(width,height) / 2 + ")");

    d3.csv("../media/mobile/stats_data/gender.csv", function(error, data) {
       var total= d3.sum(data, function(d){return d.number;});
       
       data.forEach(function(d) {
                    d.number = +d.number;
                    });
       
       var g = svg.selectAll(".arc")
       .data(pie(data))
       .enter().append("g")
       .attr("class", "arc");
       
       g.append("path")
       .attr("d", arc)
       .style("fill", function(d) { return color(d.data.gender); });
       
       g.append("text")
       .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
       .attr("dy", ".35em")
       .style("text-anchor", "middle")
       .text(function(d) { return (d.data.gender + " "+d3.round(100*d.data.number/total,1) + "%"); });
       
           
       });
    
}

function issue1()
{
    var margin = {top: 20, right: 20, bottom: 10, left: 40},
    width = 710 - margin.left - margin.right,
    height = 420 - margin.top - margin.bottom;
    
    var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);
    
    var y = d3.scale.linear()
    .range([height, 0]);
    
    var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
    
    var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10, "%");
    
    var svg = d3.select("#issue1bar").append("svg")
    .attr("width", '100%')
    .attr("height", '100%')
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    d3.csv("../media/mobile/stats_data/issue1.csv", type, function(error, data) {
           x.domain(data.map(function(d) { return d.score; }));
           y.domain([0, d3.max(data, function(d) { return d.frequency; })]);
           
           svg.append("g")
           .attr("class", "x axis")
           .attr("transform", "translate(0," + height + ")")
           .call(xAxis);
           
           svg.append("g")
           .attr("class", "y axis")
           .call(yAxis)
           .append("text")
           .attr("transform", "rotate(-90)")
           .attr("y", 6)
           .attr("dy", ".71em")
           .style("text-anchor", "end")
           .text("Frequency");
           
           svg.selectAll(".bar")
           .data(data)
           .enter().append("rect")
           .attr("class", "bar")
           .attr("x", function(d) { return x(d.score); })
           .attr("width", x.rangeBand())
           .attr("y", function(d) { return y(d.frequency); })
           .attr("height", function(d) { return height - y(d.frequency); });
           
           });
    
    function type(d) {
        d.frequency = +d.frequency;
        return d;
    }
    
}


function issue2()
{
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 710 - margin.left - margin.right,
    height = 420 - margin.top - margin.bottom;
    
    var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);
    
    var y = d3.scale.linear()
    .range([height, 0]);
    
    var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
    
    var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10, "%");
    
    var svg = d3.select("#issue2bar").append("svg")
    .attr("width", '100%')
    .attr("height", '100%')
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    d3.csv("../media/mobile/stats_data/issue2.csv", type, function(error, data) {
           x.domain(data.map(function(d) { return d.score; }));
           y.domain([0, d3.max(data, function(d) { return d.frequency; })]);
           
           svg.append("g")
           .attr("class", "x axis")
           .attr("transform", "translate(0," + height + ")")
           .call(xAxis);
           
           svg.append("g")
           .attr("class", "y axis")
           .call(yAxis)
           .append("text")
           .attr("transform", "rotate(-90)")
           .attr("y", 6)
           .attr("dy", ".71em")
           .style("text-anchor", "end")
           .text("Frequency");
           
           svg.selectAll(".bar")
           .data(data)
           .enter().append("rect")
           .attr("class", "bar")
           .attr("x", function(d) { return x(d.score); })
           .attr("width", x.rangeBand())
           .attr("y", function(d) { return y(d.frequency); })
           .attr("height", function(d) { return height - y(d.frequency); });
           
           });
    
    function type(d) {
        d.frequency = +d.frequency;
        return d;
    }
    
}


function issue3()
{
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 710 - margin.left - margin.right,
    height = 420 - margin.top - margin.bottom;
    
    var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);
    
    var y = d3.scale.linear()
    .range([height, 0]);
    
    var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
    
    var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10, "%");
    
    var svg = d3.select("#issue3bar").append("svg")
    .attr("width", '100%')
    .attr("height", '100%')
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    d3.csv("../media/mobile/stats_data/issue3.csv", type, function(error, data) {
           x.domain(data.map(function(d) { return d.score; }));
           y.domain([0, d3.max(data, function(d) { return d.frequency; })]);
           
           svg.append("g")
           .attr("class", "x axis")
           .attr("transform", "translate(0," + height + ")")
           .call(xAxis);
           
           svg.append("g")
           .attr("class", "y axis")
           .call(yAxis)
           .append("text")
           .attr("transform", "rotate(-90)")
           .attr("y", 6)
           .attr("dy", ".71em")
           .style("text-anchor", "end")
           .text("Frequency");
           
           svg.selectAll(".bar")
           .data(data)
           .enter().append("rect")
           .attr("class", "bar")
           .attr("x", function(d) { return x(d.score); })
           .attr("width", x.rangeBand())
           .attr("y", function(d) { return y(d.frequency); })
           .attr("height", function(d) { return height - y(d.frequency); });
           
           });
    
    function type(d) {
        d.frequency = +d.frequency;
        return d;
    }
    
}


function issue4()
{
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 710 - margin.left - margin.right,
    height = 420 - margin.top - margin.bottom;
    
    var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);
    
    var y = d3.scale.linear()
    .range([height, 0]);
    
    var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
    
    var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10, "%");
    
    var svg = d3.select("#issue4bar").append("svg")
    .attr("width", '100%')
    .attr("height", '100%')
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    d3.csv("../media/mobile/stats_data/issue4.csv", type, function(error, data) {
           x.domain(data.map(function(d) { return d.score; }));
           y.domain([0, d3.max(data, function(d) { return d.frequency; })]);
           
           svg.append("g")
           .attr("class", "x axis")
           .attr("transform", "translate(0," + height + ")")
           .call(xAxis);
           
           svg.append("g")
           .attr("class", "y axis")
           .call(yAxis)
           .append("text")
           .attr("transform", "rotate(-90)")
           .attr("y", 6)
           .attr("dy", ".71em")
           .style("text-anchor", "end")
           .text("Frequency");
           
           svg.selectAll(".bar")
           .data(data)
           .enter().append("rect")
           .attr("class", "bar")
           .attr("x", function(d) { return x(d.score); })
           .attr("width", x.rangeBand())
           .attr("y", function(d) { return y(d.frequency); })
           .attr("height", function(d) { return height - y(d.frequency); });
           
           });
    
    function type(d) {
        d.frequency = +d.frequency;
        return d;
    }
    
}


function issue5()
{
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 710 - margin.left - margin.right,
    height = 420 - margin.top - margin.bottom;
    
    var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);
    
    var y = d3.scale.linear()
    .range([height, 0]);
    
    var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
    
    var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10, "%");
    
    var svg = d3.select("#issue5bar").append("svg")
    .attr("width", '100%')
    .attr("height", '100%')
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    d3.csv("../media/mobile/stats_data/issue5.csv", type, function(error, data) {
           x.domain(data.map(function(d) { return d.score; }));
           y.domain([0, d3.max(data, function(d) { return d.frequency; })]);
           
           svg.append("g")
           .attr("class", "x axis")
           .attr("transform", "translate(0," + height + ")")
           .call(xAxis);
           
           svg.append("g")
           .attr("class", "y axis")
           .call(yAxis)
           .append("text")
           .attr("transform", "rotate(-90)")
           .attr("y", 6)
           .attr("dy", ".71em")
           .style("text-anchor", "end")
           .text("Frequency");
           
           svg.selectAll(".bar")
           .data(data)
           .enter().append("rect")
           .attr("class", "bar")
           .attr("x", function(d) { return x(d.score); })
           .attr("width", x.rangeBand())
           .attr("y", function(d) { return y(d.frequency); })
           .attr("height", function(d) { return height - y(d.frequency); });
           
           });
    
    function type(d) {
        d.frequency = +d.frequency;
        return d;
    }
    
}

function college()
{
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 710 - margin.left - margin.right,
    height = 420 - margin.top - margin.bottom;
    
    var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);
    
    var y = d3.scale.linear()
    .range([height, 0]);
    
    var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
    
    var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10, "%");
    
    var svg = d3.select("#college").append("svg")
    .attr("width", '100%')
    .attr("height", '100%')
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    d3.csv("../media/mobile/stats_data/college.csv", type, function(error, data) {
           x.domain(data.map(function(d) { return d.year; }));
           y.domain([0, d3.max(data, function(d) { return d.frequency; })]);
           
           svg.append("g")
           .attr("class", "x axis")
           .attr("transform", "translate(0," + height + ")")
           .call(xAxis);
           
           svg.append("g")
           .attr("class", "y axis")
           .call(yAxis)
           .append("text")
           .attr("transform", "rotate(-90)")
           .attr("y", 6)
           .attr("dy", ".71em")
           .style("text-anchor", "end")
           .text("Frequency");
           
           svg.selectAll(".bar")
           .data(data)
           .enter().append("rect")
           .attr("class", "bar")
           .attr("x", function(d) { return x(d.year); })
           .attr("width", x.rangeBand())
           .attr("y", function(d) { return y(d.frequency); })
           .attr("height", function(d) { return height - y(d.frequency); });
           
           });
    
    function type(d) {
        d.frequency = +d.frequency;
        return d;
    }
    
}


function age()
{
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 710 - margin.left - margin.right,
    height = 420 - margin.top - margin.bottom;
    
    var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);
    
    var y = d3.scale.linear()
    .range([height, 0]);
    
    var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");
    
    var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10, "%");
    
    var svg = d3.select("#age").append("svg")
    .attr("width", '100%')
    .attr("height", '100%')
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
    d3.csv("../media/mobile/stats_data/age.csv", type, function(error, data) {
           x.domain(data.map(function(d) { return d.age; }));
           y.domain([0, d3.max(data, function(d) { return d.frequency; })]);
           
           svg.append("g")
           .attr("class", "x axis")
           .attr("transform", "translate(0," + height + ")")
           .call(xAxis);
           
           svg.append("g")
           .attr("class", "y axis")
           .call(yAxis)
           .append("text")
           .attr("transform", "rotate(-90)")
           .attr("y", 6)
           .attr("dy", ".71em")
           .style("text-anchor", "end")
           .text("Frequency");
           
           svg.selectAll(".bar")
           .data(data)
           .enter().append("rect")
           .attr("class", "bar")
           .attr("x", function(d) { return x(d.age); })
           .attr("width", x.rangeBand())
           .attr("y", function(d) { return y(d.frequency); })
           .attr("height", function(d) { return height - y(d.frequency); });
           
           });
    
    function type(d) {
        d.frequency = +d.frequency;
        return d;
    }
    
}

issue1();
issue2();
issue3();
issue4();
issue5();
gender();
college();
age();

