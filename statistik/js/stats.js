console.log("Hello World!");

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
