console.log("Hello World!");

$.getJSON( "http://couchdb.pajowu.de/neulandeuphonie/_design/api/_view/count_host_word_replacements?group_level=1" , function(data){ 
	console.log(data);
	var table = $("table.wortUrl");
	$.each(data.rows, function(index, entry){
		var row = $("<tr><td>"+entry.key+"</td><td>"+entry.value+"</td></tr>");
		table.append(row);
	})
	
})

$.getJSON( "http://couchdb.pajowu.de/neulandeuphonie/_design/api/_view/count_word_replacements?group_level=1" , function(data){ 
	console.log(data);
	var table = $("table.wortAnzahl");
	$.each(data.rows, function(index, entry){
		var row = $("<tr><td>"+entry.key+"</td><td>"+entry.value+"</td></tr>");
		table.append(row);
	})
	
})
