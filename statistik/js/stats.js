console.log("Hello World!");

$.getJSON( "./json/wortUrl.json" , function(data){ 
	console.log(data);
	var table = $("table.wortUrl");
	$.each(data, function(url, wortObject){
		var anzahlGesamt = 0;
		$.each(wortObject, function(wort, anzahl){
			anzahlGesamt = anzahlGesamt + anzahl;
		})
		var row = $("<tr></tr>");
		row.append($("<td></td>").text(url));
		row.append($("<td></td>").text(anzahlGesamt));
		table.append(row);
	})
	
})

$.getJSON( "./json/wortAnzahl.json" , function(data){ 
	console.log(data);
	var table = $("table.wortAnzahl");
	$.each(data, function(wort, anzahl){
		var row = $("<tr><td>"+wort+"</td><td>"+anzahl+"</td></tr>");
		table.append(row);
	})
	
})
