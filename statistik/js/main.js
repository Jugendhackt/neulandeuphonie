var waiting = false;
function refreshStats() {
	$.getJSON("http://couchdb.pajowu.de/neulandeuphonie/_design/api/_view/count_host_word_replacements?group_level=1", function(data){
		$.each(data.rows, function(index, entry){
			//split key into parts seperated at points
			var hn = entry.key[0].split('.').reverse();
			var hostname = hn[1] + "." + hn[0];
			//check if hostname is a ip
			if (!/[0-9]/.test(hn[0].charAt(0))) entry.key[0] = hostname;
		})

		//make new table with all same keys summarized
		var newObj = {};
		for(i in data.rows){
 			var item = data.rows[i];
    			if(newObj[item.key[0]] === undefined) newObj[item.key[0]] = 0;
   			newObj[item.key[0]] += item.value;
		}

		var result = {};
		result.rows = [];
		for(i in newObj) result.rows.push({'key':i,'value':newObj[i]});


		//sort table
		result.rows.sort(function(a,b){return b.value-a.value})
		//make new data for d3 chart
		var chart = {
			     "name": "hostname",
			     "children": [
			     ]};
		var nOfEntry = 0;
		var valueOfEntry = 0;
		for (i in newObj) {
			nOfEntry += 1;
			valueOfEntry += newObj[i];
		}
		var minInclude = valueOfEntry / nOfEntry * 0.5;
		for (i in newObj) {
			if (newObj[i] >= minInclude) chart.children.push({'name':i,'size':newObj[i]});
		}

		//draw d3 chart
		var diameter = $("div#wortUrlContent").width(),
		format = d3.format(",d"),
    		color = d3.scale.category20c();
		var bubble = d3.layout.pack()
    			.sort(null)
    			.size([diameter,diameter])
			.padding(1.5);
		var svg = d3.select("div#wortUrlContent").append("svg")
			.attr("width", diameter)
			.attr("height", diameter)
			.attr("class", "bubble");

		var node = svg.selectAll(".node")
			.data(bubble.nodes(classes(chart))
			.filter(function(d) { return !d.children; }))
			.enter().append("g")
			.attr("class", "node")
			.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

		node.append("title")
			.text(function(d) { return d.className + ": " + format(d.value); });

		node.append("circle")
			.attr("r", function(d) { return d.r; })
			.style("fill", function(d) { return color(d.packageName); });

		node.append("text")
			.attr("dy", ".5em")
			.style("text-anchor", "middle")
			.text(function(d) { return d.className.substring(0, d.r / 3); });

		// Returns a flattened hierarchy containing all leaf nodes under the root.
		function classes(chart) {
			var classes = [];

			function recurse(name, node) {
				if (node.children) node.children.forEach(function(child) { recurse(node.name, child); });
				else classes.push({packageName: name, className: node.name, value: node.size});
			}

			recurse(null, chart);
			return {children: classes};
		}

		d3.select(self.frameElement).style("height", diameter + "px");
		})

	$.getJSON( "http://couchdb.pajowu.de/neulandeuphonie/_design/api/_view/count_word_replacements?group_level=1" , function(data){ 
		
		var table = $("table#wortAnzahlContent");
		table.empty();
		var valueCount = 0;
		data.rows.sort(function(a,b){return b.value-a.value})
		$.each(data.rows, function(index, entry){
			valueCount = valueCount + entry.value
			var row = $("<tr><td>"+entry.key+"</td><td>"+entry.value+"</td></tr>");
			table.append(row);
		})
		var row = $("<tr style=\"border-top: 1px solid #000;\"><td>Gesamt</td><td>"+valueCount+"</td></tr>");
		table.append(row);
	})
}

refreshStats();
$(window).scroll(function() {
    var windscroll = $(window).scrollTop();

    if (windscroll >= 200) {
        
        $('.content .pad-section').each(function(i) {
            if ($(this).position().top <= windscroll) {
                $('.nav li.active').removeClass('active');
                $('.nav li').eq(i).addClass('active');
            }
        });

    } else {

        $('nav').removeClass('fixed');
        $('nav a.active').removeClass('active');
        $('nav a:first').addClass('active');
    }

}).scroll();

$('body').delegate('nav a', 'click', function(){
  	event.preventDefault();
    $('html,body').stop().animate({
          scrollTop: $($(this).attr('href')).offset().top - $("nav")[0].getBoundingClientRect().bottom
        }, 500, 'easeInOutCubic');
        
});