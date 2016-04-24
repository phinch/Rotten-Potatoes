$("document").ready(function(){
    //Category,Event Name,Gender,Age,Marital Status,Session ID,Device,Client Time,City,State,Latitude,Longitude,Zip Code
    var dataset = [];
    var height = 500;
    var width = 500;

    d3.csv("avgs_by_price.csv", function(input){
        for(var i in input){
            console.log(input[i]["Average"])
            dataset.push(input[i]);
        }
        
        var count;

        //Draw the axes
        var viz = d3.select("#content").append("svg")
            .attr("height", height)
            .attr("width", width)
            .attr("id", "viz")

        d3.select("#viz").append("line")
            .attr("x1", 20)
            .attr("y1", 20)
            .attr("x2", 20)
            .attr("y2", height - 50)
            .attr("stroke-width", 2)
            .attr("stroke", "black");

        d3.select("#viz").append("line")
            .attr("x1", 20)
            .attr("y1", height-50)
            .attr("x2", width - 20)
            .attr("y2", height-50)
            .attr("stroke-width", 2)
            .attr("stroke", "black");

        for (var i = 0; i < dataset.length; i++){
            viz.append("text")
                .text(dataset[i]["Price"])
                .style("display", "inline-block")
                .attr("x", ((width-20)/dataset.length) * i + 20)
                .attr("y", height-10)
                .attr("font-size", "30px");

            viz.append("rect")
                .attr("height", 90*parseFloat(dataset[i]["Average"]))
                .attr("width", width/6)
                .attr("x", ((width-20)/dataset.length) * i + 20)
                .attr("y", height-50 - (90 * parseFloat(dataset[i]["Average"])))
                .attr("fill", "black");
        }
    });
});
