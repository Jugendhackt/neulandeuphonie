console.log("Hello World!");
function refreshStats() {
	$.getJSON( "http://couchdb.pajowu.de/neulandeuphonie/_design/api/_view/count_host_word_replacements?group_level=1" , function(data){ 
		console.log(data);
		var table = $("table.wortUrl");
		var valueCount = 0;
		data.rows.sort(function(a,b){return b.value-a.value})
		$.each(data.rows, function(index, entry){
			valueCount = valueCount + entry.value
			var row = $("<tr><td>"+entry.key+"</td><td>"+entry.value+"</td></tr>");
			table.append(row);
		})
		var row = $("<tr><td></td><td><hr/></td></tr>		<tr><td>Gesamt</td><td>"+valueCount+"</td></tr>");
		table.append(row);
		
	})

	$.getJSON( "http://couchdb.pajowu.de/neulandeuphonie/_design/api/_view/count_word_replacements?group_level=1" , function(data){ 
		console.log(data);
		var table = $("table.wortAnzahl");
		var valueCount = 0;
		data.rows.sort(function(a,b){return b.value-a.value})
		$.each(data.rows, function(index, entry){
			valueCount = valueCount + entry.value
			var row = $("<tr><td>"+entry.key+"</td><td>"+entry.value+"</td></tr>");
			table.append(row);
		})
		var row = $("<tr><td></td><td><hr/></td></tr>		<tr><td>Gesamt</td><td>"+valueCount+"</td></tr>");
		table.append(row);
	})
};
//check for browser support
if(typeof(EventSource)!=="undefined") {
	//create an object, passing it the name and location of the server side script
	var eSource = new EventSource("http://couchdb.pajowu.de/neulandeuphonie/_changes?filter=api/statistic&feed=");
	//detect message receipt
	eSource.onmessage = function(event) {
		//write the received data to the page
		refreshStats();
	};
}
else {
	document.getElementById("serverData").innerHTML="Whoops! Your browser doesn't receive server-sent events.";
}

refreshStats();