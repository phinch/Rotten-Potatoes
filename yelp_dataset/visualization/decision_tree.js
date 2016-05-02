$("document").ready(function(){
    //Draw lines from tier to tier iteratively
    //Note: For each button in one tier, we get the two corresponding buttons in the next tier and draw a path with text saying either Yes/No
    var numTiers = 3; //Constant, does not include the classifier tier
    var header = 77; //Put pixel height above the svg here
    var buttonheight = 40;
    var buttonwidth = 120; //Put in new values if they change

    $("#tree").attr("width", $("#tier1").width());
    $("#tree").attr("height", (numTiers + 1) * $("#tier1").height());

    //Draw paths from node to node
    for(var i = 1; i <= numTiers; i++){
        $("#tier"+i+" .node").each(function(index) {
            var parentid = $(this).parent().attr("id");
            var parenttier = parseInt(parentid.charAt(4));
            //For some index, we want to draw lines to the next tier's index*2 and (index*2+1)
            var myy = $(this).position()["top"] + 40 - header;
            if($(this).css("margin") == "0px"){
                var myx = $(this).position()["left"] + buttonwidth/2;
            }else{
                var myx = $(this).position()["left"] + buttonwidth/2 + parseInt($(this).css("margin").split(" ")[1].split('p')[0]);
            }

            for(var c = index*2; c <= index*2+1; c++){
                var child = $("#tier"+(parenttier+1)).children().eq(c);
                var childy = child.position()["top"] - header;
                var childx = child.position()["left"] + child.width()/2 + 6 + parseInt(child.css("margin").split(" ")[1].split('p')[0]);

                var middlex = (myx + childx)/2;
                var middley = (myy + childy)/2;

                var text = "Yes";
                var color = "#a3ff89";

                if(c%2 == 0){
                    text = "No";
                    var color = "#ffaa81";
                }

                d3.select("#tree").append("path")
                    .attr("d", "M"+myx+" "+myy+" L"+childx+" "+childy)
                    .attr("stroke", color);

                d3.select("#tree").append("text")
                    .text(text)
                    .attr("y", middley)
                    .attr("x", middlex)
                    .attr("text-anchor", "middle")
                    .classed("yesno", true);
            }
            
        });
    }
    //The tree is now fully drawn.

    //Let's add a tooltip for each bubble. I guess. //TODO
    //An attempt to read information from the dot file:
    var treedata = [];
    var treelinks = [];
    var treelines = []
    d3.text("../dt_graphic_representation/DT_undersampled.dot", function(text){
        var lines = text.split("\n");
        treedata[0] = $("#tier1").children().eq(0);
        //First, map the nodes of the tree
        for(var i = 0; i < lines.length; i++){
            var line = lines[i];
            if(line.charAt(2) == "-" && line.charAt(3) == ">"){
                var parenttier = treedata[line.charAt(0)].parent().attr("id").charAt(4);
                var parentindex = treedata[line.charAt(0)].index();
                if(line.charAt(0) in treelinks){
                    treelinks[line.charAt(0)].push(line.charAt(5));
                    if(parenttier != numTiers){
                        var childindex = parentindex*2 + 1;
                        treedata[line.charAt(5)] = $("#tier"+(parenttier + 1)).children().eq(childindex);
                    }
                }else{
                    treelinks[line.charAt(0)] = [line.charAt(5)];
                    if(parenttier != numTiers){
                        var childindex = parentindex*2;
                        treedata[line.charAt(5)] = $("#tier"+(parenttier + 1)).children().eq(childindex);
                    }
                }
            }else if(line.charAt(3) == "["){
                treelines[line.charAt(0)] = line;
            }
        }

        //We now have all the information we need to create a tooltip for the thing
        for(var key in treedata){

        }
    });

/*
    //TODO: Clicking on parts of the tree?
    $(".node").on("mousemove", function(event){
        var id = event.target.id;
        d3.select("#"+id+"tool").transition().style("opacity", 1);
    });

    $(".node").on("mouseleave", function(event){
        var id = event.target.id;
        d3.select("#"+id+"tool").transition().style("opacity", 0);
    });

    //TODO: Scraper stuff
*/
});
