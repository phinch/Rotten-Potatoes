var colors = ["#E3A93C", "#99D8C7", "#FCECDC", "#F29D9C", "#E2639A"]
//Palette credit: ghake's Warm Rainbow on colourlovers.com

//This visualization takes place within the context of a circle. Specify the center here.
var centerx = 500;
var centery = 500;
var radius = 500;

$("document").ready(function(){
    //Category,Event Name,Gender,Age,Marital Status,Session ID,Device,Client Time,City,State,Latitude,Longitude,Zip Code
    var dataset = [];
    var cities = new Array(); //Associative Array <String, Array>
    var categories = new Array(); //Associative <String, Integer>
    var datapoint;
    var dollars = 0;
    var pixels = radius*Math.PI*5/12;
    var citycount = 0;

    var height = 500;
    var width = 500;

    d3.csv("avgs_by_price.csv", function(input){
        for(var i in input){
            dataset.push(input[i]);
        }
        
        var count;

        //Draw the axes
        d3.select("#content").append("svg")
            .attr("height", height)
            .attr("width", width)
            .attr("id", "viz")

        d3.select("#viz").append("line")
            .attr("x1", 20)
            .attr("y1", 20)
            .attr("x2", 20)
            .attr("y2", height - 20)
            .attr("stroke-width", 2)
            .attr("stroke", "black");

        d3.select("#viz").append("line")
            .attr("x1", 20)
            .attr("y1", 20)
            .attr("x2", width - 20)
            .attr("y2", 20)
            .attr("stroke-width", 2)
            .attr("stroke", "black");

        for (var i = 0; i < dataset.length; i++){
            d3.select("#viz").append("p")
                .text(dataset["Price"])
                .style("display", "inline-block")
                .attr("x", ((width-20)/dataset.length))
                .attr("y", height-10);

            d3.select("#viz").append("svg")
                .attr("height", 90*dataset["Average"])
                .attr("width", width/6)
                .attr("x", ((width-20)/dataset.length)
                .attr("y", height-20);
        }
    });
});
