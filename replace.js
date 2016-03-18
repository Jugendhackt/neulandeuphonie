replace(document.body);
setTimeout(function () {
	replace(document.body);
}, 1000);
function replace(node) {
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "https://raw.githubusercontent.com/Jugendhackt/neulandeuphonie/master/tag_replace/de.json", true);
	xhr.onreadystatechange = function() {
	  if (xhr.readyState == 4) {
	    // JSON.parse does not evaluate the attacker's scripts.
	    var resp = JSON.parse(xhr.responseText);
	    walk(node, resp)
	  }
	}
	xhr.send();
}
function walk(node, replace)
{
	// Source: http://is.gd/mwZp7E

	var child, next;

	switch ( node.nodeType )
	{
		case 1:  // Element
		case 9:  // Document
		case 11: // Document fragment
			child = node.firstChild;
			while ( child )
			{
				next = child.nextSibling;
				walk(child, replace);
				child = next;
			}
			break;

		case 3: // Text node
			handleText(node, replace);
			break;
	}
}

function handleText(textNode, replace)
{
	var v = textNode.nodeValue;
	for (k in replace) {
		r = replace[k][Math.floor(Math.random() * replace[k].length)];
		v = v.replace(k, r);
	}
	textNode.nodeValue = v;
}
