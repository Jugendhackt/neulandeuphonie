// sometimes
setTimeout(function () {
	replace(document.body);
}, 5000);
window.onload = function(e){
	replace(document.body);
    // replace again after 10 secs to find JS-Loaded content
    setTimeout(function () {
		replace(document.body);
	}, 10000);
}
var replace_data = null;
function replace(node) {
	if (replace_data == null) {
		var xhr = new XMLHttpRequest();
		xhr.open("GET", "https://raw.githubusercontent.com/Jugendhackt/neulandeuphonie/master/tag_replace/de.json", true);
		xhr.onreadystatechange = function() {
		  if (xhr.readyState == 4) {
		    // JSON.parse does not evaluate the attacker's scripts.
		    replace_data = JSON.parse(xhr.responseText);
		    walk(node);
		  }
		}
		xhr.send();
	} else {
		walk(node);
	}
}
function walk(node)
{
	// Source: http://is.gd/mwZp7E

	var child, next;

	switch ( node.nodeType )
	{
		case 1:  // Element
			if (node.tagName === 'IMG') {

				width = node.clientWidth;
				height = node.clientHeight;
				if (width > 0 && height > 0) {
					node.removeAttribute("src");
					node.width = width;
					node.height = height;
					node.setAttribute("class","neulandeuphonie-censored");
				}
			}
		case 9:  // Document
		case 11: // Document fragment
			child = node.firstChild;
			while ( child )
			{
				next = child.nextSibling;
				walk(child, replace_data);
				child = next;
			}
			break;

		case 3: // Text node
			handleText(node, replace_data);
			break;
	}
}

function wrapCensor(a, b){
    return '<span class="neulandeuphonie-censored">' + a + '</span>';
}

function handleText(textNode)
{
	var v = textNode.nodeValue;
	var changed = false;
	for (k in replace_data) {
		r = replace_data[k][Math.floor(Math.random() * replace_data[k].length)];
		m = v.match(k);
		if (m != undefined) {
			v = v.replace(k, wrapCensor);
			changed = true;

		}
	}
	if (changed) {
		textNode.parentNode.innerHTML = v;
	}
}
