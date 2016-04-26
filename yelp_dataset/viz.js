$("document").ready(function(){
    categorymap = {
        "Sushi Bars": ["Japanese", "Asian", "Non-American", "Non-White"],
        "Japanese": ["Japanese", "Asian", "Non-American", "Non-White"],
        "Cantonese": ["Chinese", "Asian", "Non-American", "Non-White"],
        "Chinese": ["Chinese", "Asian", "Non-American", "Non-White"],
        "Thai": ["Thai", "Asian", "Non-American", "Non-White"],
        "Indian": ["Asian", "Non-American", "Non-White"],
        "Korean": ["Korean", "Asian", "Non-American", "Non-White"],
        "Pakistani": ["Asian", "Non-American", "Non-White"],
        "Mongolian": ["Asian", "Non-American", "Non-White"],
        "Asian Fusion": ["Asian", "Non-American", "Non-White"],
        "Vietnamese": ["Asian", "Non-American", "Non-White"],
        "Cambodian": ["Asian", "Non-American", "Non-White"],

        "French": ["French", "European", "Non-American"],
        "Creperies": ["French", "European", "Non-American"],
        "Italian": ["Italian", "European", "Non-American"],
        "Tapas/Small Plates": ["European", "Non-American"],
        "Tapas Bars": ["European", "Non-American"],
        "Irish": ["European", "Non-American"],
        "British": ["European", "Non-American"],
        
        "Bar": ["Bars"],
        "Dive Bar": ["Bars"],
        "Cocktail Bar": ["Bars"],
        "Dive Bars": ["Bars"],
        "Pub": ["Bars"],
        "Beer Bar": ["Bars"],
        "Bars": ["Bars"],
        "Pubs": ["Bars"],
        "Gastropubs": ["Bars"],
        "Wine Bars": ["Bars"],

        "Coffee & Tea": ["Cafes"],
        "Bubble Tea": ["Cafes"],
        "Cafes": ["Cafes"],
        "Cafe": ["Cafes"],
        "Juice Bar": ["Cafes"],

        "Steakhouses": ["American"],
        "American (New)": ["American"],
        "Breakfast and Brunch": ["Brunch", "American"],
        "Modern American": ["American"],
        "Traditional American": ["American"],
        "Steakhouse": ["American"],
        "Burgers": ["American"],
        "Diners": ["American"],
        "Fast Food": ["American"],
        "Hot Dogs": ["American"],
        "Seafood": ["American"],
        "American (Traditional)": ["American"],

        "Tex-Mex": ["Latin American", "Non-American", "Non-White"],
        "Cuban": ["Latin American", "Non-American", "Non-White"],
        "Cajun/Creole": ["Latin American", "Non-American", "Non-White"],
        "Latin American": ["Latin American", "Non-American", "Non-White"],
        "Mexican": ["Latin American", "Non-American", "Non-White"],

        "Mediterranean": ["Mediterranean", "Non-American", "Non-White"],
        "Moroccan": ["Mediterranean", "Non-American", "Non-White"],
        "Greek": ["Mediterranean", "Non-American", "Non-White"],
        "Middle Eastern": ["Mediterranean", "Non-American", "Non-White"],

        "Desserts": ["Dessert"],
        "Creperies": ["Dessert"],
        "Ice Cream & Frozen Yogurt": ["Dessert"],
        "Bakeries": ["Dessert"],
        "Bakery": ["Dessert"],
        "Donuts": ["Dessert"],

        "Bagels": ["Brunch"],

        "Food Stands": ["Food Trucks"],
        "Food Trucks": ["Food Trucks"],
        "Market Stall": ["Food Trucks"],

        "Ethiopian": ["Non-American", "Non-White"],

        "Pizza": ["Pizza"],
        "Sandwiches": ["Sandwiches"],
        "Delis": ["Sandwiches"]
    };
    $("#pricebutton").on("click", price_function);
    $("#categorybutton").on("click", cat_function);
    $("#combinebutton").on("click", combine_function);
    $(".category").hide();
    $(".price").hide();

    var true_avg = 3.74; //Constant value
    var redcolors = ["#fdd49e","#fc8d59","#d7301f","#7f0000"];
    var bluecolors = ["#DCDFE4", "#79B7C1", "#7A97B7", "#294461"]
    function price_function() {
        $(".price").on("change", check_price);
        $(".category").off("change", check_cat);
        $(".category").off("change", check_combo);
        $(".price").off("change", check_combo);
        $(".price").slideDown();
        $(".category").slideUp();
        var dataset = [];
        var height = 800;

        d3.csv("avgs_by_price.csv", function(input){
            for(var i in input){
                input[i]["Name"] = input[i]["Price"];
                dataset.push(input[i]);
            }

            width = 80*dataset.length;
            
            draw_grid(dataset, height, width);
        });
    }
    function cat_function() {
        $(".category").on("change", check_cat);
        $(".price").off("change", check_price);
        $(".category").off("change", check_combo);
        $(".price").off("change", check_combo);
        $(".category").slideDown();
        $(".price").slideUp();
        var dataset = [];
        var height = 800;

        d3.csv("avg_by_genre.csv", function(input){
            for(var i in input){
                input[i]["Name"] = input[i]["Genre"];
                dataset.push(input[i]);
            }

            width = 80*dataset.length;
            
            draw_grid(dataset, height, width);
        });
    }

    function combine_function(){
        //In anticipation of future additional filters, this function will calculate the data it needs from the raw business.txt.
        //(As such, future additional metrics should be added to business.txt.)
        //This could get gross.

        $(".category").slideDown();
        $(".price").slideDown();

        $(".category").off("change", check_cat);
        $(".price").off("change", check_price);
        $(".category").on("change", check_combo);
        $(".price").on("change", check_combo);

        check_combo();
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

        d3.csv("avg_by_genre.csv", function(input){
            for(var i in input){
                input[i]["Name"] = input[i]["Genre"];
                if (checked.has(input[i]["Genre"])){
                    dataset.push(input[i]);
                }
            }

            width = 80*dataset.length;
            
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

        d3.csv("avgs_by_price.csv", function(input){
            for(var i in input){
                input[i]["Name"] = input[i]["Price"];
                if (checked.has(input[i]["Price"])){
                    dataset.push(input[i]);
                }
            }

            width = 80*dataset.length;
            
            draw_grid(dataset, height, width);
        });
    }

    function check_combo(){
        //For now, we're combining price and genre.
        // i.e. By default, the genres will be displayed, filtered by price. (Ability to switch: TODO)
        //First, we'll find which cross-metrics we'll need by checking which checkboxes are checked (lol)
        var pricedata = [];
        var genredata = [];
        var alldata = [];
        var checked = new Set();
        var height = 800;

        $(".category").each(function(index, value){
            if(value.children[0].checked){
                checked.add(value.children[0].value);
            }
        });

        $(".price").each(function(index, value){
            if(value.children[0].checked){
                checked.add(value.children[0].value);
            }
        });

        d3.csv("avg_by_genre.csv", function(input){
            for(var i in input){
                input[i]["Name"] = input[i]["Genre"];
                if (checked.has(input[i]["Genre"])){
                    genredata.push(input[i]["Genre"]);
                }
            }

            width = 80*genredata.length;
            
            d3.csv("avgs_by_price.csv", function(input){
                for(var i in input){
                    input[i]["Name"] = input[i]["Price"];
                    if (checked.has(input[i]["Price"])){
                        pricedata.push(input[i]["Price"]);
                    }
                }



                var dsv = d3.dsv("|", "text/plain");
                console.log(pricedata, genredata);
                dsv("business.txt", function(input){
                    var genrehash = [];
                    for(var i in input){
                        //data needs to fit in both datasets
                        var pricenum = input[i]["price"];
                        var price = "";
                        for(var j = 0; j < parseInt(pricenum); j++){
                            price += "$";
                        }
                        if(pricedata.indexOf(price) == -1 || pricenum == "N/A"){
                            continue;
                        }
                        var categories = input[i]["genres"].split(" /// ");
                        var genres = [];
                        for(var j = 0; j < categories.length; j++){
                            var map = categorymap[categories[j]];
                            if(map != null){
                                for(var k = 0; k < map.length; k++){
                                    if(genres.indexOf(map[k]) == -1 && genredata.indexOf(map[k]) != -1){
                                        genres.push(map[k]);
                                    }
                                }
                            }
                        }

                        if(genres.length == 0){
                            continue;
                        }

                        var count = parseInt(input[i]["review_count"]);
                        var score = parseFloat(input[i]["avg score"])*count;
                        if(input[i]["avg score"] == "N/A"){
                            continue;
                        }
                        for(var g in genres){
                            if(genrehash[genres[g]] == null){
                                genrehash[genres[g]] = [g, score, count];
                            }else{
                                genrehash[genres[g]][1] += score;
                                genrehash[genres[g]][2] += count;
                            }
                        }
                    }
                    console.log(genredata, genrehash);
                    //Data needs to be in form [Name: xx, Average: xx], where name is the genre in this case.
                    for(var g in genredata){
                        if(genrehash[genredata[g]] != null){
                            var average = (genrehash[genredata[g]][1]/genrehash[genredata[g]][2]).toString();
                            alldata.push({"Name": genredata[g], "Average": average});
                        }
                    }
                    console.log(alldata);
                    draw_grid(alldata, height, width);
                });
            });
        });
    }

    function draw_grid(dataset, height, width){
        if(width >= 800){
            $("#content").css("overflow-x", "scroll");
        }else{
            $("#content").css("overflow-x", "hidden");
        }
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
                .attr("x", ((width-20)/dataset.length) * i + 30 + (width/dataset.length - 30)/2)
                .attr("y", height-10)
                .attr("font-size", "12px")
                .attr("width", ((width-20)/dataset.length))
                .style("word-wrap", "break-word")
                .attr("text-anchor", "middle");

            var bar = viz.append("rect")
                .attr("height", 0)
                .attr("width", width/dataset.length - 30)
                .attr("x", ((width-20)/dataset.length) * i + 30)
                .attr("y", 0)
                .attr("fill", "white")
                .classed("bar", true)
                .attr("id", "bar"+i);

            var barheight = 150*parseFloat(dataset[i]["Average"]);
            var y = height-50 - (((150/800)*height) * parseFloat(dataset[i]["Average"]));
            var color;
            if(parseFloat(dataset[i]["Average"]) < true_avg){
                var index = Math.ceil((true_avg - parseFloat(dataset[i]["Average"])*7)) - 1;
                if(index < 0){
                    index = 0;
                }else if(index > 3){
                    index = 3;
                }
                color = redcolors[index];
            }else{
                var index = Math.ceil((parseFloat(dataset[i]["Average"]-true_avg)*7)) - 1;
                if(index < 0){
                    index = 0;
                }else if(index > 3){
                    index = 3;
                }
                color = bluecolors[index];
            }
                

            d3.select("#"+"bar"+i).transition().attr("height", barheight).transition().attr("y", y).transition().attr("fill", color);
        }
    }
});
