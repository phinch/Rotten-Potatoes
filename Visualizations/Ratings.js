$("document").ready(function(){
    var reviews = new Object(); //<Restaurant Name, Reviews>
    var dsv = d3.dsv("|", "text/plain");
    var nsv = d3.dsv("\n", "text/plain");
    var times = [2007, 2015]; //TODO: Find a way to get min and max times
    var permonth = 11;

    var months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    var darkness = ["#dddddd", "#cccccc", "#bbbbbb", "#aaaaaa", "#999999", "#888888", "#777777"]

        var years = times[1]-times[0]+1;
        var width = years * 12 * permonth;
                

        //Draw the axes and captions
        var svg = d3.select("#content").append("svg")
                    .attr("width", width + 200)
                    .attr("height", 700)
                    .attr("id", "viz")
                    .style("background", "#eeeeee");

        svg.append("path")
            .attr("d", "M100,50 L100,650 L"+(width+100)+",650")
            .attr("stroke", "#444444")
            .attr("stroke-width", 1)
            .attr("fill", "none");

        //Horizontal Captions
        for(var i = 0; i <= years; i++){
            svg.append("text")
                .classed("caption", true)
                .text(times[0]+i)
                .attr("y", 675)
                .attr("x", 100+(i*permonth*12))
                .attr("text-anchor", "middle");
        }

        //Vertical Captions
        var text = "*";
        for(var i = 1; i <= 5; i++){
            var height = 675 - (i*120);
            svg.append("text")
                .classed("caption", true)
                .text(text)
                .attr("y", height)
                .attr("x", 90)
                .attr("text-anchor", "end");

            svg.append("path")
                .attr("d", "M100,"+(height-10)+" L"+(width+100)+","+(height-10))
                .attr("stroke", "#cccccc")
                .attr("stroke-width", 1);

            text += "*";
        }

    nsv('../Rotten-Potatoes/data/opentable_names.txt', function(names) {
        for (var k in names[0]){
            var key = k;
            var newo = new Array();
            newo[key] = key;
            names.push(newo);
        }
        for (var i in names){
            var restaurant = names[i][key].replace("data/opentable_csvs/", "");
            reviews[restaurant] = new Object();
            var path = "../Rotten-Potatoes/"+names[i][key]+".csv";
            readCsv(path, restaurant, times);
        }
    });

    function readCsv(path, restaurant, times){
        dsv(path, function(input){ //Review Title|Review Date|Review Score|Review Text
            for(var i in input){
                if(input[i]["Review Title"] == "ays ago" || input[i]["Review Title"].substring(0, 5) == "Dined"){
                    continue;
                }
                
                var score = input[i]["Review Score"];
                var date = input[i]["Review Title"].split(" ") //Month Day, Year
                var timeid = date[2] + date[0]; //YearMonth

                if(!(timeid in reviews[restaurant])){
                    reviews[restaurant][timeid] = score.toString() + "/1";
                }else{
                    var avg = reviews[restaurant][timeid].split("/");
                    var newtop = (parseInt(avg[0])+parseInt(score)).toString();
                    var newbot = (parseInt(avg[1])+1).toString();
                    reviews[restaurant][timeid] = newtop+"/"+newbot;
                }

            }
            lineDraw(restaurant, reviews[restaurant]);
        });
    }

    function lineDraw(restaurant, reviews){
        var timeid;
        var y;
        var x = 100;
        var first = true;

        for(var year = 2007; year <= 2016; year++){
            for(var m = 0; m <= 11; m++){
                timeid = year +months[m];
                if(!(timeid in reviews)){
                    continue;
                }

                var frac = reviews[timeid].split("/");

                if(first){
                    y = parseInt(frac[0])/parseInt(frac[1]);
                    y = 665 - y*120;
                    first = false;
                }else{
                    var dark = parseInt(frac[1]);
                    if (dark >= darkness.length){
                        dark = darkness.length-1;
                    }
                    var oldx = x;
                    var oldy = y;
                    var d = "M"+x+","+y+" L";
                    y = parseInt(frac[0])/parseInt(frac[1]);
                    y = 665 - y*120;
                    x += 11;
                    d += x+","+y;

                    var classname = restaurant.replace(/[.,\/#!$%\^&\*;:{}=\-_~()'' ]/g,"");
    
                    svg.append("path")
                        .attr("d", d)
                        .attr("stroke", darkness[dark])
                        .attr("stroke-width", 1)
                        .attr("fill", "none")
                        .classed(classname+" line", true)
                        .append("svg:title")
                        .text(genTooltip(restaurant, d, year, months[m]));
                }
            }
        }

        //Add tooltips and hovering
        $(".line").on("mouseenter", function(event){
            var restaurant = $(event.target).attr("class");
            $("."+restaurant.split(" ")[0]).attr("stroke-width", 3);
        });
        $(".line").on("mouseleave", function(event){
            var restaurant = $(event.target).attr("class");
            $("."+restaurant.split(" ")[0]).attr("stroke-width", 1);
        });
    }
    
    function genTooltip(restaurant, path, year, month){
        var tool = restaurant + ", "+month+" "+year+"\nAverage Rating: ";
        //path is in form "Mx,y Lx,y
        console.log(path);
        var ml = path.split(" ");
        var y2 = ml[1].split(",")[1];
        console.log(ml, y2);
        var rating = (parseInt(y2)-665)/-120;
        tool += Math.round(rating * 100) / 100;
        return tool;
    }
});
