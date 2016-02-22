/*global d3: false  */
"use strict";

//set up map
var w = 1500;
var h = 1000;


//map type & center point 
var projection = d3.geo.mercator()
    //.center([-47.109375, 34.664841])
    .translate([w/2-40, h/2-100])
    .scale((w/640)*95);

var path = d3.geo.path().projection(projection);

//initialize map
var svg = d3.select("#d3_map")
    .append("svg")
    .attr("width", w)
    .attr("height", h);

// seperating out the elements lets us organize the draw order
var country_group = svg.append("g");
var arcGroup = svg.append("g");
var point_group = svg.append("g");
var author_group = svg.append("g")


//reading geoJSON & CSV files
d3.json("../static/mainapp/js/countries.json", function(json){
    createMap(json);
});

var clearMap = function(){
	d3.selectAll(".arc").remove();
	d3.selectAll("circle").remove();

}

//draw world map
var createMap = function (json) {
    country_group.append("g")
        .selectAll("path")
        .data(json.features)
        .enter()
        .append("path")
        .attr("title", function(d) { return d.id; })
        .style("fill", "#43a2ca")
        .attr("d", path);
};

var createLinks = function (json) {
    var links = [];
    for(var i=0, len=json.length-1; i<len; i++){
        links.push({
            type: "LineString",
            no: json[i+1].no,
            coordinates: [
                [ json[0].lon, json[0].lat ],
                [ json[i+1].lon, json[i+1].lat ]
                ]
        });
    }
    return links;
};

// org dots on screen based on cities
var createPoints = function(json){
	var div = d3.select("body").append("div")	
    .attr("class", "tooltip")				
    .style("opacity", 0);
    
    point_group.selectAll("circle")
        .data(json.slice(1, json.length))
        .enter()
        .append("circle")
        .attr("cx", function(d) { return projection([d.lon, d.lat])[0]; })
        .attr("cy", function(d) { return projection([d.lon, d.lat])[1]; })
        .attr("org", function(d) { return d.org; })
        .attr("author", function(d) { return d.author; })
        .attr("no", function(d) { return d.no; })
        .attr("r", function(d) {return Math.sqrt(d3.select(this).attr("no"))*8;})
        .style("fill", "E7DF86")
        .style("opacity", "0.5")
        .on("mouseover", function(d) {		
            div.transition()		
                .duration(200)		
                .style("opacity", .9);		
            div	.html("<b>" + d3.select(this).attr("author") + "</b>" + "<br>"+"<b>" + d3.select(this).attr("org").split(",")[0] +"</b>")	
                .style("left", (d3.event.pageX) + "px")	
                .style("opacity","0.8")		
                .style("top", (d3.event.pageY - 28) + "px");
                
            })					
        .on("mouseout", function(d) {		
            div.transition()		
                .duration(500)		
                .style("opacity", 0);	
        });

    //functions for tweening the path
    var lineTransition = function lineTransition(path) {
        path.transition()
            .duration(3000)
            .attrTween("stroke-dasharray", tweenDash);
    };

    var tweenDash = function tweenDash() {
        var len = this.getTotalLength(),
            interpolate = d3.interpolateString("0," + len, len + "," + len);

        return function(t) { return interpolate(t); };
    };

    //assemble links from office locations
    var links = createLinks(json);

    author_group.append("svg:circle")
        .attr('cx', projection([json[0].lon, json[0].lat])[0])
        .attr('cy', projection([json[0].lon, json[0].lat])[1])
        .attr("r", 4)
        .attr("fill", "red")
        .style("opacity", 0.5)
        .style("stroke","white")
        .style("stroke-width",1)
        .on("mouseover", function(d) {
            div.transition()		
                .duration(200)		
                .style("opacity", .9);		
            div	.html("<b>" + json[0].author + "</b>" + "<br>"+"<b>" + json[0].org +"</b>")	
                .style("left", (d3.event.pageX) + "px")	
                .style("opacity","0.8")		
                .style("top", (d3.event.pageY - 28) + "px");
                
            })					
        .on("mouseout", function(d) {		
            div.transition()		
                .duration(500)		
                .style("opacity", 0);	
        });
        
	console.log(json[0])
    //append the arcs
    arcGroup.selectAll(".arc")
        .data(links)
        .enter()
        .append("path")
        .attr({ "class": "arc" })
        .attr({ d: path })
        .attr("no", function(d) { return d.no; })
        .style("fill","none")
        .style("stroke","#F2F8EA")
        .style("stroke-width","2px")
        .call(lineTransition); 
    	
};



