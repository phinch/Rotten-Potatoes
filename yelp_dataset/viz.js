$("document").ready(function(){
    document.getElementById("pricebutton").addEventListener("click", price_function);
    document.getElementById("categorybutton").addEventListener("click", cat_function);
    $(".category").hide();
    $(".price").hide();
    $(".category").change(check_cat);
    $(".price").change(check_price);
    function price_function() {
        $(".price").show();
        $(".category").hide();
        var dataset = [];
        var height = 800;
        var width = 500;

        d3.csv("avgs_by_price.csv", function(input){
            for(var i in input){
                console.log(input[i]["Average"])
                input[i]["Name"] = input[i]["Price"];
                dataset.push(input[i]);
            }
            
           draw_grid(dataset, height, width);
        });
    }
    function cat_function() {
        $(".category").show();
        $(".price").hide();
        var dataset = [];
        var height = 800;
        var width = 1600;

        d3.csv("avg_by_genre.csv", function(input){
            for(var i in input){
                console.log(input[i]["Average"])
                input[i]["Name"] = input[i]["Genre"];
                dataset.push(input[i]);
            }
            
           draw_grid(dataset, height, width);
        });
    }

    function check_cat(){
        var checked = new Set();
        $(".category").each(function(index, value){
            if(value.children[0].checked){
                checked.add(value.children[0].value);
            }
        });

        var dataset = [];
        var height = 800;
        var width = 1600;

        d3.csv("avg_by_genre.csv", function(input){
            for(var i in input){
                input[i]["Name"] = input[i]["Genre"];
                if (checked.has(input[i]["Genre"])){
                    dataset.push(input[i]);
                }
            }
            
           draw_grid(dataset, height, width);
        });
    }

    function check_price(){
        var checked = new Set();
        $(".price").each(function(index, value){
            if(value.children[0].checked){
                checked.add(value.children[0].value);
            }
        });

        var dataset = [];
        var height = 800;
        var width = 500;

        console.log(checked);

        d3.csv("avgs_by_price.csv", function(input){
            for(var i in input){
                input[i]["Name"] = input[i]["Price"];
                console.log(input[i]["Price"]);
                if (checked.has(input[i]["Price"])){
                    dataset.push(input[i]);
                }
            }

            console.log(dataset);
            
           draw_grid(dataset, height, width);
        });
    }

    function draw_grid(dataset, height, width){
        var count;

        $("#viz").remove();

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

        for(var i = 1; i <= 5; i++){
            viz.append("text")
                .text(i)
                .attr("x", 5)
                .attr("y", (height-50)/5*(5-i))
                .attr("font-size", "15px");
        }

        for (var i = 0; i < dataset.length; i++){
            viz.append("text")
                .text(dataset[i]["Name"])
                .style("display", "inline-block")
                .attr("x", ((width-20)/dataset.length) * i + 20)
                .attr("y", height-10)
                .attr("font-size", "15px");

            viz.append("rect")
                .attr("height", 150*parseFloat(dataset[i]["Average"]))
                .attr("width", width/dataset.length - 30)
                .attr("x", ((width-20)/dataset.length) * i + 20)
                .attr("y", height-50 - (150 * parseFloat(dataset[i]["Average"])))
                .attr("fill", "black");
        }
    }
});
